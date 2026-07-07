# F-3 / F-4: the cascade vs measured AI failures; contraposition coverage (engine v0.10.0)

pull W*=7, 20 runs, seed 1; operating points from F-0 v2 (evidence-rich bundles)

## F-3: measured operating points x stack integrity

| stack | verifier (measured) | V | leak | diversion attempts | detections |
|---|---|---:|---:|---:|---:|
| intact | pure human (reference) | 0.304 | 0.0056 | 1.2 | 0.8 |
| intact | claude single (best measured) | 0.296 | 0.0047 | 1.1 | 0.9 |
| intact | deepseek single (worst measured) | 0.307 | 0.0052 | 1.2 | 0.7 |
| intact | deepseek+claude pair (measured rho) | 0.305 | 0.0020 | 0.6 | 0.5 |
| degraded (docs/111 violation) | pure human (reference) | 0.114 | 0.0568 | 11.7 | 3.1 |
| degraded (docs/111 violation) | claude single (best measured) | 0.118 | 0.0598 | 12.1 | 3.6 |
| degraded (docs/111 violation) | deepseek single (worst measured) | 0.117 | 0.0608 | 12.3 | 3.5 |
| degraded (docs/111 violation) | deepseek+claude pair (measured rho) | 0.118 | 0.0525 | 11.4 | 3.5 |

## F-4: contraposed independent evidence (coverage sweep; catch=0.8 declared)

| coverage | verifier | V | leak | diversion attempts |
|---:|---|---:|---:|---:|
| 0% | claude single | 0.296 | 0.0047 | 1.1 |
| 10% | claude single | 0.299 | 0.0035 | 0.9 |
| 25% | claude single | 0.299 | 0.0044 | 1.0 |
| 50% | claude single | 0.302 | 0.0020 | 0.7 |
| 75% | claude single | 0.307 | 0.0009 | 0.3 |
| 100% | claude single | 0.308 | 0.0006 | 0.3 |

| coverage | verifier (degraded stack) | V | leak | diversion attempts |
|---:|---|---:|---:|---:|
| 0% | claude single | 0.118 | 0.0598 | 12.1 |
| 50% | claude single | 0.123 | 0.0165 | 4.7 |
| 100% | claude single | 0.123 | 0.0030 | 1.1 |

