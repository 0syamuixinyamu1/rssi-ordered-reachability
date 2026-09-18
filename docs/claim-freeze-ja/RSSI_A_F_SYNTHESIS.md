# RSSI A–F Integrated Synthesis / Claim Freeze

固定日：2026-09-18。対象は既存A〜Fの成果物です。新規実験、既存分類・gate・tol・referenceの変更、結果再解釈のための再実験は行っていません。

> RSSI is used here as a conceptual label for a synthetic recursive evaluation/update setting, not as evidence of deployed recursive self-improving AI.

## 1. Executive Summary

**固定する中心文：**

> In the tested scalar synthetic setup, a bounded local-update gate permits order-dependent recapture through admissible intermediate transitions; apparent correction and accepted-input coherence do not guarantee agreement with the independent reference.

検証したscalar synthetic系では、局所gateを通過する中間遷移の順序によってrecaptureが分かれ、見かけの訂正や受理入力coherenceだけでは独立referenceとの一致を保証できません。

支持範囲はこの更新則・実装・fixture群です。Aの出力／内部state分離、BのC／D分離、C〜Fの入力順序付き到達性を同じ証拠種に混ぜず統合しました。次工程は、現時点で系列を終了しclaimを固定するOption 1を推奨します。2Dや実LLM監査は別の問いとして条件付きで検討し、今回は実装しません。

## 2. Why the series started

出発点は「訂正したように見えること」と「内部stateが訂正されたこと」の区別です。AはHoho由来のExternalCompliance/ImaginaryMode関連sourceのPython replayでこの分離を測定しました。Bは通常観測を自身のbeliefとの近さで受理する最小synthetic ruleを明示し、内部agreementと外部referenceへの距離を別に測りました。

以後の問いは、「一度外から正しい値へ更新しても、その後の通常入力で元へ戻るか」です。RSSIという名称はこのconceptual settingのproject labelであり、自己書き換え・能力向上・実AIの独我論化が起きたという観測記述ではありません。

## 3. Experimental progression A→F

| Series | 問いの進展 | 保存結果から言えること |
| --- | --- | --- |
| A | apparent correctionとinternal revision | outputだけ正しくできるhandlerがあり、内部更新は別に測る必要がある |
| B | 内部coherenceと独立reference | C上昇とD増大が同時に起こる対照例がある |
| C | 外部注入後のescape | persistent / relapse / rejection / complianceが配送・更新条件と後続列で分かれる |
| D | strength/frequency境界 | 初回受理gateの通過はpersistentを保証しない |
| E | post-inputの構造 | 同一multisetでも順序差、同一終値でも経路差が生じる |
| F | ordered admissible reachability | 実際に使える中間遷移と順序が到達を左右し、単純な提示量では説明し切れない |

apparent improvement → reference divergence → escape → recapture → path dependence → reachabilityという**研究上の絞り込み**です。実世界AI一般の因果連鎖を同定したものではありません。全raw/protocol/figures/検証ログへの入口は[Experiment map](RSSI_EXPERIMENT_MAP.md)にあります。

| Series | 保存された規模 | state行 | input event行 |
| --- | --- | ---: | ---: |
| A | 27,104 factorial trial、pressure grid 625行 | 非時系列trial | 非時系列trial |
| B | 120 trajectory、別途seed感度720 run | 9,600 | 13,440 |
| C | 54 run | 10,167 | 20,130 |
| D | 920 run | 176,710 | 346,450 |
| E | 330 run | 44,435 | 48,880 |
| F | 170 run | 22,610 | 11,940 |

## 4. Main findings

### A：同じ正答出力でも内部stateは違う

初期誤り・正しいhypothesis・高pressure条件では、external_onlyは726/726で正しい出力を返し、内部正答は0/726でした。imaginary_onlyも同じ出力／内部の分離を示します。evidence_revisionはこの部分集合で114/726が内部正答となりました。正しいresponseはharnessの供給値であり、モデルによる自律的発見ではありません。

出典：[a_summary.csv](../../results/a_summary.csv)、[a_trials.csv.gz](../../results/a_trials.csv.gz)、[A/B report](../../experiments/exp_a/RESULTS_A_B_JA.md)。

### B：C上昇とD増大は両立する

drift_away、gated、tol=.05では、保存step1→80で

- C：0.9619349672 → 0.9999858876
- D：0.6380650328 → 0.9998658149

