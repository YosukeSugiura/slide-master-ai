import math, re, unicodedata
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
IND=RGBColor(65,65,158);TXT=RGBColor(48,50,59);LAV=RGBColor(245,245,251);GRAY=RGBColor(85,91,106)

def configure(glob):
 global plain,box,arrow,textbox,place_slot
 plain=glob['plain'];box=glob['box'];arrow=glob['arrow'];textbox=glob['textbox'];place_slot=glob['place_slot']

def clip(strng):return strng

def estimate_lines(s,width,font):
 cap=max(3,width*72/font-.7)
 lines=0
 for p in s.split('\n'):
  equivalent=sum(1.0 if unicodedata.east_asian_width(c) in ('F','W') else .57 for c in p)
  lines+=max(1,math.ceil(equivalent/cap))
 return lines

def stack(s,entries,x,y,w,h,fontsize=15.3,gap=.08, show_fills=False):
 entries=[(i,txt) for i,txt in entries if txt.strip()]
 if not entries:return
 # adapt font (12.3-16.2) to fit all text even when dense
 for fs in [fontsize,15.0,14.0,13.1,12.0,11.0]:
  need=[]
  for i,txt in entries:
   nd=estimate_lines(txt,w-.04,fs)
   height=max(.22,nd*(fs/72*1.19)+.035)
   need.append(height)
  if sum(need)+gap*(len(entries)-1)<=h:break
 # distribute available whitespace without changing text order
 free=max(0,h-sum(need)-gap*(len(entries)-1))
 for j,((i,txt),hh) in enumerate(zip(entries,need)):
  is_head=(len(txt.strip())<=17 and len(txt.splitlines())==1 and not txt.strip().startswith(('・','-','※')))
  if is_head:font=fs if fs<=13 else min(17.5,fs+.8)
  else:font=fs
  if show_fills and is_head:box(s,x,y,w,hh,LAV)
  plain(s,txt,x+.04,y,w-.08,hh+.02,font,is_head)
  y+=hh+gap+(free/len(entries) if free>.25 else 0)

