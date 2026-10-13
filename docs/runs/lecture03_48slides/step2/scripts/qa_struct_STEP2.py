from pathlib import Path
import sys,re,json,hashlib,math
from pptx import Presentation
ROOT=Path('/mnt/data/lecture03_step2/production');prs=Presentation(str(ROOT/'lecture03_48_step2_skeleton_draft.pptx'))
raw=json.loads((ROOT/'slide_source_inventory.json').read_text())
slots=json.loads((ROOT/'asset_slots_15.json').read_text())
def norm(s):return re.sub(r'\s+','',s)
issues=[];per=[]
arrowchars=set('↓↑←→↘↙')
for i,(slide,src) in enumerate(zip(prs.slides,raw)):
 text=[sh.text for sh in slide.shapes if sh.has_text_frame and sh.text.strip()]
 for sh in slide.shapes:
  if sh.has_table:
   text.extend([sh.table.cell(rr,cc).text for rr in range(len(sh.table.rows)) for cc in range(len(sh.table.columns))])
 mixed=norm('\n'.join(text))
 skipped=[];missing=[]
 for e in src['els']:
  target=norm(e['text'])
  if not target:continue
  if target in mixed:continue
  if all(c in arrowchars for c in target):skipped.append(e['index']);continue
  # elements may be split into editable text paragraphs, especially S02
  if all(norm(p.lstrip('・ ').strip()) in mixed for p in e['text'].split('\n') if p.strip()):continue
  missing.append({'index':e['index'],'text':e['text'][:90]})
 for k in ('title','intro','take'):
  v=src[k]
  if v.startswith('（'):continue
  if norm(v) not in mixed:missing.append({'field':k,'text':v[:90]})
 if missing:issues.append({'slide':i+1,'missing':missing})
 tables=[sh.table for sh in slide.shapes if sh.has_table]
 if i+1 in [9,35,37,43,44]:
  if not tables:issues.append({'slide':i+1,'missing_native_table':True})
  else:
   t=tables[0]
   if i+1 in [9,35,37]:
    md=src['table'];rows=[]
    for line in md.splitlines():
     if line.startswith('|'):
      vals=[v.strip() for v in line.strip().strip('|').split('|')]
      if all(re.fullmatch('[-: ]+',v) for v in vals):continue
      rows.append(vals)
    got=[[t.cell(r,c).text for c in range(len(t.columns))] for r in range(len(t.rows))]
    if rows!=got:issues.append({'slide':i+1,'table_mismatch':True,'expected_rows':len(rows),'got_rows':len(got)})
 if not text:issues.append({'slide':i+1,'empty':True})
 nimages=sum(1 for sh in slide.shapes if sh.shape_type==13)
 if nimages:issues.append({'slide':i+1,'unexpected_raster_images':nimages})
 per.append({'slide':i+1,'source_elements':len(src['els']),'editable_text_shapes':len(text),'native_tables':len(tables),'source_missing':len(missing),'arrow_symbols_as_native_connectors':skipped})
if len(prs.slides)!=48:issues.append({'slide_count':len(prs.slides)})
seen=set()
for slot in slots:
 if slot['asset_id'] in seen:issues.append({'duplicate_asset_id':slot['asset_id']})
 seen.add(slot['asset_id']);n=int(slot['slide_id'][1:]);s=prs.slides[n-1]
 match=[sh for sh in s.shapes if sh.has_text_frame and slot['asset_id'] in sh.text]
 if len(match)!=1:issues.append({'asset_missing_or_ambiguous':slot['asset_id'],'count':len(match)})
 if not(0<=slot['x']<=10 and 0<=slot['y']<=7.5 and slot['width']>0 and slot['height']>0 and slot['x']+slot['width']<=10.01 and slot['y']+slot['height']<=7.51):issues.append({'bad_slot_geometry':slot['asset_id']})
for sh in prs.slides[0].shapes:
 if not sh.has_text_frame:continue
 if sh.text and ('2025' in sh.text or '48' in sh.text):pass
# approximate font checking; does not equate to actual rendering font installation
noncompliant=[]
for i,slide in enumerate(prs.slides):
 for sh in slide.shapes:
  if sh.has_text_frame and sh.text.strip() and sh.text.startswith('画像挿入領域'):continue
  if sh.has_text_frame and sh.text.strip():
   fs=[run.font.size.pt for para in sh.text_frame.paragraphs for run in para.runs if run.font.size]
   if fs and min(fs)<12:noncompliant.append({'slide':i+1,'min_font_pt':min(fs),'text':sh.text[:24]})
summary={'slide_count':len(prs.slides),'editable_and_text_coverage_issues':issues,'issues_count':len(issues),'sources_scanned':sum(x['source_elements'] for x in per),'image_slots':len(slots),'strict_tables_verified':[9,35,37],'font_below_12':noncompliant,'actual_gen_shin_font_rendered':False,'slide34_source_inconsistency_unresolved':True,'batch_completed_count':8,'timestamp':'2026-10-14'}
(ROOT/'P2_structural_QC.json').write_text(json.dumps({'summary':summary,'slides':per},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ['editable_and_text_coverage_issues','font_below_12']},ensure_ascii=False,indent=2))
print('ISSUES',len(issues));print(json.dumps(issues,ensure_ascii=False,indent=2)[:3000]);print('TINY',len(noncompliant))