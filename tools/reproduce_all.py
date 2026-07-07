#!/usr/bin/env python3
"""One-command reproduction of every committed result (Phase 3 hardening).

Runs, in dependency order, every engine and analysis that produces committed
artifacts, from a clean clone. Requirements: Node.js >= 18, Python >= 3.10,
matplotlib (figures); Mesa optional (docking). LLM panels are NOT rerun (they
require model backends and are committed with provenance); everything else is.

Usage:
    python tools/reproduce_all.py            # full (~10-15 min)
    python tools/reproduce_all.py --quick    # skips behavioral sweep + docking
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUICK = "--quick" in sys.argv


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print(f"\n=== {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


# 1. Static adversarial engine: five committed scenarios (Experiments A + C).
for scen in ["baseline-medium", "behavioral-baseline", "behavioral-llm-calibrated",
             "behavioral-high-friction", "behavioral-delegation-first"]:
    run(["node", "adversarial-abm/src/index.mjs", "--scenario", f"adversarial-abm/scenarios/{scen}.json"])

# 2. Ablation and semi-open programs (static engine).
run(["node", "adversarial-abm/src/ablation.mjs"])
run(["node", "adversarial-abm/src/semi_open.mjs"])

# 3. Planning-vector construction.
run(["node", "planning-vector-construction/src/index.mjs"])

# 4. Behavioral adoption sweep + the Experiment C scenario builder (the
#    endogenous-participation mapping; slowest step).
if not QUICK:
    run([sys.executable, "run_sweep.py", "--seeds", "10"], cwd=ROOT / "behavioral-adoption-abm")
    for source, scen in [("baseline", "behavioral-baseline"), ("llm_calibrated", "behavioral-llm-calibrated"),
                         ("high_friction_launch", "behavioral-high-friction"), ("delegation_first", "behavioral-delegation-first")]:
        run([sys.executable, "build_adversarial_scenario.py", "--sweep", "outputs/expc-sweep/sweep_summary.json",
             "--source", source, "--scenario-id", scen], cwd=ROOT / "behavioral-adoption-abm")

# 5. Experiment E/F/G deterministic engine cells (longitudinal engine v0.11;
#    anchors reproduce v0.6-v0.10 exactly). The F-0 LIVE-MODEL panel is NOT here
#    (needs model backends); its committed scoring, however, is regenerable —
#    see step 5b.
run(["node", "adversarial-abm/src/longitudinal.mjs"])
run(["node", "adversarial-abm/src/e_sensitivity_k.mjs"])
run(["node", "adversarial-abm/src/e1c.mjs"])
run(["node", "adversarial-abm/src/e1b.mjs"])
run(["node", "adversarial-abm/src/e1d.mjs"])
run(["node", "adversarial-abm/src/e_f1.mjs"])
run(["node", "adversarial-abm/src/e_f2.mjs"])
run(["node", "adversarial-abm/src/e_f34.mjs"])
run(["node", "adversarial-abm/src/e_g.mjs"])
run([sys.executable, "tools/ratio_cis.py"])

# 5b. F-0 panel SCORING (deterministic; reads committed verdict jsonl, no live
#     models). The panel RUNS themselves (evidence-panel/run_panel.py) require
#     model backends and are the only step excluded from one-command repro.
import os as _os  # noqa: E402
for _inst in ("v1", "v3"):
    env = {**_os.environ, "PANEL_INSTRUMENT": _inst}
    try:
        subprocess.run([sys.executable, "evidence-panel/analyze_panel.py"], cwd=ROOT, env=env, check=True)
    except Exception as exc:  # noqa: BLE001
        print(f"panel scoring {_inst} skipped: {exc}")

# 6. Cross-framework docking (optional: requires mesa).
if not QUICK:
    try:
        run([sys.executable, "docking/mesa/run_dock.py"])
    except Exception as exc:  # noqa: BLE001 - docking is optional
        print(f"docking skipped: {exc}")

# 7. Figures and statistical annex (from committed/just-regenerated results).
run([sys.executable, "tools/make_figures.py"])
run([sys.executable, "tools/statistical_annex.py"])

print("\nAll reproduction steps completed. Compare with committed results via `git diff`.")
