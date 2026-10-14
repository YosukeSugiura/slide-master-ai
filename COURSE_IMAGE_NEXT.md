# 情報システム論 第3回 — ChatGPT画像制作（簡易入口）

対象リポジトリ: `YosukeSugiura/slide-master-ai` ／ ブランチ: **`情報システム論第3回`**
共通ルール: **`major/CHATGPT_IMAGE_NEXT.md`**（最新版）

## 新しいチャットで最初に送る文

> GitHubの`major/CHATGPT_IMAGE_NEXT.md`と`情報システム論第3回/COURSE_IMAGE_NEXT.md`、同ブランチの`IMAGE_QUEUE.md`を読み、画像制作を再開してください。最初は確認だけ。以後は「次」で1点生成、「やり直し」で修正、「完成」でまとめて納品してください。GitHub Actionsや外部APIは使わないでください。

## 画像生成時に使うファイル
- **進捗の正本**：`IMAGE_QUEUE.md`。旧`EXECUTION_STATE.json`／`P3_asset_progress.json`は過去の厳格版の履歴であり、**現在の進行ポインタとして使わない**。
- **固定個別プロンプト**：`docs/runs/lecture03_48slides/step3/prompts/{ID}_prompt_vN.txt`。制作テーマ・意味・必須フローを確認する。厳しすぎる構図・文字数・寸法の制約は共通の簡易ルールで緩和。
- **スライド全体の参照画像**：`materials/slide_references/S05.jpg`, `S06.jpg`, `S10.jpg`, `S11.jpg`, `S15.jpg`, `S17.jpg`, `S18.jpg`, `S26.jpg`。
- **画風参照**：`materials/style_references/`、`assets/accepted/`。
- **最終組み込み用PPTX**：`materials/lecture03_48slides.pptx`（現段階では編集しない）。

## 操作
- **次**：直前の画像を採用して（最初はキュー先頭から）次の図を**1枚だけChatGPTで生成**。GitHubアップロードやQC JSON更新では止めない。
- **やり直し**：同じIDを1枚再生成する。
- **完成**：採用画像のPNGを一括収集しZIP化、続いてPPTXへ組み込む。実ファイルの取得可能性は確認し、欠けているものだけ申告する。
- 必要なら「状況」でチャット内の採用状況を確認。

## 現在の引継ぎ
**4/15点をユーザーが採用済み。次は S11-B-01。**
S05-A-01／S06-B-01／S06-B-02のPNGはGitHubに保存済み。**S10-A-01は円形の合格画像がChatGPTのファイルライブラリに存在するが、GitHubへのPNG保存はまだ**。再生成せず、完成時に回収する。

手順図・循環図・比較図には、パーツごとの工程名、役割名、成果物名など**必要な文字ラベルを積極的に入れる**。文字数・語数に一律上限を設けない。

`minor`の旧指示、厳格QC、コミットやSHAを毎回要求する処理は使用しない。新しいChatGPTチャットでもユーザーへ毎回のファイルアップロードを求めない（必要な参照の読み込みがどうしてもできない場合のみ相談）。
