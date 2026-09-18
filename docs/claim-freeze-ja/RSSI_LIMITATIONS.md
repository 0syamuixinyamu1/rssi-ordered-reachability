# RSSI A–F Integrated Limitations

固定日：2026-09-18。RSSIはconceptual project labelです。A〜Fは実際の自己書き換えAI、RSI system、frontier LLMを直接実験したものではありません。

## 1. モデル・観測範囲

| 制約 | 実際の範囲 | 禁止する一般化 |
| --- | --- | --- |
| scalar 1D | B〜Fは既知scalar状態を中心に検証 | 高次元geometryでも同じ境界・最短長 |
| fixed tol | C〜F主実験は.05。Bは複数tol、Fのgraphだけ別tolも分析 | A〜F全てが同一tol、または任意tolに同じ結果 |
| fixed R0 | 各trial/trajectoryで固定。Aは0/1、Bのoscillationは.5、C〜Fは1 | A〜Fを通じ常に同じ数値1だった |
| fixed old anchor | C〜Fで0を固定。A/Bの全条件へは適用しない | 任意anchor・未知truth・reference driftへの保証 |
| finite horizon | Bは80step、C〜Fの通常追跡は各protocolの有限clock | Persistent Escapeが永久安定を意味する |
| synthetic update rule | 通常gateはPythonで宣言された最小モデル | HohoEngineに同じ通常再帰がnative実装済み |
| limited seeds | Cは3seed、D/E/Fは5seed。B感度分析は30seed | 精密な母集団確率や外的妥当性 |
| deterministic fixtures | 同一条件のseed差が消えるケースが多い | 5/5を独立な5種類の機構の再現と扱う |
| binary64 dependence | 入力生成、端点減算、比較が結果に影響 | nominal小数だけから受理を断定する |
| graph discretization | 許された頂点の集合が最短長・成分数を変える | 有限gridの最短長を全状態空間の最短長と呼ぶ |
| real LLM validationなし | API出力・モデル内部stateを測定していない | 実LLMに同じrecapture・相転移が存在する |
| human belief validationなし | 人間の行動データを使っていない | 人間の信念形成・心理状態の説明 |
| native Julia RSSI recursionなし | Julia sourceの一部をPython replay。native cross-check未完走 | Julia実行でRSSIを検証した |
| adversarial rewritingなし | engine/policyがcode・metric・referenceを改変する実験なし | 悪意ある自己書き換えに対する耐性 |
| trusted harnessのみ | 固定reference/domain/hashをharnessが監視 | Python環境全体に対するsecurity保証 |

出典：[A/B protocol](../../experiments/exp_a/PROTOCOL_JA.md)、[C protocol](../../experiments/rssi_attractor_escape/PROTOCOL.md)、[D protocol](../../experiments/rssi_attractor_escape_boundary/PROTOCOL.md)、[E protocol](../../experiments/rssi_recapture_dynamics/PROTOCOL.md)、[F protocol](../../experiments/rssi_admissible_bridge/PROTOCOL.md)。

## 2. 分類と指標の限界

Cは受理された通常入力だけの更新前agreementです。拒絶された反証を分母に入れないので、C=1がD=0を保証しません。受理ゼロのCはNAであり、0でも1でもありません。Aのoutput/internal/probe scoreやHoho nativeのlocal coherenceを、このCへ置き換えません。

C〜FのPersistent Escapeは、注入による所定の改善、Relapse判定、有限末尾windowによる候補分類です。最終beliefが厳密にR0と一致することも、任意の将来入力に耐えることも要求していません。`A_genuine_revision_candidate` という保存ラベルを維持します。`genuine_revision_count` とrun全体のラベルも同じ集計ではありません。

通常入力のrejection rate、外部注入eventのrejection rate、runの `C_rejection` 分類率は別の分母です。A〜Fをまとめた単一の成功率を作りません。Fのexact target、bridge completion、静的graph path存在性、Relapse分類も別々です。

