# Satellite Paper Roadmap — Computational Experiments (A–G)

Working title (to refine): **Adversarial and Behavioral Agent-Based Simulation for Public Resource Allocation: Stress-Testing Governance Architectures with Endogenous Participation**.

Strategic frame (author decision, 2026-07-06, recorded in the master's v1.9 queue): this paper absorbs the computational program so the master paper can cite instead of contain, shrinking rather than growing.

## Current state (2026-07-07)

- **Draft v0.5** published: doi:10.5281/zenodo.21249060 (concept 10.5281/zenodo.21246089), GitHub release v0.5. Eight findings (F1–F6 mature; F7 machine verification rebuilt after a review-round-2 construct bug and framed as directional; F8 collusive adversary, new and pessimistic-by-construction).
- **Two internal adversarial review rounds** applied and reported in the paper: round 1 (`drafts/REVIEW_ROUND_1.md`), round 2 (`drafts/REVIEW_ROUND_2.md`, five archetypes). Both are single-ecosystem process discipline, not independent validation.
- **Engines** at v0.11 (longitudinal) / v0.5.1 (static); anchor V=0.303844218531 bit-stable v0.6→v0.11; Mesa dock 15/15; `predictions.csv` at 42 rows; `tools/reproduce_all.py` covers all deterministic E/F/G cells + panel scoring (only live-model panel runs excluded).

## Corrections applied in v0.5 (from review round 2)

1. **Construct bug fixed** — the F-0 v2 clean bundles carried an unapproved above-threshold item; the de-leaked v3 instrument (`generate_vignettes_v3.py`) attaches approvals, and the false-flag half was rebuilt (gpt 0.80→0.03). The temperament-spread and evidence-richness-rescue claims are **withdrawn** as artifacts.
2. **Confidence intervals everywhere** — Wilson on rates, Fisher exact + bootstrap on correlations/ratios; qwen excluded from correlation stats (degenerate); correlations demoted to exploratory/underpowered.
3. **F-3/F-4 relabeled** as stipulated-mechanism sensitivities (not "measured"); the measured-pair→engine mapping disclosed as a moment-matched reduced form.
4. **Scope-limited** (fiscalizer): document-legible delivery-phase fraud only; "court-grade"→"tamper-evident"; human-touch flagged as project-count over-count of the value-weighted share; coverage selection unpublished.
5. **Decoding disclosed** (`DECODING.md`), high-temperature rescues dropped, no-verdict category added; per-family N reported (not a nominal 600).
6. **Ratio CIs** (Fieller + bootstrap, `RATIO_CIS.md`); lapsing-funds annuality variant; reproduce_all + stamp refresh.

## Improvement points (named, for the venue revision)

- **Power**: the F-0 correlation claims need ~10× the flawed cases before any ρ is quotable — the current n≈60 supports only "one of five 2-stacks separable from independence." A larger vignette set is the single biggest F-7 upgrade.
- **Within-instrument evidence-richness manipulation**: the "references make verifiers judge" claim is currently a cross-instrument/probe hypothesis; run the *same* vignettes with and without comparison anchors to make it a controlled result.
- **Second frontier-scale family** for the N=1000 calibration panel (currently single-family; the cross-family check is only at n=90) and for F-0 (currently the two frontier models are one hosted pair).
- **Fixed-decoding sensitivity**: report each family across a small decoding grid so the family/decoding confound is bounded, not only disclosed.
- **Value-weighted human-touch**: recompute the 15–25% figure on a real capital plan weighted by value with the mandatory-set triggers applied — expected well above 50%.
- **TOST docking margins**: upgrade the 15/15 pooled-SE docking to a pre-specified equivalence test per cell.
- **Longitudinal per-run raw dump** for the E/F/G cells (currently CIs come from summary stats), and **archetype-weight sensitivity** on the calibrated results (weights are declared-assumed, unswept).

## Pending experiments (the frontier this program reached but did not close)

- **F-0 v4 — subtler still + multimodal**: the mechanical and current-subtle instruments both saturate the frontier models on fraud detection; a harder, image-bearing instrument is needed to test real ensemble correlation, and to probe the physical-quality fraud the document layer cannot reach.
- **Experiment G+ — collusion mechanism design**: G measured that collusion breaks the verification story; the *defenses* (verified beneficial ownership, contributor Sybil-resistance, decentralized assigner/seeder/floor-setter) are unmodeled. Also the long-con timing cell (PG5) and adversarially-selected operating points (A-a) and fabricated contraposition coverage (A-b).
- **Seeded-controls operational design**: who seeds, blinding, control-manifold secrecy against a registry-reading captured operator — the E-1d/F drift instrument's unearned precondition.
- **Experiment D (human)**: the D-lite pilot protocol (`planning-behavior-calibration/D_LITE_PILOT_PROTOCOL.md`) is ready; the full human study replaces the LLM priors.

## The independence that matters most

Every review round here is author-simulated. The two highest-value external inputs, named in the reviewer cover note: an **adversary-side second author** (does the F-8 collusion analysis hold; what does a real fraudster do the model does not), and an **evals-methodology reviewer** for F-7 beyond our own. These are gating for any claim of validation, as opposed to process discipline.

## What the paper claims (inventory)

**Method contributions:**

1. A reproducible adversarial ABM framework for comparing public-allocation architectures (common world, paired seeds, deterministic engines, version-stamped outputs).
2. Endogenous participation: behavioral populations generated by a Core v0-conformant adoption model replace imposed participation blocks (Experiment C; the master's E8 bridge).
3. LLM-elicited behavioral priors as a calibration methodology — panels, archetype weighting, convergence analysis, model-sensitivity discipline (only cross-model-stable patterns are informative), and the identical human instrument as the replacement path.
4. Pre-registration discipline throughout, with honest prediction accounting (refuted-informative outcomes reported as findings).

**Findings (current):**

- F1. Architecture ranking is behavioral-population-invariant; Core v0 distributed delivers 2.0–2.7× the status quo, peaking under low adoption.
- F2. Participation without a default layer is not weaker — it is non-functioning (verified delivery zero under every realistic population).
- F3. The attentive share is structural (~2.5–5%) across all prior sources; the verification market, not adoption, binds.
- F4. The deterrence stack is individually redundant and jointly indispensable (0.87× below status quo when removed whole) — resolved into the master as docs/111.
- F5. Agenda capture prices the tutored choke point (−13% value, −35% selection), not the distributed spirit; coordinated signal corruption is robust.
- F6. The semi-open transition is a dial, not a leap (break-even ~8–10% envelope; 1.5× at half; 2.18× at full).

## Phases

### Phase 0 — Paper definition (1 session)

Outline, venue shortlist (JASSS / Computational Economics / Governance+methods venues), claims-to-evidence table, repo `CITATION.cff`. Decide the paper's spine: method-first (the framework) vs findings-first (the architecture results).

### Phase 1 — Flagship experiment: **Experiment E (author decision 2026-07-06: Option 1, enriched)**

The author selected the longitudinal option and enriched it with the program's sharpest open question: **the authority's budget-release strategy and the freezing problem** — nothing in Core v0 specifies when the authority releases budget into the allocation machinery, and excess release may freeze capital (fragmentation below activation targets; WIP locked in escrow beyond verification capacity), starving new approvals. Pre-registered design: [`adversarial-abm/EXPERIMENT_E_LONGITUDINAL_DESIGN.md`](adversarial-abm/EXPERIMENT_E_LONGITUDINAL_DESIGN.md) — engine v0.6 (multi-cycle milestone escrow, verification capacity, docs/104 expiry valve, Poisson project arrivals, reputation compounding), five release-policy families (day-zero, uniform, front-loaded, pull/CONWIP, approval-conditioned commitment — the author's non-"leverage"), optimum search with Pareto frontier (V vs frozen ratio vs latency), then adaptive adversaries incl. congestion-timed attacks against the optimized configuration. The optimal release rule is a candidate new Core v0 object via the master pipeline. Deferred options (later additions, author's call): scale/federation, distributional equity, full-lifecycle fidelity.

**Status**: E-1a executed 2026-07-06 (pull rule wins; verification capacity is the pipeline's ceiling; `RUN_2026_07_06_EXPERIMENT_E1A_RESULTS.md`). E-1c executed 2026-07-06 (AI triage = capacity insurance, +24% at scarce K; deterrence-stack slack makes imperfect AI safe — no accuracy crossover up to 20% false-pass; one-cycle timeout-reassignment recovers ~80% of stall damage; smoothing demoted pending delay-neutral reimplementation; `RUN_2026_07_06_EXPERIMENT_E1C_RESULTS.md`). E-1b executed 2026-07-06 (adaptivity neither erodes nor inverts while the docs/111 margin holds; pull removes the congestion surface; no verifier compensates a broken stack; P5 null-in-range; `RUN_2026_07_06_EXPERIMENT_E1B_RESULTS.md`). **The Experiment E program is complete.**

**Phase status (2026-07-06, all advanced under the author's full-program goal):**
- Phase 0 ✔ — `PAPER_OUTLINE.md` (claims-to-evidence map, venue shortlist, findings-first spine), `CITATION.cff`.
- Phase 1 ✔ — Experiment E program (E-1a, E-1c, E-1b).
- Phase 2 ✔ — Mesa dock **15/15 PASS** (`docking/DOCKING_REPORT.md`); internal cross-engine docks recorded.
- Phase 3 ✔ — `STATISTICAL_ANNEX.md` (paired 95% t-intervals; all headline differences exclude zero), `tools/reproduce_all.py`.
- Phase 4 ✔ — draft v0.2 (`drafts/paper.md`): five-profile adversarial review round applied (`drafts/REVIEW_ROUND_1.md` — political scientist and practitioner fatals dissolved into legal-layer framing + PB-literature benchmark; replicator checks all PASS; verifier-displacement frontier deployed to §8 with its E-1d evaluation). **Author read pending.**
- Phase 5 ✔ — released as **v0.4** (doi:10.5281/zenodo.21246089) at the author's instruction ("primera versión mejorable"); the master **v1.9** (doi:10.5281/zenodo.21246169) cites it and consolidates the program's rules.
- Master queue ✔ — v1.9 queue carries Q5 (release rule + verification ceiling) and Q6 (AI verification + second instance); the verifier-displacement design is recorded in the master's verification-throughput note.

**Experiment F executed 2026-07-07** (`adversarial-abm/RUN_2026_07_07_EXPERIMENT_F_RESULTS.md`): the real five-family panel found the fraud side degenerate (every family catches ~100% of mechanical flaws — correlation not-testable-in-range, harder instrument named) and the unpredicted finding carries the program — false-flag rates on clean work span 17%–100% under one strict prompt, so **the layered-verification problem is passing honesty, not catching fraud**: specificity-first layer composition, strict families as referees, seeded controls as the operating-point calibrator; F-1 k\*=2 dead by ρ=0.3; F-2 relocates the binding control cost to court-grade evidence production. Second-satellite-paper decision at the author's read.

**Original pre-registration (2026-07-07): Experiment F — layered heterogeneous machine verification** ([`adversarial-abm/EXPERIMENT_F_LAYERED_VERIFICATION_DESIGN.md`](adversarial-abm/EXPERIMENT_F_LAYERED_VERIFICATION_DESIGN.md)): F-0 measures real cross-engine error correlation with evidence-judgment panels (the models are the component under test — target panel of five families: latest Qwen, latest Gemma, ideally DeepSeek local, plus codex and Claude Fable hosted; the author's model-layer refresh precedes the runs), F-1 prices layers-vs-confidence under measured correlation and ensemble gaming, F-2 adds control-cost accounting to locate the new binding cost (evidence production). Candidate second satellite paper; results decide.

### Phase 2 — Cross-validation dock (1–2 sessions) — AUTHOR DECISION PENDING

Model docking (Axtell et al. 1996): independent reimplementation of the core architecture comparison, verified equivalent within tolerance. Cross-framework results cannot be seed-identical; equivalence is distributional (matched designs, overlapping confidence intervals, equivalence tests).

- **Dock 1 (recommended, committed): Mesa-native Python reimplementation** of the 5-architecture adversarial comparison. Different language, different paradigm (object-scheduler vs bespoke loops), same design; the repo already carries Mesa competence and the behavioral model's dual-path (Mesa/stdlib, byte-identical) as a precedent.
- **Dock 2 (conditional on Option 2): Agents.jl (Julia)** — performance-grade, scientifically credible, unlocks the 1M-citizen scale experiment as the same investment.
- **Dock 3 (optional, community reach): NetLogo** replication of the headline comparison — the social-simulation community's lingua franca; maximal reviewer legibility, minimal performance.

Deliverable: a docking report (design table, per-metric equivalence bands, divergences explained or fixed) — reviewers rarely see one; it is the paper's validity backbone.

### Phase 3 — Statistical hardening (1 session)

Paired CIs on every headline (some tables still report mean±sd only), seed-sensitivity annex, multiple-comparison notes, and a single reproduction script that regenerates every table and figure from a clean clone.

### Phase 4 — Writing and internal adversarial review (2–3 sessions)

Outline → full English draft → **the house method applied to ourselves**: a five-profile simulated review round (computational methodologist, political scientist, statistician, public-sector practitioner, skeptical replicator), objections converted to fixes or declared limitations → revision.

### Phase 5 — Package and release

Zenodo deposit of this repository (satellite DOI) → the master's v1.9 moment opens per its queue: cite the satellite, apply the queued items, shrink via references (net-growth goal: zero or negative).

## Decision points for the author

1. ~~Flagship experiment~~ — **decided 2026-07-06**: Experiment E (longitudinal + release policies + freezing + adaptive adversaries); design pre-registered.
2. Docking targets — deferred by the author to after Experiment E: Dock 1 (Mesa) recommended committed; Dock 2 (Julia) only if scale is wanted; Dock 3 (NetLogo) optional.
3. Paper spine (method-first or findings-first) — deferred; naturally decided with the venue in Phase 0.
