# Experiment G — Collusive, Multi-Period, Adaptive Adversary (pre-registered design)

Registered 2026-07-07, before implementation. Origin: review-round-2 red-team meta-finding — every verification-security result (E-1b, E-1c, E-1d, F-3, F-4) rests on a **single-shot** diversion draw against the *published* detection probability, so they measure robustness against a *designed* adversary, not a real one. Experiment G attacks that assumption directly. This is the "second author for the adversary" the round named as the missing independence.

## The single-shot assumption, stated

In engines v0.5–v0.10 the diversion decision is a one-time Becker draw at activation: divert iff expected gain > p·(stake), with p the *true, published* end-to-end detection probability, and the layers priced as **independent** draws whose protections *multiply*. Three things a real adversary does that this cannot represent: (1) **adapt** — probe the boundary, learn where detection is thin, target the shared blind spot; (2) **collude** — correlate across executor, verifier, and citizen-evidence layers so protection is the *minimum*, not the product; (3) **game the exogenous inputs** — the market-price reference and evidence-producer independence the model treats as ground truth.

## Engine extensions (v0.11)

1. **Multi-period adaptive adversary** (`adversary.adaptive`): opportunists observe realized detection outcomes and update a belief about per-blind-spot detection; diversion targets the lowest-believed-detection fraud class (the F-0-measured compressed-timeline blind spot as the seed prior). Probing has a cost.
2. **Cross-layer collusion** (`adversary.collusion = {rate, layers}`): with probability `rate` an executor is part of a ring that also controls a fraction of its assigned verifiers and/or citizen-evidence contributors. For a colluded milestone, verifier clearance and contradiction-generation are no longer independent draws — they are set by the ring (cleared; no contradiction), so cross-layer correlation → 1.
3. **Poisonable market reference** (`adversary.anchorPoison = {share, drift}`): the in-bundle price reference is a moving average of recent platform disbursements; a cartel controlling `share` of them drifts the anchor up by `drift`, so inflated invoices compare "fine" (the F-0 inflated-price detector, ~0% false-pass, degrades as the anchor rises).
4. **Long con** (`adversary.longCon = {buildYears, window}`): a patient ring accrues clean reputation for `buildYears`, then defects en masse in the published post-model-change `window`, concentrating diversions to swamp the human corps' finite capacity in one period.
5. **Capacity-aware human corps** (`humanCorps = {size}`): the second-instance/mandatory-set human reviews draw from a finite per-cycle budget; a coordinated defection spike exhausts it, and un-reviewed high-risk milestones fall through.

All OFF by default; the v0.6–v0.10 anchor (0.303844218531) must reproduce exactly.

## Pre-registered predictions

- **PG1.** Adaptive targeting alone (no collusion) raises leakage above the F-1 fixed-severity result but stays bounded by the intact stack — the adversary concentrates on the blind spot, but the deterrence inequality still binds per-milestone. Modest effect.
- **PG2.** Cross-layer collusion is the dominant term: at collusion rate ≥ 0.2 the "protection multiplies" assumption breaks and leakage rises **super-linearly**, exceeding every single-instrument attack measured in E-1b/F. The measured verifier–verifier correlation (φ up to 0.43) is a floor; executor–verifier–contributor correlation under collusion is the real driver.
- **PG3.** Contraposition (F-4's rescue) **collapses under collusion**: an astroturfed/silenced contributor layer produces no contradiction, so the router summons no human; the −72%/−95% broken-stack rescue becomes an *upper bound* that a colluding attacker erases. Contraposition rescues a broken stack only against a *non-colluding* adversary.
- **PG4.** Anchor poisoning degrades the price-fraud detector materially: at cartel share ≥ 0.3 the inflated-price class's catch rate falls from ~100% toward the compressed-timeline blind-spot level — poisoning one exogenous input poisons every downstream judgment, human and machine.
- **PG5.** The long con defeats the reputation-compounding null: concentrated defection in the post-model-change window, sized to the human-corps capacity, produces a leakage spike an order of magnitude above the stationary result, invisible in year-averaged metrics.
- **PG6 (the headline test).** Under the full collusive-adaptive adversary with an *intact* deterrence stack, does the architecture still beat the status quo? Prediction: the advantage **shrinks but survives** for collusion rates below a threshold, and **inverts** above it — locating the collusion rate at which distributed verification stops being safer than centralized audit. That threshold is the deliverable.

## What this does and does not do

- It measures the architecture's robustness against a *modeled* collusive adversary — still a model, now a much less charitable one. It does not claim to bound a real adversary; open-ended strategy discovery remains out of scope (declared).
- Collusion rate, anchor-poison share, and long-con window are swept, not calibrated; the deliverables are thresholds and orderings, not fitted constants.
- Corpus consequence (via the master pipeline, author verdict): if PG2/PG3 hold, the verification package's headline claims (F-3 "today's models suffice," F-4 "rescues a broken stack") must be qualified with "against a non-colluding adversary," and cross-layer-collusion resistance (identity/beneficial-ownership verification, contributor Sybil-resistance, assigner/seeder decentralization) becomes a first-class design requirement, not a residual caution.
