# Planning Layer Run Results — 2026-07-06

## Execution

First end-to-end run of the planning layer specified in [`PLANNING_LAYER_DESIGN.md`](PLANNING_LAYER_DESIGN.md):

- scenario sweep: 5 scenarios (now including `central_planning`) × 10 seeds × 104 ticks × 1,000 citizens (`run_sweep.py`);
- planning comparison: `planning_attendance_scale` ∈ {0.05 … 2.0} × 6 seeds × both planning modes × {with delegation, attentive-only} (`run_planning_comparison.py`);
- byte-identical between Mesa 3.5.1 and the stdlib fallback, re-verified after the extension.

Validation target: `planning-vector-construction` results (v0.5, 200 runs, seed 42) — Core v0 distributed channels corr(latent) 0.815–0.938 at imposed attentive shares of 2–10%, central representative family 0.315–0.650, salience 0.187.

## The attentive-share answer

The share of citizens contributing an explicit planning signal is now an emergent output:

| Scenario | attentive share (mean over run) | representation incl. delegation |
|---|---:|---:|
| high_friction_launch | 2.5% | 10.6% |
| central_planning | 3.9% | 15.3% |
| baseline | 4.1% | 18.0% |
| delegation_first | 5.0% | 20.0% |
| ai_assisted_onboarding | 5.1% | 22.0% |

The emergent range (2.5–5.1%) falls inside the 2–10% band the planning-vector experiment imposes as `attentivePlanningShare` — its participation assumptions are behaviorally realizable, which is itself a validation result.

## Distributed vs central planning quality

| Metric (baseline, 10 seeds) | distributed | central comparator |
|---|---:|---:|
| corr(vector, latent need) | 0.977 (0.963–0.992) | 0.667 (0.392–0.915) |

The distributed correlation is essentially flat (~0.97) across every scenario, including high friction. In the attendance sweep with delegation active, it stays at 0.98 down to an attentive share of **0.2%**, because delegated representation (~11% of population weight) keeps carrying signal. There is **no correlation crossover at any tested attendance level** — stronger than the pre-registered expectation (P2 predicted a low-attendance crossover).

Removing all delegation exposes the gradient: attentive-only correlation falls 0.94 → 0.72 as attentive share drops 4.4% → 0.2%, with planning-signal coverage collapsing to 35% of targets. Even then it stays above the central comparator's mean — but the **end-to-end value flips**: below ~0.5% attentive share without delegation, central mode delivers *more* value (ratio 0.69–0.74) despite worse correlation. A sharp (salience-driven) central vector concentrates funding and completes projects faster than an almost-flat distributed vector spreads it. Information superiority alone does not guarantee delivery superiority when the signal is too thin to be decisive — a genuinely end-to-end finding invisible to correlation-only comparisons.

## End-to-end value and the feedback loop

Identical behavioral population, only the vector followed by the default layer differs:

| Metric (10 seeds) | baseline (distributed) | central_planning |
|---|---:|---:|
| value_delivered_share | 0.421 | 0.320 |
| mean_platform_trust | 0.672 | 0.588 |
| active_user_share | 34.3% | 30.2% |
| abandonment_share | 11.6% | 14.2% |

Distributed planning delivers ~**1.3× the need-weighted value** of the central regime end-to-end (attendance sweep, with delegation: value ratios 1.13–1.36 across cells, noisy at 6 seeds). The gap then compounds behaviorally: fewer visible successes under central planning depress trust, which depresses activation and raises abandonment — worse planning quality erodes the platform's own user base. This feedback is emergent, not scripted.

## Prediction accounting (pre-registered in PLANNING_LAYER_DESIGN.md)

- **P1 — violated upward, informative.** Emergent distributed correlation (~0.97) lands *above* the sibling experiment's 0.815–0.938 band, not at-or-below. The behavioral model's aggregation is idealized (equal-weight averaging of honest signals) and its bias family milder than the sibling's full distortion stack; the honest-elicitation boundary (docs/87, docs/91) is doing real work. The number should be read as an upper bound conditional on honest signals.
- **P2 — refuted in the robust direction.** No correlation crossover exists at any tested attendance with delegation active (down to 0.2% attentive); the only regime where central wins end-to-end is attentive-only participation below ~0.5% — and it wins on delivery speed, not information.
- **P3 — held, with the thin-signal exception above.** Value ordering follows correlation ordering wherever the distributed signal has any thickness; the gap is compressed (1.3× in value vs ~0.31 in correlation gap) because active routing and salience herding are identical across regimes.
- **P4 — held.** `delegate_planning_coverage` emerges at 0.56–0.65, inside the sibling's prior band (0.35–0.70) — with institutional delegates pushing the high end (`delegation_first` 0.65).
- **P5 — held.** The institutional-stress scenario degrades distributed correlation only mildly (0.9716 vs 0.9770 baseline; the sibling sees 0.861 vs 0.842 in the same direction) while concentrating representation (top delegate 16%, HHI 4× baseline).

## Reading these numbers against the sibling experiment

The behavioral model *confirms the ordering and the mechanism* of `planning-vector-construction` — distributed channels out-inform every central regime, delegation is the robustness reserve, concentration degrades mildly — while disagreeing on the absolute level (0.97 vs 0.82–0.94). The disagreement decomposes into: honest signals by construction here; milder bias stack; idealized equal-weight aggregation. The two experiments now bracket the answer: the sibling's imposed distortions give the pessimistic band, the behavioral emergence gives the optimistic bound, and the true elicitation-under-pressure number — the open problem of docs/87/91 — lies between them.

## Caveats

All coefficients remain synthetic. The value ratios at 6 seeds are noisy (1.13–1.36 non-monotonic in attendance); the correlation results are stable. The central comparator is deliberately generous (truthful review of the top 30% of targets by salience); real authorities span the sibling experiment's crisis-to-high-alignment family, most of it below this comparator. Planning-signal honesty is assumed throughout — gaming, clientelist pressure, and elicitation design remain out of scope here and belong to the adversarial ABM.
