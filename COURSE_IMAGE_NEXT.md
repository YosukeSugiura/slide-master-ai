# 情報システム論 第3回 — 画像制作の入口

**制作対象ブランチ：`情報システム論第3回`**（このブランチ）  
**共通ルール正本：`major/CHATGPT_IMAGE_NEXT.md`**  
**PPTX／JPG／PNG実体：この講義ブランチ内の `materials/`, `assets/`**

## 新しいChatGPTチャットに入力する1文

> GitHubの `YosukeSugiura/slide-master-ai` で `major/CHATGPT_IMAGE_NEXT.md` を読み、次に `情報システム論第3回/COURSE_IMAGE_NEXT.md` を読んでください。初回は現在の進捗確認だけにし、以後「次」で画像を1点だけ生成・品質検査・講義ブランチへ保存して進捗更新してください。GitHub Actions/APIは使わないでください。

## 毎回の処理

1. **共通ルールを先に読む**：`major/CHATGPT_IMAGE_NEXT.md`。古い `minor/CHATGPT_NEXT.md` とGitHub Actionsは優先しない。
2. **この講義の最新状態**：`docs/runs/lecture03_48slides/step3/EXECUTION_STATE.json` と`P3_asset_progress.json`、`asset_manifest.json`。
3. **次の固定生成指示書**：`EXECUTION_STATE.json.next_prompt_file`。現時点は`S06-B-02_prompt_v3.txt`。毎回Git blob SHAと照合し、古いv2を実行しない。
4. **画像でスライドの文脈を確認**：`materials/slide_references/Sxx.jpg`（8ファイル）。画風参照 `materials/style_references/` と承認済み `assets/accepted/`。
5. **生成するのは独立素材PNG1点のみ**。生成前後の検査・GitHubへ保存と実SHA照合・状態更新は `major` の手順を厳守する。スライド全体を生成しない。
6. チャットの初回読み込みでは画像を生成せず、ユーザーの「次」を待つ。

## 現時点の引継ぎ（数字は初期状態の説明のみ）

- 全15点：**S05-A-01とS06-B-01の2点がPASS**。PNGは`assets/accepted/`へ保存済み。
- 次のID：**S06-B-02（v3／READY／0試行）**。元のv2の失敗4試行を消してはいけない。
- GitHub素材：`materials/lecture03_48slides.pptx`（STEP2骨組み48枚）、`materials/slide_references/`（8 JPG）、`materials/style_references/`（2 WEBP）、`assets/accepted/`（2 PNG）。
- `materials/asset_index.json`に個々のファイルのSHA256とバイト数。元PPTXの正式フォント描画は未検証。
- 画像15点完成後のPPTX挿入は別工程。**このチャットではPPTXを改変しない**。

## 保存先と失敗の扱い

- PASS: `assets/accepted/{asset_id}.png`
- FAIL: `assets/rejected/{asset_id}_prompt_vN_attemptK.png`
- QC/進捗: `docs/runs/lecture03_48slides/step3/qc/`, `P3_asset_progress.json`, `EXECUTION_STATE.json`

**ChatGPTツールがGitHub上の画像バイナリを視認できない場合**は必要なSxx.jpg・画風画像を初回のみ添付してもらう。**生成PNGをGitHubへ直接書き戻せない場合**も、保存完了とはせず、その場でユーザーに手動アップロードを依頼する。実際の保存と内容確認なしに「次」へ進めない。
