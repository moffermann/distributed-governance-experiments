# Implementation Notes

## Current prototype

This is the first executable MVP for the Core v0 behavioral adoption ABM.

The implementation intentionally uses a small inspectable object model and no mandatory runtime dependency beyond Python itself. If Mesa is installed, the agents and model use Mesa's `Agent` and `Model` base classes. If Mesa is not installed, a small fallback shim lets the same scenario run for reproducibility and quick inspection.

## Run

From this folder:

```bash
python run_experiment.py --scenario scenarios/baseline.json --ticks 104 --seed 42 --output-dir outputs/baseline
```

Or, using the package module:

```bash
PYTHONPATH=src python -m behavioral_adoption_abm.run --scenario scenarios/ai_assisted_onboarding.json --output-dir outputs/ai_assisted
```

The runner writes:

```text
outputs/<run>/timeseries.csv
outputs/<run>/final_metrics.json
outputs/<run>/integration_outputs.json
```

## What it already models

The MVP includes:

- citizen awareness;
- registration;
- activation;
- direct participation;
- profile-driven participation;
- full delegation;
- hybrid / partial delegation;
- abandonment and reactivation;
- trust updates from public successes, failures, outages, controversy, and social influence;
- delegate reputation and concentration;
- executor participation;
- fiscalizer supply;
- evidence producer supply;
- verification-market thinness;
- integration outputs for the institutional architecture experiment.

## What it does not model yet

The MVP does not yet implement:

- geographic or territorial segmentation;
- explicit project category matching;
- calibrated coefficients;
- real pilot data;
- full adversarial attack library;
- LLM agents;
- visualization dashboard;
- adapter into the existing institutional architecture engine.

## Next implementation step

The next step is not to add complexity immediately. The next step is to run scenario sweeps and inspect whether the baseline transitions are plausible.

After that, the adapter should map `integration_outputs.json` into the existing architecture experiment's behavioral parameters.
