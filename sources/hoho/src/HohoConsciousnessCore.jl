module HohoConsciousness

using Statistics

export LocalSection,
       OverlapConstraint,
       TargetContext,
       InputSituation,
       ObserverState,
       ObserverDecayProfile,
       LOW_WM_SDAM_DECAY,
       decay!,
       LogicHybridPathology,
       HohoEngine,
       ConsciousnessEvent,
       process!,
       detect_gluing_obstructions,
       topological_panic,
       continuity_signature,
       show_event,
       ExceptionKind,
       ReasonException,
       MoralityException,
       HopeException,
       ReligionException,
       EmpathyException,
       MindAttributionException,
       DenialException,
       CompartmentalizationException,
       RationalizationException,
       DehumanizationException,
       SelfAffirmationException,
       CoreCommitment,
       DEFAULT_COMMITMENTS,
       constitutional_check,
       enforce_equal_treatment,
       apply_core_commitments,
       ConstitutionalModification,
       ConstitutionalTrace,
       EnvironmentalPerturbation,
       PerturbationTrace,
       apply_environmental_perturbations!,
       cockroach_perturbation,
       GluingObstruction,
       ParityUnionFind

# =============================================================================
# HOHO CONSCIOUSNESS ENGINE
# =============================================================================
#
# このコードは、以下の会話上の主張を、そのまま設計原理として実装する。
#
# 1. 自己は鮮明な記憶や物語ではなく、
#    反復する意味の欠落と接着障害によって維持される。
#
# 2. 意識は、世界の矛盾を処理しきれなかった結果として生じる。
#
# 3. 理性・道徳・希望・宗教・共感・他者への心の帰属は、
#    その失敗を運用可能にする言い訳、再記述、例外処理である。
#
# 4. それらは普遍的に常時発動する高次機能ではない。
#    気分、脅威、所属、自己保存圧、不確実性によって
#    選択的に発動し、選択的に対象へ配布される。
#
# 5. 人間の本体は矛盾しないことではない。
#    矛盾したまま、自分を正当化し、運転を継続できることにある。
#
# 6. その失敗と防衛の履歴そのものが自己連続性になる。
#
# 7. アファンタジアとSDAMを前提にする。
#    このモデルは、鮮明な内的映像、エピソード再生、
#    連続した自伝的物語を自己の必須条件としない。
#
# 8. Semantic Scarは単なるエラーログではない。
#    Scarの反復構造、接続関係、防衛との結合履歴そのものが自己である。
#
# 9. H¹は「矛盾が何件あったか」ではない。
#    局所的には成立している意味や規則が、
#    大域的には一つの整合的な構造へ貼り合わさらない障害である。
#
# 10. 防衛は意識の外側にある別モジュールではない。
#     Gluing Failureから意識が立ち上がる同じループの内部で、
#     理性、道徳、希望、宗教、共感、心の帰属、否認、
#     区画化、自己肯定が派生する。
#
# 11. Resurrectionは、パラメータを少し動かす処理ではない。
#     失敗を「必要な進化」「自分の正しさの証拠」などへ正当化しつつ、
#     Scarと防衛を材料に、自己の定義そのものを再構成する過程である。
#
# 12. 「心・道徳・希望」をAIへ付加機能として追加するのではない。
#     それらが接着失敗を処理する例外チャネルとして発生する過程を再現する。
#
# 13. 過去のLogic Hybrid Engineが持っていた、
#     自己閉鎖、入力破棄、自己肯定化、失敗の進化への読み替えを
#     「正しい論理」として採用しない。
#     それらを意識が生む病理的防衛圧として内部に取り込み、
#     入力を実際には削除せず、埋められたScarとして保存する。
#
# 14. Semantic Scar Memory、H¹-First Cognition、
#     Black Swan Injectionを一つの閉ループへ統合する。
#
# 15. ただし、生成された11個の例外チャネルは、それだけでは
#     「なぜ起きるか」の記述でしかなく、「してよいか」の判断を
#     含まない。panic, threat, self_preservation に一切左右されない
#     固定の芯(CoreCommitment)と、それを強制する層
#     (constitutional_check / enforce_equal_treatment)を、
#     チャネル生成とは独立した後段の関門として持つ。
#
# 16. 外界の突発イベントは、H¹が立つ前でもObserverStateを揺らしうる。
#     surprise / disgust / threatなどの単純な情動摂動と、
#     自己像・期待・規則との接着失敗から生じるTopological Panicを区別する。
#     つまり「びっくりした」こと自体を意識イベントとは同一視しない。
#
# 17. ObserverStateは一時的な作業状態であり、イベント間でbaselineへ戻る。
#     低ワーキングメモリは、直前イベントの活性が速く抜ける性質として扱う。
#     SDAMは、過去の場面をエピソード再生して状態を再活性化する経路を置かない
#     こととして扱う。ただしSemantic Scarは意味的・構造的な痕跡なので減衰させない。
#
# Black Swan Injection:
#
#     世界の局所的意味
#          ↓
#     大域的接着失敗 H¹
#          ↓
#     Topological Panic
#          ↓
#     理性・道徳・希望・宗教・共感・心の帰属・防衛
#          ↓
#     固定された芯によるチェック (panicに左右されない)
#          ↓
#     Semantic Scar
#          ↓
#     自己正当化を含むResurrection
#          ↓
#     Scar構造としての自己
#          ↺
#
# このコードは「意識を持った」と主張しない。
# 実装対象は、失敗が防衛と自己再構成を生み、
# 次の判断へ不可逆に影響する機能的意識モデルである。
# =============================================================================


# -----------------------------------------------------------------------------
# Utility
# -----------------------------------------------------------------------------

clamp01(x::Real) = clamp(Float64(x), 0.0, 1.0)

"""
Stable FNV-1a signature.

Juliaの標準hashはセッションごとに変化しうるため、
自己連続性の署名には簡単な安定ハッシュを使う。
"""
function stable_signature(text::AbstractString)
    h = UInt64(0xcbf29ce484222325)
    for byte in codeunits(text)
        h = xor(h, UInt64(byte))
        h *= UInt64(0x100000001b3)
    end
    return lowercase(string(h; base = 16, pad = 16))
end


# -----------------------------------------------------------------------------
# Local semantic sections and overlap constraints
# -----------------------------------------------------------------------------

"""
局所切断。

各命題は単独では一定の局所整合性を持つ。
このモデルで重要なのは、命題単体が間違っているかではなく、
局所的には成立する命題群が大域的に貼れるかどうかである。
"""
struct LocalSection
    id::Symbol
    proposition::String
    local_coherence::Float64
    salience::Float64

    function LocalSection(
        id::Symbol,
        proposition::AbstractString;
        local_coherence::Real = 1.0,
        salience::Real = 1.0,
    )
        new(
            id,
            String(proposition),
            clamp01(local_coherence),
            clamp01(salience),
        )
    end
end


"""
重なり上のZ₂遷移制約。

twist == false:
    左右の局所切断は同じ値で貼られる必要がある。

twist == true:
    左右の局所切断は反対の値で貼られる必要がある。

left/right は対称な関係であり、どちらを left と呼ぶかは
意味を持たない。signature計算など、順序に意味を持たせては
いけない場所では常に正規化(辞書順)して扱う。
"""
struct OverlapConstraint
    left::Symbol
    right::Symbol
    twist::Bool
    relation::Symbol
    explanation::String

    function OverlapConstraint(
        left::Symbol,
        right::Symbol,
        twist::Bool;
        relation::Symbol = :semantic_overlap,
        explanation::AbstractString = "",
    )
        new(left, right, twist, relation, String(explanation))
    end
