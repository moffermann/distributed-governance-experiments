# Behavioral Integration Run Results (Experiment C) — 2026-07-06

## Execution

First integrated architecture-under-behavioral-population runs, per the pre-registered mapping of `../behavioral-adoption-abm/OUTPUT_TO_ADVERSARIAL_ABM.md`:

- engine: post-audit v0.4 (`ENGINE_AUDIT_2026_07_06.md`);
- four generated scenarios (committed under `scenarios/behavioral-*.json`, each with a `behavioralProvenance` block), population blocks from behavioral sweep means (10 seeds each);
- 5 architectures × 20 runs × seed 1 per scenario, common-world paired comparison;
- reference: the post-audit `baseline-medium` (imposed population).

Population blocks (imposed reference vs generated):

| Share | imposed | behavioral-baseline | llm-calibrated | high-friction | delegation-first |
|---|---:|---:|---:|---:|---:|
| attentive | 0.050 | 0.041 | 0.050 | 0.025 | 0.050 |
| salience | 0.250 | 0.092 | 0.104 | 0.063 | 0.102 |
| profile | 0.200 | 0.088 | 0.094 | 0.043 | 0.115 |
| delegator | 0.100 | 0.122 | 0.215 | 0.073 | 0.114 |
| passive (default rule) | 0.400 | 0.657 | 0.538 | 0.796 | 0.619 |

The imposed `attentiveShare: 0.05` was already behaviorally realizable (emergent 2.5–5.0%). The big imposed-vs-emergent gap is elsewhere: realistic populations are far more passive (54–80% vs 40%) and far less salience-active (6–10% vs 25%).

## Verified value per unit of budget (mean ± sd, 20 runs)

| Architecture | reference (imposed) | behavioral-baseline | llm-calibrated | high-friction | delegation-first |
|---|---:|---:|---:|---:|---:|
| status_quo | 0.128 | 0.127 | 0.127 | 0.127 | 0.128 |
| participatory_weak_verification | 0.029 | **0.000** | **0.000** | **0.000** | **0.000** |
| participatory_weak_verification_full_budget | 0.104 | 0.104 | 0.103 | 0.105 | 0.107 |
| core_v0_tutored_central_planning | 0.214 | 0.231 | 0.224 | 0.274 | 0.239 |
| core_v0_tutored_distributed_planning | 0.262 | 0.307 | 0.277 | **0.340** | 0.300 |
| **core-distributed ÷ status quo** | **2.05×** | **2.42×** | **2.18×** | **2.68×** | **2.34×** |

## Prediction accounting (pre-registered in OUTPUT_TO_ADVERSARIAL_ABM.md)

- **P1 — held.** The ranking (core distributed > core central > status quo > participatory full-budget > participatory weak) is identical under every behavioral population.
- **P2 — held in direction, upper band exceeded.** The declared band was 1.6×–2.6×; the observed multipliers run 2.18×–2.68×, with the maximum under *low* adoption. The Core advantage is not merely robust to realistic participation — it grows with passivity, because the default layer routes the passive share through the calibrated planning vector while the status quo's planner stays weakly informed.
- **P3 — refuted, informative.** More delegation (llm-calibrated, 21.5% delegators) *lowered* Core-distributed verified value relative to behavioral-baseline (0.277 vs 0.307). In this engine, delegates allocate with attentive-grade individual noise, while the default layer follows the calibrated aggregate vector (corr ≈ 0.83) — the aggregate beats individual informed picks, so weight moving from passive to delegated *loses* information. This is the corpus's E3 lesson resurfacing from a new direction: allocation quality is carried by the informational quality of the vector the default layer follows. Participation's informational value lies upstream — in *constructing* that vector (the planning-vector and behavioral planning-layer experiments) — not in per-project routing.
- **P4 — held, stronger than predicted.** Under high friction the weak participatory variant does not merely degrade: it ceases to function (8.8% budget absorption, verified value 0.000 — nothing reaches its funding target), while Core-distributed posts its *best* result (0.340). The prediction said Core's absolute value would "decline little"; it did not decline at all.

## Reading

Two headline sentences survive every population this experiment can currently generate:

1. **The architecture ordering is behavioral-population-invariant**, and the Core-distributed advantage over the status quo sits at 2.0–2.7× verified value per unit of budget.
2. **Participation without a default layer is not a weaker architecture — it is a non-functioning one** under realistic adoption: every behaviorally generated population drives the no-default participatory variant's verified delivery to zero.

And one honest boundary: the P3 result is conditional on the default vector's exogenous calibrated quality. In reality that quality is *produced* by attentive and delegated participation (the planning-construction layer), so "more passivity scores better here" must not be read as "participation is dispensable" — it means the engine correctly locates participation's value in planning construction rather than in individual project picking, exactly where the corpus put it (E3/E4, docs/87).

## Caveats

Behavioral shares come from a synthetic-and-llm-elicited behavioral model (no human data yet); planning mixes, fiscalizer composition, and attacks remain at the base scenario's calibration; the 1,000-citizen behavioral world informs shares applied to a 10,000-citizen adversarial world (scale-free by construction, declared). The weak-participatory zero is partly a funding-target artifact — with 6–15% active shares, 24 cycles cannot complete any project at the configured scarcity; real systems would see partially funded, undelivered projects, which is the same failure expressed differently.
