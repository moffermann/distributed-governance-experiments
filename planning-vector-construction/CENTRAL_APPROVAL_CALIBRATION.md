# Central Approval Calibration

## Purpose

This document defines how approval should be used in the planning-vector construction experiment.

The goal is to avoid calibrating central planning only from developed democracies or institutionally favorable cases.

Central planning should be tested across a broader approval/legitimacy distribution, including Latin American, African, and crisis-governance contexts.

## Core rule

Approval is not equal to planning correlation.

Do not read:

```text
approvalRate = 0.40
```

as:

```text
corr(central_plan, latent_value) = 0.40
```

Approval is one input into the representative information-loss mechanism.

The final correlation emerges from:

```text
approvalRate
+ turnoutRate
+ winnerVoteShare
+ supporterAlignment
+ nonSupporterAlignment
+ programFidelity
+ agendaBandwidth
+ offAgendaResponsiveness
+ institutionalDistortion
+ beneficiaryDistance
+ limitedTechnocraticRecovery
```

## Why broaden the calibration set?

A sample centered on developed democracies can overstate central planning alignment.

Many democratic or semi-democratic contexts face:

- very low approval;
- weak trust;
- fragmented mandates;
- clientelism;
- weak program fidelity;
- high corruption perception;
- weak implementation capacity;
- high distance from beneficiaries;
- unstable coalitions;
- low responsiveness outside the governing coalition.

Therefore, the central-planning baseline should include low-approval and crisis-legitimacy cases.

## Approval regimes used in the executable baseline

The scenario `core-v0-planning-channels.json` now uses the following central representative variants.

| Variant | Approval | Interpretation |
|---|---:|---|
| `central_crisis_legitimacy` | 0.06 | Severe legitimacy crisis; sub-10% approval possible in real cases. |
| `central_very_low_alignment` | 0.18 | Very low approval and weak program-to-plan fidelity. |
| `central_low_alignment` | 0.30 | Low but not extreme approval. |
| `central_median_global_south` | 0.38 | Broader global-south / institutionally complex baseline. |
| `central_median_democracy` | 0.43 | Median-ish democratic baseline. |
| `central_high_alignment` | 0.60 | Favorable central planning scenario, not baseline. |

## Why include sub-10% approval?

Some governments do reach extreme approval collapse.

Such cases should not define the ordinary baseline, but they are important to model because central planning quality should degrade sharply when representative legitimacy and program fidelity collapse.

## Why keep a high-alignment central scenario?

The model should not punish central planning by assumption.

A central government with:

- high approval;
- strong program fidelity;
- broad turnout;
- higher agenda bandwidth;
- lower distortion;
- some technocratic recovery;
- lower beneficiary distance;

should be allowed to construct a planning vector with meaningful correlation to latent public value.

This scenario is a favorable comparison case, not the assumed average.

## Recommended interpretation

The central planning model should be read as a family of regimes:

```text
crisis legitimacy
very low alignment
low alignment
median global south
median democracy
high alignment
```

not as a single universal central-planning quality.

## Current expected ranges

The exact correlations are simulation outputs, not inputs.

Expected qualitative ranges:

```text
central_crisis_legitimacy:     very low correlation
central_very_low_alignment:   low correlation
central_low_alignment:        low/moderate correlation
central_median_global_south:  moderate correlation
central_median_democracy:     moderate correlation
central_high_alignment:       moderate/high correlation
```

## Design rule

> Central planning should be calibrated with a broad legitimacy distribution, not only with developed-democracy averages.
