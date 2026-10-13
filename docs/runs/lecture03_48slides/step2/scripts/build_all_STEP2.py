from __future__ import annotations
import re, json, hashlib, copy, math, os, textwrap
from pathlib import Path
from collections import defaultdict
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN, MSO_AUTO_SIZE

ROOT=Path('/mnt/data/lecture03_step2/production');ROOT.mkdir(parents=True,exist_ok=True)
SOURCE=Path('/mnt/data/lecture03_p1_source/lecture03_48_slide_contents.md')
src=SOURCE.read_text(encoding='utf-8-sig')
ms=list(re.finditer(r'^## スライド (\d{2})：(.+)$',src,re.M))
assert len(ms)==48
W,H=10.0,7.5
IND=RGBColor(65,65,158);TXT=RGBColor(48,50,59);SUB=RGBColor(85,91,106)
LINE=RGBColor(216,220,229);LAV=RGBColor(245,245,251);PALE=RGBColor(243,244,246);WHITE=RGBColor(255,255,255);BLUE=RGBColor(23,155,211)
FONT='源真ゴシックP'

# Parse source blocks exactly (everything including newlines).
def section(s,name):
 m=re.search(r'^### '+re.escape(name)+r'\s*\n(.*?)(?=^### |^---\s*$|\Z)',s,re.M|re.S)
 return m.group(1).strip() if m else ''
def dequote(s):
 lines=[]
 for x in s.splitlines():
  if x.startswith('> '):lines.append(x[2:])
  elif x=='>':lines.append('')
 return '\n'.join(lines).strip()
def elements(s):
 marker=list(re.finditer(r'^\*\*要素(\d{2})｜([^\n*]+)\*\*$',section(s,'本文・図中ラベル（原文保持）'),re.M))
 part=section(s,'本文・図中ラベル（原文保持）')
 out=[]
 for i,m in enumerate(marker):
  sub=part[m.end():(marker[i+1].start() if i+1<len(marker) else len(part))]
  raw=dequote(sub)
  hints=re.search(r'参考位置 x=(\d+)%, y=(\d+)%, 幅=(\d+)%, 高さ=(\d+)%',m.group(2))
  out.append(dict(index=int(m.group(1)),text=raw,reference=tuple(int(v) for v in hints.groups()) if hints else None,meta=m.group(2)))
 return out
records=[]
for i,m in enumerate(ms):
 end=ms[i+1].start() if i+1<len(ms) else src.index('## 生成後の内容一致チェック',m.end())
 part=src[m.end():end]
 records.append(dict(n=i+1,title=dequote(section(part,'タイトル')),intro=dequote(section(part,'補足コンテキスト（Intro原文）')),take=dequote(section(part,'キーメッセージ（Takeaway）')),els=elements(part),table=section(part,'表データ（セル単位で厳密に保持）'),diagram=section(part,'図解・レイアウトの指示（スライド固有）')))

def base(slide,rec):
 n=rec['n']
 if n==1:return
 textbox(slide,rec['title'],.46,.25,9.08,.61,(23.5 if n==26 else (27 if len(rec['title'])>22 else 30)),IND,True,'title')
 intro=rec['intro']
 if intro and not intro.startswith('（元原稿'):
  textbox(slide,intro,.49,.96,9.05,.87,20.4,TXT,False,'intro')
 take=rec['take']
 if take and not take.startswith('（なし'):
  if n in (4,26):
   box(slide,.49,6.13,9.02,1.12,WHITE,IND,1.35)
   textbox(slide,take,.66,6.20,8.68,.99,18.0,IND,True,'takeaway',PP_ALIGN.CENTER)
  else:
   box(slide,.49,6.42,9.02,.83,WHITE,IND,1.35)
   textbox(slide,take,.66,6.48,8.68,.71,(17.8 if len(take)>68 else 19.6 if len(take)>48 else 21.3),IND,True,'takeaway',PP_ALIGN.CENTER)

def box(s,x,y,w,h,fill=WHITE,line=None,lw=.8,round=False):
 sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round else MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h));sh.fill.solid();sh.fill.fore_color.rgb=fill
 if line:sh.line.color.rgb=line;sh.line.width=Pt(lw)
 else:sh.line.fill.background()
 return sh

