scenario: behavioral-high-friction v0.4 | engine: v0.5.1
runs: 20, base seed: 1, cycles: 24, citizens: 10000, projects: 40
centralPlanningSignalMix: 0.39, distributedPlanningSignalMix: 0.66
architectures: status_quo, participatory_weak_verification, participatory_weak_verification_full_budget, core_v0_tutored_mandated_agenda, core_v0_tutored_distributed_agenda

| architecture | budget spent | unspent | funded rate | actual value/budget | verified value/budget | reported value/budget | visibility gap | leakage | funding Gini | sel(value) | central plan corr | distributed plan corr | salience corr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| status_quo | 240000.000±0.000 | 0.000±0.000 | 0.334±0.027 | 0.423±0.061 | 0.127±0.018 | 0.469±0.054 | 0.047±0.028 | 0.080±0.040 | 0.705±0.022 | 0.288±0.150 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| participatory_weak_verification | 21144.000±0.000 | 0.912±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.714±0.015 | 0.000±0.000 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| participatory_weak_verification_full_budget | 240000.000±0.000 | 0.000±0.000 | 0.250±0.032 | 0.313±0.070 | 0.105±0.023 | 0.348±0.078 | 0.035±0.025 | 0.064±0.041 | 0.704±0.021 | 0.168±0.208 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| core_v0_tutored_mandated_agenda | 240000.000±0.000 | 0.000±0.000 | 0.284±0.026 | 0.394±0.052 | 0.274±0.039 | 0.397±0.052 | 0.003±0.008 | 0.010±0.017 | 0.654±0.024 | 0.298±0.137 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| core_v0_tutored_distributed_agenda | 240000.000±0.000 | 0.000±0.000 | 0.289±0.032 | 0.489±0.055 | 0.340±0.042 | 0.493±0.050 | 0.004±0.010 | 0.009±0.016 | 0.665±0.024 | 0.619±0.083 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
