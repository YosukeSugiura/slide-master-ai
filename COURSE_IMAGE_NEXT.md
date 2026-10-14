# 情報システム論 第3回 — 画像制作の入口

**制作対象ブランチ：`情報システム論第3回`**（このブランチ）  
**共通ルール正本：`major/CHATGPT_IMAGE_NEXT.md`**  
**PPTX／JPG／PNG実体：この講義ブランチ内の `materials/`, `assets/`**

## 新しいChatGPTチャットに入力する1文

> GitHubの `YosukeSugiura/slide-master-ai` で `major/CHATGPT_IMAGE_NEXT.md` を読み、次に `情報システム論第3回/COURSE_IMAGE_NEXT.md` を読んでください。初回は現在の進捗確認だけにし、以後「次」で画像を1点だけ生成・品質検査・講義ブランチへ保存して進捗更新してください。GitHub Actions/APIは使わないでください。

## 図中ラベルの扱い（共通ルール更新：2026-10-14）

`major/CHATGPT_IMAGE_NEXT.md` の **「最優先：説明図の文字・ラベル方針」** を現在の画像生成・QCに適用する。工程図、循環図、比較図で必要な工程名・役割名・成果物名・状態名・短い補助説明は積極的に記入してよい。各部品を無記名にしない。一律の「1～2語」「ラベル2個まで」「原則無文字」という古いルールは使用しない。

既存の個別 `prompt_vN.txt` にある字数・ラベル個数の目安は努力目標とし、**教育上必要なラベルを省略する根拠にはしない**。ただし固定プロンプトの内容・名称・工程の意味関係は守り、勝手に逆向き・別工程に変えない。古いQCの無文字判定も上書きして扱い、元のFAIL履歴は保持する。

現在 `S10-A-01` は画像生成済みの候補をレビュー中（`WAIT_CONFIRMATION`）。**新しい「次」で重複生成しない**。採否と保存が確定したらstateに従って進める。

## 毎回の処理

1. **共通ルールを先に読む**：`major/CHATGPT_IMAGE_NEXT.md`。古い `minor/CHATGPT_NEXT.md` とGitHub Actionsは優先しない。
2. **この講義の最新状態**：`docs/runs/lecture03_48slides/step3/EXECUTION_STATE.json` と`P3_asset_progress.json`、`asset_manifest.json`。
3. **次の固定生成指示書**：`EXECUTION_STATE.json.next_prompt_file`。最新の対象と版は必ずstateから取得し、毎回Git blob SHAと照合する。現時点の対象は`S10-A-01_prompt_v2.txt`（レビュー待ち）。最新stateで採否・次IDを再確認する。
4. **画像でスライドの文脈を確認**：`materials/slide_references/Sxx.jpg`（8ファイル）。画風参照 `materials/style_references/` と承認済み `assets/accepted/`。
5. **生成するのは独立素材PNG1点のみ**。生成前後の検査・GitHubへ保存と実SHA照合・状態更新は `major` の手順を厳守する。スライド全体を生成しない。
6. チャットの初回読み込みでは画像を生成せず、ユーザーの「次」を待つ。

## 現時点の引継ぎ（数字は初期状態の説明のみ）

- 全15点：**S05-A-01、S06-B-01、S06-B-02の3点がPASS**。PNGは`assets/accepted/`へ保存済み。
- 確認中のID：**S10-A-01（v2／WAIT_CONFIRMATION／3試行）**。S06-B-02のv3はユーザーによる教材採用を受け、透明余白の修正だけでPASSとした。旧不合格履歴は保存。
- GitHub素材：`materials/lecture03_48slides.pptx`（STEP2骨組み48枚）、`materials/slide_references/`（8 JPG）、`materials/style_references/`（2 WEBP）、`assets/accepted/`（3 PNG）。
- `materials/asset_index.json`に個々のファイルのSHA256とバイト数。元PPTXの正式フォント描画は未検証。
- 画像15点完成後のPPTX挿入は別工程。**このチャットではPPTXを改変しない**。

## 保存先と失敗の扱い

- PASS: `assets/accepted/{asset_id}.png`
- FAIL: `assets/rejected/{asset_id}_prompt_vN_attemptK.png`
- QC/進捗: `docs/runs/lecture03_48slides/step3/qc/`, `P3_asset_progress.json`, `EXECUTION_STATE.json`

**ChatGPTツールがGitHub上の画像バイナリを視認できない場合**は必要なSxx.jpg・画風画像を初回のみ添付してもらう。**生成PNGをGitHubへ直接書き戻せない場合**も、保存完了とはせず、その場でユーザーに手動アップロードを依頼する。実際の保存と内容確認なしに「次」へ進めない。
