# Per-family decoding configuration (disclosed)

Review round 2 (evals E3, repro2 O1) flagged that the panel's decoding is not uniform across families and was under-disclosed. It cannot be made fully uniform — the thinking models emit empty or malformed JSON under a temperature-0 grammar constraint, and Gemma 4 falls into repetition loops at temperature 0 — so the honest resolution is full disclosure and a family+recommended-decoding framing, not a false claim of identical sampling.

| family | backend | temperature | format constraint | notes |
|---|---|---|---|---|
| gpt-5.5 | codex exec | provider-controlled | JSON schema (strict) | `model_reasoning_effort=low` |
| Claude (Fable) | `claude -p` | provider default | none (last-JSON parse) | full reasoning |
| gemma4:26b | ollama HTTP | **0.2** (+ repeat_penalty 1.15) | JSON mode | temp-0 repetition loops on a minority of bundles; anti-loop sampling required |
| qwen3.6:35b-a3b | ollama HTTP | 0 | JSON mode, **thinking off** | emits empty JSON under grammar constraint with thinking on |
| deepseek-r1:14b | ollama HTTP | **0.6** | **none**, num_predict 2500, last-JSON parse | r1 distills loop at temp 0 and echo inputs under grammar constraint; vendor-recommended 0.5–0.7 |

**Consequence for interpretation:** family effect and decoding effect are partially aliased. The single worst verifier (deepseek, highest false-pass) is also the only unconstrained, highest-temperature family. Cross-family comparisons are therefore reported as **family + recommended decoding**, not as a controlled sampler comparison, and the correlation/ranking claims are treated as exploratory (see the paper's Finding 7 and the statistical annex). No high-temperature "rescue" pass is used in the v3 re-run; loop-resistant cases are recorded as a no-verdict category rather than re-sampled at a third configuration.
