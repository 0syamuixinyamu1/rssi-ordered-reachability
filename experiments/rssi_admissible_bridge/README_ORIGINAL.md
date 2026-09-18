# Exp F: Admissible Bridge Geometry / Minimum Recapture Path

2026-09-17。既存C/D/Eをimportして実行したscalar Python synthetic experimentです。HohoEngine本体、Ideal E1–E8、CoreCommitment、Exp A–Eは変更していません。

**厳密なb=0への最短経路は、実数のtol=1/20では20step、既存binary64 gateでは21stepでした。** 同じ入力集合の接続性だけでは、与えられた順序での到達を保証できません。逐次受理された入力による経路を区別して記録しています。

- [EXPERIMENT_REPORT.md](EXPERIMENT_REPORT.md)：結果、証明と実装の区別、制限、Supported / Unsupported Claims。
- [PROTOCOL.md](PROTOCOL.md)：Exp F trajectory実行前に固定した条件と評価。
- `config.json`：5seed、34条件、120 post-step、primary tol=.05。
- `run_experiment.py`：全入力経路の事前生成、Cの既存Recorder/update/classifierによる実行。
- `analyze_reachability.py`：全binary64状態の最小到達frontierと離散graphの解析。engine機構ではありません。
- `validate_results.py`：独立raw replay、Fractionによる丸め境界確認、graph・順序照合、E/D/C/RSSI回帰、CSV再現性。
- `make_figures.py`：保存CSVから8図を生成。

## 再現コマンド

展開した `hoho-evaluation-experiments` から実行してください。数値計算・検証はPython 3.12標準ライブラリのみ。図にはnumpy/matplotlibを使います。

```sh
python experiments/rssi_admissible_bridge/run_experiment.py --output-dir /tmp/exp-f-reproduction
python experiments/rssi_admissible_bridge/analyze_reachability.py --output-dir /tmp/exp-f-reproduction
python experiments/rssi_admissible_bridge/validate_results.py
python experiments/rssi_admissible_bridge/make_figures.py
```

validatorは保存結果を監査し、別の一時出力先にFを再実行して全11 CSVを比較します。その後、隔離したA–Eコピーで既存E validatorを実行し、そこからD/C/RSSIの回帰が呼び出されます。A–E原本の結果を上書きしません。原本Ideal checkoutのない別端末ではその170ファイル比較だけは実行できません。

## 保存結果

| ファイル | 内容 |
|---|---|
| `results/path_manifest.json` | シミュレーション開始前に生成した170本の全入力値、token、パラメータ |
| `results/trajectories.csv` | 22,610状態行。belief、C、D、受理/拒絶数 |
| `results/events.csv` | 11,940入力行。更新前後belief、gate、受理/拒絶、入力token |
| `results/bridge_summary.csv` | 170試行の分類、長さ、TV、gap、厳密target到達、接続性 |
| `results/minimum_paths.csv` | 実数下限・binary64最短値・候補経路の実行結果 |
| `results/float_frontier.csv` | 各stepの最小到達状態、その直下のfloat、hexと厳密な有理数gap |
| `results/order_divergence.csv` | 30組の最初の状態/受理フラグ分岐、同一tokenの最初の証拠 |
| `results/order_acceptability.csv` | 同一入力tokenが異なる先行beliefで異なる受理結果になる全証拠 |
| `results/reachability_graph.csv` | 10graphの接続成分、最短長、最短経路数、witness |
| `results/graph_nodes.csv`, `graph_edges.csv` | 実際の頂点・辺。self-loopなし、無向辺を1回保存 |
| `results/graph_witness_events.csv` | graph witnessを既存offerで逐次実行した結果 |
| `results/execution.json`, `analysis.json` | 実コマンド、設定、件数、hash、最短値 |
| `results/validation.json` | F独立検証・全CSV再現性・E/D/C/RSSI回帰ログ |
| `results/baseline_reproduction.json` | F着手前の全E再現と指定baseline25件 |
| `results/initial_workspace.json`, `final_workspace.json` | git状態、原本保全の照合 |
| `protected_existing_files.json` | A–Eの既存109ファイルのhash |
| `MANIFEST_SHA256.json` | F成果物のhash |
| `figures/` | 必須7図とgeometry/noise補助図 |

`run_id`で試行を、`trajectory_id`で状態とeventを対応付けます。順序を保持してください。`input_token`はorder条件だけで元のmultiset要素を識別します。

`L_actual`は提示入力数で、初期状態と入力なしholdを含みません。`TV`は初期1→最初の入力を含み、`TV_input_only`は入力列内部だけです。`first_target_step`は厳密なb==0への初回到達。Relapseは既存の.05近傍・5step基準であり、同義ではありません。`bridge_completion`は全入力が受理され、末尾0・最終belief0となる場合です。拒絶後に回復してtargetへ到達した経路は、target=trueでもcompletion=falseになり得ます。

有限経路終了後は120stepまで空batchで状態を観測します。0入力でpaddingしていません。Cの空欄は受理観測なし、T_relapseの空欄は未観測です。

graphのtol=.049/.051は分析上の対照だけです。主実験のgateは全170試行でtol=.05のままです。Juliaは実行条件に含めず、本成果をnative validationとは呼びません。
