# Adversarial ABM Experiment

## Working title

**Adversarial Agent-Based Simulation for Public Resource Allocation: Stress-Testing Centralized, Participatory, and Distributed Governance Architectures**

## Status

Preliminary research-design baseline.

This folder starts the second satellite-paper track derived from the master working paper. It is deliberately isolated from the main architecture corpus so the experiment can evolve without rewriting Core v0 prematurely.

## Core idea

Public-resource allocation architectures should not be compared only under average, honest, or idealized behavior. They should be stress-tested under adversarial institutional conditions:

- rational ignorance;
- salience cascades;
- weak verification;
- fiscalizer capture;
- collusion;
- metric gaming;
- milestone gaming;
- evidence manipulation;
- clientelist brokerage;
- agenda capture;
- reputation lock-in;
- thin verifier markets.

The experiment will build an adversarial agent-based model (ABM) to compare institutional architectures using common agents, attacks, assumptions, and outcome metrics.

## Relationship to the master paper

The master paper presents the full architecture and already contains several computational experiments. This satellite project deepens that computational layer into an independent paper and replication package.

The master paper's current simulation layer is treated as the seed, not the final model.

This experiment should eventually answer:

```text
Which institutional mechanisms survive adversarial stress,
which fail,
and which combinations produce more delivered verified value per unit of public budget?
```

## Research question

```text
Can adversarial agent-based simulation provide a reproducible method for comparing public-resource allocation architectures under rational ignorance, salience bias, weak verification, collusion, evidence manipulation, clientelism, agenda capture, and reputation dynamics?
```

## Intended contribution

The project aims to contribute:

1. a reusable adversarial ABM framework for institutional design;
2. a library of institutional attack scenarios;
3. a set of comparable public-allocation architectures;
4. ablation tests for Core v0 mechanisms;
5. metrics centered on delivered verified social value per unit of budget;
6. a computational bridge between the master architecture and a future real-world pilot.

## Non-goals

This experiment does not claim to:

- prove real-world effectiveness without a pilot;
- replace empirical public-administration evaluation;
- validate the legal feasibility of binding citizen allocation;
- model every political behavior;
- prove that any one architecture wins universally;
- tune parameters until Core v0 wins.

## Design rule

> The simulator must make the adversary stronger before it makes the proposed architecture stronger.

If the architecture wins only under friendly assumptions, the experiment should expose that.

## Folder map

Research framing:

- [`DESIGN_BASELINE.md`](DESIGN_BASELINE.md) — preliminary research design and paper outline.
- [`SCENARIO_TAXONOMY.md`](SCENARIO_TAXONOMY.md) — distinction between scenario, architecture, operating-mode approximation, and planning model.
- [`ARCHITECTURES.md`](ARCHITECTURES.md) — institutional models to compare.
- [`IMPLEMENTED_VARIANTS.md`](IMPLEMENTED_VARIANTS.md) — architecture variants currently implemented in the executable v0 engine.
- [`PLANNING_INFORMATION_MODEL.md`](PLANNING_INFORMATION_MODEL.md) — central versus distributed planning signals and their relationship to latent value.
- [`PLANNING_CALIBRATION_FROM_EXPERIMENT_2.md`](PLANNING_CALIBRATION_FROM_EXPERIMENT_2.md) — how planning-vector construction calibrates ABM planning-signal mixes.
- [`AGENTS_AND_ATTACKS.md`](AGENTS_AND_ATTACKS.md) — agents, adversarial behaviors, and attack library. Backlog note: the citizen-comment reputational surface and its astroturf/brigading attack pair are recorded in `../behavioral-adoption-abm/COMMENT_SIGNAL_LAYER_NOTE.md`.
- [`METRICS_AND_RESULTS.md`](METRICS_AND_RESULTS.md) — outcome metrics and interpretation discipline.
- [`RESULT_INTERPRETATION_NOTES.md`](RESULT_INTERPRETATION_NOTES.md) — how to distinguish budget absorption, actual value, verified value, reported value, leakage, and visibility gaps.
- [`ROADMAP.md`](ROADMAP.md) — staged build plan from design to replication package.
- [`ENGINE_AUDIT_2026_07_06.md`](ENGINE_AUDIT_2026_07_06.md) — engine v0.4 audit: comparator-noise bug, dead population channels implemented, Core v0 conformance checklist, pre/post baseline.
- [`RUN_2026_07_06_BEHAVIORAL_INTEGRATION_RESULTS.md`](RUN_2026_07_06_BEHAVIORAL_INTEGRATION_RESULTS.md) — Experiment C: architectures under behaviorally generated populations; ranking invariant, Core advantage 2.0–2.7×, no-default participation collapses to zero.

Technical design:

- [`TECHNICAL_ENGINE_DESIGN.md`](TECHNICAL_ENGINE_DESIGN.md) — engine architecture, determinism, scheduling, threading, AI boundary, and module layout.
- [`AGENT_DECISION_MODEL.md`](AGENT_DECISION_MODEL.md) — how agents know, decide, and respond to incentives under each architecture.
- [`PROBABILITY_AND_PARAMETER_MODEL.md`](PROBABILITY_AND_PARAMETER_MODEL.md) — distributions, probabilistic decisions, parameter classes, attack severities, and sensitivity sweeps.
- [`SCENARIO_CONFIGURATION.md`](SCENARIO_CONFIGURATION.md) — scenario files, reproducibility metadata, run identity, and result headers.

## Future migration

When the experiment becomes stable, this folder should be extracted into a dedicated repository, likely:

```text
moffermann/distributed-governance-adversarial-abm
```

That future repository should contain only the computational paper, code, scenario definitions, result tables, figures, and reproduction instructions.
