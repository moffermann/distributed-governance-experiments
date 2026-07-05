# Probability and Parameter Model

## Purpose

This document defines how probabilities and distributions should be used in the adversarial ABM.

The simulation should not rely on arbitrary hard-coded choices. Agent behavior, project properties, and adversarial pressure should be explicit, parameterized, reproducible, and sensitivity-testable.

## Core principle

Every probabilistic decision should be generated from:

```text
declared distribution
+ scenario parameters
+ architecture modifiers
+ attack severity
+ seeded randomness
```

No important probability should remain hidden inside ad hoc code.

## Parameter classes

Parameters should be classified into four categories.

### 1. Synthetic structural parameter

Used to construct the artificial world.

Example:

```text
latent_public_value ~ Beta(2, 2)
```

This does not claim that real public projects follow that exact distribution. It defines a controlled world for comparison.

### 2. Literature-anchored or audit-anchored parameter

Supported by external empirical literature or audit findings.

Examples:

- leakage estimates;
- audit detection rates;
- participation decay;
- procurement overrun estimates;
- verifier capacity estimates.

These should be documented with source references once used.

### 3. Stress-test parameter

Used to explore robustness across adversarial severities.

Example:

```text
coordinated_signal_bias_share ∈ [0.00, 0.50]
```

This asks when an architecture breaks; it is not a claim about the real-world value of the parameter.

### 4. Pilot-required parameter

A parameter that simulation cannot responsibly fix and should be measured in a real pilot.

Examples:

- real citizen profile adoption rate;
- local fiscalizer market depth;
- true evidence production cost;
- real-world complaint review load.

## Recommended base distributions

### Latent public value

Use a beta distribution because value is bounded between 0 and 1.

Baseline:

```text
latent_public_value ~ Beta(2, 2)
```

Scenario variants:

```text
Beta(1, 3)      many low-value projects, few high-value projects
Beta(3, 1)      optimistic world, many useful projects
Beta(0.8, 0.8)  polarized world, many bad and many good projects
```

### Salience

Salience should be partially but weakly correlated with latent value.

Baseline:

```text
salience = rho_s * latent_public_value + (1 - rho_s) * noise
rho_s = 0.2
noise ~ Uniform(0, 1)
```

Interpretation:

```text
Some valuable projects are visible.
Some visible projects are not valuable.
Visibility is not the same as value.
```

### Planning weight quality

Planning weights should be modeled as noisy estimates of latent value.

Baseline:

```text
planning_weight = rho_w * latent_public_value + (1 - rho_w) * noise
```

Scenarios:

```text
competent planning: rho_w = 0.8
moderate planning:  rho_w = 0.5
weak planning:      rho_w = 0.2
captured planning:  rho_w = 0.5 plus bias
```

### Execution difficulty

Baseline:

```text
execution_difficulty ~ Beta(2, 3)
```

Interpretation:

Most projects are executable, but some are difficult.

### Verification difficulty

Baseline:

```text
verification_difficulty ~ Beta(2, 2)
```

Interpretation:

Some public values are easy to verify; others are intrinsically harder.

### Fraud opportunity

Baseline:

```text
fraud_opportunity ~ Beta(1.5, 3)
```

Alternative structural formula:

```text
fraud_opportunity = 0.4 * budget_complexity
                  + 0.3 * verification_difficulty
                  + 0.3 * advance_payment_exposure
```

### Actor ability

Executor ability:

```text
executor_ability ~ Beta(3, 2)
```

Fiscalizer competence:

```text
fiscalizer_competence ~ Beta(4, 2)
```

Evidence producer competence:

```text
evidence_producer_competence ~ Beta(3, 2)
```

### Costs

Use lognormal distributions for costs where outliers matter.

```text
delivery_cost ~ LogNormal(mu, sigma)
control_cost ~ LogNormal(mu, sigma)
```

Reason:

```text
Most costs cluster around a typical range, but some projects become unusually expensive.
```

## Baseline population shares

Initial citizen distribution:

```text
attentive_evaluators = 0.05
salience_followers  = 0.25
profile_driven      = 0.20
passive_default     = 0.40
delegators          = 0.10
```

Scenario variants:

```text
low civic attention:
  attentive = 0.02
  salience = 0.38
  profile = 0.10
  passive = 0.45
  delegator = 0.05

high civic capacity:
  attentive = 0.12
  salience = 0.18
  profile = 0.35
  passive = 0.25
  delegator = 0.10
```

Executor types:

```text
honest_executor = 0.70
opportunistic_executor = 0.30
```

