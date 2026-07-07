# Experiment E-1b: adaptive adversaries (engine v0.8.0)

core arm, pull W*=7 unless noted; staleness {rate 0.06, floor 0.4}; AI {pi 0.7, fp 0.05, s 0.05}; 20 runs, seed 1

## Part A: congestion as attack surface (release policy as security parameter)

| policy | staleness | adversary | V | leak | queue | detections |
|---|---|---|---:|---:|---:|---:|
| pull W=7 | off | blind | 0.304±0.015 | 0.006 | 1.2 | 0.8 |
| pull W=7 | on | blind | 0.304±0.015 | 0.006 | 1.2 | 0.8 |
| pull W=7 | on | timing-aware | 0.304±0.015 | 0.006 | 1.2 | 0.8 |
| day_zero | off | blind | 0.286±0.019 | 0.005 | 5.6 | 1.0 |
| day_zero | on | blind | 0.286±0.019 | 0.005 | 5.6 | 1.0 |
| day_zero | on | timing-aware | 0.286±0.019 | 0.005 | 5.6 | 1.0 |

Timing-awareness damage dV(blind - aware): pull = 0.000, day_zero = 0.000

## Part B: evidence gaming x stack integrity

| stack | verification | V | leak | detections |
|---|---|---:|---:|---:|
| intact | pure human | 0.304±0.015 | 0.006 | 0.8 |
| intact | AI fp=0.05 | 0.306±0.024 | 0.004 | 0.9 |
| intact | AI + gaming 0.35 | 0.306±0.025 | 0.005 | 1.3 |
| intact | AI + gaming 0.55 | 0.302±0.020 | 0.010 | 1.1 |
| degraded (docs/111 violation) | pure human | 0.114±0.008 | 0.057 | 3.1 |
| degraded (docs/111 violation) | AI fp=0.05 | 0.118±0.008 | 0.052 | 3.5 |
| degraded (docs/111 violation) | AI + gaming 0.35 | 0.115±0.010 | 0.063 | 3.1 |
| degraded (docs/111 violation) | AI + gaming 0.55 | 0.115±0.009 | 0.060 | 3.1 |

## Part C: reputation compounding over 8 years (V and leak per year, per annual budget)

| compounding | V y1 | V y2 | V y3 | V y4 | V y5 | V y6 | V y7 | V y8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| on | 0.285 | 0.306 | 0.310 | 0.314 | 0.303 | 0.319 | 0.308 | 0.320 |
| off | 0.285 | 0.304 | 0.312 | 0.300 | 0.305 | 0.320 | 0.302 | 0.301 |

| compounding | leak y1 | leak y2 | leak y3 | leak y4 | leak y5 | leak y6 | leak y7 | leak y8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| on | 0.0033 | 0.0058 | 0.0058 | 0.0064 | 0.0055 | 0.0047 | 0.0074 | 0.0091 |
| off | 0.0033 | 0.0063 | 0.0042 | 0.0068 | 0.0009 | 0.0050 | 0.0077 | 0.0085 |

