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

## Pending: rev-stat, rev-adversary, rev-repro2 — dispositions to be merged on receipt.
