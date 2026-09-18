# Frozen results index

The A–F raw results remain at the paths used by their experiment reports:

- A/B: `results/`
- C: `experiments/rssi_attractor_escape/results/`
- D: `experiments/rssi_attractor_escape_boundary/results/`
- E: `experiments/rssi_recapture_dynamics/results/`
- F: `experiments/rssi_admissible_bridge/results/`

Files larger than 1 MB are stored as deterministic gzip. `MANIFEST.json` maps every published result artifact to its original uncompressed SHA-256, byte count, and CSV row count. It also marks files compared by `scripts/reproduce.py`.

`VALIDATION_HISTORY.json` is a portable summary of completed pre-publication validation. Machine-specific commands, absolute workspace paths, private checkout locations, and the separate Ideal implementation are intentionally omitted.

`SNAPSHOT_SHA256.json` covers every public repository file other than itself. It is regenerated only when assembling a new public snapshot; ordinary validation must not rewrite it.