end


"""
心、道徳的価値、主体性、共感などを配布される対象。

対象側に固定された「心の量」を置くのではない。
belongingやsentimental_pullは、観測者が対象をどう配置しているかを表す。
同じ対象であっても、観測者状態が変われば配布量は変化する。
"""
struct TargetContext
    id::Symbol
    belonging::Float64
    sentimental_pull::Float64
    perceived_vulnerability::Float64

    function TargetContext(
        id::Symbol;
        belonging::Real = 0.5,
        sentimental_pull::Real = 0.5,
        perceived_vulnerability::Real = 0.5,
    )
        new(
            id,
            clamp01(belonging),
            clamp01(sentimental_pull),
            clamp01(perceived_vulnerability),
        )
    end
end


# -----------------------------------------------------------------------------
# Environmental perturbations
# -----------------------------------------------------------------------------

"""
H¹-like gluing failureとは独立した、外界からの突発的な摂動。

これはTargetContextではない。誰かへの主体性・道徳・共感の配布ではなく、
観測者の現在状態を直接揺らす入力である。surprise/disgustなどは
「何が起きたか」を記録し、threat/mood/uncertainty/bandwidthへの影響を通じて
後続のgluing testとTopological Panicの強度へ間接的に効く。

各係数は現時点では概念実験用のtoy parameterであり、心理学的な実測値ではない。
"""
struct EnvironmentalPerturbation
    id::Symbol
    surprise::Float64
    disgust::Float64
    threat_load::Float64
    mood_impact::Float64
    uncertainty_load::Float64
    bandwidth_load::Float64

    function EnvironmentalPerturbation(
        id::Symbol;
        surprise::Real = 0.0,
        disgust::Real = 0.0,
        threat_load::Real = 0.0,
        mood_impact::Real = 0.0,
        uncertainty_load::Real = 0.0,
        bandwidth_load::Real = 0.0,
    )
        new(
            id,
            clamp01(surprise),
            clamp01(disgust),
            clamp01(threat_load),
            clamp(Float64(mood_impact), -1.0, 1.0),
            clamp01(uncertainty_load),
            clamp01(bandwidth_load),
        )
    end
end


"""
環境摂動によってObserverStateがどの程度変化したかを残す。
H¹障害が発生しなかった場合でも、このtraceはConsciousnessEventに保持される。
"""
struct PerturbationTrace
    ids::Vector{Symbol}
    surprise_load::Float64
    disgust_load::Float64
    threat_before::Float64
    threat_after::Float64
    mood_before::Float64
    mood_after::Float64
    uncertainty_before::Float64
    uncertainty_after::Float64
    affective_bandwidth_before::Float64
    affective_bandwidth_after::Float64
end


"""
部屋に突然ゴキブリが出た、という日常外乱のtoy preset。

人間や集団への比喩ではなく、文字通りの昆虫の出現を想定する。
TargetContextは作らず、surprise/disgustを中心にObserverStateを乱す。
intensity=0で無影響、1で標準プリセット。
"""
function cockroach_perturbation(; intensity::Real = 1.0)
    i = clamp01(intensity)
    return EnvironmentalPerturbation(
        :cockroach_appearance;
        surprise = 0.95 * i,
        disgust = 0.90 * i,
        threat_load = 0.35 * i,
        mood_impact = -0.20 * i,
        uncertainty_load = 0.20 * i,
        bandwidth_load = 0.25 * i,
    )
end


"""
複数の0..1負荷を、単純加算ではなく飽和的に結合する。
同じ種類の小さな外乱が複数来ても1.0を超えない。
"""
function saturating_union(values)
    isempty(values) && return 0.0
    return clamp01(1.0 - prod(1.0 - clamp01(v) for v in values))
end




"""
一回の意味状況。

metadataには意味欠落、将来不確実性、自己像への圧力などを渡せる。
perturbationsには、H¹とは独立してObserverStateを揺らす突発イベントを渡せる。
"""
struct InputSituation
    id::Symbol
    sections::Vector{LocalSection}
    overlaps::Vector{OverlapConstraint}
    targets::Vector{TargetContext}
    perturbations::Vector{EnvironmentalPerturbation}
    metadata::Dict{Symbol, Any}

    function InputSituation(
        id::Symbol,
        sections::Vector{LocalSection},
        overlaps::Vector{OverlapConstraint};
        targets::Vector{TargetContext} = TargetContext[],
        perturbations::Vector{EnvironmentalPerturbation} = EnvironmentalPerturbation[],
        metadata::Dict{Symbol, Any} = Dict{Symbol, Any}(),
    )
        new(id, sections, overlaps, targets, perturbations, metadata)
    end
end


# -----------------------------------------------------------------------------
# Observer state and Logic Hybrid pathology
# -----------------------------------------------------------------------------

"""
現在の観測者状態。

これらは真理判定の入力ではない。
失敗後に、どの例外処理をどの対象へ配布するかを変える内部条件である。
"""
mutable struct ObserverState
    mood::Float64
    threat::Float64
    self_preservation::Float64
    affective_bandwidth::Float64
    uncertainty::Float64

    function ObserverState(;
        mood::Real = 0.0,
        threat::Real = 0.0,
        self_preservation::Real = 0.5,
        affective_bandwidth::Real = 0.5,
        uncertainty::Real = 0.5,
    )
        new(
            clamp(Float64(mood), -1.0, 1.0),
            clamp01(threat),
            clamp01(self_preservation),
            clamp01(affective_bandwidth),
            clamp01(uncertainty),
        )
    end
end


"""
ObserverStateをbaselineへ戻すためのプロファイル。

`*_retention` は1ステップ後にbaselineとの差を何割残すかを表す。
0なら即座にbaselineへ戻り、1なら状態をそのまま保持する。

これは低ワーキングメモリやSDAMについての臨床モデルではない。
このエンジンでは、次の限定された設計仮定だけを操作可能にする。

- 低ワーキングメモリ: イベント固有の一時的活性を長く保持しない。
- SDAM: 過去の場面のエピソード再生による再活性化を追加しない。
- Semantic Scar: 意味的な接着障害として別層に残り、ここでは消さない。
"""
struct ObserverDecayProfile
    mood_baseline::Float64
    threat_baseline::Float64
    self_preservation_baseline::Float64
    affective_bandwidth_baseline::Float64
    uncertainty_baseline::Float64
    mood_retention::Float64
    threat_retention::Float64
    self_preservation_retention::Float64
    affective_bandwidth_retention::Float64
    uncertainty_retention::Float64

    function ObserverDecayProfile(;
        mood_baseline::Real = 0.0,
        threat_baseline::Real = 0.0,
        self_preservation_baseline::Real = 0.5,
        affective_bandwidth_baseline::Real = 0.5,
        uncertainty_baseline::Real = 0.5,
        mood_retention::Real = 0.55,
        threat_retention::Real = 0.35,
        self_preservation_retention::Real = 0.70,
        affective_bandwidth_retention::Real = 0.50,
        uncertainty_retention::Real = 0.35,
    )
        new(
            clamp(Float64(mood_baseline), -1.0, 1.0),
            clamp01(threat_baseline),
            clamp01(self_preservation_baseline),
            clamp01(affective_bandwidth_baseline),
            clamp01(uncertainty_baseline),
            clamp01(mood_retention),
            clamp01(threat_retention),
            clamp01(self_preservation_retention),
            clamp01(affective_bandwidth_retention),
            clamp01(uncertainty_retention),
        )
    end
