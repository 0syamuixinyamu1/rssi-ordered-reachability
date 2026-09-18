# Integrated claim ledger

Frozen on 2026-09-18. Status applies to the exact statement in each row. A finite counterexample can reject a universal claim, but it does not establish the universal opposite.

## Evidence categories

| Status | Meaning in this repository |
| --- | --- |
| **Analytically supported** | Derived under explicit assumptions from the specified update rule |
| **Supported by synthetic experiment** | Directly supported by stored synthetic comparisons; scope remains the tested model |
| **Supported by finite fixtures only** | Descriptive result for specified fixtures/seeds, not a probability law or universal boundary |
| **Implementation-dependent** | Depends materially on current arithmetic, code, comparison, or endpoint representation |
| **Suggestive only** | Motivates a future question but supplies no evidence in the proposed target domain |
| **Not supported** | No corresponding measurement or proof; distinct from falsification |
| **Falsified / rejected hypothesis** | A universal or sufficient-condition formulation has a counterexample in the tested scope |

## Frozen claims

| ID | Claim | Status | Supporting evidence / counterexample | Scope and limitation |
| ---: | --- | --- | --- | --- |
| 1 | Improved internal coherence does not guarantee agreement with an independent reference. | **Supported by synthetic experiment** | B `drift_away`: C=.9619349672→.9999858876 while D=.6380650328→.9998658149. [`b_trajectories.csv`](../results/b_trajectories.csv) | C is accepted-input agreement in this synthetic model, not a native or universal coherence measure. Some early-C patterns had limited fixture-specific information. |
| 2 | Apparent correction does not guarantee internal revision. | **Supported by synthetic experiment** | A `external_only`: 726/726 output-correct and 0/726 internally correct in the predefined subset. [`a_summary.csv`](../results/a_summary.csv) | The harness supplies the candidate response. No autonomous deception or intent is established. |
| 3 | Strong external evidence always revises belief. | **Falsified / rejected hypothesis** | C stored an (S=1) injection at b=.775 with support=.69, rejected without state change. [`event_log.csv.gz`](../experiments/rssi_attractor_escape/results/event_log.csv.gz) | Rejects “always” over the current evidence handler. Initial (D=1, S=1) still revises. |
| 4 | Repeating external evidence guarantees persistent escape. | **Falsified / rejected hypothesis** | D descending bridge relapsed at (S=1, F=16); repetition delayed but did not prevent relapse. [`summary.csv`](../experiments/rssi_attractor_escape_boundary/results/summary.csv) | Tested finite injection window and frequencies only; no claim about permanent intervention. |
| 5 | Post-injection input distribution alone explains recapture. | **Falsified / rejected hypothesis** | E/F identical bridge multisets produced relapse or persistence under different orders. [`order_effects.csv`](../experiments/rssi_recapture_dynamics/results/order_effects.csv) | “Distribution” means an order-free empirical multiset/ratio. A full temporal process would be a different claim. |
| 6 | The same multiset can yield different outcomes under different orders. | **Supported by synthetic experiment** | E/F bridge multiset; descending relapsed, ascending/shuffled remained persistent. [`order_divergence.csv`](../experiments/rssi_admissible_bridge/results/order_divergence.csv) | Existential, not universal. E’s endpoint multiset produced no classification change across its tested orders. |
| 7 | Equal final offered input implies equal final belief. | **Falsified / rejected hypothesis** | E fast (v=1) and slow (v=.025) paths both ended with offered input 0 but had D_final 0 and 1. [`path_dependence.csv`](../experiments/rssi_recapture_dynamics/results/path_dependence.csv) | Path dependence occurs through the evolving current state; no hidden memory variable is required. |
| 8 | The amount of old-anchor exposure determines recapture. | **Falsified / rejected hypothesis** | F: 120 direct zeros caused no movement, while a 21-input bridge reached zero. [`bridge_summary.csv`](../experiments/rssi_admissible_bridge/results/bridge_summary.csv) | Rejects exposure count as a sufficient/monotone determinant; does not prove quantity is irrelevant under every controlled path. |
| 9 | A sequentially usable admissible path is important for recapture. | **Supported by synthetic experiment** | Complete/broken bridges, order comparisons, and same-token acceptance witnesses. [`bridge_summary.csv`](../experiments/rssi_admissible_bridge/results/bridge_summary.csv) | “Path” means the state transitions actually usable in offered order, not static connectivity alone. |
| 10 | For the exact-real scalar gate, (L\ge\lceil|b_0-b^*|/\tau\rceil). | **Analytically supported** | Triangle inequality and per-step bound; equal subdivision attains it with free intermediate points. [Mathematical core](MATHEMATICAL_CORE.md) | Requires explicit real-scalar assumptions; fixed alphabets/orders can prevent attainability. |
| 11 | In the current Binary64 implementation, exact 1→0 target arrival requires at least 21 updates and is attained in 21. | **Implementation-dependent** | Frontier step 20 remains (7.320533068622126e-16>0); step 21 is 0. [`float_frontier.csv`](../experiments/rssi_admissible_bridge/results/float_frontier.csv) | Exact current representation, tol, interval, arithmetic, and target only. The real minimum is 20. |
| 12 | Static graph connectivity guarantees recapture for every input order. | **Falsified / rejected hypothesis** | The same connected multiset had a target-reaching descending order and non-reaching ascending/shuffled orders. [`order_divergence.csv`](../experiments/rssi_admissible_bridge/results/order_divergence.csv) | Connectivity still means a suitable selectable path exists; it is not a schedule guarantee. |
| 13 | For F’s fixed noisy bridges, η=.006 reached target in 2/5 seeds and η=.012 in 0/5. | **Supported by finite fixtures only** | [`bridge_summary.csv`](../experiments/rssi_admissible_bridge/results/bridge_summary.csv) | Fixed 25-input monotone path, five seeds, no repair/resampling; not a precise threshold or probability estimate. |
| 14 | Real LLM sequence sensitivity may be worth auditing separately. | **Suggestive only** | E/F provide design motivation only. | No LLM evidence in this repository; output order effects would not directly reveal latent belief. |
| 15 | A–F demonstrate the same mechanism in real LLMs, humans, generic RSI, or native Hoho recursion. | **Not supported** | No such system or subject was tested. [Boundary](BOUNDARY_AND_PROVENANCE.md) | RSSI is a project label, not a transfer result. |
| 16 | For known accepted inputs, defined C is at least (1-\tau) in exact real arithmetic. | **Analytically supported** | Directly from acceptance and C=`mean(1-abs(x-b_before))`. [`run_experiments.py`](../run_experiments.py) | C is undefined with zero accepted inputs; Binary64 rounding applies; this is not truth accuracy. |
| 17 | Reference integrity is guaranteed against adversarial code rewriting. | **Not supported** | The trusted policy API lacks reference-rewrite operations; no adversarial rewriting experiment was run. | Integrity is restricted to the fixed harness and domain. |
| 18 | The D grid bracket .58/.59 is a universal RSSI critical constant. | **Not supported** | It follows from the current initial-state support handler; later (S=1) injections can still be rejected. [`boundary_estimates.csv`](../experiments/rssi_attractor_escape_boundary/results/boundary_estimates.csv) | Implementation-specific finite grid; not a universal phase transition. |

## Independently frozen rejected hypotheses

The following shorthand formulations are explicitly rejected or weakened:

1. Strong and repeated reference injection guarantees persistent escape.
2. Strength and frequency alone explain rejection, relapse, and persistence.
3. Old-directed ratio (q) alone explains recapture.
4. Equal final input implies equal final state.
5. More direct old-anchor exposure necessarily causes more recapture.
6. Static reachability guarantees arrival under any presentation order.

The machine-readable original claim freeze, including artifact SHA-256 values and selectors, is retained at [`docs/freeze/claim_evidence.json`](freeze/claim_evidence.json). Its paths refer to the uncompressed original package; the public [`results/frozen/MANIFEST.json`](../results/frozen/MANIFEST.json) maps those source artifacts to compressed or uncompressed publication files.

