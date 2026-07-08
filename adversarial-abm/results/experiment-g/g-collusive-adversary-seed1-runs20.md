# Experiment G: collusive/adaptive adversary (engine v0.12.0)

core arm w/ AI triage (pi 0.7, fp 0.05) + contraposition 50%; pull W*=7; 20 runs, seed 1; status-quo reference V=0.112

## Collusion sweep (intact stack, AI triage + 50% contraposition)

| collusion rate | V | leak | diversion attempts | V vs status quo |
|---:|---:|---:|---:|---:|
| 0% | 0.304 | 0.0021 | 0.6 | 2.72x |
| 5% | 0.296 | 0.0081 | 1.8 | 2.65x |
| 10% | 0.298 | 0.0090 | 2.1 | 2.67x |
| 20% | 0.295 | 0.0244 | 4.8 | 2.64x |
| 35% | 0.286 | 0.0467 | 9.2 | 2.56x |
| 50% | 0.286 | 0.0522 | 9.9 | 2.56x |

**PG6 crossover (advantage inverts, ratio→1):** not reached in [0, 0.5] — advantage survives the whole range

## PG3: contraposition rescue of a broken stack — non-colluding vs colluding

| stack | contraposition | collusion | V | leak |
|---|---|---:|---:|---:|
| degraded | 0% | 0% | 0.118 | 0.0525 |
| degraded | 50% | 0% | 0.120 | 0.0169 |
| degraded | 50% | 20% | 0.119 | 0.0333 |
| degraded | 100% | 20% | 0.122 | 0.0283 |

## PG1 adaptive targeting & PG4 anchor poisoning (intact stack)

| attack | param | V | leak |
|---|---|---:|---:|
| adaptive targeting | gain 0.1 | 0.308 | 0.0042 |
| adaptive targeting | gain 0.25 | 0.308 | 0.0066 |
| adaptive targeting | gain 0.4 | 0.304 | 0.0080 |
| anchor poisoning | 25% detection loss | 0.306 | 0.0055 |
| anchor poisoning | 50% detection loss | 0.306 | 0.0077 |
| anchor poisoning | 75% detection loss | 0.301 | 0.0153 |

