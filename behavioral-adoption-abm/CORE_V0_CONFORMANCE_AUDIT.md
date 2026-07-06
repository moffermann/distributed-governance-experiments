# Core v0 Conformance Audit — 2026-07-06

## Purpose

This document records a full audit of the behavioral adoption ABM's executable implementation against the Core v0 architecture corpus, the corrections applied as a result, and the conformance certification that the corrected implementation now carries.

The audit was performed on the state committed as "Add Mesa run result analysis for behavioral ABM" (the first executable MVP plus its first Mesa run). All corrections described here were applied in the same change set as this document.

## Normative sources checked

| Source | What it governs here |
|---|---|
| `docs/101_CORE_V0_MINIMAL_PUBLISHABLE_MODEL.md`, "What you, a citizen, actually do" | The canonical citizen action set: direct allocation, following, commenting, complaining, revocable delegation, and — critically — "do nothing — your allocation follows the public default rule" |
| `docs/107_REPUTATION_INFORMS_NEVER_EXCLUDES_AND_A038_RESOLUTION.md` | Reputation may inform choices; nothing on the platform excludes an actor from being chosen |
| `docs/108_CITIZEN_ALLOCATION_SECRECY_AND_A039_RESOLUTION.md` | The citizen-to-allocation link is secret; only voluntary self-disclosure is socially observable |
| `docs/28_CITIZEN_AUTOMATIC_ALLOCATION_PROFILE_FLOW.md` | Profile-driven automatic allocation, including edit/pause/deactivate and override |
| `experiments/planning-vector-construction/CORE_V0_PLANNING_CHANNEL_MODEL.md` | The downstream consumer's channel taxonomy (attentive, delegated, mandate) and its required inputs |
| `experiments/planning-vector-construction/TRUSTED_MICRODELEGATION_MODEL.md` | The corpus's expected Core v0 delegation pattern: trusted microdelegation as baseline, institutional/broker delegation as stress case |
| `ROLE_ONTOLOGY.md`, `METRICS.md`, `MODEL_DESIGN.md` (this experiment) | The experiment's own behavioral specification |

## Findings and corrections

### F1 — Delegation was modeled backwards relative to the corpus (conformance, critical)

The MVP modeled delegation exclusively as citizens choosing among a small fixed pool of institutional delegates (24 in baseline) scored by reputation and visibility. `TRUSTED_MICRODELEGATION_MODEL.md` defines the Core v0 baseline as the opposite: `citizen -> trusted person nearby`, with many low-weight delegates, low global concentration, and high interpersonal alignment; institutional/broker delegation is explicitly the stress channel, not the baseline.

**Correction.** Citizens can now act as trusted micro-delegates for their own social circle (`micro_delegate_willingness`, expressed only while registered and non-abandoned). Delegate choice is two-stage: the citizen first chooses a channel by comparing the best available option in each (a single softmax over both pools would let the institutional channel win by sheer candidate count), then chooses within the channel. Citizens with no trusted person available hand weight to an impersonal delegate only with probability `institutional_delegation_propensity`; otherwise their allocation stays on the public default rule. The `delegation_first` scenario was rewritten as the explicit institutional-stress case. Post-correction baseline: micro-delegation holds ~64% of delegated weight across ~77 active delegates (HHI ≈ 0.017, top delegate ≈ 4%); the stress scenario concentrates to HHI ≈ 0.073 with a ~17% top delegate.

### F2 — The public default rule was missing (conformance, critical)

`docs/101` states that a citizen who does nothing still allocates: "your allocation follows the public default rule (which tracks published planning priorities)". The MVP treated non-active citizens as absent budget: projects were funded only by `active_user_share`, so low adoption silently starved execution — contradicting the architecture, in which the mandate share always flows.

**Correction.** Project funding now receives the non-active remainder through the default layer at reduced routing efficiency (`default_routing_efficiency`), and the integration outputs expose `default_rule_share = 1 − active_user_share` so downstream experiments never read inactivity as lost allocation signal.

### F3 — Integration outputs did not cover the downstream experiment's inputs (integration)

The planning-vector experiment consumes `delegatorShare`, `delegateCount`, `delegateConcentration`, and `delegatePlatformUseRate`. None was produced.

