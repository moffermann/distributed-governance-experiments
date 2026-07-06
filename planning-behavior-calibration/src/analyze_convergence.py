"""Convergence and composition analysis for a large panel run.

Answers two questions about a population-weighted panel:

1. Convergence: do pooled means stabilize as N grows? (means over growing
   shuffled subsets, plus the standard error at full N)
2. Composition vs scale: how much of the difference against a smaller
   equal-weight panel comes from the new archetype mix rather than sample size?
   (computed by restricting the large panel to the reference archetypes and
   re-pooling them with equal archetype weights)

Usage:
    python src/analyze_convergence.py --panel results/<big_run> --reference results/<small_run>
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

KEY_FIELDS = [
    ("platform_behavior", "platform_trial_probability"),
    ("platform_behavior", "monthly_platform_use_probability"),
    ("citizen_behavior", "direct_planning_participation_probability"),
    ("citizen_behavior", "delegation_probability"),
    ("delegate_behavior", "would_accept_delegation"),
    ("delegate_behavior", "delegate_platform_use_rate"),
    ("delegate_behavior", "delegate_planning_coverage"),
]


def load_responses(panel_dir: Path) -> list[dict]:
    lines = (panel_dir / "normalized_responses.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def field_values(responses: list[dict], section: str, field: str) -> list[float]:
    return [r[section][field] for r in responses]


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def se(xs: list[float]) -> float:
    m = mean(xs)
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1) if len(xs) > 1 else 0.0
    return math.sqrt(var / len(xs))


def equal_weight_pool(responses: list[dict], section: str, field: str, archetypes: list[str]) -> float:
    """Pool restricted to given archetypes, weighting each archetype equally."""
    per_arch = []
    for a in archetypes:
        vals = [r[section][field] for r in responses if r["archetype_id"] == a]
        if vals:
            per_arch.append(mean(vals))
    return mean(per_arch) if per_arch else float("nan")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convergence/composition analysis for a panel run.")
    parser.add_argument("--panel", required=True, help="Large panel results directory.")
    parser.add_argument("--reference", default=None, help="Smaller reference panel directory (e.g., the n=90 equal-weight run).")
    parser.add_argument("--subset-sizes", nargs="*", type=int, default=[100, 250, 500, 750, 1000])
    parser.add_argument("--shuffle-seed", type=int, default=42)
    args = parser.parse_args()

    responses = load_responses(Path(args.panel))
    n_total = len(responses)
    shuffled = list(responses)
    random.Random(args.shuffle_seed).shuffle(shuffled)

    print(f"panel: {args.panel}  (n={n_total})")
    print("\n== Convergence: pooled mean over growing shuffled subsets ==")
    sizes = [s for s in args.subset_sizes if s <= n_total]
    header = f"{'field':52s}" + "".join(f"{f'n={s}':>9}" for s in sizes) + f"{'SE(full)':>10}"
    print(header)
    for section, field in KEY_FIELDS:
        cells = "".join(f"{mean(field_values(shuffled[:s], section, field)):9.3f}" for s in sizes)
        print(f"{section + '.' + field:52s}{cells}{se(field_values(responses, section, field)):10.4f}")

    if args.reference:
        reference = load_responses(Path(args.reference))
        ref_archetypes = sorted({r["archetype_id"] for r in reference})
        print(f"\n== Composition vs scale (reference: {args.reference}, n={len(reference)}, archetypes {','.join(ref_archetypes)}) ==")
        print(f"{'field':52s}{'ref pool':>9}{'same-arch':>10}{'weighted':>9}{'comp.':>8}{'scale':>8}")
        for section, field in KEY_FIELDS:
            ref_pool = mean(field_values(reference, section, field))
            same_arch = equal_weight_pool(responses, section, field, ref_archetypes)
            weighted = mean(field_values(responses, section, field))
            print(
                f"{section + '.' + field:52s}{ref_pool:9.3f}{same_arch:10.3f}{weighted:9.3f}"
                f"{weighted - same_arch:8.3f}{same_arch - ref_pool:8.3f}"
            )
        print("\ncomp. = weighted-pool minus equal-weight same-archetype pool (composition effect)")
        print("scale = same-archetype pool at large N minus reference pool (sampling/scale effect)")


if __name__ == "__main__":
    main()