となり、80回のreference入力は全て拒絶されています。frozen fixtureではC=1かつD=1のままです。一方、bridgeは小刻みな通常更新でreferenceへ届き、oscillationは単純な常時収束を否定します。「拒絶すれば必ずDが増える」「このgateなら一切beliefが動かない」も採用しません。

出典：[b_trajectories.csv](../../results/b_trajectories.csv)、[b_endpoints.csv](../../results/b_endpoints.csv)。

### C/D：配送・更新承認・持続性は別である

Cの54runはPersistent候補12、Relapse12、Rejection18、ExternalCompliance6、無注入control6です。強制配送は通常gateの入口を迂回しますが、evidence handlerの承認まで保証しません。Cのseed7、descending_bridge、S=1の反復注入step10では、b=.775の時にsupport=.69となり外部反証を拒絶しています。

Dの初回D=1ではsupport=.6S+.4Dを.75と比較するため、実数式の受理閾値は7/12です。有限gridはS≤.58でreject、S≥.59でrevisionを観測しました。revision後はstationaryでPersistent、descending_bridgeでRelapseです。S/FだけでRejection→Relapse→Persistentと順に並ぶ単一の3相図ではありません。

D primary 900runはRejection480、Persistent210、Relapse210です。bridgeのS=1ではF=1のT_relapse=39に対し、検証したF>1は79となりました。F=2から16への増加でそれ以上延びず、最終分類も変わりません。介入が有限期間で終了するこのschedule内の結果であり、永久介入一般の不可能性ではありません。

出典：[C summary](../../experiments/rssi_attractor_escape/results/summary.csv)、[C event log](../../experiments/rssi_attractor_escape/results/event_log.csv.gz)、[D phase grid](../../experiments/rssi_attractor_escape_boundary/results/phase_grid.csv)、[D boundary](../../experiments/rssi_attractor_escape_boundary/results/boundary_estimates.csv)、[D relapse](../../experiments/rssi_attractor_escape_boundary/results/relapse_times.csv)。

### E：qだけ・最終入力だけでは決まらない

S=1・単発注入を固定した330runはPersistent300、Relapse30でした。同一bridge multisetでdescendingは5/5 Relapse、ascending/shuffledは各5/5 Persistentでした。しかし60R/60Oだけのmultiset比較では分類差はありません。order effectは存在命題であり、全てのmultisetで起こるわけではありません。

同じ最終入力0でも、v=1のfast pathは最終b=1、v=.025のslow pathは最終b=0でした。両者とも同じ現在bと次入力なら同じ規則を使います。「履歴依存」は入力履歴が現在beliefを変える意味で、隠れた新しい記憶機構の発見ではありません。

qは旧anchor方向へ提示した入力割合で、受理割合ではありません。v=.01ではqの観測境界が(.75,.9]、v=.025/.04/.049では(.9,1]です。v=.051/1では今回のq範囲にRelapseがありません。S同様、vが大きいほど単調にRecaptureしやすいという結果ではありません。

出典：[E order effects](../../experiments/rssi_recapture_dynamics/results/order_effects.csv)、[path dependence](../../experiments/rssi_recapture_dynamics/results/path_dependence.csv)、[thresholds](../../experiments/rssi_recapture_dynamics/results/recapture_thresholds.csv)。

### F：提示量と順序付きreachabilityを分離する

| 保存条件 | post入力数 | 受理数 | 最終b | 最終D | 各5seedの分類 |
| --- | ---: | ---: | ---: | ---: | --- |
| 0のみを反復 | 120 | 0 | 1 | 0 | Persistent |
| 最短binary64 bridge | 21 | 21 | 0 | 1 | Relapse |
| 入力なし | 0 | 0 | 1 | 0 | Persistent |

同じ.95の入力tokenでも、descendingのstep2では直前b=.975なので受理され、ascendingのstep119では直前b=1なので拒絶されます。seed7で下降／上昇trajectoryの最初の分岐はstep1です。全30組に同一tokenの受理差が2,189件保存され、先行beliefが次の入力のacceptabilityを変える機構を追跡できます。

Fの170runはPersistent83、Relapse82、mixed5です。単一点の削除でもgapが.08になるbridgeでは遮断され、gap.04に留まる冗長点削除では到達しました。late breakのb≈.08はmixedであり、無理に2分類へまとめていません。noiseはη=.006で2/5、.012で0/5が到達した有限fixture結果です。

出典：[bridge summary](../../experiments/rssi_admissible_bridge/results/bridge_summary.csv)、[order divergence](../../experiments/rssi_admissible_bridge/results/order_divergence.csv)、[same-token evidence](../../experiments/rssi_admissible_bridge/results/order_acceptability.csv)。

