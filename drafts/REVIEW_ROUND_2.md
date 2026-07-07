# Internal Adversarial Review Round 2 — 2026-07-07 (satellite v0.4, Finding 7 focus)

Five-profile round the author requested for the F-program material added since Round 1: statistician, LLM-evaluation methodologist, public-sector fiscalizer, adversary red-teamer, reproducibility engineer. As with all house rounds, this is single-ecosystem **process discipline, not independent validation** — the reviewers are simulated by the orchestrator. Recorded honestly on that basis.

Status: rev-fiscal and rev-evals delivered; rev-stat, rev-adversary, rev-repro2 pending. Dispositions finalized once all five are in.

## VERIFIED CRITICAL BUG — Finding 7 false-flag half is construct-invalid

**rev-evals objection 1, independently verified against the data (2026-07-07):**

- All **60/60** v2 "clean" bundles contain an invoice line item above the `per_item_approval_threshold_clp` (1,000,000 CLP) that the generator publishes *inside each bundle*; 23/60 also have a unit price above it.
- gpt's 0.80 false-flag rate is **48/48 flags citing the over-threshold item** — a legitimate control-compliance concern, not a false alarm. Claude's 0.05 "best temperament" comes from *ignoring* the over-threshold items (it only checked for below-threshold structuring).
- Therefore the false-flag column measures **label conformance to a mislabeled construct**, not model judgment. Everything downstream is compromised: the family "temperament" ordering, the evidence-richness rescue (Claude 95%→5%), and the calibration probe (which "succeeds" by instructing gpt to stop naming a real issue).

**Scope of the defect (propagation):**
- Satellite `drafts/paper.md` §9 (Finding 7) — false-flag table, "evidence richness moves operating points," calibration-probe paragraph.
- Master `drafts/paper.md`/`paper.es.md` §9 (v1.9, **published** doi:10.5281/zenodo.21246169) — the "operating points steerable by instruction and by evidence richness" sentences.
- Corpus `knowledge/open-questions/verification-throughput-design.md` — the F-0 v2 evidence-richness paragraph.
- **What survives:** the false-pass / subtle-fraud separation (the leak pushes toward flagging, so it does not inflate false-pass; if anything the true false-pass is slightly higher), and the mechanical-fraud saturation result. Both stand as **underpowered-directional** (see rev-stat/rev-evals obj. 2).

**Remediation (deferred to the consolidated v0.5 re-run, so the panel is re-run ONCE with all methodology fixes):** de-leak the clean bundles (remove the published threshold or ensure no clean bundle violates a referenced control rule) OR adjudicate the label so over-threshold-without-approval is a valid flag and re-score; fix the confounds below in the same re-run; then correct both papers and the corpus and deposit a corrected version.

## rev-evals (LLM-evaluation methodologist) — 7 objections

