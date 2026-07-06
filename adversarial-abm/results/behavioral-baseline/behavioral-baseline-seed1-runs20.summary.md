scenario: behavioral-baseline v0.4 | engine: v0.5.0
runs: 20, base seed: 1, cycles: 24, citizens: 10000, projects: 40
centralPlanningSignalMix: 0.39, distributedPlanningSignalMix: 0.66
architectures: status_quo, participatory_weak_verification, participatory_weak_verification_full_budget, core_v0_tutored_central_planning, core_v0_tutored_distributed_planning

| architecture | budget spent | unspent | funded rate | actual value/budget | verified value/budget | reported value/budget | visibility gap | leakage | funding Gini | sel(value) | central plan corr | distributed plan corr | salience corr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| status_quo | 240000.000±0.000 | 0.000±0.000 | 0.334±0.027 | 0.428±0.060 | 0.127±0.016 | 0.472±0.058 | 0.044±0.027 | 0.074±0.035 | 0.705±0.022 | 0.288±0.150 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| participatory_weak_verification | 32016.000±0.000 | 0.867±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.703±0.015 | 0.000±0.000 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| participatory_weak_verification_full_budget | 240000.000±0.000 | 0.000±0.000 | 0.246±0.034 | 0.313±0.066 | 0.104±0.023 | 0.339±0.074 | 0.026±0.018 | 0.047±0.031 | 0.696±0.024 | 0.167±0.213 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| core_v0_tutored_central_planning | 240000.000±0.000 | 0.000±0.000 | 0.241±0.023 | 0.333±0.056 | 0.231±0.040 | 0.337±0.057 | 0.004±0.011 | 0.009±0.022 | 0.626±0.023 | 0.314±0.134 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| core_v0_tutored_distributed_planning | 240000.000±0.000 | 0.000±0.000 | 0.260±0.037 | 0.442±0.050 | 0.307±0.038 | 0.446±0.051 | 0.004±0.008 | 0.009±0.016 | 0.634±0.023 | 0.612±0.080 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
