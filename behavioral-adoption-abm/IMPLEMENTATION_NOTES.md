# Implementation Notes

## Current prototype

This is the executable MVP for the Core v0 behavioral adoption ABM, corrected and certified against the architecture corpus in [`CORE_V0_CONFORMANCE_AUDIT.md`](CORE_V0_CONFORMANCE_AUDIT.md).

The implementation intentionally uses a small inspectable object model and no mandatory runtime dependency beyond Python itself. If Mesa is installed, the agents and model use Mesa's `Agent` and `Model` base classes (Mesa 3.x is initialized with an integer seed). Either way the model draws every random number from one `random.Random(seed)` stream, so outputs are byte-identical with and without Mesa.

## Run

From this folder:

```bash
python run_experiment.py --scenario scenarios/baseline.json --ticks 104 --seed 42 --output-dir outputs/baseline
```

Multi-seed sweep across all scenarios:

```bash
python run_sweep.py --seeds 10 --output-dir outputs/sweep
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

`final_metrics.json` and `integration_outputs.json` include the minimum-viability flags defined in `METRICS.md`.

## What it already models

- citizen awareness (with a media-reach ceiling), registration (one-shot consideration with social-proof re-triggering), permanent rejection, activation;
- direct participation, profile-driven participation, full delegation, hybrid / partial delegation, with mode inertia and shock-driven reconsideration;
- the public default rule: non-active citizens' allocation still flows to projects at reduced routing efficiency, and `default_rule_share` is exported (docs/101);
- trusted microdelegation as the baseline delegation channel (citizens delegating to willing people in their own social circle), with the institutional delegate pool as the stress channel and a two-stage channel/candidate choice;
- delegation switching, revocation (including forced revocation when a micro-delegate becomes invalid), and concentration metrics over the combined micro + institutional weight distribution;
- abandonment and reactivation; trust updates from public successes, failures, outages, controversy, recovery events, and social influence (gated to aware citizens);
- sticky role markets for executors, fiscalizers, and evidence producers (recruitment/dropout hazards with compensation elasticity);
- verification and evidence coverage against per-project requirements and per-actor capacity, and the resulting thin-market failure rate;
- the end-to-end planning layer ([`PLANNING_LAYER_DESIGN.md`](PLANNING_LAYER_DESIGN.md)): latent needs vs salience, emergent attentive citizens, delegated planning signals with emergent coverage, distributed and central vector construction every round, default-rule routing that follows the operating mode's published vector (docs/101), and need-weighted delivered value;
- integration outputs for the institutional architecture and planning-vector experiments, including the `delegatorShare` / `delegateCount` / `delegateConcentration` / `delegatePlatformUseRate` / `delegatePlanningCoverage` mapping.

## What it does not model yet

- profile-state split (configured / active / overridden) and profile pause/override dynamics (docs/28);
- verification queueing and per-project assignment;
- geographic or territorial segmentation;
- explicit project category matching;
- calibrated coefficients or real pilot data (all parameters are synthetic);
- full adversarial attack library (belongs to the adversarial ABM);
- LLM agents;
- visualization dashboard;
- adapter into the existing institutional architecture engine.

## Next implementation step

Build the adapter that maps `integration_outputs.json` into the architecture experiment's behavioral parameters and the planning-vector experiment's delegation parameters, then prioritize empirical grounding of the fiscalizer/evidence capacity priors — the audit marks them as the parameters that set the depth of the central bottleneck finding.
