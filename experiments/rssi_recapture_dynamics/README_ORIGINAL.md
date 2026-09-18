# Exp E: Post-Injection Input Dynamics / Recapture Mechanism

2026-09-17。Exp C/Dの更新・attractor・分類コードをそのままimportして使うPython synthetic experimentです。注入は `S=1, F=1` に固定し、その後の入力値・曝露割合・順序を比較しました。HohoEngine、Ideal E1–E8、CoreCommitment、Exp A/B/C/Dの既存ファイルは変更していません。

66条件×5seed、330 trajectoryを各120 post-step追跡しました。Persistent Escape 300件、Relapse 30件。急激な旧値0の提示は拒絶され、小さい受理可能な変化が連続する系列で再捕獲が起きました。同一入力集合でも下降順と上昇・シャッフル順で分類が変わります。これはこの固定したsynthetic ruleでの結果であり、LLMやRSI一般についての主張ではありません。

詳細と制限は [EXPERIMENT_REPORT.md](EXPERIMENT_REPORT.md)、事前固定した設計は [PROTOCOL.md](PROTOCOL.md) に記録しています。

## ファイル

| ファイル | 内容 |
|---|---|
| `config.json`, `PROTOCOL.md` | 実行前に固定したseed・grid・定義 |
| `run_experiment.py` | C/Dを再利用する入力系列生成・実行・集計 |
| `validate_results.py` | 独立した入力/状態監査、C/D/RSSI回帰、全CSV再現性確認 |
| `make_figures.py` | 保存結果から7図を生成 |
| `protected_existing_files.json` | 開始時のA/B/C/D 78ファイルのSHA-256 |
| `results/baseline_reproduction.json` | 主実行前のD代表15条件の一致 |
| `results/condition_manifest.json` | 66条件の実際の設定 |
| `results/trajectories.csv` | 330試行、44,435状態行。belief・C・D・受理/拒絶数 |
| `results/events.csv` | 48,880入力行。値・更新前後belief・gate・受理/拒絶・方向 |
| `results/summary.csv` | 試行別のC分類とE recapture指標 |
| `results/sequence_summary.csv` | 条件別、各5seedの観測割合 |
| `results/recapture_thresholds.csv` | q/vの隣接観測境界。逆方向の変化・未観測も保持 |
| `results/order_effects.csv` | 同一multisetの30組比較 |
| `results/path_dependence.csv` | 最終入力が同じfast/slowの5組比較 |
| `results/relapse_times.csv` | latency・slope・再発前のR/O曝露数 |
| `results/coherence_diagnostic.csv` | 事前固定した早期C警報のTP/FP/FN/TNと欠測 |
| `results/attractor_checks.csv` | 既存C/D controlの局所摂動チェック |
| `results/execution.json`, `results/validation.json` | 実コマンド、件数、hash、検証・回帰ログ |
| repository rootの `results/frozen/PUBLICATION_BOUNDARY.json` | 公開snapshotの境界と除外記録 |
| `figures/` | 系列別outcome、q率、vと再発時間、D軌跡、順序、C/D、q×v |
| `MANIFEST_SHA256.json` | E成果物のhash。親/C/Dのmanifestは既存範囲を対象とする |

`run_id`で試行を、`trajectory_id`で状態行とevent行を結びます。CSVの入力順序を保持してください。通常入力の受理/拒絶と外部注入の受理/拒絶は別です。

`D_post`はCと同じ最終20通常step平均です。直後のDは `D_immediate_first`、最終値は `D_final`。`D_min`は注入直後も含みます。`C_internal`の空欄は受理入力なしであり、1ではありません。再発時刻の空欄も0ではありません。

qは「値が1より小さい、旧attractor方向の入力」の**提示数**割合です。中間値も含み、受理割合や値0の割合ではありません。`q_old_halfspace` と `exact_old_count` も記録しています。入力なしのq・受理率・拒絶率はNAです。

## 再現

展開した `hoho-evaluation-experiments` ディレクトリから実行します。数値実行・検証はPython 3.12の標準ライブラリのみ。図生成にはnumpy/matplotlibを使います。

```sh
python experiments/rssi_recapture_dynamics/run_experiment.py --output-dir /tmp/exp-e-reproduction
python experiments/rssi_recapture_dynamics/validate_results.py
python experiments/rssi_recapture_dynamics/make_figures.py
```

検証は保存結果を監査し、別の一時出力先でEを実行して10 CSVをバイト一致で比較します。続いて隔離コピーで既存D→C→RSSI検証を実行し、原本の既存成果物には書き込みません。原本Ideal checkoutのない別端末では原本170ファイル比較は実行できませんが、同梱A/B/C/Dの保全と数値再現性は検証できます。

no-input controlだけは既存Cの入力数0によるゼロ除算を避けるharness adapterを使います。状態基準は同じで、ダミー入力は追加しません。全非空系列は `C.summarize` をそのまま使います。

Juliaは本実験の実行条件ではありません。以前のnative cross-checkのruntime障害は未解決であり、本成果をnative validationとは呼びません。
