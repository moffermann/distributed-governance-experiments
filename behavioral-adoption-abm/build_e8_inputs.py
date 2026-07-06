"""E8 bridge inputs: behavioral trajectories -> paper-engine participation.

Runs the behavioral model per scenario and seed, extracts the participation
trajectory, and emits research/e8-behavioral-inputs.json per the mapping
pre-registered in research/e8-behavioral-participation-design.md:

    d_t  = 1 - active_user_share(t)                     (docs/101 default rule)
    pi_t = (direct_pop(t) + delegator_share(t)) / active_user_share(t)
           with the approved delegation->informed fold, capped at 0.95
    piInformed = plateau mean (last third) of direct_pop + delegator_share

Behavioral ticks (104 weeks) are resampled to the paper engine's 24 cycles.

Usage:
    python build_e8_inputs.py --seeds 10
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from behavioral_adoption_abm.core import BehavioralAdoptionModel, load_config  # noqa: E402

SCENARIOS = {
    "llm_calibrated": ROOT / "scenarios" / "llm_calibrated.json",
    "baseline": ROOT / "scenarios" / "baseline.json",
    "high_friction_launch": ROOT / "scenarios" / "high_friction_launch.json",
}
PAPER_CYCLES = 24


def trajectory(history: list[dict]) -> tuple[list[float], list[float], float]:
    # history[0] is the pre-run state; ticks 1..T are simulated weeks.
    ticks = history[1:]
    t_count = len(ticks)
    d_series, pi_series, informed_series = [], [], []
    for row in ticks:
        alpha = row["active_user_share"]
        direct_pop = row["direct_participation_share"] * row["registered_user_share"]
        informed_pop = direct_pop + row["delegator_share"]
        informed_series.append(informed_pop)
        d_series.append(1.0 - alpha)
        pi_series.append(min(0.95, informed_pop / alpha) if alpha > 0 else 0.0)
    d_cycles, pi_cycles = [], []
    for c in range(PAPER_CYCLES):
        idx = round(c * (t_count - 1) / (PAPER_CYCLES - 1))
        d_cycles.append(round(d_series[idx], 4))
        pi_cycles.append(round(pi_series[idx], 4))
    plateau = informed_series[-max(1, t_count // 3):]
    pi_informed = round(sum(plateau) / len(plateau), 4)
    return d_cycles, pi_cycles, pi_informed


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate E8 behavioral participation inputs.")
    parser.add_argument("--seeds", type=int, default=10)
    parser.add_argument("--output", default=str(ROOT.parent.parent / "research" / "e8-behavioral-inputs.json"))
    args = parser.parse_args()

    payload = {
        "generated": date.today().isoformat(),
        "mapping": "research/e8-behavioral-participation-design.md",
        "behavioral_experiment": "experiments/behavioral-adoption-abm",
        "paper_cycles": PAPER_CYCLES,
        "note": "d/pi per cycle from 104-week trajectories; delegation folded into informed (author-approved); llm-elicited priors, not empirical data.",
        "populations": {},
    }
    for name, path in SCENARIOS.items():
        runs = []
        for i in range(args.seeds):
            config = load_config(path, overrides={"seed": 42 + i})
            model = BehavioralAdoptionModel(config)
            model.run(int(model.config["ticks"]))
            d_cycles, pi_cycles, pi_informed = trajectory(model.history)
            runs.append({"seed": 42 + i, "piInformed": pi_informed, "d": d_cycles, "pi": pi_cycles})
        payload["populations"][name] = {"seeds": args.seeds, "runs": runs}
        d_end = sum(r["d"][-1] for r in runs) / len(runs)
        pi_end = sum(r["pi"][-1] for r in runs) / len(runs)
        pi_inf = sum(r["piInformed"] for r in runs) / len(runs)
        print(f"{name:24s} plateau d={d_end:.3f}  pi={pi_end:.3f}  piInformed={pi_inf:.3f}")

    out = Path(args.output)
    out.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
