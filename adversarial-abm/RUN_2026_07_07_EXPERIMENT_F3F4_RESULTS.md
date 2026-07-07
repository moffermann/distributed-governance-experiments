# F-3 / F-4 Results: the Cascade vs Measured AI Failures; Contraposition — 2026-07-07

Author questions of the same date: (1) can we *demonstrate* that the deterrence cascade jointly covers the AI verification failures? (2) how much does fraud drop as contraposed independent evidence grows, and can we measure it? Engine v0.10 (contraposition + diversion-attempts metric; anchors reproduce exactly). Operating points from F-0 v2 **measured** panels — not stipulated. 20 runs, seed 1, pull W\*=7. Raw: `results/experiment-f/f34-cascade-contraposition-seed1-runs20.md`.

## F-3: yes — the intact cascade covers the measured failures of today's models

| Stack | Verifier (measured operating point) | V | leak | diversion attempts |
|---|---|---:|---:|---:|
| **intact** | pure human (reference) | 0.304 | 0.0056 | 1.2 |
| **intact** | claude single (fp 8.3%, ff 5%) | 0.296 | 0.0047 | 1.1 |
| **intact** | **deepseek single — the worst measured (fp 21.7%)** | 0.307 | **0.0052** | 1.2 |
| **intact** | deepseek+claude pair (measured ρ_eff=0.05) | 0.305 | **0.0020** | 0.6 |
| degraded | pure human | 0.114 | 0.0568 | 11.7 |
| degraded | any measured verifier | 0.117–0.118 | 0.052–0.061 | ~12 |

The demonstration the author asked for, in one line: **a verifier that lets through 22% of subtle fraud produces the same leak as pure-human verification when the deterrence cascade is intact** — because the cascade removes the *attempts* upstream (1.2 per ~100 projects); and no verifier, however good, rescues a broken cascade. The measured two-layer pair even beats pure human on leak (0.0020) by raising anticipated end-to-end detection. This also answers the thesis-discipline question directly: **today's imperfect models suffice at the verification layer, provided the incentive cascade is intact** — model progress is upside, not a prerequisite. (F-0's panel is a pinned-version 2026 snapshot; declared.)

## F-4: contraposed evidence is the strongest single add-on measured in the program

Intact stack (claude L1), coverage = share of milestones carrying independent evidence (catch 0.8, declared):

| coverage | leak | Δleak | diversion attempts |
|---:|---:|---:|---:|
| 0% | 0.0047 | — | 1.1 |
| 50% | 0.0020 | **−57%** | 0.7 |
| 75% | 0.0009 | −81% | 0.3 |
| 100% | 0.0006 | **−87%** | 0.3 |

And the dramatic cell — the **degraded** stack (docs/111 violation):

| coverage | leak | diversion attempts |
|---:|---:|---:|
| 0% | 0.0598 | 12.1 |
| 50% | 0.0165 (**−72%**) | 4.7 |
| 100% | 0.0030 (**−95%**) | 1.1 |

The author's intuition is confirmed and exceeded: independent evidence producers — *even without active dissent, by mere existence* — collapse fraud, because anticipated near-certain contradiction **is deterrence by itself**: attempts drop before anything is detected. Contraposition is the only instrument measured in the whole program that substantially **rescues a broken deterrence stack** (leak −72% at half coverage). It is also the only channel that anchors verification to the world rather than to the executor's evidence — the boundary no model stack could cross.

## The author's four human-intervention scenarios, evaluated

1. **≥1 AI flags (true or false positive) → human.** Agreed — a flag must be resolved by someone (docs/79: machines trigger, never certify). Volume is governed by layer composition: with a calibrated-permissive L1 on evidence-rich bundles (claude-class, ff 5%), flags ≈ **6–9% of projects**; with hair-trigger layers it floods (80%+) — the specificity-first rule is what makes this scenario affordable.
2. **Both AIs low-confidence → human.** Agreed; needs confidence-score instrumentation in the panel protocol (not yet collected — named addition). Estimated band 5–10%, unmeasured.
3. **Random review on relevant projects.** Agreed — this is `s_min` (2–5% suffices per E-1c/E-1d: deterrence lives in the stack, epistemics in the seeded controls) plus the mandatory set (high stakes, thin track records, post-model-change windows, and now: **the flaw classes where models fail together** — compressed timelines).
4. **Complaints with AI disagreement → human.** Agreed; demand-driven (~1–3%), double-gated per the contraposition design.

**Volume estimate with measured numbers: humans touch ~15–25% of projects**, most touches dossier-assisted and light (resolve a named flag), versus 100% of milestones reviewed in depth today — roughly **70–85% less human verification labor**, concentrated where machines disagree, stakes are high, evidence contradicts, or dice say so. The centralization worry is answered by F-4's mechanism: the *watching* stays distributed (citizen evidence producers), while the small professional corps needs the recorded anti-capture design (cross-scope random assignment, rotation, seed/review separation, plural auditors, contestable verdicts).

## Boundaries

- Contraposition modeled with catch=0.8 and coverage as an exogenous share; endogenous citizen-coverage (salience-biased, incentive-driven) is the next refinement, and fabricated counter-evidence is not modeled (mitigations recorded in the master note).
- Scenario-2 volumes require confidence elicitation; named instrument addition.
- F-3's pair cell maps measured joint rates into the engine's common-cause form (fp/layer 0.134, ρ 0.05) — an approximation, declared.
