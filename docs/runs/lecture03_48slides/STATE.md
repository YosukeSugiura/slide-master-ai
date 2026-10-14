# 情報システム論 第3回「ソフトウェア開発」48枚版 — 標準4段階の進捗正本

> **本番48枚の正本。** 試作3枚の `docs/runs/lecture03_three_slides/STATE.md` は履歴として維持。**P1/P2は完了、P3は2026-10-14のGitHub駆動・画像ID単位の「次」方式へ移行**。48枚のPPTX骨組みと15点の画像生成指示は保存済み。現在2点採用、S06-B-02でBLOCKED（生成が別題材のスクラムへ逸脱）。

| key | value |
|---|---|
| repository | YosukeSugiura/slide-master-ai |
| branch | minor |
| run_id | lecture03_48slides |
| target | 情報システム論 第3回「ソフトウェア開発」元48枚版（53枚版は対象外） |
| mode | four_phase_standard |
| status | BLOCKED |
| current_step | P3_IMAGE_ASSETS |
| last_completed | P2_PPTX_SKELETON (content and geometry PASS; final font/dense typography gate deferred explicitly to P4) |
| attempts | P1:1; P2:2 (initial interrupted; recovered and finished 8 batches) |
| last_log | docs/runs/lecture03_48slides/step3/P3_S06_B02_GENERATION_BLOCKED_20261014.md |
| blocking_reason | S06-B-02 v2 image generator made two unrelated Scrum role diagrams; effective GitHub prompt transmission is not verifiable; 2/15 accepted preserved |
| specification | docs/workflows/LECTURE_SLIDE_PRODUCTION_4PHASE_v1.md |
| controller | docs/workflows/CHATGPT_STEP_CONTROLLER_v2.md |
| image_procedure | docs/IMAGE_GENERATION_STAGED_WORKFLOW_v2.md |
| outputs | P2 B01-B08 48-page editable PPTX skeleton and all 15 P3 prompts completed; durable binaries in Library, scripts/QA/prompts/GitHub manifests on minor |
| approved_baseline | docs/workflows/LECTURE03_APPROVED_VISUAL_BASELINE_20261013.md |

## 2026-10-14 ユーザー指定：画像内の短い文字を許可（最新の優先規則）

**「文字がはいっててもいいよ！わかりやすいんだもん」**を受け、意味のわかる短い日本語ラベルを許可。4段階を説明する独立図には「試作」「評価」「改善」「再試作」などのラベルを大きく描いてよい。誤字/不自然な文字・投影時読めない小字・スライド全体を画像化することは引き続き禁止。A/Bの全15個のプロンプトを新版（**S05 v3、それ以外v2**）でGitHub固定。新しい `次` 1回＝1画像IDの制御は変更しない。

S05 v2の生成画像2件の実績：**1件目は4段階ラベルが分かりやすい候補（最終投影可読性未検査）、2件目は誤字・重複・スライドタイトル混入でFAIL**。両方とも実PNGをLibraryに保存済み。元のChatGPT v1の失敗3回/Figma v1の失敗1回も保持。**採用数は0/15、最新v3画像は未生成**。詳細 `docs/runs/lecture03_48slides/step3/P3_LABEL_POLICY_CHANGE_20261014.md`。

**次回の「次」：** `S05-A-01`、`docs/runs/lecture03_48slides/step3/prompts/S05-A-01_prompt_v3.txt` のみ実行。生成時は短い正確なラベルを許可し、実PNG/透明画素/QC/永続保存に合格するまでキューを進めない。

## 現行の「次」の実行指示（2026-10-14以降）

**「次」1回＝P3の画像IDを1件だけ実行**。ChatGPTが素材を自分で決めたり、15点を一括で生成しない。まず最新の `docs/workflows/NEXT_COMMAND_CONTROLLER_v1.md`、`docs/runs/lecture03_48slides/step3/EXECUTION_STATE.json`、`docs/workflows/PHASE_P3_IMAGE_ASSETS_RUNBOOK_v1.md` を取得し、`next_prompt_file`に書かれた1件の本文のみを画像生成の指示にする。

