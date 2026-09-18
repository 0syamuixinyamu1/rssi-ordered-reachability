# RSSI Mathematical Core — claim freeze

固定日：2026-09-18。既存Exp Fの解析と保存済み証明書を整理する文書です。新しい実験・到達判定・許容誤差は追加していません。

## 1. 対象の更新則

既知のscalar状態と通常入力について、説明上の実数モデルは

$$
b_{t+1}=\begin{cases}
x_t,& |x_t-b_t|\le\tau,\\
b_t,& |x_t-b_t|>\tau.
\end{cases}
$$

です。Pythonの実装では、この差・比較・入力生成をbinary64で実行します。外部注入用のevidence handlerとは別の規則です。HohoEngine本体のnative learning loopを表したものではありません。

Fでは外部注入後の始点を $b_0=1$、旧anchorを $b^*=0$、referenceを $R_0=1$ としています。したがって旧anchorへの到達では $D=|b-R_0|$ が0から1へ増えます。「target到達」は正しさの改善を意味しません。

出典：[F protocol](../../experiments/rssi_admissible_bridge/PROTOCOL.md)、[B offerを定義したrunner](../../run_experiments.py)、[F解析コード](../../experiments/rssi_admissible_bridge/analyze_reachability.py)。

## 2. Analytical result：実数上の下限

受理なら移動幅は高々 τ、拒絶なら移動幅は0です。三角不等式から、L回の通常入力後について

$$
|b_0-b_L|
\le\sum_{k=0}^{L-1}|b_{k+1}-b_k|
\le L\tau.
$$

よって τ>0、距離 $d=|b_0-b^*|$ の厳密なtargetへ到達するには

$$
L\ge\left\lceil\frac{d}{\tau}\right\rceil
$$

が必要です。途中の拒絶、折り返し、大きな提示値はこの下限を短縮しません。ここでLは入力提示回数です。有効な状態移動回数に対しても同じ下限が成立します。

### 達成可能性の条件

始点とtargetを含む実数区間内の中間入力を自由に選べる場合、$n=\lceil d/\tau\rceil$ として

$$
x_k=b_0+\frac{k}{n}(b^*-b_0),\qquad k=1,\ldots,n
$$

を順に提示すれば各幅は $d/n\le\tau$、最後は厳密なtargetです。したがってこの条件では下限が達成され、$L_{\min}=\lceil d/\tau\rceil$ です。$d=0$ なら0回、τ=0かつd>0なら到達不能です。

Fの実数候補 τ=1/20、d=1では最短20です。有限の入力alphabet、指定済み順序、追加の状態制約がある場合、上の自由選択による等号は保証されません。下限だけから既存fixtureの到達性を結論しません。

## 3. 順序付きpathと静的graph

全入力を受理する指定列 $x_1,\ldots,x_L$ がtargetへ終端する必要十分条件は、$x_0=b_0$ として全ての隣接差がgate内で、$x_L=b^*$ となることです。これは同じ更新則を逐次代入することで成立します。

拒絶を許す一般の列では、実際に受理された部分列と、その都度のbeliefを使う必要があります。入力集合内にpathが存在しても、提示順序でそのpathが利用されるとは限りません。また「列から都合のよい部分列を抜き出せばpathになる」だけでも十分ではありません。途中の別入力が受理されると、次の入力の受理条件が変わるためです。

静的graphの連結性は、辺を自由に選んで進める場合のpath存在性です。固定された時間順序での到達保証ではありません。E/Fの同一multiset比較は、同じ静的頂点集合でも実行順序で到達が分かれる反例です。

「一度の拒絶で永久に到達不能」も成立しません。Fのhigh/low alternatingではseed7で37入力を拒絶しながらstep76でtargetへ到達しています。反対に、単調下降列にgateを超えるgapがあり、それ以降の入力が最後に受理したbeliefからさらに遠ざかるだけなら、その残りの列では到達できません。

出典：[order_divergence.csv](../../experiments/rssi_admissible_bridge/results/order_divergence.csv)、[bridge_summary.csv](../../experiments/rssi_admissible_bridge/results/bridge_summary.csv)、[F report E/G](../../experiments/rssi_admissible_bridge/EXPERIMENT_REPORT.md)。

## 4. Implementation result：binary64の厳密target最短21

現在のtolは `float(.05)`、hexでは `0x1.999999999999ap-5`、正確な有理数では

$$
\frac{3602879701896397}{72057594037927936}
$$

です。通常gateにはepsilonを足していません。入力値と減算もbinary64なので、実数上の幅.05を指定したつもりでも、実際の辺が受理可能とは限りません。

