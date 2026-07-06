# Planning Calibration from Experiment 2

## Purpose

This document records how the adversarial ABM uses the upstream planning-vector construction experiment to calibrate planning signals.

The ABM should not invent planning quality.

It should consume calibrated planning-signal ranges from:

```text
experiments/planning-vector-construction/
```

## Source experiment

Current source:

```text
experiment: experiments/planning-vector-construction
scenario: core-v0-planning-channels
scenario_version: 0.5
```

The source experiment estimates correlations between planning vectors and latent social value for representative central planning and Core v0 distributed planning channels.

## Important distinction

The planning-vector experiment reports target correlations:

```text
corr(planning_vector, latent_value)
```

The adversarial ABM scenario uses generator parameters:

```text
centralPlanningSignalMix
distributedPlanningSignalMix
```

These are not the same thing.

A mix parameter is used to generate a signal:

```text
planningWeight = signalMix * latentValue + (1 - signalMix) * noise
```

The resulting Pearson correlation is measured by the simulation and may differ from the mix value.

## Current baseline calibration

The current ABM baseline uses:

```text
centralPlanningSignalMix = 0.39
distributedPlanningSignalMix = 0.66
```

Approximate targets:

```text
central planning target correlation ≈ 0.44
distributed Core v0 planning target correlation ≈ 0.83
```

## Why these targets?

### Central planning

The central planning target is based on a median range between:

```text
central_median_global_south
central_median_democracy
```

from the planning-vector construction experiment.

This avoids calibrating central planning only from developed-democracy or high-alignment cases.

### Distributed Core v0 planning

The distributed planning target is based on Core v0 planning-channel scenarios such as:

```text
core_v0_tutored_distributed_voluntary
core_v0_open_trusted_microdelegation
```

This reflects the expected informational advantage of attentive participation plus auditable/revocable delegation, while not using the most optimistic open mandated participation result as the default.

## Conservative interpretation

This calibration should be treated as a medium baseline, not as a universal claim.

Future ABM sweeps should include:

```text
central_crisis_legitimacy
central_median_global_south
central_median_democracy
central_high_alignment
core_v0_conservative_distributed
core_v0_trusted_microdelegation
core_v0_open_mandated_participation
```

## Design rule

> Planning quality enters the adversarial ABM through explicit calibration ranges from the planning-vector experiment, not through arbitrary hand-picked correlations.
