#!/usr/bin/env python3
"""Immutable, slide-aware reference bundle for P3 image generation.

The ZIP contains the actual editable STEP2 PPTX, reference slide renders and
accepted illustration-style exemplars. No LibreOffice is needed at runtime.
"""
from __future__ import annotations

import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
import zipfile

from PIL import Image, ImageDraw, ImageOps
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'docs/runs/lecture03_48slides/step3/reference/lecture03_p3_context.zip'
CHECKSUM = ROOT / 'docs/runs/lecture03_48slides/step3/reference/lecture03_p3_context.sha256'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def image_to_png(data: bytes) -> bytes:
    with Image.open(BytesIO(data)) as im:
        target = BytesIO()
        im.convert('RGB').save(target, format='PNG')
    return target.getvalue()


class SlideContext:
    def __init__(self, bundle: Path = BUNDLE, checksum: Path = CHECKSUM):
        self.bundle = bundle
        expected = checksum.read_text(encoding='utf-8').strip().split()[0]
        actual = digest(bundle.read_bytes())
        if expected != actual:
            raise ValueError('P3 reference bundle checksum mismatch')
        self.archive = zipfile.ZipFile(bundle)
        self.manifest = json.loads(self.archive.read('manifest.json'))
        if self.manifest.get('schema_version') != 'p3-slide-context-1':
            raise ValueError('Unsupported reference bundle')
        self.pptx = self._read(self.manifest['source']['pptx'])
        self.presentation = Presentation(BytesIO(self.pptx))
        if len(self.presentation.slides) != 48:
            raise ValueError('PPTX not 48 slides')
        self.slide_width = self.presentation.slide_width / 914400
        self.slide_height = self.presentation.slide_height / 914400
        if abs(self.slide_width - 10) > .001 or abs(self.slide_height - 7.5) > .001:
            raise ValueError('Unexpected PPTX canvas')

    def _read(self, entry: dict) -> bytes:
        name = entry['path']
        if '..' in Path(name).parts or Path(name).is_absolute():
            raise ValueError('Unsafe reference bundle path')
        data = self.archive.read(name)
        if digest(data) != entry['sha256'] or len(data) != entry['bytes']:
            raise ValueError(f'Corrupt P3 reference: {name}')
        return data

    def slide_and_box(self, asset: dict) -> tuple[str, dict]:
        asset_id = asset['asset_id']
        sid = asset['slide_id']
        if not re.fullmatch(r'S\d{2}', sid) or not asset_id.startswith(sid + '-'):
            raise ValueError('Malformed slide asset id')
        n = int(sid[1:])
        page = self.presentation.slides[n - 1]
        if not any(sh.has_text_frame and asset_id in sh.text for sh in page.shapes):
            raise ValueError(f'{asset_id} placeholder marker missing from PPTX')
        b = asset['placeholder_bbox_in']
        expected = (b['x'], b['y'], b['width'], b['height'])
        found = False
        for sh in page.shapes:
            actual = tuple(getattr(sh, a) / 914400 for a in ('left', 'top', 'width', 'height'))
            if all(abs(a-c) < .02 for a,c in zip(actual, expected)):
                found = True
                break
        if not found:
            raise ValueError(f'{asset_id} image insertion rectangle missing from PPTX')
        if sid not in self.manifest['slide_images']:
            raise ValueError(f'{sid} slide screenshot missing')
        return sid, b

    def page_png(self, asset: dict) -> bytes:
        sid, _ = self.slide_and_box(asset)
        return image_to_png(self._read(self.manifest['slide_images'][sid]))

    def style_png(self, asset: dict) -> bytes:
        # Keep style consistent within the same slide; otherwise use the accepted
        # S05 main illustration as global lecture baseline.
        refs = self.manifest['style_references']
        sibling = next((k for k in refs if k.startswith(asset['slide_id'] + '-') and k != asset['asset_id']), None)
        key = sibling or 'S05-A-01'
        if key not in refs:
            raise ValueError('Accepted illustration style reference missing')
        raw = self._read(refs[key])
        with Image.open(BytesIO(raw)) as im:
            out = BytesIO()
            im.convert('RGBA').save(out, format='PNG')
        return out.getvalue()

    def edit_inputs(self, asset: dict) -> list[tuple[str, BytesIO, str]]:
        sid, _ = self.slide_and_box(asset)
        return [
            (f'{sid}_full_slide_context.png', BytesIO(self.page_png(asset)), 'image/png'),
            ('accepted_illustration_style.png', BytesIO(self.style_png(asset)), 'image/png'),
        ]

    def compose(self, asset: dict, candidate: bytes) -> bytes:
        """Place the generated independent RGBA asset into its *actual* PPTX slot.

        This overlay is a visual QA artifact only; it never alters the source PPTX.
        """
        sid, box = self.slide_and_box(asset)
        raw = self._read(self.manifest['slide_images'][sid])
        with Image.open(BytesIO(raw)) as reference:
            page = reference.convert('RGBA')
        W, H = page.size
        scale_x, scale_y = W/self.slide_width, H/self.slide_height
        x0 = round(box['x'] * scale_x)
        y0 = round(box['y'] * scale_y)
        x1 = round((box['x']+box['width']) * scale_x)
        y1 = round((box['y']+box['height']) * scale_y)
        if not (0 <= x0 < x1 <= W and 0 <= y0 < y1 <= H):
            raise ValueError('PPTX slot outside slide canvas')
        # Leave the PPTX-drawn rectangle and shadow intact, erase only marker text.
        pad = max(2, round(min(W,H)/250))
        ImageDraw.Draw(page).rectangle((x0+pad, y0+pad, x1-pad, y1-pad), fill=(249,249,252,255))
        with Image.open(BytesIO(candidate)) as img:
            foreground = img.convert('RGBA')
        slot_width, slot_height = x1-x0-2*pad, y1-y0-2*pad
        foreground.thumbnail((slot_width, slot_height), Image.Resampling.LANCZOS)
        left = x0+pad+(slot_width-foreground.width)//2
        top = y0+pad+(slot_height-foreground.height)//2
        page.alpha_composite(foreground, (left, top))
        out = BytesIO()
        page.convert('RGB').save(out,format='PNG')
        return out.getvalue()

    def trace(self, asset: dict) -> dict:
        sid, box = self.slide_and_box(asset)
        entry = self.manifest['slide_images'][sid]
        return {
            'source_pptx_sha256':self.manifest['source']['pptx']['sha256'],
            'slide_id':sid,
            'slide_ref_sha256':entry['sha256'],
            'style_ref_sha256':digest(self.style_png(asset)),
            'placeholder_bbox_in':box,
            'reference_bundle_sha256':digest(self.bundle.read_bytes()),
        }