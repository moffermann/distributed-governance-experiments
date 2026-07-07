# Core v0 Traceability Matrix

Every load-bearing concept in these experiments, mapped to the master-corpus object or accepted resolution that governs it ([moffermann/distributed-governance-research](https://github.com/moffermann/distributed-governance-research)). This is the anchoring contract: an experiment mechanism with no row here is either experiment-internal machinery or a gap to be flagged.

Conventions: `docs/NN` are accepted resolutions in the master corpus; `H0NN`/`C0NN` are corpus hypotheses/contradiction records; experiment locations name the engine or document that implements the concept.

## Operating-regime vocabulary (master docs/110)

The master corpus formalized the operating-regime ladder (docs/110). Experiment naming anchors to the canonical vocabulary so no variant requires reinterpretation:

| Canonical regime (docs/110) | Adversarial ABM variant | Planning-vector variants | Deprecated names (legacy aliases) |
|---|---|---|---|
| Tutored regime, mandated agenda (transition scaffold) | `core_v0_tutored_mandated_agenda` | `central_*` representative family (comparator role) | `core_v0_tutored_central_planning` |
| Tutored regime, distributed agenda | `core_v0_tutored_distributed_agenda` | `core_v0_tutored_distributed_voluntary` / `_mandated` | `core_v0_tutored_distributed_planning`, `core_v0_simple` |
| Semi-open regime (bounded envelope, automatic protocol approval) | fiscal-parallel blend runner `src/semi_open.mjs` (transition path quantified; per-project veto stage still unmodeled) | **no variant yet** | — |
| Open regime | — (open-mode lifecycle not modeled) | `core_v0_open_*` family (planning construction only) | — |

Run documents dated before 2026-07-06 use the legacy names; this table is the map. Centralized planning appears in experiments only as the status-quo comparator or the transition scaffold — never as the architecture's proposal.

## Citizen-side concepts

| Experiment concept | Where implemented | Core v0 anchor | Anchoring rule |
|---|---|---|---|
| Public default rule (non-active allocation follows published planning priorities) | behavioral `default_rule_share` + default-routed funding; adversarial `passiveAllocationMode: "planning"`; paper-engine `d` share | docs/101 ("What you, a citizen, actually do"), H033 | Inactivity is designed-for, never lost signal |
| Direct allocation | behavioral `direct_active`; adversarial attentive channel; paper-engine informed actives | docs/101, docs/21 citizen flows | Optional, revocable, per-citizen unit weight |
| Automatic allocation profiles | behavioral `profile_driven`; adversarial profile channel (noisier value proxy + near-completion preference) | docs/28 | Profiles route allocation among eligible projects only; they never construct planning vectors (CORE_V0_PLANNING_CHANNEL_MODEL) |
| Trusted microdelegation as the delegation baseline | behavioral citizen micro-delegates + two-stage channel choice; adversarial `delegationBlockSize` small informed blocks; planning-vector `TRUSTED_MICRODELEGATION_MODEL.md` | docs/21, C023, docs/101 ("delegate your allocation to someone you trust, revocable any time") | Many small delegates, high alignment, one-click revocation; institutional/broker delegation is the stress case, never the baseline |
| Delegation revocability and switching | behavioral revocation/switching rates (shock-elastic); planning-vector `delegateRevocationResponsiveness` | docs/21, A010/docs/76 concentration observability | Revocation is a citizen act; concentration is observed, never capped by platform power |
| Allocation secrecy; only voluntary self-disclosure is socially observable | behavioral `social_signal()` limited to registered/active/abandoned/recommending; no engine exposes allocation targets | docs/108 | No receipts, no per-citizen allocation ledger, aggregates only |
| Attentive planning participation | behavioral planning rounds (`attentive_share`); planning-vector `attentivePlanningShare`; paper-engine E8 informed share | docs/101, CORE_V0_PLANNING_CHANNEL_MODEL | Attentiveness is emergent in B, imposed-and-calibrated elsewhere; the emergent 4–5% validated the imposed 5% |
| Non-use, rejection, abandonment as normal outcomes | behavioral permanent rejection, churn, reactivation | docs/101 (inattention designed-for); behavioral design rule | Never tuned away; reported as outcomes |

## Planning concepts

| Experiment concept | Where implemented | Core v0 anchor | Anchoring rule |
|---|---|---|---|
| Planning vector ≠ allocation profile | planning-vector `CORE_V0_PLANNING_CHANNEL_MODEL.md`; behavioral planning layer excludes profile users from vector construction | docs/58, docs/87 | Vectors are built from attentive + delegated signals (+ optional mandate); never from salience, default routing, or profiles |
| Central planning as information loss, not incompetence | planning-vector representative machinery; adversarial `centralPlanningSignalMix`; paper-engine planner bandwidth | docs/101 limitations (agenda-setting), E4; author clarification 2026-07-06 | Central planning is **not part of Core v0's architecture** — it appears only as the status-quo comparator baseline and as a transition scaffold in tutored deployments; central planners are modeled as coherent but bandwidth-limited and salience-guided |
| Agenda capture requires a publishing choke point | adversarial `agendaCapture` (tutored-mandated regime only); distributed analog = `coordinatedSignalBias` / E7b | docs/87; author clarification 2026-07-06 (master open-questions record) | Capture of a published vector prices the tutored choke point; distributed construction has no such surface and its signal-corruption analog is measured robust |
| Honest-signal boundary | all engines | docs/87, docs/91 (open problem) | Elicitation under gaming is out of scope everywhere and declared, never silently assumed solved |
| Authority mandate as coverage amplifier | planning-vector `authorityMandateSignal` | docs/58 (tutored mode), docs/106 (enabling norm) | Mandate raises participation/coverage; it does not inject central content unless the scenario says so |

## Execution and control concepts

| Experiment concept | Where implemented | Core v0 anchor | Anchoring rule |
|---|---|---|---|
| Reputation informs, never excludes | behavioral delegate choice scoring; adversarial `reputationLoss`/`futureSelectionLoss` as deterrence costs | docs/107 | No platform mechanism removes an actor; pool exit is funders' lost preference |
| Conditional disbursement / deterrence inequality | adversarial retention/guarantee/detection terms; paper-engine regime thresholds `p·((1−a(1−r))+γ+R)` | Formal companion note Props 1–2, docs/101 | Reduced form declared where milestones are not modeled |
| Verification separated from execution | adversarial detection independent of executor; behavioral fiscalizer/evidence coverage vs requirements | docs/101, docs/40, docs/52 | Control budget and assignment never pass through the verified party |
| Evidence informs/triggers, never certifies (qualitative signals) | recorded design direction only (`behavioral-adoption-abm/COMMENT_SIGNAL_LAYER_NOTE.md`) | docs/79 | Comment layer unimplemented; guardrails fixed before any implementation |
| Audit without reputational memory deters nothing | paper-engine E7 CALIBRATED regime; adversarial low-memory variants | docs/105, E7 finding | The instrument the status quo lacks is memory, not inspection |
| Executor opportunism as type + cost draw | adversarial `opportunisticShare`, `fraudOpportunity`; paper-engine `c_eff ~ U(0.3,0.9)` | E5/E7 machinery; audit-evidence base (docs/105) | Executor-side parameters stay audit-anchored; behavioral outputs never override them |

## Calibration concepts

| Experiment concept | Where implemented | Core v0 anchor | Anchoring rule |
|---|---|---|---|
| LLM panels as synthetic priors, never empirical data | planning-behavior-calibration PROMPT_PROTOCOL + provenance blocks; `llm-elicited` provenance class | Behavioral ROADMAP Stage 5 discipline | Model-dependent; only cross-model-stable patterns are informative; the human instrument (identical) replaces them |
| Population-weighted archetypes | ARCHETYPES.md extended set, assumed weights | — (declared assumption, no corpus anchor) | Weights marked assumed, not census-fitted — flagged, not hidden |
| Audit-anchored status quo | adversarial/paper-engine calibrated regimes | docs/105, research/audit-evidence-base.md (master) | Status-quo parameters come from published audit-institution findings, never from convenience |

## Declared gaps (anchored but unimplemented)

| Gap | Anchor | Status |
|---|---|---|
| Profile pause/override state split | docs/28 §10 | Open in behavioral ABM (declared in its conformance audit) |
| Comment/reputational signal layer | docs/79, docs/107, docs/108, docs/98 | Design direction recorded; insertion points defined |
| Privacy-attitude elicitation | docs/108 (privacy concern is a behavioral trait) | Missing from the calibration instrument; flagged for v0.4 |
| ~~`agendaCapture`, `fiscalizerCollusion`, `coordinatedSignalBias` attacks~~ | docs/87; formal note Prop 4; E7b | **Closed 2026-07-06**: implemented in engine v0.5; results in `adversarial-abm/RUN_2026_07_06_ABLATION_RESULTS.md` |
