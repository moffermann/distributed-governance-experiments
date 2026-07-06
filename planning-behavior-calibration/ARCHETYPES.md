# Archetypes

> Extended 2026-07-06: the original six citizen archetypes (A1–A6) were joined by fourteen more (A7–A20, defined at the end of this document) with assumed population weights, so large panels can approximate a realistic population mix instead of an equal-weight archetype grid. Weights are declared assumptions, not census-fitted values.

## Purpose

This document defines respondent archetypes for LLM calibration and future human sampling.

The goal is not to stereotype people.

The goal is to cover behavioral variation relevant to Core v0 planning:

- direct participation;
- delegation;
- report reading;
- revocation;
- delegate platform use;
- planning coverage;
- trust in different delegate types.

## Citizen archetypes

## A1 — Older low-digital-literacy citizen

Description:

```text
Older person, limited comfort with mobile apps, may rely on family for digital tasks.
```

Expected relevance:

- likely to delegate;
- likely to choose trusted family;
- low direct planning participation;
- may read simple notifications but not detailed reports;
- revocation may require assistance despite being one click technically.

## A2 — Busy working adult

Description:

```text
Works full time, has little time for civic participation, uses mobile apps comfortably.
```

Expected relevance:

- may delegate or use simple profiles;
- may read short notifications;
- may revoke if trust is clearly violated;
- moderate digital capacity but high time scarcity.

## A3 — Politically attentive citizen

Description:

```text
Follows public affairs, compares projects, values transparency.
```

Expected relevance:

- higher direct participation;
- may become delegate;
- higher report reading;
- higher revocation responsiveness.

## A4 — Low-trust citizen

Description:

```text
Distrusts politicians, institutions, and possibly delegates.
```

Expected relevance:

- may avoid delegation;
- may participate directly if friction is low;
- high revocation likelihood if delegated action is misaligned;
- skeptical of institutional delegates.

## A5 — Rural or territorially distant citizen

Description:

```text
Lives far from central institutions and may value local knowledge highly.
```

Expected relevance:

- may trust local/community delegates;
- may value nearby projects;
- may see Core v0 as improving local voice;
- digital access may vary.

## A6 — Young digitally active citizen

Description:

```text
Comfortable with apps, notifications, and online decision interfaces.
```

Expected relevance:

- higher app use;
- moderate to high direct participation;
- may delegate selectively;
- high revocation ease.

## Delegator/delegate relationship archetypes

## D1 — Family proxy delegate

Description:

```text
A family member helps represent someone with lower digital literacy or less time.
```

Expected relevance:

- high interpersonal alignment;
- high trust;
- moderate platform use;
- moderate planning coverage;
- high willingness to explain decisions informally.

## D2 — Community/local delegate

Description:

```text
Trusted local person, neighborhood leader, teacher, community organizer, or respected local actor.
```

Expected relevance:

- good local knowledge;
- medium-high platform use;
- moderate-high planning coverage;
- alignment depends on community scope.

## D3 — Public/institutional delegate

Description:

```text
Organization, public figure, influencer, party-adjacent actor, NGO, or civic group.
```

Expected relevance:

- high platform use;
- higher planning coverage;
- lower interpersonal alignment;
- higher concentration risk.

## D4 — Plural delegated bloc

Description:

```text
A smaller set of visible delegates represent different political or social currents. They are not a single central authority and their actions remain visible and revocable.
```

Expected relevance:

- potentially high platform use;
- moderate alignment;
- higher global concentration than microdelegation;
- still more plural, auditable, and revocable than central planning.

## D5 — Broker/captured delegate

Description:

```text
Actor who tries to accumulate delegated weight for private, clientelist, institutional, or off-platform benefit.
```

Expected relevance:

- high platform use;
- low alignment;
- high manipulation risk;
- revocation depends on whether delegators read reports and understand misalignment.

## Extended citizen archetype set (A7–A20, added 2026-07-06)

Fourteen additional citizen archetypes broaden coverage of the population's occupational, material, and attitudinal variation. Full prompt-facing descriptions and per-archetype variation ranges live in `src/run_llm_panel.py`; weights are assumed population shares (provenance: assumed), used by the runner's `--total-n` population-weighted allocation.

| Id | Archetype | Assumed weight |
|---|---|---:|
| A1 | Older low-digital-literacy citizen | 0.08 |
| A2 | Busy working adult | 0.12 |
| A3 | Politically attentive citizen | 0.04 |
| A4 | Low-trust citizen | 0.07 |
| A5 | Rural or territorially distant citizen | 0.06 |
| A6 | Young digitally active citizen | 0.08 |
| A7 | Informal / gig worker | 0.06 |
| A8 | Primary caregiver running a household | 0.06 |
| A9 | Higher-education student | 0.05 |
| A10 | Small-business owner | 0.04 |
| A11 | Public-sector employee | 0.03 |
| A12 | Front-line health/education professional | 0.04 |
| A13 | Retiree active in community organizations | 0.05 |
| A14 | Unemployed / precarious worker | 0.04 |
| A15 | Person with disability or reduced mobility | 0.03 |
| A16 | Recent migrant | 0.03 |
| A17 | Ideologically opposed citizen | 0.04 |
| A18 | Digitally intensive but apolitical user | 0.04 |
| A19 | Acting neighborhood/social leader | 0.02 |
| A20 | Tech professional / early adopter | 0.02 |

The set deliberately includes archetypes expected to reject or ignore the platform (A17, A18) and natural delegate candidates (A13, A19) so that non-use and delegation supply both emerge from composition rather than from tuning.

## Sampling rule

LLM calibration should generate multiple responses per archetype and scenario variation.

Human studies should sample actual people, not ask them to role-play all archetypes, unless explicitly running a vignette experiment.

## Design rule

> Archetypes are behavioral probes, not claims that real people fit neatly into fixed categories.
