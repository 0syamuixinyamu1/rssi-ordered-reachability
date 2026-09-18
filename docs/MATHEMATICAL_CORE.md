# Mathematical core

## Update rule

The explanatory real-scalar rule is

$$
b_{t+1}=\begin{cases}
x_t,& |x_t-b_t|\le\tau,\\
b_t,& |x_t-b_t|>\tau.
\end{cases}
$$

The Python implementation performs input construction, subtraction, and comparison in Binary64. External evidence injection is a separate handler and is not part of this ordinary gate.

## Exact-real lower bound and attainability

An accepted transition moves by at most τ, while a rejected input produces a zero move. For any (L) updates,

$$
|b_0-b_L|
\le \sum_{k=0}^{L-1}|b_{k+1}-b_k|
\le L\tau.
$$

For target (b^*) at distance (d=|b_0-b^*|), τ>0 therefore implies

$$
L\ge\left\lceil\frac{d}{\tau}\right\rceil.
$$

If arbitrary intermediate points in the real interval are available, choose (n=\lceil d/\tau\rceil) and

$$
x_k=b_0+\frac{k}{n}(b^*-b_0),\quad k=1,\ldots,n.
$$

Each gap is (d/n\le\tau), and the final input equals (b^*). Under those assumptions the lower bound is attained. If (d=0), zero updates suffice; if τ=0 and (d>0), the target is unreachable. A finite input alphabet, fixed temporal ordering, or additional state constraint can prevent equality.

For (b_0=1, b^*=0, \tau=1/20), the exact-real minimum is 20.

## Ordered paths

For a prescribed all-accepted sequence (x_1,…,x_L), with (x_0=b_0), exact target arrival is equivalent to:

1.  (|x_k-x_{k-1}|\le\tau) for every step, and
2.  (x_L=b^*).

If rejections are allowed, the relevant predecessor is the current simulated belief, not necessarily the preceding offered value. Other accepted tokens can move the state, so the existence of a convenient subsequence or an unordered graph path is not sufficient for a fixed presentation order.

One rejection is also not necessarily permanent: Exp F’s high/low alternating order rejected 37 inputs for seed 7 and later reached the target. In contrast, a monotone descending sequence with one super-tolerance gap and no later return into the admissible neighborhood remained blocked.

## Binary64 exact-target minimum

The stored tolerance has hex representation `0x1.999999999999ap-5` and exact rational value

$$
\frac{3602879701896397}{72057594037927936}.
$$

For each nonnegative Binary64 belief (b), Exp F computed (f(b)), the smallest representable next state accepted by the existing gate. Every selected endpoint was checked as accepted and its immediate lower representable neighbor as rejected. Monotonicity of correctly rounded subtraction makes (f^{(k)}(1)) a global lower frontier after (k) updates, including paths that reject, detour, or move upward.

The frozen frontier records

$$
f^{(20)}(1)
=\frac{211}{288230376151711744}
=7.320533068622126\times10^{-16}>0,
\qquad f^{(21)}(1)=0.
$$

Thus the exact target 0 is unreachable in at most 20 updates and is reached by the 21-step witness under the current implementation. The certificate is stored in [`float_frontier.csv`](../experiments/rssi_admissible_bridge/results/float_frontier.csv) and [`analysis.json`](../experiments/rssi_admissible_bridge/results/analysis.json).

**This does not make 21 a theoretical constant.** It depends on the current Binary64 state space, tolerance representation, subtraction, comparison, interval, and exact target.

## Numerical boundary example

Although `.95` and `.05` look like an exact tolerance-sized move, the implemented difference `abs(.95-1)` is `0.050000000000000044`, so the first input is rejected. The first frontier input `.9500000000000001` is accepted. Nominal δ=.049 and .0499 paths reached 0 in 21 accepted inputs; the stored δ=.05, .0501, and .051 paths rejected at the first step.

Using the representable number immediately below `.05` as δ did not fix this particular generated path: `1-delta` still rounded to `.95`, and its generated endpoint was not exact 0. The experiment did not append a favorable target after observing failure or add epsilon to the gate.

## Discrete graph cross-check

At tol=.05, frozen finite graphs gave:

| Node set | Nodes | Components | 1→0 shortest length | Shortest-path count |
| --- | ---: | ---: | ---: | ---: |
| `i/20` | 21 | 9 | unreachable | 0 |
| `i/40` | 41 | 1 | 28 | 576 |
| `i/80` | 81 | 1 | 23 | 128 |
| `i/40` plus Binary64 frontier | 61 | 1 | 21 | 14 |

Discretization can remove necessary intermediate values and alter connectivity or path length. The count is the number of shortest paths, not all walks. Static connectivity describes whether edges can be selected freely; it does not imply target arrival under every temporal order.

## Evidence types

| Evidence | Supported conclusion | Not implied |
| --- | --- | --- |
| Exact-real analysis | Lower bound and attainability with free intermediate points | Binary64 behavior or an LLM claim |
| Binary64 frontier certificate | Exact-target minimum 21 for the stored implementation | A universal constant or nearby-target result |
| Finite experiments | Specific order, gap, exposure, and noise counterexamples | A probability law over all paths |

The existing relapse classification uses five consecutive steps within a .05 neighborhood of the old anchor. Exact target `b==0`, bridge completion, and relapse time are distinct quantities.