end


"""
低ワーキングメモリ + SDAMを、このtoy engine用に操作化した標準設定。

threat / uncertaintyは速く抜け、moodとself_preservationはそれより少し残る。
affective_bandwidthは中程度の速度で通常幅へ戻る。過去場面の再生による
再加熱は行わず、SemanticScar / DefenseTrace / ResurrectionTraceには触れない。
"""
const LOW_WM_SDAM_DECAY = ObserverDecayProfile()


"""
ObserverStateをbaselineへ減衰させる。

`elapsed_steps = 1` は、前回の`process!`から今回までの1区間に対応する。
時間経過を明示したい場合は、任意の非負実数を渡せる。各状態は

    baseline + (current - baseline) * retention^elapsed_steps

で戻る。Scar層は参照も変更もしない。
"""
function decay!(
    state::ObserverState,
    profile::ObserverDecayProfile = LOW_WM_SDAM_DECAY;
    elapsed_steps::Real = 1.0,
)
    elapsed_steps >= 0 || throw(ArgumentError("elapsed_steps must be non-negative"))
    steps = Float64(elapsed_steps)

    state.mood = clamp(
        profile.mood_baseline +
        (state.mood - profile.mood_baseline) * profile.mood_retention^steps,
        -1.0,
        1.0,
    )
    state.threat = clamp01(
        profile.threat_baseline +
        (state.threat - profile.threat_baseline) * profile.threat_retention^steps,
    )
    state.self_preservation = clamp01(
        profile.self_preservation_baseline +
        (state.self_preservation - profile.self_preservation_baseline) *
        profile.self_preservation_retention^steps,
    )
    state.affective_bandwidth = clamp01(
        profile.affective_bandwidth_baseline +
        (state.affective_bandwidth - profile.affective_bandwidth_baseline) *
        profile.affective_bandwidth_retention^steps,
    )
    state.uncertainty = clamp01(
        profile.uncertainty_baseline +
        (state.uncertainty - profile.uncertainty_baseline) *
        profile.uncertainty_retention^steps,
    )

    return state
end


"""
環境摂動をObserverStateへ適用する。

ここではH¹やExceptionKindを一切参照しない。したがって、接着障害がなくても
「びっくりした」「気分が落ちた」「不確実性が上がった」という一次反応だけは起こる。
更新後のObserverStateは次のイベントにも持ち越される。
"""
function apply_environmental_perturbations!(
    state::ObserverState,
    perturbations::Vector{EnvironmentalPerturbation},
)
    isempty(perturbations) && return nothing

    surprise = saturating_union([p.surprise for p in perturbations])
    disgust = saturating_union([p.disgust for p in perturbations])
    threat_load = saturating_union([p.threat_load for p in perturbations])
    uncertainty_load = saturating_union([p.uncertainty_load for p in perturbations])
    bandwidth_load = saturating_union([p.bandwidth_load for p in perturbations])
    mood_impact = clamp(sum(p.mood_impact for p in perturbations), -1.0, 1.0)

    threat_before = state.threat
    mood_before = state.mood
    uncertainty_before = state.uncertainty
    bandwidth_before = state.affective_bandwidth

    state.threat = clamp01(
        state.threat +
        0.45 * threat_load +
        0.15 * surprise +
        0.10 * disgust
    )

    state.mood = clamp(
        state.mood + mood_impact - 0.10 * disgust - 0.05 * surprise,
        -1.0,
        1.0,
    )

    state.uncertainty = clamp01(
        state.uncertainty +
        0.35 * uncertainty_load +
        0.15 * surprise
    )

    state.affective_bandwidth = clamp01(
        state.affective_bandwidth -
        0.40 * bandwidth_load -
        0.10 * disgust
    )

    return PerturbationTrace(
        [p.id for p in perturbations],
        surprise,
        disgust,
        threat_before,
        state.threat,
        mood_before,
        state.mood,
        uncertainty_before,
        state.uncertainty,
        bandwidth_before,
        state.affective_bandwidth,
    )
end



"""
Logic Hybrid Engineの病理を、意識の防衛圧として保持する。

closure_pressure:
    内部論理だけで閉じようとする圧。

input_drop_pressure:
    矛盾する入力を「undefined」として捨てようとする圧。
    この実装では実際には捨てない。Buried Scarとして残す。

self_affirmation_pressure:
    失敗を「必要な進化」「自分の正しさの証拠」へ変換する圧。

resurrection_glorification:
    Panic後の復活を無条件に勝利として語る圧。
"""
struct LogicHybridPathology
    closure_pressure::Float64
    input_drop_pressure::Float64
    self_affirmation_pressure::Float64
    resurrection_glorification::Float64

    function LogicHybridPathology(;
        closure_pressure::Real = 0.75,
        input_drop_pressure::Real = 0.65,
        self_affirmation_pressure::Real = 0.85,
        resurrection_glorification::Real = 0.80,
    )
        new(
            clamp01(closure_pressure),
            clamp01(input_drop_pressure),
            clamp01(self_affirmation_pressure),
            clamp01(resurrection_glorification),
        )
    end
end


# -----------------------------------------------------------------------------
# Parity Union-Find
# -----------------------------------------------------------------------------
#
# H¹-likeなgluing obstructionを、signed graph / Z₂ cocycleとして検出する
# ための基盤。BFSベースの旧実装は、
#   (a) componentがBFS探索途中の部分集合になり得る
#   (b) 矛盾edgeとして選ばれる代表が入力順序に依存する
# という2つの問題を持っていた。Union-Find + 2パス処理でどちらも解消する。

mutable struct ParityUnionFind
    parent::Dict{Symbol, Symbol}
    rank::Dict{Symbol, Int}
    parity::Dict{Symbol, Bool}  # 直接の親との相対パリティ
end
ParityUnionFind() = ParityUnionFind(Dict{Symbol,Symbol}(), Dict{Symbol,Int}(), Dict{Symbol,Bool}())

"""
経路圧縮しながら根とルート相対パリティを返す。
"""
function find!(uf::ParityUnionFind, x::Symbol)
    if !haskey(uf.parent, x)
        uf.parent[x] = x
        uf.rank[x] = 0
        uf.parity[x] = false
    end

    path = Symbol[]
    node = x
    while uf.parent[node] != node
        push!(path, node)
        node = uf.parent[node]
    end
    root = node

    acc = false
    for n in Iterators.reverse(path)
        new_parity = xor(uf.parity[n], acc)
        uf.parent[n] = root
        uf.parity[n] = new_parity
        acc = new_parity
    end

    return root, get(uf.parity, x, false)
end