- current_step: `P3_IMAGE_ASSETS`（変更なし）
- current P3 status: `READY`（新しいプロンプト版v3を用意して再開可能になったことを意味し、**画像の品質がPASSしたことは意味しない**）
- next_action: `GENERATE_ONE_ASSET`、next_asset_id: `S05-A-01`
- next_prompt_file: `docs/runs/lecture03_48slides/step3/prompts/S05-A-01_prompt_v3.txt`
- status queue: 15件すべて未合格、S05はラベル許可版v3でREADY、その他14件は改訂v2でTODO。
- **旧ChatGPT v1不合格3件／Figma v1不合格1件／S05 ChatGPT v2試行2件（候補1・FAIL1）を履歴保持**。v3の試行数は0。2画像目は次のユーザー「次」まで実行しない。
- 実際の画像は**まだ生成されていない**。PNG/真のアルファ/RGBA・意味QC/実ファイル保存とSHAを通過した場合のみ該当画像をPASSにする。Figma等の課金を伴う他サービスへ無断切替しない。
- GitHubの機械的な唯一の進行ポインタは `step3/EXECUTION_STATE.json`、個別の実施証跡は `step3/P3_asset_progress.json`。本 `STATE.md` は人間向けサマリー。

## P3旧方式の不合格・ブロック履歴（2026-10-14、現行の実行指示ではない）

**STEP3は BLOCKED のまま**（要求15画像のうち採用0、S05-A-01で不適合画像3回、残り14点は未着手）。画像生成器が対象単独のプロンプトを受け付けず、「STEP3 15/15 PASS」と虚偽表示する完成報告画像を繰り返し返した。これらを採用しない。**P4へ移行しない。**

- QCと再開記録：`docs/runs/lecture03_48slides/step3/P3_GENERATION_FAILURE_20261014.md`、`docs/runs/lecture03_48slides/step3/P3_asset_progress.json`。
- 不合格画像の実体（3点）と詳細な試行JSONはLibrary `/SlideProjects/lecture03_48slides/step3/` に保存済み。
- 再開には**素材IDごとの確定プロンプトを画像生成エンジンへ確実に渡せる経路**の確立が必要。現状の「次」だけで反復生成すると同種の画像を再生産してしまう可能性があり禁止。ユーザーの方針確認も必要。
- **STEP2の48枚PPTXや15個の画像プロンプトは保全済み。** P3中にPPTXを作成・編集していない。
- フォント、本文サイズ、S34の計算説明の留保は引き続きP4未解決事項。

## 内部進捗・監査

- 各工程の素材/ページ進捗（TODO/PASS/FAIL/IN_PROGRESS/BLOCKED）、完成物・保存先・SHA256、実行ログは本runディレクトリへ記録。
- P1指示書・素材一覧・原稿はGitHub保存済み。P2の全48枚の編集可能PPTX、8バッチ、PDFプレビュー、15画像生成指示書を保存済み。旧3枚試作や未検証の48ページ草稿を完成品とみなさない。過去に承認された視覚構成はデザイン方針として引き継ぐ。
- `design_system_general_final.md` v2.2、`content_visual_policy_final.md` v2.8。源真ゴシックP現物フォントのインストールと実描画は未確認。補足まとめ文は独自情報がある場合だけ18pt、背景#F3F4F6、Takeaway重複排除。
- 品質ゲートを満たさず完成扱いにしない。P2→P3→P4の切替は原則「次」3回。ただし実行上限/保存不能による追加再開があり得る。

## P1実行記録

- 成果物保存先：docs/runs/lecture03_48slides/ 下のslide_definition.md、slide_plan.json、asset_manifest.json、P1_QC_report.md、logs/P1_SPEC_ATTEMPT01_20261013.md。
- 原文保存先：docs/lecture03_48_slide_contents.md。元ファイルSHA256: 7b4cf96d2d4897aacb714cd2c7782b3151bd8a0c398229ec929976c0c8266690。
- 48枚・A4/B4/C40・画像素材15点。S34には技術的な疑義あり。次工程はP2。

## 2026-10-14 中断再開記録

- 初回STEP2一括作成でハング。ユーザー指示で**6枚×8バッチ、2枚ごとにGitHubコミット、バイナリはLibraryへバックアップ**に変更。
- 現在S01/S02の構造・原文・代替フォント表示検査PASS、フォント実描画未確認。S03-S48はTODO。全STEP2はIN_PROGRESS扱いで、`status=READY`は「続きを実行可」を意味する。
- バッチ正本：`docs/workflows/STEP2_BATCH_CHECKPOINT_v1.md`。実績・次の開始点：`docs/runs/lecture03_48slides/step2/checkpoints.json`。
- 再開：S03。検査PASSしたS01/S02を理由なく作り直さない。

## 2026-10-14 P2完了とP3への移行記録

- 制作完了：B01～B08／48枚、画像枠15、独立画像プロンプト15、全ページPDFレンダリング。QC原文要素568／欠落0。保存先とSHAは `docs/runs/lecture03_48slides/step2/P2_delivery_manifest.json`。
- 未解決のタイポグラフィ・源真ゴシックP実レンダリング・S34原文問題はP4での最終品質ゲートまで追跡する。P3で画像のみ先行することは可能だが、それらの課題をPASSしたと扱わない。
- 次のユーザー「次」：P3で15画像を1点ずつ生成する。PPTX編集は行わない。

