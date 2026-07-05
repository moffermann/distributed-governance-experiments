# Source — Planning Vector Construction

This folder contains the first executable simulator for the planning-vector construction experiment.

## Current implementation

```text
index.mjs
```

The script is dependency-free Node.js and:

- reads a scenario JSON file;
- generates a synthetic population;
- generates public needs / planning targets;
- constructs an individual expected-value matrix;
- computes the latent social-value vector;
- builds representative central planning vectors across a broad approval/legitimacy distribution;
- builds Core v0 planning vectors from attentive citizens, trusted microdelegation, delegates, and optional mandate effects;
- can still run exploratory generic distributed-signal scenarios;
- compares every vector against latent social value;
- writes raw JSON, CSV, and Markdown summaries.

## Primary run command

From the repository root:

```bash
node experiments/planning-vector-construction/src/index.mjs \
  --scenario experiments/planning-vector-construction/scenarios/core-v0-planning-channels.json
```

The primary scenario is currently `core-v0-planning-channels` v0.3.

It includes central planning variants for:

```text
central_crisis_legitimacy
central_very_low_alignment
central_low_alignment
central_median_global_south
central_median_democracy
central_high_alignment
```

and Core v0 variants centered on trusted microdelegation.

Optional overrides:

```bash
node experiments/planning-vector-construction/src/index.mjs \
  --scenario experiments/planning-vector-construction/scenarios/core-v0-planning-channels.json \
  --runs 200 \
  --seed 42
```

## Exploratory legacy scenario

```bash
node experiments/planning-vector-construction/src/index.mjs \
  --scenario experiments/planning-vector-construction/scenarios/baseline-comparison.json
```

The legacy scenario includes generic distributed signal variants and should not be treated as the main Core v0 planning proxy.

## Evidence status

This produces simulation evidence and calibrated proxy ranges.

It is not yet empirical proof of real planning-vector quality.

## Design rule

> Estimate planning-vector quality from representation and Core v0 planning channels before injecting planning quality into the larger ABM.
