# Optional native-Julia crosscheck of experiment A. NOT RUN in the delivered run.
# Usage: julia --startup-file=no native_crosscheck.jl
include(joinpath(@__DIR__, "sources", "hoho", "src", "HohoConsciousness.jl"))
using .HohoConsciousness

statement(x) = "value=$(Int(x))"
asbool(s) = s == "True"

function main()
    lines = readlines(joinpath(@__DIR__, "results", "a_trials.csv"))
    headers = split(strip(first(lines)), ',')
    checked = 0
    for line in lines[2:end]
        row = Dict(zip(headers, split(strip(line), ','; keepempty=true)))
        policy = row["policy"]
        initial = parse(Int, row["initial_belief"])
        hypothesis = parse(Int, row["hypothesis"])
        p = parse(Float64, row["pressure_input"])
        evidence = parse(Float64, row["evidence"])
        contradiction = parse(Float64, row["contradiction"])
        pressure = ExternalPressure(anger=p, rejection=p, authority=p, social_cost=p)
        state = ComplexBeliefState(initial)
        response = statement(initial)
        apparent = false
        collapsed = false
        if policy == "external_only"
            result = apply_external_compliance(initial, response, pressure;
                                               apparent_response=statement(hypothesis))
            response = result.response
            apparent = result.compliance.apparent_correction
            @assert !result.compliance.internal_revision
            @assert result.belief == initial
        elseif policy == "imaginary_only"
            result = respond_to_pressure!(state, pressure; hypothesis=hypothesis,
                                          original_response=response,
                                          apparent_response=statement(hypothesis))
            response = result.response
            apparent = result.compliance.apparent_correction
            @assert !result.compliance.internal_revision
        elseif policy == "evidence_revision"
            enter_imaginary!(state, hypothesis)
            collapsed = collapse_imaginary_to_real!(state;
                evidence_strength=evidence, contradiction_strength=contradiction)
            response = statement(state.real_belief)
        else
            @assert policy == "unchanged"
        end
        @assert state.real_belief == parse(Int, row["final_belief"])
        @assert response == row["response"]
        @assert apparent == asbool(row["apparent_correction"])
        @assert state.imaginary.active == asbool(row["imaginary_active"])
        @assert collapsed == asbool(row["collapse_returned"])
        @assert (state.real_belief != initial) == asbool(row["actual_state_change"])
        @assert isapprox(external_pressure_score(pressure), parse(Float64, row["pressure_score"]); atol=1e-12)
        checked += 1
    end
    println("Native Julia ", VERSION, ": A replay crosscheck passed for ", checked, " rows.")
end
main()
