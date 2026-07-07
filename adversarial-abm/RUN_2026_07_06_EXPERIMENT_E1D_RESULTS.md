# Experiment E-1d Results: the Verifier-Displacement Frontier, Evaluated — 2026-07-06

Small pre-committed evaluation of the second-instance design recorded in the master corpus (verification-throughput note): does passive lane-c sampling actually deliver the drift-detection latency the frontier's `s_min` is supposed to buy? Engine v0.8 + `aiDrift` extension (AI false-pass drifts upward from cycle 24 at 0.03/cycle; opportunists not drift-aware, declared); 6-year horizon, pull W\*=7, AI π=0.7 fp=0.05, 20 runs, seed 1. Regression anchor reproduced exactly (V = 0.303844218531).

## Result: passive output auditing cannot measure a verifier embedded in a working deterrence system

| lane-c sample rate s | drift-detection latency (cycles from onset; horizon-censored at 48) | V | leak |
|---:|---:|---:|---:|
| 0.02 | **48.0 ± 0.0 (never detected)** | 0.309 | 0.0039 |
| 0.05 | **48.0 ± 0.0 (never detected)** | 0.309 | 0.0039 |
| 0.15 | 43.5 ± 11.6 (mostly censored) | 0.309 | 0.0037 |
| no drift (s=0.05) | — | 0.311 | 0.0034 |

Two readings, both load-bearing:

1. **The damage is negligible while the stack holds** — a verifier drifting from 5% to ~95% false-pass over thirty cycles costs ~0.002 V and ~0.0005 leak, because the intact deterrence stack keeps the diverted-milestone base rate near zero. Consistent with E-1c/E-1b: verification is downstream of deterrence.
2. **And that is exactly why passive sampling is epistemically blind**: with almost no true positives in the stream, lane-c cannot estimate a false-pass rate at any affordable s. The latency formula ∝ 1/(s × diversion exposure) degenerates when deterrence succeeds — the healthier the system, the less its outcome audit tells you about the verifier. The silent risk is sequencing: a deployment that later degrades its stack (the docs/111 scenario) would meet a long-drifted, unmeasured verifier.

## Design consequence (adopted into the frontier)

The second-instance layer needs **seeded positive controls**: known-violation test cases injected into the AI lane at a rate q (the audit profession's proficiency-testing/mystery-shopper pattern). Each seeded case is a Bernoulli(falsePass) probe of the verifier under ground truth, so drift detection becomes a sequential test whose expected latency scales as 1/(q·π) — *independent of the deterred real-world diversion rate*. A handful of controls per cycle bounds detection latency to a few cycles regardless of how healthy the deployment is. The frontier's epistemic knob is therefore **q (seeded controls), not s (passive sampling)**; `s_min` remains for universal exposure, appeals capacity, and deterrence optics.

## Boundaries

- Drift parameters stipulated (rate 0.03/cycle from cycle 24); the claim is structural (no-positives ⇒ no measurement), not magnitude-calibrated.
- Opportunists were not drift-aware; a gamer who *learns* the drift would raise exposure and paradoxically make the drift more visible — declared, untested.
- Seeded controls are evaluated analytically (Bernoulli probe argument), not simulated; their operational design (who seeds, blinding, control secrecy) belongs to the corpus-side formalization.
