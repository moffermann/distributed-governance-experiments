# Scenario Configuration and Reproducibility

## Purpose

This document defines how simulation scenarios should be configured, stored, and reported.

The goal is to prevent important assumptions from being hidden inside source code.

A scenario file should declare:

- population size;
- project world generation;
- actor distributions;
- architecture set;
- attack set and severity;
- probability parameters;
- run count;
- seed range;
- output expectations.

## Core rule

> If a parameter can materially change a result, it should be declared in a scenario file or printed in the result header.

## Scenario file location

Recommended folder:

```text
experiments/adversarial-abm/scenarios/
```

Example files:

```text
baseline-medium.json
high-salience.json
weak-verification.json
agenda-capture.json
thin-verifier-market.json
reputation-lock-in.json
```

## Minimal scenario schema

```json
{
  "scenario_id": "baseline-medium",
  "description": "Medium adversarial baseline for first paired architecture comparison.",
  "seed": 1,
  "runs": 20,
  "cycles": 24,
  "population": {
    "citizens": 10000,
    "attentiveShare": 0.05,
    "salienceShare": 0.25,
    "profileShare": 0.20,
    "passiveShare": 0.40,
    "delegatorShare": 0.10
  },
  "projects": {
    "activePool": 40,
    "latentValue": { "dist": "beta", "alpha": 2, "beta": 2 },
    "salienceCorrelation": 0.2,
    "planningWeightCorrelation": 0.5,
    "verificationDifficulty": { "dist": "beta", "alpha": 2, "beta": 2 },
    "executionDifficulty": { "dist": "beta", "alpha": 2, "beta": 3 },
    "fraudOpportunity": { "dist": "beta", "alpha": 1.5, "beta": 3 }
  },
  "executors": {
    "honestShare": 0.70,
    "opportunisticShare": 0.30,
    "ability": { "dist": "beta", "alpha": 3, "beta": 2 }
  },
  "fiscalizers": {
    "competentHonestShare": 0.60,
    "weakHonestShare": 0.25,
    "capturableShare": 0.15,
    "competence": { "dist": "beta", "alpha": 4, "beta": 2 }
  },
  "attacks": {
    "salienceCascade": { "enabled": true, "severity": "medium", "socialProofWeight": 3.0 },
    "weakVerificationDiversion": { "enabled": true, "severity": "medium", "baseDetection": 0.25 },
    "agendaCapture": { "enabled": false },
    "fiscalizerCollusion": { "enabled": false },
    "coordinatedSignalBias": { "enabled": false }
  },
  "architectures": [
    "status_quo",
    "participatory_weak_verification",
    "core_v0_simple"
  ],
  "outputs": {
    "rawJson": true,
    "markdownTable": true,
    "csv": true,
    "sampleDecisionTrace": false
  }
}
```

## Scenario design levels

### Debug scenario

Used to inspect logic.

```text
100 citizens
20 projects
6 cycles
1-3 seeds
verbose traces enabled
```

### Paper scenario

Used for reported experiments.

```text
10,000 citizens
40-200 projects
24 cycles
20-100 seeds
paired architecture comparison
```

### Stress scenario

Used only after the engine is stable.

```text
50,000-100,000 citizens
1,000 projects
24-60 cycles
large parameter sweeps
```

## Scenario families

### Baseline-medium

A medium adversarial scenario combining low attention, moderate salience, moderate opportunism, and moderate verification difficulty.

Purpose:

```text
first fair comparison across architectures
```

### High-salience

Increases social-proof amplification and discovery concentration.

Purpose:

```text
test whether funding caps, defaults, and discovery controls prevent popularity cascades
```

### Weak-verification

Lowers detection probability and increases diversion payoff.

Purpose:

```text
test milestone gating, retention, fiscalization, and reputation memory
```

### Agenda-capture

Adds bias to planning-scope construction or central project selection.

Purpose:

```text
test how much downstream distributed allocation can correct upstream agenda bias
```

### Thin-verifier-market

Reduces fiscalizer market depth and increases repeat pairings.

Purpose:

```text
test whether fiscalization collapses when independent review capacity is scarce
```

### Reputation-lock-in

Increases weight placed on reputation in future assignments or selections.

Purpose:

```text
test whether reputation improves quality or merely concentrates opportunity
```

## Configuration inheritance

Later implementations may allow scenario files to inherit from a base file.

Example:

```json
{
  "extends": "baseline-medium.json",
  "scenario_id": "high-salience",
  "attacks": {
    "salienceCascade": {
      "enabled": true,
      "severity": "high",
      "socialProofWeight": 6.0
    }
  }
}
```

The v0 engine may avoid inheritance for simplicity and use complete files instead.

## Architecture configuration

Each architecture should have a declared rule set.

Example:

```json
{
  "architecture_id": "core_v0_simple",
  "rules": {
    "citizenAllocation": true,
    "defaultLayer": true,
    "fundingCaps": true,
    "evidenceContract": true,
    "milestoneGating": true,
    "retention": true,
    "independentFiscalization": true,
    "reputationMemory": true,
    "auditAfterFactOnly": false
  }
}
```

For v0, architecture configs may be implemented as source modules rather than separate JSON files, but the active rule set should still be printed in the output.

## Run identity

Every output should record:

```text
scenario_id
scenario_version
architecture_id
attack_id(s)
seed
run_index
code_version or commit_sha where available
```

## Result headers

Every generated table should include at least:

```text
scenario
runs
base seed
cycles
citizens
projects
active architectures
active attacks
primary metric
```

Example:

```text
scenario: baseline-medium
runs: 20
base seed: 1
N: 10,000
active projects: 40
cycles: 24
architectures: status_quo, participatory_weak_verification, core_v0_simple
attacks: salienceCascade=medium, weakVerificationDiversion=medium
primary metric: delivered verified social value per budget
```

## Reproducibility discipline

A result is reproducible only if the repository contains:

- scenario file;
- code version;
- seed list;
- architecture list;
- metric definition;
- result table;
- raw output.

## Pre-registration discipline

Before a headline experiment is run, freeze:

- scenario file;
- architectures;
- attacks;
- severity levels;
- primary metric;
- prediction;
- withdrawal condition if applicable.

Example prediction record:

```text
Experiment: E1
Scenario: baseline-medium
Prediction: Core v0 simple will reduce leakage and visibility gap relative to status quo and PB-like weak verification, but may not improve selection quality when the planning vector is weak.
Withdrawal condition: If Core v0 does not improve delivered verified value under the medium scenario, the headline claim is withdrawn and replaced by an ablation-specific claim.
```

## Design rule

> A scenario is part of the evidence. Treat it like data, not like a hidden setting.
