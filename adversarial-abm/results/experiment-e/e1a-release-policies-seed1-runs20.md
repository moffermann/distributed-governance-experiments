# Experiment E-1a: budget-release policies (longitudinal engine v0.6.0)

config: 4y x 12 cycles, citizens 2000, annual budget 24000, arrivals 2/cycle, mean target 1200, TTL 6, verify capacity 6/cycle, milestones 3, runs 20, seed 1

## Core v0 tutored-distributed arm

| policy | param | V/budget-year | frozen ratio (mean) | frozen sub (mo) | frozen WIP (mo) | queue | latency | leak | delivered | expired | unreleased@end | vs SQ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P0 day_zero |  | 0.286±0.019 | 0.237 | 0.3 | 5.2 | 5.6 | 8.5 | 0.005 | 77.0 | 13.9 | 0.00 | 2.50x |
| P1 uniform |  | 0.287±0.020 | 0.338 | 0.9 | 4.0 | 0.8 | 7.2 | 0.007 | 67.7 | 23.4 | 0.00 | 2.72x |
| P2 front_loaded | lambda=2 | 0.291±0.017 | 0.273 | 0.6 | 4.9 | 3.8 | 8.1 | 0.007 | 75.5 | 12.5 | 0.00 | 2.51x |
| P2 front_loaded | lambda=4 | 0.304±0.022 | 0.294 | 0.9 | 4.4 | 2.0 | 7.7 | 0.004 | 73.3 | 19.6 | 0.00 | 2.81x |
| P2 front_loaded | lambda=6 | 0.298±0.019 | 0.310 | 0.9 | 4.3 | 1.3 | 7.6 | 0.006 | 70.8 | 21.8 | 0.00 | 2.77x |
| P3 pull | W=2mo | 0.099±0.010 | 0.359 | 1.0 | 1.0 | 0.0 | 8.4 | 0.005 | 19.3 | 72.9 | 0.72 | 2.40x |
| P3 pull | W=4mo | 0.209±0.012 | 0.307 | 1.2 | 2.5 | 0.0 | 7.7 | 0.005 | 43.0 | 50.6 | 0.36 | 2.57x |
| P3 pull | W=6mo | 0.288±0.017 | 0.273 | 0.9 | 4.1 | 0.5 | 7.2 | 0.005 | 69.8 | 21.3 | 0.01 | 2.60x |
| P3 pull | W=8mo | 0.304±0.018 | 0.262 | 0.7 | 4.7 | 2.9 | 8.0 | 0.006 | 75.1 | 16.9 | 0.00 | 2.68x |
| P4 approval_conditioned | alpha=0.8 | 0.212±0.021 | 0.386 | 1.1 | 2.7 | 0.2 | 7.8 | 0.005 | 47.2 | 41.2 | 0.30 | 2.95x |
| P4 approval_conditioned | alpha=1.0 | 0.257±0.021 | 0.387 | 0.6 | 4.6 | 4.0 | 7.8 | 0.005 | 65.6 | 27.1 | 0.02 | 2.54x |
| P4 approval_conditioned | alpha=1.2 | 0.269±0.015 | 0.373 | 0.6 | 4.7 | 3.6 | 8.1 | 0.005 | 66.5 | 22.9 | 0.00 | 2.56x |
| P4 approval_conditioned | alpha=1.5 | 0.268±0.016 | 0.367 | 0.6 | 4.7 | 3.6 | 8.3 | 0.007 | 66.5 | 21.3 | 0.00 | 2.54x |
| P3 pull (refine) | W=7mo | 0.304±0.015 | 0.266 | 0.8 | 4.3 | 1.2 | 7.5 | 0.006 | 72.8 | 20.1 | 0.00 | 2.72x |
| P3 pull (refine) | W=7.5mo | 0.304±0.017 | 0.269 | 0.7 | 4.5 | 2.0 | 7.8 | 0.004 | 74.5 | 17.6 | 0.00 | 2.73x |
| P3 pull (refine) | W=8.5mo | 0.296±0.023 | 0.261 | 0.7 | 4.9 | 3.6 | 8.4 | 0.010 | 75.5 | 19.3 | 0.00 | 2.66x |
| P3 pull (refine) | W=9mo | 0.297±0.016 | 0.253 | 0.5 | 4.9 | 4.2 | 8.3 | 0.004 | 75.5 | 16.9 | 0.00 | 2.64x |
| P4 approval_conditioned (refine) | alpha=1.1 | 0.267±0.015 | 0.381 | 0.7 | 4.8 | 4.1 | 8.1 | 0.006 | 65.7 | 25.9 | 0.01 | 2.64x |
| P4 approval_conditioned (refine) | alpha=1.3 | 0.268±0.022 | 0.366 | 0.6 | 4.6 | 3.2 | 8.1 | 0.006 | 66.3 | 22.9 | 0.00 | 2.51x |

## Status-quo arm (same policies)

| policy | param | V/budget-year | frozen ratio | latency |
|---|---|---:|---:|---:|
| P0 day_zero |  | 0.114 | 0.244 | 9.0 |
| P1 uniform |  | 0.105 | 0.298 | 6.9 |
| P2 front_loaded | lambda=2 | 0.116 | 0.265 | 8.2 |
| P2 front_loaded | lambda=4 | 0.108 | 0.273 | 7.5 |
| P2 front_loaded | lambda=6 | 0.108 | 0.277 | 7.2 |
| P3 pull | W=2mo | 0.041 | 0.287 | 7.9 |
| P3 pull | W=4mo | 0.081 | 0.267 | 7.1 |
| P3 pull | W=6mo | 0.111 | 0.258 | 7.0 |
| P3 pull | W=8mo | 0.113 | 0.249 | 7.8 |
| P4 approval_conditioned | alpha=0.8 | 0.072 | 0.331 | 7.4 |
| P4 approval_conditioned | alpha=1.0 | 0.101 | 0.350 | 7.6 |
| P4 approval_conditioned | alpha=1.2 | 0.105 | 0.323 | 7.8 |
| P4 approval_conditioned | alpha=1.5 | 0.106 | 0.314 | 8.4 |
| P3 pull (refine) | W=7mo | 0.112 | 0.252 | 7.4 |
| P3 pull (refine) | W=7.5mo | 0.111 | 0.251 | 7.6 |
| P3 pull (refine) | W=8.5mo | 0.111 | 0.252 | 8.1 |
| P3 pull (refine) | W=9mo | 0.113 | 0.251 | 8.4 |
| P4 approval_conditioned (refine) | alpha=1.1 | 0.101 | 0.335 | 7.7 |
| P4 approval_conditioned (refine) | alpha=1.3 | 0.107 | 0.321 | 8.2 |

## Pareto frontier (core arm: max V, min frozen ratio, min latency)

- P3 pull (refine) W=7.5mo: V=0.304, frozen=0.269, latency=7.8
- P3 pull (refine) W=7mo: V=0.304, frozen=0.266, latency=7.5
- P3 pull W=8mo: V=0.304, frozen=0.262, latency=8.0
- P3 pull (refine) W=9mo: V=0.297, frozen=0.253, latency=8.3
- P3 pull W=6mo: V=0.288, frozen=0.273, latency=7.2
- P0 day_zero : V=0.286, frozen=0.237, latency=8.5