**Correction.** New integration outputs and their mapping:

| Planning-vector parameter | Behavioral ABM output |
|---|---|
| `delegatorShare` | `delegator_share` (population basis) |
| `delegateCount` | `active_delegate_count` |
| `delegateConcentration` | `delegation_concentration_hhi` (plus `top_delegate_share`) |
| `delegatePlatformUseRate` | `delegate_platform_use_rate` (weight-weighted; emergent for micro-delegates, institutional delegates treated as active professionals) |
| `delegatePlanningCoverage` | **not produced** at audit time — superseded the same day by the planning layer ([`PLANNING_LAYER_DESIGN.md`](PLANNING_LAYER_DESIGN.md)): `delegate_planning_coverage` is now emergent |

`micro_delegation_weight_share` / `institutional_delegation_weight_share` additionally let the consumer distinguish the trusted-microdelegation regime from the institutional stress regime.

### F4 — Results were not reproducible across environments (technical, critical)

The Mesa and stdlib code paths seeded different RNG streams; the same seed produced mean trust 0.95 under Mesa 3.5.1 and 0.58 under the stdlib shim. The first run document had already flagged the Mesa 3.x initialization issue (its recommended change #6).

**Correction.** The model initializes Mesa with `rng=self.seed` (integer, per the run note) and then unconditionally draws every random number from one `random.Random(seed)` stream. Verified: `final_metrics.json`, `integration_outputs.json`, and `timeseries.csv` are byte-identical (SHA-256) between Mesa 3.5.1 and the no-Mesa fallback.

### F5 — Declared parameters were dead (technical)

`verification_requirement_per_project`, `evidence_requirement_per_project`, and `recommendation_strength` existed in every scenario file but were never read; `trust_recovery_strength` was used simultaneously as an event probability and a magnitude.

**Correction.** The requirement parameters now define verification/evidence coverage (`coverage = participating × capacity / (projects × requirement)`, with new `fiscalizer_capacity` and `evidence_producer_capacity` priors), which drive `thin_market_failure_rate` and project outcomes. `recommendation_strength` and `negative_word_of_mouth_strength` now scale the positive/negative social-proof terms in registration. `trust_recovery_event_rate` (probability) was split from `trust_recovery_strength` (magnitude).

### F6 — No behavioral inertia anywhere (validity)

Every active citizen re-drew their participation mode from the softmax every tick, and every role agent re-drew participation i.i.d. every tick. Mode shares were therefore stationary softmax noise, delegation "concentration" was uniform-random rather than emergent, and the switching/revocation metrics defined in `METRICS.md` were unmeasurable.

**Correction.** Modes persist and are reconsidered with probability `mode_reconsideration_rate`, boosted by shocks (`shock_reconsideration_boost` under outages, controversies, or high failure stock) — which makes revocation elasticity to bad outcomes an emergent, measured quantity (`delegate_switching_rate`, `delegation_revocation_rate`). Role markets (executors, fiscalizers, evidence producers) use sticky recruitment/dropout hazards (`role_entry_rate`/`role_exit_rate`, unbiased around each agent's propensity) instead of weekly redraws.

### F7 — Registration and awareness saturated (validity, flagged by the first run)

A constant weekly registration hazard drove registration to ~100% in every scenario within 104 ticks, including under high friction — the first run document itself called the adoption outputs unusable for institutional inputs.

**Correction.** Registration is considered seriously once on first exposure and afterwards only occasionally, mostly re-triggered by social proof (`registration_reconsideration_rate`); the intercept and friction/privacy penalties were recalibrated; aware citizens can permanently reject (`permanent_rejection_rate`, weighted by ideological closure and privacy concern — the "reject permanently" outcome of `ROLE_ONTOLOGY.md`); campaign-driven awareness is bounded by `awareness_ceiling` (media reach). Post-correction: baseline registration ≈ 51%, high-friction ≈ 35%, AI-assisted ≈ 62% — friction now has first-order adoption effects.

### F8 — Trust saturated and churn vanished (validity)

Project outcomes pumped an unnormalized success stock to its cap, pinning mean trust near 0.95 and making abandonment ≈ 0 under Mesa. Unaware citizens also updated trust on platform events they could not have observed.

**Correction.** Outcome shocks are normalized by portfolio size, stock decay recalibrated, trust updates gated to aware citizens, the active-user drift reduced, and the churn hazard recalibrated without a hard threshold cliff. Post-correction baseline: mean trust ≈ 0.64 with real cross-seed variance, abandonment ≈ 13%, reactivation ≈ 85% — and the `trust_declining` viability flag can actually fire.

### F9 — Metrics gaps against the experiment's own specification (completeness)

`METRICS.md` defines minimum-viability thresholds, switching/revocation rates, and reactivation rate; none was implemented.

**Correction.** Added `viability` flags (active signal, delegation concentration, verification/evidence coverage, executor supply, abandonment, monotonic trust decline) to `final_metrics.json` and `integration_outputs.json`, plus `reactivation_rate`, `delegate_switching_rate`, `delegation_revocation_rate`, `mean_trust_registered`, and `permanent_rejection_share`. A multi-seed sweep runner (`run_sweep.py`) replaces the ad-hoc replication procedure of the first run.

## Conformance checklist (post-correction)

| Core v0 requirement | Source | Model mechanism | Status |
|---|---|---|---|
| Citizen actions are optional; inattention is a designed-for condition | docs/101 | All states voluntary; non-use, rejection, and abandonment are normal outcomes | Conforms |
| Doing nothing routes allocation through the public default rule | docs/101 | `default_rule_share` output; default-routed project funding | Conforms |
| Delegation is revocable at any time, one click | docs/101, docs/21 | Revocation on reconsideration, shocks, or invalid target; rates measured | Conforms |
| Trusted microdelegation is the baseline; institutional delegation is the stress case | TRUSTED_MICRODELEGATION_MODEL.md | Micro channel dominant in baseline (~64% of weight); `delegation_first` is the institutional stress scenario | Conforms |
| Reputation informs, never excludes | docs/107 | Reputation only enters choice scores; no mechanism excludes any actor; role participation is self-selection | Conforms |
| Citizen-to-allocation link is secret; only self-disclosure is observable | docs/108 | Social signals expose only registered/active/abandoned/recommending status; no agent observes another's allocation targets; no receipts exist | Conforms (by construction) |
| Automatic profiles allocate within bounds; citizen can pause/override | docs/28 | `profile_driven` mode exists; pause/override dynamics not yet modeled | Declared gap (bounded) |
| Verification is required and separate from execution | docs/101 | Coverage vs. per-project requirements gates outcome quality; supply side only | Conforms within boundary |

## Boundary: what this model deliberately does not claim

- It does not model architecture performance, attacks, collusion, or fiscalizer assignment — that is the adversarial ABM's job.
- It does not construct planning vectors and therefore does not emit `delegatePlanningCoverage`.
- It does not split profile-driven activity into configured/active/overridden states yet (first run's recommendation #3, still open).
- Every coefficient is synthetic. Nothing here is empirically calibrated; the Stage 5 discipline of `ROADMAP.md` (mark every parameter synthetic/assumed/literature-derived/prototype-derived/pilot-derived) applies in full. Current status: all synthetic.

## Calibration flags for future work

- `permanent_rejection_share` emerges around 30% of the population — plausible but unvalidated.
- `delegate_platform_use_rate` emerges around 0.85, optimistic against the 0.70 prior of `TRUSTED_MICRODELEGATION_MODEL.md`; micro-delegates self-select for civic interest in this model, which may overstate their own activity.
- `fiscalizer_capacity` / `evidence_producer_capacity` are guesses that directly set the verification bottleneck's depth; they must be among the first empirically grounded parameters.

## Certification

The executable implementation (`src/behavioral_adoption_abm/core.py`), its scenarios, and its outputs conform to Core v0 as specified in the corpus documents cited above, within the declared MVP boundary. All conformance deviations found by this audit (F1–F3) and all technical/validity defects (F4–F9) were corrected in this change set. Results are byte-identical with and without Mesa 3.5.1 for the same seed. Remaining gaps are declared above rather than hidden, following the corpus's integrate-or-bound discipline.
