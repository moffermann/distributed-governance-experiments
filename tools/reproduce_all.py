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

# 4. Behavioral adoption sweep (feeds Experiment C scenarios; slowest step).
if not QUICK:
    run([sys.executable, "run_sweep.py", "--seeds", "10"], cwd=ROOT / "behavioral-adoption-abm")

# 5. Experiment E program (longitudinal engine v0.8; anchors reproduce v0.6/v0.7).
run(["node", "adversarial-abm/src/longitudinal.mjs"])
run(["node", "adversarial-abm/src/e_sensitivity_k.mjs"])
run(["node", "adversarial-abm/src/e1c.mjs"])
run(["node", "adversarial-abm/src/e1b.mjs"])
run(["node", "adversarial-abm/src/e1d.mjs"])

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
