# Consolidated Results

Headline numbers across the experiment program, with provenance. Regenerate figures with `python tools/make_figures.py` (accessible descriptions in [`figures/FIGURES.md`](figures/FIGURES.md)). Every result directory carries a `.meta.json` stamp (engine version, scenario version, seed, runs).

## Architecture comparison under adversarial stress (A + C)

Verified value per unit of budget (mean over 20 runs, seed 1, engine v0.4.x):

| Architecture | imposed | behavioral synthetic | behavioral LLM | high friction | delegation-first |
|---|---:|---:|---:|---:|---:|
| Core v0 tutored distributed | 0.262 | 0.307 | 0.277 | **0.340** | 0.300 |
| Core v0 tutored central | 0.214 | 0.231 | 0.224 | 0.274 | 0.239 |
| Status quo | 0.128 | 0.127 | 0.127 | 0.127 | 0.128 |
| Participatory (salience full-budget) | 0.104 | 0.104 | 0.103 | 0.105 | 0.107 |
| Participatory (no default layer) | 0.029 | **0.000** | **0.000** | **0.000** | **0.000** |
| **Core distributed ÷ status quo** | **2.05×** | **2.42×** | **2.18×** | **2.68×** | **2.34×** |

Source: `adversarial-abm/results/*/…summary.csv`; interpretation and prediction accounting in `adversarial-abm/RUN_2026_07_06_BEHAVIORAL_INTEGRATION_RESULTS.md`.

## Planning-vector quality (supporting program)

corr(plan, latent social value), 200 runs, seed 42, engine v0.5.1:

| Family | Range |
|---|---|
| Core v0 distributed channels (9 variants) | 0.815 – 0.939 |
| Representative central (crisis → high alignment) | 0.315 – 0.650 |
| Salience only | 0.187 |

The families do not overlap: the worst Core v0 channel out-informs the best central regime. Source: `planning-vector-construction/results/core-v0-planning-channels/`.

## Behavioral adoption (B)

10-seed sweeps, 104 weeks, 1,000 citizens, engine v1.1.0:

| Metric | synthetic priors | LLM-calibrated priors |
|---|---:|---:|
| Registered / active share | 52% / 34% | 68% / 50% |
| Default-rule share | 66% | 50% |
| **Attentive (planning) share** | **4.1%** | **~5.0%** |
| Delegator share; micro weight | 12%; 66% | 24%; 76% |
| Evidence-undersupply flag | 10/10 seeds | 10/10 seeds |

Structural findings (stable across all prior sources): the attentive share sits at ~4–5% and the verification market, not adoption, is the binding constraint. Sources: `behavioral-adoption-abm/RUN_2026_07_06_*.md`.

## Calibration panels (feeding B)

| Panel | Model | n | Key stability result |
|---|---|---:|---|
| n=90 ×2 models | gemma-3-4b, gpt-5.5 | 180 | Levels are model-dependent; the micro-over-institutional delegate preference (≈3:1) and delegate planning coverage (0.43–0.52) are cross-model-stable |
| N=1000 weighted | gpt-5.5 | 1000 | Converges by n≈750 (±0.005); 20-archetype composition shifts pooled means ≤0.02; opposed archetype restores a plausible rejection rate |

Sources: `planning-behavior-calibration/RUN_2026_07_06_*.md`, `results/`.

## Bridge to the master paper (E8, lives in the master repository)

The behavioral trajectories replaced the paper engine's imposed participation: headline V(A2)/V(S′) = 2.26 [2.23, 2.30] at scale (vs 2.22 imposed), 2.15–2.9× across populations and scales, launch dynamics cost 1.7%. Recorded in the master repository's `research/simulation-results.md` §E8.

## Run index

| Run record | Experiment | Engine | Scenario(s) | Seeds |
|---|---|---|---|---|
| `adversarial-abm/RUN_2026_07_06_BEHAVIORAL_INTEGRATION_RESULTS.md` | A + C | v0.4 | baseline-medium + 4 behavioral | 1–20 |
| `behavioral-adoption-abm/RUN_2026_07_06_POST_AUDIT_RESULTS.md` | B (pre-planning engine, dated record) | v1.0 | 4 scenarios | 42–51 |
| `behavioral-adoption-abm/RUN_2026_07_06_PLANNING_LAYER_RESULTS.md` | B end-to-end | v1.0 | 5 scenarios + attendance sweep | 42–51 |
| `behavioral-adoption-abm/RUN_2026_07_06_LLM_CALIBRATED_RESULTS.md` | B calibrated | v1.0 | llm_calibrated vs baseline | 42–51 |
| `planning-behavior-calibration/RUN_2026_07_06_LLM_PANEL_RESULTS.md` | panels | prompt v0.3 | 6 archetypes ×2 models | persona seed 42 |
| `planning-behavior-calibration/RUN_2026_07_06_N1000_PANEL_RESULTS.md` | panel at scale | prompt v0.3 | 20 weighted archetypes | persona seed 42 |
| `planning-vector-construction/results/` | supporting | v0.5.1 | core-v0-planning-channels v0.5 | 42, 200 runs |

Engine audits: `behavioral-adoption-abm/CORE_V0_CONFORMANCE_AUDIT.md`, `adversarial-abm/ENGINE_AUDIT_2026_07_06.md`, `planning-vector-construction/ENGINE_AUDIT_2026_07_06.md`. Core v0 anchoring: [`TRACEABILITY_MATRIX.md`](TRACEABILITY_MATRIX.md).
