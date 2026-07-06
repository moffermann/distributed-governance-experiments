# Planning Behavior Calibration Experiment

## Working title

**Behavioral Calibration for Distributed Planning: LLM and Human Elicitation of Delegation, Attention, Revocation, and Platform-Use Parameters**

## Status

Executable LLM panel added (`src/run_llm_panel.py`, prompt version v0.3): runs the Spanish instrument against any OpenAI-compatible endpoint (LM Studio locally), enforces the response schema via structured output, stores raw + normalized responses with validation warnings, and fits per-archetype and pooled distributions. First panel run recorded under `results/`. Outputs map into the behavioral adoption ABM via [`OUTPUT_TO_BEHAVIORAL_ABM.md`](OUTPUT_TO_BEHAVIORAL_ABM.md).

This experiment is separate from:

```text
experiments/planning-vector-construction/
experiments/adversarial-abm/
```

## Purpose

The existing planning-vector model still depends on behavioral parameters such as:

```text
delegatePlatformUseRate
delegatePlanningCoverage
delegateAlignment
delegateRevocationResponsiveness
reportReadProbability
revocationLikelihoodAfterMisalignment
delegationLikelihood
preferredDelegateType
```

Those parameters should not remain purely discretionary.

This experiment creates a reusable behavioral instrument that can be answered by:

```text
1. LLM agents now;
2. real human participants later;
3. domain experts if needed;
4. pilot users in a future implementation.
```

The same context, questions, response schema, and distribution-fitting pipeline should work across all respondent sources.

## Core methodological idea

The LLM is not treated as a real citizen.

The LLM is used as a synthetic pre-test of a reusable behavioral instrument.

Later, the same instrument can be administered to humans, and the LLM-generated priors can be replaced or compared with empirical human distributions.

```text
LLM responses      → fitted distributions → planning-vector model
Human responses    → fitted distributions → planning-vector model
Pilot telemetry    → fitted distributions → planning-vector model
```

## Why context matters

Respondents must not answer abstract questions about politics.

They must answer in the context of a specific application:

- a mobile app;
- used to direct public project funding;
- the money is not an extra out-of-pocket payment by the citizen;
- the budget comes from public resources / taxes already collected;
- citizens can review projects;
- citizens can delegate participation;
- delegations are auditable;
- delegate actions are visible;
- delegations can be revoked with one click;
- using the app is much easier than doing paperwork at a municipal office;
- non-technical people may rely on trusted relatives or nearby people.

Without this context, answers about delegation and participation will be badly calibrated.

## Folder map

- [`DESIGN_BASELINE.md`](DESIGN_BASELINE.md) — research design and pipeline.
- [`CONTEXT_BRIEF_ES.md`](CONTEXT_BRIEF_ES.md) — Spanish context brief to show before questions.
- [`ARCHETYPES.md`](ARCHETYPES.md) — respondent archetypes for LLM and later human sampling.
- [`QUESTIONNAIRE_ES.md`](QUESTIONNAIRE_ES.md) — Spanish survey/questionnaire instrument.
- [`PROMPT_PROTOCOL.md`](PROMPT_PROTOCOL.md) — LLM prompting protocol and reproducibility requirements.
- [`RESPONSE_SCHEMA.md`](RESPONSE_SCHEMA.md) — structured response schema contract.
- [`DISTRIBUTION_FITTING.md`](DISTRIBUTION_FITTING.md) — fitting beta/logit-normal/mixture distributions and plotting.
- [`HUMAN_STUDY_PROTOCOL.md`](HUMAN_STUDY_PROTOCOL.md) — how the same instrument can be used with humans.
- [`OUTPUT_TO_PLANNING_VECTOR_MODEL.md`](OUTPUT_TO_PLANNING_VECTOR_MODEL.md) — mapping fitted distributions into `planning-vector-construction`.
- [`OUTPUT_TO_BEHAVIORAL_ABM.md`](OUTPUT_TO_BEHAVIORAL_ABM.md) — mapping panel outputs into `behavioral-adoption-abm` parameters, with validation targets and provenance rules.
- [`prompts/LLM_PROMPT_TEMPLATE_ES.md`](prompts/LLM_PROMPT_TEMPLATE_ES.md) — reusable Spanish LLM prompt template.
- [`instruments/SURVEY_INSTRUMENT_ES.md`](instruments/SURVEY_INSTRUMENT_ES.md) — human-facing Spanish survey draft.
- [`src/run_llm_panel.py`](src/run_llm_panel.py) — executable LLM panel runner (LM Studio / any OpenAI-compatible endpoint / codex-exec backend; standard library only).
- [`RUN_2026_07_06_LLM_PANEL_RESULTS.md`](RUN_2026_07_06_LLM_PANEL_RESULTS.md) — first panel runs: backend benchmark, pooled distributions, archetype differentiation, model sensitivity.
- [`RUN_2026_07_06_N1000_PANEL_RESULTS.md`](RUN_2026_07_06_N1000_PANEL_RESULTS.md) — N=1000 population-weighted panel over the 20-archetype set: convergence by n≈500–750, composition-vs-scale decomposition, new-archetype face validity.
- [`src/analyze_convergence.py`](src/analyze_convergence.py) — convergence and composition analysis for large panel runs.
- [`src/analyze_distributions.py`](src/analyze_distributions.py) — Beta fits with KS quality, archetype-mixture detection, histogram figures, and cross-panel distribution tests (requires matplotlib).
- `results/` — dated panel runs: raw responses, normalized responses, fitted summaries.

## Evidence status

LLM responses are not empirical human observations.

They are structured behavioral priors.

The outputs must be treated as:

```text
synthetic prior distributions
not human survey results
not pilot telemetry
not proof of real behavior
```

## Design rule

> The instrument must be reusable: changing the respondent source from LLM to humans should not require changing the questions, schema, or fitting method.
