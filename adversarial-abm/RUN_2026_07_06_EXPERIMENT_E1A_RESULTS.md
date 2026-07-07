# Experiment E-1a Results: Budget-Release Policies and the Freezing Problem — 2026-07-06

Pre-registered in [`EXPERIMENT_E_LONGITUDINAL_DESIGN.md`](EXPERIMENT_E_LONGITUDINAL_DESIGN.md); raw tables in `results/experiment-e/`. Longitudinal engine v0.6 (`src/longitudinal.mjs`): dynamic project arrivals, docs/104 expiry valve, multi-cycle execution with milestone escrow, verification capacity, executor pool with compounding reputation. 4 years × 12 cycles, 2,000 citizens (annual budget 24,000), behavioral-llm-calibrated population, 20 runs, seed 1. Static-engine regression after the shared-primitive exports: byte-identical.

## Headline: the author's feared freeze is real, and it lives in verification, not in fragmentation

The "atoro" exists — but not where naive intuition puts it. **Sub-threshold fragmentation stays small everywhere** (0.3–1.2 months of budget) because the corpus's own docs/104 expiry valve keeps committed capital moving — at the price of converting fragmentation into **project mortality** (uniform release: 23 of ~108 projects die unfunded). The freeze that actually binds is the **work-in-progress freeze**: day-zero release locks 5.2 months of budget in execution escrow with the verification queue saturated (5.6 pending verifications, ≈ one full month of fiscalizer capacity in backlog), and delivers *less* verified value (0.286) than the best policy (0.304).

## Policy results (Core v0 arm; full tables in results/)

| Policy | V/budget-year | Frozen WIP (months) | Verification queue | Expired projects |
|---|---:|---:|---:|---:|
| P0 day-zero | 0.286 | **5.2** | **5.6** | 13.9 |
| P1 uniform (the old hard-coded default) | 0.287 | 4.0 | 0.8 | **23.4** |
| P2 front-loaded (λ=4, best push) | 0.304 | 4.4 | 2.0 | 19.6 |
| **P3 pull, W\*≈7–8 months (best)** | **0.304** | 4.3–4.7 | 1.2–2.9 | 16.9–20.1 |
| P4 approval-conditioned (α=1.2, best) | 0.269 | 4.7 | 3.6 | 22.9 |

The Pareto frontier (max V, min frozen, min latency) is **dominated by the pull family**: pull W=7 sits at V=0.304 with the lowest latency of the top group. The architecture-vs-status-quo ranking holds under every policy (2.4×–2.9×) — release policy moves magnitude, never ordering.

## The optimal release rule (the candidate Core v0 contribution)

**Release budget against a work-in-progress ceiling calibrated to the pipeline's cycle time and its binding capacity — never against the calendar.** The K-sensitivity (`results/experiment-e/e1a-sensitivity-k.md`) pins the mechanism:

- With **scarce verification** (K=4/cycle), the whole pipeline's ceiling drops to V≈0.255 *no release policy can recover it* — and over-release actively destroys value (V falls to 0.236 at W=11 while the queue explodes to 23.5): beyond the ceiling, released budget converts to congestion, not works.
- With **calibrated verification** (K=6), W\* = 7 months of budget, V=0.304.
- With **abundant verification** (K=9), W\* stays ≈7 and V does not improve — the binding constraint hands over from verification capacity to execution duration, exactly Little's Law: healthy WIP ≈ achievable throughput × total cycle time.

Institutional statement (mechanism terms, no fitted constants): the authority should meter release so that committed-but-undelivered budget stays near *throughput × cycle time* of its delivery-and-verification pipeline; when verification capacity binds, more release is not more delivery — it is queue, and eventually less delivery. Verification capacity is the pipeline's ceiling before it is the anti-fraud instrument.

## Prediction accounting

- **P1 — confirmed in substance, with a metric correction.** Day-zero maximizes the *absolute* WIP freeze and verification congestion and does not maximize V. The pre-registered frozen-*ratio* metric (frozen/released-to-date) misleadingly favors day-zero through its denominator; the honest cross-policy metrics are the absolute frozen-months columns, used throughout. Declared, not hidden.
- **P2 — confirmed, refined.** Pull weakly dominates every push policy on the frontier; W\* tracks the *binding resource* — verification capacity when scarce, execution duration when verification is abundant — not the budget size.
- **P3 — transformed.** Fragmentation freeze stays small *because* docs/104's expiry valve works; the valve converts frozen capital into project mortality (expired count), which is a real cost of slow release (uniform: 23 dead projects) but a different one than predicted. The freeze migrated to the WIP stage.
- **P4 — refuted, informative.** Approval-conditioned commitment as implemented (release follows last cycle's activation *flow*) peaks at 0.269 — clearly below pull. The author's instinct is directionally right but the correct conditioning variable is the *stock* of outstanding commitments (WIP), not the recent approval flow: **the pull policy is approval-conditioned commitment done right**. The flow signal is noisy and laggy; conditioning on the stock is what stabilizes the loop.
- **P5, P6 — pending** (E-1b: reputation-compounding isolation and adaptive adversaries, including congestion-timed attacks).
- **P7 — confirmed.** 2.4×–2.95× vs the status quo under every policy.

## Declared boundaries

- Single load level (demand ≈ 1.2× budget) and one TTL (6 cycles); load and TTL sweeps belong to the E-1b annex.
- The frozen-ratio artifact above is recorded as a lesson for the satellite paper's metric section.
- Latency is measured on finished projects only; heavily congested cells understate it (survivor bias — visible in day-zero's 8.5 vs pull's 7.5).
- The per-project veto stage remains unmodeled (docs/110 boundary, unchanged).
