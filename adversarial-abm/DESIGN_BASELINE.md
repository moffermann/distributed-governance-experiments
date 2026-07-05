# Design Baseline — Adversarial ABM Satellite Paper

## Purpose

This document defines the initial research design for the adversarial agent-based modeling satellite paper.

The goal is to strengthen the master research program by turning its most attackable evidence layer — simulation — into a dedicated, reproducible computational research artifact.

## Working title

**Adversarial Agent-Based Simulation for Public Resource Allocation: Stress-Testing Centralized, Participatory, and Distributed Governance Architectures**

## Core thesis

Public-resource allocation systems should be evaluated under adversarial institutional conditions, not only under average or well-behaved participation.

A useful institutional simulator should compare alternative architectures under the same:

- agents;
- resources;
- information constraints;
- strategic attacks;
- verification limits;
- outcome metrics.

## Research question

```text
How do different public-resource allocation architectures perform when exposed to the same adversarial agents, information constraints, institutional weaknesses, and strategic manipulation scenarios?
```

## Secondary questions

1. Which mechanisms reduce delivered-value loss under manipulation?
2. Which mechanisms merely reduce visible concentration without improving project quality?
3. Which mechanisms shift risk from allocation to execution, verification, or agenda-setting?
4. Which Core v0 mechanisms are load-bearing?
5. Which assumptions are result-determining?
6. Under what adversarial conditions does Core v0 fail?
7. Which failure modes should become pilot instrumentation requirements?

## Main comparison logic

The simulation should not compare Core v0 to an artificially weak strawman.

It should compare:

```text
same project world
same citizen population
same adversarial agents
same budget
same attack library
same evaluation metrics
multiple institutional architectures
```

The institutional architecture is the treatment variable.

## Starting point from existing work

The current master paper already includes agent-based simulations involving:

- citizen attention constraints;
- salience-driven allocation;
- default allocation layers;
- funding-target closure;
- distributed signal aggregation;
- delivered social value;
- calibrated audit baseline;
- reputation and visibility effects.

This satellite paper should not merely repeat those results. It should generalize them into a formal adversarial simulation framework.

## Proposed paper structure

```text
1. Introduction
2. Why institutional architectures need adversarial simulation
3. Related work
4. Institutional architectures compared
5. Agent model
6. Attack library
7. Experimental design
8. Results
9. Ablation analysis
10. Implications for distributed governance
11. Limitations
12. Reproducibility package
```

## Research contribution

The contribution should be framed as computational institutional design:

```text
A reusable adversarial ABM framework for comparing public-resource allocation architectures before real-world deployment.
```

The paper should contribute:

1. a structured set of institutional architectures;
2. an adversarial agent taxonomy;
3. an institutional attack library;
4. a delivered-value metric family;
5. ablation methods for institutional mechanisms;
6. a reproducible simulation package.

## Core methodological discipline

### 1. Common-world comparison

Every architecture should be tested on the same generated project world and actor population for each seed.

### 2. Paired-seed design

Comparisons should use paired seeds wherever possible so outcome differences are attributable to institutional rules rather than random worlds.

### 3. Architecture as treatment

The institutional design is the treatment. Agents and attack pressure should remain fixed unless explicitly varied.

### 4. Ablation before headline claim

The model should report what happens when mechanisms are removed:

- no default layer;
- no milestone gating;
- no fiscalizer independence;
- no reputation memory;
- no funding caps;
- no agenda transparency;
- no evidence contract;
- no discovery controls.

### 5. Failure is a result

If Core v0 fails under a plausible adversarial scenario, the result should be preserved and used to:

- bound the claim;
- define a pilot instrumentation requirement;
- create a future attack/resolution in the master corpus if needed.

## Baseline architectures

The first version should compare at least:

1. centralized status quo with audit-after-the-fact;
2. participatory budgeting without delivery verification;
3. citizen allocation without strong fiscalization;
4. strong verification without distributed allocation;
5. Core v0 partial architecture;
6. Core v0 full architecture;
7. Core v0 with captured agenda;
8. Core v0 with distributed agenda signals.

See `ARCHITECTURES.md`.

## Adversarial scenarios

The first attack library should include:

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

See `AGENTS_AND_ATTACKS.md`.

## Primary outcome metric

The primary metric should be:

```text
delivered verified social value per unit of public budget
```

This is preferred over:

- number of projects funded;
- reported completion;
- participation rate;
- formal compliance;
- administrative activity.

The system exists to deliver value, not merely allocate money or produce reports.

## Evidence-status discipline

The paper must distinguish:

```text
formal proof under assumptions
simulation evidence
calibrated parameter support
empirical pilot evidence
legal feasibility
```

This satellite paper will produce simulation evidence, not pilot evidence.

## First implementation strategy

Start with a minimal dependency-free simulation, ideally in JavaScript or Python.

Recommended initial modules:

```text
world generation
agent generation
architecture rules
attack scenarios
metrics
experiment runner
result table generator
```

The first implementation should favor clarity and reproducibility over realism.

## Publication strategy

The paper should be written as a satellite paper, not as a replacement for the master paper.

Suggested framing:

```text
This paper develops the computational stress-testing layer of a broader research program on distributed public project governance.
```

## Success criteria for v0

The first useful version succeeds if it can answer:

1. Does Core v0 outperform weaker architectures under neutral assumptions?
2. Which mechanisms explain the difference?
3. Under which adversarial scenarios does Core v0 fail?
4. Which assumptions dominate results?
5. What must a real pilot measure because simulation cannot settle it?

## Design rule

> Do not make the model impressive by making the adversary weak.
