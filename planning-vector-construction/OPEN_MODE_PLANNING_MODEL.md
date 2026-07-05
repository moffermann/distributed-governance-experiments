# Open Mode Planning Model

## Purpose

This document defines how the planning-vector construction experiment should represent Core v0 open-mode planning.

Open mode should be modeled separately from tutored mode because the authority's role changes.

## Core distinction

## Tutored mode

The public authority still controls or authorizes the planning scope and may decide whether distributed planning signals are advisory, required, or binding.

## Open mode

The planning vector is constructed through protocol-defined distributed mechanisms rather than central authority planning.

A public authority may still mandate or support participation in a specific implementation, but it does not define the planning vector as central content.

## Open-mode scenarios

The experiment should include at least two open-mode scenarios.

## 1. Open spontaneous planning

```text
core_v0_open_spontaneous_planning
```

Characteristics:

- no authority mandate;
- attentive participation is voluntary;
- delegation is voluntary;
- delegate actions are auditable;
- delegation can be revoked;
- planning vector is generated from attentive and delegated signals;
- coverage depends on spontaneous participation and delegate ecosystem health.

This scenario tests whether open mode can build a useful planning vector without procedural reinforcement.

## 2. Open mandated participation

```text
core_v0_open_mandated_participation
```

Characteristics:

- authority or protocol requires a participation round;
- authority does not define the vector;
- mandate increases attentive participation and/or delegation coverage;
- participation must be auditable;
- distributed signal may become binding or strongly presumptive depending on implementation;
- coverage thresholds may be required by territory, group, or beneficiary category.

This scenario tests whether participation mandates improve distributed planning quality without recreating central planning.

## Authority mandate in open mode

A mandate can mean:

```text
participation must occur
coverage thresholds must be met
beneficiary consultation must be attempted
low-visibility groups must be reached
results must be published
override requires justification
```

It should not automatically mean:

```text
the authority chooses the priorities
```

## Parameters

### Attentive participation

```text
attentivePlanningShare
attentiveSignalNoise
attentiveSampleSize
attentiveSalienceBias
```

### Delegation

```text
delegatorShare
delegateCount
delegateConcentration
delegateInformationQuality
delegateAlignment
delegateAuditability
delegateRevocationResponsiveness
delegateScopeGranularity
delegateReportQuality
```

### Mandate

```text
authorityMandateMode
mandatoryParticipationBoost
mandatoryDelegationBoost
coverageRequirement
mandateConstraintWeight
authorityOverridePower
authorityMustJustifyOverride
```

## Open-mode success conditions

Open-mode planning improves when:

- attentive participation is not zero;
- delegator share is meaningful;
- delegate count is high;
- delegate concentration is low;
- auditability and revocation are strong;
- the mandate, if present, increases coverage rather than centralizing control;
- salience and broker capture are controlled.

Open-mode planning fails when:

- attentive participation is tiny;
- delegation is concentrated;
- delegates become opaque brokers;
- revocation is weak;
- reports are unreadable;
- low-visibility groups produce no signals;
- participation mandates become bureaucratic rituals rather than informative signals.

## Relationship to the adversarial ABM

This experiment should estimate planning-vector correlation for open-mode scenarios.

The adversarial ABM can then use those estimated correlations as planning inputs when testing:

```text
core_v0_open_spontaneous_planning
core_v0_open_mandated_participation
```

## Design rule

> Open-mode planning is not central planning with a survey. It is distributed planning with protocolized participation, delegation, auditability, and revocation.
