# P3画像制作 — GitHub Actions / OpenAI API 実行手順

## 目的と配置（2026-10-14）

- 手動入力「次」に依存せず、GitHub Actions が `minor` の素材キューを順に処理する。
- GitHubの既定ブランチは `main`。起動用ワークフローは **`main:.github/workflows/slide-image-assets.yml`** に置く。実行時は明示的に `minor` をcheckoutする。
- 実行コードは **`minor:scripts/generate_slide_assets.py`**。
- ステージ状態は `minor:docs/runs/lecture03_48slides/step3/EXECUTION_STATE.json`。進捗 `P3_asset_progress.json`。P2意味契約 `asset_manifest.json`。
- 固定プロンプトは `EXECUTION_STATE.next_prompt_file` の本文だけを使い、Git blob SHA-1の一致を事前に検証。生成器の `images.edit(prompt=...)` 引数へそのまま入力。`image` 引数にはSxxの実スライドと合格済み画風参照を2点指定する。
- **OpenAI APIの追加従量課金が発生する**。GitHub Actions利用料金もプランの制約に従う。ChatGPT Plusに含まれる料金ではない。

## 初回操作

1. リポジトリ **Settings → Secrets and variables → Actions → Repository secrets** に `OPENAI_API_KEY` を登録（済み）。キーの値は画面・ログ・ファイルにコピーしない。
2. GitHubの **Actions** タブで **Slide P3 image assets** を選択し、**Run workflow** をクリック。
3. まず `mode=single`、`max_calls=1`、`dry_run=true` のまま実行。**API料金なしで固定プロンプト、元PPTX SHA、画像枠、スライド参照、画風サンプルを検証**して終わる。実画像は作らない。
4. 検査成功後、同画面から `dry_run=false`、`mode=single`、`max_calls=1` で実行すると **S06-B-02 v3 を1回だけ**生成する。画像生成API1回に加え、PNG形式・alpha・縦横比を通過した場合は別途意味QC用のVision APIを1回呼ぶ。
5. APIには **48枚版PPTXの該当スライドの画像**と**承認済み画風参照**も渡す。生成結果を元PPTXの物理的な画像枠に重ねた `step3/previews/*_on_slide.png` で意味・可読性・周囲の文字との衝突を追加QCする。PASSなら `minor` の `step3/accepted/` にPNG本体・SHA256・QC・進捗・配置プレビューをcommit/pushする。FAILは `step3/rejected/` にPNGとQCおよび可能なら配置プレビューを記録し、試行上限を守る。
6. 単体結果を確認して問題がなければ `mode=batch`、`max_calls=15`、`dry_run=false` などで再実行。15は**今回の起動で許可する最大画像生成リクエスト数**であり、残り画像数ではない。FAILで同じ素材を再試行する回数も消費する。1回の起動につき1〜30回の範囲で指定できる。

## 完了・停止条件

- 現在採用済み2/15。S06-B-02 v2の不採用4件は保護し、v3は未生成、初回試行からの再開。
- 一度に1件の画像素材だけを処理・記録。失敗した同素材は **vNごとに3試行**まで。3度FAILなら `BLOCKED` で停止し、次の素材へ勝手に飛ばない。
- API起動直前に `RUNNING` をGitHubへ記録するため、ワーカーやネットワークが途中停止した場合は自動で再実行しない。ログを調査して回復・精算してから再開する（重複課金防止）。
- `single` では起動につき画像API **最大1回**、`batch` は `max_calls` で上限。OpenAI側の正確な金額上限ではない。プロジェクト側でも支払い上限・利用状況を確認する。
- AIの意味判定は人の検査と同等ではない。特にS06の矢印や教育上の意味は、初回の実画像を確認し、懸念があれば採用を差し戻す。
- Pythonの作業場所・ローカルPC環境は不要。ワークフローには `permissions: contents: write` が必要。組織/リポジトリの制限設定が勝る場合はActions実行が失敗する。
- `main` 上のワークフローが起動入口なので、`minor` だけでスクリプトを書き換えても起動UIは変わらない。
- ユーザーが明示的に実行するまで新たなAPI課金は発生しない。自動スケジュール・pushトリガーは設定していない。
- PPTXは本ワークフローで作成・変更しない。15件PASSの後で別工程P4に移る。

## 実装根拠

- OpenAI Images API `images.edit`: `gpt-image-2.5-sunburst`、`background=transparent`、`output_format=png`、倍数16のカスタム解像度を使用。
- OpenAI Responses API: `gpt-6-sol`で画像内容を独立判定（structured JSON）。
- GitHub Actions `workflow_dispatch` は原則デフォルトブランチのワークフローが必要なため、入口のみ `main` に設置。

参考: https://developers.openai.com/api/docs/guides/image-prompting
https://developers.openai.com/api/reference/python/resources/images/methods/generate
https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow

## PPTX実体と視覚検査（2026-10-14改訂）

- 永続参照バンドル：`minor:docs/runs/lecture03_48slides/step3/reference/lecture03_p3_context.zip`。同ディレクトリの`.sha256`と一致しないものは使用しない。
- バンドルには元の編集可能な **STEP2 48枚版PPTX（SHA256: 989a2a25a9469c8d3777289430ab415bd2d5f9636dbf0d969c10c7c1f0406506）**、画像枠を持つ8枚（S05/S06/S10/S11/S15/S17/S18/S26）のレンダリング画像、合格済みのS05-A-01/S06-B-01の画風参照を保存した。48枚PPTXと参照レンダリング画像の整合は元PPTX上の実寸画像枠と素材IDのテキストを検証して担保する。
- 画像参照はSTEP2のPDFレンダリング（**フォントは代替表示**）を使用する。元PPTXのフォントやレイアウトの完全一致を保証するものではないが、実スライドの構成と配置枠は検査する。
- `scripts/p3_slide_context.py` が元PPTXから画像枠の座標と素材IDを再検証し、画像生成時の参照画像2点を用意する。AI意味検査には「独立画像」「実スライド」「実挿入プレビュー」「同講義の合格済み図」の4画像を渡す。仮配置はPILによる**スライドプレビュー**でありPPTXは未更新。
- `tests/test_p3_slide_context.py` は15箇所すべての素材IDと画像枠を元PPTXから照合する。GitHub ActionsのPython依存に`python-pptx`と`pytest`を追加し、画像生成前に無課金でテストする。
- 素材内容に異なる図があればAI QCが不合格と判定する設計だが、**AI QCは完全ではない**。最初のS06-B-02出力を人の目で確認してから残りの自動一括処理へ移行すること。
- SOURCEのライブラリ版とこのバンドルは別の保存コピー。PPTXやデザインを更新したら **参照バンドルとそのSHA256を作り直すこと**。自動的な同期は行わない。
- 画像生成はユーザーが`dry_run=false`を指定した時のみ実行。実API接続と画像の品質はまだ検証していない。

