# Multi-base-seed robustness check

Five independent base seeds (1, 101, 202, 303, 404), 20 runs each; between-seed spread of the 20-run means for the two headline cells.

## Static architecture comparison (behavioral-llm-calibrated)

| base seed | V core distributed | V status quo | ratio |
|---:|---:|---:|---:|
| 1 | 0.277 | 0.127 | 2.19x |
| 101 | 0.291 | 0.130 | 2.23x |
| 202 | 0.284 | 0.129 | 2.20x |
| 303 | 0.282 | 0.126 | 2.24x |
| 404 | 0.293 | 0.129 | 2.28x |
| **between-seed** | 0.285 ± 0.006 [0.277, 0.293] | 0.128 ± 0.002 [0.126, 0.130] | 2.23x ± 0.03 [2.19, 2.28] |

## Longitudinal pull W*=7 (E-1a headline cell)

| base seed | V per budget-year |
|---:|---:|
| 1 | 0.304 |
| 101 | 0.304 |
| 202 | 0.291 |
| 303 | 0.293 |
| 404 | 0.300 |
| **between-seed** | 0.298 ± 0.005 [0.291, 0.304] |

