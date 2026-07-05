# Distributed Planning Model

## Purpose

This document defines how the experiment models distributed planning.

The goal is to avoid assuming that distributed planning is automatically better than central planning.

Distributed planning is modeled as a signal aggregation mechanism that can gain information from citizens and beneficiaries, but can also lose information through participation bias, salience, noise, and strategic manipulation.

## Core intuition

Distributed planning can be more correlated with latent social value because it can collect signals closer to where value is experienced:

- citizens;
- direct beneficiaries;
- affected parties;
- local organizations;
- evidence producers;
- issue experts;
- project-level feedback.

But it can fail when signals are sparse, biased, manipulated, or dominated by visible groups.

## Distributed signal chain

```text
population expected values
→ citizen participation
→ beneficiary and affected-party signals
→ local evidence and expert signals
→ signal aggregation
→ salience and manipulation correction
→ distributed planning vector
```

## Signal sources

### General citizen signals

Broad but noisy.

Parameters:

```text
general_signal_coverage
general_signal_noise
participation_bias
salience_sensitivity
```

### Beneficiary signals

Closer to experienced value.

Parameters:

```text
beneficiary_signal_coverage
beneficiary_signal_noise
beneficiary_weight
privacy_loss_or_nonresponse
```

### Affected-party signals

Important for antivalues and externalities.

Parameters:

```text
affected_party_coverage
affected_party_noise
affected_party_weight
```

### Local organization signals

May contain local knowledge, but may also be organized-interest signals.

Parameters:

```text
local_org_coverage
local_org_information_quality
local_org_capture_risk
```

### Expert / technical signals

Useful for long-term, low-salience, technical, preventive, or complex needs.

Parameters:

```text
expert_signal_coverage
expert_signal_noise
expert_weight
expert_capture_risk
```

## Aggregation model

A simple first version:

```text
distributed_raw[j] =
    w_general * mean(general_citizen_signals[j])
  + w_beneficiary * mean(beneficiary_signals[j])
  + w_affected * mean(affected_party_signals[j])
  + w_local * mean(local_org_signals[j])
  + w_expert * mean(expert_signals[j])
```

Then apply distortion and correction:

```text
distributed_plan[j] =
    distributed_raw[j]
  + salience_bias[j]
  + strategic_signal_bias[j]
  - deliberation_correction[j]
  - anti_capture_filter[j]
```

Normalize the final vector to the required planning-score range.

## Signal noise

Each signal is modeled as:

```text
signal = individual_expected_value_or_latent_value + noise
```

Baseline:

```text
general_signal_noise = 0.35
beneficiary_signal_noise = 0.20
affected_party_signal_noise = 0.25
local_org_signal_noise = 0.25
expert_signal_noise = 0.15
```

Interpretation:

Beneficiaries and experts may provide more accurate signals for some dimensions, but only if coverage and independence are sufficient.

## Coverage

Coverage controls how many target-value relationships receive usable signals.

Baseline priors:

```text
general_signal_coverage = 0.25
beneficiary_signal_coverage = 0.45
affected_party_coverage = 0.25
local_org_coverage = 0.20
expert_signal_coverage = 0.15
```

These are not empirical claims.

They are starting priors for a platform that actively solicits signals but is not yet universal.

## Participation bias

Distributed planning is vulnerable to organized or high-capacity groups dominating the signal layer.

```text
participation_bias ∈ [0, 1]
```

Where:

```text
0 = participation represents population evenly
1 = signals come almost only from organized/high-capacity groups
```

Baseline:

```text
participation_bias = 0.30
```

## Salience bias

Visible needs may receive more signals regardless of latent value.

```text
salience_bias_strength = 0.20
```

This should be varied because salience is a major failure mode of distributed participation.

## Strategic signal manipulation

Organized actors may coordinate signals to inflate priorities.

Parameters:

```text
strategic_signal_share
manipulation_intensity
coordination_quality
anti_capture_filter_strength
```

Baseline:

```text
strategic_signal_share = 0.10
manipulation_intensity = 0.30
anti_capture_filter_strength = 0.30
```

## Deliberative correction

Structured deliberation, source labeling, beneficiary weighting, contradiction exposure, and evidence review can reduce noise.

```text
deliberation_correction_strength ∈ [0, 1]
```

Baseline:

```text
deliberation_correction_strength = 0.30
```

Higher values should reduce salience and manipulation effects, but not eliminate them.

## Recommended baseline weights

```text
w_general = 0.25
w_beneficiary = 0.35
w_affected = 0.15
w_local = 0.15
w_expert = 0.10
```

Interpretation:

Beneficiary signals receive higher weight because the experiment's purpose is to test whether a distributed planning vector can recover information lost by representative central planning.

This must be sensitivity-tested.

## Scenario variants

### Distributed low coverage

```text
general_signal_coverage = 0.10
beneficiary_signal_coverage = 0.15
participation_bias = 0.50
salience_bias_strength = 0.35
```

Expected behavior:

Distributed planning may perform poorly and may lose to a competent central planner.

### Distributed beneficiary-weighted

```text
beneficiary_signal_coverage = 0.55
beneficiary_weight = high
salience_bias_strength = 0.15
deliberation_correction_strength = 0.40
```

Expected behavior:

Distributed planning should better recover latent value when beneficiaries are reachable and protected.

### Distributed captured

```text
strategic_signal_share = 0.30
manipulation_intensity = 0.60
anti_capture_filter_strength = 0.15
```

Expected behavior:

Distributed planning should degrade sharply.

### Distributed deliberative correction

```text
signal_coverage = medium
deliberation_correction_strength = 0.60
anti_capture_filter_strength = 0.50
```

Expected behavior:

Distributed planning should improve when noisy participation is corrected by source visibility, contradiction, and evidence context.

## Metrics

Primary:

```text
corr(distributed_plan, latent_social_value)
```

Secondary:

```text
coverage
beneficiary_value_recovery
salience_distortion
strategic_manipulation_loss
minority_recovery
low_visibility_need_recovery
false_priority_rate
```

## Relationship to open mode

This is not yet full open mode.

The experiment can model distributed signals inside a tutored or semi-open system.

Full open mode would require modeling:

- rule-change governance;
- open planning-scope construction;
- constitutional-level meta-governance;
- participation concentration safeguards;
- protocol amendment rules.

## Design rule

> Distributed planning wins only if signal coverage, beneficiary information, and anti-capture controls are strong enough to overcome participation bias and salience.
