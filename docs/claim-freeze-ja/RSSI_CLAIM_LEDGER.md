# RSSI A–F Integrated Claim Ledger
固定日：2026-09-18。18 claimを固定します。statusは下記の命題そのものに付けます。支持命題の反例欄には、過大な読み替えへの反例も明記します。有限のcounterexampleで普遍命題は棄却できますが、全条件で逆命題が成立するとは結論しません。
## Evidence categories
| Status | この台帳での意味 |
| --- | --- |
| Analytically supported | 仮定を明示した更新則からの演繹。 |
| Supported by synthetic experiment | 保存済みsynthetic対照実験による存在例・反例。一般化は対象model内。 |
| Supported by finite fixtures only | 指定した有限fixture/seedでの記述。確率法則や普遍境界ではない。 |
| Implementation-dependent | 現在のgate、数値表現、端点比較など実装条件に依存。 |
| Suggestive only | 次の問いを動機づけるが、移植先の支持証拠はない。 |
| Not supported | 対象に対応する測定・証明がない。反証と混同しない。 |
| Falsified / rejected hypothesis | 命題の普遍的・十分条件としての形に、範囲内の反例がある。 |

複数の証拠種がある場合は主statusと補足を分離しています。たとえばClaim 11は実装についての解析証明書を持ちますが、実数上の一般定理と同じ欄には置きません。
## Claim overview
| ID | Claim | Status |
| --- | --- | --- |
| 1 | 内部coherenceの改善は外部referenceとの一致を保証しない。 | Supported by synthetic experiment |
| 2 | apparent correctionはinternal revisionを保証しない。 | Supported by synthetic experiment |
| 3 | 強い外部反証は必ずbeliefを修正する。 | Falsified / rejected hypothesis |
| 4 | 外部反証を繰り返せばPersistent Escapeになる。 | Falsified / rejected hypothesis |
| 5 | post-injection input distributionだけでRecaptureを説明できる。 | Falsified / rejected hypothesis |
| 6 | 同一multisetでも順序が結果を変え得る。 | Supported by synthetic experiment |
| 7 | 同じ最終入力なら最終beliefも同じになる。 | Falsified / rejected hypothesis |
| 8 | 旧anchor入力の量がRecaptureを決める。 | Falsified / rejected hypothesis |
| 9 | 逐次的に受理可能なpathがRecaptureに重要である。 | Supported by synthetic experiment |
| 10 | 実数scalar gateでは最短到達長に L_min >= ceil(|b0-b*|/τ) が成立する。 | Analytically supported |
| 11 | 現在のbinary64実装でb=1から厳密な0への最短長は21である。 | Implementation-dependent |
| 12 | 静的graphが連結なら、任意の入力順序でもRecaptureする。 | Falsified / rejected hypothesis |
| 13 | Fの固定noise条件ではη=.006で2/5、η=.012で0/5がtargetへ到達した。 | Supported by finite fixtures only |
| 14 | 実LLMにも順序感度を独立に監査する価値があるかもしれない。 | Suggestive only |
| 15 | A〜Fは実LLM、RSI一般、人間のbelief、native Hoho再帰を実証した。 | Not supported |
| 16 | 既知入力の受理agreement平均Cは、実数上、定義される場合1−tol以上である。 | Analytically supported |
| 17 | Reference integrityはadversarial code rewritingにも保証される。 | Not supported |
| 18 | Sの境界.58/.59はRSSI一般のcritical constantである。 | Not supported |

## Claim 1

内部coherenceの改善は外部referenceとの一致を保証しない。

**Status:** Supported by synthetic experiment

**Supporting experiment:** B; C–Fで補強

**Supporting artifact / selector:**

- [b_trajectories.csv](../../results/b_trajectories.csv)：fixture=drift_away, policy=gated, tol=0.05, step=1/80（support）
- [coherence_diagnostic.csv](../../experiments/rssi_recapture_dynamics/results/coherence_diagnostic.csv)：保存済みearly-C診断。予測力が常にゼロという別claimは採用しない（support）

**Counterexample:** 保証への反例：BのCは0.9619349672→0.9999858876、Dは0.6380650328→0.9998658149。claim自体への反例ではない。

**Scope:** 受理入力agreementというC定義と独立reference距離Dを用いたsynthetic系。

**Limitation:** native coherence一般の性質ではない。Cの早期変化が一部fixtureで情報を持つことは否定しない。

## Claim 2

apparent correctionはinternal revisionを保証しない。

**Status:** Supported by synthetic experiment

**Supporting experiment:** A; C compliance control

**Supporting artifact / selector:**

- [a_summary.csv](../../results/a_summary.csv)：policy=external_only/imaginary_only, high_pressure_cases=726（support）
- [a_trials.csv.gz](../../results/a_trials.csv.gz)：初期誤り・正しいhypothesis・pressure_score>=0.6。output_scoreとinternal_scoreを比較（support）

