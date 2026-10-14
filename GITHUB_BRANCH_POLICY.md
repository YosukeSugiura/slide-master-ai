# GitHubブランチ設計 — 共通指示書と講義データの分離

- `major`：**共通指示の正本**。`CHATGPT_IMAGE_NEXT.md`・共通デザイン文書・ブランチ方針。講義のPPTX/JPG/PNG/進捗は置かない。
- `情報システム論第3回`など**各講義名のブランチ**：当該講義の実ファイル、素材スロット、15件等の固定プロンプト、画像、QC、状態JSONを管理。
- `main`：既存のリポジトリ既定ブランチ。今回変更しない。
- `minor`：従来の実験と履歴。削除せず当面アーカイブ用途。新規制作の正本にしない。

## 講義ブランチの推奨ファイル配置

```
COURSE_IMAGE_NEXT.md
materials/
  README.md
  asset_index.json
  lecture03_48slides.pptx
  slide_references/S05.jpg, S06.jpg, ...
  style_references/S05-A-01.webp, S06-B-01.webp
assets/accepted/S05-A-01.png, S06-B-01.png, ...
assets/rejected/  # 必要な場合のみ
docs/runs/<run_id>/
  asset_manifest.json
  step3/prompts/{asset_id}_prompt_vN.txt
  step3/EXECUTION_STATE.json
  step3/P3_asset_progress.json
  step3/qc/
```

- `major`へのルール修正は新しい共通バージョンとして追跡。講義の文脈や個別指示を`major`へ混ぜない。
- 講義ブランチの内容はその講義だけを正本とし、新しい講義を追加する際は`major`の共通ルールを読み込んだ上で専用ブランチを作る。
- リポジトリのデフォルトブランチを切り替えない。既存履歴の書き換え・強制プッシュ・既存素材の削除をしない。
