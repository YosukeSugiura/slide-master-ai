# マルチメディア論 第3回 — 制作入口

## 講義条件
- テーマ：画像解析 — 画像特徴量、画像エンコーダと応用
- 100分、講義のみ。学生のColab演習は実施しない。
- 全61枚の構成案を基準とする（制作過程で内容・時間配分を検証）。
- 教員側でPythonを実行した画像処理・CNN・Autoencoderの結果をスライドへ掲載する。
- 次の音声講義後に画像・音声の演習をまとめて実施する予定。

## 適用する共通規則
- 正本：major/design_system_general_final.md
- 視覚表現：major/content_visual_policy_final.md
- 制作工程：major/docs/workflows/LECTURE_SLIDE_PRODUCTION_4PHASE_v1.md
- 画像生成補助：major/CHATGPT_IMAGE_NEXT.md（生成AI画像が必要な場合のみ）
- ブランチ運用：major/GITHUB_BRANCH_POLICY.md
- 4:3、源真ゴシックP、編集可能なPPTXを基本とする。
- 定量結果・画像処理出力・学習済みモデルの中間特徴は実コードの出力を使用し、生成AIで偽装しない。

## 制作段階
1. P1：61枚の内容、意味契約、図の分類と実験仕様を確定
2. P2：編集可能なPPTX骨組み、実レンダリング、素材枠を確定
3. P3：必要な独立AI画像のみ生成・検証。Python実験は別途再現可能なコードと出力を保存
4. P4：素材統合、全ページレンダリング、内容・フォント・品質検査

## 保存先（予定）
- docs/slide_plan.md — スライドごとの詳細設計
- experiments/ — 実験コード、環境定義、再現手順
- results/ — 実験結果、評価値、可視化画像
- materials/ — PPTX、スライド参照画像
- assets/accepted/ — 採用済みの生成AI素材（必要な場合）
- docs/runs/ — 制作記録・検証結果

## 注意
現時点でブランチとこの入口文書のみ作成済み。実験結果、PPTX、PNGは未作成。