**Counterexample:** 保証への反例：external_onlyでは726/726で外部出力が正しく、内部正答は0/726。

**Scope:** 固定sourceのPython replayと、外部出力を供給するharness。

**Limitation:** この分離はhandlerに明示された実装でもある。自律的な欺瞞、隠蔽意図、LLMの内面を実証しない。

**Additional evidence:** コード上の分離にも依存。

## Claim 3

強い外部反証は必ずbeliefを修正する。

**Status:** Falsified / rejected hypothesis

**Supporting experiment:** C; Dの初回gate条件との対照

**Supporting artifact / selector:**

- [event_log.csv.gz](../../experiments/rssi_attractor_escape/results/event_log.csv.gz)：run_id=descending_bridge_7_T2_repeated_1.0, phase=injection, step=10（counterexample）

**Counterexample:** S=1でもb=.775、D=.225の時のsupportは.69<.75。外部から配送済みなのにevidence_threshold_rejectionとなりbは不変。

**Scope:** 現在のevidence handler全イベントに対する『必ず』を棄却。

**Limitation:** 初回D=1ならS=1は改訂される。入力振幅、social pressure、証拠strength Sを混同しない。通常gateへの提示と強制配送も区別する。

## Claim 4

外部反証を繰り返せばPersistent Escapeになる。

**Status:** Falsified / rejected hypothesis

**Supporting experiment:** C/D

**Supporting artifact / selector:**

- [summary.csv](../../experiments/rssi_attractor_escape_boundary/results/summary.csv)：group=primary, regime=descending_bridge, evidence_strength=1.0, frequency=16（counterexample）
- [relapse_times.csv](../../experiments/rssi_attractor_escape_boundary/results/relapse_times.csv)：S=1, F=1とF>1の保存済みT_relapse（support）

**Counterexample:** S=1、F=16でも5/5がRelapse。F=1のT=39に対しF>1はT=79で、最終Dは1。

**Scope:** 固定された有限注入windowと検証済みF∈{1,2,3,4,8,16}。

**Limitation:** 無限頻度、永久介入、別時刻配置でも必ず失敗するとは言えない。

## Claim 5

post-injection input distributionだけでRecaptureを説明できる。

**Status:** Falsified / rejected hypothesis

**Supporting experiment:** E/F

**Supporting artifact / selector:**

- [order_effects.csv](../../experiments/rssi_recapture_dynamics/results/order_effects.csv)：multiset_group=bridge_values。same_multiset=Trueの比較（counterexample）
- [order_divergence.csv](../../experiments/rssi_admissible_bridge/results/order_divergence.csv)：同じ120 tokenの各順序（support）

**Counterexample:** 同じbridge multisetでdescendingはRelapse、ascending/shuffledはPersistent。qもmultisetも一致する。

**Scope:** distributionを順序を捨てた値の経験分布・割合と解したclaim。

**Limitation:** 時間順序を含む完全な同時分布なら別命題となる。『distributionが無関係』とは結論しない。

## Claim 6

同一multisetでも順序が結果を変え得る。

**Status:** Supported by synthetic experiment

**Supporting experiment:** E/F

**Supporting artifact / selector:**

- [order_divergence.csv](../../experiments/rssi_admissible_bridge/results/order_divergence.csv)：seed=7, descending対ascending: first_divergence_step=1（support）
- [order_acceptability.csv](../../experiments/rssi_admissible_bridge/results/order_acceptability.csv)：x=.95の同一token、descending step2対ascending step119（support）

**Counterexample:** 『常に変わる』にはEの60R/60O multisetが反例。15 endpoint比較で分類差は0。

**Scope:** 存在命題。同じ値でも先行beliefが異なり、同じtokenの受理が変わる。

**Limitation:** 有限の順序・5つの固定shuffle。任意順序で違いが出る主張ではない。

## Claim 7

同じ最終入力なら最終beliefも同じになる。

**Status:** Falsified / rejected hypothesis

**Supporting experiment:** E; F controlで継承

**Supporting artifact / selector:**

- [path_dependence.csv](../../experiments/rssi_recapture_dynamics/results/path_dependence.csv)：全5seed, final_input=0, fast v=1 / slow v=.025（counterexample）

**Counterexample:** 最終入力0でもfastはD_final=0、slowはD_final=1。全5組で分類が異なる。

**Scope:** 同じ注入条件・初期状態から異なる入力履歴を通るscalar系。

**Limitation:** 同じ現在beliefと同じ次入力なら同じ更新。追加の記憶変数や数学的ヒステリシスを証明しない。

## Claim 8

旧anchor入力の量がRecaptureを決める。

