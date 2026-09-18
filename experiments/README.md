# Experiments A–F

| Series | Directory / runner | Question |
| --- | --- | --- |
| A | [`exp_a/`](exp_a/) + root [`run_experiments.py`](../run_experiments.py) | Apparent correction versus internal revision |
| B | [`exp_b/`](exp_b/) + root [`run_experiments.py`](../run_experiments.py) | Accepted-input coherence versus independent-reference distance |
| C | [`rssi_attractor_escape/`](rssi_attractor_escape/) | External reference injection and attractor escape |
| D | [`rssi_attractor_escape_boundary/`](rssi_attractor_escape_boundary/) | Evidence-strength gate and persistence boundary |
| E | [`rssi_recapture_dynamics/`](rssi_recapture_dynamics/) | Post-injection input order and recapture |
| F | [`rssi_admissible_bridge/`](rssi_admissible_bridge/) | Admissible bridge geometry and minimum recapture path |

The C–F directory names are retained from the frozen implementation because each later runner imports earlier utilities by relative path. A and B share one historical runner and result metadata. This public organization adds navigation only; it does not split or rewrite that runner.

Use [`scripts/reproduce.py`](../scripts/reproduce.py) rather than writing into checked-in result directories.

