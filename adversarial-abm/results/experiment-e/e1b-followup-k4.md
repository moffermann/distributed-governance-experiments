# E-1b follow-up: congestion attack surface at scarce capacity (K=4, staleness on)

| policy | adversary | V | leak | queue |
|---|---|---:|---:|---:|
| day_zero | blind | 0.226 | 0.0085 | 30.4 |
| day_zero | timing-aware | 0.226 | 0.0098 | 30.2 |
| pull W=7 | blind | 0.255 | 0.0095 | 8.8 |
| pull W=7 | timing-aware | 0.253 | 0.0101 | 8.8 |

Timing-awareness leak damage: day_zero +15%, pull +6%; V flat everywhere - the deterrence slack absorbs even floor-level stale detection.
