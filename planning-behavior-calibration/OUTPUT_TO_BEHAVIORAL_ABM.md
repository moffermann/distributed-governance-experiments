# Output to Behavioral Adoption ABM

## Purpose

This document defines how panel outputs (LLM-elicited now, human later — same instrument) map onto the behavioral adoption ABM's parameters, replacing synthetic guesses with elicited distributions.

The mapping is executed by `experiments/behavioral-adoption-abm/apply_llm_calibration.py`, which reads a `panel_summary.json` produced by `src/run_llm_panel.py` and writes a calibrated scenario overlay with full provenance.

## Mapping rule

Same discipline as `OUTPUT_TO_ABM.md`: a panel statistic is an observed output; an ABM parameter is a generator setting. Where the ABM parameter feeds a mechanism with known multipliers, the mapping inverts them explicitly rather than copying the raw mean.

## Direct parameter mappings

| Panel field (pooled) | ABM parameter | Inversion |
|---|---|---|
| `would_accept_delegation` mean | `micro_delegate_willingness` | ABM draws willingness with p = w × (0.5 + civic); divide by (0.5 + E[civic]) from the civic trait prior |
| `preferred_delegate_type_distribution` | `institutional_delegation_propensity` | institutional mass (expert + institution/NGO + party + influencer) ÷ (1 − would_not_delegate mass) |
| `platform_trial_probability` share < 0.2 | `permanent_rejection_rate` | share of respondents who would not even try, corrected for the ABM's per-consideration weighting factor |
| `direct_planning_participation_probability` mean | `planning_attendance_base.direct_active` | divide by (0.5 + E[civic]); hybrid and profile bases keep their synthetic ratios to direct |
| `friction.perceived_ease_of_use` beta fit | `trait_distributions.digital_confidence` | Beta method-of-moments from the pooled fit |

## Validation targets (recorded, not injected)

These panel statistics are *outputs* in the ABM (emergent), so they are recorded in the calibrated scenario's provenance block for comparison, never forced:

```text
delegation_probability          vs ABM delegation_rate / delegator_share
monthly_platform_use_probability vs ABM active_user_share (among registered)
delegate_platform_use_rate      vs ABM delegate_platform_use_rate (emergent)
delegate_planning_coverage      vs ABM delegate_planning_coverage (emergent)
revocation_likelihood_*         vs ABM delegation_revocation_rate (emergent)
```

## Not mapped (declared)

- `privacy_concern` — the instrument does not elicit privacy attitudes; flagged for instrument v0.4.
- Trust priors (`initial_trust_mean`) — institutional trust is a persona *input* here, not an elicited output.
- Fiscalizer/evidence role parameters — workload facts, not elicitable from citizen personas.

## Provenance discipline

Every calibrated scenario must carry a `_provenance` block: run id, model, temperature, prompt version, n, date, and the statement that values are **llm-elicited synthetic priors, not empirical data** (PROMPT_PROTOCOL.md's methodological statement). The human instrument replaces or validates these priors; ROADMAP Stage 5's provenance classes gain `llm-elicited` between `assumed` and `prototype-derived`.

## Design rule

> The panel elicits people-shaped priors; the ABM keeps the mechanisms. Map parameters by explicit inversion, record emergent quantities as validation targets, and never let an LLM number silently pose as empirical calibration.
