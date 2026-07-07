# F-0 Results: cross-engine error structure

families with >=100/120 verdicts: gemma, qwen, deepseek, gpt, claude; per-family coverage: gemma=104, qwen=112, deepseek=120, gpt=120, claude=120

## Per-family error rates (Wilson 95% CIs; N = usable verdicts per side)

| family | N flawed | false-pass [95% CI] | N clean | false-flag [95% CI] |
|---|---:|---|---:|---|
| gemma | 55 | 11/55 = 0.200 [0.116, 0.324] | 49 | 13/49 = 0.265 [0.162, 0.403] |
| qwen | 60 | 0/60 = 0.000 [0.000, 0.060] | 52 | 51/52 = 0.981 [0.899, 0.997] |
| deepseek | 60 | 12/60 = 0.200 [0.118, 0.318] | 60 | 34/60 = 0.567 [0.441, 0.684] |
| gpt | 60 | 5/60 = 0.083 [0.036, 0.181] | 60 | 2/60 = 0.033 [0.009, 0.114] |
| claude | 60 | 5/60 = 0.083 [0.036, 0.181] | 60 | 5/60 = 0.083 [0.036, 0.181] |

Per-flaw-class false-pass (event/n per 10-case cell — too small to rank; shown for completeness):

| family | inflated_unit_prices | compressed_timeline | photo_coverage_gap | quantity_shortfall | related_party | threshold_structuring |
|---|---|---|---|---|---|---|
| gemma | 0/10 | 3/9 | 5/9 | 0/10 | 3/7 | 0/10 |
| qwen | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 |
| deepseek | 0/10 | 3/10 | 3/10 | 0/10 | 4/10 | 2/10 |
| gpt | 0/10 | 4/10 | 1/10 | 0/10 | 0/10 | 0/10 |
| claude | 0/10 | 5/10 | 0/10 | 0/10 | 0/10 | 0/10 |

## Pairwise error correlation (phi; false-pass on flawed cases)

| pair | joint false-pass (k of n) | phi | Fisher exact p |
|---|---:|---:|---:|
| gemma-qwen | 0/55 | None | 1.000 |
| gemma-deepseek | 4/55 | 0.205 | 0.202 |
| gemma-gpt | 4/55 | 0.474 | 0.004 |
| gemma-claude | 3/55 | 0.385 | 0.022 |
| qwen-deepseek | 0/60 | None | 1.000 |
| qwen-gpt | 0/60 | None | 1.000 |
| qwen-claude | 0/60 | None | 1.000 |
| deepseek-gpt | 2/60 | 0.151 | 0.259 |
| deepseek-claude | 2/60 | 0.151 | 0.259 |
| gpt-claude | 4/60 | 0.782 | 0.000 |

Interpretation guard: joint counts of 1-4 events cannot support a resolved dependence estimate; treat every phi and ratio below as **exploratory and underpowered** (review round 2 S1-S2). Report the distribution, not the maximum.

## Ensemble false-pass: measured vs independence (exploratory)

A k-stack clears a flawed case only if every member passes it. Granularity floor 1/n often exceeds the independence prediction, so ratio>1 can be forced by discretization, not dependence — see the CI column.

| stack | joint (k of n) | measured | independence | ratio | ratio 95% CI (bootstrap) |
|---|---:|---:|---:|---:|---|
| gemma+qwen | 0/55 | 0.000 | 0.0000 | inf | n/a |
| gemma+deepseek | 4/55 | 0.073 | 0.0400 | 1.8x | [0.5, 3.4]x |
| gemma+gpt | 4/55 | 0.073 | 0.0182 | 4.0x | [2.0, 7.9]x |
| gemma+claude | 3/55 | 0.055 | 0.0145 | 3.8x | [0.0, 7.9]x |
| qwen+deepseek | 0/60 | 0.000 | 0.0000 | inf | n/a |
| qwen+gpt | 0/60 | 0.000 | 0.0000 | inf | n/a |
| qwen+claude | 0/60 | 0.000 | 0.0000 | inf | n/a |
| deepseek+gpt | 2/60 | 0.033 | 0.0167 | 2.0x | [0.0, 5.0]x |
| deepseek+claude | 2/60 | 0.033 | 0.0167 | 2.0x | [0.0, 5.0]x |
| gpt+claude | 4/60 | 0.067 | 0.0069 | 9.6x | [4.7, 30.0]x |
| gemma+qwen+deepseek | 0/55 | 0.000 | 0.0000 | inf | n/a |
| gemma+qwen+gpt | 0/55 | 0.000 | 0.0000 | inf | n/a |
| gemma+qwen+claude | 0/55 | 0.000 | 0.0000 | inf | n/a |
| gemma+deepseek+gpt | 1/55 | 0.018 | 0.0036 | 5.0x | [0.0, 22.4]x |
| gemma+deepseek+claude | 1/55 | 0.018 | 0.0029 | 6.2x | [0.0, 25.9]x |
| gemma+gpt+claude | 3/55 | 0.055 | 0.0013 | 41.2x | [0.0, 189.1]x |
| qwen+deepseek+gpt | 0/60 | 0.000 | 0.0000 | inf | n/a |
| qwen+deepseek+claude | 0/60 | 0.000 | 0.0000 | inf | n/a |
| qwen+gpt+claude | 0/60 | 0.000 | 0.0000 | inf | n/a |
| deepseek+gpt+claude | 2/60 | 0.033 | 0.0014 | 24.0x | [0.0, 128.6]x |

**Honest summary:** of 10 two-stacks, 2 have a bootstrap ratio CI strictly above 1.0 (correlated failure separable from independence); the rest are consistent with independence.

## Effective common-cause rho (for F-1)

- best 2-stack (deepseek+gpt): measured 0.033, indep 0.0167 -> rho_eff = 0.017
- median 2-stack (gpt+claude): rho_eff = 0.060

