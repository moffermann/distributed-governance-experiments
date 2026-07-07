# F-0 Results: cross-engine error structure

families with >=100/120 verdicts: gemma, qwen, deepseek, gpt, claude; per-family coverage: gemma=118, qwen=116, deepseek=120, gpt=120, claude=120

## Per-family error rates

| family | false-pass (all flawed) | false-flag (clean) | fp inflated_unit_prices | fp compressed_timeline | fp photo_coverage_gap | fp quantity_shortfall | fp related_party | fp threshold_structuring |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemma | 0.119 | 0.458 | 0.00 | 0.20 | 0.20 | 0.00 | 0.30 | 0.00 |
| qwen | 0.000 | 1.000 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| deepseek | 0.217 | 0.317 | 0.00 | 0.40 | 0.30 | 0.00 | 0.30 | 0.30 |
| gpt | 0.033 | 0.800 | 0.00 | 0.10 | 0.10 | 0.00 | 0.00 | 0.00 |
| claude | 0.083 | 0.050 | 0.00 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 |

## Pairwise error correlation (phi on false-pass indicators, flawed cases)

| pair | phi (false-pass) | phi (false-flag, clean) |
|---|---:|---:|
| gemma-qwen | None | None |
| gemma-deepseek | 0.184 | 0.095 |
| gemma-gpt | -0.069 | 0.042 |
| gemma-claude | 0.265 | 0.097 |
| qwen-deepseek | None | None |
| qwen-gpt | None | None |
| qwen-claude | None | None |
| deepseek-gpt | 0.128 | 0.161 |
| deepseek-claude | 0.427 | -0.156 |
| gpt-claude | 0.280 | 0.115 |

## Ensemble false-pass: measured vs independence

A k-stack clears a flawed case only if every member passes it.

| stack | measured | independence prediction | ratio (measured/indep) |
|---|---:|---:|---:|
| gemma+qwen | 0.000 | 0.0000 | inf |
| gemma+deepseek | 0.051 | 0.0261 | 1.9x |
| gemma+gpt | 0.000 | 0.0040 | 0.0x |
| gemma+claude | 0.034 | 0.0101 | 3.4x |
| qwen+deepseek | 0.000 | 0.0000 | inf |
| qwen+gpt | 0.000 | 0.0000 | inf |
| qwen+claude | 0.000 | 0.0000 | inf |
| deepseek+gpt | 0.017 | 0.0072 | 2.3x |
| deepseek+claude | 0.067 | 0.0181 | 3.7x |
| gpt+claude | 0.017 | 0.0028 | 6.0x |
| gemma+qwen+deepseek | 0.000 | 0.0000 | inf |
| gemma+qwen+gpt | 0.000 | 0.0000 | inf |
| gemma+qwen+claude | 0.000 | 0.0000 | inf |
| gemma+deepseek+gpt | 0.000 | 0.0009 | 0.0x |
| gemma+deepseek+claude | 0.034 | 0.0022 | 15.3x |
| gemma+gpt+claude | 0.000 | 0.0003 | 0.0x |
| qwen+deepseek+gpt | 0.000 | 0.0000 | inf |
| qwen+deepseek+claude | 0.000 | 0.0000 | inf |
| qwen+gpt+claude | 0.000 | 0.0000 | inf |
| deepseek+gpt+claude | 0.017 | 0.0006 | 27.7x |

## Effective common-cause rho (for F-1)

- best 2-stack (gemma+gpt): measured 0.000, indep 0.0040 -> rho_eff = 0.000
- median 2-stack (gemma+claude): rho_eff = 0.024