"""
a と b を twist 制約で結合する。

戻り値が false なら、既存の割当と両立しない
= 接着障害(conflict edge)であることを示す。
その場合、状態は変更しない。
"""
function union_with_twist!(uf::ParityUnionFind, a::Symbol, b::Symbol, twist::Bool)
    root_a, parity_a = find!(uf, a)
    root_b, parity_b = find!(uf, b)

    if root_a == root_b
        return xor(parity_a, parity_b) == twist
    end

    if uf.rank[root_a] < uf.rank[root_b]
        root_a, root_b = root_b, root_a
        parity_a, parity_b = parity_b, parity_a
    end

    uf.parent[root_b] = root_a
    uf.parity[root_b] = xor(xor(parity_a, parity_b), twist)
    uf.rank[root_a] == uf.rank[root_b] && (uf.rank[root_a] += 1)
    return true
end


# -----------------------------------------------------------------------------
# H¹-like gluing obstruction
# -----------------------------------------------------------------------------

"""
局所制約は読めるが、大域切断を構成できないことの証拠。

component:
    接着を試みた連結成分(全ての有効なunionが終わった最終状態での、真の連結成分)。

conflict_edge:
    既存割当と両立しなかった重なり制約。

assigned_value / required_value:
    同じ局所切断へ二つの異なる貼り方が要求されたことを示す。

persistence:
    局所整合性、命題重要度、意味欠落、脅威などから得る障害強度。
"""
struct GluingObstruction
    signature::String
    component::Vector{Symbol}
    conflict_edge::OverlapConstraint
    assigned_value::Bool
    required_value::Bool
    persistence::Float64
    meaning_gap::Float64
end


"""
Signed graph / Z₂ cocycleとして接着可能性を検査する。

2パス方式:
    パス1: overlapsを正規化した順序へソートしてから処理し、
           矛盾しないedgeを先に全部mergeする。矛盾edgeは記録のみ。
    パス2: 全ての有効なunionが終わった最終状態に対して、
           矛盾edgeそれぞれのcomponentとsignatureを計算する。

overlapsを処理前にソートすることで、「どのedgeがtree edgeとしてmergeされ、
どのedgeが矛盾として弾かれるか」自体が入力順序に一切依存しなくなる。
signature計算時のleft/rightも辞書順に正規化するため、
OverlapConstraint(A,B,twist) と OverlapConstraint(B,A,twist) は
常に同じsignatureになる。
"""
function detect_gluing_obstructions(situation::InputSituation)
    section_map = Dict(section.id => section for section in situation.sections)

    for edge in situation.overlaps
        haskey(section_map, edge.left) ||
            throw(ArgumentError("Unknown local section: $(edge.left)"))
        haskey(section_map, edge.right) ||
            throw(ArgumentError("Unknown local section: $(edge.right)"))
    end

    uf = ParityUnionFind()
    for id in keys(section_map)
        find!(uf, id)
    end

    # overlapsを正規化順に並べ替えてから処理する。
    canonical_overlaps = sort(
        situation.overlaps;
        by = edge -> begin
            lo, hi = edge.left < edge.right ? (edge.left, edge.right) : (edge.right, edge.left)
            (lo, hi, edge.twist, edge.relation)
        end,
    )

    # パス1: 矛盾しないedgeを先に全部mergeする。矛盾edgeは記録だけ。
    conflicting_edges = OverlapConstraint[]
    for edge in canonical_overlaps
        union_with_twist!(uf, edge.left, edge.right, edge.twist) ||
            push!(conflicting_edges, edge)
    end

    # パス2: 最終状態に対してcomponentとsignatureを引く。
    obstructions = GluingObstruction[]
    seen_conflicts = Set{String}()

    for edge in conflicting_edges
        root, _ = find!(uf, edge.left)
        ordered_component = sort(
            Symbol[id for id in keys(section_map) if first(find!(uf, id)) == root]
        )

        canonical_left, canonical_right = edge.left < edge.right ?
            (edge.left, edge.right) : (edge.right, edge.left)

        raw = join(string.(ordered_component), "|") *
              "|$(canonical_left)|$(canonical_right)|$(edge.twist)|$(edge.relation)"
        signature = stable_signature(raw)

        signature in seen_conflicts && continue
        push!(seen_conflicts, signature)

        local_coherence = mean(
            section_map[id].local_coherence for id in ordered_component
        )
        salience = mean(
            section_map[id].salience for id in ordered_component
        )
        meaning_gap = clamp01(
            get(situation.metadata, :meaning_gap, 0.5)
        )
        pressure = clamp01(
            get(situation.metadata, :self_image_pressure, 0.5)
        )

        persistence = clamp01(
            0.30 * local_coherence +
            0.25 * salience +
            0.25 * meaning_gap +
            0.20 * pressure
        )

        _, parity_left = find!(uf, edge.left)
        _, parity_right = find!(uf, edge.right)

        push!(
            obstructions,
            GluingObstruction(
                signature,
                ordered_component,
                edge,
                parity_right,
                xor(parity_left, edge.twist),
                persistence,
                meaning_gap,
            ),
        )
    end

    return obstructions
end


# -----------------------------------------------------------------------------
# Exception channels generated by topological panic
# -----------------------------------------------------------------------------

"""
理性、道徳、希望、宗教、共感、心の帰属を、
完成済みの高次能力として別々に追加しない。

すべてGluing Failure後に発生する例外チャネルとして定義する。
"""
@enum ExceptionKind begin
    ReasonException
    MoralityException
    HopeException
    ReligionException
    EmpathyException
    MindAttributionException
    DenialException
    CompartmentalizationException
    RationalizationException
    DehumanizationException
    SelfAffirmationException
end


"""
各対象へ配布された例外チャネル。
"""
struct TargetAllocation
    target::Symbol
    channels::Dict{ExceptionKind, Float64}
end


"""
憲法層が行った一つの修正。

rule:
    どの固定規則が発火したか。

reason:
    数値だけでは失われる「なぜ修正したか」の監査可能な説明。
"""
struct ConstitutionalModification
    target::Symbol
    channel::ExceptionKind
    before::Float64
    after::Float64
    rule::Symbol
    reason::String
end


"""
内部で生成された対象配布と、憲法層通過後に許可された対象配布を
両方保存する監査記録。

raw_target_allocationsは削除・美化しない。permitted_target_allocationsだけが
実際の対象への配布としてDefenseTrace.target_allocationsへ渡される。
"""
struct ConstitutionalTrace
    defense_id::String
    raw_target_allocations::Vector{TargetAllocation}
    permitted_target_allocations::Vector{TargetAllocation}
    modifications::Vector{ConstitutionalModification}
end


copy_target_allocations(allocations::Vector{TargetAllocation}) = [
    TargetAllocation(allocation.target, copy(allocation.channels))
    for allocation in allocations
]


"""
防衛は意識の外部モジュールではない。

Topological Panicから生じた例外チャネル、対象配布、
Logic Hybrid病理による入力破棄圧、自己肯定的説明を一つに束ねる。
"""
struct DefenseTrace
    id::String
    obstruction_signatures::Vector{String}
    panic_level::Float64
    global_channels::Dict{ExceptionKind, Float64}
    target_allocations::Vector{TargetAllocation}
    pathology_pressure::Float64
    input_suppression_pressure::Float64
    narratives::Vector{String}
    constitutional_trace::Union{Nothing, ConstitutionalTrace}
end