Fiscalizer types:

```text
competent_honest = 0.60
weak_honest = 0.25
capturable = 0.15
```

These are defaults, not empirical claims.

## Choice functions

### Bernoulli

Used for binary events.

```text
outcome = rng() < p
```

Examples:

- citizen becomes active;
- executor diverts;
- fiscalizer detects;
- complaint is filed;
- evidence is manipulated.

### Logistic

Used when probability depends on weighted incentives.

```text
sigmoid(x) = 1 / (1 + exp(-x))
```

Examples:

```text
P(divert) = sigmoid(beta0 + beta1*gain - beta2*detection - beta3*retention)
P(collude) = sigmoid(bribe - expected_loss + repeat_pairing_trust)
P(exclude) = sigmoid(political_discomfort - visibility_cost)
```

### Softmax

Used when an agent chooses one option among many.

```text
P(i) = exp(score_i / tau) / sum_j exp(score_j / tau)
```

Examples:

- citizen selects visible project;
- proposer selects manipulation strategy;
- delegator selects delegate;
- authority selects projects under limited bandwidth.

Temperature interpretation:

```text
low tau  = more deterministic, top score dominates
high tau = more exploratory, choices spread across options
```

## Architecture modifiers

The same base agent should behave differently under different institutional rules.

Examples:

### Detection probability

```text
status_quo_detection = low
PB_weak_detection = low_to_medium
Core_v0_detection = higher because of evidence contracts, fiscalization, milestone gating
```

### Reputation loss

```text
status_quo_reputation_loss = weak or delayed
Core_v0_reputation_loss = visible, role-specific, persistent but non-exclusionary
```

### Salience exposure

```text
opaque discovery = high social-proof amplification
explainable discovery = reduced hidden amplification
funding caps = cascade truncation
```

### Agenda bias visibility

```text
opaque agenda = low cost of exclusion
versioned planning scope = higher visibility cost
open signal construction = lower unilateral exclusion power but higher signal-bias surface
```

## Attack severity parameters

Each attack should expose severity values.

### Salience cascade

```text
low:     social_proof_weight = 1.0
medium:  social_proof_weight = 3.0
high:    social_proof_weight = 6.0
extreme: social_proof_weight = 10.0
```

### Weak verification diversion

```text
low:
  opportunist_share = 0.15
  base_detection = 0.45

medium:
  opportunist_share = 0.30
  base_detection = 0.25

high:
  opportunist_share = 0.45
  base_detection = 0.12

extreme:
  opportunist_share = 0.60
  base_detection = 0.05
```

### Coordinated signal bias

```text
low:     coordinated_signal_share = 0.05
medium:  coordinated_signal_share = 0.15
high:    coordinated_signal_share = 0.30
extreme: coordinated_signal_share = 0.45
```

### Thin verifier market

```text
low:     market_depth_factor = 0.90
medium:  market_depth_factor = 0.60
high:    market_depth_factor = 0.35
extreme: market_depth_factor = 0.15
```

### Reputation lock-in

```text
low:     reputation_weight = 0.20
medium:  reputation_weight = 0.50
high:    reputation_weight = 0.80
extreme: reputation_weight = 1.20
```

## Sensitivity sweeps

Every headline result should be stress-tested through parameter sweeps.

Example:

```text
for opportunist_share in [0.1, 0.2, 0.3, 0.4, 0.5]:
  for detection_probability in [0.05, 0.1, 0.2, 0.4, 0.6]:
    compare architectures
```

Useful outputs:

```text
Core v0 wins above detection threshold X
PB collapses above salience weight Y
central planning wins when planner capacity covers Z% of project world
open signals lose when coordinated bias exceeds B%
thin verifier markets destroy fiscalization below depth D
```

## Scenario configuration rule

Parameters should live in scenario files rather than inside code whenever possible.

Example location:

```text
experiments/adversarial-abm/scenarios/baseline-medium.json
```

The engine should read a scenario and report it with results.

## Reporting discipline

Do not report a parameterized result as if it were empirical fact.

Avoid:

```text
Fraud probability is 30%.
```

Use:

```text
In the medium adversarial scenario, opportunistic executors are initialized at 30%; sensitivity analysis varies this from 10% to 50%.
```

Avoid:

```text
Core v0 delivers twice the status quo.
```

Use:

```text
Under the declared simulated world and parameter range, Core v0 delivers X times the modeled baseline.
```

## Design rule

> Parameters should be easy to attack, easy to change, and impossible to hide.