| # | Severity | Objection | Disposition (pending full round) |
|---|---|---|---|
| E1 | critical | Clean-label leak (above) | **Verified**; withdraw false-flag half, rebuild on de-leaked instrument |
| E2 | critical | Correlations/ensemble ratios rest on 1–4 events (joint false-pass: gpt+claude=1, gemma+claude=2, deepseek+claude=4; φ=0.43 from 4 passes; 6.0× = one vignette) | Downgrade PF0-1/PF0-2 to "directional, underpowered"; attach Wilson/Poisson CIs; ~10× cases before any ρ is quotable |
| E3 | high | Per-family decoding configs aliased with family identity (deepseek 0.217 fp = only unconstrained + highest temp; that's the "worst 21.7%" fed into F-3) | Hold decoding fixed or run a config grid; stop attributing to "family" |
| E4 | high | "Five families" conflates frontier-hosted with 14–35B local-quantized; the φ=0.416 "hosted trait" is a 2-point line = "bigger models more cautious" | Report scale/quant tier; frame as capability-tiered, not family-peer |
| E5 | high | One fixed prompt drives every temperament number the paper treats as a model property | Report a prompt set + envelope; label operating points prompt-conditional throughout §9 |
| E6 | med-high | Orchestrator neutralization covers grading but not instrument authorship — the leak IS an authorship confound (Claude wrote "clean", Claude scores best on its own notion of clean) | Instrument + label rubric authored/adjudicated outside the tested set |
| E7 | med | Rescues at temp 0.7–1.0 (third config, selective on hard cases), silent per-family denominators (118/116/120), degenerate loop outputs parsed as verdicts | Pre-register uniform exclusion/rescue rule; intent-to-treat denominator; unparseable = no-verdict category |

## rev-fiscal (public-works auditor) — 6 objections (all scope, not method)

| # | Severity | Objection | Disposition (pending full round) |
|---|---|---|---|
| F1 | critical | Costliest fraud (pre-contract collusion/overprice; quality-below-spec that photographs fine; quantity/cubicación fraud) is never in the evidence bundle; F "subtle fraud" is all document-legible | Scope Finding 7 to document-legible delivery-phase fraud; add a "compliant evidence, defective physical work" vignette class the panel *cannot* catch; state the physical/pre-contract share is likely the majority of value-at-risk |
| F2 | critical | "Court-grade by construction" conflates provenance with chain-of-custody/content/probative weight | Replace with "tamper-evident and provenance-attested at capture"; state custody, contradiction, expert testimony remain in the loop |
| F3 | high | 15–25% human-touch fails non-delegable duty (authorless harm), universal appealability, and a mandatory set that is most of the real portfolio | Recompute value-weighted (not project-count); treat as document-verifiable layer only; name the liable authorizing officer; bound appeal load. Expect >50% value-weighted |
| F4 | high | Contraposition idealizes the citizen: salience bias, tactical rival-bidder denuncias, aligned capture (absence of contradiction ≠ correctness, yet router down-weights the quiet captured project) | Model contraposition endogenous to visibility + capture; inject fabricated counter-evidence; router must NOT down-weight zero-contradiction projects; re-run the rescue-a-broken-stack cell adversarially |
| F5 | high | Small cross-scope rotating corps: territorial-competence/civil-service/union law; issuer-pays conflict for plural audit firms; budget floor is theater unless set by a non-audited party | Institutional design naming who sets/enforces the floor independently, with one real jurisdiction's law as a worked example |
| F6 | med-high | Publishing coverage rules (s_min, mandatory set, q) hands the fraudster the map; real deterrence needs procedural surprise | Publish the coverage *rate*, keep *selection* unpredictable/unpublished; model an adversary optimizing against published thresholds |

**Both reviewers converge on the same meta-point:** Finding 7's *limitations* (§11) are honest; its *headline/abstract* language overshoots them. The correction is scope-limiting, not retraction — except the false-flag half (E1), which is a genuine construct bug requiring a re-run.

## rev-stat (statistician) — 7 objections; transcription verified faithful, inference not

Cell sizes reconstructed: 60 flawed + 60 clean/family; false-pass event counts gpt 2, claude 5, gemma 7, deepseek 13, qwen 0; ensemble co-occurrences 1–4. **No CI anywhere in the F artifacts** (the annex covers only A/C/E).

| # | Severity | Objection | Disposition |
|---|---|---|---|
| S1 | fatal | "Ensembles 1.9×–6.0× worse than independence" rests on 1–4 events; the granularity floor 1/60 already exceeds the independence predictions for 3 pairs, so ratio>1 is partly *forced by discretization*; only deepseek+claude (4 events) is cleanly CI-separable from independence | Exact/bootstrap CI on every ratio; drop cells where independence isn't rejected; honest form: "one of five 2-stacks shows correlated failure; the rest are consistent with independence" |
| S2 | major | φ correlations unpowered/CI-free; "up to φ=0.43" cherry-picks the max of 6 estimable pairs; 4/10 undefined (qwen) | CIs on every φ; report the distribution not the max |
| S3 | major | "Subtle fraud separates the families" mostly within noise — Fisher exact: gpt vs claude p=0.44, claude vs gemma p=0.56, gemma vs deepseek p=0.22; only extremes separate (gpt vs deepseek p=0.004). Per-flaw-class claims come from 10-case cells | Support only "best passes less subtle fraud than worst"; interior ranking unresolved at n≈60; no flaw-class rankings |
| S4 | major | qwen degenerate (fp 0, ff 1) — zero variance, all φ undefined, forces every stack to 0/inf; it's really a **four-family study** counted as five | Exclude qwen from correlation/ensemble stats; relabel effective panel size |
| S5 | major | v1→v2 evidence-richness is an uncontrolled two-instrument comparison; its own table contradicts the mechanism (gemma moves *opposite* 0.167→0.458, gpt barely 0.767→0.800) | Within-instrument manipulation (same vignettes ± anchors) or demote to confounded hypothesis |
| S6 | major | §9 headlines measured φ up to 0.43, but F-3 maps the same pair into the engine as ρ=0.05 (~8× smaller) while F-1 says layer benefit dies by ρ=0.3 — so the measured worst pair already exceeds the death point, yet the reassuring cascade cell runs near-independence; F-3 leak deltas have no CIs and a noise inversion (worst verifier deepseek posts the highest V=0.307) | Reconcile ρ=0.05 vs φ=0.43 vs the ρ=0.3 death point; run-level CIs; drop V-orderings inside the ±0.009 noise |
| S7 | major | Multiplicity never updated: predictions.csv now 35 rows, annex still says "23"; §9's ~10 φ, 20 ratios, 30 per-flaw cells in no multiplicity accounting | Bring F into the registry as a declared exploratory (uncorrected) set |

**Verified number mismatches:** registry = 35 predictions, paper + annex still say "twenty-three"; "600 verdicts" is nominal (actual 594: gemma 118, qwen 116); PF0-*v2 design_file is a generator script, not a design doc.

**rev-stat solid:** rates match the JSON exactly; independence arithmetic correct (granularity is the problem, not the multiplication); F-4's contraposition effect is large enough to likely survive the run counts; the qwen/instrument/saturation honesty is creditable.

## rev-repro2 (reproducibility engineer) — 4 reproductions + 7 objections

Reproductions: longitudinal anchor **PASS exact** (0.303844218531; v0.10 additions zero-RNG-when-off confirmed); statistical_annex **PASS** (empty diff); results-v2 counts **FAIL vs "120/family"** (gemma 118, qwen 116 = 594 not 600); reproduce_all **PARTIAL** — e_f34 byte-identical, but e_f1/e_f2 still stamped **v0.9.0** (never re-run by the pipeline) and **reproduce_all runs no F program at all**.

| # | Severity | Objection | Disposition |
|---|---|---|---|
| R2-1 | high | Per-family decoding heterogeneous + undisclosed (only 2/5 greedy); "identical protocol" is the prompt, not the decoding | Publish the per-family decoding table; fixed-decoding sensitivity or rescope to "family+recommended-decoding" |
| R2-2 | high | Subtle panel is 594 not 600; missingness non-ignorable (loop failures correlate with content); listwise rates | Print actual per-family N; treat "no usable output" as a verifier-failure category |
| R2-3 | med-high | Rescues at temp 0.7–1.0 on the hardest cases, unseeded, irreproducible, unmentioned in the paper | Disclose rescue procedure/count; flag rescued verdicts |
| R2-4 | med | F-3/F-4 "measured" cells inject stipulated params (pi=0.7 — contradicts E-1c's 0.9 — dossierBoost=1.25, sampleRate=0.05); **F-4 contraposition catch=0.8 is entirely stipulated** yet called "measured" | Relabel F-4 as a stipulated-mechanism sweep; state pi/catch; justify or fix pi=0.7 |
| R2-5 | med | measured-pair→engine mapping (sqrt/ρ_eff) is a moment-matched surrogate valid only at the operating point; the two engine layers aren't the two models | Disclose as reduced-form; caveat gaming/drift inferences for the pair |
| R2-6 | med | reproduce_all omits the entire F program (incl. the deterministic analyze_panel + e_f1/f2/f34 that need no live models); stale v0.9.0 stamps confirm | Add analyze_panel (both instruments) + e_f1/f2/f34; fix the reproducibility statement; refresh stamps |
| R2-7 | low-med | F-0 non-reproducible by construction; operating points hand-copied into e_f34 | Have e_f34 read from f0_v2_results.json; state F-0 is a one-time measurement |

**rev-repro2 solid:** engine determinism/seeding/zero-RNG-when-disabled all hold exactly; F1–F6 live in the fully reproducible static/longitudinal engines and are untouched by any of this.

## Convergence across four reviewers (fiscal, evals, stat, repro2)

Three independent lines hit the **same core**: Finding 7's *inferential and framing layer* overshoots its evidence, while its *engine layer and limitations section* are sound. Specifically —
1. **The false-flag / temperament / evidence-richness / calibration half is construct-invalid** (evals E1 verified; stat S5) — a re-run on a de-leaked instrument is required.
2. **The correlation / ensemble / family-ranking claims are underpowered** (stat S1–S4, evals E2) — CIs + honest "one of five pairs" framing, qwen excluded.
3. **Decoding/scale/prompt confounds** alias family identity (evals E3–E5, repro2 R2-1) — fixed decoding + capability tiers + prompt band.
4. **"Measured" is overclaimed for F-3/F-4 stipulated params** (repro2 R2-4/5, stat S6) — relabel; reconcile ρ=0.05 vs φ=0.43.
5. **Scope overshoot** (fiscal F1–F6) — Finding 7 covers document-legible delivery-phase fraud only; physical/pre-contract fraud is out of reach; "court-grade" and "15–25%" must be scoped.
6. **Bookkeeping** — registry 35≠23, "600"≠594, reproduce_all omits F (stat, repro2).

**What survives untouched:** F1–F6 (the architecture findings), the mechanical-fraud saturation, and F-4's contraposition *direction* (large enough to likely survive). The remediation is scope-limiting + a single de-leaked, fixed-decoding, CI-bearing re-run — not retraction of the program.

## Pending: rev-adversary — merged on receipt, then remediation plan finalized.
