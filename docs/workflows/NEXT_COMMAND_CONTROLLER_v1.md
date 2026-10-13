# GitHub駆動「次」コマンドコントローラ v1.0

> **適用範囲：`YosukeSugiura/slide-master-ai` の `minor`、情報システム論第3回48枚版の現行 `P3_IMAGE_ASSETS`。2026-10-14採用。** このファイルはコントローラ（実行規則）であり、画像生成AIに渡すプロンプトではない。ChatGPTがチャットの流れから次に何を描くか判断することを禁止する。

## 0. この方式で「次」が意味するもの

- **現在P3にいる場合、「次」1回＝次の画像素材IDの1件分のみ処理**。合格ならそのIDだけ進め、次の素材IDを予約して応答終了。**同じ1回の「次」で2画像目を作らない**。
- **不合格なら同じ素材内で最大3試行（初回を含む）まで再試行可**。3試行ともFAILならその素材でBLOCKEDし、他の14点へ飛ばない。
- **1画像ごとの個別承認は不要**。ユーザーは次の進行を「次」と入力するのみ。進捗・素材指示・画像QCの正本はすべてGitHubに置き、成功した実画像はLibrary等の永続保存先に置く。
- **P1/P2/P4には既定の工程単位制御を適用**。P3についてのみ本書が `docs/workflows/CHATGPT_STEP_CONTROLLER_v2.md`／`docs/workflows/LECTURE_SLIDE_PRODUCTION_4PHASE_v1.md` の「次＝工程全体を一括実行」に優先する。4段階の役割分離は維持。
- 「次」は**当該ユーザーメッセージが来た時にのみ**実行。バックグラウンドで無断継続したり、後の「次」を自動発行したりしない。

## 1. 読み取り順・正本

1. `CHATGPT_NEXT.md`（入口。古い会話履歴に従わず最新を読む）。
2. `docs/runs/lecture03_48slides/step3/EXECUTION_STATE.json`（P3の**機械向け唯一の進行ポインタ**）。
3. `docs/runs/lecture03_48slides/step3/P3_asset_progress.json`（素材単位の**実施履歴／合格判定**）。
4. `docs/runs/lecture03_48slides/asset_manifest.json`（P1/P2の意味契約・配置・除外範囲・寸法）。
5. `docs/runs/lecture03_48slides/step2/image_prompts/P2_image_prompts_manifest.json`（P2の凍結仕様）。
6. `EXECUTION_STATE.json` の `next_prompt_file` **1ファイルだけ**。UTF-8の**本文全体が画像生成への唯一の内容指示**。ヘッダーや前置き、他の画像の指示・STEP完了の文章を結合しない。
7. 成功・失敗の詳細は `docs/workflows/PHASE_P3_IMAGE_ASSETS_RUNBOOK_v1.md`。

`docs/runs/lecture03_48slides/STATE.md` はユーザーに読むための要約として同期する。**機械ポインタはEXECUTION_STATE.jsonを正本**とし、内容が矛盾するなら実行せずBLOCKEDとして報告する。古い履歴は監査証跡であり状態に混ぜない。

## 2. データ事前検査・フェイルクローズ

次のうち1つでも満たさなければ**生成しない**。

1. branch=`minor`、run_id=`lecture03_48slides`、phase=`P3_IMAGE_ASSETS`、status=`READY`、next_action=`GENERATE_ONE_ASSET`。
2. `next_asset_id` がキュー内で最初の非PASS IDであり、`P3_asset_progress.json` の対象が `READY`、他の素材が同時RUNNINGではない。
3. `next_prompt_file` が存在して対象IDとprompt_versionが一致。指定した `next_prompt_blob_sha` が**GitHub fetch_fileのblob shaと完全一致**する。
4. 単一プロンプト本文にSTEP全体の進捗文面を連結しない。生成器呼び出し時の意図は**この1点だけ**。他の画像15点やパワーポイント作成などの指示を渡さない。
5. 画像生成手段・保存手段・QCの実行可能性を確認。追加課金サービスへ切り替える場合は別途ユーザーの事前承認が必要。ユーザーが指定したChatGPT画像生成を既定とする。
6. 事前10ゲート、意味契約・配置寸法・透過条件を照合。矛盾や改変は生成を停止。

