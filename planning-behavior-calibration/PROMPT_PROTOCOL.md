# LLM Prompt Protocol

## Purpose

This document defines how LLM responses should be generated for behavioral calibration.

The goal is to produce structured synthetic priors that can later be compared with human responses.

## Core rule

The LLM must receive the same substantive context that a human respondent would receive.

The prompt must explain:

- the app is mobile;
- the app influences public project funding;
- the money comes from public funds / taxes already collected;
- the respondent is not being asked to donate extra personal money;
- the respondent can participate directly;
- the respondent can delegate;
- delegate actions are visible;
- delegation can be revoked with one click;
- this is easier than a paperwork process at a municipal office;
- non-technical people may rely on trusted relatives or nearby people.

## Prompt structure

Every LLM prompt should include:

```text
1. System instruction
2. Archetype description
3. Context brief
4. Questionnaire
5. Output schema contract
6. Instruction to answer with structured JSON only
```

## Recommended LLM settings

For distribution generation, use multiple temperatures or random seeds where available.

Initial suggestion:

```text
temperature = 0.7
n_per_archetype = 50-100
```

For reproducibility, record:

```text
model name
model provider
model version/date if available
temperature
top_p if available
prompt version
date generated
archetype id
run id
raw output
validated output
```

When the provider does not expose temperature (e.g., the codex-exec backend), record `provider-default` and rely on persona variation for distributional spread.

## Why not one response per archetype?

One response gives a point estimate.

The purpose of this experiment is to estimate distributions.

Therefore, each archetype must generate many responses under small context variations.

## Prompt variation

Permitted variations:

- country context;
- urban/rural setting;
- age;
- digital literacy;
- trust level;
- time availability;
- political interest;
- family support;
- local-community involvement;
- complexity of projects;
- report clarity.

Do not change the core app facts.

In particular, do not remove:

```text
public funds / taxes already collected
no extra personal donation
one-click revocation
auditability / visible delegate actions
mobile app context
```

## Output handling

The LLM should output structured JSON compatible with `RESPONSE_SCHEMA.md`.

The pipeline should store:

```text
raw response
parsed response
normalized response
validation warnings
```

## Invalid responses

Flag responses that:

- misunderstand that no personal donation is required;
- misunderstand that money is public/tax money;
- misunderstand revocation as a complex legal or municipal procedure;
- omit required fields;
- give probabilities outside `[0, 1]`;
- produce delegate-type distributions that do not sum to approximately 1.

## Methodological statement

The LLM does not represent real citizens.

The LLM is used as synthetic prior elicitation over behavioral parameters.

The same instrument can later be used with humans to replace or validate these priors.

## Design rule

> Prompt the LLM as if the resulting questionnaire will later be administered to real people.
