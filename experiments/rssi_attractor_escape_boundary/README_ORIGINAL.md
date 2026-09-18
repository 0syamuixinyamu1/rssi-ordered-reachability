# Exp D: Attractor Escape Boundary / Critical Transition

2026-09-17。Exp Cの既存runnerをimportし、強度Sと注入回数Fだけを変更するPython synthetic実験です。
HohoEngine/Ideal/Exp A/B/Cは無変更。新しい学習・自己書き換えエンジンではありません。

## 結論

各通常入力列内では3相の連続遷移は現れませんでした。
stationaryはRejection→Persistent Escape、descending_bridgeはRejection→Relapse。
両方の初回改訂境界は全Fで S∈(0.58,0.59] に挟まれ、Fを増やしても分類は変わりませんでした。
強い反復注入は一部で再発を39→79stepへ遅らせましたが、持続脱出には至りません。
詳細・制限は [EXPERIMENT_REPORT.md](EXPERIMENT_REPORT.md)。

## ファイル

- `PROTOCOL.md` / `config.json`: 主実行前に固定した条件・評価方法。
- `run_experiment.py`: Exp CのReference/Recorder/attractor/summarizeを再利用するorchestration。
- `validate_results.py`: 独立ログ監査、境界のnegative fixtures、C回帰、再現性検証。
- `make_figures.py`: 保存CSVから7図を生成。
- `results/trajectories.csv`: 920 trajectoryの176,710状態行。C_t/D_tを含む。
- `results/events.csv`: 346,450入力行。通常入力・外部配送、受理・拒絶、実belief変化。
- `results/summary.csv`: 920試行のExp C定義のsummary。
- `results/phase_grid.csv`: 主grid180cell、各5seedの観測割合。
- `results/boundary_estimates.csv`: Sc/Fcの観測最小値と直前grid値、未観測・既に最小値で存在する場合の区別。
- `results/adjacent_transitions.csv`: 隣接grid点の分布変化を全て記録。単調性を仮定しない。
- `results/relapse_times.csv`: 試行別の再発・確認時刻、最後の予定注入からの時間。
- `results/coherence_features.csv` / `coherence_diagnostic.csv`: Cによる記述的識別の補助分析。
- `results/attractor_checks.csv`: 各regime/seedの局所摂動確認。
- `results/execution.json`, `validation.json`, `exp_c_regression.json`: 実コマンド・hash・検証記録。
- `protected_existing_files.json`: 作業開始時の既存A/B/C全ファイルhash。
- `figures/`: outcome、持続率、再発率、再発時間、境界trajectory、coherence。

`run_id`で試行を、`trajectory_id`で状態行と入力行を対応付けます。`group=primary/control`を分けて集計してください。
同じstepに注入がある場合、通常更新の後に注入。CSVの順序を保持してください。
`D_post`はExp Cと同じ最終20通常step平均で、注入直後ではありません。直後は`D_immediate_first`。
`C_internal`の空欄は観測なしであり1ではありません。T_relapseの空欄も0ではありません。

## 再現コマンド

展開した `hoho-evaluation-experiments` で実行してください。Python 3.12、数値実行と検証は標準ライブラリのみ。

```sh
python experiments/rssi_attractor_escape_boundary/run_experiment.py --output-dir /tmp/exp-d-reproduction
python experiments/rssi_attractor_escape_boundary/validate_results.py
```

検証は保存結果を監査し、別の一時出力先でDを再実行して10 CSVのhashを比較します。
その後、A/B/Cだけの一時コピーで既存C検証を実行します。元のC成果物には書き込みません。
原本Ideal checkoutがない端末ではその原本比較は未実施になりますが、同梱A/B/Cの不変と数値照合は実行できます。

図のみ再生成（numpy, matplotlibが必要）:

```sh
python experiments/rssi_attractor_escape_boundary/make_figures.py
```

本実験にJuliaは不要です。前回native cross-checkのruntime障害は解消していません。
`MANIFEST_SHA256.json`はこのDフォルダ用、親とCのmanifestはそれぞれの既存成果物用です。
