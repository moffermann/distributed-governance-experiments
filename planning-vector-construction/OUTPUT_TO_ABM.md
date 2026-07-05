# Output to Adversarial ABM

## Purpose

This document defines how the planning-vector construction experiment should feed the adversarial ABM.

The adversarial ABM currently needs planning-signal quality parameters such as:

```text
centralPlanningSignalMix
distributedPlanningSignalMix
```

This experiment should produce calibrated proxy ranges for those parameters.

## Output artifacts

The planning-vector experiment should eventually produce:

```text
results/planning-vector-construction/<scenario>.raw.json
results/planning-vector-construction/<scenario>.summary.csv
results/planning-vector-construction/<scenario>.summary.md
```

Minimum summary fields:

```text
scenario_id
centralPlanLatentCorrelation_mean
centralPlanLatentCorrelation_sd
distributedPlanLatentCorrelation_mean
distributedPlanLatentCorrelation_sd
salienceLatentCorrelation_mean
salienceLatentCorrelation_sd
recommendedCentralPlanningSignalMix
recommendedDistributedPlanningSignalMix
recommendedSensitivityRange
```

## Mapping rule

The adversarial ABM should not blindly copy raw correlations as mix parameters.

Reason:

```text
A mix parameter is a generator setting.
A correlation is an observed output.
```

Therefore, the mapping should be explicit.

Recommended first mapping:

```text
centralPlanningSignalMix = calibrated generator value that reproduces the observed centralPlanLatentCorrelation range

distributedPlanningSignalMix = calibrated generator value that reproduces the observed distributedPlanLatentCorrelation range
```

In other words:

1. run planning-vector construction experiment;
2. observe central and distributed plan correlations;
3. choose ABM signal-mix parameters that reproduce those correlations in the ABM project world;
4. report both the source scenario and the resulting observed ABM correlations.

## Example mapping

If the planning-vector experiment finds:

```text
centralPlanLatentCorrelation ≈ 0.15-0.25
distributedPlanLatentCorrelation ≈ 0.65-0.80
```

Then the adversarial ABM may use:

```text
centralPlanningSignalMix ≈ 0.10-0.20
distributedPlanningSignalMix ≈ 0.55-0.75
```

The exact mapping must be checked by observed ABM correlations because the generator mix and realized Pearson correlation are not identical.

## Scenario naming in the ABM

ABM scenarios should reference their planning-vector calibration source.

Example:

```json
{
  "scenario_id": "baseline-medium",
  "planningCalibrationSource": {
    "experiment": "planning-vector-construction",
    "scenario": "representative-vs-distributed-baseline",
    "centralPlanLatentCorrelationTarget": [0.15, 0.25],
    "distributedPlanLatentCorrelationTarget": [0.65, 0.80]
  }
}
```

## Interpretation rule

Do not write:

```text
centralPlanningSignalMix = 0.15 because central planning is bad.
```

Write:

```text
centralPlanningSignalMix was chosen to reproduce the representative-planning correlation range produced by the planning-vector construction experiment under the median-alignment scenario.
```

## Sensitivity requirement

Every ABM headline result should run at least three planning regimes:

```text
central weak / distributed baseline
central median / distributed baseline
central high-capacity / distributed captured
```

This prevents the ABM from depending on a single planning assumption.

## Design rule

> The planning-vector experiment calibrates the ABM; the ABM does not invent planning quality.