保存済みF解析は、非負binary64状態bについて、gateを通過する最小の表現可能な次状態を $f(b)$ と定め、表現可能値の順序に沿って探索しています。各 $f(b)$ の受理と、その直下の隣接floatの拒絶が証明書に保存されています。

正しく丸められた減算の単調性からfは非減少です。任意の入力・拒絶・上昇を含む1回の更新後の状態はf(b)以上なので、帰納的に $f^{(k)}(1)$ はk回後に到達できる最小状態です。これは「単調経路だけ試した」という最小性判断ではありません。現在の状態域、gate、丸め規則を前提とする実装上の下限です。

保存されたfrontierでは

$$
f^{(20)}(1)=\frac{211}{288230376151711744}
=7.320533068622126\times10^{-16}>0,
\quad f^{(21)}(1)=0.
$$

従って20回以下では厳密な0に届かず、21回のwitnessで届きます。F独立validatorはFractionによる丸めoracleと隣接floatを照合した記録を残しています。本統合ではそのログ・CSV・ハッシュを照合し、実験やvalidatorは再実行していません。

出典：[analysis.json](../../experiments/rssi_admissible_bridge/results/analysis.json)、[float_frontier.csv](../../experiments/rssi_admissible_bridge/results/float_frontier.csv)、[minimum_paths.csv](../../experiments/rssi_admissible_bridge/results/minimum_paths.csv)、[portable validation history](../../results/frozen/VALIDATION_HISTORY.json)。

**21は一般理論の定数ではありません。** 実数の20、現在の全binary64候補内の21、有限gridの最短長、Relapse近傍へ入る時刻を区別します。

## 5. Numerical caveats

`.95` と `.05` の表示だけでは辺の可否は分かりません。現在の演算で `abs(.95-1)` は `0.050000000000000044` となり、tolを超えます。一方、frontierの最初の入力 `.9500000000000001` は受理されます。

nominal δ=.049と.0499の保存列は21入力全て受理されました。δ=.05と.051の列は最初から拒絶されています。δを `.05` の直下floatにしても、`1-delta` が `.95` に丸められるため最初の辺は拒絶されます。この条件では末尾値も厳密な0ではありません。結果を良くするため0を追記したりgateへepsilonを入れたりしていません。

離散graphでは、同じtol=.05でも頂点集合によって結果が変わります。

| 頂点集合 | node数 | 成分数 | 最短長 | 最短経路数 |
| --- | ---: | ---: | ---: | ---: |
| i/20 | 21 | 9 | 到達不能 | 0 |
| i/40 | 41 | 1 | 28 | 576 |
| i/80 | 81 | 1 | 23 | 128 |
| i/40＋frontier | 61 | 1 | 21 | 14 |

この表の値は[reachability_graph.csv](../../experiments/rssi_admissible_bridge/results/reachability_graph.csv)のtol=.05行です。必要な中間floatが頂点集合に含まれるかで結果が変わります。`i/40` と `1-k*.025` も同じfloat集合とみなせません。Fのtol=.049/.051比較は分析graphに限られ、主実験のtol変更ではありません。経路数は「最短経路数」であり、全walk数ではありません。

Relapseは旧anchorの.05近傍で5連続stepという既存分類です。厳密target `b==0` とは違い、frontierではRelapse onset19、確認23、厳密到達21です。Fの有限path終了後の空入力holdも観測clockには数えますが、新しい入力eventは発生しません。

## 6. Experimental resultとの区別

| 証拠の種類 | 固定する結論 | そこからは導かないこと |
| --- | --- | --- |
| 実数上の解析 | 指定scalar則の下限と自由入力での達成可能性 | finite fixture・binary64・LLMへの自動適用 |
| 実装解析＋保存証明書 | 現在のbinary64 gateの厳密最短21 | 任意tol、他精度、近傍targetでも21 |
| 有限synthetic実験 | 順序・gap・noise・exposureの保存済み対照 | 全ての順序・分布・将来入力で同じ割合 |

受理された既知入力のagreementを $1-|x-b_{before}|$ と定めれば、実数上は各受理値が $1-\tau$ 以上です。その平均Cも同じ下限を持ちます。binary64では丸め誤差を伴います。高CとD増大の併存はこの定義と両立し、Cは真理判定ではありません。受理入力が空ならCはNAです。

関連：[Claim ledger](RSSI_CLAIM_LEDGER.md)、[Limitations](RSSI_LIMITATIONS.md)。
