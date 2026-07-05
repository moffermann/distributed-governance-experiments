# Scenario Taxonomy

## Purpose

This document clarifies the difference between scenarios, architectures, operating modes, and planning models in the adversarial ABM.

The first executable simulations should not be read as full Core v0, full open mode, or a complete model of public administration.

## Four separate concepts

The simulator separates:

```text
scenario
architecture
operating-mode approximation
planning model
```

## 1. Scenario

A scenario is the synthetic environment being tested.

It defines:

- population size;
- project world;
- distributions;
- attack severity;
- seed and run count;
- architectures compared;
- output settings.

Example:

```text
baseline-medium v0.3
```

This is not an operating mode. It is a test environment.

## 2. Architecture

An architecture is an institutional rule set tested inside the scenario.

Examples:

```text
status_quo
participatory_weak_verification
participatory_weak_verification_full_budget
core_v0_tutored_central_planning
core_v0_tutored_distributed_planning
```

The architecture determines:

- who allocates;
- whether passive budget is used;
- what planning signal is followed;
- whether funding caps exist;
- detection strength;
- review confidence;
- retention;
- guarantees;
- reputational memory.

## 3. Operating-mode approximation

The current simulator does not implement full Core v0 operating modes.

It approximates them.

### Status quo

Approximates a central public allocation model with weak delivery verification and weak reputational memory.

### Weak participatory models

Approximate participatory or civic-platform allocation without strong evidential contracts, conditional disbursement, or role-specific reputational memory.

### Core v0 tutored-central planning

Approximates a tutored Core v0 deployment where the public authority still provides the planning/default vector, but Core v0's downstream controls are active.

### Core v0 tutored-distributed planning

Approximates a tutored or semi-open Core v0 deployment where a parallel distributed planning/default vector is available and closer to beneficiary/citizen information.

### Open mode

Not implemented yet.

Open mode would require:

- open construction of planning scopes;
- protocolized rule-change governance;
- signal elicitation mechanics;
- anti-capture controls;
- meta-governance rules.

## 4. Planning model

Planning determines the priority vector used for central selection or passive/default allocation.

The current simulator distinguishes:

```text
centralPlanningWeight
distributedPlanningWeight
salience
```

### Central planning

Used by:

```text
status_quo
core_v0_tutored_central_planning
```

Baseline signal quality:

```text
centralPlanningSignalMix = 0.15
```

Interpretation:

Central planning is weakly correlated with latent value because it is distant from real beneficiary needs.

### Distributed parallel planning

Used by:

```text
core_v0_tutored_distributed_planning
```

Baseline signal quality:

```text
distributedPlanningSignalMix = 0.70
```

Interpretation:

Distributed planning is modeled as closer to latent value because it aggregates more local, beneficiary, citizen, and social information.

This is a proxy, not yet a full open-planning institution.

### Salience allocation

Used by:

```text
participatory_weak_verification_full_budget
```

Interpretation:

Passive budget is absorbed through visibility/popularity rather than value-informed planning.

## Current baseline variants

| Variant | Allocation | Passive/default budget | Planning signal | Verification | Approximation |
|---|---|---|---|---|---|
| `status_quo` | central authority | central allocation | central low-information | weak | centralized state allocation |
| `participatory_weak_verification` | active citizens only | unspent | none | weak | low-absorption participation |
| `participatory_weak_verification_full_budget` | citizens + passive salience | salience | none | weak | salience-driven participation |
| `core_v0_tutored_central_planning` | citizens + default | central low-information | central | strong | tutored Core v0 with authority default |
| `core_v0_tutored_distributed_planning` | citizens + default | distributed higher-information | distributed | strong | tutored/semi-open Core v0 with parallel social planning |

## Interpretation warning

Do not interpret current results as:

```text
Core v0 open mode beats the status quo.
```

The current simulator can only support narrower statements, such as:

```text
Under the baseline synthetic world, Core v0 with distributed-parallel planning and stronger verification performs differently from status quo central low-information planning with weak verification.
```

## Design rule

> Never say Core v0 wins without naming the operating-mode approximation and planning model being tested.
