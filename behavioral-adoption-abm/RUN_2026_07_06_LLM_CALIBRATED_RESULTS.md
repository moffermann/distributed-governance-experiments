# LLM-Calibrated Run Results — 2026-07-06

## Execution

First run of the ABM under LLM-elicited priors instead of synthetic guesses:

- calibration source: `planning-behavior-calibration` panel run `2026-07-06-gpt-5.5-n15` — 90 personas (6 archetypes × 15 variations), gpt-5.5 via the codex-exec backend (reasoning effort `low`, schema-enforced output), 90/90 valid in 105 seconds, prompt version v0.3;
- mapping: `OUTPUT_TO_BEHAVIORAL_ABM.md` executed by `apply_llm_calibration.py` → `scenarios/llm_calibrated.json`;
- comparison: baseline (synthetic priors) vs `llm_calibrated`, 10 seeds each, 104 ticks, 1,000 citizens.

These are **llm-elicited synthetic priors, not empirical data**. Stated intent overestimates real behavior (the panel's rejection share maps to 0.0 because no persona reported trial probability below 0.2 — the intention-action gap in its purest form); the human instrument, unchanged, replaces these priors when administered.

## Mapped parameters

| Parameter | Synthetic | LLM-elicited (gpt-5.5) |
|---|---:|---:|
| `micro_delegate_willingness` | 0.250 | 0.452 |
| `institutional_delegation_propensity` | 0.250 | 0.235 |
| `permanent_rejection_rate` | 0.350 | 0.000 |
| `planning_attendance_base.direct_active` | 0.550 | 0.450 |
| `digital_confidence` beta mean | 0.524 | 0.651 |

The elicited institutional-delegation propensity (0.235) lands almost exactly on the synthetic guess (0.25) — independent support for the corpus's trusted-microdelegation baseline. The panel's preferred-delegate-type distribution gives 74% trusted-person types against 23% institutional types (would-not-delegate 3%).

## Baseline vs LLM-calibrated (10 seeds)

| Metric | baseline (synthetic) | llm_calibrated |
|---|---:|---:|
| Registered users | 52.1% | 72.3% |
| Active users | 34.3% | 52.5% |
| Default-rule share | 65.7% | 47.5% |
| Delegator share (population) | 12.2% | 26.1% |
| Active delegates | 75 | 163 |
| Delegation HHI | 0.018 | 0.009 |
| Micro-delegation weight share | 66.2% | 76.6% |
| **Attentive share (mean)** | **4.1%** | **4.1%** |
| Distributed planning correlation | 0.977 | 0.981 |
| Evidence coverage | 0.62 | 0.61 |
| Thin-market failure risk | 0.39 | 0.39 |
| Value delivered share | 0.42 | 0.41 |
| Viability flags | evidence 10/10, verification 5/10 | evidence 10/10, verification 6/10 |

## What is sensitive to priors and what is not

**Sensitive (adoption-side):** registration, activation, and delegation volume scale with the elicited optimism — more willing micro-delegates flood the supply, halving concentration and pushing micro-delegation weight to 77%.

**Robust (structural):** the two headline findings survive the calibration source unchanged. The attentive share stays at ~4.1% — more users but the same fraction attends planning — and the verification bottleneck fires in 10/10 seeds in both regimes: participation optimism cannot buy verification capacity, so delivered value does not move (0.42 vs 0.41). The binding constraint is structural, not behavioral.

**Emergent-vs-elicited cross-check:** `delegate_planning_coverage` emerges at 0.533 under calibrated priors; the panel independently elicited 0.516 for the same quantity — the mechanism and the personas agree. `delegate_platform_use_rate` emerges higher (0.87) than elicited (0.54), because in-model delegates are drawn from active users; flagged as the next reconciliation point.

## Model sensitivity

The same instrument on the local `gemma-3-4b` panel produces markedly different pooled levels (e.g., delegation probability 0.75 vs 0.52; would-accept-delegation 0.73 vs 0.42, with implausible archetype orderings such as low-digital elders accepting delegation at 0.85). Both models agree on the micro-over-institutional delegate preference (84/15 and 74/23). LLM-elicited priors are model-dependent; any downstream use must cite panel run id and model, and conclusions should be limited to patterns stable across models until human data exists.

## Recalibration from the N=1000 weighted panel (same day)

The scenario was re-derived from the 1,000-persona population-weighted panel over the extended 20-archetype set (`planning-behavior-calibration/RUN_2026_07_06_N1000_PANEL_RESULTS.md`). Mapped parameters moved little — micro willingness 0.452 → 0.475, attendance base 0.450 → 0.435 — with one qualitative fix: the ideologically-opposed archetype supplies genuine rejection, so `permanent_rejection_rate` maps to 0.078 instead of the n=90 panel's implausible 0.000. Re-run (10 seeds): registered 68.3%, active 49.8%, delegator share 24.1%, attentive share 4.0%, evidence undersupply 10/10 seeds, value 0.38. The structural findings now hold across three prior sources: synthetic, llm-elicited n=90, and llm-elicited N=1000 weighted.

## Distribution-based calibration and the mean-sufficiency check (added same day)

Two follow-ups on whether pooled *means* are the right thing to inject:

**Mapping correction.** The attendance inversion had divided by the willingness civic factor (0.5 + E[civic] = 0.925) instead of the attendance civic factor (0.5 + 0.5·E[civic] = 0.7125), understating attendance by ~23%. Corrected: `planning_attendance_base.direct_active` maps to 0.565 (not 0.435), and the calibrated attentive share is ~5.0%.

**Mean vs distribution, resolved empirically and theoretically.** For any parameter that terminates in a Bernoulli draw (e.g. delegate willingness), E[bernoulli(P)] = E[P]: the mean is provably sufficient and a fitted distribution adds nothing. A distribution matters only under nonlinearity (trait sigmoids — which is why trait priors are Beta-configurable) or **persistence**. The new `planning_attendance_distribution` config draws a persistent per-citizen attendance propensity from the panel's fitted Beta(2.36, 3.51) — the same subpopulation attends round after round — generated as `scenarios/llm_calibrated_dist.json` via `--distributions`. Result (10 seeds each): attentive share 4.98% (mean mode) vs 4.70% (persistent mode), distributed correlation 0.981 vs 0.979, value overlapping. Persistence narrows *who* attends, but delegated representation keeps the planning vector's quality intact — the mean approach is adequate for this model, now as a checked result rather than an assumption. The distribution machinery stays available for when person-persistent signal biases enter the model, where it would bind.

## Backend note

The panel's codex-exec backend (OpenAI Codex CLI, ChatGPT-plan auth) processes requests with true server-side parallelism: 90 personas in 105 s (~1.2 s effective per response) against ~20 s per response on the serialized local LM Studio server — roughly a 17× throughput gain at 12 concurrent requests, with schema-enforced output in both backends. Reasoning effort `minimal` is rejected by the model's built-in tools; `low` is the fast tier that works.
