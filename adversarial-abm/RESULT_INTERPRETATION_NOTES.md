# Result Interpretation Notes

## Purpose

This document explains how to read the first adversarial ABM result tables.

The goal is to avoid confusing four different things:

```text
budget absorption
actual delivered value
verified delivered value
reported value
```

An architecture can look strong on one dimension and weak on another.

## 1. Budget absorption

Budget absorption answers:

```text
How much of the available public allocation was actually committed to projects?
```

Metrics:

```text
budgetSpent
budgetUtilizationRate
unspentBudgetRate
```

A low-performing architecture may fail because:

- it spends badly;
- it cannot absorb available budget;
- participation is too low;
- its discovery layer cannot route passive citizens;
- projects fail to close funding.

These are different failures.

For this reason, the simulator now includes both:

```text
participatory_weak_verification
participatory_weak_verification_full_budget
```

The first exposes low absorption under weak participation/default design.

The second forces full budget flow through weak participatory/salience allocation so that weak verification can be examined separately from unused budget.

## 2. Actual value per budget

Actual value answers:

```text
How much real value was delivered in the simulated world?
```

Metric:

```text
actualValuePerBudget
```

This is based on the simulator's latent ground truth and execution outcome.

It is not necessarily visible to citizens or institutions.

A centralized planner may score well here if its planning signal is correlated with latent value.

## 3. Verified value per budget

Verified value answers:

```text
How much of the delivered value is detected, reviewed, or credibly visible under the architecture?
```

Metric:

```text
verifiedValuePerBudget
```

This is closer to the master paper's accountability claim.

An architecture can deliver some real value but fail to verify it.

An architecture can also report success without verifying real delivery.

## 4. Reported value per budget

Reported value answers:

```text
How much value appears to have been completed according to reported or administratively visible completion?
```

Metric:

```text
reportedValuePerBudget
```

This can exceed actual delivered value when diversion, weak verification, or self-reporting allow false completion.

## 5. Visibility gap

Visibility gap answers:

```text
How much reported value exceeds actual delivered value?
```

Metric:

```text
visibilityGapPerBudget = reportedValuePerBudget - actualValuePerBudget
```

A high visibility gap means the architecture is producing official confidence faster than real value.

## 6. Leakage

Leakage answers:

```text
How much committed budget was diverted or lost through opportunistic execution?
```

Metric:

```text
leakageRate
```

This is separate from low project quality. A low-value project can be honestly executed, and a high-value project can leak.

## 7. Selection quality

Selection quality answers:

```text
Did the architecture fund projects correlated with latent public value?
```

Metrics:

```text
selectionValueCorrelation
qualityGap
```

This measures allocation quality, not execution or verification quality.

## 8. Concentration

Concentration answers:

```text
Did funding concentrate in a small set of projects or high-salience projects?
```

Metrics:

```text
fundingGini
topSalienceFundingShare
```

Concentration is not always bad, but under salience attack it may indicate cascade vulnerability.

## Initial interpretation discipline

Do not read a result as:

```text
Architecture X wins.
```

Read it as:

```text
Architecture X performs better on metric M under scenario S with assumptions A.
```

Examples:

```text
Core v0 may reduce leakage and visibility gap while not necessarily maximizing actual value under a competent planner scenario.

A participatory weak-verification model may fail by low budget absorption unless a full-budget variant is tested.

A full-budget participatory variant may spend all available budget but still perform poorly on verified value if verification remains weak.
```

## Design rule

> Always distinguish allocation, absorption, execution, verification, and reporting before drawing institutional conclusions.