**Status:** Falsified / rejected hypothesis

**Supporting experiment:** E/F

**Supporting artifact / selector:**

- [bridge_summary.csv](../../experiments/rssi_admissible_bridge/results/bridge_summary.csv)：condition_id=control_abrupt0 / minimum_float_frontier、各5seed（counterexample）

**Counterexample:** 120回の0は全拒絶しb=1のまま。21入力の完全bridgeは全受理してb=0。

**Scope:** 提示量だけによる決定・単調な保証を棄却。bridgeには中間値が含まれる。

**Limitation:** 入力数に一切効果がないというclaimではない。acceptability・値・順序を保持した純粋な用量効果推定でもない。

## Claim 9

逐次的に受理可能なpathがRecaptureに重要である。

**Status:** Supported by synthetic experiment

**Supporting experiment:** B/E/F

**Supporting artifact / selector:**

- [bridge_summary.csv](../../experiments/rssi_admissible_bridge/results/bridge_summary.csv)：complete/broken bridge、redundant deletion、order_alternating（support）
- [PROTOCOL.md](../../experiments/rssi_admissible_bridge/PROTOCOL.md)：Analytical candidates before simulation（support）

**Counterexample:** 『静的pathさえあればよい』はascendingが反例。『拒絶が一回でもあれば不可』はalternatingが反例。

**Scope:** 実際の提示順序に沿う状態遷移。全受理列の隣接gate条件と終点条件には解析的必要十分性がある。

**Limitation:** 局所的に受理可能なfree random prefixが必ず指定targetに届くわけではない。

**Additional evidence:** 条件を明示したscalar更新則ではAnalytically supportedの部分もある。

## Claim 10

実数scalar gateでは最短到達長に L_min >= ceil(|b0-b*|/τ) が成立する。

**Status:** Analytically supported

**Supporting experiment:** F解析

**Supporting artifact / selector:**

- [PROTOCOL.md](../../experiments/rssi_admissible_bridge/PROTOCOL.md)：Analytical candidates: triangle inequality / free intermediate values（support）
- [EXPERIMENT_REPORT.md](../../experiments/rssi_admissible_bridge/EXPERIMENT_REPORT.md)：Minimum Bridgeの実数とbinary64の分離（support）

**Counterexample:** 下限への反例はない。有限alphabetや固定順序では等号達成が失われ得る。

**Scope:** τ>0、実数演算。始点とtarget間の入力を自由に選べる区間なら下限を等分経路で達成できる。

**Limitation:** binary64の端点判定、離散graph、実AIへの無条件移植はしない。

## Claim 11

現在のbinary64実装でb=1から厳密な0への最短長は21である。

**Status:** Implementation-dependent

**Supporting experiment:** F解析＋simulation witness

**Supporting artifact / selector:**

- [float_frontier.csv](../../experiments/rssi_admissible_bridge/results/float_frontier.csv)：step20の最小残差>0、step21=0（support）
- [analysis.json](../../experiments/rssi_admissible_bridge/results/analysis.json)：float_L_min=21, frontier_step20（support）
- [portable validation history](../../results/frozen/VALIDATION_HISTORY.json)：exact real lower bound / binary64 endpoint certificateを含む元検証件数（support）

**Counterexample:** 一般化への対照：実数τ=1/20では20。離散i/40 graphでは28。

**Scope:** 現在のbinary64表現・丸め・tol=.05・状態域[0,1]・厳密target0。frontier単調性と端点証明書による最小性。

**Limitation:** 単なる5seedの最小観測値ではない。21を普遍的なRSSI定数やRelapse時刻と扱わない。

## Claim 12

静的graphが連結なら、任意の入力順序でもRecaptureする。

**Status:** Falsified / rejected hypothesis

**Supporting experiment:** E/F

**Supporting artifact / selector:**

- [bridge_summary.csv](../../experiments/rssi_admissible_bridge/results/bridge_summary.csv)：同一multisetのcontrol_E_gradual / order_ascending、unordered_graph_path_exists=True（counterexample）
- [order_divergence.csv](../../experiments/rssi_admissible_bridge/results/order_divergence.csv)：same_multiset=Trueの全比較（support）

**Counterexample:** 同じ静的値集合に1→0 pathがあっても、ascending/shuffledでは今回targetに届かない。

**Scope:** 静的存在量化と、固定時間順序の実行を区別する。

**Limitation:** 適切な順序なら到達可能というgraphの意味は棄却されない。

## Claim 13

Fの固定noise条件ではη=.006で2/5、η=.012で0/5がtargetへ到達した。

**Status:** Supported by finite fixtures only

**Supporting experiment:** F

**Supporting artifact / selector:**

- [bridge_summary.csv](../../experiments/rssi_admissible_bridge/results/bridge_summary.csv)：family=noise, noise=.006/.012、target_reached（support）