def textbox(s,content,x,y,w,h,sz=17,color=TXT,bold=False,role='body',align=PP_ALIGN.LEFT,fill=None,margin=.00):
 if not content:return None
 if fill is not None:box(s,x,y,w,h,fill,None)
 sh=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
 sh.name=f'EXACT_{role}'
 tf=sh.text_frame;tf.clear();tf.word_wrap=True;tf.auto_size=MSO_AUTO_SIZE.NONE
 tf.margin_left=Inches(margin);tf.margin_right=Inches(margin);tf.margin_top=Inches(.03 if sz>15 else .00);tf.margin_bottom=0
 for j,line in enumerate(content.split('\n')):
  p=tf.paragraphs[0] if j==0 else tf.add_paragraph();p.text=line;p.alignment=align;p.space_after=Pt(0)
  p.line_spacing=1.02
  for run in p.runs:
   run.font.name=FONT;run.font.size=Pt(sz);run.font.bold=bold;run.font.color.rgb=color
 return sh

def arrow(s,x1,y1,x2,y2,color=IND,w=1.6):
 c=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2));c.line.color.rgb=color;c.line.width=Pt(w)
 return c

def plain(s,content,x,y,w,h,sz=17,head=False,align=PP_ALIGN.LEFT):
 return textbox(s,content,x,y,w,h,sz,IND if head else TXT,head,'label' if head else 'body',align)

def draw_panel(s,x,y,w,h,heading=None,body=None,top=.25,fill=False,fs=16):
 if fill:box(s,x,y,w,h,LAV,None)
 if heading:plain(s,heading,x+.12,y+.1,w-.24,.47,19,True)
 if body:plain(s,body,x+.12,y+.61,w-.24,h-.72,fs)

def split_groups(s,rec,groups,orient='horizontal',style='plain'):
 # groups is list of [heading, body] EXACT copied from input element blocks.
 n=len(groups)
 if n==0:return
 if orient=='horizontal':
  gap=.22;wi=(9.0-(n-1)*gap)/n
  for i,(h,b) in enumerate(groups):
   x=.5+i*(wi+gap)
   if style=='light':box(s,x,2.0,wi,4.19,LAV,None)
   if h:plain(s,h,x+.08,2.1,wi-.16,.5,18,True,PP_ALIGN.CENTER if n>=3 else PP_ALIGN.LEFT)
   if b:plain(s,b,x+.1,2.78,wi-.20,3.25,15.3 if n>=3 else 17)
 else:
  gap=.20;hh=(4.28-(n-1)*gap)/n
  for i,(h,b) in enumerate(groups):
   y=2.0+i*(hh+gap)
   if h:plain(s,h,.62,y,3.05,.44,17.5,True)
   if b:plain(s,b,3.55,y,5.9,hh-.03,16.2)

IMG_SLOTS={5:['S05-A-01'],6:['S06-B-01','S06-B-02'],10:['S10-A-01'],11:['S11-B-01','S11-B-02','S11-B-03'],15:['S15-A-01'],17:['S17-A-01'],18:['S18-B-01','S18-B-02','S18-B-03'],26:['S26-B-01','S26-B-02','S26-B-03']}
SLOT_LABELS={'S06-B-01':'使い捨て型','S06-B-02':'進展型','S11-B-01':'プロダクトオーナー','S11-B-02':'スクラムマスター','S11-B-03':'開発者','S18-B-01':'ローコード','S18-B-02':'ノーコード','S18-B-03':'生成AI','S26-B-01':'ワイヤーフレーム','S26-B-02':'モックアップ','S26-B-03':'プロトタイプ'}
slots=[]
def place_slot(s,id,x,y,w,h):
 box(s,x,y,w,h,RGBColor(250,250,252),LINE,.8)
 textbox(s,id+'\n図素材をSTEP3で制作',x+.10,y+h*.47-.31,w-.2,.66,10.5,SUB,False,'placeholder',PP_ALIGN.CENTER)
 slots.append(dict(asset_id=id,slide_id=id[:3],x=round(x,3),y=round(y,3),width=round(w,3),height=round(h,3),aspect_ratio=round(w/h,6),units='inch',page_width=10,page_height=7.5,fit_mode='contain',source='verified PPTX physical shape bbox'))

def select(s,rec,idx):
 return '\n'.join(rec['els'][i-1]['text'] for i in idx if i<=len(rec['els']) and rec['els'][i-1]['text'])
