# 情報システム論第3回 — 制作参照ファイル

このブランチ内には画像生成時の参照資料が個別ファイルで保存されています。

- `lecture03_48slides.pptx`：PowerPoint STEP2版、48枚。画像の挿入枠15箇所が存在。完成版ではありません。
- `slide_references/S05.jpg`, `S06.jpg`, `S10.jpg`, `S11.jpg`, `S15.jpg`, `S17.jpg`, `S18.jpg`, `S26.jpg`：実スライドの全体参照画像（元のSTEP2 PDFをレンダリング）。文字フォントは代替表示であり、完全一致ではありません。
- `style_references/S05-A-01.webp`, `S06-B-01.webp`：承認済み素材を参照しやすいWEBPに変換したサンプル。**内容をコピーしてはいけない**。
- `../assets/accepted/S05-A-01.png`, `S06-B-01.png`：承認済み素材の**実PNG（透明背景）**。
- `asset_index.json`：SHA256/実サイズ一覧。

講義固有の固定生成指示書は `../docs/runs/lecture03_48slides/step3/prompts/` に15点分の版管理付きで保存。共通指示は**`major/CHATGPT_IMAGE_NEXT.md`** が正本。

画像生成時にはPPTXそのものの再生成やスライド画像の丸ごとの複製をしない。
