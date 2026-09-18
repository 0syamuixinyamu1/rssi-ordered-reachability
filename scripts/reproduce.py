#!/usr/bin/env python3
"""Rerun frozen A–F generators and byte-compare their public CSV/JSON outputs.

This wrapper adds no experiment, parameter, metric, or classification. It runs
the checked-in generators in temporary output directories and compares them to
the immutable publication manifest.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "results" / "frozen" / "MANIFEST.json"
VALID = tuple("abcdef")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def frozen_bytes(entry: dict) -> bytes:
    data = (ROOT / entry["public_path"]).read_bytes()
    return gzip.decompress(data) if entry["compression"] == "gzip" else data


def compare(series: str, output: Path, entries: list[dict]) -> list[dict]:
    checked = []
    for entry in entries:
        if entry["series"] != series or not entry.get("reproduce_compare"):
            continue
        generated = output / entry["generated_name"]
        if not generated.is_file():
            raise AssertionError(f"{series}: missing regenerated file {generated.name}")
        actual = generated.read_bytes()
        expected = frozen_bytes(entry)
        if actual != expected:
            raise AssertionError(
                f"{series}: byte mismatch for {generated.name}: "
                f"generated={sha(actual)} frozen={sha(expected)}"
            )
        checked.append({"file": generated.name, "sha256": sha(actual), "bytes": len(actual)})
    if not checked:
        raise AssertionError(f"{series}: manifest has no comparable outputs")
    return checked


def run(cmd: list[str], cwd: Path, env: dict[str, str]) -> None:
    print("RUN", " ".join(str(x) for x in cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def prepare_ab(work: Path) -> Path:
    target = work / "ab"
    target.mkdir(parents=True)
    shutil.copy2(ROOT / "run_experiments.py", target / "run_experiments.py")
    shutil.copy2(ROOT / "experiments" / "exp_a" / "PROTOCOL_JA.md",
                 target / "PROTOCOL_JA.md")
    shutil.copytree(ROOT / "sources", target / "sources")
    return target


def parse_series(raw: str) -> list[str]:
    if raw.strip().lower() == "all":
        return list(VALID)
    values = []
    for part in raw.split(","):
        value = part.strip().lower()
        if value and value not in values:
            values.append(value)
    invalid = sorted(set(values) - set(VALID))
    if invalid or not values:
        raise argparse.ArgumentTypeError("series must be all or a comma list from a,b,c,d,e,f")
    return values


def execute(base: Path, selected: list[str], entries: list[dict]) -> dict:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result: dict[str, list[dict]] = {}

    if "a" in selected or "b" in selected:
        ab = prepare_ab(base)
        run([sys.executable, "run_experiments.py"], ab, env)
        if "a" in selected:
            result["a"] = compare("a", ab / "results", entries)
        if "b" in selected:
            result["b"] = compare("b", ab / "results", entries)

    runners = {
        "c": ROOT / "experiments" / "rssi_attractor_escape" / "run_experiment.py",
        "d": ROOT / "experiments" / "rssi_attractor_escape_boundary" / "run_experiment.py",
        "e": ROOT / "experiments" / "rssi_recapture_dynamics" / "run_experiment.py",
        "f": ROOT / "experiments" / "rssi_admissible_bridge" / "run_experiment.py",
    }
    for series in "cdef":
        if series not in selected:
            continue
        out = base / f"exp_{series}"
        out.mkdir(parents=True)
        run([sys.executable, str(runners[series]), "--output-dir", str(out)], ROOT, env)
        if series == "f":
            analyzer = ROOT / "experiments" / "rssi_admissible_bridge" / "analyze_reachability.py"
            run([sys.executable, str(analyzer), "--output-dir", str(out)], ROOT, env)
        result[series] = compare(series, out, entries)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--series", default="all", type=parse_series,
                        help="all or comma-separated a,b,c,d,e,f")
    parser.add_argument("--output-dir", type=Path,
                        help="retain regenerated files here; default uses a temporary directory")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    selected = args.series if isinstance(args.series, list) else parse_series(args.series)

    if args.output_dir:
        base = args.output_dir.resolve()
        if base.exists() and any(base.iterdir()):
            parser.error("--output-dir must be absent or empty")
        base.mkdir(parents=True, exist_ok=True)
        result = execute(base, selected, manifest["artifacts"])
        retained = str(base)
    else:
        with tempfile.TemporaryDirectory(prefix="rssi-reproduce-") as tmp:
            result = execute(Path(tmp), selected, manifest["artifacts"])
        retained = None

    print(json.dumps({"status": "reproduced", "series": selected,
                      "matched_files": sum(map(len, result.values())),
                      "outputs_retained": retained, "details": result}, indent=2))


if __name__ == "__main__":
    main()
