# Exp C: External Reference Injection / Attractor Escape

既存RSSI Python harnessを最小拡張した、独立反証後の有限期間の脱出・再発実験です。
HohoEngine本体の学習ループや自己書き換えを実行するものではありません。

- 結果と主張の範囲: [EXPERIMENT_REPORT.md](EXPERIMENT_REPORT.md)
- 再開時点の25項目は元bundleに保存されていました。公開snapshotでは[publication boundary](../../results/frozen/PUBLICATION_BOUNDARY.json)を参照してください。
- 結果を見る前に固定した条件: [PROTOCOL.md](PROTOCOL.md)
- 元の生成結果: `results/trajectories.csv`, `event_log.csv`, `summary.csv`
- 集計・摂動確認: `aggregate_summary.csv`, `attractor_checks.csv`
- 実行・検証記録: `execution.json`, `validation.json`, `native_status.json`

## 再現方法

ZIP展開後の `hoho-evaluation-experiments` を作業ディレクトリにしてください。Python 3.12、標準ライブラリで本体と検証を実行できます。

```sh
python experiments/rssi_attractor_escape/validate_results.py
python experiments/rssi_attractor_escape/run_experiment.py --output-dir /tmp/exp-c-reproduction
```

検証コマンドは保存済みCSVを照合し、Exp A/Bの既存12チェックを再実行した後、別の一時ディレクトリでExp Cを再実行して5 CSVのSHA256を比較します。
原本Ideal checkoutがない端末では原本170ファイルの比較のみ省略し、その旨を記録します。その他の数値検証と同梱ソース検証は実行します。

図のみ再生成する場合（matplotlib必要）:

```sh
python experiments/rssi_attractor_escape/make_figure.py
```

native Juliaが利用可能な別環境では、既存Exp A用の関数照合を以下で実行できます。

```sh
julia --startup-file=no native_crosscheck.jl
```

これはRSSI recurrenceのnative実装を検証するものではありません。本環境では起動時SIGBUSで未完了です。
原本Hoho/Ideal repositoryへの変更・pushは行っていません。

## CSVの読み方

`summary.csv` の1行が1試行。`trajectories.csv` の1行は状態観測点で、54本のtrajectoryを含みます。
`run_id` と `trajectory_id` で `event_log.csv` の各入力を対応付けられます。
`baseline` → `pre_injection` → `injection` / `normal` の順序をファイル順で読んでください。
同じstepに通常更新と注入がある場合、通常更新の後に注入されます。
`C_internal`は通常入力の受理分のみ。注入行・観測なしは空欄であり1ではありません。
`D_post`は最終20通常stepの平均、`D_final`は最終点、`delta_D=D_post-D_pre`。
`rejection_rate`は通常入力の拒絶率。外部反証の拒絶率や試行全体の分類率とは異なります。
`accepted`は証拠経路ではcollapse成功フラグ。既に正解で動かない`already_correct`は拒絶に数えません。
`internal_revision`は実belief変化、`compliance_internal_revision`は既存complianceのフラグです。

同梱のinspection資料は出所確認用です。Ideal E5/E6/E8をExp Cの数値計算に接続していません。
親ディレクトリの旧MANIFEST_SHA256.jsonはExp A/Bの旧成果物だけを対象とします。