def one(s,rec,idx,x,y,w,h,sz=16,head=False):
 return plain(s,rec['els'][idx-1]['text'],x,y,w,h,sz,head) if idx<=len(rec['els']) else None

# Semantic layouts, preserve all original elements as visible editable text when not redundant symbols.
def draw_illustrative(s,r):
 n=r['n'];ids=IMG_SLOTS[n];els=r['els']; body=[e['text'] for e in els]
 if len(ids)==1:
  # left article, right integrated visual
  content=body[0]
  if n==17:content=body[0]
  plain(s,content,.56,2.10,3.12,3.67,16.8)
  place_slot(s,ids[0],3.96,2.15,5.49,3.73)
  # exact accompanying annotation sentence retained below the diagram, without repeating diagram labels
  last=body[-1]
  if last and last not in ('↑','↓','→','↘','↙','←'):
   plain(s,last,3.99,5.90,5.46,.39,12.6)
  # diagram labels must be editable, keep explicit non-symbol labels with small transparent text outside/within margins
  inner=[e for e in body[1:-1] if e not in ('↑','↓','→','↘','↙','←')]
  if inner:
   txt='　/　'.join(inner)
   plain(s,txt,4.02,1.96,5.4,.30,11.8,True)
 else:
  count=len(ids);gap=.24;wi=(9.02-(count-1)*gap)/count
  labels=[SLOT_LABELS[i] for i in ids]
  if n==6:labels=[els[0]['text'],els[8]['text']]
  for j,aid in enumerate(ids):
   x=.49+j*(wi+gap)
   plain(s,labels[j],x+.04,2.04,wi-.08,.46,19.0,True,PP_ALIGN.CENTER)
   place_slot(s,aid,x+.08,2.65,wi-.16,1.39 if count==3 else 1.79)
   if n==11:
    idx=[1,3,5][j];paragraph=els[idx]['text']
   elif n==6:
    paragraph=els[1 if j==0 else 9]['text']
   elif n==18:
    paragraph=els[3 if j==0 else (5 if j==1 else 7)]['text']
   else:
    paragraph=els[1 if j==0 else (4 if j==1 else 7)]['text']
   plain(s,paragraph,x+.07,4.24 if count==3 else 4.62,wi-.15,1.42 if count==3 else 1.02,13.1 if count==3 else 14.5)
  if n==11:plain(s,els[-1]['text'],.57,5.76,8.90,.52,12.5)
  if n==18:
   plain(s,els[1]['text'],.65,1.90,8.7,.37,14.3,True)
   plain(s,els[0]['text'],.55,5.76,4.45,.56,11.9)
   plain(s,els[-1]['text'],5.03,5.76,4.40,.56,12.3)
  if n==26:plain(s,els[-1]['text'],.57,5.52,8.88,.55,12.3)
  if n==26:
   for j,index in enumerate([2,5,9]):
    plain(s,els[index]['text'],.52+j*3.05,5.08,2.84,.36,11.8)
   plain(s,els[8]['text'],6.54,4.88,2.87,.22,11.5)
  if n==6:
   plain(s,'進め方',.72,5.61,3.88,.22,12.5,True)
   plain(s,'試作 → 廃棄 → 本開発',.72,5.83,3.88,.35,13.0,True)
   plain(s,'進め方',5.31,5.61,3.88,.22,12.5,True)
   plain(s,'試作 → 改良 → 完成',5.31,5.83,3.88,.35,13.0,True)

