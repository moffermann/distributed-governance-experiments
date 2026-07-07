# Semi-open regime: the transition path (first quantification)

engine v0.5.1, population: behavioral-llm-calibrated (envelope side), 20 runs, seed 1
Blend: V = e*V(core distributed | envelope slice) + (1-e)*V(status quo | complement); per-budget metrics blend exactly by budget share.

| envelope share e | V(envelope) | V(complement) | V(blended) | vs pure status quo |
|---:|---:|---:|---:|---:|
| 0% | — | 0.127 | 0.127 | 1.00x |
| 5% | 0.016 | 0.128 | 0.123 | 0.97x |
| 10% | 0.196 | 0.127 | 0.134 | 1.06x |
| 20% | 0.243 | 0.125 | 0.149 | 1.17x |
| 35% | 0.274 | 0.125 | 0.177 | 1.40x |
| 50% | 0.269 | 0.118 | 0.193 | 1.52x |
| 75% | 0.286 | 0.108 | 0.242 | 1.91x |
| 100% | 0.276 | — | 0.276 | 2.18x |

