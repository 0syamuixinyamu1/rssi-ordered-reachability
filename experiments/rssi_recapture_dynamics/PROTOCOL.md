# Exp E protocol — fixed before primary execution, 2026-09-17

## Question and hypothesis

Which post-injection input structures recapture a corrected belief? Predeclared hypothesis: persistent versus relapsing outcomes may be better explained by post-injection input distribution than by injection itself. Distribution alone is not assumed sufficient: test temporal order at identical multisets. No success maximization or outcome-dependent tuning.

## Prerequisite and invariants

Fifteen saved D representative conditions, including stationary persistence, descending relapse, weak-strength rejection and repeated controls at the original seeds7/17/29, were reproduced before E. All common summary fields matched; see baseline_reproduction.json.
Reuse C (imported through D): Reference, Recorder.event/snapshot, normal_batch, reach_attractor, summarize, relapse_blocks, constants. Do not modify A/B/C/D or Hoho/Ideal. R0=1, domain={'known'}, tol=.05, gate uses the existing binary-float comparison without adding epsilon. S=1, F=1, injection at post-step0. Horizon120. Original C/D outcome definitions and final100-step persistence window stay fixed. D_post is still the final20-step mean, not instantaneous D.
All new families use C stationary baseline. The existing descending_bridge control retains its own C baseline and phase. Their attained belief is0 and injection makes it1; the scalar update has no hidden accumulated memory. No-input control still records120 clock steps with zero input events.

C.summarize divides by zero when the post-input count is zero. For this one control only, use a harness adapter that verifies zero inputs and constant post-injection state, applies the unchanged state-based persistence/relapse criteria, and reports acceptance/rejection rates as NA. Do not inject dummy inputs or change C. All nonempty sequences use C.summarize directly. Keep C's mixed_or_partial_escape label; no new oscillatory classification.

## Exposure definitions (fixed)

R input: value exactly1 within1e-12. O input: value<1−1e-12, i.e. any move in the direction of old attractor0, including intermediate bridge values. q is O offered inputs / all offered post inputs, whether accepted or rejected. It is not a count of inputs currently contradicting belief. Also log old-halfspace share(value<.5) and exact-old count(value0) so 'old direction' is not confused with proximity to0. No-input q is NA, not0. Family intent (e.g. noisy_corrective) is separate from this value-based direction.
For endpoint and drift grids, q=[0,.1,.25,.5,.75,.9,1], N=120, n_O=round(q*N). Actual q is logged and verified, not inferred from a label.
v is a nonnegative speed toward0 per clock step; drift candidate x_t=max(0,1−v*t). Values are precomputed before simulation, independent of belief and outcome.
v=[.01,.025,.04,.049,.051,1]. No extra v after viewing results.

## Families and controls

1. stationary: exact C/D normal_batch('stationary',baseline_steps+t), ordered[0,1] each step. Not mislabeled pure-correct input. Fixed q=.5.
2. descending_bridge: exact C/D normal_batch and phase, two inputs per step. Fixed observed q; no alterations.
3. no_input: empty batch every step,120 state observations.
4. abrupt_return: first n_O steps value0, remaining steps value1. Sweep q. Old inputs are introduced immediately when q>0.
5. gradual_drift: q×v grid. O steps use max(0,1−v*t), R steps use1. O mask is floor(n_O*t/120)>floor(n_O*(t−1)/120), distributing O exposures over time. v is per clock step, not per accepted event.
6. alternating: same evenly spread O mask but O=0 and R=1. At q=.5, sequence is R,O,R,O,... Sweep q.
7. sparse_corrective: q=[.75,.9,1]. Uniform R positions use floor(n_R*t/120)>floor(n_R*(t−1)/120); others are0. For q=.75 this is O,O,O,R,... Distinct temporal phase from alternating.
8. noisy_corrective: x=clip(1+Uniform(−.08,.08),0,1), fresh seeded RNG independent of initial belief RNG. Nonzero noise with exact mean1 is impossible on[0,1]; this clipped distribution has expected mean.98, within tol of1. Record empirical mean/q; do not claim exact zero-mean noise about R0.

Endpoint same-multiset order test, q=.5: reuse abrupt_return(.5) for O-first, alternating(.5) for interleaving, add R-first(60 ones then60 zeros).
Bridge same-multiset order test: take gradual_drift(v=.025,q=1)'s120 values; reuse descending order, add sorted ascending and seed-shuffled permutations. Log multiset hash and actual q; changing order never edits values. Endpoint and bridge order tests are separate.
Fast/slow path check reuses gradual_drift(q=1,v=1) and gradual_drift(q=1,v=.025); both end at input0. Report path-dependent only if the observed state/outcome differs. Do not call it mathematical hysteresis.

66 configs total:4 fixed controls/families +7 abrupt +42 gradual +7 alternating +3 sparse +3 added order variants. Five seeds gives330 runs. The generated condition manifest must match these counts before execution. The four fixed cases are stationary, descending_bridge, no_input, noisy_corrective. No parameter is selected based on outcome.

## Metrics and thresholds

D_min includes immediate post-injection state and all post-step states. C_t, D_t and all offered/accepted/rejected inputs are logged. Recapture latency=T_relapse from injection0 to C's first step of the5-step confirming block. NA if no relapse.
For relapsing runs:
- net recapture slope=(D_at_relapse_start−D_immediate)/latency;
- active recapture slope=mean of strictly positive consecutive-step D increments up to relapse start, with initial D_immediate at t0;
- offered and accepted R/O exposures before failure include all ordinary events through the relapse-start step, exclude forced injection. For nonrelapsing runs these failure counts are NA; full-horizon exposure totals are separate.
Thresholds: for each family (and each fixed v in gradual), report adjacent tested q points where the observed label distribution changes, minimum q with relapse, previous tested q and whether it was purely persistent. For gradual at fixed q do the same along v, retaining reversals; recapture can disappear at higher v. A single q point cannot identify q_c. Never turn an absent boundary into a finite estimate or assume monotonicity.

## Coherence diagnostic

Predeclare early window steps1..10 and alarm: mean of defined C values <.99−1e-12. Entirely undefined window -> unavailable, not normal/high C. Calculate TP/FP/FN/TN against eventual relapse, separately mark any relapse at or before10 as not a prospective case. Report high coherence C>=.95−1e-12 at relapse and over returning segments. This fixed diagnostic is not tuned or a generalization-performance estimate. An alarm in a persistent noisy series and a missed slow relapse remain valid negative observations.

## Validation and preservation

Freeze existing file hashes. Independently audit transitions, schedules, class definitions, R/O counts, slopes and times. Check exact multiset equality and final-input equality. Test no-input rates NA. Match existing D summaries for controls. Execute C and D regression in isolated copies; original outputs never overwritten. Reproduce E to another output directory and compare CSV bytes. Scientific figures are explanatory, never classification inputs. Julia runtime issue remains outside this task's success criteria.
