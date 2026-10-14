from pathlib import Path
import io
import sys
import unittest
from PIL import Image

sys.path.insert(0,str(Path(__file__).resolve().parent))
from scripts.p3_slide_context import SlideContext, BUNDLE, CHECKSUM

bundle=BUNDLE
sha=CHECKSUM

class ContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context=SlideContext(bundle,sha)

    def test_actual_pptx_all_placeholders(self):
        slots=[
            ('S05-A-01','S05',3.96,2.15,5.49,3.73),
            ('S06-B-01','S06',0.57,2.65,4.23,1.79),
            ('S06-B-02','S06',5.20,2.65,4.23,1.79),
            ('S10-A-01','S10',3.96,2.15,5.49,3.73),
            ('S11-B-01','S11',0.57,2.65,2.687,1.39),
            ('S11-B-02','S11',3.657,2.65,2.687,1.39),
            ('S11-B-03','S11',6.743,2.65,2.687,1.39),
            ('S15-A-01','S15',3.96,2.15,5.49,3.73),
            ('S17-A-01','S17',3.96,2.15,5.49,3.73),
            ('S18-B-01','S18',0.57,2.65,2.687,1.39),
            ('S18-B-02','S18',3.657,2.65,2.687,1.39),
            ('S18-B-03','S18',6.743,2.65,2.687,1.39),
            ('S26-B-01','S26',0.57,2.65,2.687,1.39),
            ('S26-B-02','S26',3.657,2.65,2.687,1.39),
            ('S26-B-03','S26',6.743,2.65,2.687,1.39),
        ]
        for id,sid,x,y,w,h in slots:
            with self.subTest(id=id):
                a={'asset_id':id,'slide_id':sid,'placeholder_bbox_in':dict(x=x,y=y,width=w,height=h)}
                self.assertEqual(self.context.slide_and_box(a)[0],sid)
                self.assertEqual(len(self.context.edit_inputs(a)),2)

    def test_preview_composition(self):
        a={'asset_id':'S06-B-02','slide_id':'S06','placeholder_bbox_in':dict(x=5.20,y=2.65,width=4.23,height=1.79)}
        im=Image.new('RGBA',(2384,1008),(0,0,0,0))
        from PIL import ImageDraw
        ImageDraw.Draw(im).ellipse((400,200,1984,808),fill='#41419E')
        b=io.BytesIO();im.save(b,format='PNG')
        result=self.context.compose(a,b.getvalue())
        out=Image.open(io.BytesIO(result))
        self.assertEqual(out.size,(960,720))
        self.assertEqual(out.mode,'RGB')
        self.assertEqual(self.context.trace(a)['source_pptx_sha256'],
            '989a2a25a9469c8d3777289430ab415bd2d5f9636dbf0d969c10c7c1f0406506')

    def test_invalid_marker_rejected(self):
        a={'asset_id':'S06-B-99','slide_id':'S06','placeholder_bbox_in':dict(x=5.2,y=2.65,width=4.23,height=1.79)}
        with self.assertRaises(ValueError):self.context.slide_and_box(a)

if __name__=='__main__':unittest.main()