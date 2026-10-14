# ChatGPT画像素材制作 — 「次」で1点ずつ進める専用入口

> 対象は大学講義「情報システム論 第3回：ソフトウェア開発」（48枚版）の **P3独立画像15素材のみ**。GitHub private repository `YosukeSugiura/slide-master-ai` の **`minor` ブランチ**を正本とする。GitHub Actions、OpenAI有料API、PPTX再生成は行わない。

## 新しいChatGPTチャットへの最初の指示

「GitHubの `YosukeSugiura/slide-master-ai` / `minor` にある `CHATGPT_IMAGE_NEXT.md` を全文読み、そこに書かれた固定ルールで画像素材のP3制作を再開してください。初回は読込み・状況報告のみ。以降、『次』で1素材だけ画像生成、検査、保存・GitHub状態更新を実施してください。」

このファイルの読込みだけで**画像を作ってはならない**。初回は現状と次の素材IDを返す。

## 1. 読み取るファイル（毎回、GitHubの最新を確認）

1. `docs/runs/lecture03_48slides/step3/EXECUTION_STATE.json` — 現在のキューと次の素材、固定プロンプトのバージョン・Git blob SHA、現在の状態
2. `docs/runs/lecture03_48slides/step3/P3_asset_progress.json` — 採否・試行履歴・保存先
3. `docs/runs/lecture03_48slides/asset_manifest.json` — スライド番号、画像枠x/y/w/h、意味契約、禁止事項
4. `docs/runs/lecture03_48slides/step3/reference/lecture03_p3_context.zip` — STEP2の元48枚PPTX、対象8スライドのレンダリング参照（ZIP内 `slides/Sxx.jpg`）、合格済みのスタイル見本（ZIP内 `style/S05-A-01.webp`, `style/S06-B-01.webp`）、`manifest.json`
5. `docs/runs/lecture03_48slides/step3/reference/lecture03_p3_context.sha256` — ZIPの整合性検査値
6. `EXECUTION_STATE.json.next_prompt_file` の指す `step3/prompts/{asset_id}_prompt_vN.txt` — **生成する内容についての唯一の固定指示**

最新stateの`next_prompt_blob_sha`と、GitHubから取得したプロンプトのblob SHAが一致しなければ実行しない。失敗した過去のプロンプトや古いREADMEを優先しない。

**参照ZIPに入るスライド画像は .jpg、スタイル画像は .webp。これらを図の生成内容と混同しない。** ZIP/PPTXは参照用であり、画像生成の最終成果物ではない。

## 2. 作る画像の形式と意味

- ユーザーが「次」と入力したら、最新状態の未完了素材 **1点だけ**をChatGPTの画像生成機能で作成する。画像を生成しないまま進捗だけ進めない。
- **1画像＝独立した透明背景の2Dフラットイラスト**。画像の中でスライド全体を再現したり、別の画像IDの図を混ぜたりしない。
- 図の内容は対象`prompt_vN.txt`を尊重。背景・造形・意味・見た目のルールは`docs/workflows/PHASE_P3_IMAGE_ASSETS_RUNBOOK_v1.md`も参照するが、個別図の内容を勝手に書き換えない。
- 合格済みの画像を再生成しない。現時点ではS05-A-01とS06-B-01の2点がPASS、S06-B-02はv3未実行（0試行）でREADY。
- 日本語ラベルは短く正確なものを許可。管理ID・スライド番号・本文の再印字・偽文字は禁止。
- 画像枠のサイズと比率はasset_manifestに記録された実測値を使い、端切れ、極端な余白を避ける。
- 既存スライド画像・画風見本は**参照資料**であり、編集対象画像として丸ごと描き直すのではない。

## 3. GitHubの参照バイナリにアクセスできない場合

GitHubの接続ツールが非テキスト画像・ZIPを取得できない／画像生成へ視覚参照として渡せない場合、**アクセスできたと偽らない**。該当参照ファイルの添付をユーザーに依頼し、その素材で停止する。ファイルが取得できないのに、元スライドを見た前提でPASSさせない。

既存の参照画像はZIPにあり、チャットによってはユーザーによる**初回一括添付が必要**。GitHubを唯一の**指示・状態の正本**とすることと、ChatGPT画像生成に私有画像の実ピクセルを渡せることは別である。

