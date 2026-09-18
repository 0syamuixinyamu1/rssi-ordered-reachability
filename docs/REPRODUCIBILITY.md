# Reproducibility

## Requirements

- Python 3.10 or later; the frozen execution used Python 3.12.14.
- Standard library only for runners, snapshot validation, and CSV reproduction.
- Optional `matplotlib` for figure regeneration; figures do not determine classifications.
- No network, API key, LLM account, Julia runtime, or private Ideal repository is required.

The scalar arithmetic relies on ordinary Python `float` behavior. Exact Binary64 result reproduction should use a conventional IEEE-754 CPython build. Platform/Python differences must be reported rather than hidden by changing tolerances or expected values.

## Frozen data layout

Files at or below 1 MB remain uncompressed. Larger raw CSVs are stored as deterministic gzip files with suffix `.csv.gz`. The public manifest records:

- source-series label;
- original artifact path;
- publication path;
- whether gzip was used;
- SHA-256 and byte size of uncompressed content;
- SHA-256 and byte size of the stored file;
- CSV row count.

Inspect or extract a compressed file with:

```bash
gzip -dc experiments/rssi_admissible_bridge/results/events.csv.gz | head
gzip -dc results/a_trials.csv.gz > /tmp/a_trials.csv
```

## Level 1 — publication integrity, no experiment run

```bash
python scripts/validate_snapshot.py
```

This streams through frozen artifacts, verifies the manifest and row counts, independently checks the representative A–F values used in the README, resolves local Markdown links, checks required claim categories and scope warnings, parses `CITATION.cff` conservatively, and scans tracked publication files for obvious secrets and local absolute paths.

Expected result:

```text
PUBLIC SNAPSHOT VALID: all checks passed
```

The detailed machine-readable result is written only when `--report PATH` is supplied, avoiding an unrequested change to the checkout.

## Level 2 — regenerate existing A–F CSVs

Run every frozen generator in temporary directories and compare output bytes with the public frozen artifacts:

```bash
python scripts/reproduce.py --series all
```

Or select a comma-separated subset:

```bash
python scripts/reproduce.py --series a,b,c
python scripts/reproduce.py --series d
python scripts/reproduce.py --series e,f
```

The wrapper does not change tracked results. A/B are run together in an isolated copy because they share one historical runner. C–F accept temporary output directories. F additionally runs its existing graph-analysis command. Only existing A–F computations are rerun; no parameter, metric, classification, or experiment is added.

Use `--output-dir reproduction-output` to retain regenerated files. The default deletes temporary output after comparison.

## Underlying commands

From the repository root, the existing commands are:

```bash
python run_experiments.py
python experiments/rssi_attractor_escape/run_experiment.py --output-dir <dir>
python experiments/rssi_attractor_escape_boundary/run_experiment.py --output-dir <dir>
python experiments/rssi_recapture_dynamics/run_experiment.py --output-dir <dir>
python experiments/rssi_admissible_bridge/run_experiment.py --output-dir <dir>
python experiments/rssi_admissible_bridge/analyze_reachability.py --output-dir <same-dir>
```

Running the first command directly writes uncompressed A/B CSVs to `results/`; the portable wrapper avoids that working-tree change.

## Fixed seeds and sizes

| Series | Seeds / deterministic basis | Expected run scale |
| --- | --- | --- |
| A | exhaustive deterministic Cartesian product | 27,104 trials + 625 pressure rows |
| B | fixed fixtures; sensitivity seeds 0–29 | 120 trajectories + 720 sensitivity runs |
| C | 7, 17, 29 | 54 runs |
| D | 7, 17, 29, 41, 53 | 900 primary + 20 control runs |
| E | 7, 17, 29, 41, 53 | 330 runs |
| F | 7, 17, 29, 41, 53 | 170 runs; all paths stored before replay |

D/E/F full parameter values are in their checked-in `config.json`; C arms and schedules are in its frozen `PROTOCOL.md` and runner. F’s exact input arrays and optional tokens are in [`path_manifest.json`](../experiments/rssi_admissible_bridge/results/path_manifest.json).

## Reproduction interpretation

A byte match shows that the checked-in deterministic implementation regenerated the frozen CSV under the current runtime. It does not add evidence beyond A–F, establish external validity, or convert an implementation-dependent value into an analytic theorem.

A mismatch must be reported with the affected file, runtime, and first differing hash. Do not “fix” it by changing tol, gate, reference, classification, input order, or expected results.

## Native Julia status

[`native_crosscheck.jl`](../native_crosscheck.jl) is retained as a historical comparison artifact. Native execution did not complete successfully in the original work and is not part of the public reproduction requirement. Do not call Python synthetic recurrence “native validation.”