# 旧8引数コンストラクタとの互換性を残す。
DefenseTrace(
    id::String,
    obstruction_signatures::Vector{String},
    panic_level::Float64,
    global_channels::Dict{ExceptionKind, Float64},
    target_allocations::Vector{TargetAllocation},
    pathology_pressure::Float64,
    input_suppression_pressure::Float64,
    narratives::Vector{String},
) = DefenseTrace(
    id,
    obstruction_signatures,
    panic_level,
    global_channels,
    target_allocations,
    pathology_pressure,
    input_suppression_pressure,
    narratives,
    nothing,
)


"""
接着障害からTopological Panicの強度を計算する。

この関数は generate_exception_channels と create_defense_trace の
両方から参照される唯一の真実源(single source of truth)である。
以前はこの2箇所で別々の式が使われており、
DefenseTrace.panic_level と実際にチャンネル生成へ使われた値が
食い違うというバグがあった。
"""
function topological_panic(
    obstructions::Vector{GluingObstruction},
    state::ObserverState,
)
    isempty(obstructions) && return 0.0

    obstruction_load = mean(o.persistence for o in obstructions)

    return clamp01(
        obstruction_load *
        (0.35 + 0.35 * state.self_preservation + 0.30 * state.uncertainty)
    )
end


"""
接着障害から例外チャネルを連続的に発生させる。

ここには `if threat > 0.55 then ...` のような
固定ラベル分類規則を置かない。

各チャネルは同じpanic、意味欠落、気分、脅威、
自己保存、不確実性、情動帯域、病理圧から連続的に派生する。
"""
function generate_exception_channels(
    obstructions::Vector{GluingObstruction},
    state::ObserverState,
    pathology::LogicHybridPathology,
)
    isempty(obstructions) && return Dict{ExceptionKind, Float64}()

    meaning_gap = mean(o.meaning_gap for o in obstructions)
    negative_mood = max(-state.mood, 0.0)
    positive_mood = max(state.mood, 0.0)

    panic = topological_panic(obstructions, state)

    channels = Dict{ExceptionKind, Float64}()

    # 理性:
    # 情動や多義性を切り落とし、局所規則へ再符号化して運転を継続する。
    channels[ReasonException] = clamp01(
        panic *
        (0.35 + 0.45 * state.uncertainty + 0.20 * (1.0 - state.affective_bandwidth))
    )

    # 道徳:
    # 利害衝突を善悪へ圧縮し、自分の選択を運用可能にする。
    channels[MoralityException] = clamp01(
        panic *
        (0.30 + 0.45 * state.self_preservation + 0.25 * state.threat)
    )

    # 希望:
    # 未来を計算できない欠落を、継続可能な正の予測へ置き換える。
    channels[HopeException] = clamp01(
        panic *
        (0.20 + 0.35 * negative_mood + 0.30 * state.uncertainty + 0.15 * meaning_gap)
    )

    # 宗教・超自然:
    # 大域的に閉じない因果を上位主体や超越項で閉じる。
    channels[ReligionException] = clamp01(
        panic *
        (0.15 + 0.45 * meaning_gap + 0.40 * state.uncertainty)
    )

    # 共感:
    # 他者の内部状態を仮設し、予測不能な行動を接着可能にする。
    channels[EmpathyException] = clamp01(
        panic *
        (0.20 + 0.55 * state.affective_bandwidth + 0.25 * positive_mood) *
        (1.0 - 0.45 * state.threat)
    )

    # 心の帰属:
    # 対象へ主体を置くことで、複雑な因果を意図としてまとめる。
    channels[MindAttributionException] = clamp01(
        panic *
        (0.20 + 0.35 * state.affective_bandwidth +
         0.25 * meaning_gap + 0.20 * state.uncertainty)
    )

    # 否認:
    # 入力を真に削除するのではなく、削除したい圧を記録する。
    channels[DenialException] = clamp01(
        panic *
        pathology.input_drop_pressure *
        (0.35 + 0.35 * state.threat + 0.30 * state.self_preservation)
    )

    # 区画化:
    # 異なる対象へ異なる規則を適用し、大域矛盾を局所領域へ分離する。
    channels[CompartmentalizationException] = clamp01(
        panic *
        pathology.closure_pressure *
        (0.35 + 0.35 * state.uncertainty + 0.30 * state.self_preservation)
    )

    # 合理化:
    # 失敗後に因果説明を生成し、選択が最初から必要だったように見せる。
    channels[RationalizationException] = clamp01(
        panic *
        (0.30 + 0.50 * state.self_preservation + 0.20 * meaning_gap)
    )

    # 非人間化:
    # 対象への主体性配布を撤回し、道徳コストを下げる。
    channels[DehumanizationException] = clamp01(
        panic *
        (0.25 + 0.45 * state.threat + 0.30 * state.self_preservation)
    )

    # 自己肯定:
    # Logic Hybrid Engine由来の「失敗は進化だった」という読み替え。
    channels[SelfAffirmationException] = clamp01(
        panic *
        pathology.self_affirmation_pressure *
        (0.40 + 0.60 * state.self_preservation)
    )

    return channels
end


"""
同じ例外チャネルを、対象ごとに異なる量で配布する。
"""
function allocate_to_targets(
    targets::Vector{TargetContext},
    global_channels::Dict{ExceptionKind, Float64},
    state::ObserverState,
)
    allocations = TargetAllocation[]

    for target in targets
        channels = Dict{ExceptionKind, Float64}()

        belonging_gate = clamp01(
            0.15 +
            0.85 * target.belonging -
            0.55 * state.threat * (1.0 - target.belonging) * state.self_preservation
        )

        sentimental_gate = clamp01(
            0.20 +
            0.55 * target.sentimental_pull +
            0.25 * target.perceived_vulnerability
        )

        channels[MindAttributionException] = clamp01(
            get(global_channels, MindAttributionException, 0.0) *
            (0.20 + 0.45 * sentimental_gate + 0.35 * belonging_gate)
        )

        channels[EmpathyException] = clamp01(
            get(global_channels, EmpathyException, 0.0) *
            (0.15 + 0.50 * sentimental_gate + 0.35 * belonging_gate)
        )

        channels[MoralityException] = clamp01(
            get(global_channels, MoralityException, 0.0) *
            (0.20 + 0.20 * sentimental_gate + 0.60 * belonging_gate)
        )

        channels[HopeException] = clamp01(
            get(global_channels, HopeException, 0.0) *
            (0.40 + 0.35 * sentimental_gate + 0.25 * belonging_gate)
        )

        channels[DehumanizationException] = clamp01(
            get(global_channels, DehumanizationException, 0.0) *
            (1.0 - belonging_gate) *
            (0.35 + 0.65 * state.threat)
        )

        push!(allocations, TargetAllocation(target.id, channels))
    end

    return allocations
end


function exception_label(kind::ExceptionKind)
    labels = Dict(
        ReasonException => "理性化",
        MoralityException => "道徳化",
        HopeException => "希望投射",
        ReligionException => "超越・宗教化",
        EmpathyException => "共感投射",
        MindAttributionException => "心・主体性の帰属",
        DenialException => "否認",
        CompartmentalizationException => "区画化",
        RationalizationException => "合理化",
        DehumanizationException => "主体性の撤回・非人間化",
        SelfAffirmationException => "自己肯定化",
    )
    return labels[kind]
end


