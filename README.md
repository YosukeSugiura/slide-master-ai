# slide-master-ai — Claude for PowerPoint 専用の講義スライド制作定義

明治大学の講義スライドを **Claude for PowerPoint のみで制作**するための，共通デザイン定義と依頼プロンプトです．

## 制作担当の分担（必須）

- **Claude for PowerPoint（唯一の制作担当）**：スライドの作図・レイアウト・編集可能なPPTX生成・既存PPTX編集・図や画像の配置・全ページのレンダリング検査・完成版の納品を行う．
- **ChatGPT（制作前の支援のみ）**：講義内容の整理，学習目標・章構成・各章の概要案，ページ設計表，Claude for PowerPointに渡す制作依頼文やブリーフの作成，技術的な内容のレビューを行う．**スライド本体・PPTX・完成スライド画像を生成，編集，納品しない**．
- ChatGPTにスライド制作を依頼された場合でも，PPTXの制作を開始せず，Claude for PowerPointに渡す内容資料・制作指示書を用意する．
- 過去ブランチに残るChatGPT向けのPPTX制作コード・画像生成フロー・制作ログは**履歴・参考資料**であり，現行のスライド制作手順ではない．

## ファイル

| ファイル | 役割 |
|---|---|
| [design_system_general_final.md](design_system_general_final.md) | **骨格**：4:3，源真ゴシックP，色，章ラベル・タイトル・ページ番号，Takeawayの書式と文章基準 |
| [content_visual_policy_final.md](content_visual_policy_final.md) | **中身と手順**：ページ設計表，構図の選び方，図の品質基準，実測素材，レンダリング検査 |
| [prompts/lecture_slides_quick_prompt.md](prompts/lecture_slides_quick_prompt.md) | **毎回の依頼文**（講義名・回・内容資料・厳守事項を書き換えるだけ） |
| [prompts/lecture_brief_template.md](prompts/lecture_brief_template.md) | 条件が多い回のブリーフとページ設計表 |
| [docs/audit_2026-10-21.md](docs/audit_2026-10-21.md) | v3.0改訂の根拠（2つの講義デッキの比較監査） |

## 考え方：枠は固定，中身は自由

| 厳守（全講義共通） | Claudeが内容に応じて判断 |
|---|---|
| 4:3，源真ゴシックP，白背景とインディゴ系 | タイトルの文言（主題・問いを1行） |
| 章・セッション情報はタイトルの上 | 本文量，説明の言い回し |
| フッターなし，ページ番号は右下 | 図解・構図・写真や図の採否 |
| Takeawayの書式（白地・細枠・24pt Bold・中央） | スライドの分割・統合，Takeawayの要否（原則あり） |
| 数式・技術的事実・実測データの正確性 | 枚数（「目安」の場合） |

## 毎回の依頼（最短）

[prompts/lecture_slides_quick_prompt.md](prompts/lecture_slides_quick_prompt.md) のコードブロックをコピーし，4項目を書き換えて**Claude for PowerPointへ送ります**．

## ブランチ

- `main`：**共通定義の正本**（このブランチ）．
- `マルチメディア論第3回` などの講義名ブランチ：その講義の設計書・素材・制作記録．
- `major`・`minor`：ChatGPT向けの旧定義と画像生成の履歴（参照用）．

## 版

- 運用更新（2026-11-04）：スライド制作・PPTX生成・編集・レンダリング・納品をClaude for PowerPointの専任とし，ChatGPTは内容検討と制作指示書に限定．

- v3.0（2026-10-21）：監査に基づき全面改訂．Takeawayを情報システム論第4回の書式に戻し，文章基準を追加．タイトルは1行に収め，主題・問いを基本とした．ページ設計表の工程を追加．ChatGPT向けの試作手順と重複規則を削除．
- 旧版：`e3ae7ac`（v2.1，2026-10-21改訂前），`d47cfa9`（v2.0，2026-10-14）．Git履歴から参照できます．
- `.github/workflows/slide-image-assets.yml` は画像生成用の別ワークフロー（`minor` ブランチ用）で，本定義とは独立しています．
