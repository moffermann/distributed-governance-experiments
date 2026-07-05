# Planning Information Model

## Purpose

This document defines how the adversarial ABM represents planning information.

It separates three concepts that must not be conflated:

```text
latent public value
central planning signal
distributed planning signal
```

This distinction is load-bearing for the satellite paper.

## Core problem

A central planner may follow a plan faithfully and still allocate poorly if the plan was constructed far from the real needs, preferences, and lived information of beneficiaries.

The problem is not only execution failure after planning.

The problem is also information loss during planning.

This is the institutional version of the Friedman spending problem: when decision-makers spend other people's money on other people, the informational and incentive link between real value and allocation can weaken.

## Latent public value

Each project has a simulated ground-truth value:

```text
latentValue
```

This value is known to the simulator but not directly known to agents.

It represents the public value the project would generate if selected and executed well.

## Central planning signal

The central planner receives a low-information planning signal:

```text
centralPlanningWeight
```

In the baseline scenario, this signal is generated as:

```text
centralPlanningWeight = centralPlanningSignalMix * latentValue
                      + (1 - centralPlanningSignalMix) * noise
```

Baseline:

```text
centralPlanningSignalMix = 0.15
```

Interpretation:

The central plan is only weakly related to latent value.

This models information loss between real beneficiary value and centralized planning priorities.

## Distributed planning signal

The distributed planning/default layer receives a higher-information signal:

```text
distributedPlanningWeight
```

In the baseline scenario, this is generated as:

```text
distributedPlanningWeight = distributedPlanningSignalMix * latentValue
                          + (1 - distributedPlanningSignalMix) * noise
```

Baseline:

```text
distributedPlanningSignalMix = 0.70
```

Interpretation:

The distributed planning signal is closer to latent value because it represents aggregated signals from citizens, beneficiaries, affected parties, local knowledge, evidence, and parallel social prioritization.

This is not full open-mode planning yet. It is a first simplified proxy for distributed parallel planning in a tutored or semi-open simulation.

## Salience

The simulation also generates:

```text
salience
```

Salience is weakly correlated with latent value, but mostly independent:

```text
salience = salienceCorrelation * latentValue
         + (1 - salienceCorrelation) * noise
```

Baseline:

```text
salienceCorrelation = 0.20
```

Salience models visibility, attractiveness, popularity, emotional pull, or platform attention, not public value.

## Architecture use of planning signals

## `status_quo`

Uses:

```text
centralPlanningWeight
```

Interpretation:

The centralized status quo selects projects through a central planning vector that is weakly correlated with latent value.

## `participatory_weak_verification`

Uses no planning signal for passive allocation.

Interpretation:

Only active citizens allocate; passive capacity remains unspent.

## `participatory_weak_verification_full_budget`

Uses salience for passive allocation.

Interpretation:

The passive share is absorbed through visibility/popularity rather than planning or value-informed defaults.

## `core_v0_tutored_central_planning`

Uses:

```text
centralPlanningWeight
```

Interpretation:

This approximates a tutored Core v0 deployment where the authority still provides the default planning vector, but the execution, evidence, fiscalization, retention, and reputation mechanisms are stronger.

## `core_v0_tutored_distributed_planning`

Uses:

```text
distributedPlanningWeight
```

Interpretation:

This approximates a tutored or semi-open Core v0 deployment with a parallel distributed planning/default vector built closer to citizen and beneficiary information.

It is not yet mature open mode.

It is a simplified first implementation of the idea that society can construct a more informative planning layer than a central planner disconnected from beneficiary needs.

## What is not implemented yet

The v0.3 simulator does not yet implement a full distributed planning institution.

It does not yet model:

- individual citizen signals per project;
- beneficiary signal coverage;
- strategic signal manipulation;
- signal aggregation rules;
- deliberation over planning weights;
- agenda-capture countermeasures;
- formal open-mode meta-governance.

Those are future extensions.

For now, `distributedPlanningWeight` is a simplified proxy.

## Reported correlations

The simulator reports effective correlations:

```text
centralPlanningValueCorrelation
distributedPlanningValueCorrelation
salienceValueCorrelation
```

These are measured per run and summarized across runs.

This is necessary because the declared mix parameter is not identical to the realized Pearson correlation in a small project world.

## Why this matters

Planning quality can dominate results.

A strong central planner can make the status quo look good.

A weak central planner can make the status quo fail before execution begins.

A strong distributed planning signal can improve Core v0's default layer.

A captured or biased distributed signal can become a new failure mode.

Therefore, planning information must be explicit, measured, and varied through sensitivity analysis.

## Design rule

> Never compare architectures without reporting how strongly each planning signal correlates with latent public value.