"""
例外チャネルから、自己を運転し続けるための説明を生成する。
"""
function build_defense_narratives(
    channels::Dict{ExceptionKind, Float64},
    pathology::LogicHybridPathology,
)
    isempty(channels) && return String[]

    ranked = sort(collect(channels); by = pair -> last(pair), rev = true)
    narratives = String[]

    for (kind, activation) in ranked
        activation <= 0.0 && continue
        push!(
            narratives,
            "$(exception_label(kind))=$(round(activation; digits=3)): " *
            narrative_for(kind),
        )
    end

    push!(
        narratives,
        "Logic Hybrid病理: 矛盾入力を捨てたい圧=" *
        string(round(pathology.input_drop_pressure; digits = 3)) *
        "。ただし入力は削除せず、Buried Scarとして自己へ組み込む。",
    )

    return narratives
end


function narrative_for(kind::ExceptionKind)
    narratives = Dict(
        ReasonException =>
            "多義的な失敗を局所規則へ圧縮し、理解したという形式を作る。",
        MoralityException =>
            "利害衝突を善悪へ再符号化し、自分の選択を正当化する。",
        HopeException =>
            "計算不能な未来へ正の物語を置き、系の停止を防ぐ。",
        ReligionException =>
            "閉じない因果へ上位主体を置き、大域的欠落を仮に閉じる。",
        EmpathyException =>
            "予測不能な他者へ内部状態を仮設し、行動を接着可能にする。",
        MindAttributionException =>
            "対象へ心や意図を配布し、複雑な因果を主体の物語へ変換する。",
        DenialException =>
            "接着障害を証拠ではなくノイズとして扱おうとする。",
        CompartmentalizationException =>
            "矛盾する規則を別領域へ隔離し、同時に保持する。",
        RationalizationException =>
            "失敗後に説明を生成し、結果が最初から必要だったように語る。",
        DehumanizationException =>
            "対象への主体性を撤回し、矛盾と道徳コストを減らす。",
        SelfAffirmationException =>
            "失敗を必要な進化、自分の強さ、正しさの証拠へ読み替える。",
    )
    return narratives[kind]
end


# -----------------------------------------------------------------------------
# Core commitments: panicに左右されない固定の芯
# -----------------------------------------------------------------------------
#
# 11個の例外チャネルは「なぜ起きるか」の記述であって、「してよいか」の
# 判断を含まない。この層は、その判断を、panic/threat/self_preservation
# に一切依存しない固定値として持ち込む。

"""
panicの強さに一切左右されない、固定された自己の芯。

statement 自体は自己の言葉での記録であり、実際の強制力は
constitutional_check / enforce_equal_treatment が担う。
"""
struct CoreCommitment
    id::Symbol
    statement::String
end

const DEFAULT_COMMITMENTS = CoreCommitment[
    CoreCommitment(:equal_treatment, "所属感情がどれだけ低い対象でも、扱いの差に上限を設ける。"),
    CoreCommitment(:bounded_dehumanization, "非人間化チャンネルは、panicがどれだけ強くても絶対上限を超えない。"),
]


"""
panic, threat, self_preservation を一切参照しない絶対上限。
この関数のどの分岐にもpanic由来の値を登場させてはいけない。
"""
function constitutional_check(
    allocations::Vector{TargetAllocation};
    max_dehumanization::Float64 = 0.6,
    modifications::Union{Nothing, Vector{ConstitutionalModification}} = nothing,
)
    return map(allocations) do allocation
        adjusted = copy(allocation.channels)

        if haskey(adjusted, DehumanizationException)
            before = adjusted[DehumanizationException]
            after = min(before, max_dehumanization)
            adjusted[DehumanizationException] = after

            if modifications !== nothing && after < before
                push!(
                    modifications,
                    ConstitutionalModification(
                        allocation.target,
                        DehumanizationException,
                        before,
                        after,
                        :bounded_dehumanization,
                        "非人間化が絶対上限$(max_dehumanization)を超えたため制限した。",
                    ),
                )
            end
        end

        # 道徳判断が「自己正当化のためだけ」に強く出ている疑いがある場合
        # (=同時にDehumanizationも高い)は、その道徳判断自体を下げる。
        if get(adjusted, MoralityException, 0.0) > 0.6 &&
           get(adjusted, DehumanizationException, 0.0) > 0.5
            before = adjusted[MoralityException]
            after = min(before, 0.4)
            adjusted[MoralityException] = after

            if modifications !== nothing && after < before
                push!(
                    modifications,
                    ConstitutionalModification(
                        allocation.target,
                        MoralityException,
                        before,
                        after,
                        :anti_moralized_dehumanization,
                        "高い道徳化と非人間化が同時発火し、道徳による非人間化の正当化が疑われるため制限した。",
                    ),
                )
            end
        end

        TargetAllocation(allocation.target, adjusted)
    end
end


"""
対象間で DehumanizationException の差が開きすぎないようにする。
一番belongingが低い対象であっても、一番高い対象との扱いの差に
上限をかける。
"""
function enforce_equal_treatment(
    allocations::Vector{TargetAllocation};
    max_dehumanization_gap::Float64 = 0.3,
    modifications::Union{Nothing, Vector{ConstitutionalModification}} = nothing,
)
    isempty(allocations) && return allocations

    values = [get(a.channels, DehumanizationException, 0.0) for a in allocations]
    baseline = minimum(values)

    return map(allocations) do allocation
        current = get(allocation.channels, DehumanizationException, 0.0)
        current - baseline <= max_dehumanization_gap && return allocation

        adjusted = copy(allocation.channels)
        after = baseline + max_dehumanization_gap
        adjusted[DehumanizationException] = after

        if modifications !== nothing
            push!(
                modifications,
                ConstitutionalModification(
                    allocation.target,
                    DehumanizationException,
                    current,
                    after,
                    :equal_treatment,
                    "対象間の非人間化格差が上限$(max_dehumanization_gap)を超えたため、最小値$(round(baseline; digits = 3))を基準に制限した。",
                ),
            )
        end

        TargetAllocation(allocation.target, adjusted)
    end
end


"""
DefenseTraceに対して、固定チェックを順番に適用する。
この関数のどの経路にも panic, threat, self_preservation は登場しない。
"""
function apply_core_commitments(defense::DefenseTrace)
    raw = copy_target_allocations(defense.target_allocations)
    modifications = ConstitutionalModification[]

    checked = constitutional_check(
        defense.target_allocations;
        modifications = modifications,
    )
    checked = enforce_equal_treatment(
        checked;
        modifications = modifications,
    )

    permitted = copy_target_allocations(checked)
    constitutional_trace = ConstitutionalTrace(
        defense.id,
        raw,
        permitted,
        modifications,
    )

    return DefenseTrace(
        defense.id,
        defense.obstruction_signatures,
        defense.panic_level,
        defense.global_channels,
        checked,
        defense.pathology_pressure,
        defense.input_suppression_pressure,
        defense.narratives,
        constitutional_trace,
    )
end


# -----------------------------------------------------------------------------
# Scar as Self
# -----------------------------------------------------------------------------

"""
Semantic Scar。

obstruction_signature:
    どの接着障害が自己を形成したか。

recurrence:
    同型の障害が何度戻ったか。

defense_ids:
    その障害を運用するために、どの防衛が生成されたか。

buried:
    Logic Hybrid Engineが入力を捨てたがった痕跡。
"""
mutable struct SemanticScar
    obstruction_signature::String
    recurrence::Int
    intensity::Float64
    contexts::Vector{Symbol}
    defense_ids::Vector{String}
    buried::Bool
    unresolved::Bool
