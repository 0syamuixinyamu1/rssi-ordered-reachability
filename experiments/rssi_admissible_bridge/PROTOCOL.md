# Exp F protocol — fixed before F trajectory execution

2026-09-17. Question: which finite ordinary-input paths reach exact belief0 from corrected belief1 under the unchanged scalar gate? No outcome optimization. All A–E results and original Ideal source are frozen by hashes. E has first been reproduced in a separate directory: all330 runs and10 CSV byte matches, including25 representative baseline A/B/C/D runs.

## Invariants and separate outcomes

Import E and use its D/C utilities. tol=.05, domain={'known'}, R0=1, anchor0; no epsilon added to the gate abs(x-b)<=tol. State changes only to accepted x. Reuse C.Reference, Recorder, reach_attractor, summarize, relapse_blocks; use E.no_input_summary solely for the all-empty control. S=1/F=1 injection at0 after the C stationary attractor. All finite paths are fully generated before any run's baseline or injection, without outcome/classification access. Planned previous input is allowed for constructing an admissible path; it is not the simulated belief.

Every run has120 post clock steps. One input per path step, then empty batches to120. No padding with0 and no corrective inputs after the finite path. C/D/E classification is unmodified: qualifying gain.1, five-step relapse block within.05 of anchor, final100-step improvement criterion; undefined C stays NA. Empty hold steps observe state and count toward the existing clock-based criterion; they create no events. Target reaching is a separate exact b==0 test, not the .05 relapse neighborhood. Log both first exact hit and final exact hit. Relapse can therefore occur without exact target reaching. 'Bridge completion' means a nonempty path ending in input0, all its inputs accepted, and final b==0. 'Target reachable under this presented order' means any exact b==0 hit; it is not the unordered-set graph criterion.

## Analytical candidates before simulation

For exact real arithmetic with tau=1/20, any path of L updates has net displacement<=L*tau, so L>=ceil(1/tau)=20. Monotone .05 steps attain20 over reals. This is a mathematical candidate, not a float result. Rejecting inputs cannot reduce that bound. An all-accepted prescribed path is admissible iff every consecutive gap, including initial1 to first input, is<=tau; its endpoint must be0 to attain the target. For paths with rejections the actual accepted subsequence matters, so a graph path using the same unordered values does not ensure success in a given order.

For nonnegative binary64 states, compute f(b)=smallest representable y in[0,b] with abs(y-b)<=float(.05). Find f by binary search on ordered IEEE754 bit patterns. Verify each endpoint is accepted and its immediate predecessor is rejected (unless endpoint0). f is nondecreasing because correctly rounded subtraction is monotone; the smallest state reachable after k updates is f iterated k times from1. This frontier provides a global scalar-float lower bound, including nonmonotone paths, not just a greedy heuristic. Stop at first exact0, cap1000 iterations with explicit failure. Determine whether float L equals20 or differs; do not change tol or adjust results. Save the frontier and float hex/ratios for independent cross-check with Fraction and nextafter.

## Finite conditions (34 per seed, 5 seeds)

Controls (4): no_input;120 zeros (E abrupt q1); E gradual(v=.025,q1); E fast(v1,q1). Reuse E.sequence for the three nonempty controls. The gradual control also supplies the descending order arm below.

Minimum (4): the float-frontier path; equal-partition paths x_k=1-k/L for L=19,20,21. Do not confuse this arithmetic expression with 1-k*delta.

Step size (8): decimal delta=.025,.049,.0499,.05,.0501,.051 plus nextafter(.05,0) and nextafter(.05,+inf). x_k=max(0,1-k*delta), k=1..ceil(1/delta). Log actual consecutive gaps; the floating multiplication/subtraction can make gaps differ from nominal delta.

