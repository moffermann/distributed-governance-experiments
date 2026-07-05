# Planning Vector Construction Experiment

## Working title

**Representative Information Loss and Distributed Planning Signals: Constructing Public-Value Planning Vectors for Institutional Simulation**

## Status

Preliminary design baseline.

This experiment is separate from `experiments/adversarial-abm/`.

The adversarial ABM compares allocation, execution, verification, and accountability architectures. This experiment focuses on an earlier question:

```text
How is the planning vector constructed before public resources are allocated?
```

## Core idea

Before comparing public-resource allocation architectures, the research program needs a fairer proxy for the quality of the planning vector each architecture receives.

A central planning vector should not be arbitrarily assumed to be good or bad.

Its correlation with latent public value should be derived from mechanisms such as:

- electoral participation;
- winner vote share;
- approval;
- supporter versus non-supporter alignment;
- program-to-plan fidelity;
- bureaucratic and coalition distortion;
- lobbying or organized-interest distortion;
- distance from beneficiaries;
- technocratic capacity.

A distributed planning vector should also not be assumed to be magically good.

Its quality should be derived from mechanisms such as:

- citizen signal coverage;
- beneficiary signal coverage;
- affected-party signal coverage;
- signal noise;
- participation bias;
- salience bias;
- strategic signal manipulation;
- deliberative correction;
- anti-capture filtering.

## Purpose

The output of this experiment should eventually calibrate inputs for the larger adversarial ABM:

```text
centralPlanningSignalMix
distributedPlanningSignalMix
```

Instead of assigning these values arbitrarily, this experiment will estimate plausible ranges for them under different representative and distributed-planning scenarios.

## Current design documents

- [`DESIGN_BASELINE.md`](DESIGN_BASELINE.md) — research question, model overview, and experiment structure.
- [`REPRESENTATIVE_PLANNING_MODEL.md`](REPRESENTATIVE_PLANNING_MODEL.md) — central/representative planning information-loss model.
- [`DISTRIBUTED_PLANNING_MODEL.md`](DISTRIBUTED_PLANNING_MODEL.md) — distributed signal aggregation and planning-vector model.
- [`CALIBRATION_PRIORS.md`](CALIBRATION_PRIORS.md) — initial proxy parameters, real-world anchors, and sensitivity ranges.
- [`SCENARIO_CONFIGURATION.md`](SCENARIO_CONFIGURATION.md) — scenario schema and planned scenario families.
- [`OUTPUT_TO_ABM.md`](OUTPUT_TO_ABM.md) — how this experiment feeds the adversarial ABM.

## Evidence status

This experiment will initially produce simulation evidence and calibrated proxy ranges, not empirical proof.

The purpose is to produce a more disciplined proxy for planning-vector quality than a single arbitrary correlation value.

## Design rule

> Do not punish central planning by assumption; model the information that survives representation.

And symmetrically:

> Do not reward distributed planning by assumption; model the information that survives participation, noise, salience, and manipulation.
