scenario: baseline-medium v0.4 | engine: v0.5.0
runs: 20, base seed: 1, cycles: 24, citizens: 10000, projects: 40
centralPlanningSignalMix: 0.39, distributedPlanningSignalMix: 0.66
architectures: status_quo, participatory_weak_verification, participatory_weak_verification_full_budget, core_v0_tutored_central_planning, core_v0_tutored_distributed_planning

| architecture | budget spent | unspent | funded rate | actual value/budget | verified value/budget | reported value/budget | visibility gap | leakage | funding Gini | sel(value) | central plan corr | distributed plan corr | salience corr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| status_quo | 240000.000±0.000 | 0.000±0.000 | 0.334±0.027 | 0.420±0.061 | 0.128±0.019 | 0.470±0.053 | 0.050±0.031 | 0.088±0.053 | 0.705±0.022 | 0.288±0.150 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| participatory_weak_verification | 72000.000±0.000 | 0.700±0.000 | 0.030±0.022 | 0.087±0.077 | 0.029±0.025 | 0.100±0.083 | 0.013±0.027 | 0.016±0.029 | 0.772±0.010 | 0.108±0.139 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| participatory_weak_verification_full_budget | 240000.000±0.000 | 0.000±0.000 | 0.247±0.031 | 0.311±0.068 | 0.104±0.023 | 0.349±0.079 | 0.038±0.028 | 0.069±0.038 | 0.693±0.024 | 0.172±0.215 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| core_v0_tutored_central_planning | 240000.000±0.000 | 0.000±0.000 | 0.209±0.031 | 0.307±0.052 | 0.214±0.036 | 0.310±0.050 | 0.003±0.008 | 0.005±0.012 | 0.595±0.031 | 0.401±0.099 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
| core_v0_tutored_distributed_planning | 240000.000±0.000 | 0.000±0.000 | 0.223±0.037 | 0.378±0.072 | 0.262±0.052 | 0.380±0.073 | 0.002±0.006 | 0.002±0.007 | 0.604±0.027 | 0.610±0.093 | 0.459±0.114 | 0.829±0.056 | 0.188±0.185 |
