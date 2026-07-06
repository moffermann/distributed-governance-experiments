# Human Study Protocol

## Purpose

This document explains how the same behavioral calibration instrument can later be administered to real people.

The human study is not required for the initial simulation, but the instrument should be designed so that a future human study can replace LLM priors with empirical distributions.

## Core principle

The LLM protocol and human protocol must use the same substantive context and question structure.

This enables direct comparison:

```text
LLM priors vs human responses
```

## Human study design

Recommended first study:

```text
online survey / vignette experiment
```

Participants should first read the context brief.

Then they answer the questionnaire.

## Minimum metadata

Collect:

```text
country
age band
digital literacy
urban/rural context
political interest
trust in family
trust in local community
trust in institutions
previous use of government digital services
comfort with mobile apps
```

## Context checks

Include comprehension questions:

```text
Does the app require extra personal money?
Where do project funds come from?
How hard is revocation?
```

Participants who fail context checks should be flagged.

A separate analysis may examine how misunderstanding changes behavior.

## Ethical considerations

Before running with humans, the study should include:

- informed consent;
- privacy statement;
- no collection of unnecessary sensitive data;
- option to stop answering;
- clear statement that the app is hypothetical unless deployed;
- no deception about money or political consequences.

## Comparison with LLM responses

Compare:

```text
means
medians
variance
5th / 50th / 95th percentiles
correlation matrix
cluster structure
```

Important questions:

```text
Does the LLM overestimate app use?
Does the LLM underestimate family delegation?
Does the LLM overestimate report reading?
Does the LLM overestimate revocation?
Does the LLM underestimate low digital literacy barriers?
```

## Output

Human responses should use the same normalized schema as LLM responses.

This allows:

```text
human_raw → human_validated → fitted distributions → planning-vector model
```

## Design rule

> The LLM phase is a synthetic pre-test; the human phase is the empirical calibration path.
