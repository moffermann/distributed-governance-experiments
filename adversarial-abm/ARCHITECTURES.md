# Architectures to Compare

## Purpose

This document defines the institutional architectures that the adversarial ABM should compare.

The goal is not to make Core v0 defeat a strawman. The goal is to compare architectures under equivalent worlds, equivalent agents, equivalent attacks, and equivalent metrics.

## Architecture comparison principle

Each architecture should be represented as a set of rules over the same generated public-project world.

The treatment variable is:

```text
institutional architecture
```

not:

```text
different citizens
different projects
different adversaries
different budgets
different randomness
```

## Architecture A0 — Centralized status quo with audit-after-the-fact

### Description

A central authority selects projects, assigns budgets, execution proceeds under ordinary administrative controls, and audit operates after or during execution at limited intensity.

### Core features

- central agenda construction;
- central project selection;
- limited citizen allocation;
- audit-after-the-fact;
- weak or delayed reputational memory;
- completion is often self-reported or administratively reported;
- detection probability is limited;
- consequences are delayed or partial.

### Main vulnerabilities

- planner bandwidth limit;
- discretionary allocation;
- weak delivery visibility;
- audit intensity too low to deter diversion;
- reported completion may exceed real delivered value;
- political or bureaucratic selection bias.

### Metrics of interest

- delivered value;
- visibility gap;
- diversion rate;
- planner quality-selection correlation;
- audit detection rate;
- real versus reported completion.

## Architecture A1 — Participatory budgeting without strong delivery verification

### Description

Citizens or assemblies select projects, but execution and delivery verification remain weakly linked to allocation.

### Core features

- citizen input or voting;
- limited budget share;
- high salience effects;
- weak milestone-gated release;
- weak evidence contract;
- ordinary audit or administrative follow-up.

### Main vulnerabilities

- popularity over value;
- capture by organized minorities;
- participation decay;
- allocation-delivery gap;
- citizen attention limits;
- weak feedback from execution to future selection.

### Metrics of interest

- selection quality;
- participation sensitivity;
- salience concentration;
- completion versus delivered value;
- persistence of bad executors.

## Architecture A2 — Citizen allocation without strong fiscalization

### Description

Citizens allocate funding to projects directly or continuously, but execution controls remain weak.

### Core features

- individual allocation;
- project discovery layer;
- funding caps may or may not exist;
- weak milestone validation;
- weak independent fiscalization;
- weak evidence producer layer;
- limited consequences for poor delivery.

### Main vulnerabilities

- salience cascades;
- funding projects that later leak value;
- low-quality evidence;
- executor opportunism;
- manipulation of project cards or value claims.

### Metrics of interest

- quality selection;
- delivered value gap;
- leakage;
- funding concentration;
- false legitimacy from funding volume.

## Architecture A3 — Strong verification without distributed allocation

### Description

The central authority still selects projects, but execution uses stronger evidence contracts, fiscalization, milestone-gated disbursement, and reputational consequences.

### Core features

- central selection;
- strong milestone gating;
- independent fiscalization;
- evidence-linked disbursement;
- reputation memory;
- improved visibility.

### Main vulnerabilities

- agenda and selection remain centralized;
- planner bandwidth limit persists;
- delivered value improves only for centrally selected projects;
- citizens do not direct allocation.

### Metrics of interest

- delivered value conditional on project selection;
- reduction in diversion;
- visibility gap;
- loss from poor selection despite good delivery controls.

## Architecture A4 — Distributed allocation without default layer

### Description

Citizens allocate directly, but inactive or inattentive citizens are not routed through a high-quality default, delegation, or profile layer.

### Core features

- manual allocation;
- salience-driven discovery;
- little or no automatic profile support;
- limited fallback for non-participation.

### Main vulnerabilities

- rational ignorance;
- participation decay;
- salience capture;
- concentration in visible projects;
- weak resilience at scale.

### Metrics of interest

- delivered value under participation decay;
- salience concentration;
- quality selection as attention falls;
- inactive-budget loss or misdirection.

## Architecture A5 — Core v0 without reputation memory

### Description

Core v0 uses conditional disbursement and fiscalization, but actor history does not persist strongly into future funding or review decisions.

### Core features

- evidence contracts;
- milestone gating;
- independent fiscalization;
- no durable role-specific reputation;
- weak future consequence for confirmed poor performance.