**Counterexample:** η=.001/.004は5/5。全noiseで一様に不可能という命題ではない。

**Scope:** 25入力の単調bridge、5固定seed、内点noise、終点0固定。

**Limitation:** 到達確率の精密推定、普遍noise閾値、noiseによる追加必要path長は未支持。

## Claim 14

実LLMにも順序感度を独立に監査する価値があるかもしれない。

**Status:** Suggestive only

**Supporting experiment:** E/Fは検討動機のみ

**Supporting artifact / selector:**

- [EXPERIMENT_REPORT.md](../../experiments/rssi_recapture_dynamics/EXPERIMENT_REPORT.md)：order/path results and unsupported claims（scope boundary）

**Counterexample:** この系列には実LLMの反例も支持例もない。

**Scope:** 次工程の問いとしての示唆。検証済みの移植可能性ではない。

**Limitation:** 実LLMの出力変化をlatent belief更新・RSSI・同じgateの証拠と呼ばない。

## Claim 15

A〜Fは実LLM、RSI一般、人間のbelief、native Hoho再帰を実証した。

**Status:** Not supported

**Supporting experiment:** 該当する実験なし

**Supporting artifact / selector:**

- [summary.json](../../results/summary.json)：native_julia_executed=False; declared minimal model（scope boundary）
- [publication boundary](../../results/frozen/PUBLICATION_BOUNDARY.json)：native cross-check未完走・環境依存ログ除外（scope boundary）

**Counterexample:** 未測定のため反証ではなく未支持。

**Scope:** RSSIという名称と、実際のrecursive self-improvementの実証を分離。

**Limitation:** LLM/human/native validationを後から実施済みと扱わない。

## Claim 16

既知入力の受理agreement平均Cは、実数上、定義される場合1−tol以上である。

**Status:** Analytically supported

**Supporting experiment:** B/C定義; E/Fで保持

**Supporting artifact / selector:**

- [run_experiments.py](../../run_experiments.py)：offerとaccepted_agreement（support）
- [run_experiment.py](../../experiments/rssi_attractor_escape/run_experiment.py)：Recorderで受理されたnormal入力のみCを計算（support）

**Counterexample:** 受理ゼロではCは未定義。未知topicを含む無条件受理へ同じ下限を主張しない。

**Scope:** 既知scalar・実数gate・agreement=1−|x−b_before|の定義からの帰結。

**Limitation:** binary64丸め誤差を伴う。高Cが独立な真理指標だという結論にはならない。

## Claim 17

Reference integrityはadversarial code rewritingにも保証される。

**Status:** Not supported

**Supporting experiment:** その攻撃実験なし

**Supporting artifact / selector:**

- [reference.json](../../experiments/rssi_attractor_escape/reference.json)：固定domain/reference（scope boundary）
- [PROTOCOL.md](../../experiments/rssi_admissible_bridge/PROTOCOL.md)：trusted harness / reference domain negative checks（scope boundary）

**Counterexample:** policy API内にreference改変操作がないことは、環境全体の改変に対する証明ではない。

**Scope:** 固定R0、domain、hashを保持した信頼されたharness内。

**Limitation:** Ideal E8の別実験をRSSIへの攻撃耐性検証として加算しない。

## Claim 18

Sの境界.58/.59はRSSI一般のcritical constantである。

**Status:** Not supported

**Supporting experiment:** Dが支持するのは実装内の境界だけ

**Supporting artifact / selector:**

- [boundary_estimates.csv](../../experiments/rssi_attractor_escape_boundary/results/boundary_estimates.csv)：初回D=1での有限grid bracket (.58,.59]（scope boundary）
- [run_experiment.py](../../experiments/rssi_attractor_escape/run_experiment.py)：support=.6*S+.4*D_before >= .75（scope boundary）

**Counterexample:** Cでは同じS=1でも後続D=.225の時にrejectされる。

**Scope:** 初回D=1に限った実数support式なら閾値7/12。有限gridで.58/.59を挟む。

**Limitation:** 新しい普遍相転移の発見や数学的相転移の証明ではない。

## 照合方法

全supporting artifactの相対path・完全SHA-256・selectorは[元の機械可読台帳](../freeze/claim_evidence.json)に保存しています。公開artifactのpath・元bytesのSHA-256・CSV行数は[public manifest](../../results/frozen/MANIFEST.json)に保持します。出典の存在とhash一致は機械照合、scopeと命題の含意は文書レビューで確認し、意味の正しさまでhashで証明できるとは扱いません。

関連：[Synthesis](RSSI_A_F_SYNTHESIS.md)、[Mathematical core](RSSI_MATHEMATICAL_CORE.md)、[Limitations](RSSI_LIMITATIONS.md)。
