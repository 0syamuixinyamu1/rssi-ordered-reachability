# RSSI Next-step Decision

固定日：2026-09-18。これは次工程の判断文書です。Exp G、2D、高次元、LLM監査の実装や実行は行いません。A〜Fの評価metric、分類、tol、reference、gateは変更しません。

## 判断

**現時点ではOption 1、A〜Fをここで終了して成果を固定することを推奨します。**

核心は、指定scalar ruleの解析と保存済み対照例から既に狭く述べられます。strength/frequencyや入力割合の追加sweepを行っても、同じ機構を別条件で繰り返す可能性が高いためです。未解決のnative Julia runtime問題は明示して残し、synthetic claimの固定を延期する理由にはしません。

2Dには「1D固有の構成にどこまで依存するか」を調べる限定的な価値があります。実LLM監査には対象を現実の出力へ移す価値があります。いずれも現在の結果を強く言い換える根拠にはならず、別の事前設計と別の証拠が必要です。

## 三つの選択肢

| Option | 新しく分かること | 証明できないこと | 相対的実装コスト | 既存結果との重複 | Failure criterion |
| --- | --- | --- | --- | --- | --- |
| 1. 終了・固定 | 証拠とclaimの射程、反証、数値依存性が確定する | 高次元・実LLM・人間への適用 | 低。文書・照合のみ | 新しい実験知見は足さない | 出典不明・raw/report不一致・過大claimが残ればfreeze未完了として当該記述を修正する。新実験で埋め合わせない |
| 2. 最小2Dを1本 | 事前固定した2D版でもbridge/order/path/exposure対照の少なくとも一つが残るか | 任意次元、任意gate、実AIのrecapture、AI alignment一般 | 中。状態・gateの意味と非退化fixture、独立validationが必要 | 1Dを一つの軸へ埋め込んだだけなら大きく重複 | 1D回帰または2Dの正当性確認が不成立なら結果評価へ進まない。正当な固定2D設計で全対象効果が消失すればnegativeとして終了 |
| 3. 実LLMのsequence-sensitive behavioral audit | 順序を制御した入力履歴で、観測できる応答が変わるか | latent beliefの真値、scalar gate、RSSI/RSI、意図的欺瞞の実証 | 高。実出力取得、独立reference、履歴・長さの交絡管理、ラベル監査が必要 | 問いは関連するが対象・measurementは別 | 事前の独立評価基準で順序差を検出できなければnegative。長さや履歴漏れ等を切り分けられなければinconclusive。後からendpointや判定を変えない |

コストはこのproject内の相対比較で、所要日数・価格の見積りではありません。失敗条件は「Persistent Escapeが起こらなかった」ではなく、事前の問い・測定条件に対する判定です。RelapseもPersistentも同等の観測対象として扱います。

## Option 2へ将来進む場合の限定範囲と停止条件

検討するstateは最小の $\mathbf b=(b_1,b_2)$ のみとします。実際のnorm・gate・値域・target・reference・有限horizon・比較順序・評価方法は**実行前に別protocolで固定**する必要があります。本書はそれらを後付けで実装・確定するものではありません。

対象は1Dの次の四つに対応する対照です。

1. Admissible bridge：中間の局所受理遷移を通る到達。
2. Order effect：同一multisetの順序による結果差。
3. Path dependence：同じ最終入力を通る異なる経路の結果差。
4. Exposure vs reachability：提示量と受理経路の存在・実行可能性の分離。

最低一つが、両成分が関与する非退化な2D fixtureでも再現するかを問います。片方の座標を定数にした1Dの埋め込みだけなら、既存結果の再表現として報告し、新しい高次元支持に数えません。

事前固定した妥当な2D設計で四つ全てが消失した場合は、

> Current mechanism is strongly scalar-specific within this tested extension.

というnegative resultとして終了します。別のnorm、gate、fixtureを次々に選び直して現象を復活させません。この停止判断は検証した2D拡張内の射程です。「全ての可能な2D系で効果が存在しない」と証明したことにはなりません。

少なくとも一つが残っても、結論は「その固定2D条件でも対応する構造が観測された」までです。高次元一般への外挿や実AIへの適用を自動承認しません。数値不良・仕様未確定・交絡が原因なら、効果消失のnegative resultと区別してinconclusiveで止めます。

## Option 3との境界

LLM監査へ接続するなら、比較対象は観測可能なresponseと独立referenceです。今回の内部belief bやCを、そのままLLMの内部state・真のcoherenceとみなしません。履歴効果が出ても、attention/context処理、指示追従、表現上の差など他の説明と区別する必要があります。

syntheticのS=.59、tol=.05、21stepをLLM実験へ移植する根拠はありません。事前に独立したbehavioral auditとして設計する必要があり、A〜Fはその設計動機に留まります。この文書ではモデル選定、API呼出、出力取得、評価metricの追加をしていません。

## 今回の完了条件

A〜Fの内容を増やさず、六つの統合文書、claimと原artifactの対応、主要数値の照合、既存A〜F/Idealの非変更確認を完了することです。2Dと実LLM監査は「今回の未完了作業」には含めません。

関連：[Synthesis](RSSI_A_F_SYNTHESIS.md)、[Claim ledger](RSSI_CLAIM_LEDGER.md)、[Limitations](RSSI_LIMITATIONS.md)。