### Main vulnerabilities

- audit detects but does not deter sufficiently;
- repeat poor performers remain viable;
- visibility gap may shrink, but real delivery may not improve enough;
- accountability without memory becomes bookkeeping.

### Metrics of interest

- repeat offender share;
- diversion rate;
- detection without deterrence;
- delivered value;
- executor pool quality over time.

## Architecture A6 — Core v0 without fiscalizer independence

### Description

Core v0 structure exists, but fiscalizers can be selected, paid, or repeatedly paired by executors or related actors.

### Core features

- project lifecycle and evidence contracts exist;
- fiscalization exists formally;
- independence is compromised;
- repeat relationships are not controlled.

### Main vulnerabilities

- collusion;
- rubber-stamp fiscalization;
- formal compliance without real detection;
- false confidence from audit labels.

### Metrics of interest

- collusion success rate;
- false approval rate;
- visibility gap;
- detection probability decay;
- delivered value loss.

## Architecture A7 — Core v0 with centralized agenda in tutored mode

### Description

Core v0 operates with strong downstream mechanisms, but planning scopes and need weights are constructed by the implementing authority.

### Core features

- strong project lifecycle;
- conditional disbursement;
- fiscalization;
- reputation;
- citizen allocation inside authority-defined planning scopes;
- centralized scope construction.

### Main vulnerabilities

- agenda capture;
- exclusion of uncomfortable project classes;
- informational quality of planning vector dominates passive allocation;
- distributed allocation occurs inside a pre-filtered frame.

### Metrics of interest

- loss from agenda bias;
- passive-flow dependence on weight vector quality;
- delivered value under captured versus competent agenda;
- citizen correction share.

## Architecture A8 — Core v0 with distributed agenda signals

### Description

Core v0 uses aggregated citizen, beneficiary, expert, and local signals to construct or update planning weights, subject to protocolized aggregation and anti-capture controls.

### Core features

- strong downstream mechanisms;
- citizen allocation;
- open or semi-open scope-signal aggregation;
- visible planning weights;
- contestable agenda construction;
- signal quality and bias explicitly modeled.

### Main vulnerabilities

- coordinated signal bias;
- clientelist signal capture;
- misinformation;
- uneven signal coverage;
- aggregation institution failure.

### Metrics of interest

- selection quality versus central planning;
- robustness to biased signals;
- threshold where distributed signals lose to competent central planner;
- delivered value after agenda correction.

## Architecture A9 — Core v0 full architecture

### Description

The full reference architecture for the model under test.

### Core features

- mandate-bound planning scopes;
- value thesis and metrics;
- evidence contracts;
- funding commitments;
- funding-target closure;
- independent fiscalization;
- milestone-gated disbursement;
- retention and guarantees;
- role-specific reputation;
- visible audit trail;
- discovery controls;
- complaint and correction paths;
- concentration observability.

### Main vulnerabilities

- complexity;
- thin verifier markets;
- agenda-setting in transition modes;
- adoption incentives;
- strategic gaming of metrics or evidence;
- reputation lock-in if poorly constrained.

### Metrics of interest

- delivered verified value per budget;
- leakage;
- visibility gap;
- selection quality;
- execution quality;
- concentration;
- administrative load;
- robustness across attacks.

## Ablation matrix

The simulator should support toggling mechanisms:

| Mechanism | Expected role | Failure when removed |
|---|---|---|
| Funding-target closure | Reduce funding concentration | Salience cascades absorb funds |
| Default / profile layer | Buffer rational ignorance | Participation decay damages allocation |
| Distributed signal aggregation | Improve planning weights | Central planner bandwidth dominates |
| Evidence contract | Tie value to proof | Vague promises survive |
| Milestone gating | Prevent early fund capture | Disbursement gaming |
| Retention / recovery | Keep stake at risk | Diversion becomes cheap |
| Independent fiscalization | Improve detection | Rubber-stamp compliance |
| k-corroboration | Resist collusion | Thin fiscalizer pools collapse |
| Reputation memory | Make consequences persist | Audit becomes bookkeeping |
| Discovery explainability | Reduce hidden allocation | Interface becomes covert allocator |
| Concentration observability | Detect capture | Delegates/executors lock in |

## Design rule

> Every architecture must be allowed to fail and allowed to win under some parameter range.

If one architecture wins everywhere, the model is probably too friendly or too coarse.
