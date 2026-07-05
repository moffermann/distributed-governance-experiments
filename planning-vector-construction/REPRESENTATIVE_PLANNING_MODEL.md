# Representative Planning Model

## Purpose

This document defines how the experiment models central representative planning.

The goal is to avoid an arbitrary assumption that central planning is poorly correlated with latent public value.

Instead, the model derives central planning quality from representation, approval, mandate fidelity, and institutional distortion.

## Core intuition

A representative government may follow a plan and still produce a weak planning vector if the plan is only weakly connected to the population's latent expected value.

The information loss can occur before execution.

## Representation chain

The representative planning vector is modeled as:

```text
population expected values
→ voters
→ winner coalition
→ approved coalition
→ promised program
→ actual plan
→ central planning vector
```

## Baseline objects

### Citizens

Each citizen has:

```text
citizen_id
territory
group_id
beneficiary_profile
issue_preference_vector
turnout_probability
candidate_alignment_vector
approval_probability
```

### Issues / needs / projects

Each possible planning target has:

```text
target_id
territory
issue_category
beneficiary_group
visibility
individual_expected_value_by_citizen
latent_social_value
```

### Representative actor

The governing actor has:

```text
winner_vote_share
turnout_rate
approval_rate
supporter_alignment
non_supporter_alignment
program_fidelity
technocratic_capacity
bureaucratic_distortion
coalition_distortion
lobbying_distortion
beneficiary_distance
```

## Effective mandate share

A simple first proxy:

```text
electoral_mandate_share = turnout_rate * winner_vote_share
```

Example:

```text
turnout_rate = 0.555
winner_vote_share = 0.52

electoral_mandate_share = 0.2886
```

This does not mean only 28.86% of the population is governed.

It means the winner's direct electoral support contains a compressed subset of population information.

## Approval-adjusted alignment

Approval is treated as a proxy for surviving perceived alignment after governing begins.

It does not directly equal plan-value correlation.

But it can help estimate how much of the population still sees the governing plan as aligned with expected value.

Baseline proxy:

```text
approved_share = approval_rate
non_approved_share = 1 - approval_rate
```

The central plan is more aligned with the approved group than the non-approved group:

```text
supporter_alignment > non_supporter_alignment
```

## Representative preference vector

A simple first version:

```text
supporter_vector = mean_expected_value(approved_or_supporting_group)
non_supporter_vector = mean_expected_value(non_supporting_group)
```

Then:

```text
representative_preference_vector =
    supporter_alignment * approval_rate * supporter_vector
  + non_supporter_alignment * (1 - approval_rate) * non_supporter_vector
```

This models partial inclusion of non-supporter preferences, but with lower weight.

## Program-to-plan fidelity

The plan actually implemented may drift from the program voters expected.

```text
program_fidelity ∈ [0, 1]
```

Where:

```text
1 = actual plan matches promised program
0 = actual plan unrelated to promised program
```

Program drift:

```text
actual_program_vector = program_fidelity * representative_preference_vector
                      + (1 - program_fidelity) * political_drift_vector
```

## Institutional distortion

Central planning may be further distorted by:

- coalition bargaining;
- bureaucracy;
- lobbying;
- budget rigidity;
- national media salience;
- distance from local beneficiaries;
- administrative inertia.

A first proxy:

```text
institutional_distortion =
    bureaucratic_distortion
  + coalition_distortion
  + lobbying_distortion
  + beneficiary_distance
```

The central planning vector can be modeled as:

```text
central_plan_raw =
    (1 - institutional_distortion) * actual_program_vector
  + technocratic_capacity * technocratic_signal
  + lobbying_distortion * organized_interest_vector
  + bureaucratic_distortion * inertia_vector
  + noise
```

Then normalize to a bounded planning vector.

## Technocratic capacity

The central state may have real technical information.

This should not be ignored.

```text
technocratic_signal = latent_social_value + noise
```

Technocratic capacity can improve correlation even if electoral alignment is weak.

Scenarios should distinguish:

```text
low democratic alignment + low technocratic capacity
low democratic alignment + high technocratic capacity
high democratic alignment + low technocratic capacity
high democratic alignment + high technocratic capacity
```

## Recommended baseline priors

These are initial simulation priors, not empirical claims.

```text
turnout_rate = 0.555
winner_vote_share = 0.52
approval_rate = 0.40
supporter_alignment = 0.70
non_supporter_alignment = 0.15
program_fidelity = 0.60
technocratic_capacity = 0.20
bureaucratic_distortion = 0.15
coalition_distortion = 0.10
lobbying_distortion = 0.10
beneficiary_distance = 0.15
```

Interpretation:

The central plan is not random.

It contains some electoral, approval, and technocratic information.

But much of the population's expected value is compressed, underweighted, or distorted before becoming a planning vector.

## Scenario variants

### Central low alignment

```text
turnout_rate = 0.555
winner_vote_share = 0.52
approval_rate = 0.30
program_fidelity = 0.45
technocratic_capacity = 0.15
institutional_distortion = high
```

### Central median alignment

```text
approval_rate = 0.40
program_fidelity = 0.60
technocratic_capacity = 0.20
institutional_distortion = medium
```

### Central high alignment

```text
approval_rate = 0.60
program_fidelity = 0.75
technocratic_capacity = 0.30
institutional_distortion = low-medium
```

### Technocratic high-capacity central planning

```text
approval_rate = 0.40
program_fidelity = 0.55
technocratic_capacity = 0.55
institutional_distortion = medium
```

This scenario is important because central planning should be allowed to perform well where the state has high technical capacity.

## Metrics

Primary:

```text
corr(central_plan, latent_social_value)
```

Secondary:

```text
supporter_alignment_score
non_supporter_alignment_score
minority_loss
beneficiary_distance_loss
program_drift_loss
technocratic_recovery
organized_interest_distortion
```

## Interpretation rule

Do not interpret approval as correlation.

Approval is one input to the alignment-loss mechanism.

The actual output is the measured correlation between the generated central planning vector and latent social value.

## Design rule

> The central planner should be allowed to win when representative alignment, program fidelity, and technocratic capacity are high.
