# Model docking: JS adversarial ABM ↔ Mesa reimplementation

**Docking style:** Axtell, Axelrod, Epstein & Cohen (1996) — *distributional*
equivalence, not stream identity. A second team reimplements the model in a
different language and paradigm with an independent RNG; the docking succeeds if
the two engines produce the same *distributions* of output metrics.

- **Reference engine (ground truth):** `adversarial-abm/src/index.mjs`
  (engine v0.5.1, mulberry32 PRNG), committed summary
  `adversarial-abm/results/behavioral-llm-calibrated/behavioral-llm-calibrated-seed1-runs20.summary.csv`.
- **Docked engine:** `docking/mesa/model.py` + `docking/mesa/run_dock.py`
  (Mesa **3.5.1**, Python `random.Random`).
- **Scenario:** `adversarial-abm/scenarios/behavioral-llm-calibrated.json`
  (v0.4) — 10 000 citizens, 40 projects, 24 cycles, **20 runs**, base seed 1.
- **Independent RNG:** the world is generated once per run with
  `random.Random(seed)` for seeds **1..20** (the JS "common-world paired
  comparison"); each architecture then plays that shared world with its own
  derived `random.Random`. No mulberry32 clone is used anywhere.

## Reproduction

```bash
python docking/mesa/run_dock.py     # writes docking/mesa/results.json
```

(Mesa is required: `pip install mesa`. Run from the repository root.)

## Equivalence test

For each metric and architecture, PASS iff

```
|mean_JS − mean_Mesa|  ≤  2 · sqrt( sd_JS²/20 + sd_Mesa²/20 )
```

i.e. the gap between the two independent 20-run sample means is within two
pooled standard errors — a ~95% band under the null "same population".

## Results

### Primary metric — `verifiedValuePerBudget` (Σ verified value / Σ funded)

| architecture | JS mean±sd | Mesa mean±sd | \|Δ\| | band (2·pooled SE) | verdict |
|---|---:|---:|---:|---:|:--:|
| status_quo | 0.12674±0.01841 | 0.13446±0.01771 | 0.00772 | 0.01142 | **PASS** |
| participatory_weak_verification | 0.00000±0.00000 | 0.00000±0.00000 | 0.00000 | 0.00000 | **PASS** |
| participatory_weak_verification_full_budget | 0.10263±0.02425 | 0.10339±0.01792 | 0.00076 | 0.01348 | **PASS** |
| core_v0_tutored_mandated_agenda | 0.22446±0.03409 | 0.22705±0.02982 | 0.00259 | 0.02026 | **PASS** |
| core_v0_tutored_distributed_agenda | 0.27742±0.04013 | 0.27798±0.03721 | 0.00055 | 0.02447 | **PASS** |

### `leakageRate` (Σ leakage / Σ funded)

| architecture | JS mean±sd | Mesa mean±sd | \|Δ\| | band (2·pooled SE) | verdict |
|---|---:|---:|---:|---:|:--:|
| status_quo | 0.08413±0.04800 | 0.07212±0.05057 | 0.01201 | 0.03118 | **PASS** |
| participatory_weak_verification | 0.00000±0.00000 | 0.00000±0.00000 | 0.00000 | 0.00000 | **PASS** |
| participatory_weak_verification_full_budget | 0.06592±0.03974 | 0.06109±0.04249 | 0.00483 | 0.02602 | **PASS** |
| core_v0_tutored_mandated_agenda | 0.00780±0.02009 | 0.00418±0.01309 | 0.00363 | 0.01072 | **PASS** |
| core_v0_tutored_distributed_agenda | 0.00885±0.02252 | 0.00663±0.01692 | 0.00222 | 0.01260 | **PASS** |

### `selectionValueCorrelation` (Pearson: funded-flag vs latent value)

| architecture | JS mean±sd | Mesa mean±sd | \|Δ\| | band (2·pooled SE) | verdict |
|---|---:|---:|---:|---:|:--:|
| status_quo | 0.28845±0.15049 | 0.32604±0.16472 | 0.03759 | 0.09978 | **PASS** |
| participatory_weak_verification | 0.00000±0.00000 | 0.00000±0.00000 | 0.00000 | 0.00000 | **PASS** |
| participatory_weak_verification_full_budget | 0.16605±0.21868 | 0.21111±0.14438 | 0.04506 | 0.11719 | **PASS** |
| core_v0_tutored_mandated_agenda | 0.36119±0.12060 | 0.38413±0.12122 | 0.02294 | 0.07647 | **PASS** |
| core_v0_tutored_distributed_agenda | 0.61606±0.08144 | 0.58559±0.09771 | 0.03047 | 0.05688 | **PASS** |

**Verdict: 15/15 PASS** (5 architectures × 3 metrics). The Mesa reimplementation
is distributionally equivalent to the JavaScript reference engine, and it
reproduces the qualitative ordering the paper relies on:

- Core v0 distributed agenda delivers the most verified value per budget
  (≈0.278), roughly **2.2×** the status-quo central planner (≈0.127/0.134).
- The mandated-agenda transition scaffold sits below distributed (≈0.227) but
  well above status quo.
- Weak participation with no default layer **absorbs almost no budget and
  executes nothing** (verified value exactly 0; only ~15.4% of budget spent).
- Salience-financed full-budget participation restores spending but leaks
  (~0.06) and selects value only weakly (sel≈0.17–0.21), landing near status
  quo on verified value.
- Leakage is an order of magnitude lower under both Core v0 variants
  (~0.004–0.009) than under status quo or salience participation (~0.06–0.08),
  reproducing the verification-plus-deterrence effect.

## `selectionValueCorrelation` feasibility

It was feasible and is included above. It is computed exactly as in the JS
`computeMetrics`: Pearson correlation between each project's funded-flag
(1 if executed, else 0) and its latent value, across all 40 projects, averaged
over runs. The correlation std devs are large (funded-flag is binary over 40
projects, so per-run estimates are noisy), which is why the bands are wide — but
the means track the JS engine closely and preserve the ordering
distributed > mandated > status_quo > full_budget > participatory(=0).

## Honest discussion of divergences

All gaps are within band; none indicates a porting defect. The notable points:

1. **`status_quo` is the largest relative gap on the primary metric**
   (Δ=0.0077, 68% of its band). Its verified value runs slightly *high* in Mesa
   (0.1345 vs 0.1267) and, consistently, its leakage runs slightly *low*
   (0.0721 vs 0.0841). These move together: status quo has the weakest
   verification (`detectionBase` 0.15, `reviewConfidence` 0.35), so it is the
   architecture whose output is most sensitive to exactly which opportunistic
   executors divert and get away with it. With independent RNG streams the Monte
   Carlo realisation of those Bernoulli diversion/detection events differs, and
   0.68 σ of drift over 20 runs is exactly what the band anticipates. Both
   metrics remain comfortably inside their bands.

2. **`participatory_weak_verification` is an exact structural zero, not a
   near-miss.** With `fundingCaps=false` and `passiveAllocationMode="none"`,
   only the attentive (498) and salience (1043) channels spend, so budget spent
   is a deterministic 1541 × 24 = 36 984 (utilisation 0.1541, sd 0 in both
   engines), and no project ever reaches its budget target within 24 cycles, so
   `fundedRate=0` and every value/leakage metric is identically 0. Both engines
   reproduce this exactly, so the docking of this row is trivially perfect
   (Δ=0, band=0). This is the low-absorption failure the variant exists to show.

3. **Correlation bands are wide** because the funded-flag is a 40-point binary
   vector; the per-run Pearson estimate has high variance. The means still agree
   to within ~0.03–0.05 everywhere, so the ordering the paper reports is robust
   across the two independent implementations.

### Why distributions match despite different RNGs

The engines share *marginals*, not streams: `sampleDist`'s `beta`/`uniform`
specs map to `random.betavariate`/`random.uniform`; JS Box–Muller `normal` maps
to `random.gauss`; sampling-without-replacement (`drawSample`) maps to
`random.sample`; roulette selection (`weightedPick`) and the deterministic
`allocateDefault`/`allocateCentral` fills are ported line-for-line. Because
every stochastic primitive draws from the identical distribution family and the
mechanism logic is identical, the aggregate metrics converge to the same
population means — which is precisely what a docking is meant to demonstrate.
```
