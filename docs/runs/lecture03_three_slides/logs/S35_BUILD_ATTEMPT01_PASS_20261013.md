# S35_BUILD — スライド35の表PPTX制作・品質検査

- step_id: S35_BUILD
- attempt: 1（初回のレイアウトで文字の重なりを検知し、**同工程内で行高・補足配置を改訂、再レンダリング**）
- 結果: **PASS（スライド35単体）**
- 対象: スライド35「入力チェック①：形式・範囲・存在」
- 準拠: design_system_general_final.md v2.1、content_visual_policy_final.md v2.6、docs/lecture03_48_selected_3_contents.md
- 成果物PPTX: `slide35_input_checks_editable_v1.pptx`
- 実レンダリング: `slide35_input_checks_editable_v1_preview.png`（1600 × 1200ピクセル）
- 監査文書: `S35_QC_report_v1.md`（詳細はチャットで納品）
- 出力先: ChatGPT作業環境 `/mnt/data/lecture03_step_run/slide35_pptx_table/`
- 編集可能な表: 3列×7行のネイティブPowerPoint表1点、**全21セル**を入力原文と厳密照合してPASS。画像数0点。スライド全体のアスペクト比4:3。
- タイトル・Intro2文・Takeaway2文: PPTX内部のテキスト文字列を原文と厳密照合PASS。補足2文は内容を保ち、単一行にまとめた（項目の文言は維持）。
- 主要配色: 白背景、見出し#41419E、本文#30323B、見出しセルに#F5F5FB、Takeawayに白地・紫の1.3pt直線枠。
- 指定書体: PowerPoint内に「源真ゴシックP」設定、代替フォント（Noto Sans系）でPDF/PNGを実レンダリング。源真ゴシックP実描画は未検証。
- 文字はみ出し: 初回レンダリングで見つかった表下段の字の重なりを行高調整で修正。最終プレビューは目視で大きな文字切れ・重なりなし。
- SHA-256(PPTX): `e75c471e59df41338b43771e9c1169f346b7d7193980e39340dea9d552f74548`
- SHA-256(PNG): `8ab9fb45a5950f14a0d98d24228cafb3a23fbd912223011490c4ddef5902a7b7`
- PNG/PPTX/PDF/QAバイナリは**GitHub未アップロード**。このチャットの実ファイルだけを納品している。
- 次工程: `S3_MERGE_QC`。スライド11／17／35の既存PPTXを順序どおりに統合し、原稿・画像・表・編集可能性・実レンダリングを3枚一括で確認する。以前のA/B/C比較E03は保留のまま。
