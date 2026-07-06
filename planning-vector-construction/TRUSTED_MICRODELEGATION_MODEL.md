# Trusted Microdelegation Model

## Purpose

This document refines the Core v0 planning-channel model by distinguishing trusted microdelegation from institutional bloc delegation.

The expected Core v0 delegation pattern should not be modeled primarily as citizens delegating to large institutions, parties, national influencers, or a small number of political brokers.

A more realistic baseline is:

```text
citizen → trusted person nearby
```

Examples:

- a parent delegates to an adult child;
- an older citizen delegates to a spouse, child, sibling, or trusted neighbor;
- a low-technology user delegates to someone in the household;
- a citizen delegates to a known local person with aligned preferences;
- small social circles delegate to trusted people who understand their preferences.

## Core distinction

## Local/family concentration is not global concentration

A household may concentrate its internal delegation in one trusted person.

That does not mean the whole system is globally concentrated.

The risk appears when delegated weight becomes globally concentrated in a small number of impersonal or institutional delegates.

## Trusted microdelegation

Trusted microdelegation has:

```text
many delegates
low global concentration
high interpersonal alignment
high auditability
high revocability
high report visibility
small represented clusters
```

## Institutional / broker delegation

Institutional or broker delegation has:

```text
few high-weight delegates
high global concentration
lower interpersonal alignment
more political packaging
higher capture risk
weaker personal preference knowledge
```

## Why Core v0 should start from microdelegation

Core v0 is assumed to run on a ubiquitous interface, such as a mobile phone.

This changes the delegation logic:

- delegation can be granular;
- delegation can be changed quickly;
- delegate actions are visible;
- revocation is one click away;
- reports can be pushed instantly;
- trusted relatives or nearby people can represent low-technology users;
- the delegator does not disappear from the system.

Therefore, the baseline should give trusted microdelegation higher alignment and lower information loss than ordinary political representation.

## Delegation is not automatically active signal

Delegation means that a citizen grants represented planning weight to a delegate.

It does not mean that every delegate actively reviews every planning target in every cycle.

The model therefore separates:

```text
delegatorShare
from
delegatePlatformUseRate
from
delegatePlanningCoverage
```

### `delegatorShare`

The share of represented citizen weight delegated to delegate actors.

### `delegatePlatformUseRate`

The share of delegates expected to actively use the platform during the planning cycle.

Delegates should have a much higher use rate than ordinary citizens because they accepted responsibility, receive notifications, and are visible/revocable.

But their use rate should not be assumed to be 100%.

### `delegatePlanningCoverage`

The share of the planning vector that an active delegate is expected to review or update.

A delegate can be active but still review only part of the vector.

Unreviewed targets should fall back to a stale, neutral, or lower-information signal rather than a full active signal.

## Initial platform-use priors

Suggested initial priors:

| Scenario type | `delegatePlatformUseRate` | `delegatePlanningCoverage` |
|---|---:|---:|
| Trusted microdelegation | 0.70 | 0.45 |
| Family proxy high trust | 0.65 | 0.35 |
| Mixed trusted delegation | 0.68 | 0.42 |
| Tutored voluntary | 0.68 | 0.40 |
| Tutored mandated | 0.78 | 0.55 |
| Open mandated participation | 0.85 | 0.60 |
| Institutional delegate emergence | 0.90 | 0.70 |
| Plural concentrated delegation | 0.85 | 0.65 |

Interpretation:

- family proxies may be highly aligned but not always deep reviewers;
- institutional delegates may be very active but less personally aligned;
- mandated participation increases both use and coverage;
- trusted microdelegation remains strong but no longer assumes complete vector review.

## Parameters

A trusted microdelegation baseline should use:

```text
delegatorShare = medium-high
delegateCount = high
delegateConcentration = low
delegateAlignment = high
delegateAuditability = very high
delegateRevocationResponsiveness = very high
delegateScopeGranularity = high
delegateReportQuality = high
delegatePlatformUseRate = high but not perfect
delegatePlanningCoverage = partial but meaningful
```

Example for 10,000 citizens:

```text
delegatorShare = 0.35
delegateCount = 1500
delegateConcentration = 0.08
delegateAlignment = 0.90
delegateAuditability = 0.95
delegateRevocationResponsiveness = 0.95
delegateScopeGranularity = 0.85
delegateReportQuality = 0.88
delegatePlatformUseRate = 0.70
delegatePlanningCoverage = 0.45
```

This represents roughly 3,500 delegated citizens spread across many microdelegates.

The average delegated weight per delegate is small, but unequal.

## Stress cases

Stress cases should remain, but should not define the baseline.

Examples:

```text
core_v0_open_institutional_delegate_emergence
core_v0_open_plural_delegation_concentrated
core_v0_open_family_proxy_low_review
```

These test whether delegation degrades when:

- weight concentrates globally;
- institutions capture attention;
- revocation is technically available but socially unused;
- reports are not read;
- family delegation becomes coercive;
- delegates are active but not personally aligned;
- delegates use the platform often but cover only part of the vector.

## Planning-vector effect

Trusted microdelegation should improve planning-vector quality when:

```text
interpersonal alignment is high;
auditability is high;
revocation is credible;
delegate count is large;
global concentration is low;
delegate reports are readable;
mandates are granular;
delegate platform use is high enough;
delegate planning coverage is meaningful.
```

It should degrade when:

```text
global concentration increases;
auditability weakens;
revocation is rarely used;
delegates become impersonal;
mandates become broad and opaque;
delegate platform use is low;
delegate planning coverage is shallow.
```

## Design rule

> Core v0 delegation should be modeled first as trusted microdelegation, with platform use and planning coverage explicitly represented, and broker/institutional capture treated as stress cases rather than the baseline.
