"""CLI runner for the Core v0 behavioral adoption ABM."""

from __future__ import annotations

import argparse
import json

from .core import load_config, run_scenario


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Core v0 behavioral adoption ABM.")
    parser.add_argument("--scenario", default="scenarios/baseline.json", help="Path to scenario JSON file.")
    parser.add_argument("--ticks", type=int, default=None, help="Override number of ticks.")
    parser.add_argument("--seed", type=int, default=None, help="Override scenario seed.")
    parser.add_argument("--output-dir", default="outputs/latest", help="Output directory for CSV/JSON results.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    overrides = {}
    if args.ticks is not None:
        overrides["ticks"] = args.ticks
    if args.seed is not None:
        overrides["seed"] = args.seed
    config = load_config(args.scenario, overrides=overrides)
    model = run_scenario(config, args.output_dir)
    print(json.dumps(model.integration_outputs(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
