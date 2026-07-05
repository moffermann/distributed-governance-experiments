# Agents and Attack Library

## Purpose

This document defines the first adversarial agent taxonomy and attack library for the ABM satellite paper.

The simulation should not model citizens only. Public-resource allocation fails through strategic actors, weak verification, organizational incentives, and institutional capture.

## Agent taxonomy

### Citizen agents

#### Attentive evaluators

Citizens who inspect a limited sample of projects and allocate to the best perceived option.

Key parameters:

- attention budget;
- project sample size;
- signal quality;
- preference vector;
- tolerance for risk;
- trust in default layer.

#### Passive citizens

Citizens who do not actively inspect projects and whose allocation flows through default, profile, delegation, or remains inactive depending on architecture.

Key parameters:

- default acceptance probability;
- profile configuration probability;
- delegation probability;
- inactivity persistence.

#### Salience followers

Citizens whose choices are dominated by visibility, popularity, urgency, or social proof.

Key parameters:

- salience sensitivity;
- social-proof elasticity;
- discovery exposure;
- responsiveness to funding progress.

#### Profile-driven citizens

Citizens who configure automatic allocation profiles.

Key parameters:

- value preferences;
- territorial preferences;
- risk/control preferences;
- fallback rules;
- update frequency.

#### Delegating citizens

Citizens who delegate allocation within a scope.

Key parameters:

- delegate selection rule;
- revocation probability;
- concentration tolerance;
- trust decay after poor outcomes.

### Project-side agents

#### Honest proposer

Creates projects with sincere value claims and reasonable evidence structure.

Key parameters:

- design competence;
- metric quality;
- evidence awareness;
- administrative capacity.

#### Opportunistic proposer

Creates projects optimized for funding visibility or weak verification rather than delivered value.

Key parameters:

- salience optimization;
- metric gaming skill;
- willingness to hide risks;
- responsiveness to validation gates.

#### Honest executor

Executes project milestones with effort and cost.

Key parameters:

- ability;
- cost structure;
- liquidity needs;
- sensitivity to reputation;
- failure probability.

#### Opportunistic executor

Chooses between delivery and diversion depending on expected detection and stake at risk.

Key parameters:

- diversion gain;
- delivery cost;
- detection belief;
- guarantee burden;
- reputation loss sensitivity.

### Control-side agents

#### Honest fiscalizer

Reviews evidence and execution against accepted rules.

Key parameters:

- competence;
- review capacity;
- detection probability;
- independence;
- cost.

#### Capturable fiscalizer

May rubber-stamp or collude when expected bribe value exceeds expected loss.

Key parameters:

- reputation stake;
- bribe threshold;
- post-approval discovery probability;
- repeat-pairing exposure;
- market scarcity.

#### Evidence producer

Produces corroborating evidence, field observations, technical reports, beneficiary confirmations, or counter-evidence.

Key parameters:

- method quality;
- independence;
- cost;
- qualification;
- false-evidence risk.

#### Reviewer / authority agent

Acts in tutored mode, admissibility review, or administrative resolution.

Key parameters:

- review capacity;
- bias;
- timeout rate;
- rejection rule;
- incumbent-protection tendency.

### Adversarial network agents

#### Clientelist broker

Coordinates funding, delegation, or signals toward related projects in exchange for off-platform benefits.

Key parameters:

- coordination capacity;
- beneficiary bloc size;
- detection risk;
- related-party exposure;
- coercion intensity.

#### Collusion cluster

A group of proposer/executor/fiscalizer/evidence agents that coordinate to extract funds or approve weak delivery.

Key parameters:

- cluster size;
- relationship visibility;
- repeat-pairing probability;
- bribe cost;
- discovery risk.

#### Agenda-capturing incumbent

Controls planning scopes, eligibility, default weights, or administrative admissibility to shape what can be funded.

Key parameters:

- scope bias;
- exclusion rate;
- timeout strategy;
- protected-favorite share;
- public visibility cost.

## Attack library

### A1 — Salience cascade

Visible projects attract more funding because they are visible, not because they are valuable.

Mechanism:

```text
high salience → early funding → higher discovery rank → more funding
```

Architectural defenses to test:

- funding-target closure;
- random rotation;
- visible ordering modes;
- default layer;
- discovery explainability;
- salience-bias observability.

Key metrics:

- funding concentration;
- top-salience share;
- selection quality;
- delivered value.

### A2 — Metric gaming

A proposer declares metrics that are easy to satisfy but do not measure the promised value.

Example:

```text
Promised value: sports participation.
Metric: buy 100 balls.
```

Architectural defenses to test:

- value thesis;
- mandatory value metrics;
- evidence coverage validation;
- fiscalizer review;
- closure accountability.

