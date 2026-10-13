# S17_SKELETON — スライド17のPPTX骨組み先行実験

- outcome: **PASS（PPTX骨組みと実レンダリングのみ）**
- スライド17 MLOps の編集可能なPPTX骨組みを新規制作。ユーザーの明示した「PPTX → 図生成 → 差し込み」に従う。
- PPTX: `slide17_MLOps_PPTX_first_skeleton.pptx`（ChatGPT内のパス `/mnt/data/lecture03_step_run/slide17_pptx_first/`）
- PNGプレビュー: `slide17_MLOps_PPTX_first_skeleton_preview.png`（実PPTXをLibreOfficeでPDFへ変換後、1600×1200でPNG化）
- 画像配置枠: x=3.75 in, y=2.44 in, width=5.86 in, height=3.18 in, ratio=1.84277; 枠はPPTXの点線プレースホルダーで、**AI主図はまだ生成・配置していない**。
- editable text shapes: 20。PPTXの画像オブジェクト: 0。
- 固定の原稿：タイトル、Intro2行、Takeaway2行、主な活動の流れを照合。MLOps本文は表示用の箇条書きへ短文化。講義元原稿は変更なし。
- 本PPTX SHA256: `2ec2e73535ec5551ba19129ed56e0fb98ce8fc91008356e1760875e9b6ef9667`。
- PowerPoint指定フォント源真ゴシックPは環境にないため、実レンダリングでは代替書体が使用されている。実フォントでの確認は未実施。
- 画像未生成なのでMLOps循環の工程順序とフィードバック経路の視覚的正確性は**未評価**。PPTX全体はまだ未完成。
- PPTXとPNGの**GitHubへのバイナリアップロードは未実施**。当チャットに納品し、GitHubにはこのテキストログと手順・STATEを保存する。
- 旧A/B/C比較のE03は**保留**し、記録を改変しない。新たな active workflow はS17_IMG。
- 次の「次」で行うこと：図を独立画像1点で生成し、その画像を単体評価する（S17_IMG）。同じ応答で組込み工程まで飛ばさない。