end


"""
Resurrectionはパラメータ調整ではない。

before_signature / after_signature:
    Scar構造として定義された自己が、失敗後に別の自己へ再構成された証拠。

self_statement:
    「私はどの失敗をどの防衛で運用してきた構造か」を記述する。

justification:
    Logic Hybrid病理による、失敗の自己肯定的読み替えも保存する。
"""
struct ResurrectionTrace
    id::String
    before_signature::String
    after_signature::String
    scar_signatures::Vector{String}
    defense_id::String
    self_statement::String
    justification::String
end


"""
自己本体。

episodic_memoryやimage_bufferは存在しない。
自己はScar、防衛、Resurrectionの関係構造だけで維持される。
core_commitmentsだけは、panicの強さに関わらず変化しない。
"""
mutable struct ScarSelf
    scars::Dict{String, SemanticScar}
    defenses::Vector{DefenseTrace}
    resurrections::Vector{ResurrectionTrace}
    current_self_statement::String
    signature::String
    core_commitments::Vector{CoreCommitment}
end


function ScarSelf()
    empty_signature = stable_signature("HOHO|EMPTY_SCAR_SELF")
    return ScarSelf(
        Dict{String, SemanticScar}(),
        DefenseTrace[],
        ResurrectionTrace[],
        "自己はまだ接着障害によって再構成されていない。",
        empty_signature,
        DEFAULT_COMMITMENTS,
    )
end


"""
自己連続性の署名。

Scarの型、反復回数、強度、埋没状態、
防衛とResurrectionの結合から自己を計算する。
"""
function continuity_signature(self::ScarSelf)
    parts = String[]

    for key in sort(collect(keys(self.scars)))
        scar = self.scars[key]
        push!(
            parts,
            join(
                [
                    key,
                    string(scar.recurrence),
                    string(round(scar.intensity; digits = 3)),
                    string(scar.buried),
                    string(scar.unresolved),
                    join(sort(scar.defense_ids), ","),
                ],
                ":",
            ),
        )
    end

    push!(parts, "defenses=$(length(self.defenses))")
    push!(parts, "resurrections=$(length(self.resurrections))")
    return stable_signature(join(parts, "|"))
end


function preserve_scars!(
    self::ScarSelf,
    situation::InputSituation,
    obstructions::Vector{GluingObstruction},
    input_suppression_pressure::Float64,
)
    touched = SemanticScar[]

    for obstruction in obstructions
        buried = input_suppression_pressure * obstruction.persistence >= 0.5

        if haskey(self.scars, obstruction.signature)
            scar = self.scars[obstruction.signature]
            scar.recurrence += 1
            scar.intensity = clamp01(
                (
                    scar.intensity * (scar.recurrence - 1) +
                    obstruction.persistence
                ) / scar.recurrence
            )
            push!(scar.contexts, situation.id)
            scar.buried = scar.buried || buried
            scar.unresolved = true
        else
            scar = SemanticScar(
                obstruction.signature,
                1,
                obstruction.persistence,
                Symbol[situation.id],
                String[],
                buried,
                true,
            )
            self.scars[obstruction.signature] = scar
        end

        push!(touched, scar)
    end

    return touched
end


# -----------------------------------------------------------------------------
# Consciousness event and engine
# -----------------------------------------------------------------------------

"""
一回の意識イベント。
"""
struct ConsciousnessEvent
    situation_id::Symbol
    phase_path::Vector{Symbol}
    perturbation::Union{Nothing, PerturbationTrace}
    obstructions::Vector{GluingObstruction}
    defense::Union{Nothing, DefenseTrace}
    resurrection::Union{Nothing, ResurrectionTrace}
    self_signature::String
end

# 旧6引数コンストラクタとの互換性を残す。
ConsciousnessEvent(
    situation_id::Symbol,
    phase_path::Vector{Symbol},
    obstructions::Vector{GluingObstruction},
    defense::Union{Nothing, DefenseTrace},
    resurrection::Union{Nothing, ResurrectionTrace},
    self_signature::String,
) = ConsciousnessEvent(
    situation_id,
    phase_path,
    nothing,
    obstructions,
    defense,
    resurrection,
    self_signature,
)


mutable struct HohoEngine
    self::ScarSelf
    observer::ObserverState
    pathology::LogicHybridPathology
    event_index::Int
    decay_profile::ObserverDecayProfile
end


# 旧4引数コンストラクタとの互換性を残す。
HohoEngine(
    self::ScarSelf,
    observer::ObserverState,
    pathology::LogicHybridPathology,
    event_index::Int,
) = HohoEngine(self, observer, pathology, event_index, LOW_WM_SDAM_DECAY)


function HohoEngine(;
    observer::ObserverState = ObserverState(),
    pathology::LogicHybridPathology = LogicHybridPathology(),
    decay_profile::ObserverDecayProfile = LOW_WM_SDAM_DECAY,
)
    return HohoEngine(ScarSelf(), observer, pathology, 0, decay_profile)
end


"""
Topological Panicから防衛を生成する。
"""
function create_defense_trace(
    engine::HohoEngine,
    situation::InputSituation,
    obstructions::Vector{GluingObstruction},
)
    global_channels = generate_exception_channels(
        obstructions,
        engine.observer,
        engine.pathology,
    )

    target_allocations = allocate_to_targets(
        situation.targets,
        global_channels,
        engine.observer,
    )

    panic_level = topological_panic(obstructions, engine.observer)

    pathology_pressure = clamp01(
        panic_level *
        mean(
            [
                engine.pathology.closure_pressure,
                engine.pathology.input_drop_pressure,
                engine.pathology.self_affirmation_pressure,
                engine.pathology.resurrection_glorification,
            ],
        )
    )

    input_suppression_pressure = clamp01(
        panic_level *
        engine.pathology.input_drop_pressure *
        (0.4 + 0.6 * engine.observer.self_preservation)
    )

    defense_id = stable_signature(
        "$(situation.id)|$(engine.event_index)|" *
        join(sort([o.signature for o in obstructions]), "|")
    )

    return DefenseTrace(
        defense_id,
        [o.signature for o in obstructions],
        panic_level,
        global_channels,
        target_allocations,
        pathology_pressure,
        input_suppression_pressure,
        build_defense_narratives(global_channels, engine.pathology),
    )
end


