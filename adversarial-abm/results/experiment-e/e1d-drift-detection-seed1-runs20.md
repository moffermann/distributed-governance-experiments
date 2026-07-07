# E-1d: drift-detection latency of passive sampling (engine v0.8.0)

drift: falsePass +0.03/cycle from cycle 24; horizon 72 cycles (latency censored at 48); pull W=7; AI pi=0.7 fp=0.05; 20 runs, seed 1

| sample rate s | latency (cycles, censored@48) | V | leak |
|---:|---:|---:|---:|
| 0.02 | 48.0 ± 0.0 | 0.309 | 0.0039 |
| 0.05 | 48.0 ± 0.0 | 0.309 | 0.0039 |
| 0.15 | 43.5 ± 11.6 | 0.309 | 0.0037 |
| no drift (s=0.05) | — | 0.311 | 0.0034 |