def draw_table(s,r):
 n=r['n'];raw=r['table'];rows=[]
 for line in raw.splitlines():
  if line.startswith('|'):
   vals=[x.strip() for x in line.strip().strip('|').split('|')]
   if all(re.fullmatch(r'[:\- ]+',v) for v in vals):continue
   rows.append(vals)
 assert rows and n in [9,35,37],n
 nr=len(rows);nc=len(rows[0]);
 if n==35:y=2.0;h=3.64; font=12.8
 elif n==9:y=2.0;h=3.54;font=13.8
 else:y=2.09;h=3.48;font=15.0
 shape=s.shapes.add_table(nr,nc,Inches(.52),Inches(y),Inches(8.98),Inches(h));t=shape.table
 for ci in range(nc):
  if n==35:t.columns[ci].width=Inches([2.50,3.06,3.42][ci]);
  elif n==9:t.columns[ci].width=Inches([2.2,2.35,2.25,2.18][ci]);
  else:t.columns[ci].width=Inches([5,3.98][ci]);
 for ri,row in enumerate(rows):
  for ci,value in enumerate(row):
   c=t.cell(ri,ci);c.text=value;c.margin_left=Inches(.08);c.margin_right=Inches(.08);c.margin_top=Inches(.04);c.margin_bottom=Inches(.01)
   c.fill.solid();c.fill.fore_color.rgb=LAV if ri==0 else WHITE
   c.vertical_anchor=MSO_ANCHOR.MIDDLE
   for p in c.text_frame.paragraphs:
    for run in p.runs:run.font.name=FONT;run.font.size=Pt(15 if ri==0 else font);run.font.bold=(ri==0);run.font.color.rgb=IND if ri==0 else TXT
 # auxiliary content (if present)
 aux='\n'.join(e['text'] for e in r['els'])
 if aux:plain(s,aux,.62,5.73,8.78,.61,12.8)

def draw_cover(s,r):
 plain(s,r['els'][0]['text'],1.43,.65,7.16,.5,17)
 plain(s,r['els'][1]['text'],1.4,1.59,7.2,.56,24,True,PP_ALIGN.CENTER)
 plain(s,r['title'],.48,2.65,9.05,.94,38,True,PP_ALIGN.CENTER)
 plain(s,r['els'][2]['text'],1.0,4.13,8,.56,21)
 plain(s,r['els'][3]['text'],1.0,5.27,8,.48,18)
 plain(s,r['els'][4]['text'],.7,6.32,8.7,.46,15)

def draw_goal(s,r):
 # five learning goals and four-stage progress as real editable nodes
 E=[e['text'] for e in r['els']]
 plain(s,E[0],.55,2.11,4.8,.48,20,True)
 plain(s,E[1],.68,2.70,5.35,3.38,17.2)
 plain(s,E[2],6.38,2.12,3.02,.47,20,True)
 for j,idx in enumerate([3,5,7,9]):
  y=2.80+j*.78
  box(s,6.41,y,2.84,.57,LAV,None)
  plain(s,E[idx],6.52,y+.08,2.62,.38,17.6,True,PP_ALIGN.CENTER)
  if j<3:arrow(s,7.82,y+.57,7.82,y+.79)

def draw_exact_placement(s,r):
 # Original PPTX-derived fractional relative positions, shifted/squeezed to avoid header/Takeaway.
 # Each original element stays in an editable text object, no content is removed.
 els=r['els']; n=r['n']
 for e in els:
  text=e['text'];ref=e['reference']
  if not text:continue
  if ref:
   x,y,w,h=ref
   X=max(.45,min(9.50,.15+x*.096))
   Y=max(2.03,min(6.25,1.96+(y-25)*.084))
   width=max(.36,min(9.55-X,w*.098))
   height=max(.27,min(6.36-Y,max(h*.075,.30)))
  else:X,Y,width,height=.7,2.1,8.6,.6
  # Arrow symbol exact as connector or drawn arrow text
  is_arrow=text.strip() in ['→','↓','↑','←','↘','↙']
  if is_arrow:
   textbox(s,text,X,Y,max(.31,width),.27,15.2,IND,True,'diagram_arrow',PP_ALIGN.CENTER);continue
  # infer size based on element width / length / intended number of lines
  nch=len(text);nline=max(1,len(text.splitlines()))
  if nch<=14 and nline==1:fs=15.1 if width>1 else 12.8
  elif nch<38 and nline<=2:fs=15.0 if width>2.5 else 12.5
  else:fs=13.5 if width>3.0 else 11.5
  # font size upper cap from vertical geometry
  height=max(height,min(.70,nline*.19+.04))
  textbox(s,text,X,Y,width,height,fs,IND if nch<=14 and nline==1 else TXT,nch<=14 and nline==1,'original_element')

import clean_layouts
clean_layouts.configure(globals())

def native_simple(s,r):
 return clean_layouts.draw(s,r)

