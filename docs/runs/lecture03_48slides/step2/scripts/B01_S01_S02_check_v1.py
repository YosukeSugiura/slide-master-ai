from pptx import Presentation
from pathlib import Path
import hashlib,json, shutil
from PIL import Image
p=Path('/mnt/data/lecture03_step2/checkpoints/lecture03_STEP2_checkpoint_S01-S02_v1.pptx')
r=Presentation(p)
required={1:["明治大学 理工学部 情報科学科 ／ 2025年度","「情報システム論」第3回","ソフトウェア開発","開発手法から具体的な設計技術へ","システム開発技術（2） ／ 100分講義（全48枚）","FE（基本情報技術者試験）対策として，定義・分類・具体例を丁寧に扱う．"],2:["本日の達成目標","第2回では，開発プロセスの全体像を学んだ．","今回は，開発手法と具体的な設計技術を学ぶ．","開発の進め方から，実装に必要な設計へ．","まず，前回の内容を振り返る．","到達目標","代表的な開発手法を比較できる．","外部設計の内容を説明できる．","コード設計と入力チェックを理解する．","論理設計と物理設計を区別できる．","内部設計の役割を説明できる．","本日の流れ","開発手法","外部設計","データ設計","内部設計"]}
page=[]
for i,slide in enumerate(r.slides,1):
 text='\n'.join(sh.text for sh in slide.shapes if sh.has_text_frame)
 missing=[x for x in required[i] if x not in text]
 fonts=set()
 for sh in slide.shapes:
  if sh.has_text_frame:
   for para in sh.text_frame.paragraphs:
    if para.text.strip():
     fonts.add(para.font.name or next((run.font.name for run in para.runs if run.font.name),None))
 page.append({'slide':i,'title':'ソフトウェア開発' if i==1 else '本日の達成目標','required_literals':len(required[i]),'missing_literals':missing,'editable_text':sum(sh.has_text_frame and bool(sh.text.strip()) for sh in slide.shapes),'images':sum(sh.shape_type==13 for sh in slide.shapes),'font_names':sorted(map(str,fonts)),'qc':'PASS_WITH_FONT_RENDERING_CAVEAT' if not missing and fonts=={'源真ゴシックP'} else 'FAIL'})
assert len(r.slides)==2 and all(x['qc'].startswith('PASS') for x in page),page
pdir=p.parent
shutil.copyfile(pdir/'render/S-1.png',pdir/'S01_preview.png')
shutil.copyfile(pdir/'render/VERIFY-2.png',pdir/'S02_preview.png')
im1=Image.open(pdir/'S01_preview.png').convert('RGB').resize((960,720));im2=Image.open(pdir/'S02_preview.png').convert('RGB').resize((960,720))
mont=Image.new('RGB',(1920,720),'white');mont.paste(im1,(0,0));mont.paste(im2,(960,0));mont.save(pdir/'checkpoint_S01-S02_overview.png')
meta={'pages':page,'PPTX_SHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'PPTX_BYTES':p.stat().st_size,'rendered_from_actual_pptx':True,'pdf_pages':2,'font_display':'substitute_Noto_Sans_CJK_JP','pass_gate':'STRUCTURE_AND_VISIBLE_LAYOUT_ONLY','batch_complete':False}
(pdir/'checkpoint_S01-S02_QC.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(meta,ensure_ascii=False,indent=2))