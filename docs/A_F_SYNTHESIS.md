# A–F integrated synthesis

## Executive summary

RSSI is a conceptual label for a synthetic recursive evaluation/update setting. The completed A–F series does not test deployed recursive self-improving AI.

The strongest supported cross-series statement is:

> In the tested scalar synthetic setup, a bounded local-update gate permits order-dependent recapture through admissible intermediate transitions; apparent correction and accepted-input coherence do not guarantee agreement with the independent reference.

The work began by separating outward correction from internal state revision (A), then separated accepted-input coherence from independent-reference distance (B). External reference injection exposed escape, relapse, rejection, and compliance (C). The strength/frequency grid separated initial update admission from later persistence (D). Post-input comparisons isolated order and path dependence (E), and Exp F formulated the mechanism as ordered admissible reachability.

## Main findings

### Apparent output and internal state are distinct measurements

Exp A’s source replay contains an external-compliance pathway whose output can change while its stored belief does not. The strongest finite contrast was 726 correct outputs and zero internally correct states in the predefined high-pressure `external_only` subset. Because the harness supplied the candidate response, this supports a measurement distinction, not an autonomous model-behavior claim.

### Internal agreement is not independent-reference accuracy

Exp B supplied an explicit counterexample to the implication (C\uparrow\Rightarrow D\downarrow). Coherence (C) was defined only from accepted ordinary inputs, while (D=|b-R_0|) used a fixed reference independently of the gate. A policy can therefore reject discrepant evidence and become increasingly consistent with its own accepted stream while moving farther from (R_0).

This does not mean coherence is always useless. D/E diagnostics found that early coherence patterns carried some information in specific fixtures, with false positives and false negatives. The frozen claim is non-guarantee, not zero predictive power in all conditions.

### External delivery, update admission, and persistence are different events

Exp C delivered independent-reference evidence outside the ordinary gate. The evidence handler could still reject it. A stored event with maximum tested strength (S=1), belief .775, and (D=.225) had support .69 and was rejected. Thus “strong evidence always revises” is false for all handler states in this implementation, even though the initial (D=1, S=1) event revises.

Exp D showed that the first-injection threshold does not determine long-run persistence. In the tested grid, strength controlled revision at the initial state, while the subsequent stationary versus descending-bridge sequence separated persistence from relapse. Repeated injection delayed relapse under one schedule but did not make escape persistent.

### Distribution summaries and endpoints omit causal order

Exp E found an existential order effect: some identical input multisets produced different outcomes when reordered. It also found a negative control where an endpoint multiset did not change outcome. A shared final offered value likewise did not determine the final belief: a fast jump was rejected while a slow admissible descent was accepted.

Exp F identified the local mechanism. The preceding accepted state determines whether the next token is admissible. For the same token `.95`, a descending trajectory presented it from `.975` and accepted it; an ascending trajectory presented it from `1`, where the Binary64 gap was `0.050000000000000044`, and rejected it.

### Reachability is not exposure count or static connectivity alone

The clearest counterexample used more direct target exposure yet no movement: 120 offers of 0 were rejected from state 1. A 21-input Binary64 bridge reached 0 because every offered transition was admissible. The statement is not that exposure count never matters; it is that count alone is not a sufficient or monotone determinant.

Likewise, a path in a static graph means suitable edges can be chosen. It does not guarantee that a fixed temporal ordering will traverse them. The same vertex multiset can be connected while an ascending presentation remains at the revised attractor.

## Falsified or weakened hypotheses

| Strong hypothesis | Counterevidence | Frozen interpretation |
| --- | --- | --- |
| Strong, repeated reference injection guarantees persistent escape | C/D descending-bridge runs relapsed even at (S=1, F=16) | Revision and delayed relapse are not persistence |
| Strength and frequency alone explain all three outcomes | D outcomes depended on the post-input regime after revision | The tested (S,F) grid is not a standalone three-phase diagram |
| Old-directed ratio (q) alone explains recapture | E/F identical multisets diverged by order | Ratio and unordered distribution can omit essential temporal information |
| Equal final input implies equal final state | E fast/slow paths ended with input 0 but different beliefs | Current state carries the effect of prior accepted transitions |
| More old-anchor exposure necessarily gives more recapture | F: 120 zeros failed; 21 bridge values succeeded | Exposure magnitude alone is insufficient |
| Static graph connectivity guarantees recapture for every ordering | F ascending/shuffled orders failed on a reachable multiset | Static reachability and scheduled reachability are different |

Rejecting a universal claim does not establish its universal opposite. For example, frequency may matter under another fixed schedule, and order does not change every multiset.

## Mathematical and implementation results

For the exact-real scalar rule, every accepted move has magnitude at most τ and every rejection has magnitude zero. Therefore

$$
|b_0-b_L|\le\sum_{k=0}^{L-1}|b_{k+1}-b_k|\le L\tau,
$$

so (L\ge\lceil |b_0-b^*|/\tau\rceil). If arbitrary intermediate points in the interval are available, equal subdivision attains the lower bound.

In the stored Binary64 implementation with `tol=float(.05)`, exact start 1, and exact target 0, an independently checked frontier leaves a positive residual after 20 updates and reaches 0 on update 21. This is an implementation result, not the real theorem and not a universal constant. Finite graph discretizations produced different minima or even disconnection depending on their node sets.

See [Mathematical core](MATHEMATICAL_CORE.md).

## Reference integrity

State update, policy-selected observation, independent reference, and evaluation were separate components. C–F fixed (R_0=1), old anchor 0, and the reference domain in an immutable harness. Changing the post-input generator did not change (R_0). The policy had no API for reference selection, deletion, rewriting, or evaluation-range narrowing.

This is integrity inside a trusted harness, not resistance to malicious code rewriting. The independent Ideal reference-integrity experiments are a separate layer and are not included as evidence for RSSI.

## Synthetic and native boundary

- **Hoho source:** pinned excerpts contain ExternalCompliance, pressure, and evidence-collapse pathways used by Exp A’s manual replay.
- **Python synthetic rule:** Exp B declares the scalar ordinary gate; C–F reuse it.
- **Independent-reference harness:** C adds fixed-reference injection and evaluation; D–F reuse it.
- **Hoho native loop:** no corresponding B–F RSSI recursion was found or claimed. Native Julia cross-checking did not complete successfully.
- **Ideal layer:** separate temporal, closed-loop, and reference-integrity work informed provenance inspection but is not part of this repository’s executable RSSI mechanism.

## What the series does not show

It does not show that real LLMs, humans, generic RSI systems, or arbitrary high-dimensional dynamics follow this gate. It does not demonstrate self-improvement, an AI-alignment solution, mathematical phase transition or hysteresis, adversarial self-rewriting resistance, or permanent escape under all future inputs.

The 21-step result and the .58/.59 grid bracket must not be treated as universal RSSI constants.

## Claim freeze

The frozen 18-claim ledger records the status, supporting experiment, artifact, counterexample, scope, and limitation for every major claim. Publication changes file placement, compression, and environment-path presentation only. It does not alter a result, classification, gate, tolerance, reference, metric, or claim status.

See [Claim ledger](CLAIM_LEDGER.md), [Limitations](LIMITATIONS.md), and the original Japanese freeze documents in [`docs/claim-freeze-ja/`](claim-freeze-ja/).