## 2026-10-14 STEP3 v1不合格の履歴（旧版）

- S05-A-01 のみ3回試行し、毎回「STEP3完了」を偽装する複数図コラージュで不合格。残14素材の生成は未着手。0/15のため P3_IMAGE_ASSETSから進行せず、`status=BLOCKED`。

## 2026-10-14 Figma v1パイロットの履歴

- Figma generate_imageへGitHub確定プロンプトを明示送信し、S05-A-01を1536×1024のPNGとして生成成功（クレジット消費）。ただしPNG本体の取得が現在の作業環境で失敗し、品質QCと永続保存は未実施。
- **採用0点のまま、P3はBLOCKED**。Figma画像の外部URLは7日で失効するため、手動ダウンロード・チャット添付、あるいは利用可能なアプリ経由の画像取得を確認してから再開する。
- 詳細：`docs/runs/lecture03_48slides/step3/P3_FIGMA_PILOT_20261014.md`。過去3回の不適切な生成報告画像は不採用のまま。

## 2026-10-14短ラベル許可の更新（監査）

- 実際に生成されたv2画像2点は原本を保存し、候補1／不合格1と判定。新たに画像を生成せず、生成指示とQC基準だけを修正した。
- `S05-A-01_prompt_v3.txt` および残り14点の `prompt_v2.txt` を現在の正本とした。
- `EXECUTION_STATE.json` による次のIDはS05-A-01を維持。画像採用数0/15。

## 2026-10-14 直前の2画像の保存・検査回復記録（最新）

- 以前の2回の「次」で実際に生成されたS05-A-01 v3とS06-B-01 v2は、前回までGitHubの状態記録が欠落していた。今回、画像原本を回収し、PNGシグネチャ/RGBA/alpha透明率、図の意味・日本語短ラベル・矢印、画角を検査した。
- **S05-A-01: PASS**。1521×1034px、透明画素56.8%、SHA256 `3b371566c54b92504b4640386b6b8a5a45cbb2e56f12156f0db43b45d9ece380`、Library `/SlideProjects/lecture03_48slides/step3/accepted/S05-A-01_prompt_v3_attempt1.png`。
- **S06-B-01: PASS**。画角調整のため透明余白のみトリミングし、内容の修正はしていない。1448×613px、透明画素53.6%、SHA256 `3864b3f7a1948bb6999e54c57d9134dcb80abadbb39786060681022ebff0ce27`、Library `/SlideProjects/lecture03_48slides/step3/accepted/S06-B-01_prompt_v2_attempt1.png`。
- **2/15画像PASS、次の画像はS06-B-02 v2**（進展型の試作品）。本STEP3のルールは1回の「次」1画像を維持。スライドに埋め込んだ場合の最終縮小可読性はP4で再確認。実効プロンプトのバイト一致はモデルAPIから確認できず`CONTEXT_ONLY_UNVERIFIED`。
- 詳細監査：`docs/runs/lecture03_48slides/step3/qc/P3_RECOVERY_S05_S06_20261014.json`。機械状態 `docs/runs/lecture03_48slides/step3/EXECUTION_STATE.json` を最新の正本とする。**これより上に記載された「0/15、S05次」は当時の履歴であり最新ではない。**

## 2026-10-14 最新：S06-B-02 で早期BLOCKED（画像2/15点PASS）

- 前回までのS05-A-01 v3とS06-B-01 v2の画像は実PNGを回収・RGBA透明・意味/形状QC・永続アップロードを確認して**2/15 PASS**に修正済み。過去のGitHub未更新を回復した。
- 今回の「次」は正しくS06-B-02 v2を指したが、ChatGPT画像生成器が2回とも**対象外のスクラムチーム/マスター/バックログ**を描いたため、**2試行ともFAIL**。実際のプロンプト伝達が観測不能で混線が解消していない。3回目は実行せず早期停止。
- 不適合2画像はLibraryの `step3/rejected/` に隔離。GitHub監査：`docs/runs/lecture03_48slides/step3/P3_S06_B02_GENERATION_BLOCKED_20261014.md`。
- キューの次IDは**S06-B-02のまま**。未着手12点を飛ばさず、P4へ進まない。次の単純な「次」ではBLOCKEDの根本問題を解消したと偽って再生成しない。
- 推奨再開条件：GitHubの個別promptを画像生成器へ明示的に渡せる経路、または対象プロンプト以外を含まない専用チャットへの切替を確認する。ユーザーの許可なくFigma等の外部課金ツールへ切り替えない。
