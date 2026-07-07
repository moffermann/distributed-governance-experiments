# Internal Adversarial Review Round 2 — 2026-07-07 (satellite v0.4 → v0.5, Finding 7 focus)

> **Remediation status (applied in v0.5 / master v1.10):** the construct bug (E1) is fixed — the de-leaked v3 instrument overturned the false-flag half (gpt 0.80→0.03) and the corrected, CI-bearing result is capability-tiered, with the temperament-spread and evidence-richness claims withdrawn as artifacts. CIs, Fisher tests, and bootstrap ratio intervals added; qwen excluded from correlation stats (S1–S4, E2). Decoding disclosed (`DECODING.md`), rescues dropped, no-verdict category added (E3, E7, R2-1/2/3). F-3/F-4 relabeled as stipulated-mechanism sensitivities; F-4 collusion caveat added via Experiment G (S6, R2-4/5). Scope-limited per the fiscalizer (F1–F6): document-legible only, "court-grade"→"tamper-evident," human-touch flagged as project-count over-count of the value-weighted share, coverage selection unpublished. The adversary meta-finding (single-shot → collusion) became Experiment G and Finding 8. Bookkeeping fixed (predictions 42, "600"→per-family N, reproduce_all covers F/G). Both papers re-rendered and re-deposited (satellite v0.5, master v1.10). Remaining, named not silent: ~10× more cases for powered correlations, a within-instrument evidence-richness manipulation, a second frontier-scale family, value-weighted human-touch on a real capital plan, and the collusion-resistance mechanism-design study.

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

## rev-adversary (red-teamer) — the deepest finding: the single-shot adversary model

**Root flaw (architectural, not statistical):** the diversion decision is drawn ONCE at activation as a Becker expected-value bet against the *published* end-to-end detection probability. F-3's "cascade covers a 21.7% verifier" comes entirely from "the cascade removes the attempts upstream" (1.2/100) — an *output of the single-shot draw*, not an observation of adversary behavior. A real adversary is multi-period, adaptive, collusive, and games the model's exogenous inputs. **Conformance to the design ≠ robustness against the world.** Every headline ratio should be read as robustness against a *designed* adversary, not a real one.

