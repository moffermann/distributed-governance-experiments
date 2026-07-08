# Experiment H: Project Allocation Rules — the two-layer decomposition

Two-layer static engine; core arm unless noted; 40 runs, seed 1; 6 categories, value cap 0.3. Verified value per budget.

## (a) The incidental leak — marginal at realistic profile compositions

| incidental share of profiles | V central | V distributed | ratio |
|---:|---:|---:|---:|
| 0.0 | 0.2701 | 0.2855 | 1.06× |
| 0.1 | 0.2566 | 0.2695 | 1.05× |
| 0.2 | 0.2376 | 0.2533 | 1.07× |
| 0.3 | 0.2166 | 0.2364 | 1.09× |
| 0.5 | 0.1731 | 0.2012 | 1.16× |
| 0.9 | 0.0615 | 0.1053 | 1.71× |

At a moderately-misaligned categorization (35% of the pool), value-targeted profile rules self-correct and only attribute-incidental rules leak; distributing the partition is marginal (≈1.05–1.16× at realistic incidental shares). A misaligned project's leaked funding is small because "near me" is one weighted rule balanced by value-aligned ones ("pending funding" tracks the attentive minority; thematic rules track value).

## (b) The ceiling — distributing #1 goes from irrelevant to decisive as the central categorization worsens

| central categorization misaligned | V central | V distributed | advantage of distributing #1 |
|---:|---:|---:|---:|
| 0% | 0.2391 | 0.2391 | 1.00× |
| 20% | 0.2440 | 0.2590 | 1.06× |
| 35% | 0.2376 | 0.2533 | 1.07× |
| 50% | 0.2330 | 0.2687 | 1.15× |
| 65% | 0.2104 | 0.2883 | 1.37× |
| 80% | 0.1627 | 0.2850 | 1.75× |
| 90% | 0.1197 | 0.2946 | 2.46× |

The distributed arm is **flat** across categorization quality (it re-categorizes to value); the central arm collapses. So distributing the categorization is **irrelevant** when it is well-drawn (1.00×), **marginal** under moderate misalignment (~1.06–1.15×; citizens' profiles route around bad categories), and **decisive** when the categorization is mostly bad (1.75×→2.46×; the good projects are not even eligible, and #2 cannot route to what is absent). Delivered value is **robust to a bad central categorization** under distribution and **fragile to it** under central planning.

## (c) Core v0 vs the central status quo — the advantage grows as central planning worsens

| central categorization misaligned | status quo V | Core v0 V | Core v0 / status quo |
|---:|---:|---:|---:|
| 0% | 0.1285 | 0.2414 | 1.88× |
| 20% | 0.1178 | 0.2486 | 2.11× |
| 35% | 0.1061 | 0.2539 | 2.39× |
| 50% | 0.0946 | 0.2696 | 2.85× |
| 65% | 0.0773 | 0.2899 | 3.75× |
| 80% | 0.0632 | 0.2964 | 4.69× |
| 90% | 0.0521 | 0.2981 | 5.73× |

**The combined effect.** Comparing architectures, Core v0's advantage over a central status quo is **not fixed** — it is a function of central-planning quality, rising from 1.88× (well-drawn categorization) to **5.73×** (mostly-bad). Two effects compound: the *advantage of choosing* (#2 routes to higher-value projects) and *avoiding an imposed bad central plan* (#1 re-categorizes rather than being stuck with the authority's categories). The fused single-weight model could express neither; the two-layer model shows both, and that they multiply. (The base ratio here is scenario-specific with two-layer on, not the cross-population 2.0–2.7× headline; the finding is the trend, not the base.)

Boundary: allocation-quality layer only; the verification/deterrence/release pipeline is downstream and unchanged. Simulation evidence about a model.
