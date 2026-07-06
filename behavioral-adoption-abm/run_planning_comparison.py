"""Distributed-vs-central planning comparison for the behavioral adoption ABM.

Sweeps `planning_attendance_scale` (a dial on how often active citizens attend
planning rounds) across seeds and both planning modes, to locate:

1. the emergent attentive-share range,
2. the crossover below which the bandwidth-limited central planner out-informs
   the distributed vector,
3. the end-to-end delivered-value gap between the two regimes.

Usage:
    python run_planning_comparison.py --seeds 6 --output-dir outputs/planning_comparison
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from behavioral_adoption_abm.core import BehavioralAdoptionModel, load_config, write_json  # noqa: E402

SCALES = [0.05, 0.10, 0.25, 0.50, 1.00, 1.50, 2.00]
KEYS = [
    "attentive_share_mean",
    "planning_representation_share",
    "planning_signal_coverage",
    "delegate_planning_coverage",
    "distributed_planning_correlation",
    "central_planning_correlation",
    "value_delivered_share",
    "active_user_share",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare distributed vs central planning end-to-end.")
    parser.add_argument("--scenario", default="scenarios/baseline.json", help="Base scenario file.")
    parser.add_argument("--seeds", type=int, default=6, help="Replications per cell.")
    parser.add_argument("--scales", nargs="*", type=float, default=None, help="planning_attendance_scale values.")
    parser.add_argument("--no-delegation", action="store_true", help="Also sweep an attentive-only variant (all delegation disabled).")
    parser.add_argument("--output-dir", default="outputs/planning_comparison", help="Directory for the summary JSON.")
    return parser.parse_args()


def run_cell(scenario: str, scale: float, mode: str, seeds: int, extra: dict | None = None) -> dict:
    acc = {k: [] for k in KEYS}
    for i in range(seeds):
        config = load_config(
            scenario,
            overrides={"seed": 42 + i, "planning_attendance_scale": scale, "planning_mode": mode, **(extra or {})},
        )
        model = BehavioralAdoptionModel(config)
        model.run(int(model.config["ticks"]))
        m = model.final_metrics()
        for k in KEYS:
            acc[k].append(m[k])
    return {k: sum(v) / len(v) for k, v in acc.items()}


NO_DELEGATION = {
    "micro_delegate_willingness": 0.0,
    "institutional_delegate_count": 0,
    "institutional_delegation_propensity": 0.0,
}


def main() -> None:
    args = parse_args()
    scales = args.scales or SCALES
    variants = [("with_delegation", None)]
    if args.no_delegation:
        variants.append(("attentive_only", NO_DELEGATION))
    rows = []
    for variant_name, extra in variants:
        for scale in scales:
            dist = run_cell(args.scenario, scale, "distributed", args.seeds, extra)
            cent = run_cell(args.scenario, scale, "central", args.seeds, extra)
            rows.append({
                "variant": variant_name,
                "planning_attendance_scale": scale,
            "attentive_share_mean": dist["attentive_share_mean"],
            "planning_representation_share": dist["planning_representation_share"],
            "planning_signal_coverage": dist["planning_signal_coverage"],
            "delegate_planning_coverage": dist["delegate_planning_coverage"],
            "distributed_correlation": dist["distributed_planning_correlation"],
            "central_correlation": dist["central_planning_correlation"],
            "correlation_gap": dist["distributed_planning_correlation"] - dist["central_planning_correlation"],
            "value_share_distributed_mode": dist["value_delivered_share"],
            "value_share_central_mode": cent["value_delivered_share"],
                "value_ratio_distributed_over_central": (
                    dist["value_delivered_share"] / cent["value_delivered_share"]
                    if cent["value_delivered_share"] > 0 else 0.0
                ),
            })
    write_json(Path(args.output_dir) / "planning_comparison.json", {"seeds": args.seeds, "rows": rows})

    header = (
        f"{'variant':>16} {'scale':>6} {'attentive':>10} {'repres.':>8} {'coverage':>9} {'del.cov':>8} "
        f"{'corr(dist)':>11} {'corr(cent)':>11} {'gap':>8} {'val(dist)':>10} {'val(cent)':>10} {'ratio':>7}"
    )
    print(header)
    print("-" * len(header))
    for r in rows:
        print(
            f"{r['variant']:>16} {r['planning_attendance_scale']:>6.2f} {r['attentive_share_mean']:>10.4f} "
            f"{r['planning_representation_share']:>8.4f} {r['planning_signal_coverage']:>9.4f} "
            f"{r['delegate_planning_coverage']:>8.4f} {r['distributed_correlation']:>11.4f} "
            f"{r['central_correlation']:>11.4f} {r['correlation_gap']:>8.4f} "
            f"{r['value_share_distributed_mode']:>10.4f} {r['value_share_central_mode']:>10.4f} "
            f"{r['value_ratio_distributed_over_central']:>7.4f}"
        )
    for variant_name, _ in variants:
        variant_rows = [r for r in rows if r["variant"] == variant_name]
        losing = [r for r in variant_rows if r["correlation_gap"] <= 0]
        if losing:
            floor = max(losing, key=lambda r: r["planning_attendance_scale"])
            print(
                f"\n[{variant_name}] central out-informs distributed up to attentive_share_mean "
                f"~{floor['attentive_share_mean']:.4f} (scale {floor['planning_attendance_scale']})"
            )
        else:
            print(f"\n[{variant_name}] distributed out-informs central at every tested attendance level")


if __name__ == "__main__":
    main()
