# マルチメディア論 第3回 — 講義制作の入口

## 現行の内容指定（P1 v3：2026-10-15）
- **現行正本：[docs/p1_v3/README.md](docs/p1_v3/README.md)**
- 全49枚・100分・学生Colab実習なし。49枚の各スライドにタイトル、Intro、表示用要点、図の意味・計算条件、Takeaway、方式A/B/Cを定義。
- 各章の詳細：docs/p1_v3/01_foundations_S01-S10.md、02_filtering_S11-S22.md、03_encoding_S23-S31.md、04_cnn_S32-S39.md、05_autoencoder_S40-S49.md。
- 実験の再現条件：docs/p1_v3/06_experiment_contracts.md。
- 中心の問い：「画像から何を取り出し、何を残せば、目的の処理ができるのか？」
- シラバス対応：第3回「画像解析：画像特徴量，画像エンコーダと応用」。第2回は機械学習・深層学習、第4回は音声、第6回は画像・音声解析演習。

## 共通制作条件（majorの正本）
- major/design_system_general_final.md：4:3、源真ゴシックP、文字階層・配色・Takeaway・編集性。
- major/content_visual_policy_final.md：意味契約と分類A/B/C、制作工程P1→P2→P3→P4、画像生成指示・独立検証。
- major/CHATGPT_IMAGE_NEXT.md：画像生成が必要な場合の簡易運用。
- major/GITHUB_BRANCH_POLICY.md：講義ごとのブランチに制作物を保存する。

## 旧設計と現在の状態
- docs/slide_plan.md：旧61枚構成（履歴）。
- docs/slide_plan_v2.md と docs/p1_v2/：旧49枚の章別再構成案（履歴）。
- 過去のPPTX・実験画像・Python成果物はv3の正本ではなく、品質確認を経ない限り流用しない。
- **v3は現在P1の内容設計段階。PPTX/PDF・実験結果・独立画像は新たには制作していない。**
- P2は全ページ編集可能なPPTX骨組みと実レンダリング、P3は必要なA/B画像素材、P4は合格素材の統合と最終QC。数値・実験図は正確なプログラム描画を使用する。
