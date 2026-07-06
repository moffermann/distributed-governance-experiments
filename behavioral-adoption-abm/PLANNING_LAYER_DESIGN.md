# Planning Layer Design — End-to-End Extension

## Purpose

This document specifies (before implementation was run) the planning layer added to the behavioral adoption ABM, turning it into an end-to-end model:

```text
adoption -> participation modes -> attentive/delegated planning signals
-> planning-vector construction (distributed vs central)
-> default-rule routing -> project funding -> execution outcomes
-> trust feedback -> adoption
```

It exists to answer three questions the base model could not:

1. **What share of citizens is actually attentive** in the planning sense — the `attentivePlanningShare` the planning-vector experiment imposes as a parameter — when attention emerges from adoption, friction, trust, and mode choice?
2. **Does the planning-vector experiment's headline ordering survive behavioral emergence?** That experiment (`planning-vector-construction`, run 2026-07-06, 200 runs, seed 42) finds Core v0 distributed channels at corr(latent) 0.815–0.938 with only 2–10% attentive citizens, against representative central planning at 0.315–0.650 and raw salience at 0.187. Its participation shares are imposed; here they are emergent.
3. **What does each planning regime deliver end-to-end**, in verified value, when the same behavioral population lives under a distributed vector or a central one?

## Validation target

From `experiments/planning-vector-construction/results/core-v0-planning-channels` (v0.5, 200 runs, seed 42, 10,000 citizens, 80 targets):

| Vector family | corr(latent) |
|---|---:|
| Core v0 distributed channels (9 variants) | 0.815 – 0.938 |
| Central representative (high alignment → crisis) | 0.650 → 0.315 |
| Salience only | 0.187 |

## Model additions

### Planning targets and ground truth

- `planning_target_count` (J, default 16) public-need targets with a latent `true_need` vector (normalized gamma draws).
- `target_salience`: visibility of each need, only partially correlated with truth (0.5 truth + 0.5 noise, normalized). Salience is what herding and the planner's attention see; truth is what delivers value.
- Every project belongs to one target category. A project's delivered value is `latent_value × need_weight(category)`, so funding a real need is worth more than funding a visible one.

### Attentive citizens (endogenous)

Every `planning_round_interval` ticks (default 4 ≈ monthly), active citizens may contribute an explicit planning signal. Attendance probability depends on mode — direct 0.55, hybrid 0.40, profile-driven 0.15, delegated 0.00 (they delegated exactly this act) — scaled by civic interest and by `planning_attendance_scale` (the experimental dial). Per `CORE_V0_PLANNING_CHANNEL_MODEL.md`, **allocation profiles and passive default routing contribute nothing to the planning vector**; profile users may attend in person, at low propensity.

An attentive citizen reviews only `~0.5 × attention_budget × J` targets (coverage is bounded by attention), with signal noise decreasing in civic interest.

**`attentive_share`** = citizens contributing an own signal in the round / population. This is the number the user asked for, and it is an output, not a parameter.

### Delegated planning signals (endogenous)

Delegates who are themselves active contribute signals carrying their `delegated_weight`:

- **Micro-delegates** (citizens): planning coverage `0.30 + 0.45 × attention_budget` — partial but meaningful, per `TRUSTED_MICRODELEGATION_MODEL.md` ("a delegate can be active but still review only part of the vector"). `delegate_planning_coverage` is therefore **emergent** here, where the sibling experiment uses priors (0.35–0.70).
- **Institutional delegates**: high coverage (0.70) but politically packaged signal (0.8 truth + 0.2 salience, higher noise) — active professionals, less personal preference knowledge.

`planning_representation_share` = (attentive citizens + delegated weight represented by contributing delegates) / population.

### Distributed vector construction

Per target: weighted mean of all signals received. Targets nobody reviewed decay toward a neutral prior (`stale_signal_retention`), per the microdelegation model's stale-fallback rule. Normalized.

### Central planner (comparator)

