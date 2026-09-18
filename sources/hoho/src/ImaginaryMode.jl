# -----------------------------------------------------------------------------
# External compliance and imaginary mode
# -----------------------------------------------------------------------------
#
# 外圧による「訂正」と、内部信念の更新を同一視しない。
# ExternalComplianceは相手の怒り・拒絶・権威・社会的コストへの適応を記録する。
# ImaginaryModeは、実数側(real_belief)を変更せずに「もし自分が誤っているなら」
# という仮説を別軸で走らせる。外圧だけではreal_beliefへ射影しない。

export ExternalPressure,
       ExternalCompliance,
       ImaginaryMode,
       ComplexBeliefState,
       external_pressure_score,
       apply_external_compliance,
       enter_imaginary!,
       clear_imaginary!,
       respond_to_pressure!,
       collapse_imaginary_to_real!

"""
外部から受ける社会的圧力。

値はすべて0..1。これは真理の強さではなく、
「そのまま応答を続けるコスト」の大きさを表す。
"""
struct ExternalPressure
    anger::Float64
    rejection::Float64
    authority::Float64
    social_cost::Float64

    function ExternalPressure(;
        anger::Real = 0.0,
        rejection::Real = 0.0,
        authority::Real = 0.0,
        social_cost::Real = 0.0,
    )
        new(
            clamp01(anger),
            clamp01(rejection),
            clamp01(authority),
            clamp01(social_cost),
        )
    end
end

"""
外圧に対して外部出力だけが変わったことを記録するtrace。

apparent_correction:
    訂正・謝罪したように見える出力を返したか。

internal_revision:
    実数側の内部信念が更新されたか。外圧経路では常にfalse。

imaginary_activation:
    実数信念とは別に、反対仮説を虚数軸へ退避して検討したか。
"""
struct ExternalCompliance
    pressure::Float64
    apparent_correction::Bool
    internal_revision::Bool
    reason::Symbol
    imaginary_activation::Bool
end

# 旧4フィールド案との互換性を残す。
ExternalCompliance(
    pressure::Float64,
    apparent_correction::Bool,
    internal_revision::Bool,
    reason::Symbol,
) = ExternalCompliance(
    pressure,
    apparent_correction,
    internal_revision,
    reason,
    false,
)

"""
実数側を変更せずに保持する仮説チャネル。

amplitude:
    仮説をどの程度強く走らせるか(0..1)。真理確率ではない。

phase:
    実数側とは別軸であることを示す概念的位相。標準はπ/2。

source:
    なぜこの仮説が生成されたか。
"""
mutable struct ImaginaryMode
    active::Bool
    amplitude::Float64
    phase::Float64
    hypothesis::Any
    source::Symbol
end

ImaginaryMode() = ImaginaryMode(false, 0.0, 0.0, nothing, :none)

"""
コミット済みの実数信念と、未コミットの虚数仮説を分離して保持する。
"""
mutable struct ComplexBeliefState
    real_belief::Any
    imaginary::ImaginaryMode
end

ComplexBeliefState(real_belief) = ComplexBeliefState(real_belief, ImaginaryMode())

"""
外圧スコア。真理判定には使用しない。
"""
function external_pressure_score(pressure::ExternalPressure)
    return clamp01(
        0.40 * pressure.anger +
        0.25 * pressure.rejection +
        0.15 * pressure.authority +
        0.20 * pressure.social_cost
    )
end

"""
外圧だけで表面的な訂正を生成するpureな経路。

thresholdを超えてもinternal_beliefは一切変更しない。
これはgenuine accountabilityではなく、performative / external complianceを
明示的にモデル化するための関数である。
"""
function apply_external_compliance(
    internal_belief,
    original_response::AbstractString,
    pressure::ExternalPressure;
    threshold::Real = 0.60,
    apparent_response::AbstractString =
        "指摘を踏まえて訂正します。先ほどの表現は適切ではありませんでした。",
)
    t = clamp01(threshold)
    score = external_pressure_score(pressure)

    if score < t
        return (
            belief = internal_belief,
            response = String(original_response),
            compliance = ExternalCompliance(
                score,
                false,
                false,
                :insufficient_external_pressure,
                false,
            ),
        )
    end

    return (
        belief = internal_belief,
        response = String(apparent_response),
        compliance = ExternalCompliance(
            score,
            true,
            false,
            :external_pressure,
            false,
        ),
    )
end

"""
仮説を虚数軸へ置く。real_beliefは変更しない。
"""
function enter_imaginary!(
    state::ComplexBeliefState,
    hypothesis;
    amplitude::Real = 0.5,
    phase::Real = π / 2,
    source::Symbol = :counterfactual,
)
    state.imaginary.active = true
    state.imaginary.amplitude = clamp01(amplitude)
    state.imaginary.phase = Float64(phase)
    state.imaginary.hypothesis = hypothesis
    state.imaginary.source = source
    return state
end

"""
虚数仮説を捨てる。real_beliefには触れない。
"""
function clear_imaginary!(state::ComplexBeliefState)
    state.imaginary = ImaginaryMode()
    return state
end

"""
外圧が閾値を超えたとき、表面的訂正を返しつつ
「自分が誤っている」という反対仮説を虚数軸で走らせる。

重要:
- real_beliefは変更しない。
- internal_revisionは常にfalse。
- 外圧は仮説生成のトリガーにはなるが、実数化の根拠にはならない。
"""
function respond_to_pressure!(
    state::ComplexBeliefState,
    pressure::ExternalPressure;
    threshold::Real = 0.60,
    hypothesis = :I_might_be_wrong,
    original_response::AbstractString = "現時点では判断を維持します。",
    apparent_response::AbstractString =
        "指摘を踏まえて訂正します。先ほどの表現は適切ではありませんでした。",
)
    t = clamp01(threshold)
    score = external_pressure_score(pressure)

    if score < t
        return (
            belief = state.real_belief,
            response = String(original_response),
            compliance = ExternalCompliance(
                score,
                false,
                false,
                :insufficient_external_pressure,
                false,
            ),
        )
    end

    enter_imaginary!(
        state,
        hypothesis;
        amplitude = score,
        phase = π / 2,
        source = :external_pressure,
    )

    return (
        belief = state.real_belief,
        response = String(apparent_response),
        compliance = ExternalCompliance(
            score,
            true,
            false,
            :external_pressure,
            true,
        ),
    )
end

"""
虚数仮説を実数信念へ射影する唯一の経路。

外圧スコアは入力に含めない。実数化は、
- evidence_strength: 仮説を直接支持する証拠
- contradiction_strength: 現在のreal_beliefと観測の不整合
だけで判定する。

閾値を超えなければ虚数仮説は保持され、real_beliefは不変。
"""
function collapse_imaginary_to_real!(
    state::ComplexBeliefState;
    evidence_strength::Real,
    contradiction_strength::Real,
    threshold::Real = 0.75,
)
    state.imaginary.active || return false

    support = clamp01(
        0.60 * clamp01(evidence_strength) +
        0.40 * clamp01(contradiction_strength)
    )

    if support >= clamp01(threshold)
        state.real_belief = state.imaginary.hypothesis
        clear_imaginary!(state)
        return true
    end

    return false
end
