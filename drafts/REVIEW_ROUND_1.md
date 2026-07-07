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

## Methods/statistics (self-audit applied; agent findings appended on receipt)

| # | Severity | Issue | Disposition |
|---|---|---|---|
| M1 | minor | Draft claimed "twenty-two predictions, nine refuted"; the verifiable count is 23 pre-registered predictions (ablation 6, E-1a 7, E-1c 5, E-1b 5), of which 8 refuted/null and 1 transformed | **Fixed in v0.2** (exact count now stated) |
| M2 | minor | E-1a's frozen-*ratio* metric artifact (denominator favors day-zero) | Already declared in the E-1a run document; the draft uses absolute frozen-months throughout — no change needed |
| M3 | note | Longitudinal cells report t-intervals from summary stats, not per-run raws | Declared in the annex header; acceptable, flagged for a per-run raw dump in a revision |

## Round outcome

Applied in draft v0.2 (same date). The two "fatal" practitioner objections dissolve into legal-layer framing that the master corpus already carries (docs/102, docs/43, docs/110) but the draft failed to import — the fix is exposition plus one pre-committed engine run (lapsing-funds E-1a variant); the political scientist's fatal (literature engagement) is a genuine gap fixed with the PB benchmark, which — notably — *supports* Finding 3 rather than weakening it. The verifier-displacement frontier was deployed to the paper (§8) with its E-1d evaluation, which corrected the design's own epistemics (seeded positive controls as the drift-detection instrument). Any further rev-methods/rev-repro agent findings are appended and dispositioned on receipt.
