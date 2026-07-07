# Internal Adversarial Review Round 1 — 2026-07-06

Five-profile simulated review of draft v0.1 (the master program's house method applied to this paper). Objections verbatim-summarized with dispositions; every objection becomes a fix, a declared limitation, or named future work — never silence.

## Political scientist

| # | Severity | Objection | Disposition |
|---|---|---|---|
| P1 | fatal | Floats free of the empirical PB literature; Finding 3 presented as discovery without confronting participation data | **Fix in v0.2**: engage the PB empirics in-text — observed PB participation rates (Porto Alegre single-digit shares of adults; cross-national surveys) land in the same single-digit band as the simulated attentive share, which becomes the finding's external benchmark instead of synthetic/LLM concordance; add real references; state where the simulated polity diverges (no party mobilization, no campaigns) |
| P2 | major | Status quo is value-inert and scored on the challenger's home metric | **Fix + declare**: state that the status quo is audit-calibrated including its actual control regime (the master's A036/docs/105 discipline) and that its flatness across *participation* populations is by construction (it has no participation channel); declare V as the challenger-relevant metric and the incumbent's unmeasured functions (legitimacy, bargaining, responsiveness) as an explicit boundary; distributional-equity metrics named as the designed follow-up (roadmap Option 3) |
| P3 | major | "Latent social value" smuggles a contested normative theory | **Fix in v0.2**: name the commitment in the methods (value as discoverable/aggregable; the deliberative-constructivist tradition is outside the model), and name the alternative-objective test (min-share/Rawlsian) as future work |
| P4 | major | Canon-migration framing is circular self-validation | **Fix in v0.2**: reframe honestly as single-ecosystem process discipline (author's own adversarial pipeline, author verdicts), not independent validation; external expert review (the master's prepared packets) named as the pending independence step; conclusion wording softened |
| P5 | minor | Synthetic+LLM agreement is not convergent validity | **Fix in v0.2**: Finding 3 restated as hypothesis pending the identical human instrument; support shifts to the PB empirical benchmark (P1's fix) |

## Public-sector practitioner

| # | Severity | Objection | Disposition |
|---|---|---|---|
| Q1 | fatal | E-1a assumes away budget annuality; pull rule "violates the appropriations act" | **Fix + declare + future run**: the no-lapse treasury was a declared assumption; v0.2 states the legal vehicle explicitly — the release rule operates *within whatever carryforward instrument the jurisdiction has* (capital funds, revolving funds, multi-year investment programs; the semi-open envelope is precisely such a vehicle), and within a strict-annuality regime it degenerates to within-year pull; an E-1a variant with lapsing funds is pre-committed as the next engine run |
| Q2 | fatal | No procurement law between allocation and disbursement; reputation-informs conflicts with statutory debarment | **Fix in v0.2**: state the layering — citizen allocation directs funds to *projects*; executor award and payment run through existing procurement law (the master's allocation-act characterization, docs/102); milestone-gated disbursement maps to progress payments; statutory debarment is country law operating *outside* the platform, fully compatible with the platform itself never excluding (docs/43/107 boundary); procurement cost/delay named unmodeled |
| Q3 | major | Budget mostly non-discretionary; no authority veto | **Fix scope in v0.2**: every headline claim scoped to the discretionary capital/grant slice; envelope calibration to real budget composition = deployment configuration; the veto gap already declared (docs/110 boundary) and repeated where it matters |
| Q4 | major | AI-gated disbursement vs due process; audit bodies are independent, not fundable throughput | **Fix + declare**: distinguish the architecture's own control market (fiscalizers, fundable capacity — what the model prices) from constitutionally independent state audit (unmodeled, unchanged, used only for calibration); complaint paths are the appeal hook for machine-gated decisions; administrative-law status of automated disbursement named as an open deployment question alongside the second-instance human design |
| Q5 | minor | "Allocation secrecy" unexplained reads as anti-sunshine | **Fix in v0.2**: one sentence — individual-choice privacy (ballot-style, anti-coercion) with full aggregate transparency; everything institutional remains public (docs/108) |
| Q6 | minor | The governed object is a capital-project fund, not "the budget" | **Fix in v0.2**: same scope statement as Q3, applied to title-adjacent claims ("public-resource allocation" → the discretionary, project-shaped portion) |

## Replicator (checks executed directly)

| # | Check | Result |
|---|---|---|
| R1 | Static engine rerun (behavioral-llm-calibrated) vs committed results | **PASS** — zero diffs |
| R2 | Statistical annex regeneration idempotent | **PASS** — zero diffs |
| R3 | Headline numbers present in their claimed sources (2.26 bridge; 0.304 E-1a; 0.316 E-1c; 0.87× ablation; anchor 0.303844218531) | **PASS** — all found |
| R4 | Mesa dock independent reproduction | **PASS** — 15/15 distributional equivalence (docking report) |

## Methodologist (agent findings, reviewed against draft v0.1; several already fixed in v0.2)

| # | Severity | Objection | Disposition |
|---|---|---|---|
| M1 | major | §9 docking was an unfilled placeholder citing a nonexistent report; SQ divergence (0.1345 vs 0.1267 → dock-side ratio ≈2.07×) undisclosed | **Fixed in v0.2/v0.3**: the report exists (15/15 PASS table committed) and §9 now carries the numbers *and discloses the SQ divergence explicitly*, restating the docking claim as ordinal/distributional (~5% ratio agreement), with a pre-specified TOST margin named for revision |
| M2 | major | Blanket pre-registration claim false for ablation/E-1b (atomic commits) and semi-open (no design file) | **Fixed in v0.3**: §2 now states the verifiability gradient honestly (separate-commit designs for E-1a/E-1c; atomic for ablation/E-1b; semi-open classed exploratory); `predictions.csv` registry committed |
| M3 | major | "Advantage peaks under low adoption" rides on the stipulated honest high-quality default vector | **Fixed in v0.3**: Finding 1 names the condition and prices it with the existing signal-mix sweep (1.63× at mix 0.2) — conditional claim, never below the status quo in range |
| M4 | major | E8 cross-validation not reproducible from this repo | **Fixed in v0.3**: E8 scoped explicitly as external evidence reproducible in the master repository |
| M5 | minor | Finding 3 range misattributed (across scenarios, not prior sources) and "insensitive to adoption" self-contradictory | **Fixed in v0.3**: attribution corrected (2.5% high-friction → 5.1% AI-assisted onboarding; all prior sources land inside), "bounded disposition" replaces "insensitive"; 0.309 attributed to the master's §E8 record |
| M6 | minor | Experiment C mapping and archetype weights not cited by path / no weight sensitivity | Mapping is `behavioral-adoption-abm/OUTPUT_TO_ADVERSARIAL_ABM.md` (outline's claims map); archetype-weight sensitivity added to future work — **partially addressed, flagged open** |

## Statistician (agent findings)

| # | Severity | Objection | Disposition |
|---|---|---|---|
| S1 | major | All CIs conditional on a single base RNG seed | **Fixed in v0.3**: multi-base-seed check committed (`tools/multiseed_check.mjs`) — 5 independent base seeds: static ratio spans 2.19–2.28× (sd 0.03), longitudinal pull 0.291–0.304 (sd 0.005); seed 1 sits at the low end, so single-seed reporting was conservative; annex updated |
| S2 | major | Docking equivalence criterion undefined/unfalsifiable | **Fixed in v0.3**: criterion (2-pooled-SE per cell, fixed in the docking brief before the port ran) now stated in §9 with the residual divergence disclosed; TOST named for revision |
| S3 | major | Ratio drift across artifacts (2.18/2.19 etc.), no ratio CIs | **Fixed in v0.3**: RESULTS.md regenerated on the full-precision ratio-of-means convention (2.19/2.69/2.35), intra-file inconsistency removed; ratio CIs (Fieller/bootstrap) flagged for revision |
| S4 | major | Cross-model discipline exercised only at n=90; N=1,000 single-family; convergence is within-model | **Fixed in v0.3**: §2 restates the limits plainly; second frontier-scale family named future work |
| S5 | major | Mean-sufficiency asserted, not demonstrated | **Fixed in v0.3**: §2 now cites the committed distribution-vs-means fixed-seed analysis as the test (it was performed, the draft failed to cite it) |
| S6 | minor | Multiple-comparison control narrative; no committed registry | **Fixed in v0.3**: `predictions.csv` committed (23 rows, outcome-labeled); annex adds the BH/FDR statement over the confirmatory set |

## Replicator (agent findings + checks executed directly)

| # | Severity | Finding | Disposition |
|---|---|---|---|
| R1 | pass | Static engine rerun == committed to full float precision; annex regeneration byte-identical; docking JS reference matches fresh run | — |
| R2 | medium | RESULTS.md ratios disagree with annex/paper (rounded-input convention) | **Fixed in v0.3** (see S3) |
| R3 | medium | reproduce_all never exercised the Experiment C scenario builder | **Fixed in v0.3**: builder wired into the pipeline (4 sources) |
| R4 | medium | Longitudinal numbers verified only against committed artifacts (per the no-sweep instruction) | Accepted; `reproduce_all.py` covers the reruns; multi-seed check adds independent replication |
| R5 | medium | Clean-clone fragility: no requirements.txt, unpinned matplotlib/mesa, autocrlf phantom diffs | **Fixed in v0.3**: `requirements.txt` (matplotlib, mesa pinned to the docking major), `.gitattributes` with eol normalization |
| R6 | low-med | E8 bridge unverifiable from this repo | **Fixed in v0.3** (see M4) |
| R7 | process | Repo was a moving target during review; claims should pin to a tag | **Fixed in v0.3**: review baseline tagged `paper-v0.3` |

## Round outcome

Applied across drafts v0.2–v0.3 (same date, tagged `paper-v0.3`). The two "fatal" practitioner objections dissolve into legal-layer framing the master corpus already carries (docs/102, docs/43, docs/110) but the draft failed to import; the political scientist's fatal (literature engagement) is fixed with the PB benchmark, which *supports* Finding 3; the methodologist's and statistician's majors produced real new artifacts (multi-base-seed check, predictions registry, honest pre-registration gradient, SQ-divergence disclosure, requirements/eol infrastructure) and honest reframings (conditional low-adoption claim, external E8 scope, single-family panel limits). The verifier-displacement frontier was deployed to §8 with its E-1d evaluation (seeded positive controls as the drift-detection instrument). Items left open for the venue revision, named: TOST margins for docking, Fieller/bootstrap ratio CIs, archetype-weight sensitivity, a second frontier-scale panel family, the lapsing-funds E-1a variant, and a per-run raw dump for longitudinal cells.
