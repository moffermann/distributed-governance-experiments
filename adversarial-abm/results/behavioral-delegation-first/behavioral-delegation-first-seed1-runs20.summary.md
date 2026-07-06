scenario: behavioral-delegation-first v0.4 | engine: v0.5.0
runs: 20, base seed: 1, cycles: 24, citizens: 10000, projects: 40
centralPlanningSignalMix: 0.39, distributedPlanningSignalMix: 0.66
architectures: status_quo, participatory_weak_verification, participatory_weak_verification_full_budget, core_v0_tutored_central_planning, core_v0_tutored_distributed_planning

| architecture | budget spent | unspent | funded rate | actual value/budget | verified value/budget | reported value/budget | visibility gap | leakage | funding Gini | sel(value) | central plan corr | distributed plan corr | salience corr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| status_quo | 240000.000±0.000 | 0.000±0.000 | 0.334±0.027 | 0.420±0.061 | 0.128±0.019 | 0.470±0.053 | 0.050±0.031 | 0.088±0.053 | 0.705±0.022 | 0.288±0.150 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| participatory_weak_verification | 36432.000±0.000 | 0.848±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.000±0.000 | 0.691±0.016 | 0.000±0.000 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| participatory_weak_verification_full_budget | 240000.000±0.000 | 0.000±0.000 | 0.247±0.030 | 0.313±0.068 | 0.107±0.023 | 0.340±0.076 | 0.026±0.022 | 0.064±0.032 | 0.692±0.024 | 0.166±0.219 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| core_v0_tutored_central_planning | 240000.000±0.000 | 0.000±0.000 | 0.236±0.024 | 0.345±0.042 | 0.239±0.030 | 0.345±0.042 | 0.000±0.002 | 0.005±0.017 | 0.616±0.025 | 0.328±0.100 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| core_v0_tutored_distributed_planning | 240000.000±0.000 | 0.000±0.000 | 0.253±0.030 | 0.432±0.046 | 0.300±0.037 | 0.436±0.041 | 0.005±0.014 | 0.009±0.020 | 0.627±0.023 | 0.615±0.072 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
