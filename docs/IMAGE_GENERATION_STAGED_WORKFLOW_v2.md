# 独立図の一括制作手順 v2.0 — 4段階方式STEP3専用

> 正本：`docs/workflows/LECTURE_SLIDE_PRODUCTION_4PHASE_v1.md`。分類A/B/Cと意味検証は`content_visual_policy_final.md` v2.8。旧`docs/IMAGE_GENERATION_STAGED_WORKFLOW_v1.md`は手動レビュー等の歴史的記録で、本標準ルートでは利用しない。

## 2026-10-14改訂：P3の実行粒度の優先規則

**現在のSTEP3では「次」1回でキュー先頭の画像ID1点だけを処理する。** 本書後述の「全未完了素材を連続して処理」「次1回＝工程全体」等の旧運用説明より、`docs/workflows/NEXT_COMMAND_CONTROLLER_v1.md` と `docs/workflows/PHASE_P3_IMAGE_ASSETS_RUNBOOK_v1.md` が優先する。すべての画像指示は `step3/prompts/{asset_id}_prompt_vN.txt` から1点分のみ取得し、画像生成器に進捗管理・他素材・完了報告の文言を渡さない。RGBA透過・実ファイル検査と保存証跡を必須とし、**15点すべてPASSするまでP4に移行しない**。

## 前提と責務

- STEP2で**実PPTXの画像挿入枠を確定し、画像IDごとの指示書・事前10ゲートをPASS**させてあること。
- STEP3が生成するのは**PNGなどの独立画像素材だけ**。PPTX骨組みの編集、図のPPTX後付け修正、スライド全体のレンダリングはSTEP4の担当。
- 同じChatGPT通常チャットで多数の素材を**順次**処理する。1回の画像生成ツール呼出しの対象は常に**1つの素材IDに対応する1画像**。「次」1回は全素材を処理するための大工程承認であり、1素材ごとの承認を求めない。
- 手動で全プロンプトを個別承認したいというユーザーの明示要求がある場合のみ、個別レビュー型へ切り替える。通常は追加Image APIの課金なし。

## 入力は素材ID別manifestのみ

最低限： `run_id,slide_id,asset_id,class(A/B),meaning_contract,excluded,visual_subject,format,transparent_background,aspect_ratio,output_px,prompt_text,prompt_version,ten_gate_qc,placeholder_bbox_in,source_sha`。
PPTX全体の作成指示・タイトル・Takeaway・本文・別スライドのプロンプト、プレビュー画像は**画像生成への入力に混ぜない**。背景は透明を優先するが不自然なら白地も可（仕様に記録）。

## 実行ループ（asset_manifestの全未完了ID）

1. P2の確定プロンプトを読み、完成品宣言（何を描くか）、主体・場面・動作、必要な関係・方向、色・画角、禁止事項、想定挿入枠比を点検。10項目事前検査が欠けるIDは生成不可。
2. そのIDについて独立画像1点を生成し、画像サイズ・RGBA/透過・背景・画角・未指定文字やタイトルの混入を検査。
3. **意味の必須条件（矢印/関係/役割）**と5項目視覚評価（主役・意味・視線誘導・情報量・造形統一）を別々に評価。致命的違反1点でもFAIL。採用しない。
4. 不合格の場合、元指示書の意味契約に戻り原因・新プロンプト版を記録。**初回含め最大3試行**。3回すべて不合格なら`BLOCKED`、勝手に意味を削る・画像を切り抜く・旧資産へ黙って置換しない。
5. PASS画像に `SHA256,filename,width,height,alpha,source,prompt_version,qc,storage_location` を付ける。元の挿入枠と合致しなければその画像はPASSにしない。
6. 既にPASSのIDは原則再生成しない。すべての必須IDがPASSであるか、検証済みの保存先から後続工程で再取得できる場合だけSTEP3全体PASS。
7. 内部生成器の実効プロンプトが観測できなければ**未確認**と正確に記録。ユーザーが承認した仕様が内部へ完全伝達されたと断言しない。

## 返却契約

画像ファイル一式、各画像のQCシート、指示版・試行履歴・SHA256、PPTXの挿入枠IDと対応するmanifestを納品。
画像が1点でも未検証/未保存ならSTEP4へ進まない。実行上限に達しただけなら同じSTEP3に留まり、次の「次」で未完了分から再開。外部Image API課金は別途事前承認が必要。

## 禁止事項

スライド全体画像、複数対象の比較ポスター、疑似日本語、意図しない文字列、指定外のロゴ、誤った矢印、誤りを隠すPPTX上の後付け補修、スライド全体の図形コーディングでA/B画像の代用、無制限な同一画像の試行。
