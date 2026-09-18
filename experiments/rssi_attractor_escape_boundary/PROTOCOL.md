# Exp D protocol — fixed before primary execution, 2026-09-17

Question: within the fixed Exp C model, what strength/frequency boundaries separate rejection, relapse and persistent escape? No optimization target or result-dependent tuning.

## Prerequisite and invariants

Exp C validation was run in an isolated copy before this file was created: all 54 runs reproduced, all five numerical CSV hashes matched, 12 C audit groups and 12 prior RSSI checks passed. Evidence: results/exp_c_regression.json.
Import the existing C runner; reuse Reference, Recorder, reach_attractor, normal_batch, summarize, and all numerical constants unchanged. Exp A/B are imported by C unchanged. No monkey-patching of classification, horizon, strength meaning, tolerance, reference, input regime or attractor definition.
R0 remains C's frozen full-domain scalar reference=1, D=abs(b-1), ordinary tol=.05, support=.6*S+.4*D_before >=.75. External delivery bypasses the ordinary gate; it does not force state assignment on rejected evidence.

## Primary grid

S=[.1,.2,.25,.3,.4,.5,.55,.58,.59,.6,.7,.75,.8,.9,1].
F=[1,2,3,4,8,16]. Seeds=[7,17,29,41,53].
Two separate strata: stationary and descending_bridge, exactly C's existing streams before and after intervention. They are not tuned grid variables.
90 cells per stratum, 180 total, five seeds each: 900 primary runs.
The extra .58/.59 points are fixed a priori around the existing handler's initial-state threshold (.75-.4)/.6. This is not a result-driven refinement or a newly discovered universal critical constant.

F counts forced deliveries in the same window [0,20]. For F=1: schedule=(0,). For F>1: integer steps nearest to 20*i/(F-1), i=0..F-1, using (20*i+(F-1)//2)//(F-1). No duplicate times. F=3 gives exactly (0,10,20). Timings for different F are not all nested: F's effect refers to this specified schedule family, not an isolated dose-rate law.
All runs resume ordinary update through post-step120, with at least100 ordinary steps after final injection. Use the same C summary and classifications. D_post retains C's final20-step mean, while D_immediate_first denotes the instantaneous response. Do not substitute the user's illustrative D_post notation for C's saved metric.

## Controls

No-injection and ordinary-gate-only reference at(0,10,20): 2 regimes*5 seeds*2 controls=20 additional runs; 920 total.
C's single/repeated baselines at S=.25,.75,1 and original seeds7,17,29 are contained exactly in the grid (F=1,3); compare all original numerical summary fields. C's no-injection and gate-only controls are also matched. Do not re-run compliance as a new primary factor.

## Boundaries and dynamics

Keep complete C labels, including mixed/partial if observed. For each fixed F, record adjacent sampled S changes in the full observed outcome distribution, and vice versa. Do not force monotonicity or a three-stage order.
Also report minimum sampled S (and minimum sampled F) producing (i) any qualifying revision, (ii) any persistent escape. Give the preceding tested value as the lower bound, distinguish already present at the lowest sample and not observed in range. For seeds, report observed counts/rates, not estimated population probabilities. Retain every reversal, if any, in adjacent-transition tables.
T_relapse: C's first qualifying revision to the first step of a five-step confirmation block; also record confirmation and time since last scheduled injection. No eligible revision => NA, no observed relapse => censored/NA, never zero.
Report whether changes in S/F delay relapse without yielding persistence. Do not identify a discontinuity in an explicit threshold handler as a mathematical thermodynamic phase transition.

## Coherence diagnostic (descriptive, fixed before results)

Keep full C_t and D_t for every run. For primary runs, compare mean baseline last20 C, mean first20 post C, mean last20 post C, and the full first20 C vector, treating NA separately. Evaluate within each regime and in pooled data; report the majority-class baseline.
For each feature use leave-one-seed-out majority label lookup based solely on that rounded(12 decimals) C feature, with training-set majority fallback for unseen features. Report feature label-collisions and observed accuracy on all cells and the preregistered S=.58/.59 boundary subset. This is a descriptive separability diagnostic. Repeated seeds can have identical paths; it is not an independent generalization test. Early features occur after injection; late features are retrospective, not prospective prediction.

## Optional test

No hysteresis experiment is included in the primary specification: independent cells reset to the same attractor. Do not infer hysteresis from these reset cells or from a delayed-relapse pattern. A controlled up/down sweep with carried state would be a separate optional experiment; it is not required to complete D.

## Validation and preservation

Hash all existing A/B/C files before D and verify unchanged afterward; preserve original Ideal repository (clean ed8168a). Independently replay logged scalar events and C/D, verify baseline/local probes, schedules, classification and metric arithmetic; compare overlapping C controls; include boundary-analysis negative fixtures for broad/mixed/nonmonotone patterns. Run full fixed-seed D reproduction to a separate output directory and compare all main CSV hashes. Run existing C/RSSI validation only in an isolated copy to avoid overwriting C validation artifacts.
No native-Julia success requirement: D is Python synthetic. Existing native runtime failure is not repaired by changing Hoho or experiment design.
