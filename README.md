# RSSI Ordered Reachability

**A synthetic study of path-dependent state transitions under bounded local-update rules.**

RSSI originally stood for *Recursive Solipsistic Self-Improvement*. In this repository it is a conceptual project label, not evidence of a deployed recursive self-improving AI. The experiments use a one-dimensional synthetic state, fixed fixtures, and a trusted independent-reference harness. They do not test a frontier LLM, a human subject, or a native HohoEngine learning loop.

[日本語 README](README_JA.md) · [Experiment map](docs/EXPERIMENT_MAP.md) · [A–F synthesis](docs/A_F_SYNTHESIS.md) · [Claim ledger](docs/CLAIM_LEDGER.md) · [Reproduction](docs/REPRODUCIBILITY.md) · [Publication audit](docs/PUBLICATION_AUDIT.md)

## Core rule

For state (b_t), offered input (x_t), and tolerance τ, the ordinary synthetic update is

$$
b_{t+1}=\begin{cases}
x_t,& |x_t-b_t|\le\tau,\\
b_t,& |x_t-b_t|>\tau.
\end{cases}
$$

Within the tested scalar setup, a distant target can remain rejected under direct presentation yet become reachable through a correctly ordered chain of locally admissible intermediate states. The same input multiset—and even the same input token—can be accepted or rejected differently because prior updates place the state in a different location.

The narrow frozen claim is:

> In the tested scalar synthetic setup, a bounded local-update gate permits order-dependent recapture through admissible intermediate transitions; apparent correction and accepted-input coherence do not guarantee agreement with the independent reference.

This is an ordered-reachability result for a synthetic dynamical system. It is not evidence for the Law of Attraction or any supernatural “manifestation” mechanism.

## Representative Exp F counterexample

Starting immediately after revision at state 1, Exp F compared the following precomputed input paths. Each row was reproduced for five fixed seeds; these conditions are deterministic after path construction.

| Condition | Post inputs | Accepted | Initial state | Final state |
| --- | ---: | ---: | ---: | ---: |
| Direct target `0` repeated | 120 | 0 | 1 | 1 |
| Shortest Binary64 admissible bridge | 21 | 21 | 1 | 0 |

Thus, in this implementation,

$$
120\times\text{direct target}\not\Rightarrow\text{state transition},
\qquad
21\text{-step admissible bridge}\Rightarrow 1\rightarrow0.
$$

The number 21 is **not universal**. In exact real arithmetic, when arbitrary intermediate points in the interval are available,

$$
L_{\min}=\left\lceil\frac{d}{\tau}\right\rceil.
$$

For (d=1, \tau=.05), the real minimum is 20. The observed exact-target minimum of 21 is specific to the stored Binary64 representation, subtraction, comparison, and target (b=0). See [Mathematical core](docs/MATHEMATICAL_CORE.md), [bridge summary](experiments/rssi_admissible_bridge/results/bridge_summary.csv), and [float frontier](experiments/rssi_admissible_bridge/results/float_frontier.csv).

## A–F research progression

The arrow below is a progression of research questions, not a causal chain established for real AI:

$$
\text{apparent improvement}
\rightarrow\text{reference divergence}
\rightarrow\text{escape}
\rightarrow\text{recapture}
\rightarrow\text{path dependence}
\rightarrow\text{reachability}.
$$

| Experiment | Question narrowed | Frozen result |
| --- | --- | --- |
| A | Can apparent correction be separated from internal revision? | In a source replay, correct output did not guarantee an internal-state change. |
| B | Does higher accepted-input coherence imply lower independent-reference distance? | No. A fixture increased internal agreement while moving farther from its fixed reference. |
| C | What follows independent external-reference injection? | Persistent escape, relapse, rejection, and external compliance all occurred under predefined arms. |
| D | Do injection strength and frequency determine the final outcome? | Strength gated initial revision, but the post-injection input regime determined persistence versus relapse in the tested grid. |
| E | Can post-injection order and path alter recapture? | Yes. Some identical multisets and equal endpoints produced different outcomes under different orders or paths. |
| F | What makes the old anchor reachable? | Sequentially usable admissible transitions explained the strongest contrasts better than raw exposure count or static connectivity alone. |

Detailed counts, counterexamples, and qualifications are in the [synthesis](docs/A_F_SYNTHESIS.md). Every frozen claim is classified in the [claim ledger](docs/CLAIM_LEDGER.md).

## What is in the repository

```text
rssi-ordered-reachability/
├── README.md / README_JA.md
├── LICENSE / CITATION.cff
├── PROTOCOL_JA.md                 # frozen Exp A/B protocol
├── run_experiments.py             # shared Exp A/B runner
├── docs/                          # public synthesis, claims, math, limits, audit
├── experiments/
│   ├── exp_a/                     # A protocol and navigation
│   ├── exp_b/                     # B protocol and navigation
│   ├── rssi_attractor_escape/     # Exp C
│   ├── rssi_attractor_escape_boundary/ # Exp D
│   ├── rssi_recapture_dynamics/   # Exp E
│   └── rssi_admissible_bridge/    # Exp F
├── results/                       # A/B frozen results and global frozen manifest
├── scripts/                       # portable validation and reproduction
└── sources/hoho/                  # pinned public source excerpts used by Exp A
```

The original C–F directory names are retained because later runners import earlier runners by relative path. Frozen CSVs larger than 1 MB are stored as deterministic `.csv.gz`; their manifest records the SHA-256 of the original uncompressed bytes.

## Verify the published snapshot

Python 3.10+ and the standard library are sufficient for data generation and validation. The frozen run used Python 3.12.14.

```bash
python scripts/validate_snapshot.py
```

This command verifies compressed and uncompressed artifact hashes, row counts, representative A–F claims, internal links, citation/license files, and the absence of obvious secrets or local absolute paths. It does not run a new experiment.

To rerun the existing deterministic A–F generators in temporary directories and compare their CSV bytes with the frozen snapshot:

```bash
python scripts/reproduce.py --series all
```

Individual series are supported, for example `--series a,b,c` or `--series f`. No network access, API key, or LLM call is used. Exact commands, seeds, expected runtime behavior, and decompression examples are in [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md).

## Evidence discipline

The claim ledger distinguishes:

- **Analytically supported**
- **Supported by synthetic experiment**
- **Supported by finite fixtures only**
- **Implementation-dependent**
- **Suggestive only**
- **Not supported**
- **Falsified / rejected hypothesis**

The following are not promoted to supported claims: transfer to real LLMs or human belief dynamics; native HohoEngine RSSI recursion; recursive self-improvement; an AI-alignment solution; arbitrary high-dimensional generalization; universal phase transitions or hysteresis; adversarial self-rewriting resistance.

## Synthetic / HohoEngine / real-AI boundary

Exp A is a manual Python replay of bounded pathways from pinned, publicly licensed HohoEngine source excerpts. Exp B declares the minimal scalar gate. Exp C integrates the replay and scalar rule with an independent-reference harness. Exp D–F reuse that Python harness. The inspected HohoEngine does not supply the B–F ordinary RSSI recursion, and native Julia cross-checking did not complete successfully. The separate Ideal E1–E8 implementation is not included in this public repository and is not required to reproduce A–F.

See [Boundary and provenance](docs/BOUNDARY_AND_PROVENANCE.md) and [Limitations](docs/LIMITATIONS.md).

## Citation and license

Citation metadata is provided in [CITATION.cff](CITATION.cff). Code and documentation in this snapshot are released under the [MIT License](LICENSE). The pinned Hoho source excerpts retain their original MIT license in [sources/hoho/LICENSE](sources/hoho/LICENSE).
