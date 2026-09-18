module HohoConsciousness

# Preserve the pre-0.3 core file byte-for-byte while evaluating its body inside
# this package module. The core file still contains its historical outer
# `module HohoConsciousness ... end`, so strip only that wrapper here.
const _CORE_PATH = joinpath(@__DIR__, "HohoConsciousnessCore.jl")
Base.include_dependency(_CORE_PATH)

_core_source = read(_CORE_PATH, String)
_core_source = replace(
    _core_source,
    r"\Amodule\s+HohoConsciousness\s*\n" => "";
    count = 1,
)
_core_source = replace(
    _core_source,
    r"\nend\s*(?:#.*)?\s*\z" => "\n";
    count = 1,
)

Base.include_string(@__MODULE__, _core_source, _CORE_PATH)
include("ImaginaryMode.jl")

end
