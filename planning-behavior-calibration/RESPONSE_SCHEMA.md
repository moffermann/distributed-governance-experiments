# Response Schema Contract

## Purpose

This document defines the structured response format for LLM and human behavioral calibration.

A formal JSON Schema can be generated later from this contract.

## Top-level fields

```text
response_id
respondent_source
model_or_sample_info
archetype_id
context_understanding
platform_behavior
citizen_behavior
delegate_behavior
friction
free_text
confidence
```

## `respondent_source`

Allowed values:

```text
llm
human
expert
pilot
```

## `context_understanding`

Required fields:

```text
not_extra_personal_money: boolean
public_funds: boolean
one_click_revocation: boolean
understanding_score: number 0-1
```

Responses with failed context checks should be flagged.

They should not always be discarded, because misunderstanding is itself useful for human usability analysis.

## `platform_behavior`

All probability fields use `[0, 1]`.

Required fields:

```text
platform_trial_probability
monthly_platform_use_probability
notification_driven_use_probability
```

Interpretation:

- `platform_trial_probability` estimates whether the person would open or try the app at least once.
- `monthly_platform_use_probability` estimates basic active use, even if the person does not directly participate.
- `notification_driven_use_probability` estimates whether reminders can increase active use.

These are upstream of direct participation and delegation.

## `citizen_behavior`

All probability fields use `[0, 1]`.

Required fields:

```text
direct_review_probability
direct_planning_participation_probability
delegation_probability
preferred_delegate_type_distribution
revocation_ease_effect
report_visibility_effect
report_read_probability_short
report_read_probability_detailed
revocation_likelihood_after_misalignment
revocation_likelihood_after_inactivity
```

### `preferred_delegate_type_distribution`

Must sum approximately to `1.0`.

Fields:

```text
family_member
partner_or_spouse
trusted_friend
trusted_neighbor
local_community_leader
technical_expert
public_institution_or_ngo
political_party_or_political_actor
public_influencer
would_not_delegate
```

## `delegate_behavior`

All fields use `[0, 1]`.

Required fields:

```text
would_accept_delegation
delegate_platform_use_rate
delegate_planning_coverage
delegate_responsibility_effect
delegate_revocation_discipline_effect
alignment_with_close_delegator
alignment_with_impersonal_delegators
delegate_report_quality_willingness
```

`would_accept_delegation` (added in prompt version v0.3) is the probability of accepting to act as delegate if a family member or neighbor asked — it anchors the behavioral ABM's `micro_delegate_willingness` parameter.

## `friction`

Required fields:

```text
perceived_ease_of_use
perceived_understanding
need_for_assistance
```

## `free_text`

Required fields:

```text
participation_reason
trust_reason
revocation_reason
```

## `confidence`

Required fields:

```text
overall: number 0-1
notes: string
```

## Validation rules

1. All probability values must be between `0` and `1`.
2. Preferred delegate distribution should sum to `1.0 ± 0.02`.
3. Responses must pass the context checks or be flagged.
4. Free-text explanations must be preserved for qualitative analysis.
5. LLM raw responses must be stored before normalization.
6. Platform-use fields must be preserved separately from direct participation fields.

## Design rule

> The response format must be identical across LLM, human, expert, and pilot sources whenever possible.
