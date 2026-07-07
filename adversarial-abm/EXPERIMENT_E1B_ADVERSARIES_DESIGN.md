# Experiment E-1b — Adaptive Adversaries (pre-registered design addendum)

Registered 2026-07-06, before any implementation or run. Completes the Experiment E program ([`EXPERIMENT_E_LONGITUDINAL_DESIGN.md`](EXPERIMENT_E_LONGITUDINAL_DESIGN.md), phase E-1b; original predictions P5–P6) plus the cells E-1c queued (evidence gaming against the AI lane; the degraded-stack × AI coupling behind E-1c's conditional finding).

## Model extensions (engine v0.7 → v0.8; all zero-RNG when disabled, v0.7 anchor must reproduce exactly)

1. **Verification staleness** (`staleness: {rate, floor}`): detection at verification degrades with the item's queue age — `d_eff = d · max(floor, 1 − rate·age)`. Evidence goes cold in a backlog. This is the sensitivity flagged in the E-1a design (default remained "delayed, not degraded"); E-1b turns it on because it is what makes congestion an attack surface at all.
2. **Timing-aware opportunists** (`timingAware: true`): at activation, the opportunist observes the current verification backlog and anticipates the stale detection — the deterrence inequality uses `d · max(floor, 1 − rate·(queue/K))`. Congestion now *invites* diversion.
3. **Evidence gaming against the AI lane** (`evidenceGaming: {skill}`): a diverting executor invests in fooling the machine verifier — effective AI false-pass on diverted milestones becomes `min(0.95, falsePass + skill)`; anticipated in the deterrence coupling.
4. **Architecture overrides** (`archOverride`): the longitudinal runner accepts per-run architecture field overrides, enabling the degraded-stack (docs/111 K10) cells.
5. **Reputation-compounding switch** (`reputationCompounding: false`): stake scale fixed at 1 and executor selection made reputation-blind — isolating P5.
6. **Per-year verified-value series**: V accrual recorded by year for the P5 trajectory comparison (horizon 8 years in Part C).

## Cells (20 runs, seed 1, core arm, pull W\*=7 unless noted)

- **Part A — congestion as attack surface (P6/PB1-PB2):** staleness {rate 0.06, floor 0.4} × policies {pull W=7, day-zero} × opportunists {timing-blind, timing-aware}, plus no-staleness baselines.
- **Part B — gaming × stack integrity (PB3):** {intact, degraded stack (K10 values: detection 0.15, retention 0.05, guarantee 0.02, memory terms 0.02, review confidence 0.35)} × {pure human, AI (π=0.7, fp=0.05, s=0.05), AI + gaming 0.35, AI + gaming 0.55}.
- **Part C — reputation compounding (P5/PB4):** horizon 8 years, compounding {on, off}, per-year V and leak trajectories.

## Pre-registered predictions

- **PB1 (P6 sharpened).** Timing-aware adversaries do more damage under congestion-generating release: ΔV(aware − blind) under day-zero exceeds the same difference under pull by a factor ≥ 2 — the release policy is a *security* parameter, and frozen capital is an attack surface, not only an efficiency cost.
- **PB2.** Staleness alone (blind adversaries) costs modestly under pull and more under day-zero (its queue is longer).
- **PB3.** The intact stack bounds evidence gaming: with docs/111-compliant terms, even gaming skill 0.55 keeps leak within ~2× baseline and V above the pure-human degraded cell. On the **degraded stack**, AI + gaming collapses — leak explodes and V falls below degraded-pure-human: E-1c's conditional ("lax accuracy requires an intact stack") made quantitative. Joint reading: the docs/111 margin is a *precondition of the AI lane*, not only of the semi-open envelope.
- **PB4 (P5).** With reputation compounding, the core arm's yearly leak declines and V rises over the 8-year horizon (the R term compounds); with compounding off, both stay flat. The architecture's advantage grows with time.
- **PB5.** Even the worst adaptive cell on an intact stack stays above the status quo's E-1a level (V > 0.113): adaptivity erodes, never inverts, the ranking — provided the stack holds.

## Declared boundaries

- Staleness parameters are stipulated (rate 0.06/cycle, floor 0.4), not calibrated; the claim tested is directional (congestion → attack surface), not magnitude.
- Adversary adaptivity is structural (timing awareness, gaming skill), not open-ended strategy search — as declared in the E design.
- Degraded-stack cells model the docs/111 violation, not any proposed configuration.
