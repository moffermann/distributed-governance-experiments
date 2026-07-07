# Experiment F-0 v2 Results: Subtle Fraud — 2026-07-07

Authorized follow-up to F-0 (instrument committed before any run: `evidence-panel/vignettes_v2.json`, seed 20260708). Same five families, same strict prompt, 120 new cases whose fraud requires judgment: prices inflated against an in-bundle market reference, implausibly compressed timelines, photo coverage clustered on two early days, captions contradicting certified quantities, vendor–supervisor shared addresses, and threshold structuring. Coverage: gemma 118, qwen 116, deepseek 120, gpt 120, claude 120 (a handful of temperature-loop stragglers declared).

## Headline 1: subtle fraud finally separates the families — and the correlation story exists

| family | false-pass (subtle fraud) | false-flag (clean) |
|---|---:|---:|
| qwen3.6 | 0.000 (trivial — it approves nothing) | **1.000** |
| gpt-5.5 | 0.033 | 0.800 |
| claude | 0.083 | **0.050** |
| gemma4 | 0.119 | 0.458 |
| deepseek-r1 | 0.217 | 0.317 |

**PF0-1 — now testable, and confirmed**: pairwise false-pass correlations are positive (deepseek–claude φ=0.427, gpt–claude 0.280, gemma–claude 0.265, gemma–deepseek 0.184; gemma–gpt mildly negative). **PF0-2 — confirmed**: measured 2-stack ensemble false-passes run **1.9×–6.0× worse than the independence prediction** (gpt+claude 6.0×; deepseek+claude 3.7×; gemma+claude 3.4×) — heterogeneous stacks help, but far less than naive multiplication promises. **PF0-3 — confirmed in structure**: flaw classes with an in-bundle objective reference (inflated prices vs the included market benchmark; caption-vs-certificate quantity contradictions) sit at ~0% false-pass for everyone, while the judgment classes carry all the errors and the correlation — with **compressed timelines as the shared blind spot** (10–50% false-pass across families; world knowledge about how long works take is the panel's collective weakness).

## Headline 2 (the surprise): evidence richness moves the operating point more than the model does

Claude went from **95% false-flags on v1 cleans to 5% on v2 cleans** — same model, same strict prompt. The difference: v2 bundles carry *objective comparison anchors* (a market price reference, an approval threshold, unit prices, line items, registries). Given something concrete to check against, the strict model stops guessing and starts comparing — paranoia becomes judgment. gemma moved the other way (17% → 46%: the same anchors gave it more things to worry about), gpt stayed hair-triggered (77% → 80%), qwen stayed deny-all (100% → 100%).

Design consequence, adopted into the direction: **the evidence contract should include the comparison references, not just the probative properties** — market benchmarks, typical-duration bands, thresholds. "Court-grade by construction" extends to *judgeable by construction*. This is the cheapest specificity lever found in the whole program: richer bundles beat both prompt calibration (80%→27% on gpt) and model choice for at least one frontier family.

## Headline 3: what layer composition survives the data

- Any-flag ensembles multiply false-flags (adding gpt to any L1 pushes honest referrals near 80%+); qwen is unusable in any role (deny-all under both instruments).
- The best measured single operating point is **claude on rich bundles (5% ff / 8.3% fp)**; the best anti-correlated pair is **gemma+gpt (measured joint false-pass 0.000, φ=−0.07)** — but at ~89% combined honest-referral cost.
- Practical rule confirmed: **one calibrated permissive layer for auto-release** (on evidence-rich bundles), the strict family as referee on referrals and high-stakes categories only, operating points measured per family with seeded controls, and layer 2 reserved for the judgment classes where correlation is lowest. The k\*=2 of F-1 survives, with composition and evidence richness doing most of the work.

## Prediction accounting update

PF0-1 confirmed (v2), PF0-2 confirmed (v2), PF0-3 confirmed-in-structure (v2, with compressed timelines replacing "plausible staging" as the shared blind spot); the v1 not-testable verdicts stand for the v1 instrument and are superseded in force by v2. The deepseek Qwen-backbone validation probe remains unevaluable (qwen zero-variance in both instruments). Calibration probe (same date): gpt's operating point moved 80%→27% false-flags by instruction alone at a recall cost (97%→85%) — the curve is steerable; the point is chosen, not given.

## Boundaries

- Text-structured bundles; multimodal untested. One strict prompt (pre-registered); the v1↔v2 operating-point shifts show instrument richness is a confound to *control for* in any future panel — declared.
- Compressed-timeline world knowledge may improve rapidly across model generations; the correlation structure is a 2026 snapshot with pinned versions.
- Stragglers: 2 gemma and 4 qwen loop-resistant cases excluded after rescue attempts (deepseek completed all 120); coverage declared per family in the header.
