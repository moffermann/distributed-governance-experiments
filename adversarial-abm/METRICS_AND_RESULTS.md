# Metrics and Result Discipline

## Purpose

This document defines the initial metric family and interpretation discipline for the adversarial ABM satellite project.

The simulation should not optimize for participation, funding volume, or formal completion alone. It should measure whether public resources become delivered, verified social value.

## Primary metric

```text
delivered verified social value per unit of public budget
```

Short form:

```text
DVV / budget
```

This is the central outcome metric because the purpose of public allocation is not to allocate money, produce reports, or mark projects complete. The purpose is to deliver value to the society that funded the budget.

## Metric decomposition

Delivered verified value should be decomposed into at least four stages:

```text
potential value
selected value
executed value
verified delivered value
```

### Potential value

The latent value available in the project universe.

This is not directly visible to agents, but exists in the simulation as ground truth.

### Selected value

The value of projects selected or funded by an architecture.

This measures allocation quality.

### Executed value

The value that would be delivered after executor behavior, effort, failure, or diversion.

This measures delivery quality.

### Verified delivered value

The delivered value that is detected, verified, or credibly recorded by the system.

This measures accountability and visibility.

## Core formula concept

A simple first version may define:

```text
project_delivered_value = latent_value * execution_quality * non_diverted_share * verification_status_weight
```

A later version may separate:

```text
beneficiary value
common-good value
territorial value
continuity value
antivalue penalty
verification confidence
```

## Primary comparisons

The simulator should compare:

```text
architecture A vs architecture B
under same world
same agents
same attacks
same seed
```

The preferred comparison is paired:

```text
DVV_A(seed_i) - DVV_B(seed_i)
```

not independent averages alone.

## Selection metrics

These measure whether the architecture funds valuable projects.

- selected-value mean;
- funded-project latent quality;
- quality gap between funded and unfunded projects;
- correlation between funding and latent value;
- correlation between funding and salience;
- share of budget captured by high-salience low-value projects;
- value lost to agenda exclusion;
- passive-flow dependence on planning weights.

## Delivery metrics

These measure whether selected projects actually deliver.

- execution quality;
- diversion rate;
- milestone completion quality;
- leakage rate;
- verified delivery ratio;
- delivery delay;
- unrecoverable early release;
- retained funds used for correction;
- guarantee recovery rate.

## Verification and accountability metrics

These measure whether the system sees what happened.

- detection probability;
- false approval rate;
- false rejection rate;
- reported completion;
- real completion;
- visibility gap:

```text
reported completion - real delivered value
```

- evidence sufficiency rate;
- contradiction discovery rate;
- complaint founded rate;
- time from issue to review;
- responsibility event creation rate;
- repeat-offender persistence.

## Concentration metrics

These measure capture, lock-in, and cascade effects.

- funding Gini;
- executor assignment Gini;
- fiscalizer assignment concentration;
- delegate represented-weight concentration;
- top-salience share;
- top-executor share;
- repeated actor-pair frequency;
- cluster capture share;
- entrant survival rate.

## Participation and attention metrics

These measure citizen-side feasibility.

- active evaluator share;
- passive share;
- profile-driven share;
- delegated share;
- untouched-default share;
- participation decay;
- attention cost per decision;
- quality sensitivity to active attention;
- value loss from rational ignorance.

## Adversarial robustness metrics

These measure resilience under attacks.

- value retained under attack severity;
- attack success rate;
- attack detected before harm;
- attack detected after harm;
- attack hidden;
- attack visible but unresolved;
- honest actor collateral damage;
- administrative burden added by defense;
- robustness frontier across attack severity.

## Administrative burden metrics

These are important because an architecture can win on value but fail operationally.

- review workload;
- fiscalizer workload;
- number of generated disputes;
- number of warnings;
- number of Yellow cases;
- number of Red blockers;
- average time to execution-ready state;
- cost of control as share of project budget;
- projects abandoned due to procedural burden;
- honest low-margin executor exclusion.

## Equity and distribution metrics

These should be added once the first model is stable.

- territorial funding distribution;
- low-salience group funding;
- vulnerable-beneficiary coverage;
- dense-zone capture;
- preventive versus remedial funding;
- long-horizon versus short-horizon funding;
- effect of default weights on distribution.

## Result-status labels

Every headline result should be labeled by evidence status:

```text
FORMAL       — derived from a stated model or proposition
SIMULATED    — produced by ABM under declared assumptions
CALIBRATED   — parameterized from external empirical sources
SENSITIVITY  — robustness or parameter sweep result
POST-HOC     — not pre-registered; exploratory
PILOT        — future real-world result, not yet available
```

## Interpretation discipline

### Avoid overclaiming

Do not write:

```text
The architecture delivers 2x the status quo.
```

Write:

```text
In the simulated environment under the stated calibrated parameters, the architecture delivers 2x the modeled baseline.
```

### Separate direction from magnitude

Some results may support direction but not precise effect size.

Use:

```text
supports directional claim
magnitude parameter-dependent
```

where appropriate.

### Identify result-determining assumptions

Each experiment should report the assumptions most responsible for the result, such as:

- detection probability;
- signal bias;
- planner bandwidth;
- social-proof strength;
- fiscalizer market depth;
- reputation memory strength;
- executor cost distribution;
- corruption payoff;
- citizen attention share.

### Preserve negative results

Failed predictions are valuable. Each failed prediction should produce one of:

- revised mechanism claim;
- bounded limitation;
- new attack scenario;
- pilot instrumentation requirement.

## Minimum output table for each experiment

Each experiment should report:

| Field | Description |
|---|---|
| Experiment ID | Stable identifier, e.g. E8-A1 |
| Architectures compared | Which institutional models are tested |
| Attack scenario | Attack type and severity |
| Seeds / runs | Reproducibility details |
| Primary metric | DVV / budget unless justified otherwise |
| Secondary metrics | Concentration, leakage, visibility gap, etc. |
| Prediction | Pre-run expectation |
| Result | Numeric result |
| Interpretation | What the result supports |
| Failed prediction? | Yes/no and why |
| Result-determining assumptions | Parameters that matter most |
| Claim status | Supported, weakened, bounded, failed |
| Next validation | Sensitivity, calibration, pilot, external review |

## Design rule

> The metric system should punish hidden failure, not reward official completion.
