# Distributed Governance — Computational Experiments

Satellite experiments workspace of the distributed governance research program. The master architecture corpus, the working paper, and the E1–E8 simulation suite live in [moffermann/distributed-governance-research](https://github.com/moffermann/distributed-governance-research); this repository holds the experiment programs that stress-test, calibrate, and extend that architecture computationally, and it is the working home of a planned second (satellite) paper.

Extracted from the master repository on 2026-07-06 with full git history (`experiments/` subtree), per the migration rule the workspace declared for itself.

## The experiment program

The program was conceived as a four-stage sequence:

```text
Experiment A — institutional architecture comparison   (adversarial-abm)
Experiment B — behavioral adoption and role formation  (behavioral-adoption-abm)
Experiment C — integrated A under B's populations      (adapter + integrated runs, complete)
Experiment D — calibration against real-world data     (pending; human instrument ready)
```

Two supporting programs feed A and B:

```text
planning-vector-construction   — how planning vectors are built (representative,
                                 distributed, Core v0 channels, trusted microdelegation);
                                 calibrates A's planning-signal mixes
planning-behavior-calibration  — behavioral elicitation instrument (LLM panels now,
                                 the identical human instrument later); calibrates B's priors
```

## Status table

| Experiment | Status | Key results |
|---|---|---|
| `adversarial-abm/` (A) | engine v0.5, audited; five attacks implemented; ablation program complete | `ENGINE_AUDIT_2026_07_06.md`, `RUN_2026_07_06_BEHAVIORAL_INTEGRATION_RESULTS.md`, `RUN_2026_07_06_ABLATION_RESULTS.md` |
| `behavioral-adoption-abm/` (B) | audited + Core v0 certified, end-to-end planning layer, LLM-calibrated | `CORE_V0_CONFORMANCE_AUDIT.md`, `RUN_2026_07_06_PLANNING_LAYER_RESULTS.md`, `RUN_2026_07_06_LLM_CALIBRATED_RESULTS.md` |
| Experiment C (A × B) | complete | mapping `behavioral-adoption-abm/OUTPUT_TO_ADVERSARIAL_ABM.md`; results in `adversarial-abm/RUN_2026_07_06_BEHAVIORAL_INTEGRATION_RESULTS.md` |
| `planning-vector-construction/` | executable, audited 2026-07-06, v0.5 results regenerated | `ENGINE_AUDIT_2026_07_06.md`, `results/core-v0-planning-channels/` |
| `planning-behavior-calibration/` | executable panel, 3 LLM runs (n=90 ×2 models, N=1000 weighted) | `RUN_2026_07_06_N1000_PANEL_RESULTS.md` |
| Experiment D | pending | human study protocol ready (`planning-behavior-calibration/HUMAN_STUDY_PROTOCOL.md`) |

## Headline findings so far

1. **The architecture ranking is behavioral-population-invariant** (Experiment C): under four behaviorally generated populations, Core v0 tutored-distributed delivers 2.0–2.7× the status quo's verified value per unit of budget, peaking under *low* adoption.
2. **Participation without a default layer is not a weaker architecture — it is a non-functioning one**: every realistic population drives the no-default participatory variant's verified delivery to zero.
3. **The attentive share is structural**: ~2.5–5% of citizens contribute explicit planning signals, regardless of prior source (synthetic, LLM n=90, LLM N=1000 weighted) — and it lands inside the range the planning-vector experiment had assumed.
4. **The master paper's participation assumptions were behaviorally realizable**: the imposed informed share (0.30) emerges at 0.309 from the LLM-calibrated population; the master's E8 (in the master repository) shows its headline surviving these populations at 2.26 [2.23, 2.30].
5. **The deterrence stack is individually redundant and jointly indispensable** (ablation program): removing any single term costs ≤ 0.003 in verified value; removing the whole stack collapses the architecture below the status quo (0.87×). The only attack that bites is capture of a *published* vector — a choke point that exists only in the tutored-with-mandated-agenda regime, so its price (−13% value, −35% selection) is evidence for distributed agenda construction, whose analog attack (coordinated signal corruption) is measured robust. No single-parameter sweep pushes the advantage below 1.63×.
6. **The semi-open transition is a dial, not a leap** (docs/110's first quantification): blended value rises monotonically and near-linearly with the envelope share — break-even near 8–10%, 1.5× at half the budget, 2.18× at full — so adoption can be gradual without a performance valley.

## Reading order

1. This README, then [`RESULTS.md`](RESULTS.md) (consolidated numbers with provenance and the run index) and [`TRACEABILITY_MATRIX.md`](TRACEABILITY_MATRIX.md) — every load-bearing concept mapped to its Core v0 anchor in the master corpus, plus the declared gaps. Figures with accessible textual descriptions: [`figures/FIGURES.md`](figures/FIGURES.md) (regenerate via `python tools/make_figures.py`).
2. Each experiment's own `README.md`.
3. Audits before results: `behavioral-adoption-abm/CORE_V0_CONFORMANCE_AUDIT.md`, `adversarial-abm/ENGINE_AUDIT_2026_07_06.md`, and `planning-vector-construction/ENGINE_AUDIT_2026_07_06.md` record what was corrected and certified in each engine.
4. `RUN_*.md` documents are dated records, newest supersedes; superseded ones carry forward pointers.

## Relationship to the master repository

- Core v0 (the architecture) is defined in the master corpus; experiments here conform to it and never redefine it — conformance audits cite the master's `docs/` resolutions (docs/101, docs/107, docs/108, and others) by name.
- The master's E8 experiment consumes `behavioral-adoption-abm/build_e8_inputs.py` output from this repository; its design and results live with the master paper's evidence suite.
- Experimental findings are simulation evidence — not institutional proof, not legal authorization, not empirical pilot validation.

## Reproduction quickstart

```bash
# Experiment A baseline (dependency-free Node.js)
node adversarial-abm/src/index.mjs --scenario adversarial-abm/scenarios/baseline-medium.json

# Experiment B sweep (Python stdlib; Mesa optional)
cd behavioral-adoption-abm && python run_sweep.py --seeds 10

# Experiment C: regenerate integrated scenarios from a fresh sweep
cd behavioral-adoption-abm && python build_adversarial_scenario.py --sweep outputs/expc-sweep/sweep_summary.json --source baseline --scenario-id behavioral-baseline

# LLM calibration panel (LM Studio or codex backend)
cd planning-behavior-calibration && python src/run_llm_panel.py --backend codex-exec --total-n 1000
```

All engines are deterministic under seed; behavioral results are byte-identical with and without Mesa.

## License

Code is MIT-licensed; documents and results are CC BY 4.0 — see [`LICENSE.md`](LICENSE.md).
