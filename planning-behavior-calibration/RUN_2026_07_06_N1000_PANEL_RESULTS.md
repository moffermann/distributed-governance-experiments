# N=1000 Weighted Panel Results — 2026-07-06

## Execution

Scale test of the instrument on the codex-exec backend (gpt-5.5, reasoning `low`, prompt v0.3):

- 1,000 personas allocated across the **extended 20-archetype set** (`ARCHETYPES.md`, A1–A20) proportionally to their assumed population weights — the set now includes rejecting and ignoring archetypes (ideologically opposed A17, apolitical A18), natural delegate candidates (organized retiree A13, acting neighborhood leader A19), and material-condition variation (informal worker A7, caregiver A8, unemployed A14, disability A15, migrant A16);
- 12 concurrent requests, **1,000/1,000 valid in 1,242 s** (~1.24 s effective per response), zero failures, zero context-check flags;
- convergence and composition analysis: `src/analyze_convergence.py`.

## Does it converge? Yes, by n≈500–750

Pooled means over growing shuffled subsets:

| Field | n=100 | n=250 | n=500 | n=750 | n=1000 | SE(full) |
|---|---:|---:|---:|---:|---:|---:|
| platform_trial_probability | 0.677 | 0.696 | 0.702 | 0.706 | 0.706 | 0.005 |
| monthly_platform_use_probability | 0.415 | 0.427 | 0.432 | 0.437 | 0.437 | 0.005 |
| direct_planning_participation_probability | 0.385 | 0.392 | 0.397 | 0.403 | 0.402 | 0.006 |
| delegation_probability | 0.521 | 0.528 | 0.528 | 0.527 | 0.530 | 0.005 |
| would_accept_delegation | 0.429 | 0.434 | 0.434 | 0.439 | 0.440 | 0.005 |
| delegate_platform_use_rate | 0.515 | 0.524 | 0.529 | 0.536 | 0.536 | 0.005 |
| delegate_planning_coverage | 0.483 | 0.489 | 0.494 | 0.502 | 0.502 | 0.005 |

Every field is stable to ±0.005 from n≈750 onward, with full-sample standard errors of ±0.005–0.006.

## Composition vs scale: the n=90 panel was already representative

Decomposition against the n=90 equal-weight A1–A6 panel (same model, same prompt): restricting the N=1000 panel to A1–A6 and re-pooling equal-weight isolates the sampling effect; the difference between that and the weighted pool isolates the composition effect.

| Field | ref (n=90) | same-archetypes (N=1000) | weighted (N=1000) | composition | scale |
|---|---:|---:|---:|---:|---:|
| platform_trial_probability | 0.709 | 0.713 | 0.706 | −0.007 | +0.004 |
| monthly_platform_use_probability | 0.441 | 0.450 | 0.437 | −0.014 | +0.010 |
| direct_planning_participation_probability | 0.416 | 0.424 | 0.402 | −0.021 | +0.007 |
| delegation_probability | 0.519 | 0.523 | 0.530 | +0.007 | +0.003 |
| would_accept_delegation | 0.418 | 0.432 | 0.440 | +0.008 | +0.014 |

Both effects are ≤0.02 everywhere. The instrument is highly stable in gpt-5.5: 90 personas already captured the pooled levels, and the realistic composition shifts direct participation down by only ~2 points (the apolitical, opposed, and precarious archetypes lower it; the leaders and professionals partially offset).

## New-archetype face validity

| Archetype | trial | direct planning | delegate | would accept delegation |
|---|---:|---:|---:|---:|
| A17 ideologically opposed | 0.17 | 0.06 | 0.20 | 0.17 |
| A18 apolitical digital user | 0.70 | 0.26 | 0.61 | 0.31 |
| A19 neighborhood leader | 0.83 | 0.56 | 0.43 | **0.85** |
| A20 tech professional | 0.88 | 0.61 | 0.38 | 0.53 |
| A13 organized retiree | 0.73 | 0.42 | 0.61 | 0.60 |
| A14 unemployed/precarious | 0.63 | 0.32 | 0.62 | 0.38 |

The orderings are coherent without any tuning: the opposed archetype finally supplies genuine rejection (fixing the n=90 panel's zero mapped rejection rate — now 7.8% after inversion), and the acting neighborhood leader is the strongest delegate-acceptance archetype, exactly the supply the trusted-microdelegation design assumes.

## Stability of the headline patterns

- Preferred delegate types: micro 74.2% / institutional 22.8% / would-not 3.0% — **identical to the n=90 panel** (74.1/22.7) and consistent with the gemma panel's ordering.
- `delegate_planning_coverage` 0.502, inside the trusted-microdelegation prior band.
- Remapped into the ABM (`behavioral-adoption-abm/scenarios/llm_calibrated.json`, provenance updated): registered 68.3%, active 49.8%, attentive share 4.0%, verification undersupply 10/10 seeds, value 0.38 — the structural findings survive a third consecutive prior source.

## Distribution analysis (added same day)

`src/analyze_distributions.py` fits Betas by method of moments, renders histograms with fitted overlays to `results/<run>/figures/`, and tests a second panel against the first's empirical distribution. Key numbers at N=1000:

| Field | Beta(a, b) | KS | archetype-mean spread |
|---|---|---:|---:|
| platform_trial_probability | (4.68, 1.95) | 0.111 | 0.71 |
| monthly_platform_use_probability | (3.21, 4.14) | 0.070 | 0.56 |
| direct_planning_participation_probability | (2.36, 3.51) | 0.046 | 0.54 |
| delegation_probability | (5.59, 4.96) | 0.106 | 0.50 |
| would_accept_delegation | (3.99, 5.09) | 0.075 | 0.68 |
| delegate_platform_use_rate | (4.20, 3.64) | 0.086 | 0.55 |
| delegate_planning_coverage | (5.34, 5.30) | 0.059 | 0.45 |

The fields are **archetype mixtures**, not clean Betas: per-archetype means span up to 0.71 (trial: opposed 0.17 → tech professional 0.88), which is what degrades the single-Beta fit on trial and delegation (KS ~0.11). Where a distribution is needed downstream, prefer the per-archetype mixture or empirical resampling over the pooled Beta.

**Is gemma inside the gpt-5.5 distribution?** Both statements are true and they answer different questions. Gemma's pooled means fall inside the *person-level* support of the gpt-5.5 panel — at the tails (delegation at the 98th percentile, would-accept at the 97th, direct participation at the 7th): individual "gemma-like" respondents exist in the gpt-5.5 population. But as a *population*, gemma is definitively different: against the sampling distribution of the mean, |z| runs 14–57, and the distribution overlap coefficients are only 0.15–0.37 — partly because gemma's person-level spread is 2–3× narrower (it collapses heterogeneity, sd 0.05 on delegation vs 0.15). Gemma is not a plausible resample of gpt-5.5; it is a different prior with a few of its moments landing inside the other's tails.

## Caveats

Assumed archetype weights are not census-fitted; the convergence shown is *within-model* stability of gpt-5.5 under persona variation, not agreement with human behavior. Model-to-model divergence (see the gemma comparison) remains the larger uncertainty, and the human instrument remains the calibration that counts.
