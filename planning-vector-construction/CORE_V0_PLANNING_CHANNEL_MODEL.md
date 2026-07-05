# Core v0 Planning Channel Model

## Purpose

This document defines how Core v0 planning-vector construction should be modeled in the planning-vector experiment.

It corrects an important distinction:

```text
project allocation profiles are not planning-vector construction
```

A project allocation profile routes a citizen's allocation among already-published eligible projects.

A planning vector defines which public needs, values, territories, or functions should be prioritized before projects are selected or financed.

## Core distinction

## Planning-vector construction

Answers:

```text
What should the public system prioritize?
```

Examples:

- rural schools;
- preventive health;
- low-visibility territories;
- childhood infrastructure;
- maintenance-heavy services;
- vulnerable beneficiaries;
- public-safety externalities;
- territorial equity.

## Project allocation profiles

Answer:

```text
How should my allocation be routed among eligible projects?
```

Examples:

- projects near me;
- almost-funded projects;
- projects with confirmed fiscalizer;
- rural-school projects;
- low-risk projects;
- sports projects;
- cultural projects.

Allocation profiles operate after a planning scope and eligible project universe exist.

They do not construct the planning vector.

## Core v0 planning sources

In Core v0, a distributed planning vector should be constructed from:

```text
1. attentive citizen planning signals;
2. delegated planning signals;
3. optional authority mandate effects.
```

It should not be constructed from:

```text
1. project allocation profiles;
2. passive default routing;
3. raw salience;
4. platform recommendation exposure.
```

## Attentive citizen planning signal

Attentive citizens are citizens who explicitly participate in the planning process.

They may express priorities over:

- needs;
- values;
- territories;
- beneficiary groups;
- planning scopes;
- public functions;
- neglected categories.

Parameters:

```text
attentivePlanningShare
attentiveSignalNoise
attentiveSampleSize
attentiveCoverageBias
attentiveSalienceBias
attentiveDeliberationCorrection
```

Interpretation:

Attentive participation has relatively good information where it exists, but low coverage if participation is spontaneous.

## Delegated planning signal

Delegated planning comes from citizens assigning planning influence to delegates.

The model must distinguish:

```text
delegatorShare
from
delegateCount
```

`delegatorShare` is the share of population weight represented through delegation.

`delegateCount` is the number of delegate actors receiving that represented weight.

Example:

```text
delegatorShare = 0.10
delegateCount = 500
```

means:

```text
10% of the represented planning weight is delegated across 500 delegate actors.
```

It does not mean that 10% of citizens are delegates.

## Why Core v0 delegation differs from ordinary political representation

Ordinary political representation compresses broad authority into periodic elections.

Core v0 delegation is intended to be:

- scoped;
- auditable;
- revocable;
- reportable;
- many-to-many;
- closer to beneficiaries or issue communities;
- separable by public function, territory, value, or project domain.

Therefore, delegated planning in Core v0 should have lower information loss than winner-take-mandate representative planning when:

```text
delegateCount is high;
delegateConcentration is low;
delegateAuditability is high;
revocationResponsiveness is high;
delegateScopeGranularity is high;
delegateReportQuality is high.
```

It should degrade when:

```text
delegateCount is low;
delegateConcentration is high;
delegates become brokers;
reports are opaque;
revocation is weak;
clientelism appears;
related-party capture appears.
```

## Delegate signal quality

A first proxy:

```text
effective_delegate_quality =
    delegateInformationQuality
  * auditability_factor
  * revocation_factor
  * scope_granularity_factor
  * concentration_penalty
  * alignment_factor
```

Where:

```text
auditability_factor = 0.5 + 0.5 * delegateAuditability
revocation_factor = 0.5 + 0.5 * delegateRevocationResponsiveness
scope_granularity_factor = 0.5 + 0.5 * delegateScopeGranularity
concentration_penalty = 1 - 0.5 * delegateConcentration
alignment_factor = delegateAlignment
```

This is a first modeling approximation, not a final empirical formula.

## Authority mandate effect

A public authority can affect Core v0 planning without directly defining the planning vector.

Possible authority modes:

```text
none
enabled_voluntary
mandated_participation
mandated_binding_distributed_signal
```

The authority may:

- open a planning scope;
- require a participation round;
- require territorial coverage;
- require beneficiary consultation;
- define protected floors;
- require justification for overriding distributed signals;
- provide funding for participation support;
- make the distributed signal binding or advisory.

In this experiment, authority mandate should be modeled as a coverage and constraint amplifier, not as central planning content unless the scenario explicitly says so.

## Core v0 planning vector formula

A first version:

```text
core_v0_planning_vector[j] = normalize(
    w_attentive * attentive_signal[j]
  + w_delegate  * delegated_signal[j]
  + w_mandate   * authority_mandate_signal[j]
)
```

Where:

```text
w_attentive + w_delegate + w_mandate = 1
```

The weights should be derived from scenario parameters, not fixed globally.

## Suggested Core v0 planning scenarios

### `core_v0_tutored_distributed_voluntary`

The authority enables a planning scope. Participation is voluntary.

### `core_v0_tutored_distributed_mandated`

The authority keeps legal/tutored control but requires a distributed planning signal before finalizing or using the vector.

### `core_v0_open_spontaneous_planning`

Open-mode planning with no authority mandate; planning emerges from attentive citizens and delegable representation.

### `core_v0_open_mandated_participation`

Open-mode planning with a procedural participation mandate that increases coverage without giving central authority control over the planning vector.

### `core_v0_open_delegate_concentration_risk`

A stress case where high represented weight is delegated to too few delegates.

### `core_v0_open_low_attention_high_delegation`

Low attentive participation but broad, auditable, revocable delegated representation.

## Excluded from this experiment

Do not model the following as planning-vector construction:

```text
automatic project allocation profiles
passive default routing
project discovery ranking
recommendation surfaces
funding target closure
milestone gating
fiscalization
```

Those belong to the adversarial ABM, not to this upstream planning-vector construction experiment.

## Design rule

> Core v0 planning is built from attentive participation and auditable/revocable delegation, optionally reinforced by authority mandate — not from project allocation profiles.
