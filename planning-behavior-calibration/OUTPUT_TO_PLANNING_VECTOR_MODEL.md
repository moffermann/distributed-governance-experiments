# Output to Planning Vector Model

## Purpose

This document defines how behavioral calibration outputs feed into:

```text
experiments/planning-vector-construction/
```

## Parameters calibrated by this experiment

Primary outputs:

```text
delegatePlatformUseRate
delegatePlanningCoverage
delegateAlignment
delegateReportQuality
delegateRevocationResponsiveness
reportReadProbability
revocationLikelihoodAfterMisalignment
delegationProbability
preferredDelegateTypeDistribution
```

## Mapping to planning-vector scenarios

Example mapping:

```text
family_proxy_high_trust
→ core_v0_open_family_proxy_high_trust

trusted_microdelegation
→ core_v0_open_trusted_microdelegation

local/community delegate
→ core_v0_open_mixed_trusted_delegation

institutional delegate
→ core_v0_open_institutional_delegate_emergence

plural bloc delegate
→ core_v0_open_plural_delegation_concentrated
```

## Distribution use

The planning-vector model should not only use means.

For each scenario, it should support:

```text
p25
p50
p75
p05
p95
random draw with fixed seed
```

This allows sensitivity analysis:

```text
conservative case
median case
optimistic case
stress case
```

## Example fitted-prior input

```json
{
  "core_v0_open_trusted_microdelegation": {
    "delegatePlatformUseRate": {
      "dist": "beta",
      "alpha": 7.2,
      "beta": 3.1,
      "mean": 0.70,
      "p25": 0.61,
      "p50": 0.72,
      "p75": 0.80
    },
    "delegatePlanningCoverage": {
      "dist": "beta",
      "alpha": 4.0,
      "beta": 5.0,
      "mean": 0.44,
      "p25": 0.32,
      "p50": 0.43,
      "p75": 0.56
    }
  }
}
```

## Reproducibility rule

The planning-vector model should record:

```text
behavioral_prior_source
prior_version
respondent_source: llm / human / expert / pilot
archetype mapping
selected quantile or random seed
```

## Interpretation rule

Do not write:

```text
Delegates use the platform 70% of the time.
```

Write:

```text
Under the LLM-calibrated trusted-microdelegation prior, the fitted median delegate platform-use rate is approximately 70%; the planning-vector model is tested across lower and upper quantiles.
```

## Design rule

> Behavioral calibration produces distributions; planning-vector construction consumes distributions.
