# Planning Vector Construction Experiment

## Working title

**Representative Information Loss and Core v0 Planning Channels: Constructing Public-Value Planning Vectors for Institutional Simulation**

## Status

Preliminary executable baseline.

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
- agenda bandwidth;
- off-agenda responsiveness;
- bureaucratic and coalition distortion;
- lobbying or organized-interest distortion;
- distance from beneficiaries;
- limited technocratic recovery.

A Core v0 distributed planning vector should also not be assumed to be magically good.

It should be built from Core v0 planning channels:

- attentive citizen planning signals;
- delegated planning signals;
- delegate count and concentration;
- delegate auditability;
- delegate revocability;
- delegate scope granularity;
- optional authority mandate effects.

Project allocation profiles and passive defaults are excluded from planning-vector construction. They belong to downstream project allocation.

## Purpose

The output of this experiment should eventually calibrate inputs for the larger adversarial ABM:

```text
centralPlanningSignalMix
distributedPlanningSignalMix
```

Instead of assigning these values arbitrarily, this experiment estimates plausible ranges for them under representative central planning and Core v0 planning-channel scenarios.

## Current design documents

- [`DESIGN_BASELINE.md`](DESIGN_BASELINE.md) — research question, model overview, and experiment structure.
- [`REPRESENTATIVE_PLANNING_MODEL.md`](REPRESENTATIVE_PLANNING_MODEL.md) — central/representative planning information-loss model.
- [`AGENDA_COMPRESSION_MODEL.md`](AGENDA_COMPRESSION_MODEL.md) — agenda bandwidth and off-agenda responsiveness as representative information-loss mechanisms.
- [`CORE_V0_PLANNING_CHANNEL_MODEL.md`](CORE_V0_PLANNING_CHANNEL_MODEL.md) — Core v0 planning from attentive citizens, delegates, and optional authority mandate.
- [`OPEN_MODE_PLANNING_MODEL.md`](OPEN_MODE_PLANNING_MODEL.md) — open-mode planning with and without participation mandate.
- [`DISTRIBUTED_PLANNING_MODEL.md`](DISTRIBUTED_PLANNING_MODEL.md) — exploratory generic distributed signal aggregation model, not the primary Core v0 planning proxy.
- [`CALIBRATION_PRIORS.md`](CALIBRATION_PRIORS.md) — initial proxy parameters, real-world anchors, and sensitivity ranges.
- [`SCENARIO_CONFIGURATION.md`](SCENARIO_CONFIGURATION.md) — scenario schema and planned scenario families.
- [`OUTPUT_TO_ABM.md`](OUTPUT_TO_ABM.md) — how this experiment feeds the adversarial ABM.

## Executable baseline

Primary Core v0 channel scenario:

- [`scenarios/core-v0-planning-channels.json`](scenarios/core-v0-planning-channels.json) — representative central planning versus Core v0 planning channels.

Exploratory generic distributed-signal scenario:

- [`scenarios/baseline-comparison.json`](scenarios/baseline-comparison.json) — earlier representative versus generic distributed-signal comparison.

Executable:

- [`src/index.mjs`](src/index.mjs) — dependency-free Node.js simulator.
- [`src/README.md`](src/README.md) — run instructions and evidence-status note.

Run from the repository root:

```bash
node experiments/planning-vector-construction/src/index.mjs \
  --scenario experiments/planning-vector-construction/scenarios/core-v0-planning-channels.json
```

## Evidence status

This experiment produces simulation evidence and calibrated proxy ranges, not empirical proof.

The purpose is to produce a more disciplined proxy for planning-vector quality than a single arbitrary correlation value.

## Design rule

> Do not punish central planning by assumption; model the information that survives representation.

And symmetrically:

> Do not reward Core v0 planning by assumption; model the information that survives attentive participation, delegation, auditability, revocation, concentration, and optional mandate.
