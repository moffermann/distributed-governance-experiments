# Ablation and Sensitivity Program — pre-registered design

Registered 2026-07-06, before the engine changes and runs it specifies. Purpose: find where Core v0 actually breaks — which mechanisms carry the architecture's advantage, at which parameter values the advantage collapses, and what the three so-far-unimplemented attacks do to it. Findings that suggest Core v0 changes flow back to the master corpus through its attack → defense → resolution pipeline with the author's verdict; nothing here redefines Core v0 directly.

## Base configuration

All runs use the `behavioral-llm-calibrated` population (the best-grounded one) on engine v0.5, 20 runs, seed 1, unless stated. The reference arm is `core_v0_tutored_distributed_planning` (V ≈ 0.277 verified value/budget; status quo 0.127).

## Axis 1 — Mechanism ablation (knock-outs, one at a time)

| Id | Knock-out | Implements |
|---|---|---|
| K1 | `fundingCaps: false` | no funding-target closure |
| K2 | `detectionBase: 0.15` | status-quo inspection intensity |
| K3 | `retention: 0.05, guarantee: 0.02` | status-quo financial terms |
| K4 | `reputationLoss: 0.02, futureSelectionLoss: 0.02` | no reputational memory |
| K5 | `passiveAllocationMode: "salience"` | no default layer (passivity herds) |
| K6 | `planningSource: "central"` | central default vector |
| K7 | `delegatorShare → passive` | no delegation channel |
| K8 | `profileShare → passive` | no profile channel |
| K9 | `socialProofDamping: 1.0` | no herding brake |

## Axis 2 — Parameter sensitivity (cliff-hunting sweeps)

Sweeps on the intact architecture, reporting the Core-distributed ÷ status-quo ratio at each point and the thresholds where it crosses 1.5× and 1.0×:

- `detectionBase` ∈ {0.15, 0.25, 0.35, 0.55, 0.75}
- `executors.opportunisticShare` ∈ {0.1, 0.3, 0.5, 0.7}
- `distributedPlanningSignalMix` ∈ {0.2, 0.4, 0.66, 0.8}
- `population.delegationBlockSize` ∈ {1, 3, 10, 50}
- `salienceCascade.socialProofWeight` ∈ {1, 3, 6}

## Axis 3 — The three unimplemented attacks

- **`fiscalizerCollusion`** (attacks Proposition 4's collusion-proofness): with probability `collusionRate`, a diverting opportunist's detection is bought off — and sophisticated opportunists anticipate it, so effective detection also falls inside the deterrence inequality. Sweep `collusionRate` ∈ {0.15, 0.30, 0.50}.
- **`agendaCapture`** (attacks docs/87's open problem): a captured share of the distributed default vector is redirected to a favored project set — `score′ = (1−severity)·w + severity·1[favored]`. Sweep `severity` ∈ {0.15, 0.30, 0.50}.
- **`coordinatedSignalBias`** (E7b's geometry in this engine): a share of attentive citizens allocates to a favored set instead of their own information. Sweep `share` ∈ {0.10, 0.30, 0.50}.

Attack implementations must consume zero RNG draws when disabled, so all committed baselines stay byte-identical.

## Pre-registered predictions (derived from the corpus's own claims)

- **P1.** The largest single-mechanism loss in *verified* value is the default layer (K5): under realistic populations 50–80% of weight flows through it, so its removal collapses Core toward the salience-participatory level (~0.10) — the Experiment C zero-delivery finding approached from above.
- **P2.** Among the *deterrence* terms, reputational memory (K4) costs more than inspection intensity (K2): the corpus claims detection without memory buys a smaller lie, not more delivery (E7). Concretely: K4's leak increase exceeds K2's.
- **P3.** The financial terms (K3) and memory (K4) are partially substitutable — each alone leaves the deterrence inequality binding for part of the cost support — so neither alone reproduces the full zero-control leak; removing both would (not run as a knock-out pair in the main table; noted for a follow-up if P3 fails).
- **P4.** The planning-source ablation (K6) costs approximately the committed core-central gap (ΔV ≈ 0.05, from 0.277 to ≈ 0.224) — a selection-channel effect, no leak change.
- **P5.** Per unit of severity, `agendaCapture` is the most damaging attack: it corrupts the channel carrying the passive majority. `fiscalizerCollusion` damages verified value roughly linearly in `collusionRate`; `coordinatedSignalBias` only matters at high shares (E7b found the crossover near 30%).
- **P6 (cliffs).** The Core advantage stays above 1.5× for every single-parameter sweep point within the audit-anchored ranges (detection ≥ 0.35, opportunists ≤ 0.5); it approaches 1.0× only under high-severity agenda capture (≥ 0.5) — the honest boundary: an architecture whose default vector is captured is not distributed governance anymore.

## Outputs

Engine v0.5 (attacks + architecture overrides + parameterized module), an `ablation.mjs` runner, `results/ablation/` tables, and a vulnerability report ranking mechanisms and attack severities with the prediction accounting.