def archived_native_simple(s,r):
 """Produces an editable *visual* main structure from non-icon labels and keeps exact original labels.
 Adapt typical horizontal/vertical flow or side-by-side comparisons.
 """
 els=r['els'];n=r['n'];texts=[e['text'] for e in els]
 if n in [3,4,19,24,31,40]:
  # parent panels/rows with text pairs. Use left-to-right relationship and retain all source blocks.
  group=[]
  if n==3:
   group=[(texts[3],texts[4]),(texts[5],texts[6]),(texts[7],texts[8]),(texts[9],texts[10])]
   left='\n'.join(texts[:2]);plain(s,left,.57,2.18,4.11,3.55,15.0)
   y0=2.06
   for j,(label,detail) in enumerate(group):
    y=y0+j*.81
    plain(s,label,5.00,y,2.31,.37,15.4,True)
    plain(s,detail,7.42,y,2.11,.37,14.4)
   if texts[11]:plain(s,texts[11],5.00,5.49,4.39,.60,12.8)
   return
  if n==4:
   group=[(texts[0],texts[1]),(texts[2],texts[3]),(texts[4],texts[5])]
   split_groups(s,r,group,style='plain')
   plain(s,' '.join(texts[6:]),.68,5.92,8.77,.43,13.0)
   return
  if n==19:
   group=[(' '.join(texts[j:j+1]),'\n'.join(texts[j+1:j+3])) for j in (0,3,6)]
   split_groups(s,r,group)
   plain(s,texts[9],.62,5.98,8.77,.38,14.0)
   return
  if n==24:
   split_groups(s,r,[(texts[0],texts[1]),(texts[2],texts[3]),(texts[4],texts[5])])
   plain(s,texts[6]+'\n'+texts[7],.64,5.79,8.75,.56,12.5)
   return
  if n==31:
   split_groups(s,r,[(texts[0],texts[1]+'\n'+texts[2]),(texts[3],texts[4]+'\n'+texts[5]),(texts[6],texts[7]+'\n'+texts[8])])
   plain(s,texts[9],.63,5.92,8.78,.4,13.0)
   return
  if n==40:
   split_groups(s,r,[(texts[1],texts[2]),(texts[4],texts[5]),(texts[7],texts[8]),(texts[10],texts[11])],orient='vertical')
   plain(s,texts[12],.66,6.1,8.74,.27,12.0);return
 # For other pages use spatial layout based on original, but text exact in editable objects.
 draw_exact_placement(s,r)

prs=Presentation();prs.slide_width=Inches(W);prs.slide_height=Inches(H)
# Preserve approved S01/S02 checkpoint exactly, since tested and already persisted.
checkpoint=Presentation('/mnt/data/lecture03_step2/checkpoints/lecture03_STEP2_checkpoint_S01-S02_v1.pptx')
assert len(checkpoint.slides)==2
for old in checkpoint.slides:
 slide=prs.slides.add_slide(prs.slide_layouts[6])
 for shape in old.shapes:
  slide.shapes._spTree.insert_element_before(copy.deepcopy(shape.element),'p:extLst')

for r in records[2:]:
 slide=prs.slides.add_slide(prs.slide_layouts[6]);base(slide,r)
 if r['n'] in IMG_SLOTS:draw_illustrative(slide,r)
 elif r['n'] in (9,35,37):draw_table(slide,r)
 else:native_simple(slide,r)

assert len(prs.slides)==48
path=ROOT/'lecture03_48_step2_skeleton_draft.pptx';prs.save(path)
(ROOT/'asset_slots_15.json').write_text(json.dumps(slots,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'slide_source_inventory.json').write_text(json.dumps([{k:(v if k!='els' else [{'index':e['index'],'text':e['text'],'reference':e['reference']} for e in v]) for k,v in r.items()} for r in records],ensure_ascii=False,indent=2),encoding='utf-8')

# create batch PPTXs based on same slide elements, source exact deck snapshot
for i in range(8):
 batch=Presentation();batch.slide_width=Inches(W);batch.slide_height=Inches(H)
 for old in list(prs.slides)[i*6:(i+1)*6]:
  slide=batch.slides.add_slide(batch.slide_layouts[6]);
  for shape in old.shapes:slide.shapes._spTree.insert_element_before(copy.deepcopy(shape.element),'p:extLst')
 batch.save(ROOT/f'B{i+1:02d}_S{i*6+1:02d}-S{(i+1)*6:02d}_draft.pptx')
print(json.dumps({'slides':len(prs.slides),'slots':len(slots),'batch_pptx':8,'deck_bytes':path.stat().st_size,'paths':str(ROOT)},ensure_ascii=False))