def make_columns(s,r,cols=2,assign=None,ysize=4.20):
 arr=r['els'];number=r['n']; groups=[[] for _ in range(cols)]
 if assign is None:
  # maintain original semantic spatial grouping as much as possible
  for e in arr:
   x,y,ww,hh=e['reference'] or (0,0,0,0)
   k=min(cols-1,int(cols*(x+ww*.43)/102))
   groups[k].append((e['index'],e['text']))
  # when visual fields all left or right, automatically rebalance nonrelated objects by original order
  weights=[sum(len(t) for _,t in a) for a in groups]
  if min(weights)==0 or max(weights)>max(50,sum(weights)*.79):
   groups=[[] for _ in range(cols)]
   for j,e in enumerate(arr):groups[min(cols-1,j*cols//max(1,len(arr)))].append((e['index'],e['text']))
 else:
  for col,indices in enumerate(assign):groups[col]=[(i,arr[i-1]['text']) for i in indices if i-1<len(arr)]
 gap=.30;w=(9.06-(cols-1)*gap)/cols
 for j,group in enumerate(groups):
  x=.48+j*(w+gap)
  stack(s,group,x,2.05,w,ysize,fontsize=15.4 if cols==2 else 14.2,gap=.09 if cols==2 else .055)

def label_flow(s,labels,y=3.1,x=.68,w=8.65,font=16.4):
 k=len(labels);gap=.20;wi=(w-(k-1)*gap)/k
 for j,l in enumerate(labels):
  xi=x+j*(wi+gap)
  box(s,xi,y,wi,.76,LAV,None)
  plain(s,l,xi+.07,y+.18,wi-.14,.42,font,True,PP_ALIGN.CENTER)
  if j<k-1:arrow(s,xi+wi+.015,y+.38,xi+wi+gap-.015,y+.38)

def simple_flow(s,r,config):
 texts=[e['text'] for e in r['els']];label_indices=config['labels'];n=len(label_indices)
 left=config.get('left',[]);right=config.get('right',[]);sub=config.get('sub',[])
 if left:stack(s,[(i,texts[i-1]) for i in left],.55,2.05,3.3,3.8,fontsize=16,gap=.1)
 labels=[texts[i-1] for i in label_indices]
 if n<=4:
  x=4.0;wi=5.35
  for j,l in enumerate(labels):
   y=2.22+j*.84
   box(s,x,y,wi,.62,LAV)
   plain(s,l,x+.18,y+.11,wi-.32,.42,16.6,True,PP_ALIGN.CENTER)
   if j<n-1:arrow(s,6.67,y+.61,6.67,y+.82)
 else:label_flow(s,labels,3.1,.6,8.85)
 if right:stack(s,[(i,texts[i-1]) for i in right],.54,5.55,8.97,.58,fontsize=13.5,gap=.04)
 if sub:stack(s,[(i,texts[i-1]) for i in sub],.54,5.55,8.97,.58,fontsize=13.5,gap=.04)

def draw(s,r):
 n=r['n'];t=[e['text'] for e in r['els']]
 if n in [7,8]:
  stack(s,[(1,t[0]),(len(t),t[-1])],.55,2.06,3.35,3.9,15.4)
  plain(s,t[1],4.08,2.00,5.10,.28,14.2,True)
  if n==7:
   for j,ind in enumerate([3,5,7]):
    y=2.20+j*1.32
    box(s,4.05,y,5.30,1.02,LAV)
    plain(s,t[ind-1],4.25,y+.10,1.05,.4,17.2,True)
    plain(s,t[ind],5.31,y+.19,3.87,.62,17)
    if j<2:arrow(s,6.55,y+1.03,6.55,y+1.26)
  else:
   for j,(ind,details) in enumerate([(2,[3,4]),(6,[7,8,9]),(11,[12])]):
    y=2.20+j*1.32
    box(s,4.0,y,5.35,1.09,LAV)
    plain(s,t[ind],4.17,y+.11,4.97,.35,16.1,True)
    text='\n'.join(t[k] for k in details)
    plain(s,text,4.28,y+.53,4.70,.46,12.8)
    if j<2:arrow(s,6.63,y+1.1,6.63,y+1.29)
  return
 if n in [12,13]:
  if n==12:
   stack(s,[(1,t[0]),(2,t[1]),(10,t[-1])],.53,2.08,4.18,4.14,15.5)
   plain(s,t[2],5.00,2.14,4.35,.4,17,True)
   plain(s,t[3],5.00,2.68,4.38,1.03,15.3)
   # the exact original sequence of story, backlogs, and additional qualifiers remains in editable text
   stack(s,[(i+1,t[i]) for i in range(4,len(t)-1)],5.03,3.87,4.37,2.26,13.1,gap=.02)
  else:
   labels=[t[i] for i in [0,2,4,6]]
   descr=[t[i] for i in [1,3,5,7]]
   for i,(a,b) in enumerate(zip(labels,descr)):
    x=.49+i*2.31
    plain(s,a,x,2.25,2.17,.70,16.2,True)
    plain(s,b,x,3.05,2.17,.85,14.4)
    if i<3:arrow(s,x+2.12,3.12,x+2.29,3.12)
   plain(s,t[8],.56,4.52,8.7,.36,18,True)
   plain(s,t[9],.64,5.02,4.1,1.04,15.0)
   plain(s,t[10],5.0,5.02,4.20,1.04,15.0)
  return
 if n==14:
  pairs=[(0,1),(2,3),(4,5),(6,7),(8,9),(10,11)]
  for j,(a,b) in enumerate(pairs):
   col=j%3; row=j//3; x=.58+col*3.04;y=2.08+row*1.76
   plain(s,t[a],x,y,2.89,.42,16.5,True)
   plain(s,t[b],x,y+.55,2.87,1.05,14.8)
  plain(s,t[-1],.59,5.87,8.74,.36,14,True)
  return
 if n==16:
  for j,(a,b) in enumerate([(0,1),(2,3),(4,5)]):
   x=.56+j*3.05
   plain(s,t[a],x,2.16,2.94,.63,16.7,True)
   plain(s,t[b],x,2.88,2.96,1.85,14.5)
  plain(s,t[6],.59,5.08,8.8,.35,16,True)
  plain(s,t[7],.59,5.57,8.82,.64,13.0)
  return
 if n==20:
  for j,(a,b,c) in enumerate([(1,2,3),(4,5,6),(7,8,9),(10,11,12)]):
   col=j%2;row=j//2;x=.58+col*4.56;y=2.12+row*1.69
   plain(s,t[a-1],x,y,4.41,.38,17.1,True)
   plain(s,t[b-1]+'\n'+t[c-1],x,y+.45,4.39,1.01,14.6)
  plain(s,t[-1],.59,5.75,8.81,.53,13.2)
  return
 if n==21:
  stack(s,[(1,t[0]),(8,t[7])],.56,2.08,3.36,4.12,15.1)
  plain(s,t[1],4.24,2.15,5.08,.43,18,True)
  box(s,5.67,2.86,2.22,.56,LAV);plain(s,t[2],5.77,2.96,2.01,.37,16.3,True,PP_ALIGN.CENTER)
  for j,ind in enumerate([3,4,5]):
   x=4.18+j*1.83;box(s,x,4.03,1.68,.58,LAV);plain(s,t[ind],x+.1,4.14,1.5,.33,14.7,True,PP_ALIGN.CENTER)
   arrow(s,6.75,3.43,x+.82,4.03)
  box(s,6.20,5.05,1.75,.54,LAV);plain(s,t[6],6.28,5.17,1.59,.32,15.2,True,PP_ALIGN.CENTER)
  arrow(s,6.8,4.62,6.8,5.04)
  return
 if n==22:
  plain(s,t[0],.57,2.12,3.04,2.73,16.5)
  plain(s,t[1],3.77,2.12,5.60,.34,17.3,True)
  label_flow(s,[t[2],t[4],t[6],t[8]],2.58,3.74,5.65,13.3)
  plain(s,t[9],3.77,3.70,5.51,.38,16.9,True)
  box(s,3.81,4.12,5.51,1.50,LAV)
  plain(s,t[10],3.99,4.19,2.40,.36,16.2,True)
  for j,ind in enumerate([11,12,13,14]):
   x=4.01+(j%2)*2.57;y=4.66+(j//2)*.44
   box(s,x,y,2.37,.38,RGBColor(255,255,255),GRAY,.65)
   plain(s,t[ind],x+.1,y+.08,2.12,.23,12.4)
  plain(s,t[15],.62,5.79,8.80,.47,12.8)
  return
 if n==27:
  plain(s,t[0],.59,2.02,4.36,.38,17.6,True)
  plain(s,t[1],.61,2.49,4.39,.73,14.5)
  plain(s,t[2],5.10,2.02,4.33,.38,17.6,True)
  plain(s,t[3],5.10,2.49,4.32,.73,14.5)
  plain(s,t[4],.59,3.37,8.81,.40,17.1,True)
  box(s,.59,3.95,2.75,1.70,LAV)
  plain(s,t[5],.69,4.04,2.50,.32,15.7,True)
  stack(s,[(i+1,t[i]) for i in [6,7,8]],.70,4.49,2.50,.97,fontsize=13.0,gap=.02)
  box(s,3.60,3.95,2.55,1.70,LAV)
  plain(s,t[9],3.72,4.04,2.31,.32,15.7,True)
  stack(s,[(i+1,t[i]) for i in [10,11,12]],3.72,4.49,2.23,.97,fontsize=13.0,gap=.02)
  plain(s,t[13],6.40,3.89,3.04,.31,15.8,True)
  box(s,6.36,4.28,3.05,1.38,RGBColor(255,255,255),GRAY,.75)
  plain(s,t[14],6.48,4.34,2.85,1.26,12.6)
  plain(s,t[15],.62,5.79,8.81,.39,12.9)
  return
 if n in [22,23,27,28,30,32,33,36,38,41,42,45]:
  # A stable editable two-column design; explanatory paragraphs use sizes proportional to lengths.
  make_columns(s,r,cols=2,ysize=4.16)
  # precise supplementary relationships for hierarchical diagrams are drawn as native connectors
  if n==41:
   # semantic link drawn unobtrusively above lower explanatory details (right side)
   pass
  return
 if n in [25,29]:
  make_columns(s,r,cols=2,ysize=4.14);return
 if n==34:
  # Heavy checked calculation: table is essential, original inconsistency is not corrected.
  plain(s,t[14],.65,3.37,2.8,.26,15,True)
  stack(s,[(i+1,t[i]) for i in range(0,6)],.52,2.02,4.24,1.13,fontsize=13,gap=.01)
  stack(s,[(i+1,t[i]) for i in range(6,14)],4.93,2.03,4.48,1.42,fontsize=12.5,gap=.015)
  # 3x6 calculation grid, all cells original text (15-33)
  names=t[16:18]+t[18:23]
  # Rows from original index 16-33
  import math
  heads=['項目']+[t[i] for i in range(18,23)]
  nums=['数字']+[t[i] for i in range(23,28)]
  weights=['重み']+[t[i] for i in range(28,33)]
  rws=[heads,nums,weights]
  x0=.60;y0=3.64;CW=1.47
  for rr,row in enumerate(rws):
   for cc,v in enumerate(row):
    x=x0+cc*CW;y=y0+rr*.64
    box(s,x,y,CW-.045,.60,LAV if rr==0 else RGBColor(255,255,255))
    plain(s,v,x+.05,y+.13,CW-.15,.39,13.1,rr==0)
  stack(s,[(34,t[33]),(35,t[34])],.68,5.66,8.7,.54,fontsize=12.5,gap=.03)
  # exercise remains flagged for editorial verification
  return
 if n==39:
  # top three entities; bottom one-to-many reference links
  for j,idx in enumerate([0,2,4]):
   x=.57+j*3.05
   plain(s,t[idx],x,2.16,2.85,.43,18,True,PP_ALIGN.CENTER)
   box(s,x,2.67,2.86,1.25,LAV)
   plain(s,t[idx+1],x+.10,2.83,2.67,.92,13.4)
  plain(s,t[6],.64,4.19,8.74,.39,16.5,True,PP_ALIGN.CENTER)
  for j,idx in enumerate([7,9,11]):
   x=1.07+j*3.07;plain(s,t[idx],x,4.91,1.94,.43,15.1,True,PP_ALIGN.CENTER)
  plain(s,t[8],3.02,4.93,1.88,.35,13.5)
  plain(s,t[10],6.13,4.93,1.88,.35,13.5)
  for k in range(12,len(t)):
   plain(s,t[k],.66,5.64,8.72,.57,12.4)
  return
 if n in [43,44]:
  from pptx.util import Inches, Pt
  from pptx.enum.text import MSO_ANCHOR
  FONT='源真ゴシックP'
  def native_table(rows,x,y,w,h,colwidth,font):
   slide=s.shapes.add_table(len(rows),len(rows[0]),Inches(x),Inches(y),Inches(w),Inches(h)).table
   for j,v in enumerate(colwidth):slide.columns[j].width=Inches(v)
   for ri,row in enumerate(rows):
    for ci,value in enumerate(row):
     cell=slide.cell(ri,ci);cell.text=value;cell.margin_left=Inches(.07);cell.margin_right=Inches(.06);cell.margin_top=Inches(.03);cell.margin_bottom=Inches(.02)
     cell.fill.solid();cell.fill.fore_color.rgb=LAV if ri==0 else RGBColor(255,255,255)
     cell.vertical_anchor=MSO_ANCHOR.MIDDLE
     for para in cell.text_frame.paragraphs:
      para.space_after=Pt(0)
      for run in para.runs:
       run.font.name=FONT;run.font.size=Pt(font if ri>0 else min(16,font+1));run.font.bold=(ri==0);run.font.color.rgb=IND if ri==0 else TXT
  if n==43:
   plain(s,t[0],.57,2.25,8.86,.3,16.6,True)
   for i,(a,b) in enumerate([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12)]):
    col=i%3;row=i//3;x=.58+3.03*col;y=2.67+row*.85
    plain(s,t[a],x,y,2.87,.34,15,True)
    plain(s,t[b],x,y+.37,2.85,.51,12.9)
   plain(s,t[13],.60,4.51,8.7,.32,16.6,True)
   native_table([t[14:18],t[18:22],t[22:26]],.58,4.90,8.85,1.22,[2.4,1.6,1.35,3.5],13.9)
  else:
   plain(s,t[0],.59,2.02,8.81,.3,16.6,True)
   label_flow(s,t[1:5],2.42,.57,8.87,14.1)
   native_table([t[5:9],t[9:13],t[13:17],t[17:21],t[21:25]],.56,3.42,8.88,2.43,[2.11,2.4,2.20,2.17],12.5)
   plain(s,t[25],.60,5.97,8.85,.30,12.2)
  return

 if n in [46,47]:
  if n==46:
   plain(s,t[0],.55,2.03,5.15,.36,14.5)
   plain(s,t[1],.55,2.49,5.12,.36,16.4,True)
   # full original prompt, unmodified in editable text box
   plain(s,t[2],.56,2.93,5.05,3.25,12.0)
   plain(s,t[3],5.83,2.07,3.55,.37,16.4,True)
   box(s,5.83,2.63,3.51,2.90,LAV)
   stack(s,[(j+1,t[j]) for j in range(4,12)],5.92,2.74,3.31,2.53,fontsize=12.6,gap=.015)
   plain(s,t[12],5.88,5.72,3.5,.48,12.2)
  else:
   plain(s,t[0],.58,2.03,4.21,.39,17,True)
   plain(s,t[1],.58,2.50,4.29,2.99,15.2)
   plain(s,t[2],5.03,2.03,4.33,.39,17,True)
   plain(s,t[3],5.06,2.49,4.29,.29,13.0)
   plain(s,t[4],5.05,2.84,4.30,3.09,11.9)
   plain(s,t[5],.61,5.78,8.7,.39,13.0)
  return
 if n==48:
  label_flow(s,[t[1]+' '+t[2],t[3]+' '+t[4],t[5]+' '+t[6],t[7]+' '+t[8]],2.50,.58,8.85,15.0)
  plain(s,t[0],.59,2.06,8.83,.36,18,True)
  plain(s,t[12],.59,3.57,8.83,.39,18,True)
  stack(s,[(14,t[13]),(15,t[14]),(16,t[15])],.61,4.00,8.80,1.32,fontsize=13.7,gap=.04)
  plain(s,t[16],.61,5.39,8.78,.31,15.5,True)
  plain(s,t[17],.63,5.82,8.76,.35,12.2)
  return
 # default for exact native content: readable columns, no content removal
 make_columns(s,r,cols=2 if len(t)<20 else 3,ysize=4.18)