## 4. 「次」「やり直し」「状況」「スキップ」

- **次**：stateがREADYの場合、最初の未PASS項目の固定プロンプトを読み、必要なSxx参照画像とスタイル例を視覚的に確認し、**画像を1点だけ生成してQC/永続保存**する。PASSで保存が実証された場合のみ次のIDへ進む。FAILなら現在のIDに留まる。**「次」だけで前画像を無条件採用しない**。
- **やり直し**：現在の未PASS素材のみ再試行。原則同一プロンプト版の試行上限は3回。超過時は新しいvNに改善内容を明記し、古い履歴を保全。合格済み画像の無断上書き禁止。
- **状況**：GitHubの最新state・progressの内容と、実際に存在するファイルを検査し、読み取り専用で報告。
- **スキップ**：基本的に禁止。ユーザーが明示した場合は当該素材を保留とする運用変更を別途合意し、旧ログを保全してから進める。
- 保存不能・品質未確認・必須参照なし・矛盾する状態なら**BLOCKED**として止め、次の素材へ進んだと虚偽報告しない。

## 5. 1点を生成した後の品質検査

対象固有の意味契約、誤読の禁止、矢印方向・因果関係、対象スライドとの図柄・色・余白の整合を検査。実ファイルが得られた場合、PNGシグネチャ、RGBA、alpha=0画素率（目標10%以上）、縦横比誤差（目標1.8%以内）、縮小可読性、テキストの正確性を記録する。

**画像がチャット画面に出たことは保存完了ではない。** 実ファイルの取得と永続保存を確認する。

## 6. 合格画像・不合格画像・進捗の保存

合格時の希望配置：
- `docs/runs/lecture03_48slides/step3/accepted/{asset_id}.png` — GitHubのPNG実体（成功とみなすにはblob存在・読戻しと実SHA256照合が必要）
- `docs/runs/lecture03_48slides/step3/qc/{asset_id}_prompt_vN_attemptK.json` — 実施日時・判定と理由、画像SHA256、参照プロンプトとそのGit blob SHA、画像情報、保存先
- `docs/runs/lecture03_48slides/step3/P3_asset_progress.json` と `EXECUTION_STATE.json` — **採用画像の保存を確認した後に**当該1点をPASSに変更

不合格時の希望配置：
- `docs/runs/lecture03_48slides/step3/rejected/{asset_id}_prompt_vN_attemptK.png`
- 同じ`qc/`ディレクトリの詳細ログ。失敗試行を隠して新しいIDに進まない。

生成バイナリのGitHub書込を現在のChatGPT/接続ツールが実行できない場合はLibrary等の永続保存を代替とし、実在・所在・SHAをGitHubログへ明記する。その場合は**「PNG本体もGitHubに保存済み」と主張しない**。ユーザーが完全GitHub保存を必須とするなら、GitHubへのバイナリ書込経路を別途用意するまでSTOPする。

進捗の`EXECUTION_STATE.json`は最後に競合を検査して更新する。別チャットで同時に「次」を実行しない。

## 7. 対象キュー

順番は **`EXECUTION_STATE.json.queue`が唯一の正本**。現時点の15件：

S05-A-01(PASS) → S06-B-01(PASS) → **S06-B-02(v3 READY)** → S10-A-01 → S11-B-01 → S11-B-02 → S11-B-03 → S15-A-01 → S17-A-01 → S18-B-01 → S18-B-02 → S18-B-03 → S26-B-01 → S26-B-02 → S26-B-03。

この一覧は初期状態の説明であって、チャットに状態を永久キャッシュしてはいけない。

## 8. 他の実行方式との境界

本ファイルは **P3のChatGPT手動画像制作**だけに適用される。旧 `CHATGPT_NEXT.md`はP1〜P4全体の入口、`NEXT_COMMAND_CONTROLLER_v1.md`は従来版、`.github/workflows/slide-image-assets.yml`と`scripts/generate_slide_assets.py`はAPI版である。

**この方式ではGitHub Actionsを起動しない。OpenAI API secretも使わない。PPTXの編集は全15点が揃ってから別工程で行う。**

現状のlimitations: ChatGPT側での私有GitHubバイナリの直接取得、画像生成ツールへの参照転送、および生成されたPNGのGitHubへの書き戻しはツール/接続状態に依存する。確認できない作業を自動完了と報告しない。
