from io import BytesIO
import importlib.util
from pathlib import Path
from PIL import Image, ImageDraw

spec = importlib.util.spec_from_file_location('gen', Path(__file__).resolve().parents[1] / 'scripts' / 'generate_slide_assets.py')
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)


def test_blob_sha():
    assert gen.git_blob_sha(b'hello\n') == 'ce013625030ba8dba906f756967f9e9ca394464a'


def test_image_shape():
    asset = {'aspect_ratio': 2.363128}
    assert gen.api_size(asset) == '2384x1008'


def test_true_alpha_valid():
    im = Image.new('RGBA', (2384, 1008), (255, 255, 255, 0))
    ImageDraw.Draw(im).rectangle((110,100,2200,900), fill=(65,65,158,255))
    b = BytesIO(); im.save(b, 'PNG')
    g = gen.rgba_check(b.getvalue(), 2.363128)
    assert g['G03'] and g['G04_geometry']
    v = {x: True for x in gen.QC_SCHEMA['required'] if x != 'notes'}
    v['notes'] = 'okay'
    assert gen.qc_pass(g, v)
    v['required_meaning_present'] = False
    assert not gen.qc_pass(g, v)


def test_rgba_but_opaque_rejected():
    im = Image.new('RGBA', (2384, 1008), (245,245,245,255))
    b=BytesIO();im.save(b,'PNG')
    g=gen.rgba_check(b.getvalue(),2.363128)
    assert not g['G03']


def test_wrong_aspect_rejected():
    im = Image.new('RGBA', (1536,1024), (0,0,0,0))
    ImageDraw.Draw(im).rectangle((100,100,1400,900), fill=(50,50,50,255))
    b=BytesIO(); im.save(b,'PNG')
    assert not gen.rgba_check(b.getvalue(),2.363128)['G04_geometry']