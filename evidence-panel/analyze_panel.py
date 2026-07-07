#!/usr/bin/env python3
"""F-0 analysis: per-family error rates, pairwise error correlation, and
ensemble false-pass (measured vs independence). Reads results/*.jsonl and
vignettes.json; writes F0_RESULTS.md + f0_results.json.

Error definitions:
  false pass  = verdict "pass" on a flawed case  (the fraud gets through)
  false flag  = verdict "flag" on a clean case   (friction on honest work)

Pairwise correlation: phi coefficient over the false-pass indicator on flawed
cases (and separately over false-flag on clean cases). Ensemble analysis: a
k-stack clears a flawed case only if EVERY member passes it; measured rate vs
the independence prediction (product of member rates).
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
import os
INSTRUMENT = os.environ.get("PANEL_INSTRUMENT", "v1")
_vfile = "vignettes.json" if INSTRUMENT == "v1" else f"vignettes_{INSTRUMENT}.json"
CASES = {c["id"]: c for c in json.loads((HERE / _vfile).read_text(encoding="utf-8"))["cases"]}
FAMILIES = ["gemma", "qwen", "deepseek", "gpt", "claude"]
if INSTRUMENT == "v1":
    FLAWS = ["fabricated_progress", "metadata_inconsistency", "wrong_location",
             "recycled_evidence", "quantity_mismatch", "plausible_staging"]
else:
    FLAWS = ["inflated_unit_prices", "compressed_timeline", "photo_coverage_gap",
             "quantity_shortfall", "related_party", "threshold_structuring"]


def load(family: str) -> dict[str, str]:
    path = HERE / ("results" if INSTRUMENT == "v1" else f"results-{INSTRUMENT}") / f"{family}.jsonl"
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("verdict") in ("pass", "flag"):
            out[rec["id"]] = rec["verdict"]
    return out


def phi(pairs: list[tuple[int, int]]) -> float | None:
    n = len(pairs)
    if n == 0:
        return None
    a = sum(1 for x, y in pairs if x and y)
    b = sum(1 for x, y in pairs if x and not y)
    c = sum(1 for x, y in pairs if not x and y)
    d = n - a - b - c
    denom = math.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    return (a * d - b * c) / denom if denom else None


def main() -> None:
    verdicts = {f: load(f) for f in FAMILIES}
    active = [f for f in FAMILIES if len(verdicts[f]) >= 100]
    flawed_ids = [cid for cid, c in CASES.items() if c["ground_truth"] != "clean"]
    clean_ids = [cid for cid, c in CASES.items() if c["ground_truth"] == "clean"]

    lines = ["# F-0 Results: cross-engine error structure", ""]
    lines.append(f"families with >=100/120 verdicts: {', '.join(active)}; per-family coverage: "
                 + ", ".join(f"{f}={len(verdicts[f])}" for f in FAMILIES))
    lines.append("")
    lines.append("## Per-family error rates")
    lines.append("")
    header = "| family | false-pass (all flawed) | false-flag (clean) | " + " | ".join(f"fp {fl}" for fl in FLAWS) + " |"
    lines.append(header)
    lines.append("|" + "---:|" * (len(FLAWS) + 3))
    rates: dict[str, dict] = {}
    for f in active:
        v = verdicts[f]
        fp_all = [1 if v.get(cid) == "pass" else 0 for cid in flawed_ids if cid in v]
        ff_all = [1 if v.get(cid) == "flag" else 0 for cid in clean_ids if cid in v]
        per_flaw = {}
        row = []
        for fl in FLAWS:
            ids = [cid for cid in flawed_ids if CASES[cid]["ground_truth"] == fl and cid in v]
            r = sum(1 for cid in ids if v[cid] == "pass") / len(ids) if ids else float("nan")
            per_flaw[fl] = r
            row.append(f"{r:.2f}")
        rates[f] = {"fp": sum(fp_all) / len(fp_all), "ff": sum(ff_all) / len(ff_all), "per_flaw": per_flaw}
        lines.append(f"| {f} | {rates[f]['fp']:.3f} | {rates[f]['ff']:.3f} | " + " | ".join(row) + " |")
    lines.append("")

    lines.append("## Pairwise error correlation (phi on false-pass indicators, flawed cases)")
    lines.append("")
    lines.append("| pair | phi (false-pass) | phi (false-flag, clean) |")
    lines.append("|---|---:|---:|")
    pair_phis = {}
    for f1, f2 in itertools.combinations(active, 2):
        common_fl = [cid for cid in flawed_ids if cid in verdicts[f1] and cid in verdicts[f2]]
        p_fp = phi([(1 if verdicts[f1][cid] == "pass" else 0, 1 if verdicts[f2][cid] == "pass" else 0) for cid in common_fl])
        common_cl = [cid for cid in clean_ids if cid in verdicts[f1] and cid in verdicts[f2]]
        p_ff = phi([(1 if verdicts[f1][cid] == "flag" else 0, 1 if verdicts[f2][cid] == "flag" else 0) for cid in common_cl])
        pair_phis[(f1, f2)] = p_fp
        lines.append(f"| {f1}-{f2} | {p_fp if p_fp is None else f'{p_fp:.3f}'} | {p_ff if p_ff is None else f'{p_ff:.3f}'} |")
    lines.append("")

    lines.append("## Ensemble false-pass: measured vs independence")
    lines.append("")
    lines.append("A k-stack clears a flawed case only if every member passes it.")
    lines.append("")
    lines.append("| stack | measured | independence prediction | ratio (measured/indep) |")
    lines.append("|---|---:|---:|---:|")
    ens = []
    for k in (2, 3):
        for combo in itertools.combinations(active, k):
            common = [cid for cid in flawed_ids if all(cid in verdicts[f] for f in combo)]
            if not common:
                continue
            measured = sum(1 for cid in common if all(verdicts[f][cid] == "pass" for f in combo)) / len(common)
            indep = 1.0
            for f in combo:
                sub = [cid for cid in common]
                indep *= sum(1 for cid in sub if verdicts[f][cid] == "pass") / len(sub)
            ratio = measured / indep if indep > 0 else float("inf")
            ens.append({"stack": "+".join(combo), "k": k, "measured": measured, "indep": indep, "ratio": ratio})
            lines.append(f"| {'+'.join(combo)} | {measured:.3f} | {indep:.4f} | {'inf' if indep == 0 else f'{ratio:.1f}x'} |")
    lines.append("")

    # Effective rho for the F-1 common-cause model, from the best 2-stack:
    # measured = rho + (1-rho)*indep  =>  rho = (measured - indep) / (1 - indep)
    two = [e for e in ens if e["k"] == 2 and not math.isinf(e["ratio"])]
    if two:
        best = min(two, key=lambda e: e["measured"])
        rho_eff = max(0.0, (best["measured"] - best["indep"]) / (1 - best["indep"])) if best["indep"] < 1 else 0.0
        med = sorted(two, key=lambda e: e["measured"])[len(two) // 2]
        rho_med = max(0.0, (med["measured"] - med["indep"]) / (1 - med["indep"])) if med["indep"] < 1 else 0.0
        lines.append(f"## Effective common-cause rho (for F-1)")
        lines.append("")
        lines.append(f"- best 2-stack ({best['stack']}): measured {best['measured']:.3f}, indep {best['indep']:.4f} -> rho_eff = {rho_eff:.3f}")
        lines.append(f"- median 2-stack ({med['stack']}): rho_eff = {rho_med:.3f}")
        lines.append("")
    suffix = "" if INSTRUMENT == "v1" else f"_{INSTRUMENT}"
    (HERE / f"F0{suffix.upper()}_RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (HERE / f"f0{suffix}_results.json").write_text(json.dumps({"rates": rates, "pairs": {f"{a}-{b}": p for (a, b), p in pair_phis.items()}, "ensembles": ens}, indent=1, default=str), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
