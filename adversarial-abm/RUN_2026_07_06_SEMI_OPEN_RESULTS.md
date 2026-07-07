# Semi-Open Regime: First Quantification — 2026-07-06

The semi-open regime (master docs/110: a bounded mandated envelope on protocol autopilot, the fiscal parallel) had never been measured. This run traces the **transition path**: share `e` of the budget and a disjoint slice of the project pool run on Core v0's distributed machinery, the complement stays with the status quo, and per-budget value blends exactly by budget share. Engine v0.5.1, `behavioral-llm-calibrated` population on the envelope side, 20 runs, seed 1 (`src/semi_open.mjs`, results in `results/semi-open/`).

## The transition path

| envelope e | V(envelope) | V(complement) | V(blended) | vs pure status quo |
|---:|---:|---:|---:|---:|
| 0% | — | 0.127 | 0.127 | 1.00× |
| 5% | 0.016 | 0.128 | 0.123 | 0.97× |
| 10% | 0.196 | 0.127 | 0.134 | 1.06× |
| 20% | 0.243 | 0.125 | 0.149 | 1.17× |
| 35% | 0.274 | 0.125 | 0.177 | 1.40× |
| 50% | 0.269 | 0.118 | 0.193 | 1.52× |
| 75% | 0.286 | 0.108 | 0.242 | 1.91× |
| 100% | 0.276 | — | 0.276 | 2.18× |

## Findings

1. **The transition is a dial, not a leap.** Above the granularity floor, blended value improves monotonically in the envelope share — approximately linearly — with **no valley and no threshold**: a government can move from the status quo toward the open regime in increments, and every increment pays. Break-even sits near e ≈ 8–10%; half the budget in the envelope already yields 1.5×.
2. **The 5% cell is portfolio granularity, not regime failure.** At e = 5% the envelope holds two projects; with 3× scarcity, lumpy targets rarely complete within the horizon, so envelope value collapses (0.016). The practical reading matches the E7 municipal caveat: **minimum sensible envelopes contain enough projects to diversify completion risk** — in this configuration, roughly the 10% slice (4+ projects). A real deployment hits the same floor as a tiny pilot with two big works.
3. **The envelope reaches full-architecture performance early.** V(envelope) is already ≈ 0.27 from e = 35% — the machinery does not need the whole budget to work at full quality; what grows with e is the *share of budget enjoying it*.

## Declared boundaries

- The engine has never modeled a per-project authority veto stage, so tutored and semi-open differ here **only in envelope structure**; the decision-layer difference (veto vs automatic protocol approval) is not priced by this experiment and belongs to the agenda-setting study (docs/110's pending mechanism design).
- The ontological frontier is represented by a proportional random partition of the project pool (this engine's projects carry no category ontology); frontier-classification gaming is therefore out of scope here, as declared in docs/110's residuals.
- Envelope-side population is the LLM-calibrated one; complement-side behavior is the status quo's by construction.
