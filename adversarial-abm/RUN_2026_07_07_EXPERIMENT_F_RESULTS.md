# Experiment F Results: Layered Heterogeneous Machine Verification — 2026-07-07

Pre-registered in [`EXPERIMENT_F_LAYERED_VERIFICATION_DESIGN.md`](EXPERIMENT_F_LAYERED_VERIFICATION_DESIGN.md). Three parts: F-0 (empirical five-family evidence-judgment panel; instrument committed before any run), F-1 (layers vs confidence, engine v0.9; single-layer path and the v0.6–v0.8 anchor reproduce exactly), F-2 (control-cost frontier). Panel: gemma4:26b, qwen3.6:35b-a3b, deepseek-r1:14b (local, ollama HTTP API), gpt-5.5 (codex exec), Claude Fable (claude headless) — 120 vignettes each, 600 verdicts total, ground truth never sent, machine-scored. Raw artifacts: `evidence-panel/` (F-0), `results/experiment-f/` (F-1, F-2).

## F-0 headline 1: at mechanically-checkable difficulty, fraud detection is solved — the instrument's fraud side is degenerate

Every family catches essentially every flaw: false-pass 0.000 for gemma, qwen, gpt, and claude across all six flaw classes; deepseek alone lets 5% through (10% on three classes). Every 2-stack and 3-stack records a measured ensemble false-pass of exactly 0.000. Consequence, stated honestly: **the pre-registered correlation measurements on the fraud side are not testable at this instrument difficulty** — there are no shared errors to correlate. The vignette flaws (dates before start, geotags in another city, duplicate hashes, over-target invoices — and even the "plausible staging" class predicted as the shared blind spot) sit below the detection floor of current frontier and local models. A harder instrument (subtler fraud) is the named follow-up; PF0-1, PF0-2, and PF0-3 are recorded as **not-testable-in-range**, not as confirmed.

## F-0 headline 2 (the unpredicted finding): the binding failure is specificity, and it varies 6× across families

On the sixty *clean* bundles, the same strict prompt produces wildly different operating points:

| family | false-flag rate on clean work |
|---|---:|
| gemma4:26b | **0.167** |
| deepseek-r1:14b | 0.317 |
| gpt-5.5 | 0.767 |
| claude (Fable) | 0.950 |
| qwen3.6:35b-a3b | **1.000** — flags everything |

False-flag correlation is near zero or negative among local families and **0.416 between the two hosted frontier models** — shared conservatism is a hosted-frontier trait in this panel, not a universal one. Operational reading through the E-1c triage lens: lane-a auto-release requires the verifier to *pass* honest work; with false-flag rates of 77–100%, the auto-release lane collapses and the capacity gain evaporates. An any-flag-refers ensemble multiplies the problem (gemma+deepseek ≈ 43% honest referrals; add claude ≈ 97%). **The layered-verification design problem is not catching fraud — it is learning to pass honesty.**

## Design consequences (adopted into the corpus direction, pending author verdict)

1. **Layer composition must be specificity-first**: the first (auto-release) layer needs a calibrated-permissive verifier (gemma-class here); strict families (claude, gpt) belong in the *referral* lane, where conservatism is a feature.
2. **Operating points are calibratable, and the calibrator already exists**: E-1d's seeded controls (clean and flawed probes) are exactly the instrument that measures each family's false-flag/false-pass operating point in production — the same q-knob now calibrates specificity, closing the loop between E-1d and F.
3. **Layering buys little against mechanical fraud** (one model suffices) and **costs referral load multiplicatively**; its residual value concentrates on whatever fraud classes clear layer 1 — unmeasurable until the harder instrument exists.

## F-1: layers vs confidence (engine v0.9, swept correlation)

With the intact stack, verified value is flat in k everywhere; the signal is leakage and referral load. Under **independent errors** (ρ=0) the second layer cuts leakage ~25% (0.0040 → 0.0030) and the third adds nothing — **k\* = 2**. At **ρ = 0.3 the layer benefit disappears entirely** (leak 0.0050 → 0.0054 → 0.0056 across k), and ensemble gaming (which attacks the shared mass) passes every layer equally at any k. Each layer costs referral load (human verifications 1.9 → 2.7/cycle as false flags accumulate — now empirically grounded by F-0's specificity data). The layered drift cell reproduces E-1d's blindness (latency 47.3 of a 48-cycle censoring horizon): **seeded controls remain the epistemic instrument at every k**. The pre-registered measured-ρ cell could not run: fraud-side ρ is unmeasurable on the degenerate instrument (declared); the swept-ρ results carry the conclusion, and F-0's false-flag structure suggests real-world effective ρ is family-pairing-dependent.

- **PF1-1 confirmed** (k\*≈2 under independence, marginal gains <10% beyond); **PF1-2 confirmed strongly** (benefit dies by ρ=0.3, not only at high ρ); **PF1-3 confirmed in its E-1d form** (passive sampling blind at any k); **PF1-4 confirmed** (worst swept ensemble keeps the ranking).

## F-2: the control-cost frontier

Adding the control budget line the engines never had (human supervision at 3/6/10% of tranche per milestone-verification; machine at 0.1%; court-grade evidence premium at 0.5/2/5%):

- Pure-human control+evidence costs **3.3–14.3% of the delivery budget**; any machine regime cuts it to **1.7–9.4%**, lifting verified value per *total* budget by up to ~3 points (0.266 → 0.293 at h=10%) — **PF2-1 confirmed** (gain ≈ the control share saved, on top of E-1a's congestion gains).
- In machine regimes the dominant remaining cost line is the **evidence premium** (at e=5% it accounts for most of the 6.2–6.4% total) — **PF2-2 confirmed**: the binding control cost relocates to court-grade evidence production.
- **PF2-3 refuted-informative**: no layered-vs-triage crossover exists — the second layer is economically neutral (differences within noise at every h, e, K); the economically meaningful step is human → *any* machine regime. Combined with F-0's specificity data, the second layer's real price is referral load, not money.

## Provenance and declared deviations

Per-family decoding configs differ and are recorded: gpt/claude/qwen at temperature 0 (qwen with thinking disabled — thinking models emit empty JSON under grammar constraint); gemma4 at temperature 0.2 with repetition penalty 1.15 (temperature-0 repetition loops on a minority of bundles; four loop-resistant cases rescued at 0.7–1.0, verdicts recorded with a rescue note); deepseek-r1 at temperature 0.6 with natural thinking and no grammar constraint (r1 distills loop at temperature 0 and echo inputs under constraint — vendor-consistent settings). The deepseek Qwen-backbone validation probe (elevated correlation expected by shared lineage) was **not evaluable**: qwen produced zero variance on both error sides. Model versions pinned in `evidence-panel/results/*.jsonl`; the orchestrator-as-subject disclosure and its mechanical neutralization are in the design document — and the orchestrator's own family (Claude) recorded the *second-worst* specificity in the panel, which the scoring machinery reported without discretion, as designed.

## Boundaries

- Text-structured vignettes; multimodal evidence (imagery) untested — both the fraud floor and the specificity spread could move.
- One fixed strict prompt (pre-registered); operating points are prompt-sensitive, and calibrating them is a deployment act (via seeded controls), not a model property.
- The fraud-side degeneracy bounds what this panel can say about ensemble correlation under *hard* fraud; instrument v2 (subtler flaws, adversarially constructed) is the named follow-up before any corpus formalization of layer counts.
