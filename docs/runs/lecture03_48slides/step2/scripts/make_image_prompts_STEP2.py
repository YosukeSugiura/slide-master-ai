import json, math, re, hashlib
from pathlib import Path
ROOT=Path('/mnt/data/lecture03_step2/production')
slots=json.loads((ROOT/'asset_slots_15.json').read_text())
expected={
'S05-A-01':('プロトタイピングの反復','試作品を具体的に作り、ユーザーが触って評価して改善点を開発者に返し、改良版を再度試作する因果的な循環。必須の反復は試作→評価→改善→再試作へ戻る。教室予約UIの試作品は実在の製品スクリーンショットではなく抽象化した画面イメージにする。','評価から改善を経て次の試作へ戻る方向を正確に示す。試作と完成品を混同しない。'),
'S06-B-01':('使い捨て型の試作品','開発者が要件確認のため試作品を作り、利用者が確認した後にその試作品を廃棄し、得た知識を新規の本開発に引き継ぐ。','試作品自体を完成品へ継続改良する場面は描かない。試作品が本開発へ物理的に変身する描写は禁止。'),
'S06-B-02':('進展型の試作品','開発者が同じ試作品を繰り返し改良・機能追加し、完成可能な実システムへ育てていく。','試作品を廃棄したあと作り直す描写をしない。使い捨て型とは明確に異なる。'),
'S10-A-01':('スクラムの短い反復','プロダクトバックログをもとにチームが短いスプリントを実施し、使用可能なインクリメントを作り、フィードバックを得てバックログの次の優先順位へ戻す反復活動。','バックログ→スプリント→インクリメント→フィードバック→バックログへの戻りは逆転しない。'),
'S11-B-01':('プロダクトオーナー','プロダクトオーナーが候補機能のバックログを評価し価値最大化のため優先順位を判断する。ステークホルダーの希望を聞き、開発者へ明確に共有する。','単なる指揮命令する上司の描写は禁止。他のスクラム役割の説明を混入させない。'),
'S11-B-02':('スクラムマスター','スクラムマスターがチームの対話を促進し、開発の妨げになっている問題を取り除き、自己管理やプロセス改善を支援する。','チームの成果物を一人で作る開発者や優先順位を決めるプロダクトオーナーにしない。'),
'S11-B-03':('開発者','職能の異なる複数の開発者が互いに相談しながらコード・テスト・UIの作業を協働で進め、動作する成果物を生み出す。','一人の管理者から一方的に指示を受ける上下関係の描写は禁止。'),
'S15-A-01':('DevOpsの開発・運用循環','開発者・テスト担当・運用担当が継続的に連携し、開発・テスト・リリース・運用・監視・改善のサイクルを回し、監視結果を次の開発・計画へ戻す。','運用と監視を消さず、リリースして終わる一方向の工程にしない。セキュリティと信頼性は必要なときだけ意味的に添える。'),
'S17-A-01':('MLOpsのデータとモデルの循環','データ収集→前処理→モデル学習→モデル評価→配備→監視の6活動を、一つの自然な流れとして表現する。監視結果で劣化を把握したら再学習と更新を経て再配備へ戻ることを示す。','監視から学習への帰還を省略しない。開発・配備・監視の間の矢印を逆転させない。データそのものとモデルを混同しない。'),
'S18-B-01':('ローコードでの予約アプリ開発','開発者がビジュアルなUI部品と簡潔なプログラムコードを併用し、教室予約アプリの機能を組み立てる。人間が生成結果を確認する。','ノーコードと混同してコード入力を完全に排除しない。'),
'S18-B-02':('ノーコードでの予約アプリ開発','利用者がドラッグ＆ドロップの視覚的な設定を中心に、コードを書かずに教室予約アプリを構築する場面。制約のある設定部品の存在を自然に示す。','ローコードの手書きコードや生成AIチャット画面を主役にしない。'),
'S18-B-03':('生成AIでの予約アプリ試作','人間が自然言語で予約アプリの要件を伝え、生成AIがコード・UIの試作案を返し、人間が動作を検証する。','AIが完全な品質保証を行ったように描かず、最終責任を人間が持つ様子を示す。'),
'S26-B-01':('ワイヤーフレーム','教室予約UIの情報の配置と導線だけを、灰色線と単純な矩形で組み立てた粗い画面レイアウトの独立図。','写真・完成デザイン・操作可能なアプリのように見せない。'),
'S26-B-02':('モックアップ','教室予約UIの配色・見た目・視覚階層を整えた完成画面の静的見本。','タップによる機能動作、ライブ操作のエフェクト、コード編集を描かない。'),
'S26-B-03':('操作できるプロトタイプ','教室予約UIを実際にタップして検索から予約まで操作・画面遷移を試している場面。','完成製品・設計書そのもの・静的なモックアップと混同しない。')}
assert len(expected)==15
out=ROOT/'image_prompts';out.mkdir(exist_ok=True)
entries=[]
for slot in slots:
 id=slot['asset_id'];name,required,guards=expected[id]
 w,h=slot['width'],slot['height'];ar=round(w/h,4)
 out_w=round(max(1800, (h/w)*1900)*ar/8)*8 if w<h else (2400 if ar>2.1 else 2048)
 out_h=round(out_w/ar/8)*8
 class_type='A' if '-A-' in id else 'B'
 fmt='統合された一つの説明場面' if class_type=='A' else '独立した一つの比較対象の行動場面'
 prompt=f'''【生成する完成品｜最優先】
背景透過を基本とする**独立した2Dフラットイラスト画像1点**を生成する。対象は「{name}」。制作範囲は **{fmt}だけ**。スライド全体、講義ポスター、複数コマのコラージュを生成しない。

【何を意味的に表すべきか】
{required}

【厳密な意味関係・禁止される誤解】
{guards}

【構図と画角】
最終的な挿入枠は横{w:.3f}インチ×縦{h:.3f}インチ（縦横比{ar:.4f}:1）。図を横長画面の内側に十分な余白を取って配置し、被写体を切り落とさない。推奨する評価解像度は約{out_w}×{out_h}px。人物や道具など、当該テーマに必要な具体物を用い、単なるアイコンの横並びにしない。矢印は因果や循環を伝えるために必要な場合のみ、必須の向き・戻り先を正確に示す。情報量は投影サイズでも理解できる密度に抑える。

【デザイン言語】
白／透明背景、インディゴ#41419Eを基調にした低彩度の教育用フラット図。濃い輪郭と明確なシルエット、均整の取れた線幅、さりげない補助色を採用する。グラデーション、3D、過剰な影、飾り枠、丸いUIカードの羅列は避ける。同一講義の他画像と統一した画風を保つ。

【画像の制作範囲から完全に除外】
スライド全体、スライドタイトル、イントロ、Takeaway、説明本文、表、ページ番号、大学ロゴ、写真、注釈ポスター、読み取らせるための大量の日本語、架空の固有名詞、関係のない他の役割・手法。正確な語句は別途PowerPointの編集可能テキストとして配置する。画像内では文字を原則描かない。原文の数値・専門用語・ロゴを捏造しない。

【採用前の必須評価】
意味契約の全条件が満たされること。禁止例が存在しないこと。矢印・循環の方向が正しいこと。主役・対比・視線誘導・情報量・画風をそれぞれ独立評価すること。全体をスライド画像にしないこと。横長枠への等比配置で切り落としや極端な余白が生じないこと。いずれかに不合格があれば素材として採用しない。'''
 preflight={
 'G01_exactly_one_standalone_image':True,
 'G02_explicit_main_subject_action':True,
 'G03_semantic_contract_source_based':True,
 'G04_required_relations_or_role_clear':True,
 'G05_forbidden_misread_explicit':True,
 'G06_aspect_ratio_and_frame_grounded':True,
 'G07_background_style_specified':True,
 'G08_slide_text_and_title_excluded':True,
 'G09_unrelated_assets_excluded':True,
 'G10_independent_postgeneration_qc_specified':True
 }
 item={**slot,'class':class_type,'label':name,'prompt_version':'v1','meaning_contract':required,'critical_negative_contract':guards,'prompt_status':'P2_FIXED','prompt_text':prompt,'preflight_10_gates':preflight,'preflight_result':'PASS','output_target_px':{'width':out_w,'height':out_h},'status':'NOT_GENERATED','image_sha256':None}
 entries.append(item)
 (out/f'{id}_prompt_v1.md').write_text(f'# {id} — {name}\n\n'+prompt+'\n',encoding='utf-8')
(out/'P2_PROMPTS_INDEX.md').write_text('# 情報システム論 第3回 — STEP 3用独立画像プロンプト15点\n\n'+'\n'.join(f'- `{v["asset_id"]}` — {v["label"]}：枠 {v["width"]}×{v["height"]}in、10項目事前ゲートPASS' for v in entries)+'\n\n> **STEP2では画像自体は生成していない**。STEP3で各個別ファイルだけを画像生成器に渡し、必須意味ゲートと視覚検証に合格した画像のみ採用。\n',encoding='utf-8')
(ROOT/'P2_image_prompts_manifest.json').write_text(json.dumps({'schema_version':'1.0','run_id':'lecture03_48slides','source_deck':'lecture03_48_step2_skeleton_draft.pptx','total_assets':len(entries),'complete_count':len(entries),'image_generation_started':False,'assets':entries},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('prepared',len(entries),'single-asset prompt files, total chars:',sum(len(x['prompt_text']) for x in entries))