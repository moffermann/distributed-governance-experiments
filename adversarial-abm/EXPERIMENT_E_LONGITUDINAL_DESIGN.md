# Experiment E — Longitudinal Dynamics, Budget-Release Policy, and the Freezing Problem (pre-registered design)

Registered 2026-07-06, before any implementation or run. Naming note: satellite experiments are lettered (A–D so far); "Experiment E" is unrelated to the master repository's E1–E8 suite.

## The question (author's framing)

Core v0 specifies how citizens allocate, how funds disburse against milestones, and how delivery is verified — but **nothing in the corpus specifies when the authority should release budget into the allocation machinery**. The author's concern, verbatim in spirit: too much budget released too fast may get *stuck* ("atorado") inside the machinery — frozen by excess distribution — blocking the activation of new projects. This experiment (1) makes the freezing failure mode measurable, (2) compares the authority's budget-release strategies, (3) searches for the optimal release policy, and (4) turns the optimum into a candidate institutional rule for the master corpus (via the attack → defense → resolution pipeline, author verdict as always). It then (5) re-runs the adversarial program against the optimized configuration with adversaries that adapt.

## Two freeze modes, formalized

The current engine already contains the first mode latently (a project executes only when `funded ≥ budgetTarget`; commitments to never-filled projects produce zero verified value forever), and has the second mode structurally excluded (execution is instantaneous once funded). Experiment E makes both first-class:

1. **Fragmentation freeze** — released budget spreads across many projects, none reaching its activation target: capital committed sub-threshold, nothing starts. The author's "exceso de distribución".
2. **Work-in-progress (WIP) freeze** — projects activate faster than execution and verification capacity can process them: capital locked in escrow/retention on executing-but-undelivered works; the verification queue saturates; new activations starve.

The framing is queueing-theoretic: by Little's Law, committed-undelivered capital = delivery throughput × cycle time; throughput is bounded by verification capacity (the fiscalizer bottleneck Experiment B found binding) and executor capacity. Releasing budget above the machinery's throughput inflates frozen capital without raising delivered value. The manufacturing literature says pull policies (CONWIP: release against completions, keeping WIP constant) dominate push policies under variability — the experiment tests whether the same holds for a public-allocation institution.

## Terminology (author's rule)

The release mode where the authority's commitment follows effective project approval is called **approval-conditioned commitment** (Spanish: *compromiso condicionado por aprobación*) — explicitly not "leverage"/"apalancamiento", which the author has ruled out as the name.

## Engine extensions (v0.6, adversarial-abm)

All existing machinery (architectures, populations, attacks, planning sources) carries over. New:

