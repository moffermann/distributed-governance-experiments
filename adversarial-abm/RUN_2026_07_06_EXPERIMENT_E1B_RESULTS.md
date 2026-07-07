# Experiment E-1b Results: Adaptive Adversaries — 2026-07-06

Pre-registered in [`EXPERIMENT_E1B_ADVERSARIES_DESIGN.md`](EXPERIMENT_E1B_ADVERSARIES_DESIGN.md); raw tables in `results/experiment-e/e1b-*`. Engine v0.8 (staleness, timing-aware opportunists, evidence gaming, architecture overrides, compounding switch, per-year series — all zero-RNG when disabled; the v0.6/v0.7 anchor reproduces exactly: V = 0.303844218531). 20 runs, seed 1, core arm.

## The umbrella finding of the E program

**Adversary adaptation neither erodes nor inverts the architecture while the docs/111 margin holds — and when the stack is broken, no verifier (human or machine) matters.** Every adaptive channel this phase threw at the intact configuration — congestion-timed diversion under stale evidence, evidence gaming against the AI lane up to skill 0.55, eight years of adversary-facing dynamics — moved verified value by at most noise and leakage by at most fractions of a point. The reason is the same one the ablation found (docs/111) and E-1c rediscovered: the audited deterrence stack holds the inequality with slack, and adaptive adversaries operate *at the margin* of an inequality that is nowhere near its margin.

## Part A — congestion as an attack surface: real, tiny, and removed by the pull rule

At calibrated capacity (K=6), staleness and timing awareness change **nothing to three decimals**: the pull rule keeps the backlog at ~0.2 cycles, so evidence never goes cold — the surface does not engage. At scarce capacity (K=4, follow-up cells), where day-zero release drives the queue to 30 pending verifications and detection sits at the staleness floor (40% of nominal), the timing-aware adversary gains **+15% leakage under day-zero vs +6% under pull, with V flat everywhere** — the slack absorbs even floor-level detection.

- **PB1 — refuted in magnitude, confirmed in direction and in its institutional form.** The release policy *is* a security parameter, but not because pull "suffers less": **pull removes the attack surface outright** (backlog too short for evidence to stale), while push policies at scarce capacity create it — and even then the intact stack bounds the damage to leakage fractions.
- **PB2 — confirmed only under joint failure.** Staleness costs day-zero at scarce K (V 0.226 vs pull's 0.255) and costs nothing at calibrated K.

## Part B — evidence gaming × stack integrity: verification is downstream of deterrence

| Stack | Pure human | AI fp=0.05 | AI + gaming 0.35 | AI + gaming 0.55 |
|---|---:|---:|---:|---:|
| Intact | 0.304 / leak 0.006 | 0.306 / 0.004 | 0.306 / 0.005 | 0.302 / 0.010 |
| Degraded (docs/111 violation) | 0.114 / 0.057 | 0.118 / 0.052 | 0.115 / 0.063 | 0.115 / 0.060 |

- **PB3, first half — confirmed.** The intact stack bounds evidence gaming: skill 0.55 lifts leak from 0.006 to 0.010 (~1.7×) with V statistically flat. A gamer who can fool the AI more than half the time still gains almost nothing, because the stack deters the diversion decision upstream of any verification.
- **PB3, second half — refuted, and the revision is cleaner than the prediction.** Degraded + gamed AI does **not** collapse below degraded-pure-human — it is a wash (0.115 vs 0.114): on a broken stack, human detection (0.15 base, 0.35 review confidence) is already near-blind, so the AI's false passes replace verifications that would have missed anyway. Revised lesson, sharper than the original conditional: **verification instruments — human or machine — are downstream of the deterrence stack; nothing at the verification layer compensates a broken incentive floor.** The docs/111 margin is the precondition of the *entire* verification layer, not merely of the AI lane.
- Cross-engine validation: the degraded-stack cell (0.114, leak 0.057) reproduces the static ablation's K10 (0.110, leak 0.053) in a structurally different engine — an internal dock the satellite paper should report.

## Part C — reputation compounding (P5): null in range

Over eight years, the per-year V series with compounding on (0.285 → 0.320) and off (0.285 → 0.301) differ within noise, and yearly leak shows no declining trend either way. **P5 is null-in-range**: at realistic project throughput (~4 projects per executor per 8 years) reputation accumulates too slowly to move a deterrence inequality that is not at its margin, and reputation-weighted selection tilts assignment only modestly. The honest answer to the program's original question — does the advantage grow with time or erode under adaptation? — is **neither: it is flat and robust from the first cycle**, because the stack deters from the start. (Consistent with, not contradicting, the E7 finding that *removing* memory from the status quo's margin-dwelling configuration matters — the calibrated architecture simply does not dwell at the margin.)

- **PB4 — refuted (null).** Declared honestly rather than rescued.
- **PB5 — confirmed.** Worst adaptive intact cell: 0.302 — still 2.7× the status quo's E-1a level.

## Program closure (E-1a + E-1c + E-1b)

The Experiment E program closes with a three-line institutional summary:

1. **Size the capacity** (E-1a): verification capacity is the pipeline's ceiling; no release policy compensates for its absence.
2. **Meter the release** (E-1a): pull against a WIP ceiling calibrated to throughput × cycle time; calendar-based release freezes capital, and at scarce capacity creates the only congestion attack surface this program found.
3. **Protect the margin** (ablation → docs/111, confirmed twice here): the deterrence stack's slack is what makes the whole edifice insensitive — to verifier error (E-1c), to evidence gaming, to congestion timing, and to time itself (E-1b). Everything else is optimization.

The evidence bundle for the master pipeline is complete: the budget-release rule (E-1a), the verification-throughput package with its measured behavior (E-1c), and the adversarial robustness boundaries (E-1b). Pending: author verdict on how much travels to the corpus and in what form.

## Declared boundaries

- Staleness parameters stipulated, directional claim only; adversary adaptivity structural, not open-ended search (as pre-registered).
- P5's null is at this engine's project granularity; economies with much higher per-executor project throughput could compound faster (declared, untested).
- Degraded-stack cells model the docs/111 violation, not a proposed configuration.