| # | Severity | Exploit | Design change |
|---|---|---|---|
| A-a | critical | **Blind-spot targeting:** submit compressed-timeline fraud (the panel-wide shared blind spot, 10–50% fp across all five families), not class-averaged; real fp ≈ top of range, correlated across every layer — exactly where k*=2/ρ=0.3 collapses. Plus: the published A041 margin is a vuln-disclosure feed (hit the thin-margin scope); penalty priced nominal not collectable (thin-cap SPV, fresh shell per project defeats reputation memory) | Compute margin on *collectable* penalty (bonding/escrow/verified beneficial ownership); publish that a margin test *passed*, not its value; re-run F-3 with an adversarially-*selected* operating point |
| A-b | critical | **Contraposition capture** (F-4's crown jewel is the softest target: coverage exogenous, catch=0.8, fabrication not modeled): contributors are the same 2.5–5% attentive share = a handful of identifiable people per project via the public feed. Silence→invisibility (no contradiction ⇒ no human summoned; captured layer reads clean); astroturf→laundering (sockpuppet confirmations raise confidence, suppress s_min); weaponize→capacity DoS (fabricated counter-evidence against honest rivals exhausts the corps) | Model fabricated/astroturfed coverage explicitly; **confirmation must be non-suppressive** (agreement never lowers the floor); require contributor independence *established* (Sybil-resistance), not assumed; bond contradiction-filing. F-4's "rescues a broken stack" is an upper bound assuming the attacker ignores the rescue instrument |
| A-c | high | **Forged provenance at scale:** attestation binds capture, not fact. Staged-but-real (build one real 20m, submit for the 2km; reuse one site across phantom projects); insider-signed (executor holds the devices → clone the key); $300 SDR GPS spoofing | Corroborate provenance across independent channels; model key-compromise; the durable backstop is contraposition — so (c) is only as strong as (b) is unbroken |
| A-d | high | **Seed evasion:** seeds are known-bad by construction → fingerprint (no corresponding real project in the *public* registry is decisive); radical transparency is the seed's enemy; a captured/steered operator (F-0 proves steerability by instruction alone) partitions "probe vs real" | Seeds must be indistinguishable ⇒ real projects with planted violations (stings), secret/rotated manifold, seeder org-separate from operator; state the 1/(q·π) latency as *conditional on seed-indistinguishability* (currently unearned) |
| A-e | high | **Root capture:** anti-capture protects the leaves (auditors) and leaves the root (assigner/seeder/floor-setter) exposed. Own the randomizer → "random" becomes "directed." Starve the floor (the paper's own efficiency results are the capturer's justification to pin it at the epistemic minimum). Thin-market audit oligopoly colludes | Distribute + adversarially-review the assigner/seeder/floor-setter; index the floor to caseload/stakes (not a scalar a capturer pins low); treat "minimum viable corps" as a *security* parameter, not only a drift-detection one |
| A-f | critical | **The master exploit — collusion the single-shot model cannot see:** shell + captured assigner + astroturfed confirmation + recognized seeds = every layer independently reports clean; the ABM prices these as *independent* draws and multiplies protection, but under collusion cross-layer ρ≈1 and protection is the *minimum*, not the product. Never measured executor–verifier–contributor correlation. Plus **poison the exogenous market-price reference** (the anchor F-0 relies on); plus **the long con** (build clean reputation for years — the 8-year null assumes stationarity — then defect en masse in the published post-model-change window to swamp the 15–25% corps) | **Build a collusion-aware, multi-period, adaptive adversary engine**: probes the boundary, selects blind spots, cycles identity, correlates across layers, treats the market reference and evidence-producer independence as attacker-influenceable. This is the missing independent check and the model class most likely to move the headline ratio |

**Defenses the adversary judged genuinely sound:** universal-exposure/selective-inspection (correct deterrence shape; fails only vs the capturing/colluding actor); contraposition-as-anticipated-deterrence (logic right; the failure is the capturability assumption, not the logic); price-vs-in-bundle-reference (strong vs non-collusive price fraud; fails only when the anchor is poisoned); the A041 publish-the-margin rule (defeats the internal salami-slicer — but the same publication arms the external targeter).

**Meta-finding:** the independence that matters most is **not a second frontier model for the priors — it is a second author for the adversary.** The single-shot diversion draw is the specific choice that lets the cascade look complete and lets protections multiply instead of collude. The "model progress is upside" asymmetry is true for the verifier but equally upside for the fraudster's evidence generation — the arms race is symmetric; the paper counts one side.

---

# Consolidated remediation plan (all five reviewers)

## Tier 1 — Correctness (papers + corpus become honest). Required before any re-deposit.

1. **Re-run the F-0 panel once, fixing every methodology defect together:** de-leak the clean bundles (remove/neutralize the in-bundle threshold so "clean" violates no referenced control rule); **fixed decoding across families** (or a disclosed config grid); a **prompt set** (not one strict prompt) reporting the operating-point envelope; **more cases** for power (target ~40–60/flaw class); uniform, pre-registered exclusion/rescue rule; degenerate outputs → a no-verdict category.
2. **Add CIs everywhere in F** (Wilson on rates, exact/bootstrap on ratios and φ); **downgrade the correlation/ensemble claims** to "one of five 2-stacks shows correlated failure; the rest are consistent with independence — underpowered, exploratory, uncorrected"; **exclude qwen** from correlation/ensemble stats (four-family study); no flaw-class rankings from small cells.
3. **Relabel F-3/F-4 honestly:** F-4 is a *stipulated-mechanism sweep* (catch/pi/dossierBoost stated and justified, pi reconciled with E-1c), not "measured"; the measured-pair→engine mapping disclosed as a moment-matched reduced form; reconcile ρ=0.05 vs φ=0.43 vs the ρ=0.3 death point; drop V-orderings inside noise.
4. **Scope Finding 7 (fiscalizer):** it covers *document-legible, delivery-phase* fraud only; add the "compliant evidence, defective physical work / pre-contract / quantity" fraud the panel *cannot* catch; replace "court-grade by construction" with "tamper-evident, provenance-attested at capture" (custody, contradiction, expert testimony remain in the loop); recompute human-touch *value-weighted* (expect >50%); publish the coverage *rate*, keep *selection* unpredictable.
5. **Bookkeeping:** registry 35 not 23; "600" → 594 with per-family N in the table; add analyze_panel + e_f1/f2/f34 to reproduce_all and refresh the stale v0.9.0 stamps; fix the reproducibility statement to exclude only live-model runs.
6. **Propagate corrections** to the master (§9, published v1.9) and the corpus note; deposit corrected versions (satellite v0.5, master v1.10) — noting the v1.9 error honestly in the changelog.

## Tier 2 — Depth (new research, not a fix). The highest-value item the round surfaced.

7. **The collusion-aware, multi-period, adaptive adversary engine** (adversary A-f): the single most valuable next experiment — it directly attacks the single-shot assumption underlying every verification-security result, and the adversary judged it "the model class most likely to move the headline ratio." Candidate flagship of a genuine follow-up. Also folds in: adversarially-selected operating points (A-a), fabricated contraposition coverage (A-b), poisoned market reference (A-f), the long-con window attack.

## What survives untouched
F1–F6 (architecture findings, fully reproducible static/longitudinal engines), mechanical-fraud saturation, and F-4's contraposition *direction* (effect large enough to likely survive, once fabrication is modeled it becomes an upper bound). The remediation is scope-limiting + one clean re-run + honest relabeling — **not retraction of the program.**
