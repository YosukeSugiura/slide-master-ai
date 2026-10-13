# S17_INSERT — MLOps画像のPPTX組込み・実レンダリング

- step_id: S17_INSERT
- attempt: 1
- outcome: **PASS（PPTX先行方式の試作1枚）**
- 利用PPTX骨組み: slide17_MLOps_PPTX_first_skeleton.pptx
- 採用素材: S17_A_MLOPS_LIFECYCLE_v1.png（S17_IMGの独立評価PASS）
- 完成PPTX: slide17_MLOps_PPTX_first_integrated_v1.pptx
- 実プレビュー: slide17_MLOps_PPTX_first_integrated_v1_preview.png（LibreOfficeで実際のPPTXから生成、1600×1200）。
- 画像挿入位置: x3.75, y2.44, 幅5.86, 高さ3.18 in、画角保持。プレースホルダーの文字・枠は削除。
- 独立画像オブジェクト: 1、編集可能な文字オブジェクト: 25。データ収集、前処理、学習、評価、配備、監視、再学習・更新の工程ラベルは編集可能なPPTXテキストとして追加。
- 固定原文のタイトル・Intro2文・Takeaway2文、主な活動の流れを抽出して照合済み。編集可能な左の説明文も維持。
- 図の意味：監視から再学習・更新へ、さらに学習／配備へ戻る経路が視認できる。誤った矢印のPPTX後付け修復なし。
- PPTX内フォント名は源真ゴシックP。現在のLibreOfficeプレビューは代替フォントであり、源真ゴシックP実描画は未検証。
- 軽微な残課題：生成図のアイコン面の陰影、画風の完全なフラット性。教育効果は未実測。
- PPTX SHA256: 73044bf9e6ac6b445591780fa9f2a4fde4a046225258b822964c1b9f7e3e1daf
- preview SHA256: 5920d64d435b77884961bebe6732c0471561f599b25b3d33841b71b385a13a4f
- PNG/PPTX本体はChatGPT内の /mnt/data/lecture03_step_run/slide17_pptx_first/ に実在。**GitHubへバイナリは未アップロード**。GitHub上はこの監査ログのみ。
- 次の工程: S35_BUILD（スライド35の編集可能な入力チェック表をPPTXとして制作し実レンダリング）。旧A/B/C実験E03は保留状態のまま。
