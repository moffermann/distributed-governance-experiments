# Agenda Compression Model

## Purpose

This document explains the additional information-loss mechanism used by the executable planning-vector construction simulator.

The central representative plan should not receive a full, project-level average of supporter preferences.

A government does not normally transform every preference of every supporter into a complete value-ranked planning vector. It compresses preferences into an agenda: a limited set of issues, slogans, priorities, projects, ministries, programs, negotiations, and budget lines.

## Core idea

Representative planning loses information through agenda compression.

The model therefore adds two parameters:

```text
agendaBandwidth
offAgendaResponsiveness
```

## `agendaBandwidth`

This controls the share of the supporter's preference vector that survives as explicit agenda priority.

Example:

```text
agendaBandwidth = 0.12
```

means that only the top 12% of the supporter-preference vector is strongly represented in the governing agenda.

This is not a claim that only 12% of policies exist. It is a proxy for the fact that only a limited share of the population's full value map becomes an active planning priority.

## `offAgendaResponsiveness`

This controls how much the government remains responsive to values outside the active agenda.

Example:

```text
offAgendaResponsiveness = 0.08
```

means that off-agenda needs still have some influence, but most of their signal is replaced by low-information priors, salience, administrative inertia, or noise.

## Compression formula

For a representative preference vector:

```text
supporter_vector
```

the simulator keeps the top agenda-bandwidth share mostly intact and replaces the rest with:

```text
offAgendaResponsiveness * original_value
+ (1 - offAgendaResponsiveness) * low_information_prior
```

The low-information prior is based on a mixture of salience and random noise.

## Why this matters

Without agenda compression, the model gives the central planner too much project-level information.

Even if approval is low or the winner's mandate is partial, the average preference vector of supporters may still remain highly correlated with latent social value because every citizen's full expected-value matrix contains broad information.

Agenda compression models the additional loss between:

```text
what supporters might value
```

and:

```text
what the government actually turns into planning priority
```

## Current priors

Initial executable scenario:

| Variant | agendaBandwidth | offAgendaResponsiveness |
|---|---:|---:|
| `central_low_alignment` | 0.08 | 0.03 |
| `central_median_alignment` | 0.12 | 0.08 |
| `central_high_alignment` | 0.25 | 0.18 |
| `central_technocratic_capacity` | 0.15 | 0.10 |

## Interpretation

Low bandwidth does not mean central planning is stupid.

It means a representative system compresses heterogeneous social preferences into a politically governed agenda with limited capacity to preserve off-agenda beneficiary value.

High-capacity, high-approval, high-fidelity central planning can still perform well in the model.

## Design rule

> Do not model representative planning as if the government receives the full preference vector of its supporters.