## 3. 厳密なプロンプト運用と現実のツール制約

- GitHubの`step3/prompts/`にある`*.txt`ファイルは**前置きのない生成本文だけ**。状態ファイルやチャットのまとめは画像生成入力に入れない。
- **現環境のChatGPT画像生成ツールでは、APIに確定プロンプト文字列を渡す公開された編集可能な引数がない場合がある**。その場合、ChatGPTが内容を読んで生成器に意図を伝えることはできても、**厳密に同一バイト列がモデルへ渡ったことは機械検証できない**。`transport_verification="CONTEXT_ONLY_UNVERIFIED"`と記録し、正確に渡ったと主張しない。
- 重要：プロンプト伝達の不可観測性は画像のPASSを意味しない。**生成された実画像を独立QCで合格判定して初めて採用可**。誤った完了報告画像・別題材・PNGの見かけだけの市松模様は即FAIL。
- 外部の明示prompt引数を持つ生成ツールに無承認で乗り換えない。ユーザーがChatGPT画像生成を選んでいるので、可能な範囲で1素材のみのコンテキストに限定する。
- `*.txt`は**実行時にそのまま読む**。生成の場で素材本文を即興で書き直さない。改訂が必要なら新しい `prompt_vN.txt`をコミットし、旧版とQC履歴を保存し、最新stateのhash参照を付け替える。

## 4. 1素材のトランザクション

1. **開始直前**：GitHubの最新state／progress／prompt blob SHAを検証。RUNNINGの記録を保存できないなら生成しない。
2. `asset_id`, `prompt_version`, `prompt_blob_sha`をログに固定し、生成器へ**1件だけ**要求。
3. 生成後、実ファイルと文字通りの形式・サイズ・透過画素を調べる（**本物のRGBA透明**を要求。背景に市松模様が画像として描かれている場合はFAIL）。
4. 意味契約、矢印方向、独立性、文字混入、画風、余白、縮小可読性をQCする。**生成結果の「PASS」等の文字は証拠として扱わない**。3回まで該当IDのみ限定再試行。
5. PASSならPNG本体を再取得可能な場所へ保存、実SHA256を計算、`library_file_id`または検証済みGitHubのblobと名前を記録し**読み戻し確認**。保存先がURL期限付き・実存未確認ならPASSしない。
6. 結果とログを `P3_asset_progress.json` に保存・再読。**最後に** `EXECUTION_STATE.json`の参照SHAを指定して原子的に更新し、キュー内の次の未完了IDをセット。GitHubの更新競合が発生したら再読・調停し、二重生成をしない。
7. キュー15点が全件PASSの時だけP3終了判定→`STATE.md`を`P4_FINAL_PPTX`のREADYへ更新。画像をPPTXへ挿入するのは**別のユーザーの「次」**を待つ。

## 5. 状態とユーザー向け応答

`READY`＝次が実行可。 `RUNNING`＝同一資産処理中。 `BLOCKED`＝品質／保存／モデル能力不足。 `WAIT_CONFIRMATION`＝課金／重大な指示改訂等。 `DONE`＝P3全15画像が独立QCと保存PASS。

各「次」後は**対象素材ID、実際の採否、生成ファイルの保存先、次IDを短く返す**。FAIL／BLOCKEDなら理由を明記。未実施を「15/15完了」と偽らない。「状況」は読み取りのみで生成しない。

## 6. 従来の失敗履歴

- 過去のChatGPT画像生成3回による「STEP3完了報告風画像」は`S05-A-01`の**v1失敗履歴**。
- Figmaの`S05-A-01`の実画像は市松模様／透過不良・構図不合格で**採用しない**。プランクレジットを再消費する無承認Figma再実行は禁止。
- 今回新規に作成した`S05-A-01_prompt_v2.txt`は**修正された別版**であり、v1試行回数を消さず、v2の最大3試行枠を別に持つ。新規版の作成＝画像生成したことではない。