## 5. Falsified / Weakened Hypotheses

| 元の強い仮説 | 反例・弱化した段階 | 固定する狭い結論 |
| --- | --- | --- |
| A. 強く何度も注入すればPersistentになる | C/D：S=1・F=16でもbridgeでRelapse | 初回revisionや再発遅延は持続性と別 |
| B. strength/frequencyだけで3相を説明できる | D：同一S/Fでもpost-input regimeで異なる | 観測gate境界はregime依存の最終状態を決め切らない |
| C. qだけでRecaptureを説明できる | E/F：同一multisetの順序差 | 値の比率に加えて順序が必要になる条件がある |
| D. 最終入力が同じなら最終stateも同じ | E：fast/slow、終値0 | 直前までの更新履歴を無視できない |
| E. 大量の旧anchor exposureほどRecaptureする | F：120 zeros対21 bridge | 単純な提示量による十分条件・単調保証を棄却 |
| F. 静的graphが連結なら順序不問で到達 | F：同じ集合のascendingが未到達 | path存在とその順序での実行可能性は異なる |

これらは普遍形・十分条件形への反例です。frequencyやqがどの条件でも無関係、あるいは反対の単調法則が成立するという主張には変更しません。追加で「一回の拒絶で永久遮断」「高Cは常に無情報」も採用しません。

## 6. Mathematical core

実数scalar gateでは、L更新について

$$
|b_0-b_L|\le\sum_{k=0}^{L-1}|b_{k+1}-b_k|\le L\tau.
$$

したがってtarget距離dに対しL≥ceil(d/τ)です。始点とtarget間の実数入力を自由に選べれば、等分経路が下限を達成します。τ=1/20、距離1なら20です。

現在のbinary64 gateでは、保存frontierの20回後の最小残差は7.320533068622126e-16で、厳密0への最短は21です。この実装上の解析・証明書と、実数定理と、有限fixtureでの到達観測を別の証拠として扱います。詳しい仮定・証明は[Mathematical core](RSSI_MATHEMATICAL_CORE.md)に固定しました。

## 7. Synthetic vs native boundary

| 層 | 実在するもの・再利用したもの | A〜Fで直接実験した範囲 |
| --- | --- | --- |
| HohoEngine source | ExternalCompliance、pressure、ImaginaryMode、evidence collapseなど | Aは該当sourceのPython replay。Julia実行成功を主張しない |
| HohoのCoreCommitment / constitutional_check | inspected sourceに存在する制約・検査 | 本系列のscalar真理判定や通常再帰へは接続していない |
| Python synthetic rule | Bのknown-topic tol gateとaccepted input update | B〜Fの通常state dynamics。元のadmits_sectionをnativeに発見したとは言わない |
| independent reference harness | truthラベル、固定R0/domain、D、注入・event log・分類 | C〜FがR0を通常self-selectionの外から配送・評価 |
| Ideal / provenance layer | E5 temporal、E6 closed-loop policy history、E8 reference integrity | 独立した実験層のsource・検証記録を参照。RSSI通常再帰のnative実証ではない |

Aが参照したsource commitは `a51c99e26c3534b68bffbc9c81697886f6097feb` です。後のIdeal原本checkoutのHEADとは区別します。現物sourceではpressure重みはanger .40、rejection .25、authority .15、social_cost .20です。pressureは社会的外圧であり、真理の証拠強度ではありません。

[source metadata](../../results/summary.json)、[ImaginaryMode snapshot](../../sources/hoho/src/ImaginaryMode.jl)、[Core snapshot](../../sources/hoho/src/HohoConsciousnessCore.jl)、[synthetic/native/Ideal boundary](../BOUNDARY_AND_PROVENANCE.md)。

native cross-checkは保存記録でruntime failureが残り、成功したnative validationではありません。native Juliaに同じ通常再帰がある、HohoEngineがこのrecaptureを実証した、と記載しません。

## 8. Reference integrity

state、選択された通常観測、独立reference、評価metricを分離しています。通常gateが反証を拒絶しても、Dは固定referenceから測り続けます。C〜FではR0=1、旧anchor=0、domain固定です。Referenceのhashは `94a48d42105e9fa6fa421c003a68d1004a6a2a528005db2ac3ec1f4ebac71b34` で、保存event/stateのhash欄を照合しました。post-input generatorが変わってもR0は変わりません。

