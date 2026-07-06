# Planning Vector Construction Results

scenario: core-v0-planning-channels v0.5
runs: 200, base seed: 42, citizens: 10000, targets: 80

| vector | class | mode | mandate | corr(latent) | top20 latent mean | priority gap | MSE | attentive | delegator | delegates | concentration | delegate quality | platform use | planning coverage | top1 delegate | top10 delegates |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| core_v0_open_mandated_participation | core_v0_planning | open | mandated_participation | 0.938±0.011 | 0.748±0.024 | 0.468±0.032 | 0.009±0.002 | 0.100±0.000 | 0.350±0.000 | 1800.000±0.000 | 0.080±0.000 | 0.854±0.000 | 0.850±0.000 | 0.600±0.000 | 0.001±0.000 | 0.011±0.000 |
| core_v0_tutored_distributed_mandated | core_v0_planning | tutored | mandated_participation | 0.907±0.017 | 0.740±0.024 | 0.452±0.032 | 0.013±0.003 | 0.080±0.000 | 0.240±0.000 | 950.000±0.000 | 0.120±0.000 | 0.792±0.000 | 0.780±0.000 | 0.550±0.000 | 0.003±0.000 | 0.022±0.000 |
| core_v0_open_institutional_delegate_emergence | core_v0_planning | open | none | 0.869±0.023 | 0.729±0.026 | 0.432±0.036 | 0.017±0.003 | 0.050±0.000 | 0.300±0.000 | 250.000±0.000 | 0.380±0.000 | 0.658±0.000 | 0.900±0.000 | 0.700±0.000 | 0.020±0.000 | 0.116±0.000 |
| core_v0_open_trusted_microdelegation | core_v0_planning | open | none | 0.861±0.024 | 0.727±0.027 | 0.429±0.035 | 0.018±0.004 | 0.050±0.000 | 0.350±0.000 | 1500.000±0.000 | 0.080±0.000 | 0.845±0.000 | 0.700±0.000 | 0.450±0.000 | 0.002±0.000 | 0.013±0.000 |
| core_v0_tutored_distributed_voluntary | core_v0_planning | tutored | enabled_voluntary | 0.844±0.027 | 0.722±0.028 | 0.419±0.036 | 0.020±0.004 | 0.050±0.000 | 0.180±0.000 | 650.000±0.000 | 0.160±0.000 | 0.763±0.000 | 0.680±0.000 | 0.400±0.000 | 0.004±0.000 | 0.033±0.000 |
| core_v0_open_mixed_trusted_delegation | core_v0_planning | open | none | 0.843±0.028 | 0.723±0.027 | 0.420±0.037 | 0.020±0.004 | 0.050±0.000 | 0.300±0.000 | 1000.000±0.000 | 0.140±0.000 | 0.787±0.000 | 0.680±0.000 | 0.420±0.000 | 0.003±0.000 | 0.022±0.000 |
| core_v0_open_plural_delegation_concentrated | core_v0_planning | open | none | 0.842±0.028 | 0.722±0.027 | 0.419±0.035 | 0.020±0.004 | 0.040±0.000 | 0.300±0.000 | 60.000±0.000 | 0.550±0.000 | 0.656±0.000 | 0.850±0.000 | 0.650±0.000 | 0.074±0.000 | 0.363±0.000 |
| core_v0_open_family_proxy_high_trust | core_v0_planning | open | none | 0.816±0.031 | 0.718±0.027 | 0.407±0.037 | 0.023±0.004 | 0.040±0.000 | 0.450±0.000 | 2200.000±0.000 | 0.050±0.000 | 0.862±0.000 | 0.650±0.000 | 0.350±0.000 | 0.001±0.000 | 0.009±0.000 |
| core_v0_open_low_attention_high_trusted_delegation | core_v0_planning | open | none | 0.815±0.031 | 0.718±0.027 | 0.406±0.037 | 0.023±0.004 | 0.020±0.000 | 0.400±0.000 | 1800.000±0.000 | 0.100±0.000 | 0.822±0.000 | 0.700±0.000 | 0.420±0.000 | 0.001±0.000 | 0.012±0.000 |
| central_high_alignment | representative |  |  | 0.650±0.054 | 0.708±0.034 | 0.328±0.042 | 0.044±0.008 |  |  |  |  |  |  |  |  |  |
| central_median_democracy | representative |  |  | 0.483±0.081 | 0.657±0.037 | 0.249±0.051 | 0.063±0.011 |  |  |  |  |  |  |  |  |  |
| central_median_global_south | representative |  |  | 0.432±0.089 | 0.639±0.041 | 0.222±0.055 | 0.069±0.012 |  |  |  |  |  |  |  |  |  |
| central_low_alignment | representative |  |  | 0.369±0.091 | 0.618±0.041 | 0.190±0.054 | 0.075±0.012 |  |  |  |  |  |  |  |  |  |
| central_very_low_alignment | representative |  |  | 0.341±0.088 | 0.607±0.038 | 0.176±0.053 | 0.079±0.013 |  |  |  |  |  |  |  |  |  |
| central_crisis_legitimacy | representative |  |  | 0.315±0.096 | 0.600±0.042 | 0.155±0.061 | 0.081±0.013 |  |  |  |  |  |  |  |  |  |
| salience_vector | salience |  |  | 0.187±0.107 | 0.572±0.042 | 0.101±0.062 | 0.114±0.017 |  |  |  |  |  |  |  |  |  |
