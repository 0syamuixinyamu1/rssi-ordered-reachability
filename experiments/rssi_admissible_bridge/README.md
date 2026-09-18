# Experiment F — Admissible bridge geometry

Exp F treats the unchanged ordinary scalar gate as a state-transition rule. It compares exact-real and Binary64 minima, step sizes, broken bridges, detours, ordering, exposure, noise, and finite graph discretizations.

- [`PROTOCOL.md`](PROTOCOL.md)
- [`config.json`](config.json)
- [`EXPERIMENT_REPORT.md`](EXPERIMENT_REPORT.md)
- [`run_experiment.py`](run_experiment.py)
- [`analyze_reachability.py`](analyze_reachability.py)
- [`results/bridge_summary.csv`](results/bridge_summary.csv)
- [`results/float_frontier.csv`](results/float_frontier.csv)
- [`results/order_divergence.csv`](results/order_divergence.csv)
- [`results/reachability_graph.csv`](results/reachability_graph.csv)
- [`figures/exposure_vs_bridge.png`](figures/exposure_vs_bridge.png)

Exact target `b==0`, bridge completion, relapse classification, and static graph connectivity are kept separate. The Binary64 minimum 21 is implementation-dependent; the exact-real result under free intermediate points is 20 for distance 1 and τ=.05.

[`README_ORIGINAL.md`](README_ORIGINAL.md) preserves the original experiment-facing README, with publication path sanitization only.

