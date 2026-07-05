# Technical Engine Design — Adversarial ABM

## Purpose

This document specifies how the adversarial ABM should be implemented technically.

It complements the conceptual design documents by answering engineering questions:

- whether to use an ABM framework;
- whether agents are threads;
- whether agents use AI;
- how the simulation is scheduled;
- how state is represented;
- how architectures and attacks plug into the engine;
- how reproducibility is preserved.

## Core technical decision

The first version should be a deterministic, discrete-cycle simulation engine with agents represented as data plus decision policies.

It should not begin as:

- one thread per agent;
- a real-time actor system;
- a multi-process environment;
- an LLM-agent environment;
- a black-box ABM framework.

## Recommended implementation language

Start with JavaScript / Node.js, consistent with the existing dependency-free simulation style in `scripts/simulation/allocation-sim.mjs`.

Recommended properties:

```text
Node.js
ES modules
no required runtime dependencies in v0
seeded deterministic PRNG
JSON/CSV/Markdown outputs
```

Python may be added later for analysis, plots, statistical tables, or notebooks.

## Why not start with a large ABM framework?

ABM frameworks are useful, but the first paper needs maximum transparency.

The first engine should keep institutional rules visible in source code instead of hiding behavior behind framework conventions.

Reasons:

1. institutional architecture is the treatment variable;
2. every rule must be inspectable;
3. every run must be exactly reproducible;
4. every result should be explainable in the paper;
5. reviewers should not need to learn a specialized ABM environment to inspect the logic.

A future version may evaluate Mesa, Repast, NetLogo, GAMA, or another ABM framework if the experiment grows beyond the simple engine.

## Agent representation

Agents should be represented as records in memory, not as threads.

Example:

```text
Citizen {
  id
  type
  territory
  value_preferences
  attention_budget
  signal_quality
  profile_rule
  delegation_state
}
```

Behavior should be defined by policy functions:

```text
decideCitizenAllocation(citizen, visible_projects, architecture, rng)
decideExecutorAction(executor, project, architecture, attack, rng)
decideFiscalizerReview(fiscalizer, evidence, architecture, attack, rng)
```

This separates:

```text
agent state
from
agent decision policy
```

## Threads and parallelism

Do not model agents as threads.

Bad design:

```text
10,000 citizens = 10,000 threads
```

Good design:

```text
10,000 citizens = array of records processed by deterministic loops
```

Parallelism, if needed later, should happen at the run or seed level:

```text
worker 1 runs seed 1
worker 2 runs seed 2
worker 3 runs seed 3
```

The unit of parallel execution is the simulation run, not the individual agent.

## AI agents

The first version should not use LLM-backed or AI-backed agents.

Agents should begin as transparent, parametric decision models:

- heuristics;
- probability distributions;
- utility functions;
- thresholds;
- softmax choices;
- logistic decisions.

Reason:

```text
A deterministic parametric model is easier to reproduce, inspect, criticize, and falsify than an LLM-agent environment.
```

AI may be added later as an extension for:

- generating synthetic project proposals;
- generating adversarial strategies;
- stress-testing metric gaming;
- producing human-readable traces;
- simulating adaptive adversarial behavior.

But AI must not be required for the first computational claims.

## Simulation type

The engine should be a discrete-time, cycle-based simulation.

Typical cycle:

```text
1. planning / scope construction
2. project publication and visibility update
3. discovery surface computation
4. citizen allocation
5. funding closure
6. executor delivery/diversion decision
7. evidence generation
8. fiscalizer review
9. disbursement / retention / recovery
10. reputation and responsibility update
11. metric recording
```

A cycle may represent one month, matching the current master simulation style.

## Common-world comparison

The engine must generate the world once per seed and run every architecture against that same world.

```text
world = generateWorld(seed)
agents = generateAgents(seed)

for architecture in architectures:
    sim = clone(world, agents)
    run(sim, architecture)
```

This prevents accidental comparison between different worlds.

## Determinism requirements

The simulator must be deterministic under:

```text
same seed
same scenario config
same architecture
same code version
```

Therefore v0 should avoid:

