# Calibration Priors — Planning Vector Construction

## Purpose

This document defines initial parameter priors for the planning-vector construction experiment.

The goal is not to claim that these values are final empirical estimates.

The goal is to start with proxies that are:

- explicit;
- plausible;
- source-aware;
- sensitivity-testable;
- replaceable by country-specific calibration.

## Calibration philosophy

The experiment should not say:

```text
centralPlanningSignalMix = 0.15 because central planning is bad.
```

It should estimate planning quality from mechanisms:

```text
turnout
winner vote share
approval
program fidelity
institutional distortion
technocratic capacity
beneficiary distance
```

Likewise, distributed planning quality should be estimated from:

```text
signal coverage
signal noise
beneficiary signal weight
participation bias
salience bias
strategic manipulation
anti-capture filtering
```

## External anchors to use first

## 1. Voter turnout

Use international turnout data as an anchor for electoral participation.

Initial global proxy:

```text
turnout_rate = 0.555
```

Rationale:

International IDEA reported global voter participation of approximately 55.5% in 2023 in public reporting on its Global State of Democracy work.

Sensitivity range:

```text
low:    0.40
medium: 0.555
high:   0.75
```

Country-specific implementations should replace this with national electoral data.

## 2. Winner vote share

Initial proxy for a winning executive candidate in a competitive election:

```text
winner_vote_share = 0.52
```

This represents a narrow majority among voters, not among the entire adult population.

Sensitivity range:

```text
plurality/minority mandate: 0.35-0.45
narrow majority/runoff:     0.50-0.55
strong majority:            0.60-0.65
```

Effective direct electoral mandate:

```text
electoral_mandate_share = turnout_rate * winner_vote_share
```

Baseline:

```text
0.555 * 0.52 = 0.2886
```

Interpretation:

The elected government may control planning authority while directly carrying only a compressed subset of population preference information.

## 3. Approval rate

Initial proxy:

```text
approval_rate = 0.40
```

Rationale:

Approval varies widely by country and moment. The initial model treats 40% as a medium-low governing alignment prior, not as a universal fact.

Sensitivity range:

```text
low approval:     0.20-0.30
medium approval:  0.35-0.45
high approval:    0.55-0.65
exceptional:      0.70+
```

Country-specific implementations should replace this with polling averages or approval datasets.

## 4. Program-to-plan fidelity

Initial proxy:

```text
program_fidelity = 0.60
```

Interpretation:

The implemented planning vector partly follows the promised program but is transformed by bargaining, constraints, drift, bureaucracy, and political incentives.

Sensitivity range:

```text
low fidelity:     0.30-0.45
medium fidelity:  0.50-0.65
high fidelity:    0.75-0.90
```

## 5. Supporter versus non-supporter alignment

Initial proxies:

```text
supporter_alignment = 0.70
non_supporter_alignment = 0.15
```

Interpretation:

A representative plan is more aligned with the groups that approve or support the government than with groups outside the governing coalition.

Sensitivity ranges:

```text
supporter_alignment:     0.55-0.85
non_supporter_alignment: 0.00-0.35
```

## 6. Technocratic capacity

Initial proxy:

```text
technocratic_capacity = 0.20
```

Interpretation:

The central planner may recover some latent value through expert information, professional bureaucracy, statistics, and sectoral knowledge.

Sensitivity range:

```text
low capacity:     0.05-0.15
medium capacity:  0.20-0.35
high capacity:    0.45-0.65
```

This parameter allows central planning to perform well in high-capacity scenarios.

## 7. Institutional distortion

Initial components:

```text
bureaucratic_distortion = 0.15
coalition_distortion = 0.10
lobbying_distortion = 0.10
beneficiary_distance = 0.15
```

Combined distortion should be bounded rather than simply summed without limit.

Suggested transform:

```text
institutional_distortion = 1 - product(1 - component_k)
```

Baseline:

```text
1 - (0.85 * 0.90 * 0.90 * 0.85) ≈ 0.414
```

Interpretation:

The plan is meaningfully transformed after the electoral mandate.

## Distributed planning priors

## 1. Signal coverage

Initial proxies:

```text
general_signal_coverage = 0.25
beneficiary_signal_coverage = 0.45
affected_party_coverage = 0.25
local_org_coverage = 0.20
expert_signal_coverage = 0.15
```

Interpretation:

Distributed planning does not require everyone to participate, but it needs enough coverage to recover local and beneficiary information.

## 2. Signal noise

Initial proxies:

```text
general_signal_noise = 0.35
beneficiary_signal_noise = 0.20
affected_party_signal_noise = 0.25
local_org_signal_noise = 0.25
expert_signal_noise = 0.15
```

Interpretation:

Direct beneficiaries and experts may have more accurate signals for some dimensions, but they still contain noise.

## 3. Signal weights

Initial proxy weights:

```text
w_general = 0.25
w_beneficiary = 0.35
w_affected = 0.15
w_local = 0.15
w_expert = 0.10
```

These should be sensitivity-tested.

## 4. Distributed failure parameters

Initial proxies:

```text
participation_bias = 0.30
salience_bias_strength = 0.20
strategic_signal_share = 0.10
manipulation_intensity = 0.30
anti_capture_filter_strength = 0.30
deliberation_correction_strength = 0.30
```

Interpretation:

Distributed planning has more local information, but it is vulnerable to unequal participation, visibility distortion, and manipulation.

## Suggested central-planning scenarios

| Scenario | Turnout | Winner share | Approval | Program fidelity | Tech capacity | Distortion | Expected result |
|---|---:|---:|---:|---:|---:|---:|---|
| central_low_alignment | 0.555 | 0.52 | 0.30 | 0.45 | 0.15 | high | low plan-value correlation |
| central_median_alignment | 0.555 | 0.52 | 0.40 | 0.60 | 0.20 | medium | modest plan-value correlation |
| central_high_alignment | 0.70 | 0.58 | 0.60 | 0.75 | 0.30 | low-medium | moderate/high correlation |
| central_technocratic | 0.555 | 0.52 | 0.40 | 0.55 | 0.55 | medium | central can perform well despite weak approval |

## Suggested distributed-planning scenarios

| Scenario | General coverage | Beneficiary coverage | Signal noise | Strategic bias | Correction | Expected result |
|---|---:|---:|---:|---:|---:|---|
| distributed_low_coverage | 0.10 | 0.15 | high | medium | low | weak distributed vector |
| distributed_baseline | 0.25 | 0.45 | medium | medium-low | medium | stronger than weak central planning |
| distributed_beneficiary_weighted | 0.30 | 0.60 | medium-low | medium-low | medium-high | high plan-value correlation |
| distributed_captured | 0.30 | 0.30 | medium | high | low | distributed vector degrades |

## Output calibration target

The experiment should output estimated ranges such as:

```text
centralPlanningSignalMix range:      0.10-0.35 under median representative assumptions
distributedPlanningSignalMix range:  0.45-0.75 under baseline distributed assumptions
```

These are not hard-coded conclusions.

They should be generated by the simulation and updated as real calibration improves.

## Future data sources

Potential calibration sources:

- International IDEA turnout database and Global State of Democracy reports;
- CSES individual-level election surveys;
- Latinobarometer institutional trust and democracy-support surveys;
- executive approval datasets;
- national polling averages;
- electoral-result datasets;
- public-opinion priority surveys;
- participatory budgeting participation data;
- civic platform signal data from pilots.

## Design rule

> Defaults are not conclusions. Defaults are starting points for sensitivity analysis.
