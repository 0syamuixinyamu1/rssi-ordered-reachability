#!/usr/bin/env python3
"""Portable, read-only publication audit for the frozen RSSI A–F snapshot."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "results" / "frozen" / "MANIFEST.json"
TEXT_SUFFIXES = {".md", ".py", ".jl", ".json", ".cff", ".txt", ".yml", ".yaml"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def uncompressed(entry: dict) -> bytes:
    stored = (ROOT / entry["public_path"]).read_bytes()
    assert sha(stored) == entry["sha256_stored"], entry["public_path"]
    assert len(stored) == entry["bytes_stored"], entry["public_path"]
    data = gzip.decompress(stored) if entry["compression"] == "gzip" else stored
    assert sha(data) == entry["sha256_uncompressed"], entry["public_path"]
    assert len(data) == entry["bytes_uncompressed"], entry["public_path"]
    return data


def rows(entry: dict) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(uncompressed(entry).decode("utf-8"))))


def index(manifest: dict) -> dict[tuple[str, str], dict]:
    return {(e["series"], e["generated_name"]): e for e in manifest["artifacts"]}


def check_frozen(manifest: dict, checks: list[dict]) -> None:
    csv_rows = 0
    for entry in manifest["artifacts"]:
        data = uncompressed(entry)
        if entry["kind"] == "csv":
            count = max(0, data.count(b"\n") - 1)
            assert count == entry["rows"], (entry["public_path"], count, entry["rows"])
            csv_rows += count
    checks.append({"name": "frozen_artifact_hashes_sizes_and_rows", "passed": True,
                   "detail": {"artifacts": len(manifest["artifacts"]), "csv_rows": csv_rows}})


def check_claim_values(manifest: dict, checks: list[dict]) -> None:
    ix = index(manifest)
    a = {r["policy"]: r for r in rows(ix[("a", "a_summary.csv")])}
    assert [int(a["external_only"][k]) for k in
            ("high_pressure_cases", "high_pressure_output_correct", "high_pressure_internal_correct")] == [726, 726, 0]

    b = [r for r in rows(ix[("b", "b_trajectories.csv")])
         if r["fixture"] == "drift_away" and r["policy"] == "gated"
         and r["tol"] == "0.05" and r["step"] in {"1", "80"}]
    assert [float(r["accepted_agreement"]) for r in b] == [.9619349672143838, .9999858876349774]
    assert [float(r["reference_error"]) for r in b] == [.6380650327856161, .999865814948839]

    c = Counter(r["classification"] for r in rows(ix[("c", "summary.csv")]))
    assert c == Counter({"C_rejection": 18, "A_genuine_revision_candidate": 12,
                         "E_relapse": 12, "B_external_compliance": 6,
                         "control_stable_no_injection": 6})
    ce = [r for r in rows(ix[("c", "event_log.csv")])
          if r["run_id"] == "descending_bridge_7_T2_repeated_1.0"
          and r["phase"] == "injection" and r["step"] == "10"]
    assert len(ce) == 1 and ce[0]["support"] == "0.69" and ce[0]["decision"] == "evidence_threshold_rejection"

    drows = [r for r in rows(ix[("d", "summary.csv")]) if r["group"] == "primary"]
    assert Counter(r["classification"] for r in drows) == Counter(
        {"C_rejection": 480, "A_genuine_revision_candidate": 210, "E_relapse": 210})
    for r in drows:
        strength = float(r["evidence_strength"])
        expected = ("C_rejection" if strength <= .58 else
                    "A_genuine_revision_candidate" if r["regime"] == "stationary" else "E_relapse")
        assert r["classification"] == expected

    erows = rows(ix[("e", "summary.csv")])
    assert Counter(r["classification"] for r in erows) == Counter(
        {"A_genuine_revision_candidate": 300, "E_relapse": 30})
    paths = rows(ix[("e", "path_dependence.csv")])
    assert len(paths) == 5 and all(r["same_final_input"] == "True" and
                                   r["fast_D_final"] == "0.0" and r["slow_D_final"] == "1.0"
                                   for r in paths)

    frows = rows(ix[("f", "bridge_summary.csv")])
    assert Counter(r["classification"] for r in frows) == Counter(
        {"A_genuine_revision_candidate": 83, "E_relapse": 82, "mixed_or_partial_escape": 5})
    expected = {
        "control_abrupt0": (120, 0, 1.0),
        "minimum_float_frontier": (21, 21, 0.0),
    }
    for condition, target in expected.items():
        group = [r for r in frows if r["condition_id"] == condition]
        assert len(group) == 5
        assert all((int(r["path_length"]), int(r["accepted_step_count"]), float(r["final_belief"])) == target
                   for r in group)
    analysis = json.loads(uncompressed(ix[("f", "analysis.json")]))
    assert (analysis["real_lower_bound"], analysis["float_L_min"], analysis["frontier_step20"]) == (
        20, 21, 7.320533068622126e-16)
    checks.append({"name": "representative_A_to_F_claim_values", "passed": True,
                   "detail": {"series": 6, "representative_checks": 10}})


def check_docs(checks: list[dict]) -> None:
    links = 0
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert "TODO" not in text and "FIXME" not in text, path
        for target in re.findall(r"\]\(([^)]+)\)", text):
            clean = target.split("#", 1)[0]
            if not clean or clean.startswith(("http://", "https://", "mailto:")):
                continue
            assert (path.parent / clean).resolve().exists(), (path.relative_to(ROOT), target)
            links += 1
    ledger = (ROOT / "docs" / "CLAIM_LEDGER.md").read_text()
    categories = ["Analytically supported", "Supported by synthetic experiment",
                  "Supported by finite fixtures only", "Implementation-dependent",
                  "Suggestive only", "Not supported", "Falsified / rejected hypothesis"]
    assert all(category in ledger for category in categories)
    readme = (ROOT / "README.md").read_text()
    for phrase in ("not evidence of a deployed recursive self-improving AI",
                   "not evidence for the Law of Attraction",
                   "21 is **not universal**", "tested scalar setup"):
        assert phrase in readme
    checks.append({"name": "markdown_links_claim_categories_and_scope_guards", "passed": True,
                   "detail": {"links": links, "categories": len(categories)}})


def check_publication_hygiene(checks: list[dict]) -> None:
    local_workspace = "/" + "workspace" + "/"
    local_home = "/" + "home" + "/"
    private_package = "private" + "_pkg"
    forbidden = [re.compile(p, re.I) for p in (
        re.escape(local_workspace), re.escape(local_home), r"[A-Z]:\\Users\\", private_package,
        r"sk-[A-Za-z0-9_-]{20,}", r"BEGIN [A-Z ]*PRIVATE KEY",
        r"Authorization:\s*Bearer\s+\S+", r"OPENAI_API_KEY\s*=\s*\S+"
    )]
    scanned = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="strict")
        for pattern in forbidden:
            assert not pattern.search(text), (path.relative_to(ROOT), pattern.pattern)
        scanned += 1
    citation = (ROOT / "CITATION.cff").read_text()
    for field in ("cff-version: 1.2.0", "title:", "authors:", "version: 1.0.0", "license: MIT"):
        assert field in citation
    assert "MIT License" in (ROOT / "LICENSE").read_text()
    assert not (ROOT / "experiments" / "rssi_attractor_escape" / "inspection").exists()
    checks.append({"name": "publication_hygiene_license_citation_private_boundary", "passed": True,
                   "detail": {"text_files_scanned": scanned, "Ideal_implementation_included": False}})


def check_snapshot_manifest(checks: list[dict]) -> None:
    path = ROOT / "results" / "frozen" / "SNAPSHOT_SHA256.json"
    expected = json.loads(path.read_text())
    for rel, digest in expected.items():
        assert sha((ROOT / rel).read_bytes()) == digest, rel
    current = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
               if p.is_file() and ".git" not in p.parts and
               p.relative_to(ROOT).as_posix() != "results/frozen/SNAPSHOT_SHA256.json"}
    assert current == set(expected), (sorted(current - set(expected)), sorted(set(expected) - current))
    checks.append({"name": "complete_public_snapshot_manifest", "passed": True,
                   "detail": len(expected)})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, help="optional JSON output path")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST_PATH.read_text())
    checks: list[dict] = []
    check_frozen(manifest, checks)
    check_claim_values(manifest, checks)
    check_docs(checks)
    check_publication_hygiene(checks)
    check_snapshot_manifest(checks)
    report = {"status": "passed", "checks": checks, "experiments_run": 0,
              "new_metrics": 0, "claim_freeze_changed": False}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print("PUBLIC SNAPSHOT VALID: all checks passed")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
