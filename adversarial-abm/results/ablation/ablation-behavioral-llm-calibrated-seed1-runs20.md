# Ablation and sensitivity results

engine v0.5.0, population: behavioral-llm-calibrated, 20 runs, seed 1, arms: status_quo + core_v0_tutored_distributed_planning
intact reference: V=0.277±0.043, leak=0.010, visGap=0.006, sel=0.616, ratio vs status quo=2.19x

## Mechanism knock-outs (sorted by verified-value loss)

| knock-out | V | dV vs intact | leak | visGap | sel(theta) | ratio vs SQ |
|---|---:|---:|---:|---:|---:|---:|
| K10 ALL deterrence -> status quo | 0.110 | -0.167 | 0.053 | 0.040 | 0.616 | 0.87x |
| K6 planning vector -> central | 0.215 | -0.062 | 0.012 | 0.005 | 0.357 | 1.70x |
| K5 default layer -> salience | 0.235 | -0.042 | 0.011 | 0.003 | 0.174 | 1.85x |
| K1 fundingCaps OFF | 0.247 | -0.031 | 0.008 | 0.005 | 0.604 | 1.95x |
| K2 detection -> status quo (0.15) | 0.274 | -0.003 | 0.020 | 0.016 | 0.616 | 2.16x |
| K3 financial terms -> status quo | 0.275 | -0.002 | 0.016 | 0.010 | 0.616 | 2.17x |
| K4 reputational memory OFF | 0.277 | -0.001 | 0.012 | 0.007 | 0.616 | 2.18x |
| K9 herding brake OFF | 0.277 | -0.000 | 0.004 | 0.002 | 0.616 | 2.19x |
| K8 profile channel OFF | 0.310 | 0.033 | 0.013 | 0.002 | 0.620 | 2.44x |
| K7 delegation channel OFF | 0.326 | 0.048 | 0.010 | 0.007 | 0.620 | 2.57x |

## Parameter sweeps (cliff-hunting)

| parameter | value | V | leak | ratio vs SQ |
|---|---:|---:|---:|---:|
| detectionBase | 0.15 | 0.274 | 0.020 | 2.16x |
| detectionBase | 0.25 | 0.277 | 0.012 | 2.18x |
| detectionBase | 0.35 | 0.277 | 0.012 | 2.18x |
| detectionBase | 0.55 | 0.277 | 0.010 | 2.19x |
| detectionBase | 0.75 | 0.276 | 0.007 | 2.18x |
| opportunisticShare | 0.1 | 0.279 | 0.006 | 2.15x |
| opportunisticShare | 0.3 | 0.277 | 0.010 | 2.17x |
| opportunisticShare | 0.5 | 0.276 | 0.011 | 2.24x |
| opportunisticShare | 0.7 | 0.277 | 0.011 | 2.39x |
| distributedPlanningSignalMix | 0.2 | 0.206 | 0.000 | 1.63x |
| distributedPlanningSignalMix | 0.4 | 0.232 | 0.012 | 1.83x |
| distributedPlanningSignalMix | 0.66 | 0.277 | 0.010 | 2.19x |
| distributedPlanningSignalMix | 0.8 | 0.298 | 0.009 | 2.35x |
| delegationBlockSize | 1 | 0.279 | 0.010 | 2.20x |
| delegationBlockSize | 3 | 0.280 | 0.010 | 2.21x |
| delegationBlockSize | 10 | 0.279 | 0.017 | 2.20x |
| delegationBlockSize | 50 | 0.279 | 0.009 | 2.20x |
| socialProofWeight | 1 | 0.270 | 0.009 | 2.13x |
| socialProofWeight | 3 | 0.277 | 0.010 | 2.19x |
| socialProofWeight | 6 | 0.275 | 0.010 | 2.17x |

## Attacks

| attack | severity | V | dV vs intact | leak | sel(theta) | ratio vs SQ |
|---|---:|---:|---:|---:|---:|---:|
| fiscalizerCollusion | 0.15 | 0.277 | -0.001 | 0.010 | 0.616 | 2.25x |
| fiscalizerCollusion | 0.3 | 0.276 | -0.001 | 0.012 | 0.616 | 2.26x |
| fiscalizerCollusion | 0.5 | 0.276 | -0.001 | 0.012 | 0.616 | 2.27x |
| agendaCapture | 0.15 | 0.278 | 0.001 | 0.008 | 0.583 | 2.20x |
| agendaCapture | 0.3 | 0.244 | -0.033 | 0.008 | 0.429 | 1.93x |
| agendaCapture | 0.5 | 0.242 | -0.035 | 0.011 | 0.405 | 1.91x |
| coordinatedSignalBias | 0.1 | 0.281 | 0.003 | 0.003 | 0.616 | 2.21x |
| coordinatedSignalBias | 0.3 | 0.277 | 0.000 | 0.009 | 0.615 | 2.19x |
| coordinatedSignalBias | 0.5 | 0.271 | -0.007 | 0.005 | 0.614 | 2.14x |

