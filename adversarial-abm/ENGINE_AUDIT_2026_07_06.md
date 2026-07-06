# Engine Audit — 2026-07-06

## Purpose

Audit of the executable v0 engine (`src/index.mjs`) for implementation bugs and Core v0 conformance, performed before the engine is used for the integrated behavioral runs (Experiment C). All corrections were applied in this change set as engine v0.4; the pre-fix reference numbers below were produced from the committed v0.3 state.

## Findings and corrections

### AF1 — Random noise inside the sort comparator (bug, critical semantics)

Attentive citizens ranked their sampled projects with a comparator that drew **fresh perception noise on every pairwise comparison**. This is a non-transitive comparator: the sort's outcome is implementation-defined rather than a ranking of noisy perceptions, the effective information noise diverges from the configured `informationNoise` semantics (each comparison was an independent coin flip for close values), and the RNG draw count depended on the sort algorithm's internal comparison count.

**Correction.** Perception is computed once per citizen-project pair (`utility = latentValue + noise + terms`), then ranked. This is what `AGENT_DECISION_MODEL.md`'s attentive-citizen specification describes.

### AF2 — `profileShare` and `delegatorShare` were dead parameters (conformance, critical for integration)

The scenario declares a five-way population split (attentive 5%, salience 25%, profile 20%, passive 40%, delegators 10%) and `AGENT_DECISION_MODEL.md` specifies profile-driven and delegating citizens as distinct channels with their own scoring — but the engine computed `remaining = N − attentive − salience` and routed the whole 70% through the passive mode. Profile users and delegators silently inherited the default planning vector in Core variants. This mattered doubly: it inflated Core results (30% of the population borrowed the high-quality calibrated planning signal instead of allocating with their own noisier information), and it made `delegatorShare` — the largest behavioral-vs-imposed discrepancy Experiment C tests — a no-op.

**Correction.** Where the architecture provides a default layer (`passiveAllocationMode: "planning"`, per the spec's `hasDefaultLayer` condition):

- **profile-driven citizens** allocate through a noisier value proxy with a near-completion preference (`noiseScale` 1.5, `+0.20 × fundingProgress`) — configured preferences, not inspection;
- **delegating citizens** allocate through delegates: represented weight in blocks (`population.delegationBlockSize`, default 3 — the trusted-microdelegation proxy of many small, informed delegates) with attentive-grade information.

Architectures without a default layer keep the previous behavior: those shares remain in the passive block, per the spec.

### AF3 — Unabsorbed active allocation evaporated instead of following the default rule (Core v0 conformance, immaterial in practice)

When an active citizen's sampled or visible projects were already full mid-cycle, the unabsorbed allocation vanished. Under Core v0 the unexercised remainder follows the public default rule (docs/101, "or do nothing — your allocation follows the public default rule"). Measured impact at baseline parameters: ~6 units out of 240,000 (0.003%) — corrected for semantics, declared immaterial. The weak participatory variants keep the loss: low absorption is the failure mode they exist to demonstrate.

### AF4 — Attentive samples drawn with replacement (minor)

Citizens could sample the same project twice, shrinking their effective comparison set. Corrected to a without-replacement partial Fisher-Yates draw.

### AF5 — Notes, not corrected

- The per-architecture RNG stream is seeded with the architecture's **index** in the scenario list, so reordering `architectures` changes individual draws (paired-world comparison is unaffected; summary means shift within noise). Acceptable; documented here.
- Milestone-level conditional disbursement is not modeled: execution resolves in one step with retention/guarantee/reputation as deterrence terms. This is a declared v0 simplification (`IMPLEMENTED_VARIANTS.md`), consistent with the formal note's deterrence inequality in reduced form — bounded, not hidden.

## Core v0 conformance checklist

| Requirement | Source | Engine mechanism | Status |
|---|---|---|---|
| Reputation informs, never excludes | docs/107 | `reputationLoss` and `futureSelectionLoss` are deterrence *costs* (pool exit by lost preference); no mechanism excludes any executor | Conforms |
| Default rule follows published planning priorities | docs/101 | `passiveAllocationMode: "planning"` routes passive weight by the planning vector; leftover now included (AF3) | Conforms |
| Delegation is a distinct, informed, plural channel | docs/101, TRUSTED_MICRODELEGATION_MODEL | Implemented in AF2 as small-block informed allocation | Conforms (proxy) |
| Profiles are bounded automation, not planning | docs/28, CORE_V0_PLANNING_CHANNEL_MODEL | Profile channel routes allocation only; planning vectors come from the calibrated mixes | Conforms |
| Verification separated from execution | docs/101 | Detection probability independent of the executor; review confidence caps verified value | Conforms |
| Funding conditional on delivery | docs/101 | Reduced form (retention/guarantee terms in the deterrence inequality); milestones not modeled | Bounded, declared |

## Pre-fix vs post-fix baseline (baseline-medium, seed 1, 20 runs)

Verified value per unit of budget:

| Architecture | v0.3 (pre-audit) | v0.4 (post-audit) |
|---|---:|---:|
| status_quo | 0.128 | 0.128 |
| participatory_weak_verification | 0.031 | 0.029 |
| participatory_weak_verification_full_budget | 0.106 | 0.104 |
| core_v0_tutored_central_planning | 0.254 | 0.214 |
| core_v0_tutored_distributed_planning | 0.314 | 0.262 |

The ranking is unchanged. The Core variants **lose** ground (distributed: 2.45× → 2.05× over status quo): 30% of the population now allocates with its own noisier information instead of silently borrowing the calibrated planning vector. The audit made the model more honest and the proposed architecture weaker — the folder's own design rule ("the simulator must make the adversary stronger before it makes the proposed architecture stronger") working as intended. Selection-value correlation *improved* for Core variants (informed channels choose projects, not just plan ranks) while funding concentration (Gini) fell.

## Certification

Engine v0.4 conforms to Core v0 within its declared simplifications; all implementation defects found (AF1–AF4) were corrected in this change set, and the remaining reduced-form boundaries are documented above rather than hidden.
