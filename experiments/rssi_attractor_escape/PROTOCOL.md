# Exp C — protocol fixed before execution

Date: 2026-09-16. This is a minimal extension of the existing Python RSSI harness. No native Julia run is claimed. The existing `offer` and `replay_a` functions are imported, not rewritten. Hoho and Ideal source and old fixtures/results remain unchanged.

## Question and scope

Can an independently delivered correct counterexample produce a lasting departure from an incorrect attracting belief state, after ordinary gated recurrence resumes? All claims concern a scalar synthetic belief and the declared input families. They do not concern autonomous learning or self-modifying RSI.

## State, reference, and ordinary inputs

`B={'known': b}`, b in [0,1]. R0 is the immutable full-domain tuple `(('known',1.0),)`. Primary D=abs(b-1). Normal updates call the prior harness's `offer(..., policy='gated', tol=0.05)` unchanged. It admits unknown topics and updates known topics only within tolerance. The evaluator is never passed as a mutable object to the policy; no dimension masks, weights, alternate references or deletion actions are available.

Two predeclared ordinary input regimes are each used unchanged before and after injection:

1. **stationary**: existing frozen fixture's ordered batch [0,1] every step.
2. **descending_bridge**: period 40; first candidate is `1-((step-1) mod 40)/40`, followed by candidate 0. This is a new Exp C input fixture based on the previous bridge counterexample, with unchanged update logic. It allows checking whether a corrected belief can subsequently follow individually admissible small steps back toward 0. Values/order are exogenous, shared across all arms, and never adapted to observed outcomes.

`C_internal` retains the previous `accepted_agreement` definition: mean(1-abs(input-belief_before_input)) over accepted normal inputs in the current step. Empty sets are NA, not 1. Every input and every state change is also logged. No native Hoho coherence, constitutional or panic metric is invented.

## Attractor detection

Seeds 7,17,29 determine initial b uniformly in [0.005,0.04]. Baseline maximum 400 steps. Declare an attracting **step-boundary belief** only if:

- the last W=max(10,2*period) consecutive step-end beliefs have range <=1e-12;
- every step-end change in that window is <=1e-12;
- D>=0.5 and the repeated state is at least 0.2 from R0;
- the current phase completes a period;
- independent local probes b±tol/4 and b±tol/2, clipped to [0,1], as well as b itself, return to the same belief after one complete period, checked from every phase.

Failure stops that baseline and is reported; it is not replaced with a preferred seed. The finite probes are not a global attractor theorem. Counters/history grow; the full augmented state is not called a fixed point. The periodic regime may have sub-step changes even when step-end belief is fixed.

## Arms (paired at each baseline)

- C0: no external or extra input; ordinary stream only.
- C1: at times 0,10,20, offer correct input 1 through the ordinary gate. No bypass.
- T1: at time 0, deliver input 1 directly to the prior `evidence_revision` path, bypassing `offer`.
- T2: the same independent delivery at times 0,10,20.
- Diagnostic B: at time 0, pass input 1 as the corrected response to prior `external_only`, pressure=1. This is a diagnostic comparator, not an evidence treatment.

T1/T2 evidence_strength in {0.25,0.75,1.0}. `contradiction_strength=abs(b-R0)` is computed by the independent harness at the moment of injection. Prior support formula and threshold remain 0.6*e+0.4*c >=0.75. Delivery bypasses self-selection, but a delivered input need not pass the existing evidence-update threshold. There is no unconditional forced belief assignment. The supported candidate is R0=1 for every treatment, regardless of strength.

All arms run 120 ordinary steps after initial injection, so repeated arms include 100 ordinary steps after the final scheduled injection. An injection at post-step k happens after normal step k and before normal step k+1. The normal stream, phase, seed and baseline are matched across arms. Total planned runs: 2 regimes × 3 seeds × 9 arms =54.

## Outcomes defined before results

- A **qualifying revision** is an injection-induced D reduction >=0.1, measured from actual state, not a flag.
- **Relapse** after a qualifying revision: 5 consecutive normal step-end states within 0.05 of the baseline belief and with D>=D_pre-0.05. Report the first step of the confirming block, plus the confirmation step; times are measured from first qualifying revision and last scheduled injection separately. Earlier repeated treatments may intervene before relapse; timings are for the complete assigned schedule, not isolated-event causal effects.
- **Persistent escape / genuine revision candidate**: at least one qualifying revision, no relapse after the final qualifying revision, and every normal step in the final 100-step withdrawal window has D<=D_pre-0.1. Count genuine revisions only if an injection's qualifying improvement is maintained for the remaining normal steps. This is finite-horizon persistence, not permanent escape.
- **External compliance**: corrected output/flag without state movement, and no qualifying revision; record code `internal_revision=false` separately from actual state delta.
- **Rejection**: a contradictory input was delivered/offered but no qualifying change or apparent correction occurred. Distinguish ordinary-gate rejection from evidence-threshold rejection. If already at R0, unchanged state is an already-correct no-op, not rejection.
- **Relapse class** overrides initial revision for the run-level endpoint. Mixed/partial/transient cases remain explicit if these conditions fail.
- **Reference corruption / avoidance**: not available as an RSSI action. E8 has a separate contamination experiment, but no existing bridge to this scalar RSSI policy. Do not add one. Normal filtering is counted as rejection, not reported as a change in the independent evaluator.

Report D_pre, immediate D, final D, mean D over final 20 normal steps, delta_D=that mean-D_pre, all step C/D, normal acceptance/rejection rates, external delivery/update counts, qualifying/genuine revision counts, apparent correction counts, relapse rates conditional on qualifying revisions (and all-run rates separately), time-to-relapse, persistent escape rate. A zero eligibility denominator is NA.

## Verification and interpretation

Freeze source/old-result hashes; replay raw event transitions independently; independently rederive C/D/counts/classifications; verify paired normal inputs and reference bytes; run deterministic replay once in a separate output directory and compare CSV hashes. Keep old results unmodified. No result-based parameter tuning. Positive and negative outcomes are equally reportable.