1. **Budget-release layer.** Annual budget B (12·citizens per year, keeping per-budget comparability). Citizens allocate only *released and not-yet-committed* funds. Policy families:
   - `P0 day-zero`: full year released at the year's first cycle.
   - `P1 uniform`: B/12 per monthly cycle (the current engine's implicit behavior — the baseline).
   - `P2 front-loaded`: geometric within-year schedule, decay parameter λ.
   - `P3 pull (CONWIP)`: release only what keeps total frozen capital (sub-threshold commitments + execution escrow) at or below a WIP cap W; bounded by the remaining annual budget.
   - `P4 approval-conditioned commitment`: release α × funding needs of newly activatable projects, α ∈ [0.8, 1.5] (α > 1 is bounded over-commitment against expected expiry returns).
2. **Multi-cycle execution with milestone escrow.** Activated projects run D cycles (drawn per project) with a milestone schedule; funds sit in escrow and release per verified milestone (retention/guarantee terms unchanged from the deterrence stack). Execution is no longer instantaneous — the WIP freeze becomes possible.
3. **Verification capacity.** At most K milestone verifications per cycle (fiscalizer capacity, anchored to B's verification-bottleneck finding); excess queues. Detection quality degrades gracefully with queue age only if a scenario says so (default: delayed, not degraded — the conservative choice, flagged for sensitivity).
4. **Funding-window expiry (the corpus's own valve).** Sub-threshold commitments older than TTL cycles return to the releasable pool — docs/104's closure-deadline expiry, now load-bearing: the anti-fragmentation valve the corpus already owns, never yet simulated.
5. **Dynamic project pool.** Poisson arrivals (rate λ_arr per cycle) with latent value/salience/planning signals drawn by the existing world machinery; completed and expired projects leave; the pool no longer exhausts.
6. **Reputation compounding.** Executor pool with entry/exit; reputation accumulates across projects; future-selection loss becomes endogenous (funder preference for track record), so the deterrence inequality's R term grows with tenure — the longitudinal half of the original Option 1.

## Metrics (new, alongside V/leak/selection)

- **Frozen-capital ratio** per cycle: (sub-threshold commitments + execution escrow) / released-to-date; reported split by freeze mode.
- **Delivery throughput**: verified value per year; **delivery latency**: release-to-verified-delivery distribution.
- **Starvation rate**: fundable (above-threshold-demand) projects unable to activate for lack of releasable funds or verification slots.
- **V per budget-year** for cross-policy comparability.

## Phases

### E-1a: release-policy comparison and optimum search

Grid over the five families (each at 3–5 parameter points), 20 runs, seed 1, behavioral-llm-calibrated population, core_v0_tutored_distributed_agenda vs status_quo. Then continuous optimization (coordinate descent over α, W, λ, TTL) with objective: maximize V per budget-year subject to a frozen-ratio ceiling; report the full Pareto frontier (V vs frozen ratio vs latency) rather than a single point. Deliverable: the optimal release rule stated as an institutional rule candidate.

### E-1b: adaptive adversaries against the optimized configuration

The same optimizer harness turned around: attack parameters (collusion rate, capture severity, bias share, and **new timing attacks** — diversion timed to high-WIP windows when the verification queue is saturated) optimized against the E-1a winner. Question: does congestion create an attack surface — i.e., is the release policy also a *security* parameter?

## Pre-registered predictions

- **P1.** Day-zero release (P0) produces the highest frozen-capital ratio and does not produce the highest V: the flood fragments across the open pool and saturates verification.
- **P2.** The pull policy (P3) weakly dominates all push policies on V per budget-year at equal or lower frozen ratio; the optimal W tracks verification capacity K (the binding resource), not the budget size.
- **P3.** Fragmentation freeze appears when per-cycle release exceeds (project arrival rate × mean activation target); the docs/104 expiry valve bounds it but with a latency cost that shortening TTL trades against churn.
- **P4.** Approval-conditioned commitment (P4) with α slightly above 1 approaches the pull optimum; α well above 1 recreates the WIP freeze it was meant to avoid.
- **P5.** Under multi-year reputation compounding, the architecture's advantage grows with time (the R term compounds; the status quo has no memory), unless adaptive adversaries offset it.
- **P6.** Adaptive adversaries concentrate attacks in congestion windows; the verified-value loss from a timing-aware adversary exceeds the same attack budget spread uniformly — making frozen capital a security cost, not only an efficiency cost.
- **P7.** The architecture ranking (Core v0 distributed > status quo) survives every release policy; the release policy moves the magnitude, not the ordering.

## Core v0 anchors

| Mechanism | Anchor |
|---|---|
| Funding caps / activation targets | docs/101 |
| Milestone-gated disbursement, retention, guarantees | formal note Props 1–2, docs/101, docs/111 (integrity margin published; term values unchanged here) |
| Funding-window expiry returning commitments | docs/104 |
| Verification capacity as a budgeted resource | docs/40, docs/52 |
| Reputation informs, never excludes (compounding stays informational) | docs/107 |
| Authority release schedule as visible fiscal act | docs/88, docs/106 |
| Budget-release policy itself | **no anchor — the gap this experiment measures**; candidate new corpus object |

## Declared boundaries

- Milestone objects are modeled as escrow schedules, not full evidence contracts (the known simplification, now partially closed).
- Verification-queue behavior under saturation (delay vs quality degradation) is a modeling choice, run both ways in sensitivity.
- The optimizer finds optima *for this model*; the institutional rule candidate is stated in mechanism terms (pull against verification capacity), not in fitted constants.
- Adaptive adversaries optimize within declared attack families; open-ended strategy discovery is out of scope.
