# Behavioral Adoption ABM Experiment

## Working title

**Behavioral Adoption and Delegation Simulation for Core v0: Modeling Human Use, Trust, Participation, and Role Formation in a Distributed Governance Platform**

## Status

Executable MVP added, then audited and corrected against Core v0 ([`CORE_V0_CONFORMANCE_AUDIT.md`](CORE_V0_CONFORMANCE_AUDIT.md)), then extended end-to-end with a planning layer: emergent attentive citizens, delegated planning signals, distributed-vs-central vector construction, default-rule routing, and need-weighted delivered value ([`PLANNING_LAYER_DESIGN.md`](PLANNING_LAYER_DESIGN.md), results in [`RUN_2026_07_06_PLANNING_LAYER_RESULTS.md`](RUN_2026_07_06_PLANNING_LAYER_RESULTS.md)).

This folder defines a new satellite experiment focused on the behavioral unknowns that were previously imposed as parameters in the Core v0 architecture experiments.

The existing adversarial ABM experiment asks which institutional architectures survive strategic stress once participation, delegation, verification, and execution are available. This experiment asks a prior behavioral question:

```text
Where do participation, delegation, active use, inactivity, abandonment, evidence production,
fiscalization supply, and executor participation actually come from?
```

## Core idea

Core v0 should not be modeled as a platform with generic users. It should be modeled as an ecosystem of roles whose behavior emerges from trust, incentives, friction, perceived legitimacy, social influence, prior experience, and institutional feedback.

The key behavioral variables are not constants. They should be endogenous outputs of the simulation.

Examples:

- registered users;
- active users;
- inactive registered users;
- passive citizens;
- partial delegators;
- full delegators;
- profile-driven users;
- voluntary fiscalizers;
- professional fiscalizers;
- evidence producers;
- honest executors;
- opportunistic executors;
- organizations willing to participate;
- users who abandon after friction or bad outcomes;
- users who recommend Core after successful outcomes.

## Quick start

The first executable prototype can run with Python's standard library only. Mesa is optional: if installed, the model uses Mesa's `Agent` and `Model` base classes; if not, a small fallback shim keeps the run reproducible.

From this folder:

```bash
python run_experiment.py --scenario scenarios/baseline.json --ticks 104 --seed 42 --output-dir outputs/baseline
```

Or as a module:

```bash
PYTHONPATH=src python -m behavioral_adoption_abm.run --scenario scenarios/ai_assisted_onboarding.json --output-dir outputs/ai_assisted
```

Each run writes:

```text
outputs/<run>/timeseries.csv
outputs/<run>/final_metrics.json
outputs/<run>/integration_outputs.json
```

The `integration_outputs.json` file is the bridge to the existing institutional architecture experiment.

## Relationship to existing experiments

This experiment is deliberately separated from the architecture-comparison engine.

The recommended sequence is:

```text
Experiment A — institutional architecture comparison
Experiment B — behavioral adoption and role-formation ABM
Experiment C — integrated architecture + behavioral simulation
Experiment D — calibration against pilot or real-world adoption data
```

The current architecture experiment may continue using imposed behavioral parameters for controlled comparison. This experiment is designed to generate those parameters from a behavioral model.

## Primary research question

```text
Under what behavioral, institutional, trust, friction, and incentive conditions does Core v0 generate
sustained human participation, meaningful delegation, adequate fiscalization supply, credible evidence
production, and enough executor participation to operate as a live governance platform?
```

## Secondary questions

1. What share of citizens become fully active, partially active, passive-but-delegated, passive-and-inactive, or abandoned?
2. What share of active users choose direct allocation, profile-based allocation, partial delegation, or full delegation?
3. Does delegation concentrate in a small number of trusted actors or remain distributed?
4. Are there enough fiscalizers and evidence producers to sustain verification markets?
5. What incentives are required for honest executors and organizations to participate?
6. What level of platform friction prevents adoption?
7. How damaging are early failures, public controversies, or service outages to trust and retention?
8. Which roles appear naturally and which require explicit institutional incentives?
9. What minimum liquidity, trust, evidence, and fiscalization thresholds are needed before Core becomes self-sustaining?

## Intended contribution

This experiment should contribute:

1. an explicit behavioral ontology of Core v0 roles;
2. a reproducible agent-based model of adoption, use, delegation, role formation, trust, and abandonment;
3. behavioral parameters that can feed the institutional architecture experiment;
4. a way to test onboarding, incentives, UX friction, social diffusion, fiscalizer supply, and evidence production before a live pilot;
5. a bridge between theoretical mechanism design and real-world platform adoption.

## Non-goals

This experiment does not claim to:

