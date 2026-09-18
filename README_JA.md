# RSSI Ordered Reachability

**bounded local-update ruleにおけるpath-dependent state transitionを調べたsynthetic研究repositoryです。**

RSSIは当初 *Recursive Solipsistic Self-Improvement* の略として使ったconceptual labelです。A〜Fは、実際の自己改良AI、frontier LLM、人間、HohoEngine native learning loopを直接実験したものではありません。

[English README](README.md) · [実験map](docs/EXPERIMENT_MAP.md) · [A–F統合](docs/A_F_SYNTHESIS.md) · [Claim Ledger](docs/CLAIM_LEDGER.md) · [再現手順](docs/REPRODUCIBILITY.md) · [公開監査](docs/PUBLICATION_AUDIT.md)

## 中心規則

現在stateを (b_t)、提示入力を (x_t)、許容幅をτとすると、通常更新は

$$
b_{t+1}=\begin{cases}
x_t,& |x_t-b_t|\le\tau,\\
b_t,& |x_t-b_t|>\tau
\end{cases}
$$

です。

tested scalar synthetic setupでは、遠いtargetを直接提示しても拒絶され続ける一方、局所的にadmissibleな中間stateを適切な順序で連結するとtargetへ到達できます。また、同じmultisetや同じinput tokenでも、それ以前のtrajectoryによって受理／拒絶と最終stateが変わる場合があります。

固定する最も狭い中心claimは次です。

> 検証したscalar synthetic setupでは、bounded local-update gateの下で、受理可能な中間遷移を通じて順序依存のrecaptureが起こり得ます。見かけの訂正と受理入力に対するcoherenceは、独立referenceとの一致を保証しません。

これはsynthetic dynamical-systemの結果です。Law of Attractionや超自然的な「引き寄せ」の実証ではありません。

## Exp Fの代表例

外部revision直後のstate 1から、次の二条件を比較しました。

| 条件 | post入力 | 受理 | 初期state | 最終state |
| --- | ---: | ---: | ---: | ---: |
| 直接target `0`を反復 | 120 | 0 | 1 | 1 |
| 最短Binary64 admissible bridge | 21 | 21 | 1 | 0 |

したがって、現在実装では

$$
120\times\text{direct target}\not\Rightarrow\text{state transition},
\qquad
21\text{-step admissible bridge}\Rightarrow1\rightarrow0
$$

でした。ただし21は普遍定数ではありません。実数scalar modelで任意の中間点を選べるなら

$$
L_{\min}=\left\lceil\frac{d}{\tau}\right\rceil
$$

であり、(d=1, \tau=.05) なら20です。21は保存済みBinary64実装で厳密に0へ到達する場合の結果です。詳細は[Mathematical Core](docs/MATHEMATICAL_CORE.md)を参照してください。

## A→Fの絞り込み

$$
\text{apparent improvement}
\rightarrow\text{reference divergence}
\rightarrow\text{escape}
\rightarrow\text{recapture}
\rightarrow\text{path dependence}
\rightarrow\text{reachability}
$$

これはA〜Fにおける研究上の問題設定の絞り込みであり、real AI一般について実証された因果連鎖ではありません。

| Exp | 問い | 固定された結果 |
| --- | --- | --- |
| A | apparent correctionとinternal revision | 正しい外部出力は内部state更新を保証しない |
| B | internal coherenceと独立reference距離 | Cの上昇とDの悪化が両立するfixtureがある |
| C | 独立reference注入後の状態 | persistent / relapse / rejection / complianceを観測 |
| D | strength / frequency境界 | strengthは初回revision gateを決めても持続性を保証しない |
| E | post-input sequence | 同一multisetや同一終値でも順序・pathで分岐する条件がある |
| F | admissible bridge geometry | 曝露量や静的連結性だけでなく、順序どおり利用できるpathが重要 |

## 公開snapshotの確認

Python 3.10以上の標準libraryで検証できます。frozen実行環境はPython 3.12.14でした。

```bash
python scripts/validate_snapshot.py
```

これはartifact hash、行数、代表数値、link、LICENSE/CITATION、秘密情報・local pathの混入を確認し、新しい実験は実行しません。

既存A〜Fのrunnerを一時directoryで再実行し、frozen CSVとbyte単位で比較する場合は次を使用します。

```bash
python scripts/reproduce.py --series all
```

個別指定は `--series a,b,c` や `--series f` です。network、API key、LLM callは不要です。詳細は[REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md)にあります。

## Claim Freeze

ClaimはAnalytically supported、Supported by synthetic experiment、Supported by finite fixtures only、Implementation-dependent、Suggestive only、Not supported、Falsified / rejected hypothesisに分けています。

real LLM、人間のbelief、native HohoEngine RSSI recursion、recursive self-improvement、AI alignment、高次元一般、普遍的相転移／hysteresis、adversarial self-rewriting resistanceはSupportedへ昇格させていません。

## 公開境界

Exp Aは固定Hoho sourceの一部をPythonでreplayします。Exp Bは明示したscalar gateです。C〜FはPythonのindependent-reference harnessを再利用します。HohoEngine nativeにB〜Fの通常再帰が存在するとは主張しません。Ideal E1〜E8の実装・fixture・testはこの公開repositoryに含めていません。

大容量CSVは内容を変えず、1 MB超だけdeterministic gzipで保存しました。展開前後のSHA-256は[frozen manifest](results/frozen/MANIFEST.json)で確認できます。

codeと文書は[MIT License](LICENSE)です。引用情報は[CITATION.cff](CITATION.cff)にあります。
