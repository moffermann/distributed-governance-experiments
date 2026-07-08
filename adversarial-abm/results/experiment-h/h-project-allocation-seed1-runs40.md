# Experiment H: Project Allocation Rules — the two-layer decomposition

Two-layer static engine; core arm; 40 runs, seed 1; 6 categories, misaligned share 0.35, value cap 0.3. Verified value per budget.

## Distributing the macro partition (#1) across profile compositions (#2)

| incidental share of profiles (#2) | V, central partition | V, distributed partition | advantage of distributing #1 |
|---:|---:|---:|---:|
| 0.0 | 0.2128 | 0.2911 | 1.37× |
| 0.1 | 0.1951 | 0.2742 | 1.41× |
| 0.3 | 0.1616 | 0.2415 | 1.49× |
| 0.5 | 0.1292 | 0.2061 | 1.60× |
| 0.7 | 0.0965 | 0.1597 | 1.66× |
| 0.9 | 0.0496 | 0.1067 | 2.15× |

**Finding (PL1, ratio form).** The advantage of distributing the macro categorization (#1) grows with the share of attribute-incidental profile rules: 1.41× at 0.1 incidental, 2.15× at 0.9. When the inattentive majority routes by value-orthogonal rules ("near me"), only distributing #1 removes the misaligned projects they would otherwise leak into; when profiles are value-targeted, they self-correct and #1 matters less. This decomposition is impossible in the fused single-weight model.

## #1-vs-#2 contribution decomposition (at a mixed profile composition, incidental 0.5)

| configuration | V |
|---|---:|
| central #1, mixed #2 (baseline) | 0.1292 |
| **distribute #1 only** (distributed partition, mixed #2) | 0.2061  (Δ +0.0769) |
| **improve #2 only** (central partition, all-targeted profiles) | 0.2128  (Δ +0.0836) |
| both | 0.2911  (Δ +0.1619) |

**Decomposition.** From the central/mixed baseline, distributing #1 alone adds 0.0769 and improving #2 alone (value-targeted profiles) adds 0.0836; the two are #2-dominant here and combine to 0.1619. The point is that the two-layer model **can attribute** the advantage to a layer; the fused model reported one number.

Boundary: this is the allocation-quality layer only; the pipeline (verification, deterrence, release) is downstream and unchanged. Simulation evidence about a model.
