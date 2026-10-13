# GitHub主導「次」制御への移行とドライラン検査（2026-10-14）

## 採用された実行仕様

**P3のみ「次」1回＝1素材IDを生成・個別評価・ファイル保存**。同じ「次」で2件目を生成しない。15点全部の画像が本当にPASSした場合にのみP4へ進む。PPTXはP3で変更しない。ChatGPT画像生成を標準とし、Figma等の課金が必要な外部生成は無承認で起動しない。

- コントローラ：`docs/workflows/NEXT_COMMAND_CONTROLLER_v1.md`
- P3実行規則：`docs/workflows/PHASE_P3_IMAGE_ASSETS_RUNBOOK_v1.md`
- 正本の機械状態：`docs/runs/lecture03_48slides/step3/EXECUTION_STATE.json`
- 素材履歴：`docs/runs/lecture03_48slides/step3/P3_asset_progress.json`
- P1/P2図の意味・配置：`docs/runs/lecture03_48slides/asset_manifest.json`
- 入口：`CHATGPT_NEXT.md`

## 全15画像のプロンプト固定・入力の分離

`docs/runs/lecture03_48slides/step3/prompts/`に**生成本文だけのtxt15件**を保存。見出し・STEPの達成状況を含めない。S05だけ`v2`で、2人のみの作業場面、試作→操作評価→改善→再試作の循環、**真のアルファ透過**、背景チェッカー描画禁止、複製された人物禁止、平坦で精緻なインディゴ基調の2Dイラストとした。v1は旧フォルダに保存して不採用履歴を保持。

残り14素材は`step2/image_prompts/P2_image_prompts_manifest.json`の確定生成本文に一致するv1を、そのまま素のtxtへ複製。**15件すべてGitHub blob SHAを取得してEXECUTION_STATE.jsonのqueueに固定・照合済み。**

## 実行済み検査（画像生成ではない）

- 画像ID=15、重複0、順序・slide_id整合、参照txt存在15/15、参照blob SHA一致15/15。
- 画像生成本文が先頭から内容本文で始まり、Markdown見出しを含まない15/15。
- 14点のv1プロンプト本文はSTEP2確定プロンプトと一致14/14。S05のみv2として明示改訂。
- 画像の生成指示に「STEP3完了」・「15/15」などの進捗報告文章がないことを照合15/15。
- `EXECUTION_STATE.json`、`P3_asset_progress.json`、`asset_manifest.json`、人間用`STATE.md`の同一画像ID／版／状態の整合性を検証。
- **ドライラン：** `次` → `GENERATE_ONE_ASSET` → `S05-A-01` → `docs/runs/lecture03_48slides/step3/prompts/S05-A-01_prompt_v2.txt`（blob `50185e920465f2264b4a81652123cc19f8221084`）。
- **この移行中に画像生成は一切実行していない。** 採用画像0/15、新しいv2生成試行0回、その他14点未着手。
- 旧ChatGPT v1失敗3回とFigma v1のアップロードJPEG（チェッカーを描き込んだ非透過）の不採用履歴は保存済み。成功扱いへ書き換えていない。

## 実際の画像生成についての未保証条件

ChatGPT画像生成ツールの有効プロンプト本文がAPI上で観測できない場合は、GitHubの文字列を**モデルへ完全に同じバイト列で渡したことを保証できない**。あくまでGitHub固定テキストを唯一の意図として使い、生成後のPNGバイナリ／RGBA透過／意味・構図・矢印／保存SHAの**実物検査で合否判定**する。これを機械的に保証したかのように報告しない。

## 保存と次のトリガ

この移行を監査して最終状態を`READY`にした後、ユーザーの次のメッセージが**「次」**なら、その時だけS05-A-01 v2の1素材に着手する。S05がPASSなら`next_asset_id=S06-B-01`に進み、別の「次」を待つ。失敗なら同じ素材で限定再試行し、規定回数までにPASSしなければBLOCKED。生成・QC・永続保存を伴わない限り次IDへ進めない。
