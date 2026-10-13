from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pathlib import Path
import json,hashlib

OUT=Path('/mnt/data/lecture03_step2/checkpoints')
prs=Presentation(); prs.slide_width=Inches(10); prs.slide_height=Inches(7.5)
BLANK=prs.slide_layouts[6]
WHITE=RGBColor(255,255,255); IND=RGBColor(65,65,158); DARK=RGBColor(48,50,59); GRAY=RGBColor(85,91,106); LIGHT=RGBColor(216,220,229); LAV=RGBColor(245,245,251)
FONT='源真ゴシックP'

def shape_rect(s,x,y,w,h,fill=WHITE,line=None,line_width=1.0):
    sh=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb=fill
    if line:
        sh.line.color.rgb=line;sh.line.width=Pt(line_width)
    else:sh.line.fill.background()
    return sh

def add_text(s,content,x,y,w,h,size=18,color=DARK,bold=False,align=PP_ALIGN.LEFT,margin=0.0,line_spacing=None):
    sh=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=sh.text_frame;tf.clear();tf.word_wrap=True
    tf.margin_left=Inches(margin); tf.margin_right=Inches(margin);tf.margin_top=Inches(.01);tf.margin_bottom=Inches(0)
    for k,line in enumerate(content.split('\n')):
        p=tf.paragraphs[0] if k==0 else tf.add_paragraph();p.text=line
        p.alignment=align;p.font.name=FONT;p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=color
        if line_spacing:p.line_spacing=line_spacing
        p.space_after=Pt(0)
    return sh

def add_base(title,intro,takeaway):
    s=prs.slides.add_slide(BLANK)
    shape_rect(s,0,0,10,7.5)
    add_text(s,title,.52,.22,8.95,.53,32,IND,True)
    add_text(s,intro,.54,1.02,8.92,1.08,22,DARK)
    shape_rect(s,.49,6.25,9.02,1.02,WHITE,IND,1.3)
    add_text(s,takeaway,.71,6.34,8.58,.85,24,IND,True,PP_ALIGN.CENTER)
    return s

# 01 cover: no Intro or Takeaway, original year and labels unchanged.
s=prs.slides.add_slide(BLANK);shape_rect(s,0,0,10,7.5)
add_text(s,'明治大学 理工学部 情報科学科 ／ 2025年度',.6,.72,8.8,.45,18,GRAY,False,PP_ALIGN.CENTER)
add_text(s,'「情報システム論」第3回',.5,1.68,9,.55,24,IND,True,PP_ALIGN.CENTER)
add_text(s,'ソフトウェア開発',.48,2.67,9.04,1.08,43,IND,True,PP_ALIGN.CENTER)
add_text(s,'開発手法から具体的な設計技術へ',.6,4.22,8.8,.57,23,DARK,False,PP_ALIGN.CENTER)
add_text(s,'システム開発技術（2） ／ 100分講義（全48枚）',.4,5.35,9.2,.52,19,DARK,False,PP_ALIGN.CENTER)
add_text(s,'FE（基本情報技術者試験）対策として，定義・分類・具体例を丁寧に扱う．',.38,6.16,9.24,.49,17,GRAY,False,PP_ALIGN.CENTER)

# 02 goals and flow: exact text, editable elements.
s=add_base('本日の達成目標','第2回では，開発プロセスの全体像を学んだ．\n今回は，開発手法と具体的な設計技術を学ぶ．','開発の進め方から，実装に必要な設計へ．\nまず，前回の内容を振り返る．')
add_text(s,'到達目標',.55,2.36,5.7,.52,22,IND,True)
goals=['代表的な開発手法を比較できる．','外部設計の内容を説明できる．','コード設計と入力チェックを理解する．','論理設計と物理設計を区別できる．','内部設計の役割を説明できる．']
for j,line in enumerate(goals):
    cy=3.08+j*.59
    shape_rect(s,.65,cy+.18,.075,.075,IND)
    add_text(s,line,.88,cy,5.38,.44,18,DARK)
add_text(s,'本日の流れ',6.38,2.36,2.95,.53,22,IND,True,PP_ALIGN.CENTER)
for j,v in enumerate(['開発手法','外部設計','データ設計','内部設計']):
    y=3.10+j*.73
    shape_rect(s,6.86,y,1.99,.48,LAV)
    add_text(s,v,6.89,y+.03,1.93,.41,18,IND,True,PP_ALIGN.CENTER)
    if j<3:
        ln=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(7.85),Inches(y+.5),Inches(7.85),Inches(y+.70))
        ln.line.color.rgb=IND;ln.line.width=Pt(1.9)
        # arrowhead with native editable geometry, not an A/B illustration
        tri=s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW,Inches(7.77),Inches(y+.60),Inches(.16),Inches(.15))
        tri.fill.solid();tri.fill.fore_color.rgb=IND;tri.line.fill.background()

file=OUT/'lecture03_STEP2_checkpoint_S01-S02_v1.pptx'
prs.save(file)
sha=hashlib.sha256(file.read_bytes()).hexdigest()
res={'pages':[1,2],'slide_count':len(prs.slides),'image_objects':0,'native_tables':0,'sha256':sha,'size_bytes':file.stat().st_size,'font_name_requested':FONT,'render_font_validated':False,'qc_status':'PENDING_RENDER'}
(OUT/'checkpoint_S01-S02_metadata.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(res,ensure_ascii=False))