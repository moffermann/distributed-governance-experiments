"""Multi-seed sweep runner for the behavioral adoption ABM.

Runs every scenario file given (or all scenarios/*.json) across N seeds and
writes per-scenario mean/min/max integration outputs plus viability flags.

Usage:
    python run_sweep.py --seeds 10 --output-dir outputs/sweep
    python run_sweep.py --scenarios scenarios/baseline.json scenarios/delegation_first.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from behavioral_adoption_abm.core import (  # noqa: E402
    INTEGRATION_KEYS,
    BehavioralAdoptionModel,
    load_config,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sweep the behavioral adoption ABM across seeds.")
    parser.add_argument("--scenarios", nargs="*", default=None, help="Scenario JSON files (default: scenarios/*.json).")
    parser.add_argument("--seeds", type=int, default=10, help="Number of replications per scenario.")
    parser.add_argument("--ticks", type=int, default=None, help="Override number of ticks.")
    parser.add_argument("--output-dir", default="outputs/sweep", help="Directory for sweep_summary.json.")
    return parser.parse_args()


def sweep_scenario(path: Path, seeds: int, ticks: int | None) -> dict:
    per_seed = []
    flag_counts: dict[str, int] = {}
    for i in range(seeds):
        config = load_config(path, overrides={"seed": 42 + i, **({"ticks": ticks} if ticks else {})})
        model = BehavioralAdoptionModel(config)
        model.run(int(model.config["ticks"]))
        per_seed.append(model.final_metrics())
        for flag, value in model.viability_flags().items():
            flag_counts[flag] = flag_counts.get(flag, 0) + int(value)
    summary = {}
    for key in INTEGRATION_KEYS:
        values = [m.get(key, 0.0) for m in per_seed]
        summary[key] = {
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }
    return {
        "scenario_id": load_config(path)["scenario_id"],
        "seeds": seeds,
        "metrics": summary,
        "viability_flag_frequency": {k: v / seeds for k, v in sorted(flag_counts.items())},
    }


def main() -> None:
    args = parse_args()
    scenario_paths = (
        [Path(p) for p in args.scenarios]
        if args.scenarios
        else sorted((ROOT / "scenarios").glob("*.json"))
    )
    results = [sweep_scenario(path, args.seeds, args.ticks) for path in scenario_paths]
    out = Path(args.output_dir)
    write_json(out / "sweep_summary.json", {"scenarios": results})

    key_columns = [
        "registered_user_share",
        "active_user_share",
        "default_rule_share",
        "direct_participation_share",
        "profile_driven_share",
        "full_delegation_share",
        "partial_delegation_share",
        "delegator_share",
        "active_delegate_count",
        "delegation_concentration_hhi",
        "top_delegate_share",
        "micro_delegation_weight_share",
        "delegate_platform_use_rate",
        "abandonment_share",
        "mean_platform_trust",
        "verification_coverage_rate",
        "evidence_coverage_rate",
        "thin_market_failure_rate",
        "recommendation_rate",
    ]
    for result in results:
        print(f"\n== {result['scenario_id']} (n={result['seeds']}) ==")
        for key in key_columns:
            stats = result["metrics"][key]
            print(f"  {key:38s} mean={stats['mean']:8.4f}  min={stats['min']:8.4f}  max={stats['max']:8.4f}")
        flags = {k: v for k, v in result["viability_flag_frequency"].items() if v > 0}
        print(f"  viability flags raised: {flags if flags else 'none'}")


if __name__ == "__main__":
    main()
