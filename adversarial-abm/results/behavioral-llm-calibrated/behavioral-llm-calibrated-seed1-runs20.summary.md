scenario: behavioral-llm-calibrated v0.4 | engine: v0.5.1
runs: 20, base seed: 1, cycles: 24, citizens: 10000, projects: 40
centralPlanningSignalMix: 0.39, distributedPlanningSignalMix: 0.66
architectures: status_quo, participatory_weak_verification, participatory_weak_verification_full_budget, core_v0_tutored_mandated_agenda, core_v0_tutored_distributed_agenda

| architecture | budget spent | unspent | funded rate | actual value/budget | verified value/budget | reported value/budget | visibility gap | leakage | funding Gini | sel(value) | central plan corr | distributed plan corr | salience corr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| status_quo | 240000.000±0.000 | 0.000±0.000 | 0.334±0.027 | 0.421±0.063 | 0.127±0.018 | 0.468±0.054 | 0.047±0.028 | 0.084±0.048 | 0.705±0.022 | 0.288±0.150 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| participatory_weak_verification | 36984.000±0.000 | 0.846±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.696±0.016 | 0.000±0.000 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| participatory_weak_verification_full_budget | 240000.000±0.000 | 0.000±0.000 | 0.247±0.030 | 0.307±0.069 | 0.103±0.024 | 0.343±0.071 | 0.036±0.025 | 0.066±0.040 | 0.693±0.023 | 0.166±0.219 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| core_v0_tutored_mandated_agenda | 240000.000±0.000 | 0.000±0.000 | 0.225±0.026 | 0.322±0.048 | 0.224±0.034 | 0.324±0.049 | 0.002±0.010 | 0.008±0.020 | 0.599±0.027 | 0.361±0.121 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| core_v0_tutored_distributed_agenda | 240000.000±0.000 | 0.000±0.000 | 0.236±0.036 | 0.401±0.055 | 0.277±0.040 | 0.408±0.056 | 0.007±0.019 | 0.009±0.023 | 0.616±0.023 | 0.616±0.081 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
