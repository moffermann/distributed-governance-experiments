# Design Baseline — Planning Vector Construction

## Purpose

This document defines the initial design for the planning-vector construction experiment.

The experiment asks how different governance mechanisms construct a planning vector before money is allocated.

It is upstream of the adversarial ABM.

## Core question

```text
How much of the population's latent expected public value survives into the planning vector under representative central planning versus distributed planning?
```

## Why this matters

In the adversarial ABM, a planning vector can dominate results.

If the central planner receives a planning vector strongly correlated with latent value, the status quo can select valuable projects even if execution accountability is weak.

If the central planner receives a weakly correlated planning vector, the status quo loses value before execution starts.

Therefore, the model should not assign planning-vector quality arbitrarily.

It should derive planning-vector quality from a representation and information-transmission model.

## Conceptual distinction

The experiment distinguishes:

```text
individual expected value
latent social value
representative planning vector
distributed planning vector
salience vector
```

## Individual expected value

Each citizen has an expected value for each possible public need, issue, or project.

```text
V[i, j] = expected value citizen i assigns to need/project j
```

This can vary by:

- territory;
- income group;
- beneficiary status;
- ideology;
- service exposure;
- salience exposure;
- issue knowledge.

## Latent social value

The simulator's ground-truth social value is an aggregation of individual expected values.

Baseline:

```text
L[j] = weighted_mean_i(V[i, j])
```

Later versions may add:

- beneficiary weights;
- protected-floor weights;
- continuity weights;
- antivalue penalties;
- common-good weights.

## Representative planning vector

A representative planning vector is produced through a chain:

```text
citizen preferences
→ turnout
→ vote choice
→ winner coalition
→ approval / disapproval
→ promised program
→ actual governing plan
→ bureaucratic / coalition / lobbying distortion
→ central planning vector
```

At each step, information may be lost or distorted.

## Distributed planning vector

A distributed planning vector is produced through a different chain:

```text
citizen signals
+ beneficiary signals
+ affected-party signals
+ local evidence
+ expert signals
+ deliberative correction
- salience distortion
- strategic manipulation
→ distributed planning vector
```

This vector may be closer to latent social value when coverage is good, beneficiary signals are included, and capture controls work.

It may be worse than central planning when coverage is thin, participation is biased, salience dominates, or organized groups manipulate signals.

## Experiment structure

The experiment should generate:

1. a population of citizens;
2. a universe of needs/projects;
3. an individual expected-value matrix;
4. a latent social-value vector;
5. a central representative planning vector;
6. a distributed planning vector;
7. a salience vector;
8. comparison metrics.

## Main output metrics

Primary:

```text
corr(representative_plan, latent_social_value)
corr(distributed_plan, latent_social_value)
corr(salience_vector, latent_social_value)
```

Secondary:

```text
coverage
minority preference loss
approval-weighted alignment
beneficiary value recovery
salience distortion
strategic manipulation sensitivity
planning error by group
planning error by territory
planning error by beneficiary status
```

## Mechanism comparison

The first version should compare at least:

1. representative central planning with low approval;
2. representative central planning with median approval;
3. representative central planning with high approval;
4. technocratic central planning with weak democratic linkage;
5. distributed planning with low signal coverage;
6. distributed planning with beneficiary-weighted signals;
7. distributed planning with high salience bias;
8. distributed planning with coordinated manipulation;
9. hybrid planning: representative mandate plus distributed correction.

## Key hypothesis

The planning vector used by a central representative regime is not weak because the planner necessarily ignores planning.

It is weak because the planning vector is filtered through representation, winner-take-mandate compression, approval limits, program drift, institutional distortion, and distance from beneficiaries.

## Research contribution

This experiment can contribute a reusable method for estimating planning-signal quality from representation parameters rather than assuming planning quality directly.

## Relationship to Friedman spending logic

The experiment operationalizes the insight that when decision-makers allocate other people's resources for other people, informational and incentive alignment weakens.

The representative planning model should therefore estimate how much individual expected value survives into a central plan.

The distributed planning model should estimate whether more local information survives when citizens and beneficiaries send direct signals, while accounting for participation and manipulation problems.

## Design rule

> Planning quality must be derived, not assumed.
