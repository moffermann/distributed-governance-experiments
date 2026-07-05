# Roadmap — Adversarial ABM Satellite Project

## Purpose

This roadmap defines the staged path from preliminary design to a publishable computational satellite paper and eventual standalone replication repository.

## Phase 0 — Research framing

Status: started.

Goals:

- define research question;
- define architecture comparison set;
- define agent taxonomy;
- define attack library;
- define metrics;
- define result interpretation discipline;
- keep the project separate from the master architecture corpus.

Outputs:

- `README.md`;
- `DESIGN_BASELINE.md`;
- `ARCHITECTURES.md`;
- `AGENTS_AND_ATTACKS.md`;
- `METRICS_AND_RESULTS.md`;
- `ROADMAP.md`.

Exit condition:

```text
A reader can understand what the experiment is, why it matters, what it will compare, and what counts as success or failure.
```

## Phase 1 — Minimal simulator skeleton

Goal:

Build the first executable version of the adversarial ABM.

Recommended structure:

```text
experiments/adversarial-abm/src/
  world/
  agents/
  architectures/
  attacks/
  metrics/
  experiments/
  runner
```

Minimum features:

- seeded deterministic world generation;
- project latent value;
- project salience;
- budget targets;
- citizen attention types;
- at least three architectures;
- at least two attacks;
- delivered-value metric;
- result table output.

Initial architectures:

1. centralized status quo;
2. participatory/citizen allocation without delivery controls;
3. Core v0 simplified.

Initial attacks:

1. salience cascade;
2. diversion under weak verification.

Exit condition:

```text
The simulator can run paired-seed comparisons and produce stable result tables.
```

## Phase 2 — Architecture ablation layer

Goal:

Represent Core v0 as a set of toggleable mechanisms rather than one monolithic treatment.

Mechanisms to toggle:

- funding-target closure;
- default/profile layer;
- evidence contract;
- milestone gating;
- retention/recovery;
- independent fiscalization;
- k-corroboration;
- reputation memory;
- discovery explainability;
- concentration observability.

Exit condition:

```text
The simulator can show which mechanisms are load-bearing and which are secondary under each attack.
```

## Phase 3 — Full adversarial library v0

Goal:

Implement the first complete attack library.

Attacks:

1. salience cascade;
2. metric gaming;
3. milestone gaming;
4. fiscalizer collusion;
5. evidence manipulation;
6. clientelist brokerage;
7. incumbent agenda capture;
8. coordinated signal bias;
9. thin verifier market;
10. reputation lock-in.

Exit condition:

```text
Every attack has at least one testable severity parameter and at least one architectural defense toggle.
```

## Phase 4 — Calibration and sensitivity

Goal:

Separate arbitrary assumptions from externally anchored parameters.

Tasks:

- identify parameters already supported by the master paper's audit evidence base;
- identify parameters requiring literature search;
- identify parameters that must remain synthetic;
- run sensitivity sweeps;
- identify result-determining assumptions.

Parameter classes:

```text
externally anchored
plausible synthetic
exploratory stress parameter
unknown / pilot-required
```

Exit condition:

```text
Headline results survive reasonable parameter ranges or are explicitly bounded.
```

## Phase 5 — Pre-registration discipline

Goal:

Before running headline experiments, freeze:

- hypotheses;
- architectures;
- attacks;
- severity ranges;
- primary metrics;
- withdrawal conditions;
- reporting rules.

Example withdrawal condition:

```text
If Core v0 full architecture does not outperform the calibrated status-quo baseline on delivered verified value under medium attack severity, the headline superiority claim is withdrawn and replaced with a bounded-mechanism claim.
```

Exit condition:

```text
The main computational claims are not defined after seeing results.
```

## Phase 6 — Paper draft

Goal:

Write the satellite paper.

Suggested paper sections:

```text
1. Introduction
2. Why institutional architectures need adversarial simulation
3. Related work
4. Architectures compared
5. Agent model
6. Attack library
7. Experimental design
8. Results
9. Ablation analysis
10. Implications for distributed governance
11. Limitations
12. Reproducibility package
```

Exit condition:

```text
The paper can stand alone while pointing to the master paper as the broader architecture source.
```

## Phase 7 — Replication package

Goal:

Prepare the code and results for external review.

Package should include:

- README;
- exact run commands;
- dependency list;
- seed list;
- scenario definitions;
- generated result tables;
- figures;
- pre-registration notes;
- paper draft;
- license and citation.

Exit condition:

```text
An external reviewer can reproduce every table in the paper.
```

## Phase 8 — Migration to standalone repository

Goal:

Extract the mature experiment into its own repository.

Candidate repository name:

```text
moffermann/distributed-governance-adversarial-abm
```

Migration contents:

- paper satellite;
- simulator source code;
- experiment definitions;
- synthetic datasets or seeds;
- result tables;
- figures;
- reproduction instructions;
- license;
- citation file.

Do not migrate:

- full master corpus;
- all architecture docs;
- all attacks/defenses;
- unrelated paper drafts;
- private review material.

The standalone repository should reference the master repository as the architecture source.

## Immediate next steps

1. Decide implementation language: JavaScript to extend current simulation, or Python for analysis/plotting convenience.
2. Create a minimal executable simulator skeleton.
3. Implement three architectures: centralized, PB-like, Core v0 simplified.
4. Implement two attacks: salience cascade and weak-verification diversion.
5. Produce first paired-seed results table.
6. Expand to ablations.

## Design rule

> The first version should be small enough to run, inspect, and falsify.