A bandwidth-limited authority: it reviews the top `central_planner_bandwidth_fraction × J` targets **selected by salience** (visible needs get planner attention) with noise `central_planner_noise`; unreviewed targets are filled with salience itself (the planner's default is visibility). This mirrors the representative information-loss mechanism of the sibling experiment without copying its numbers; where the emergent central correlation lands within their regime family (crisis → high alignment) is itself a result.

Both vectors are constructed every round in every run, so every scenario yields a paired distributed-vs-central quality comparison; `planning_mode` decides only which vector the default layer follows for funding.

### End-to-end funding and value

Project funding per tick combines (docs/101, "What you, a citizen, actually do"):

- **active routing** (`active_user_share`): citizens route by 0.5 salience + 0.5 perceived quality — herding included;
- **default routing** (the non-active remainder × `default_routing_efficiency`): follows the *published planning vector* of the operating mode — the direct implementation of "your allocation follows the public default rule (which tracks published planning priorities)".

Delivered value accumulates on success as `latent_value × need_weight(category)`; `value_delivered_share` divides by the fixed total potential of the portfolio, so scenarios are comparable.

### Amendment (2026-07-06, before any comparison run)

The first smoke run produced a distributed correlation of 0.995 — a wisdom-of-crowds artifact: with unbiased signal noise, averaging across contributors converges on truth trivially, and the initial salience construction (0.5 truth) made the central comparator too truthful as well. Both distortions the sibling experiment explicitly parameterizes (`attentiveSalienceBias`, `attentiveCoverageBias`) were added before any comparison was run: attentive perception blends salience into truth (`attentive_salience_bias`, 0.35; micro-delegates 0.20 — they know their circle's real needs better), attentive target sampling clusters on visible needs (so invisible needs can stay unreviewed), and salience itself now carries only `salience_truth_mix` = 0.25 truth. The pre-registered expectations below were not modified.

## Pre-registered expectations

Written before the first end-to-end run:

- **P1.** The emergent distributed correlation at baseline adoption lands **at or below** the sibling experiment's Core v0 band (0.815–0.938): behavioral friction, partial coverage, and non-representative attentiveness should cost quality. How much is the finding.
- **P2.** Distributed beats the central comparator at baseline attendance, and there exists a low-attendance crossover below which the bandwidth-limited planner wins. Locating the crossover in `attentive_share` terms is the deliverable.
- **P3.** End-to-end `value_delivered_share` ordering follows vector-quality ordering, with a compressed gap: active routing and salience herding are identical across planning modes and dilute the default layer's advantage.
- **P4.** `delegate_planning_coverage` emerges inside the sibling experiment's prior band (roughly 0.35–0.70).
- **P5.** The institutional-stress scenario (`delegation_first`) degrades the distributed correlation only mildly relative to baseline (the sibling experiment sees 0.861 → 0.842 under concentration), but concentrates representation.

## Conformance notes

- Profiles and default routing never construct the planning vector (`CORE_V0_PLANNING_CHANNEL_MODEL.md`, "It should not be constructed from").
- The default layer follows published planning priorities (docs/101) — in central mode those are the authority's, in distributed mode the aggregated citizen/delegate vector; the behavioral population is identical.
- Delegated planning weight is represented signal, not assumed activity: delegate platform use and coverage gate it (`TRUSTED_MICRODELEGATION_MODEL.md`).
- No agent ever observes another citizen's allocation or planning signal; only aggregates enter the vectors (docs/108).

## Outputs added

Integration outputs: `attentive_share`, `attentive_share_mean`, `planning_representation_share`, `planning_signal_coverage`, `delegate_planning_coverage`, `distributed_planning_correlation`, `central_planning_correlation`, `followed_planning_correlation`, `value_delivered_share`, plus the general enrichment set (`trust_p10/p50/p90`, `top_10_delegate_share`, `sustained_active_user_share`, `mean_awareness_to_registration_delay_ticks`). `final_metrics.json` additionally carries `trust_by_state` and `abandonment_reason_distribution`.

New viability flag: `distributed_planning_weak` — the behavioral population failed to out-inform the bandwidth-limited planner.

New scenario: `central_planning.json` (baseline behavioral parameters, `planning_mode: "central"`).

New runner: `run_planning_comparison.py` — sweeps `planning_attendance_scale` across seeds and both planning modes to locate the attentive-share crossover and the end-to-end value gap.

## Boundary

The planning layer models signal construction and routing quality, not deliberation, gaming, or elicitation honesty — the open problem of docs/87 and docs/91 (honest elicitation under gaming and clientelism pressure) is out of scope here and stays with the adversarial ABM. All coefficients remain synthetic pending Stage 5 calibration.
