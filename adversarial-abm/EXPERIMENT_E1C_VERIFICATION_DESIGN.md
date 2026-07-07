# Experiment E-1c — Verification Throughput: AI Triage and Verification Windows (pre-registered design)

Registered 2026-07-06, before any implementation or run. Companion to [`EXPERIMENT_E_LONGITUDINAL_DESIGN.md`](EXPERIMENT_E_LONGITUDINAL_DESIGN.md) (E-1a executed; E-1b adaptive adversaries queued after this phase, per the author). Evaluates the verification-throughput package recorded in the master corpus (`knowledge/open-questions/verification-throughput-design.md`), on the longitudinal engine v0.6.

## Questions

1. **At what AI accuracy does triage verification dominate pure-human verification?** The dominance threshold answers the author's "total or partial" question mechanically: partial by design, with the frontier where measured accuracy permits (the docs/110 demarcation applied to verification).
2. What do verification windows (timeout → reassignment) add, and is the queueing prediction right that they fix the tail but not the ceiling?
3. Do the instruments interact (AI triage + demand smoothing vs the sum of parts)?

## Model extensions (engine v0.6 → v0.7)

1. **AI triage lanes on milestone verification.** Parameters: protocolizable share `pi` (fraction of milestones whose evidence class is machine-checkable), `aiFalsePass` (probability the AI clears a diverted milestone), `aiFalseFlag` (probability it flags an honest one). Lane a: protocolizable + AI-cleared → instant tranche release (no human slot consumed). Lane b: flagged or non-protocolizable → human queue; the AI dossier raises human effectiveness (detection ×`dossierBoost`, default 1.25, declared assumption). Lane c: share `s` of AI-cleared milestones sampled into the human queue for re-verification.
2. **Anticipating opportunists (the deterrence coupling — the honest part).** Sophisticated opportunists face the *effective* end-to-end detection under triage, which enters the deterrence inequality exactly as fiscalizer collusion did in v0.5: `effDetection = pi · (aiCatch + aiFalsePass · s · detection) + (1 − pi) · detection`, with `aiCatch = (1 − aiFalsePass) · detection-equivalent` — i.e., a leaky AI lane is not only a leak channel, it *weakens deterrence upstream*, and the experiment must price both.
3. **Verification windows.** Heterogeneous service: with probability `pStall` a queued verification is assigned to an unresponsive fiscalizer and blocks its slot for `stallCycles` (default 6) unless a timeout `T_o` reassigns it (reassignment consumes a fresh slot). Sweep windows on/off at `T_o ∈ {1, 2, 3}`.
4. **Demand smoothing.** Milestone due dates staggered across projects (uniform jitter within ±2 cycles at activation), on/off.

## Sweeps (20 runs, seed 1, behavioral-llm-calibrated population, core arm + status quo where meaningful)

- `aiFalsePass ∈ {0.01, 0.03, 0.05, 0.10, 0.20}` × `pi ∈ {0.4, 0.7, 0.9}` × `s ∈ {0.05, 0.15}`, at human capacity K=6 (calibrated) and K=4 (scarce), against the E-1a pure-human baselines (pull W\*=7).
- Windows: `pStall ∈ {0.1, 0.25}` × `T_o ∈ {off, 1, 2, 3}`, pure-human K=6.
- Interaction cell: best AI config + smoothing on/off; smoothing alone.

## Pre-registered predictions

- **PC1.** AI triage with `aiFalsePass ≤ 0.05` and `s ≥ 0.05` dominates pure-human verification at both K levels — at scarce K it lifts the E-1a ceiling (V > 0.255), which no release policy could do.
- **PC2.** A dominance crossover exists: above some `aiFalsePass*` (predicted between 0.10 and 0.20 at `s = 0.05`), the leak-and-deterrence cost outweighs the throughput gain and pure-human verification wins — the measured frontier of "partial by design".
- **PC3.** Raising the sampling rate `s` moves `aiFalsePass*` upward materially (sampling converts AI error into bounded leak and restores deterrence) — the cheap knob is the audit sample, not model perfection.
- **PC4.** Verification windows reduce tail latency and expired-project mortality under stalls but do not raise V's ceiling at saturated K (timeouts fix stragglers, not throughput); their value concentrates where `pStall` is high.
- **PC5.** Demand smoothing alone yields a small but free V gain at K=6 (queue peaks flattened) and near zero at K=9; combined with AI triage the effects are approximately additive, not synergistic.

## Deliverables

Results tables + the `aiFalsePass*` frontier per (`pi`, `s`, K); prediction accounting; the verification-package evidence bundle for the master pipeline (joint with E-1a's release rule and, after E-1b, the adaptive-adversary results), at the author's verdict.

## Declared boundaries

- AI accuracy is a swept parameter, not a claim about any real model; the frontier is stated as an accuracy *requirement*, which a deployment must demonstrate against lane-c measurements.
- Adversarial evidence against the AI (staged imagery, sensor spoofing) is represented only through `aiFalsePass`; modeling adaptive evidence-gaming belongs to E-1b's adversary harness.
- `dossierBoost` is a declared assumption (sensitivity-swept at {1.0, 1.25, 1.5}).