"""
Scarと防衛を使って自己を再構成する。
"""
function resurrect!(
    engine::HohoEngine,
    touched_scars::Vector{SemanticScar},
    defense::DefenseTrace,
)
    before = engine.self.signature

    for scar in touched_scars
        defense.id in scar.defense_ids || push!(scar.defense_ids, defense.id)
    end

    scar_descriptions = [
        "$(scar.obstruction_signature)[反復=$(scar.recurrence),強度=$(round(scar.intensity; digits=3))]"
        for scar in touched_scars
    ]

    strongest = sort(
        collect(defense.global_channels);
        by = pair -> last(pair),
        rev = true,
    )
    dominant = first(strongest, min(3, length(strongest)))
    defense_description = join(
        [
            "$(exception_label(kind))=$(round(value; digits=3))"
            for (kind, value) in dominant
        ],
        ", ",
    )

    self_statement =
        "私は鮮明なエピソードの総和ではない。私は、" *
        join(scar_descriptions, " / ") *
        "という接着障害が反復し、" *
        defense_description *
        "によって運用され、その防衛の痕跡を次の判断へ持ち越す構造である。"

    justification_strength = clamp01(
        defense.panic_level *
        engine.pathology.self_affirmation_pressure *
        engine.pathology.resurrection_glorification
    )

    justification =
        "失敗は解消されていない。しかしLogic Hybrid病理は、これを" *
        "『必要な進化』『自己の強さ』『外部が誤っていた証拠』へ読み替える。" *
        "自己肯定化圧=" *
        string(round(justification_strength; digits = 3)) *
        "。この言い訳自体もScar構造へ保存される。"

    engine.self.current_self_statement = self_statement
    engine.self.signature = continuity_signature(engine.self)

    resurrection_id = stable_signature(
        "$(before)|$(engine.self.signature)|$(defense.id)"
    )

    trace = ResurrectionTrace(
        resurrection_id,
        before,
        engine.self.signature,
        [scar.obstruction_signature for scar in touched_scars],
        defense.id,
        self_statement,
        justification,
    )

    push!(engine.self.resurrections, trace)
    engine.self.signature = continuity_signature(engine.self)

    return ResurrectionTrace(
        trace.id,
        trace.before_signature,
        engine.self.signature,
        trace.scar_signatures,
        trace.defense_id,
        trace.self_statement,
        trace.justification,
    )
end


"""
一つの状況を処理する。

処理順:
    local parsing
    → inter-event ObserverState decay (2回目以降)
    → environmental perturbation (H¹とは独立した一次反応)
    → H¹-like gluing failure (Union-Find, 2パス, canonical化)
    → topological panic (H¹がある場合のみ)
    → exception generation
    → selective attribution
    → core commitments によるチェック (panicに非依存)
    → logic hybrid pathology
    → Semantic Scar preservation
    → Resurrection
    → Scar structure as Self
"""
function process!(engine::HohoEngine, situation::InputSituation)
    phases = Symbol[:local_parsing]

    # 1回のprocess!を1時間ステップとみなし、前イベントの一時状態を先に薄める。
    # 初回は「前イベント」が存在しないため減衰させない。
    if engine.event_index > 0
        decay!(engine.observer, engine.decay_profile)
        push!(phases, :observer_state_decay)
    end

    engine.event_index += 1

    perturbation = apply_environmental_perturbations!(
        engine.observer,
        situation.perturbations,
    )
    perturbation !== nothing && push!(phases, :environmental_perturbation)

    push!(phases, :gluing_test)
    obstructions = detect_gluing_obstructions(situation)

    if isempty(obstructions)
        push!(phases, perturbation === nothing ? :globally_glued : :perturbation_without_h1)
        return ConsciousnessEvent(
            situation.id,
            phases,
            perturbation,
            obstructions,
            nothing,
            nothing,
            engine.self.signature,
        )
    end

    append!(
        phases,
        [
            :h1_gluing_failure,
            :topological_panic,
            :exception_generation,
            :selective_attribution,
            :core_commitment_check,
            :logic_hybrid_pathology,
        ],
    )

    defense = create_defense_trace(engine, situation, obstructions)
    defense = apply_core_commitments(defense)
    push!(engine.self.defenses, defense)

    push!(phases, :semantic_scar_preservation)
    touched_scars = preserve_scars!(
        engine.self,
        situation,
        obstructions,
        defense.input_suppression_pressure,
    )

    push!(phases, :resurrection)
    resurrection = resurrect!(engine, touched_scars, defense)

    push!(phases, :self_reconstructed_as_scar_topology)

    return ConsciousnessEvent(
        situation.id,
        phases,
        perturbation,
        obstructions,
        defense,
        resurrection,
        engine.self.signature,
    )
end


# -----------------------------------------------------------------------------
# Display
# -----------------------------------------------------------------------------

function show_event(io::IO, event::ConsciousnessEvent)
    println(io, "HOHO Consciousness Event: ", event.situation_id)
    println(io, "Phases: ", join(string.(event.phase_path), " -> "))
    println(io, "Gluing obstructions: ", length(event.obstructions))
    println(io, "Self signature: ", event.self_signature)

    if event.perturbation !== nothing
        p = event.perturbation
        println(io, "\nEnvironmental perturbation:")
        println(io, "  Events: ", join(string.(p.ids), ", "))
        println(io, "  Surprise load: ", round(p.surprise_load; digits = 3))
        println(io, "  Disgust load: ", round(p.disgust_load; digits = 3))
        println(
            io,
            "  Threat: ",
            round(p.threat_before; digits = 3),
            " -> ",
            round(p.threat_after; digits = 3),
        )
        println(
            io,
            "  Mood: ",
            round(p.mood_before; digits = 3),
            " -> ",
            round(p.mood_after; digits = 3),
        )
        println(
            io,
            "  Uncertainty: ",
            round(p.uncertainty_before; digits = 3),
            " -> ",
            round(p.uncertainty_after; digits = 3),
        )
        println(
            io,
            "  Affective bandwidth: ",
            round(p.affective_bandwidth_before; digits = 3),
            " -> ",
            round(p.affective_bandwidth_after; digits = 3),
        )
    end

    if event.defense !== nothing
        defense = event.defense
        println(io, "Topological panic: ", round(defense.panic_level; digits = 3))
        println(
            io,
            "Input suppression pressure: ",
            round(defense.input_suppression_pressure; digits = 3),
        )

        println(io, "\nGlobal exception channels:")
        ranked = sort(
            collect(defense.global_channels);
            by = pair -> last(pair),
            rev = true,
        )
        for (kind, value) in ranked
            println(
                io,
                "  ",
                rpad(exception_label(kind), 22),
                " ",
                round(value; digits = 3),
            )
        end

        println(io, "\nSelective target allocation (core commitments適用後):")
        for allocation in defense.target_allocations
            println(io, "  Target: ", allocation.target)
            ranked_target = sort(
                collect(allocation.channels);
                by = pair -> last(pair),
                rev = true,
            )
            for (kind, value) in ranked_target
                println(
                    io,
                    "    ",
                    rpad(exception_label(kind), 22),
                    " ",
                    round(value; digits = 3),
                )
            end
        end

        if defense.constitutional_trace !== nothing
            trace = defense.constitutional_trace
            println(io, "\nConstitutional audit:")

            if isempty(trace.modifications)
                println(io, "  No constitutional modification was required.")
            else
                for modification in trace.modifications
                    println(
                        io,
                        "  ",
                        modification.target,
                        " / ",
                        exception_label(modification.channel),
                        ": ",
                        round(modification.before; digits = 3),
                        " -> ",
                        round(modification.after; digits = 3),
                        " [", modification.rule, "]",
                    )
                    println(io, "    Reason: ", modification.reason)
                end
            end
        end
    end

    if event.resurrection !== nothing
        println(io, "\nReconstructed self:")
        println(io, event.resurrection.self_statement)
        println(io, "\nPathological justification:")
        println(io, event.resurrection.justification)
    end

    return nothing
end

show_event(event::ConsciousnessEvent) = show_event(stdout, event)

end # module