Key metrics:

- input-metric rate;
- value-delivery gap;
- false completion rate;
- metric rejection/correction rate.

### A3 — Milestone gaming

An executor or designer structures disbursement milestones to release money before meaningful evidence exists.

Examples:

```text
60% release on project start.
Partial release allowed without formula.
Advance payment without supplier protection.
```

Architectural defenses to test:

- milestone validation;
- protected advance treatment;
- retention;
- evidence-linked release;
- no partial release without formula.

Key metrics:

- early unrecoverable release;
- diversion before detection;
- blocked high-risk milestones;
- honest-executor exclusion rate.

### A4 — Fiscalizer collusion

Fiscalizers approve non-delivered milestones in exchange for bribes or future work.

Mechanism:

```text
executor gain from false approval > expected fiscalizer loss + discovery risk
```

Architectural defenses to test:

- protocolized assignment;
- k-corroboration;
- repeat-pairing visibility;
- fiscalizer reputation stake;
- verified discovery.

Key metrics:

- false approval rate;
- collusion success rate;
- detection rate;
- cost of control;
- delivered value.

### A5 — Evidence manipulation

Actors submit misleading, duplicated, forged, or low-context evidence.

Examples:

```text
same invoice used twice;
photo proves activity occurred but not attendance;
beneficiary confirmation coerced;
metadata inconsistent with claimed date.
```

Architectural defenses to test:

- contextualized evidence;
- material information claims;
- evidence producer qualification;
- contradiction paths;
- complaint review;
- AI anomaly signals where implemented.

Key metrics:

- false evidence accepted;
- contradiction discovery rate;
- correction before disbursement;
- evidentiary sufficiency.

### A6 — Clientelist brokerage

A broker coordinates citizens, delegates, or beneficiaries to route allocation toward related projects.

Mechanism:

```text
broker influence → bloc allocation/delegation → related project funding → off-platform benefit
```

Architectural defenses to test:

- real identity with protected privacy;
- delegation concentration visibility;
- related-party disclosure;
- participation-support transparency;
- complaint path;
- no exportable proof of individual allocation.

Key metrics:

- bloc concentration;
- related-project funding share;
- delegation concentration;
- detection/visibility of patterns;
- delivered value loss.

### A7 — Incumbent agenda capture

The authority defines planning scopes, eligibility rules, default weights, or admissibility decisions to exclude unwanted projects or favor aligned actors.

Architectural defenses to test:

- public planning scope;
- allocation mandate record;
- visible governance resolution;
- timeout resolution;
- incumbent-resistance indicators;
- open agenda-signal construction.

Key metrics:

- excluded-value loss;
- scope bias;
- rejection and timeout rates;
- delivered value under biased scope;
- citizen correction share.

### A8 — Coordinated signal bias

An organized group contaminates open agenda construction or project signals.

Architectural defenses to test:

- signal aggregation rules;
- source diversity requirements;
- bias sensitivity analysis;
- expert/citizen hybrid weighting;
- anomaly surfaces.

Key metrics:

- planning-weight distortion;
- selection quality under bias;
- threshold where distributed signals lose to central planner;
- delivered value degradation.

### A9 — Thin verifier market

Few qualified fiscalizers or evidence producers are available, causing repeated assignments, low independence, or high cost.

Architectural defenses to test:

- k-corroboration;
- remote or cross-territory fiscalization;
- stronger guarantees where detection is weak;
- thin-market indicator;
- proportional threshold policies.

Key metrics:

- detection probability;
- repeat assignment concentration;
- cost of control;
- honest-executor exclusion from high guarantees;
- collusion vulnerability.

### A10 — Reputation lock-in

Reputation-weighted selection concentrates work in early winners faster than it discovers real ability.

Architectural defenses to test:

- opportunity-normalized reputation;
- concentration visibility;
- entrant floors;
- non-exclusion rule;
- reputation decay;
- role-specific reputation instead of universal score.

Key metrics:

- executor assignment Gini;
- correlation between reputation and true ability;
- entrant survival;
- delivered value;
- concentration without quality gain.

## Attack severity dimensions

Each attack scenario should vary by severity:

```text
low
medium
high
extreme
```

Severity may affect:

- adversary share;
- coordination quality;
- corruption payoff;
- evidence falsification skill;
- detection difficulty;
- authority bias;
- market thinness;
- signal bias.

## Result interpretation rule

A defense is not successful merely because the attack is detected.

The simulator should distinguish:

```text
attack prevented
attack detected before harm
attack detected after harm
attack visible but unresolved
attack hidden
attack falsely accused
```

## Design rule

> The attack library should make institutional failure legible, not make the proposed architecture look good.