- predict real adoption rates without empirical calibration;
- replace pilot data;
- model every political, cultural, or psychological factor;
- prove that Core v0 will be adopted;
- tune assumptions until adoption looks successful;
- collapse institutional performance and human adoption into one opaque model.

## Design rule

> The model must treat non-use, distrust, abandonment, apathy, and delegation concentration as normal outcomes, not as bugs.

If Core only works when every citizen behaves like an attentive civic optimizer, the experiment should expose that.

## Folder map

Research design:

- [`ROLE_ONTOLOGY.md`](ROLE_ONTOLOGY.md) — first operational map of behavioral roles, motivations, actions, incentives, risks, and observable metrics.
- [`METRICS.md`](METRICS.md) — adoption, activity, delegation, trust, fiscalization, evidence, executor, and retention metrics.
- [`MODEL_DESIGN.md`](MODEL_DESIGN.md) — proposed ABM structure, state variables, scheduling logic, and connection points to the architecture experiment.
- [`ROADMAP.md`](ROADMAP.md) — staged plan from documentation to executable Mesa/Python simulation and later calibration.
- [`IMPLEMENTATION_NOTES.md`](IMPLEMENTATION_NOTES.md) — current implementation boundary, run instructions, and next technical steps.
- [`CORE_V0_CONFORMANCE_AUDIT.md`](CORE_V0_CONFORMANCE_AUDIT.md) — audit of the implementation against the Core v0 corpus: findings, corrections, certification, and declared gaps.
- [`PLANNING_LAYER_DESIGN.md`](PLANNING_LAYER_DESIGN.md) — pre-registered design of the end-to-end planning layer: attentive citizens, delegated signals, distributed vs central vector construction, and the value chain.
- [`RUN_2026_07_06_MESA_RESULTS.md`](RUN_2026_07_06_MESA_RESULTS.md) — first (pre-audit) Mesa run, kept as a dated record.
- [`RUN_2026_07_06_POST_AUDIT_RESULTS.md`](RUN_2026_07_06_POST_AUDIT_RESULTS.md) — post-audit 10-seed sweep results and interpretation (pre-planning engine, kept as a dated record).
- [`RUN_2026_07_06_PLANNING_LAYER_RESULTS.md`](RUN_2026_07_06_PLANNING_LAYER_RESULTS.md) — end-to-end planning results: emergent attentive share, distributed-vs-central comparison, value feedback loop, prediction accounting.
- [`RUN_2026_07_06_LLM_CALIBRATED_RESULTS.md`](RUN_2026_07_06_LLM_CALIBRATED_RESULTS.md) — LLM-elicited priors vs synthetic: what is prior-sensitive and what is structural.

Executable prototype:

- [`run_experiment.py`](run_experiment.py) — convenience command-line runner.
- [`run_sweep.py`](run_sweep.py) — multi-seed sweep across all scenarios with mean/min/max summaries and viability-flag frequencies.
- [`run_planning_comparison.py`](run_planning_comparison.py) — distributed-vs-central sweep over planning attendance, with an attentive-only (no-delegation) variant.
- [`apply_llm_calibration.py`](apply_llm_calibration.py) — maps a `planning-behavior-calibration` LLM panel onto ABM parameters and writes `scenarios/llm_calibrated.json` with provenance (see `OUTPUT_TO_BEHAVIORAL_ABM.md` in that experiment).
- [`OUTPUT_TO_ADVERSARIAL_ABM.md`](OUTPUT_TO_ADVERSARIAL_ABM.md) — Experiment C pre-registered mapping: behavioral populations replace the adversarial ABM's imposed population block.
- [`build_adversarial_scenario.py`](build_adversarial_scenario.py) — Experiment C adapter: sweep means → generated adversarial scenarios with provenance (results in `../adversarial-abm/RUN_2026_07_06_BEHAVIORAL_INTEGRATION_RESULTS.md`).
- [`src/behavioral_adoption_abm/core.py`](src/behavioral_adoption_abm/core.py) — MVP model, agents, metrics, scenario loading, and result writers.
- [`src/behavioral_adoption_abm/run.py`](src/behavioral_adoption_abm/run.py) — package CLI entry point.
- [`scenarios/`](scenarios/) — baseline and stress scenarios.
- [`outputs/`](outputs/) — ignored/generated run outputs.

## Implementation direction

The first implementation uses Python with an inspectable ABM structure. Mesa remains the intended native ABM base when installed, but the MVP can run without mandatory external dependencies so early review is not blocked by environment setup.

The model should initially remain simple and deterministic enough to inspect. LLM-based agents may be added later only for bounded qualitative sub-simulations, not as the first source of numerical results.
