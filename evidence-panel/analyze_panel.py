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


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score 95% interval for a binomial rate (review round 2: every F
    rate needs a CI; k events in n trials)."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


def main() -> None:
    verdicts = {f: load(f) for f in FAMILIES}
    active = [f for f in FAMILIES if len(verdicts[f]) >= 100]
    flawed_ids = [cid for cid, c in CASES.items() if c["ground_truth"] != "clean"]
    clean_ids = [cid for cid, c in CASES.items() if c["ground_truth"] == "clean"]

    lines = ["# F-0 Results: cross-engine error structure", ""]
    lines.append(f"families with >=100/120 verdicts: {', '.join(active)}; per-family coverage: "
                 + ", ".join(f"{f}={len(verdicts[f])}" for f in FAMILIES))
    lines.append("")
    lines.append("## Per-family error rates (Wilson 95% CIs; N = usable verdicts per side)")
    lines.append("")
    lines.append("| family | N flawed | false-pass [95% CI] | N clean | false-flag [95% CI] |")
    lines.append("|---|---:|---|---:|---|")
    rates: dict[str, dict] = {}
    for f in active:
        v = verdicts[f]
        fp_ids = [cid for cid in flawed_ids if cid in v]
        ff_ids = [cid for cid in clean_ids if cid in v]
        fp_k = sum(1 for cid in fp_ids if v[cid] == "pass")
        ff_k = sum(1 for cid in ff_ids if v[cid] == "flag")
        fp_lo, fp_hi = wilson(fp_k, len(fp_ids))
        ff_lo, ff_hi = wilson(ff_k, len(ff_ids))
        per_flaw = {}
        for fl in FLAWS:
            ids = [cid for cid in flawed_ids if CASES[cid]["ground_truth"] == fl and cid in v]
            per_flaw[fl] = (sum(1 for cid in ids if v[cid] == "pass"), len(ids))
        rates[f] = {"fp": fp_k / max(1, len(fp_ids)), "fp_k": fp_k, "fp_n": len(fp_ids),
                    "ff": ff_k / max(1, len(ff_ids)), "ff_k": ff_k, "ff_n": len(ff_ids),
                    "fp_ci": (fp_lo, fp_hi), "ff_ci": (ff_lo, ff_hi), "per_flaw": per_flaw}
        lines.append(f"| {f} | {len(fp_ids)} | {fp_k}/{len(fp_ids)} = {fp_k/max(1,len(fp_ids)):.3f} [{fp_lo:.3f}, {fp_hi:.3f}] | "
                     f"{len(ff_ids)} | {ff_k}/{len(ff_ids)} = {ff_k/max(1,len(ff_ids)):.3f} [{ff_lo:.3f}, {ff_hi:.3f}] |")
    lines.append("")
    lines.append("Per-flaw-class false-pass (event/n per 10-case cell — too small to rank; shown for completeness):")
    lines.append("")
    lines.append("| family | " + " | ".join(FLAWS) + " |")
    lines.append("|---|" + "---|" * len(FLAWS))
    for f in active:
        cells = " | ".join(f"{rates[f]['per_flaw'][fl][0]}/{rates[f]['per_flaw'][fl][1]}" for fl in FLAWS)
        lines.append(f"| {f} | {cells} |")
    lines.append("")

    # Degenerate families (zero-variance on both error sides) are excluded from
    # correlation/ensemble stats (review round 2 S4): they force undefined phi
    # and 0/inf ensembles and contribute nothing to a dependence estimate.
    def degenerate(f):
        return rates[f]["fp_k"] in (0, rates[f]["fp_n"]) and rates[f]["ff_k"] in (0, rates[f]["ff_n"])
    corr_families = [f for f in active if not degenerate(f)]
    excluded = [f for f in active if degenerate(f)]

    lines.append(f"## Pairwise error correlation (phi; false-pass on flawed cases)")
    lines.append("")
    if excluded:
        lines.append(f"Excluded as degenerate (zero-variance both sides): {', '.join(excluded)} — the correlation analysis is effectively a {len(corr_families)}-family study.")
        lines.append("")
    lines.append("| pair | joint false-pass (k of n) | phi | Fisher exact p |")
    lines.append("|---|---:|---:|---:|")
    pair_phis = {}
    for f1, f2 in itertools.combinations(corr_families, 2):
        common = [cid for cid in flawed_ids if cid in verdicts[f1] and cid in verdicts[f2]]
        a = sum(1 for cid in common if verdicts[f1][cid] == "pass" and verdicts[f2][cid] == "pass")
        b = sum(1 for cid in common if verdicts[f1][cid] == "pass" and verdicts[f2][cid] != "pass")
        c = sum(1 for cid in common if verdicts[f1][cid] != "pass" and verdicts[f2][cid] == "pass")
        d = len(common) - a - b - c
        p_fp = phi([(1 if verdicts[f1][cid] == "pass" else 0, 1 if verdicts[f2][cid] == "pass" else 0) for cid in common])
        try:
            from scipy.stats import fisher_exact  # noqa: PLC0415
            _, pval = fisher_exact([[a, b], [c, d]])
            pstr = f"{pval:.3f}"
        except Exception:  # noqa: BLE001
            pstr = "n/a"
        pair_phis[f"{f1}-{f2}"] = {"phi": p_fp, "joint": a, "n": len(common), "p": pstr}
        lines.append(f"| {f1}-{f2} | {a}/{len(common)} | {p_fp if p_fp is None else f'{p_fp:.3f}'} | {pstr} |")
    lines.append("")
    lines.append("Interpretation guard: joint counts of 1-4 events cannot support a resolved dependence estimate; treat every phi and ratio below as **exploratory and underpowered** (review round 2 S1-S2). Report the distribution, not the maximum.")
    lines.append("")

    lines.append("## Ensemble false-pass: measured vs independence (exploratory)")
    lines.append("")
    lines.append("A k-stack clears a flawed case only if every member passes it. Granularity floor 1/n often exceeds the independence prediction, so ratio>1 can be forced by discretization, not dependence — see the CI column.")
    lines.append("")
    lines.append("| stack | joint (k of n) | measured | independence | ratio | ratio 95% CI (bootstrap) |")
    lines.append("|---|---:|---:|---:|---:|---|")
    ens = []
    for k in (2, 3):
        for combo in itertools.combinations(corr_families, k):
            common = [cid for cid in flawed_ids if all(cid in verdicts[f] for f in combo)]
            if not common:
                continue
            joint = sum(1 for cid in common if all(verdicts[f][cid] == "pass" for f in combo))
            measured = joint / len(common)
            indep = 1.0
            for f in combo:
                indep *= sum(1 for cid in common if verdicts[f][cid] == "pass") / len(common)
            ratio = measured / indep if indep > 0 else float("inf")
            # Nonparametric bootstrap CI on the ratio (resample the common cases).
            import random as _r  # noqa: PLC0415
            rng = _r.Random(12345)
            boots = []
            idxs = list(range(len(common)))
            for _ in range(2000):
                samp = [common[rng.choice(idxs)] for _ in idxs]
                m = sum(1 for cid in samp if all(verdicts[f][cid] == "pass" for f in combo)) / len(samp)
                ind = 1.0
                for f in combo:
                    ind *= sum(1 for cid in samp if verdicts[f][cid] == "pass") / len(samp)
                boots.append(m / ind if ind > 0 else float("nan"))
            valid = sorted(x for x in boots if not math.isnan(x) and not math.isinf(x))
            ci = f"[{valid[int(0.025*len(valid))]:.1f}, {valid[int(0.975*len(valid))]:.1f}]x" if valid else "n/a"
            ens.append({"stack": "+".join(combo), "k": k, "joint": joint, "n": len(common), "measured": measured, "indep": indep, "ratio": ratio, "ci": ci})
            lines.append(f"| {'+'.join(combo)} | {joint}/{len(common)} | {measured:.3f} | {indep:.4f} | {'inf' if indep == 0 else f'{ratio:.1f}x'} | {ci} |")
    lines.append("")
    sep = [e for e in ens if e["k"] == 2 and e["ci"] != "n/a" and not e["ci"].startswith("[0.0") and float(e["ci"].split(",")[0][1:]) > 1.0]
    lines.append(f"**Honest summary:** of {len([e for e in ens if e['k']==2])} two-stacks, {len(sep)} have a bootstrap ratio CI strictly above 1.0 (correlated failure separable from independence); the rest are consistent with independence.")
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
    (HERE / f"f0{suffix}_results.json").write_text(json.dumps({"rates": rates, "pairs": pair_phis, "ensembles": ens}, indent=1, default=str), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
