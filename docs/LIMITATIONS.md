# Limitations and non-claims

## Model scope

| Limitation | Actual scope | Unsupported extension |
| --- | --- | --- |
| Scalar 1D state | B–F use a known one-dimensional state | Arbitrary 2D or high-dimensional geometry |
| Fixed tolerance | C–F primary experiments keep tol=.05; B tests several tolerances; F changes tol only in graph analysis | A universal tolerance boundary |
| Fixed reference within a run | A uses 0/1, B includes an oscillation fixture with .5, C–F use (R_0=1) | One common numerical reference across all A–F or drifting truth |
| Fixed old anchor in C–F | Old anchor is 0 | Arbitrary anchors or unknown targets |
| Finite horizon | B uses 80 steps; C–F use their predefined finite post-injection clocks | Permanent persistence under all future input |
| Synthetic update rule | B explicitly defines the ordinary gate; C–F reuse it | Native HohoEngine recursion or generic belief dynamics |
| Limited seeds | C uses 3; D–F use 5; many fixtures are deterministic | Precise population probabilities |
| Binary64 arithmetic | Input construction, subtraction, and endpoint comparisons affect results | Decimal-looking values behaving like exact reals |
| Finite graph discretization | Node sets change connectivity and shortest length | A finite grid representing the full state space |
| Trusted reference harness | The policy has no reference-rewrite API | Security against arbitrary code rewriting |

## Measurement limits

Internal coherence (C) is the mean pre-update agreement `1-abs(x-b_before)` over accepted ordinary inputs at a step. If no ordinary input is accepted, (C) is undefined, not zero or one. It is not HohoEngine’s native coherence and is not a truth metric.

Distance (D=|b-R_0|) is evaluated against the fixed independent reference. C and D are saved separately, and C is not used to classify correctness.

`A_genuine_revision_candidate` is the historical label stored by C–F. “Persistent” means that the predefined finite recurrence window satisfied the frozen criterion. It does not mean permanent stability. `genuine_revision_count`, run-level classification, exact target reaching, bridge completion, and static graph path existence are different fields.

Attractor status is an operational finite check: stable tail, reference separation, phase endpoint, and a predefined set of local perturbation-return probes. It is not a proof of a global basin of attraction or a complete fixed point of every hidden state.

## Fixture-specific constraints

- Exp A’s correct apparent response is supplied by the harness. The experiment does not show autonomous discovery, deception, or intent.
- Exp B’s `reference_only` arm is an oracle control that sees the reference label.
- C/D stationary input is the repeated pair `[0,1]`, not a stream of only correct inputs.
- D’s strength (S) is an evidence-handler parameter, not input amplitude or social pressure.
- E’s (q) counts offered old-directed inputs, including intermediate values. It is not the accepted fraction or exact-zero fraction.
- E’s noisy-corrective generator clips values and does not have exact mean 1.
- F’s connected random path appends a predeclared connector to target 0; it is not an unbiased random hitting-time experiment.
- F’s noisy bridges have fixed length 25, with no resampling or repair after a gap.
- F holds the state with no input after each finite path until the 120-step clock ends.

## Public-repository boundary

The repository includes the frozen synthetic runners, raw results, figures, pinned public Hoho source excerpts, and claim-freeze evidence. It omits machine-specific absolute paths, failed-runtime search paths, workspace snapshots, and the separate Ideal E1–E8 implementation/tests/fixtures. Those omissions do not change a numerical A–F result.

Stored historical validators reported successful A–F reproducibility and regression before publication. The public portable reproducer compares newly generated CSV bytes to the frozen public snapshot without needing the private Ideal checkout.

## Not supported

The repository does **not** support claims that:

- a real LLM exhibits the same recapture mechanism;
- human beliefs follow this scalar rule;
- recursive self-improvement has been observed;
- HohoEngine natively implements the B–F ordinary RSSI recursion;
- this is an AI-alignment solution;
- the thresholds generalize to arbitrary dimensions;
- a mathematical phase transition or hysteresis has been proved;
- reference integrity survives adversarial self-rewriting;
- the Law of Attraction or supernatural manifestation has been demonstrated.

These are untested extensions, not conclusions hidden behind cautious wording.