- `Math.random()`;
- `Date.now()` inside simulation logic;
- external API calls;
- nondeterministic thread ordering;
- LLM calls;
- hidden global state.

All randomness should flow from a seeded PRNG.

## Suggested module structure

```text
experiments/adversarial-abm/src/
  index.mjs

  core/
    rng.mjs
    scheduler.mjs
    cloneWorld.mjs
    config.mjs
    output.mjs

  world/
    generateWorld.mjs
    generateProjects.mjs
    generateAgents.mjs

  agents/
    citizenPolicies.mjs
    proposerPolicies.mjs
    executorPolicies.mjs
    fiscalizerPolicies.mjs
    authorityPolicies.mjs
    adversaryPolicies.mjs

  architectures/
    statusQuo.mjs
    participatoryBudgeting.mjs
    coreV0Simple.mjs
    coreV0Full.mjs

  attacks/
    salienceCascade.mjs
    weakVerificationDiversion.mjs
    fiscalizerCollusion.mjs
    agendaCapture.mjs

  metrics/
    deliveredValue.mjs
    selectionQuality.mjs
    leakage.mjs
    visibilityGap.mjs
    concentration.mjs

  experiments/
    e1_baselineComparison.mjs
    e2_ablation.mjs
    e3_attackStress.mjs

  scenarios/
    baseline-medium.json
    high-salience.json
    weak-verification.json
```

## State model

The engine should distinguish five kinds of state.

### 1. World state

Generated once per seed.

Includes:

- projects;
- territories;
- latent public values;
- salience;
- verification difficulty;
- fraud opportunity;
- baseline actor pools.

### 2. Agent state

Generated once per seed.

Includes:

- citizens;
- proposers;
- executors;
- fiscalizers;
- evidence producers;
- authority/planner;
- adversarial clusters.

### 3. Architecture state

Defined by each institutional model.

Includes toggles such as:

- citizen allocation;
- default layer;
- funding caps;
- evidence contract;
- milestone gating;
- fiscalization independence;
- reputation memory;
- discovery explainability.

### 4. Attack state

Defined by scenario severity.

Includes:

- social-proof strength;
- opportunist share;
- signal bias;
- verifier market thinness;
- collusion pressure;
- agenda capture intensity.

### 5. Runtime state

Changes during a run.

Includes:

- project funding;
- milestone status;
- execution state;
- evidence state;
- disbursement state;
- fiscalizer assignments;
- reputation summaries;
- recorded metrics.

## Architecture interface

Each architecture should expose a common interface.

Example:

```text
Architecture {
  name
  rules
  constructScope(sim)
  publishProjects(sim)
  rankProjects(sim)
  allocate(sim)
  closeFunding(sim)
  executeProjects(sim)
  reviewEvidence(sim)
  disburse(sim)
  updateReputation(sim)
}
```

In early versions, some functions may be shared across architectures and controlled by rule flags.

## Attack interface

Each attack should expose a common interface.

Example:

```text
Attack {
  name
  severity
  parameters
  modifyWorld(world)
  modifyAgents(agents)
  modifyDecisionContext(context)
  modifyPayoffs(payoffs)
  recordAttackMetrics(sim)
}
```

An attack should not secretly rewrite results. It should change incentives, information, or behavior before actions occur.

## Output formats

The first version should produce:

```text
results/raw/*.json
results/tables/*.md
results/tables/*.csv
```

Later versions may produce figures.

## Minimum viable engine

The first executable version should implement:

- seeded world generation;
- 10,000 citizens;
- 40 active projects;
- 24 cycles;
- three architectures;
- two attacks;
- delivered-value metric;
- leakage metric;
- visibility-gap metric;
- concentration metric;
- paired-seed results table.

## Technical non-goals for v0

Do not implement in v0:

- a UI;
- database storage;
- real API integration;
- true multi-threaded agent runtime;
- LLM agents;
- interactive visualization;
- full country/legal simulation;
- every Core v0 object.

## Engineering rule

> The first engine should be small enough to understand, deterministic enough to reproduce, and modular enough to attack.
