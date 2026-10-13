# STEP3 Figma画像生成パイロット記録 — 2026-10-14

## 前提

- 対象：`S05-A-01`、プロトタイピングの反復。GitHub `docs/runs/lecture03_48slides/step2/image_prompts/S05-A-01_prompt_v1.md` の本文を読み込み、**明示的な文字列でFigma generate_imageに送付**した。
- 利用モデル：`gpt-image-2.5-sunburst`。指示画角1472×1000px。Figma生成画像は1536×1024px（画像生成はFigma AIクレジット消費）。
- 生成結果：API応答は**画像生成成功**、PNG配布URLあり。これは**品質PASSを意味しない**。
- 配布URL：`https://www.figma.com/api/mcp/asset/a6d1cfe7-3594-4bea-a8cf-8a60781e1f26.png`（応答の有効期限7日、約2026-10-21まで）。
- **重要：永続的な画像保存・画像の意味契約QCは未達**。外部URLのコンテナダウンロードがDNS/アクセス制限で失敗し、GitHub/LibraryへのPNGのアップロードとSHA256取得・実画像検証ができていない。リンク期限までにPNGをダウンロードして再添付する必要がある。

## 判定と今後

- `S05-A-01`：**GENERATED_UNRETRIEVED_UNVERIFIED**（合格0）。2026-10-14の従来ChatGPT image generation失敗3回は履歴として保持。Figma経路の試行は別方式の初回。
- Figmaに接続できることと、**原稿の個別プロンプトを実際に送れることは確認した**。画像が指定内容かどうか、画風・矢印・透過背景・縮小時の可読性は**未確認**。
- 別途、画像が外部から取得できる安定した方法を確認してから、素材単位の個別QC→保存→次の素材、という順番へ移行する。
- **残14点の生成は未実施**、P3はまだ未完了（P4へ進まない）。追加Figmaクレジットを勝手に消費する連続生成は行わない。