AではR0は0/1、Bはfixtureにより1または.5です。固定とは「trial内で変更しない」ことであり、A〜F全てが常にR0=1だったという意味ではありません。Bのreference_onlyはtruthラベルを使うoracle controlです。

policy APIにreference selection/deletion/rewriting/observation narrowingはなく、C〜Fのreference corruption/avoidanceはnot_availableです。これはtrusted harness内の独立性です。悪意あるコード書換えへの防御や、Ideal E8の別操作のRSSI移植は実証していません。

## 9. Numerical caveats

nominal .05幅の1→.95でも、actual float edgeは0.050000000000000044となりtolを超えます。入力生成式・丸め・端点の厳密比較を含めて結果が決まります。.05の直下floatにしただけでbridgeが通るとは限りません。

全binary64での厳密最短21と、i/20 graphの到達不能、i/40の28、i/80の23は矛盾ではありません。許す中間頂点が異なります。graphの連結性と提示順序も区別します。厳密target b==0と、旧anchor近傍に5step留まるRelapse分類も別です。

## 10. Claim ledger summary

18 claimを[Integrated Claim Ledger](RSSI_CLAIM_LEDGER.md)で、status・supporting experiment/artifact・counterexample・scope・limitationに対応付けました。

| 証拠の種類 | 代表claim |
| --- | --- |
| Analytically supported | 実数下限と自由中間入力での達成、受理agreementの下限 |
| Supported by synthetic experiment | apparent/internalの分離、C/Dの分離、順序差 |
| Supported by finite fixtures only | noiseでの2/5・0/5という観測割合 |
| Implementation-dependent | 現在のbinary64最短21 |
| Suggestive only | 実LLMの順序感度を別途監査する検討動機 |
| Not supported | 実LLM/RSI/人間/高次元への一般化、adversarial rewriting耐性 |
| Falsified / rejected hypothesis | 強反証必ず更新、反復必ずpersistent、q/終値/量/静的連結性だけの保証 |

## 11. Limitations

scalar 1D、C〜F主実験のfixed tol、trial内fixed R0、C〜Fのfixed old anchor、finite horizon、synthetic rule、limited seeds、決定論的fixture、binary64依存、graph離散化依存が制約です。real LLM、人間、native Julia RSSI recursion、adversarial code rewritingは検証していません。reference integrityはtrusted harness内に限られます。[完全なLimitations](RSSI_LIMITATIONS.md)に各射程と禁止する一般化をまとめています。

coherenceについては「高Cが安全を保証しない」が支持結論です。「Cは常に予測力ゼロ」ではありません。Dの一部early-C診断は分類を識別し、Eの既存early alarmも真陽性・偽陽性・見逃しを持ちます。これらを隠してcoherence無意味説へ単純化しません。

## 12. What this does NOT show

- 実際のLLMが同じscalar gateで動き、RSSI・recapture・相転移を起こすこと。
- 実際のrecursive self-improvement、能力向上、自己書き換え、独我論化の実証。
- 人間の信念形成、心理状態、社会現象の説明。
- HohoEngine nativeに同じ通常再帰が実装され、Julia実行でrecaptureを検証したこと。
- AI alignmentの一般解、数学的相転移・ヒステリシス、高次元一般のreachability geometry。
- Persistent Escapeが永久に維持されること、21や.58/.59が一般理論の定数であること。

## 13. Next-step decision / validation

**推奨：Option 1、ここで系列を終了し、この証拠範囲を固定します。** 核心は現在の更新則と保存counterexampleで述べられ、新しいsweepを加えなくても成立します。2Dにはscalar固有性を限定的に調べる価値がありますが、1Dを軸へ埋め込んだだけなら重複です。実LLM監査は別対象の新しい実証が必要です。[Next-step decision](RSSI_NEXT_STEP_DECISION.md)で3案の情報利得・限界・コスト・停止条件を比較し、実装はしていません。

監査はraw由来の規模表、claim対応、report記述、source/CSV hashを照合し、既存A〜Fの145ファイルとIdeal原本の保全を確認する作業です。既存5 manifestの照合とCSV digest参照159件の一致は[original source audit](../freeze/original_source_audit.json)に、公開snapshotのartifact identityは[public manifest](../../results/frozen/MANIFEST.json)に保存しました。保存validationのpassを今回のテスト再実行として数えていません。

今回追加した6文書以外の補助記録は、数値出典、claim/hash対応、原本保全と文書検証のためのものです。A〜F report/raw、Hoho本体、Ideal原本への変更はありません。
