# Experiment H: Project Allocation Rules — the two-layer decomposition

Two-layer static engine; core arm; 40 runs, seed 1; 6 categories, misaligned share 0.35, value cap 0.3. Verified value per budget.

## Distributing the macro partition (#1) across profile compositions (#2)

| incidental share of profiles (#2) | V, central partition | V, distributed partition | advantage of distributing #1 |
|---:|---:|---:|---:|
| 0.0 | 0.2701 | 0.2855 | 1.06× |
| 0.1 | 0.2566 | 0.2695 | 1.05× |
| 0.3 | 0.2166 | 0.2364 | 1.09× |
| 0.5 | 0.1731 | 0.2012 | 1.16× |
| 0.7 | 0.1214 | 0.1567 | 1.29× |
| 0.9 | 0.0615 | 0.1053 | 1.71× |

**Finding (PL1, ratio form).** The advantage of distributing the macro categorization (#1) grows with the share of attribute-incidental profile rules: 1.05× at 0.1 incidental, 1.71× at 0.9. When the inattentive majority routes by value-orthogonal rules ("near me"), only distributing #1 removes the misaligned projects they would otherwise leak into; when profiles are value-targeted, they self-correct and #1 matters less. This decomposition is impossible in the fused single-weight model.

## #1-vs-#2 contribution decomposition (at a mixed profile composition, incidental 0.5)

| configuration | V |
|---|---:|
| central #1, mixed #2 (baseline) | 0.1731 |
| **distribute #1 only** (distributed partition, mixed #2) | 0.2012  (Δ +0.0281) |
| **improve #2 only** (central partition, all-targeted profiles) | 0.2701  (Δ +0.0971) |
| both | 0.2855  (Δ +0.1124) |

**Decomposition.** From the central/mixed baseline, distributing #1 alone adds 0.0281 and improving #2 alone (value-targeted profiles) adds 0.0971; the two are #2-dominant here and combine to 0.1124. The point is that the two-layer model **can attribute** the advantage to a layer; the fused model reported one number.

Boundary: this is the allocation-quality layer only; the pipeline (verification, deterrence, release) is downstream and unchanged. Simulation evidence about a model.
