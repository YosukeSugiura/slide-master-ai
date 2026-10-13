# ChatGPT講義スライド制作 — 標準入口（4段階）

> **現行の標準制作方式**（2026-10-13採用、P3は2026-10-14改訂）。ユーザーの初回制作プロンプトと「次」で、指示書→全ページPPTX骨組み→独立画像→画像組込・最終検査まで進む。**P3以外の「次」は原則ステージ単位。P3に限り「次」1回＝1画像ID**（GitHubの実行状態で決定）。一時的な実行上限なら同じステージの続きを次の「次」で再開する。品質ゲートを省いて成功扱いにしない。

## 最初に読む正本（順序厳守）

1. **現在がP3なら最優先**：`docs/workflows/NEXT_COMMAND_CONTROLLER_v1.md` → `docs/runs/lecture03_48slides/step3/EXECUTION_STATE.json` → `docs/workflows/PHASE_P3_IMAGE_ASSETS_RUNBOOK_v1.md`。画像IDと実行プロンプトはGitHubの最新STATEで決め、チャットの自由判断で選ばない。
2. `docs/workflows/LECTURE_SLIDE_PRODUCTION_4PHASE_v1.md` — 4段階の責務境界・全ページQC・工程間成果物。
3. `docs/workflows/CHATGPT_STEP_CONTROLLER_v2.md` — P3以外の基本制御。P3は専用NEXTコントローラが優先。
4. 対象デッキの `docs/runs/<run_id>/STATE.md` — **デッキ固有**の人間向け進捗。P3の機械的な次タスクは `step3/EXECUTION_STATE.json` が唯一の正本。新規デッキには別STATEを作る。この第3回48枚版では `docs/runs/lecture03_48slides/STATE.md`。
5. `design_system_general_final.md` v2.2、`content_visual_policy_final.md` v2.8、当該原稿、`docs/IMAGE_GENERATION_STAGED_WORKFLOW_v2.md`、当該講義で承認されたデザイン基準。

**旧手順との優先順位**：`docs/workflows/CHATGPT_STEP_CONTROLLER_v1.md`、`docs/workflows/LECTURE03_ABC_AND_3SLIDES_v1.md`、`docs/IMAGE_GENERATION_STAGED_WORKFLOW_v1.md`、試作3枚のSTATEは**履歴・参考**。新規制作時にそれらの素材別・1画像別「次」方式を標準へ戻さない。

## 4段階の入力と納品

| ユーザー入力 | ステージ・担当 | 必須成果物 |
|---|---|---|
| **① 最初の制作プロンプト** | `P1_SPEC` / 原稿・構成設計 | 全ページ定義書と素材インベントリ。**画像/PPTX生成はしない** |
| **② 「次」①** | `P2_PPTX_SKELETON` / **PowerPoint制作** | **全ページの編集可能な画像未挿入PPTX**・全ページの実プレビュー・画像枠確定・**全画像の生成指示書**。画像生成はしない |
| **③ P3の「次」（画像IDごと）** | `P3_IMAGE_ASSETS` / **画像生成** | **「次」1回で指定の画像ID1点だけ**を生成・QC・保存。15点PASSになるまで繰り返す。**PPTXを作成・修正しない** |
| **④ P3全15点完了後の「次」** | `P4_FINAL_PPTX` / **PowerPoint制作** | 合格素材のみ挿入した完成PPTX、全ページ再レンダリング・原文/図/表/編集可能性QC。画像生成しない |

`P1_SPEC` の初回プロンプトは、対象講義と元原稿（GitHubファイル名・添付ファイルなど）を特定する。対象が情報システム論第3回の48枚なら「情報システム論第3回・48枚版をこの4段階で開始」と指定すればよい。**単に「次」だけでは初回プロンプトの代用にしない。**

## 短い操作

- **次／はい**：P3では `step3/EXECUTION_STATE.json` に書かれた**1素材IDだけ**実行し、実ファイルQCと保存を確認して次IDをセットする。2枚目には進まない。P1/P2/P4は従来どおり工程単位。
- **状況／確認**：最新STATE・実在する成果物・不合格項目を報告。作業/進捗更新はしない。
- **やり直し**：失敗した1素材の履歴を確認し、同一版の最大試行回数を超えない範囲で再試行。新版ならファイル追加＋版更新し、旧版の失敗を消さない。合格済みは維持。
- **止めて／再開**：中断・再開（再開はREADYにするだけ）。
- **P3の一意な入力**：`EXECUTION_STATE.json`の `next_prompt_file` の**ファイル本文だけ**を画像生成対象とする。GitHubの文書や会話に記載された「STEP全体の完了」などは画像生成入力に混ぜない。必須入力、保存先、意味契約、原稿が曖昧なら確認かBLOCKED。実行上限で中断した場合は進捗保存して同じステージから続行。

## デザイン・権限の固定

- 情報システム論第3回では**承認された再設計版**（`docs/workflows/LECTURE03_APPROVED_VISUAL_BASELINE_20261013.md`）を採用。大きい主図・余白・白/インディゴ、源真ゴシックP、補足まとめ文は必要な場合だけ**18pt・薄灰#F3F4F6**、Takeawayと意味重複させない。元原稿・表・専門用語は厳密照合。
- 画像分類A/B/Cと、旧実験の「画像先行/PPTX先行/同時依頼」は混同しない。分類Cは画像生成なし。
- GitHub minorは非公開のまま。承認なしの外部有料Image API、Codex CLI/Cloudへの自動委譲、原稿の変更・公開化は禁止。
- **バイナリ永続化を検証**：GitHubのログだけでPPTX/画像が保存されたと主張しない。別セッションでも再開できる保存先がない場合はその問題を記録し、未達状態で止める。

新しいチャットで続ける場合は「`YosukeSugiura/slide-master-ai` の `minor/CHATGPT_NEXT.md` を読み、現行4段階方式で続けて」と指示する。
