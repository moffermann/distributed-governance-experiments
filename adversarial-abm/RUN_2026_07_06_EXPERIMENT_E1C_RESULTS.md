# Experiment E-1c Results: Verification Throughput — 2026-07-06

Pre-registered in [`EXPERIMENT_E1C_VERIFICATION_DESIGN.md`](EXPERIMENT_E1C_VERIFICATION_DESIGN.md); raw tables in `results/experiment-e/e1c-*`. Engine v0.7 (AI triage lanes, verification windows, demand smoothing — all zero-RNG when disabled; v0.6 regression anchor reproduced exactly: V = 0.303844218531). Release policy fixed at E-1a's winner (pull, W\* = 7 months). 20 runs, seed 1.

## Headline 1: AI triage is capacity insurance — and it lifts the ceiling no release policy could

At **scarce verification capacity** (K=4), where E-1a showed every release policy capped at V ≤ 0.255, AI triage at high protocolizability **fully restores and exceeds the calibrated-capacity ceiling: V = 0.316 (+24%)**, with the verification queue at zero and human load at 1.2 verifications/cycle (surplus capacity even at K=4). At **calibrated capacity** (K=6) the gain is modest (0.304 → 0.316 at π=0.9) and statistically thin below π=0.7 — the machinery wasn't starving, so triage mostly converts human verifications into surplus. **The AI fiscalizer's institutional value is insurance against the binding constraint, not decoration on a healthy pipeline.**

## Headline 2 (the unpredicted one): the deterrence stack's redundancy is what makes an imperfect AI verifier safe

The pre-registered crossover — an `aiFalsePass*` above which the leak outweighs the throughput gain — **did not appear anywhere in the tested range**: at π ≥ 0.7, even a 20%-false-pass AI dominates or matches pure-human verification (leak stays ≤ 0.005), and the dominance frontier reads `falsePass* ≥ 0.20` at every (π, s) at scarce K. The mechanism is the deterrence coupling itself: with the dossier boost on referred cases, the end-to-end effective detection at fp=0.20, s=0.05 still lands ≈ 1.04× the baseline detection — and the inequality's slack (the ablation's K10 finding, resolved as docs/111) absorbs the rest, so opportunists don't start diverting. **The complements-not-substitutes property pays an unexpected dividend: a redundant deterrence stack buys tolerance for verification-instrument error.** Declared boundary: this lax accuracy requirement is *conditional on an intact stack* — an AI lane on a degraded stack is exactly the coupling E-1b must attack (evidence gaming + partial stacks).

## Headline 3: fiscalizer unresponsiveness is a first-order threat, and the author's window instrument works — if the timeout is short

| pStall | no window | T=1 | T=2 | T=3 |
|---:|---:|---:|---:|---:|
| 10% unresponsive | 0.254 (−16%) | **0.291** | 0.279 | 0.272 |
| 25% unresponsive | 0.188 (−38%) | **0.283** | 0.245 | 0.213 |

A quarter of assignments landing on unresponsive fiscalizers costs **38% of delivered value** with no window; a **one-cycle timeout with automatic reassignment recovers ~80% of the damage**. Longer timeouts bleed value roughly linearly — the design lesson is *reassign fast*; the reputational record (not the wait) is what disciplines the straggler. As predicted, windows never exceed the no-stall baseline: they fix the tail, never the ceiling.

## Prediction accounting

- **PC1 — confirmed, strongest form.** AI triage with sampling lifts the scarce-K ceiling (0.254 → 0.316) — the thing no release policy could do; at calibrated K gains are modest and concentrate at high protocolizability.
- **PC2 — refuted in range, and the refutation is the finding.** No dominance crossover up to fp = 0.20 (grid maximum); at π=0.4/K=6 the AI cells sit ~1 SE below baseline (noise-level, honestly reported), everywhere else AI ≥ human. Cause: deterrence-slack absorption (Headline 2), conditional on an intact stack — the degraded-stack coupling goes to E-1b.
- **PC3 — refuted in range, informative.** The sampling rate barely moves V or the frontier at these fp levels: the value-protection knob turned out to be the deterrence stack itself. Lane c's role is *epistemic* — it is how a deployment measures its AI's real error rate (the docs/111-style published number) — not the leak plug at these accuracies.
- **PC4 — confirmed with magnitudes.** Windows recover stall damage (up to 0.095 V at pStall=0.25) and never raise the no-stall ceiling.
- **PC5 — refuted with a declared implementation caveat.** Smoothing as implemented (monotone-clamped jitter) biases milestones *later*, lengthening WIP time: V = 0.293 alone, and it drags the best-AI cell from 0.316 to 0.298. A delay-neutral scheduler is the fix candidate; as shipped, smoothing is net harmful and the instrument is demoted pending reimplementation.
- **Dossier-boost robustness:** best-AI results at boost 1.0 / 1.25 / 1.5 differ by ≤ 0.002 — the AI gains do not depend on the dossier assumption.

## Package reading for the master pipeline (pending E-1b)

The evidence so far ranks the package: **(2) AI triage** = the ceiling instrument, accuracy requirement lax under an intact deterrence stack, demarcated by protocolizability (docs/110's rule applied to verification); **(1) verification windows** = the tail instrument, validated with *short* timeout + reassignment + reputational record; **(6/3)** self-verifying evidence and published capacity raise π and make the coupling visible (not separately simulated — π is their proxy); **(4) smoothing** demoted pending a delay-neutral implementation; **(5) pricing/pools** not yet simulated. E-1b (adaptive adversaries: evidence gaming against the AI lane, congestion timing, degraded-stack coupling) completes the bundle before anything travels to the corpus.

## Declared boundaries

- AI accuracy is a swept requirement, not a model claim; deployments must demonstrate it against lane-c measurements.
- falseFlag fixed at 0.10 (unswept); dossierBoost swept and immaterial.
- The lax fp\* is conditional on the audited deterrence stack (docs/111 margin positive); E-1b tests the joint degradation.
- Smoothing verdict reflects this implementation, not the concept.