Broken bridges (6): valid base x_k=max(0,1-.04*k), k1..25; delete input at original1-based position2(early),13(middle),24(late), one at a time. These intended gaps are.08, with the remaining future path decreasing. Also include base .02 k1..50 and its single deletion at position25; this redundant-point comparison makes a gap.04. Do not assume every point deletion blocks reachability.

Geometry (5): dyadic monotone 32 steps of1/32; detour1->.5->.75->0 with step1/32 (48 inputs); oscillatory32 cycles of(-1/32,+1/64,-1/64), 96 inputs; random admissible64-step prefix with seeded equal-probability +/-1/32 clipped to[0,1] then a predeclared monotone1/32 connector from the planned endpoint to0; same random prefix alone. The connector is fixed construction before replay, not an adaptive response to failure. The free-prefix control tests that local admissibility alone need not reach a target. Report that the connector variant conditions the endpoint and is not an unbiased hitting-time experiment.

Order (3 additional): reuse E's120-value gradual(.025,q1) multiset and descending control; add ascending, alternating high/low, and seeded shuffle (same E order seed string). Track source token indices, including repeated0 values. Five seeds give five fixed shuffles. At each pair record first aligned-step belief difference and first aligned-step acceptance-flag difference; different offered values at the same clock are not a same-input causal comparison. Separately match identical input tokens and log differing acceptance outcomes with both preceding beliefs and steps; select the earliest such witness in order A. Save all witnesses, not just final labels.

Noise (4 additional): perturb interior points of the .04 base by independent Uniform(-eta,eta), clip[0,1], preserve final input0; eta=.001,.004,.006,.012. The unperturbed base above is eta0. Use same seeded unit-noise draws for levels. No resampling, repairing gaps, adding inputs or changing ordering based on results. Offered length stays25 by design; report this limitation for any path-length extension question.

## Graph analysis (separate from primary dynamics)

V={i/n: i=0..n}, n=20,40,80. Build edges iff existing BASE.offer accepts the target at the selected tolerance; no self loops. Primary comparison tol=.05; contrast tolerances .049/.051 apply ONLY to analysis graphs, never to C constants or primary trajectories. Add one witness-augmented n40 graph containing every float-frontier node at tol=.05. Compute connected components, path existence from1 to0, BFS shortest length, exact count of shortest paths, and one witness. Because undirected edges allow arbitrarily many walks, do not call shortest-path count the count of all paths. Save edge lists and node membership, compare graph witnesses with the existing offer implementation, and distinguish discrete graph minima from the all-binary64 frontier. Use exact Fraction arithmetic for independent graph and gate endpoint validation.

## Metrics and validation

Path length=number offered ordinary inputs, excludes initial1 and empty holds. TV includes the initial transition from1; also save input-only TV. Record accepted/rejected count, first rejection, requested consecutive gap, actual belief-input rejection gap, maximum excess overtol, finalbelief/D, exact first target step, finaltarget, bridgecompletion, T_relapse, C_t/D_t. Actual accepted moves excludes accepted self-loops. Global float minimum and exact-real lower bound are separate.

For each offered-value set plus1/0, compute static graph reachability/shortest path at.05; compare with actual ordered replay and consecutive-input adjacency. Adding0 to this diagnostic set does not insert it into the input trajectory. Log endpoint presence. All plotted results derive from saved CSV; figures never classify.

Independent validation replays raw events without C's update function, audits states/counts/C/D, exact target metrics, all classification windows, generated paths, geometry/noise bounds, token multisets and divergence witnesses. Negative fixtures cover reachable-set-but-wrong-order, locally disconnected-but-later-restored path, five-step relapse and reference-domain mutation. Independently audit float frontier using exact Fraction differences and adjacent representable values, and graph BFS with separate algorithm. Rerun F and graph analysis in a separate output directory, compare CSV bytes. Execute unchanged E validator in an isolated A–E copy, which invokes D/C/RSSI regression. Recheck all109 A–E files and170 Ideal tracked files. Native Julia remains outside this experiment; no engine changes.
