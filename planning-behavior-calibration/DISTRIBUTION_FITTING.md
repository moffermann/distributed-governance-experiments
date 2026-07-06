# Distribution Fitting

## Purpose

This document defines how structured LLM or human responses should be converted into parameter distributions.

The planning-vector model should not use a single hand-picked value when a behavioral variable is uncertain.

It should use fitted distributions.

## Input data

Validated responses should contain values in `[0, 1]` for variables such as:

```text
direct_participation_probability
delegation_probability
report_read_probability_short
report_read_probability_detailed
revocation_likelihood_after_misalignment
revocation_likelihood_after_inactivity
delegate_platform_use_rate
delegate_planning_coverage
alignment_with_close_delegator
alignment_with_impersonal_delegators
```

## Recommended distributions

## Beta distribution

Use for most bounded variables in `[0, 1]`.

Examples:

```text
delegate_platform_use_rate ~ Beta(alpha, beta)
delegate_planning_coverage ~ Beta(alpha, beta)
revocation_likelihood_after_misalignment ~ Beta(alpha, beta)
```

## Mixture of Betas

Use when responses appear multimodal.

Example:

```text
family_proxy may split into highly active helpers and low-activity helpers
```

## Logit-normal

Use when values are bounded but have heavy tails after transformation.

## Categorical / multinomial

Use for delegate-type preferences.

Example:

```text
preferred_delegate_type_distribution
```

## Dirichlet

Use for multi-channel allocation weights where the components must sum to 1.

## Required plots

For each variable and archetype:

```text
histogram
density estimate
boxplot or violin plot
empirical CDF
fitted distribution overlay
5th / 50th / 95th percentile markers
```

For relationships:

```text
correlation matrix
scatter: platform use vs planning coverage
scatter: report read vs revocation likelihood
scatter: alignment vs delegate type
scatter: digital literacy vs delegation probability
```

## LLM vs human comparison

When human data exist, compare:

```text
mean difference
median difference
variance difference
Kolmogorov-Smirnov distance
Wasserstein distance
quantile differences
correlation structure
```

## Reproducibility

Store:

```text
raw responses
validated responses
normalization code
fitted distribution parameters
random seed
fitting method
plots
```

The planning-vector model should read fitted distributions from an exported JSON file rather than calling the LLM directly.

## Output file

Recommended output:

```text
data/fitted/behavioral_priors_v0.json
```

Example:

```json
{
  "family_proxy_high_trust": {
    "delegate_platform_use_rate": {
      "dist": "beta",
      "alpha": 7.2,
      "beta": 3.1,
      "mean": 0.70,
      "p05": 0.45,
      "p50": 0.71,
      "p95": 0.88
    },
    "delegate_planning_coverage": {
      "dist": "beta",
      "alpha": 4.0,
      "beta": 6.2,
      "mean": 0.39,
      "p05": 0.16,
      "p50": 0.38,
      "p95": 0.65
    }
  }
}
```

## Design rule

> Use LLM or human responses to fit behavioral distributions, then freeze those distributions before running planning-vector or ABM simulations.
