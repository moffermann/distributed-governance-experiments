#!/usr/bin/env python3
"""Run the Mesa docking replication across all five architectures x 20 runs.

Reproduction:
    python docking/mesa/run_dock.py

Reads adversarial-abm/scenarios/behavioral-llm-calibrated.json, generates one
shared world per run seed (1..20), plays every architecture on that world, and
writes per-architecture mean/sd for verifiedValuePerBudget, leakageRate, and
selectionValueCorrelation to docking/mesa/results.json.
"""

from __future__ import annotations

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import GovernanceModel, generate_world, resolve_architectures  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SCENARIO_PATH = os.path.join(
    REPO, "adversarial-abm", "scenarios", "behavioral-llm-calibrated.json")

METRICS = ["verifiedValuePerBudget", "leakageRate", "selectionValueCorrelation",
           "fundedRate", "budgetSpent", "budgetUtilizationRate"]


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _sd(xs):
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def main():
    with open(SCENARIO_PATH, "r", encoding="utf-8") as fh:
        scenario = json.load(fh)

    architectures = resolve_architectures(scenario)
    runs = scenario["runs"]  # 20
    base_seed = scenario["seed"]  # 1 -> seeds 1..20

    # raw[arch_id][metric] = list over runs
    raw = {a["id"]: {m: [] for m in METRICS} for a in architectures}

    for r in range(runs):
        run_seed = base_seed + r  # 1..20
        # Common world, shared across architectures (paired comparison).
        world = generate_world(run_seed, scenario)
        for arch_index, arch in enumerate(architectures):
            # Independent derived seed per (run, architecture).
            model_seed = run_seed * 1000 + arch_index
            model = GovernanceModel(world, arch, scenario, seed=model_seed)
            metrics = model.run()
            for m in METRICS:
                raw[arch["id"]][m].append(metrics[m])

    summary = {}
    for arch in architectures:
        aid = arch["id"]
        summary[aid] = {
            "label": arch["label"],
            **{m: {"mean": _mean(raw[aid][m]), "sd": _sd(raw[aid][m])} for m in METRICS},
        }

    out = {
        "scenario_id": scenario["scenario_id"],
        "scenario_version": scenario.get("scenario_version"),
        "runs": runs,
        "base_seed": base_seed,
        "cycles": scenario["cycles"],
        "engine": "mesa-docking",
        "mesa_version": __import__("mesa").__version__,
        "summary": summary,
    }

    out_path = os.path.join(HERE, "results.json")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")

    # Console report.
    print(f"Mesa {out['mesa_version']} | scenario {out['scenario_id']} "
          f"v{out['scenario_version']} | runs {runs} seeds {base_seed}..{base_seed + runs - 1}")
    print(f"{'architecture':<46} {'verifVal/budget':>18} {'leakageRate':>16} {'sel(value)':>16}")
    for aid, s in summary.items():
        def cell(m):
            return f"{s[m]['mean']:.5f}±{s[m]['sd']:.5f}"
        print(f"{aid:<46} {cell('verifiedValuePerBudget'):>18} "
              f"{cell('leakageRate'):>16} {cell('selectionValueCorrelation'):>16}")
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
