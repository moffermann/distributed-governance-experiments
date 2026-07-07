# F-0 Results: cross-engine error structure

families with >=100/120 verdicts: gemma, qwen, deepseek, gpt, claude; per-family coverage: gemma=120, qwen=120, deepseek=120, gpt=120, claude=120

## Per-family error rates

| family | false-pass (all flawed) | false-flag (clean) | fp fabricated_progress | fp metadata_inconsistency | fp wrong_location | fp recycled_evidence | fp quantity_mismatch | fp plausible_staging |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemma | 0.000 | 0.167 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| qwen | 0.000 | 1.000 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| deepseek | 0.050 | 0.317 | 0.10 | 0.10 | 0.00 | 0.00 | 0.00 | 0.10 |
| gpt | 0.000 | 0.767 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| claude | 0.000 | 0.950 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## Pairwise error correlation (phi on false-pass indicators, flawed cases)

| pair | phi (false-pass) | phi (false-flag, clean) |
|---|---:|---:|
| gemma-qwen | None | None |
| gemma-deepseek | None | -0.112 |
| gemma-gpt | None | 0.035 |
| gemma-claude | None | -0.103 |
| qwen-deepseek | None | None |
| qwen-gpt | None | None |
| qwen-claude | None | None |
| deepseek-gpt | None | 0.037 |
| deepseek-claude | None | 0.156 |
| gpt-claude | None | 0.416 |

## Ensemble false-pass: measured vs independence

A k-stack clears a flawed case only if every member passes it.

| stack | measured | independence prediction | ratio (measured/indep) |
|---|---:|---:|---:|
| gemma+qwen | 0.000 | 0.0000 | inf |
| gemma+deepseek | 0.000 | 0.0000 | inf |
| gemma+gpt | 0.000 | 0.0000 | inf |
| gemma+claude | 0.000 | 0.0000 | inf |
| qwen+deepseek | 0.000 | 0.0000 | inf |
| qwen+gpt | 0.000 | 0.0000 | inf |
| qwen+claude | 0.000 | 0.0000 | inf |
| deepseek+gpt | 0.000 | 0.0000 | inf |
| deepseek+claude | 0.000 | 0.0000 | inf |
| gpt+claude | 0.000 | 0.0000 | inf |
| gemma+qwen+deepseek | 0.000 | 0.0000 | inf |
| gemma+qwen+gpt | 0.000 | 0.0000 | inf |
| gemma+qwen+claude | 0.000 | 0.0000 | inf |
| gemma+deepseek+gpt | 0.000 | 0.0000 | inf |
| gemma+deepseek+claude | 0.000 | 0.0000 | inf |
| gemma+gpt+claude | 0.000 | 0.0000 | inf |
| qwen+deepseek+gpt | 0.000 | 0.0000 | inf |
| qwen+deepseek+claude | 0.000 | 0.0000 | inf |
| qwen+gpt+claude | 0.000 | 0.0000 | inf |
| deepseek+gpt+claude | 0.000 | 0.0000 | inf |

