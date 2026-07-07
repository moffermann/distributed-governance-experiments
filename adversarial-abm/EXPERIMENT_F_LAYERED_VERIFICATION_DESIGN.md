# Experiment F — Layered Heterogeneous Machine Verification (pre-registered design)

Registered 2026-07-07, before any implementation or run. Author direction recorded in the master corpus (verification-throughput note, "Layered heterogeneous machine verification"). Candidate second satellite paper; results decide whether F becomes a section or a standalone paper.

**Sequencing (author instruction):** the local model layer is refreshed *before* the F-0 panel runs — latest Qwen family (Alibaba), latest available Gemma generation, and ideally DeepSeek as a third local family (open-weights distills allow a local, account-free option if hardware permits) — alongside **two hosted frontier families: the codex backend already in use, and Claude (Fable), added at the author's instruction** (headless CLI backend, mirroring the codex-exec pattern). The correlation measurement requires **at least three genuinely distinct model families**; the target panel is five.

**Orchestrator-as-subject disclosure.** The agent orchestrating this experiment program belongs to one of the tested families (Claude). The design neutralizes the judge-and-party surface mechanically: the vignette set with its ground-truth labels is committed *before* any panel run; every verdict is machine-scored against those labels with no orchestrator discretion; all families run the identical prompt protocol; and per-family model versions are recorded in provenance blocks. The orchestrator writes the instrument, not the grades.

## The question and its correction

Can layers of specialized machine agents — different engines per layer — replace first-instance fiscalization **entirely**, and at what confidence? The correction fixed in discussion and carried throughout: layers replace the *first instance* totally; the E-1d human floor (seeded controls, ensemble audit, the mandatory set, court-facing certification) is irreducible, because total replacement removes the instrument that measures the ensemble.

## F-0 — Empirical cross-engine error correlation (the models are the component under test)

Unlike the calibration panels (synthetic priors), F-0 measures the proposed component directly.

**Instrument.** ~120 evidence-case vignettes with known ground truth: ~60 clean, ~60 flawed across declared flaw classes — fabricated progress, metadata/date inconsistencies, wrong-location indicators, recycled evidence, quantity mismatches, plausible staged completion. Version 1 is text-structured evidence bundles (descriptions, metadata, dates, amounts, geo references, custody records); multimodal (imagery) is a declared later stage. Each case is judged by every model family: verdict (pass/flag), confidence, stated reason.

**Metrics.** Per-family false-pass and false-flag rates; pairwise error correlation (phi coefficient on error indicators, per flaw class); ensemble false-pass for k ∈ {1, 2, 3} under (a) measured correlation and (b) the independence prediction — the gap is the headline.

**Pre-registered predictions.**
- **PF0-1.** Independence is rejected: pairwise error correlation is substantially positive overall.
- **PF0-2.** A 2-layer heterogeneous ensemble beats the best single family, but by materially less than independence predicts.
- **PF0-3.** Correlation is flaw-class-structured: near zero on mechanical checks (metadata, arithmetic, date consistency), high on plausible-staging cases (the shared blind spot).

## F-1 — Layers vs confidence in the pipeline (engine extension)

Longitudinal engine gains multi-layer AI lanes: k layers, per-layer false-pass p_i, and a common-cause correlation model (with probability ρ a diverted milestone is *ensemble-blind* — passes every layer; otherwise layers draw independently). Ensemble gaming attacks the shared component (skill adds to the ensemble-blind mass). The deterrence coupling generalizes: opportunists anticipate the ensemble's end-to-end detection.

**Sweeps.** k ∈ {1, 2, 3, 4} × ρ ∈ {F-0's measured value, 0, 0.3, 0.6} × gaming {off, 0.35} at K scarce and calibrated, pull W\*=7, seeded controls on.

**Pre-registered predictions.**
- **PF1-1.** k\* ≈ 2–3: marginal verified-value and leak gains beyond the second heterogeneous layer are under 10% of the first layer's gain.
- **PF1-2.** Under high ρ, layer count beyond 2 is irrelevant — the ensemble-blind mass dominates.
- **PF1-3.** Seeded controls detect ensemble degradation at latency ∝ 1/(q·π) regardless of k, and measure ρ in passing (probe pass-pairs vs product of singles).
- **PF1-4.** With the intact deterrence stack, even the worst swept ensemble keeps the architecture's ranking (the E-1b robustness carries over).

## F-2 — The control-cost frontier (budget accounting)

The engines so far treat verification capacity as a constraint, not a cost. F-2 adds a control budget line: human verification cost per milestone (anchored to real supervision costs, 3–10% of project cost, swept), machine marginal cost (~0.1%, declared), seeded-control and human-floor costs, and an evidence-production premium per milestone for court-grade-by-construction evidence (attested provenance, trusted timestamps, custody records — swept). Output: **V per total budget** (delivery + control + evidence) across three regimes — pure human (E-1a baseline), triage (E-1c), full layered (F) — and the location of the new binding cost.

**Pre-registered predictions.**
- **PF2-1.** Full layering converts most of the human supervision share into delivered value: the V-per-total-budget gain is bounded by and close to the control share saved (single-digit percent), *on top of* the latency/congestion gains E-1a priced.
- **PF2-2.** The new binding control cost is evidence production; the floor of total control+evidence cost is set by the court-grade premium, not by verification labor.
- **PF2-3.** Below some evidence-premium threshold, the layered regime dominates triage at every K; above it, the premium eats the savings — a measurable crossover.

## Declared boundaries

- Text vignettes proxy multimodal evidence; measured ρ may understate real-world correlation on imagery (both directions argued: shared vision blind spots vs heterogeneous multimodal stacks). Declared, staged for later.
- No stack of models sees what is absent from the evidence: ground-truth anchoring (attested capture, sensors, citizen presence) is modeled only as the evidence premium, not simulated forensically.
- Court-grade properties are a cost line, not a simulated legal process; the legal adapter per jurisdiction is out of scope by the author's framing (technical grounds only).
- Panel provenance: F-0 verdicts are model behavior measurements — reproducible per pinned model versions; model updates change the measurement (versions recorded in provenance blocks, as in the calibration panels).
