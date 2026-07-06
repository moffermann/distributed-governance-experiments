# Ablation and Sensitivity Results — 2026-07-06

Pre-registered in [`ABLATION_AND_SENSITIVITY_DESIGN.md`](ABLATION_AND_SENSITIVITY_DESIGN.md); raw tables in `results/ablation/`. Engine v0.5 (attacks implemented; disabled-attack paths verified byte-identical to the committed baselines), population `behavioral-llm-calibrated`, 20 runs, seed 1. Intact reference: V = 0.277, leak = 0.010, sel(θ) = 0.616, advantage 2.19× over the status quo.

## The headline vulnerability finding

**Core v0's deterrence stack is individually redundant and jointly indispensable.** Removing any single deterrence term costs almost nothing — detection to status-quo intensity (K2): ΔV −0.003; financial terms to status-quo levels (K3): −0.002; reputational memory off (K4): −0.001 — because the intact architecture holds the deterrence inequality with large slack. Removing the **whole stack at once** (K10) collapses verified value by 60% (0.277 → 0.110) and drops the architecture **below the status quo (0.87×)** while its selection quality stays perfect (sel 0.616): distributed selection cannot compensate for unverifiable delivery. There is no single point of failure, and there is also no partial-deployment shortcut: an implementation that ships half the stack believing the terms are substitutes at full strength is shipping the collapse case.

## Prediction accounting

- **P1 — refuted, informative.** The largest *single* knock-out is not the default layer but the planning vector (K6, central default: ΔV −0.062). The default-layer knock-out (K5) comes second (−0.042) and does **not** collapse Core to participatory levels: selection quality craters (0.616 → 0.174) but funding caps and verified delivery hold the floor. Refinement of the corpus claim: the default layer's value is *selection*; the delivery machinery is an independent floor.
- **P2 — refuted, informative.** Memory-off does not out-cost detection-off; both are ≈ 0 alone. The corpus's "audit without memory deters nobody" (E7) is a claim about the *status quo's margin* (detection as the only instrument); in the architecture's interior the stack is over-provisioned and any single term is dispensable. This strengthens, not weakens, the design case — and relocates the risk to partial deployments (see headline).
- **P3 — confirmed and completed.** Neither financial terms nor memory alone reproduces the zero-control leak; the pre-announced follow-up cell (K10) shows the joint removal does: leak ×5, verified value −60%.
- **P4 — confirmed.** The planning-source ablation costs −0.062, close to (slightly above) the committed core-central gap.
- **P5 — confirmed in ranking.** `agendaCapture` is the only attack that bites (ΔV −0.033 at severity 0.3, −0.035 at 0.5; selection 0.616 → 0.405). `fiscalizerCollusion` is **neutralized by the deterrence stack**: even with effective detection halved, the inequality still binds, so opportunists don't divert — Proposition 4's redundancy made visible; the status quo, whose deterrence is marginal, suffers more, so the *ratio* actually rises. `coordinatedSignalBias` is minor at allocation stage (≤ −0.007 at 50% of attentives) — with the declared boundary that this engine's distributed vector is exogenous, so signal bias cannot corrupt vector *construction*; that channel is covered by E7b and the behavioral planning layer.
- **P6 — mixed.** "Above 1.5× at every single-parameter sweep point" — confirmed, minimum 1.63× (signal mix 0.2). "Approaches 1.0× under high-severity agenda capture" — refuted: even 50% capture keeps 1.91×, because caps and verified delivery keep captured-but-funded projects delivering. Where sub-1.0× actually lives is K10: total deterrence removal.

## Sweep findings (no cliffs)

- `detectionBase` 0.15–0.75: flat (deterrence slack absorbs it).
- `opportunisticShare` 0.1–0.7: Core's V flat; the **advantage rises to 2.39× at 70% opportunists** — the dirtier the executor pool, the bigger the architecture's edge, because the status quo degrades and Core doesn't.
- `distributedPlanningSignalMix` 0.2–0.8: the one real driver — 1.63× to 2.35×. Everything keeps pointing at planning-vector informational quality (E2/E4/docs/87) as the binding lever.
- `delegationBlockSize`, `socialProofWeight`: flat.

## Vulnerability ranking and corpus feedback

1. **Joint deterrence removal (critical, by construction not by surprise).** The corpus's formal note already treats the terms as one inequality; the finding adds a *deployment warning*: partial stacks are not proportionally weaker — they can be worse than the status quo. Candidate for the master pipeline as a deployment-configuration note, not an architecture change.
2. **Default-vector quality / agenda capture (the standing open problem).** K6, the signal-mix sweep, and the only effective attack all point at docs/87. The corpus already owns this limitation; these results quantify its price in this engine (up to −0.062 V and −35% selection quality).
3. **Non-vulnerabilities (worth stating):** fiscalizer collusion at plausible rates, coordinated allocation bias, delegation blockiness, herding weight, and executor-pool composition — none moves the advantage below 1.6×, and several move it up.

No finding requires a Core v0 change; two candidate notes (deployment warning on partial deterrence stacks; the quantified agenda-capture price) are queued for the master repository's attack → defense → resolution pipeline at the author's discretion.
