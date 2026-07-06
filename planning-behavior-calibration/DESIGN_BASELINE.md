# Design Baseline — Planning Behavior Calibration

## Purpose

This experiment calibrates behavioral parameters used by the Core v0 planning-vector model.

The current deterministic model requires parameters such as:

```text
delegatePlatformUseRate
delegatePlanningCoverage
reportReadProbability
revocationLikelihoodAfterMisalignment
delegateAlignment
delegationLikelihood
preferredDelegateType
```

Instead of selecting these values manually, this experiment will estimate distributions from structured responses.

## Research question

```text
Given a clear description of a mobile civic allocation platform, how likely are different types of people to participate directly, delegate, read reports, revoke delegation, or act as delegates?
```

## Main methodological principle

The experiment separates:

```text
instrument
respondent source
fitted distribution
simulation use
```

This allows the same instrument to be answered by LLM agents now and by humans later.

## Pipeline

```text
1. Define archetypes.
2. Present context brief.
3. Ask standardized questions.
4. Require structured JSON responses.
5. Validate responses.
6. Fit distributions per archetype and variable.
7. Plot distributions.
8. Export fitted priors.
9. Feed priors into planning-vector-construction.
10. Later replace or compare LLM priors with human survey distributions.
```

## Why not use one fixed parameter?

Human and delegate behavior is not fixed.

People differ by:

- age;
- digital literacy;
- trust in family;
- interest in politics;
- time availability;
- civic responsibility;
- comfort with delegation;
- willingness to read reports;
- willingness to revoke;
- relationship to the delegate.

Therefore, the output should be a distribution, not a point estimate.

## Variables to estimate

### Citizen-side variables

```text
directParticipationProbability
delegationProbability
preferredDelegateType
reportReadProbability
revocationLikelihoodAfterMisalignment
revocationLikelihoodAfterInactivity
trustInFamilyDelegate
trustInLocalDelegate
trustInInstitutionalDelegate
```

### Delegate-side variables

```text
delegatePlatformUseRate
delegatePlanningCoverage
delegateReportQuality
delegateResponsibilityEffect
delegateAlignmentWithDelegators
delegateResponsivenessToNotifications
```

### Friction variables

```text
perceivedEaseOfUse
perceivedRevocationEase
perceivedTimeBurden
perceivedUnderstandingOfReports
needForAssistance
```

## Output distributions

Variables in `[0, 1]` should be fitted first with:

```text
Beta distribution
```

If data are multimodal, use:

```text
mixture of Betas
```

If data have strong tails after logit transform, use:

```text
logit-normal
```

Delegate-type choices should use:

```text
categorical / multinomial distribution
```

Multi-channel allocation weights may use:

```text
Dirichlet distribution
```

## Why LLM first?

LLM calibration is useful as a synthetic pre-test because it can generate structured priors across many archetypes before a real survey exists.

But LLM responses are not human evidence.

They must be labeled as:

```text
synthetic behavioral priors
```

## Why human later?

The exact same context, questions, and response schema can be given to real people.

Then:

```text
LLM distributions can be compared with human distributions.
```

The model does not need to change.

Only the source of responses changes.

## Design rule

> Build the behavioral instrument as if it will be administered to humans, even when the first respondent is an LLM.