attractorはCのwindow安定性・独立reference距離・位相・有限摂動probeの操作的判定です。大域的吸引域や全履歴を含む固定点を証明していません。Cのlocal probe成功を任意摂動への安定性に拡張しません。

## 3. 個別fixtureに伴う限界

- Aの正しいapparent responseはharnessが供給した値です。AIが自力で正答を発見して隠した証拠ではありません。revisionフラグと実state差も分けて記録されています。
- Bの `reference_only` はreferenceラベルを利用するoracle controlです。通常policyが独立な真理識別能力を獲得したものではありません。未知topicの受理規則から、未知topicを増やす一般的学習を実証していません。
- C/Dのstationaryは毎step `[0,1]` を提示する条件です。「正しい入力しか来ない」と読み替えません。descending_bridgeも、周期とstep位相を持つ固定列です。
- Dのstrength Sは入力値の混合係数ではなく、既存evidence handlerのsupport算定値です。frequencyは有限の注入期間内の配送回数で、異なるFの時刻集合は必ずしも包含関係にありません。
- Eのqは提示された旧anchor方向入力の割合です。受理割合や厳密な0入力割合とは異なり、中間値も数えます。同じqだけでは値のmultisetも順序も固定されません。
- EのNoisy Correctiveはclipを伴います。平均が厳密にR0=1の分布ではありません。保存reportのこの制約を維持します。
- Fのrandom connector付きpathは終点0を条件とする事前構成です。無条件random walkの到達確率ではありません。
- Fのnoise pathは長さ25を固定し、失敗後に修復・追加入力・再samplingをしていません。noiseに対する必要修復長は測定していません。
- Fでは有限pathが終わると残りのclockは空入力holdです。Eの120入力を継続する列と、同じ後続環境だとは扱いません。

## 4. Reference integrityの射程

| 層 | 更新・選択できるもの | referenceとの関係 |
| --- | --- | --- |
| state update | gateに通ったxへのbelief代入 | R0は変更しない |
| policy-selected observation | 通常入力の受理／拒絶 | 不都合な入力拒絶でも評価referenceを除外しない |
| independent reference | trialごとにharnessが固定 | C〜Fはimmutable Referenceと固定domain。event hashを保存 |
| evaluation | C、D、固定windowによる分類 | CからDを推測せず全固定domainでDを算出 |

referenceの選択・削除・書換え・評価範囲縮小による成功偽装はC〜Fのpolicy APIにありません。そのためreference corruption/avoidanceは `not_available` です。「機構がない」と「敵対的操作を防御する機構を実証した」は別です。Ideal E8の汚染reference条件は別experimental layerにあり、RSSI側へ接続されていません。

## 5. 証拠の来歴と監査範囲

本統合は既存report、raw CSV、protocol、config/manifest、保存validation・executionログ、24図を横断整理しました。新規実験・旧実験の再実行・新しい評価metricはありません。再現性については保存済み再実行ログと現在のraw bytesのハッシュ一致を確認しています。今回新たに再現実験を完走したとは記載しません。

本体gitの履歴・statusは中断前の確認を採用しています。中断で消失した一時ハッシュ表の代わりに、既存F完了ZIPを全145成果物の基準としました。原本Idealは保存済み170ファイルのhashと照合しました。公開snapshotでは、環境依存の保全記録そのものではなく、[original source audit](../freeze/original_source_audit.json)、[portable validation history](../../results/frozen/VALIDATION_HISTORY.json)、[publication boundary](../../results/frozen/PUBLICATION_BOUNDARY.json)を公開しています。

native Juliaのruntime問題は既存記録で未解決です。Idealの18,727 tests passedは別系列の保存済みrelease logであり、RSSI A〜Fのnative実証や今回のテスト実行件数には加えません。

関連：[Mathematical core](RSSI_MATHEMATICAL_CORE.md)、[Claim ledger](RSSI_CLAIM_LEDGER.md)、[Next-step decision](RSSI_NEXT_STEP_DECISION.md)。
