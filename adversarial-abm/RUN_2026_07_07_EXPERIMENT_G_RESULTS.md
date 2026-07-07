# Experiment G Results: the Collusive, Multi-Period, Adaptive Adversary — 2026-07-07

Pre-registered in [`EXPERIMENT_G_COLLUSIVE_ADVERSARY_DESIGN.md`](EXPERIMENT_G_COLLUSIVE_ADVERSARY_DESIGN.md); origin: review-round-2 red-team meta-finding that every verification-security result rests on a single-shot diversion draw. Engine v0.11 (collusion, adaptive targeting, anchor poisoning; the v0.6–v0.10 anchor reproduces to 12 decimals). 20 runs, seed 1, core arm + AI triage + 50% contraposition. Raw: `results/experiment-g/`.

## Headline: collusion is the first attack that moves leakage by an order of magnitude — and the verified-value advantage still survives

| collusion rate | V | leak | diversion attempts | V vs status quo |
|---:|---:|---:|---:|---:|
| 0% | 0.304 | 0.0021 | 0.6 | 2.72× |
| 5% | 0.296 | 0.0081 | 1.8 | 2.65× |
| 10% | 0.298 | 0.0090 | 2.1 | 2.67× |
| 20% | 0.295 | 0.0244 | 4.8 | 2.64× |
| 35% | 0.286 | 0.0467 | 9.2 | 2.56× |
| 50% | 0.286 | 0.0522 | 9.9 | 2.56× |

Two facts sit in tension and both are the finding:

1. **Leakage rises ~25× (0.0021 → 0.052)** as collusion goes 0→50% — the first attack in the entire program to move leakage by an order of magnitude. Everything in E-1b (timing, gaming, drift) moved leak by <2×, because those attacks fight the deterrence inequality per-milestone; collusion *bypasses* it — the ring diverts, its verifiers clear, its contributors stay silent, so cross-layer protection is the **minimum, not the product**. **PG2 confirmed:** cross-layer collusion is the dominant leakage term, qualitatively unlike single-instrument attacks.
2. **The verified-value advantage over the status quo survives the whole range** (2.72× → 2.56×), so **PG6's crossover is not reached by collusion rate alone in [0, 0.5]** on the V metric. The honest majority carries verified delivery; collusion steals money without collapsing the value the architecture delivers per budget. The security story lives in the *leak* column, not the *V ratio* — a distinction the earlier verification findings, which reported V, obscured.

## PG3 — collusion erases the contraposition rescue

| stack | contraposition | collusion | leak |
|---|---|---:|---:|
| degraded | 0% | 0% | 0.0525 |
| degraded | 50% | 0% | **0.0169** (the F-4 rescue: −68%) |
| degraded | 50% | 20% | 0.0333 (rescue roughly halved) |
| degraded | 100% | 20% | 0.0283 (vs 0.0030 without collusion — an order of magnitude worse) |

**PG3 confirmed.** F-4's "contraposition rescues a broken stack" holds against a *non-colluding* adversary; under collusion the colluded milestones produce no contradiction, so the router summons no human and the rescue is roughly halved at 20% collusion (and full coverage under collusion never approaches the no-collusion rescue). Contraposition's power is exactly as strong as the *independence* of the contributor layer — which a colluding ring captures.

## PG1 / PG4 — adaptive targeting and anchor poisoning: real but bounded

Adaptive blind-spot targeting (leak 0.004→0.008 across gain 0.1–0.4) and anchor poisoning (0.0055→0.0153 across 25–75% detection loss) both raise leakage modestly on the intact stack — **PG1 confirmed (modest), PG4 confirmed (real, bounded)** — because both still route through a per-milestone deterrence inequality that binds. They are dangerous mainly as *inputs to collusion* (a poisoned anchor plus a captured verifier is worse than either alone), which the full-ring cell already subsumes.

## What this does to the program's verification claims

The single-shot results are not wrong — they are **scoped to a non-colluding adversary**, and Experiment G measures exactly how much that scope was doing:

- "Today's imperfect models suffice at the verification layer" (F-3) → **holds against a non-colluding adversary**; under collusion the verifier is irrelevant (the ring clears its own), and leakage is set by the collusion rate, not the model.
- "Contraposition rescues a broken stack" (F-4) → **holds against a non-colluding adversary**; collusion halves it.
- The deterrence cascade removing *attempts* upstream (E-1b/F-3) → **holds per-milestone**; collusion is not a per-milestone bet, so it is the one thing the cascade does not deter.

**Design consequence (candidate for the master pipeline, author verdict):** cross-layer collusion resistance is a first-class requirement, not a residual caution — verified beneficial-ownership / identity so a ring cannot cycle shells; contributor-layer Sybil-resistance and opposed-interest attestation so contraposition coverage cannot be astroturfed or silenced; and decentralization of the assigner/seeder/floor-setter (the root the round flagged) so a ring cannot route its own fraud to its own captured reviewer. The published-margin (docs/111) and the human floor should be sized against a *collusion* threat model, not only a rational-single-actor one.

## Boundaries

- Collusion is modeled as a ring that deterministically controls its milestone's verifier and contributor outcomes; the *formation* of rings (recruitment, detection of the ring itself via network analysis) is not modeled — an intentionally pessimistic upper bound on a ring's per-milestone power, a lower bound on the system's ability to detect the ring.
- Rates are swept, not calibrated; the deliverable is the ordering and the ~25× leak sensitivity, not a fitted collusion prevalence.
- The long-con window attack (PG5) is represented only through its steady-state collusion analog here; the concentrated-defection timing cell is named as the next refinement.
- Still a single-author adversary model — less charitable than the single-shot one, but not a real adversary. The genuine independence remains external red-teaming.
