# Scenario Configuration — Planning Vector Construction

## Purpose

This document defines how scenarios should be configured for the planning-vector construction experiment.

The experiment should output planning-signal quality estimates that can later feed the adversarial ABM.

## Scenario file location

Recommended folder:

```text
experiments/planning-vector-construction/scenarios/
```

## Minimal scenario schema

```json
{
  "scenario_id": "representative-vs-distributed-baseline",
  "scenario_version": "0.1",
  "seed": 1,
  "runs": 100,
  "population": {
    "citizens": 10000,
    "groups": 8,
    "territories": 20,
    "targets": 80,
    "preferencePolarization": 0.35,
    "territorialHeterogeneity": 0.30,
    "beneficiaryConcentration": 0.25
  },
  "representativePlanning": {
    "turnoutRate": 0.555,
    "winnerVoteShare": 0.52,
    "approvalRate": 0.40,
    "supporterAlignment": 0.70,
    "nonSupporterAlignment": 0.15,
    "programFidelity": 0.60,
    "technocraticCapacity": 0.20,
    "bureaucraticDistortion": 0.15,
    "coalitionDistortion": 0.10,
    "lobbyingDistortion": 0.10,
    "beneficiaryDistance": 0.15
  },
  "distributedPlanning": {
    "generalSignalCoverage": 0.25,
    "beneficiarySignalCoverage": 0.45,
    "affectedPartyCoverage": 0.25,
    "localOrgCoverage": 0.20,
    "expertSignalCoverage": 0.15,
    "generalSignalNoise": 0.35,
    "beneficiarySignalNoise": 0.20,
    "affectedPartySignalNoise": 0.25,
    "localOrgSignalNoise": 0.25,
    "expertSignalNoise": 0.15,
    "wGeneral": 0.25,
    "wBeneficiary": 0.35,
    "wAffected": 0.15,
    "wLocal": 0.15,
    "wExpert": 0.10,
    "participationBias": 0.30,
    "salienceBiasStrength": 0.20,
    "strategicSignalShare": 0.10,
    "manipulationIntensity": 0.30,
    "antiCaptureFilterStrength": 0.30,
    "deliberationCorrectionStrength": 0.30
  },
  "outputs": {
    "rawJson": true,
    "markdownTable": true,
    "csv": true
  }
}
```

## Scenario families

## 1. Representative planning scenarios

### `central-low-alignment`

Tests a government with low approval, weak program fidelity, low technocratic recovery, and high distortion.

### `central-median-alignment`

Baseline representative planning scenario.

### `central-high-alignment`

Tests a strong mandate and high approval environment.

### `central-technocratic-capacity`

Tests whether technical state capacity can compensate for weak representative alignment.

## 2. Distributed planning scenarios

### `distributed-low-coverage`

Tests sparse and biased distributed signals.

### `distributed-baseline`

Baseline distributed signal scenario.

### `distributed-beneficiary-weighted`

Tests higher beneficiary signal coverage and weight.

### `distributed-captured`

Tests coordinated manipulation and weak anti-capture filtering.

### `distributed-deliberative-correction`

Tests whether deliberation and source correction improve signal quality.

## 3. Hybrid scenarios

### `central-plus-distributed-correction`

Starts with a representative plan and applies distributed correction to underrepresented targets.

Possible formula:

```text
hybrid_plan = (1 - correction_weight) * central_plan
            + correction_weight * distributed_plan
```

### `tutored-parallel-planning`

Models a tutored mode where the public authority keeps legal control, but distributed planning signals are visible and influence the default planning vector.

## Output metrics

Each scenario should output:

```text
centralPlanLatentCorrelation
distributedPlanLatentCorrelation
salienceLatentCorrelation
hybridPlanLatentCorrelation where applicable
supporterCoverage
nonSupporterLoss
beneficiaryRecovery
minorityPreferenceLoss
strategicBiasLoss
salienceDistortion
```

## Reproducibility rule

Each result should record:

```text
scenario_id
scenario_version
seed
run_index
parameter set
code version or commit sha where available
```

## Design rule

> The scenario file is part of the evidence. Treat it as data, not as hidden configuration.
