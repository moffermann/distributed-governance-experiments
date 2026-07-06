"""Convenience runner for the behavioral adoption ABM.

Usage:
    python run_experiment.py --scenario scenarios/baseline.json --ticks 104 --seed 42
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from behavioral_adoption_abm.run import main


if __name__ == "__main__":
    main()
