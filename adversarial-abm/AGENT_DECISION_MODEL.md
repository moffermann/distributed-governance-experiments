# Agent Decision Model

## Purpose

This document specifies how agents make decisions inside the adversarial ABM.

The simulation does not require agents to be intelligent in the human or AI sense. It requires agents to be:

- boundedly informed;
- strategically responsive;
- probabilistic;
- reproducible;
- inspectable;
- comparable across architectures.

## Core principle

An agent decision should be modeled as:

```text
agent type
+ information available
+ incentives
+ institutional architecture
+ attack pressure
+ individual noise
= probability of action
```

The same agent may behave differently under different architectures because the architecture changes information, incentives, detection, memory, and consequences.

## Information layers

The simulator should distinguish:

```text
true world state
public information
private signal
manipulated information
reviewed information
verified information
```

### True world state

Known only to the simulator.

Examples:

- latent public value;
- actual delivery quality;
- real diversion;
- true actor type;
- true collusion relationship.

### Public information

Visible to citizens or actors.

Examples:

- project title;
- project category;
- citizen-facing summary;
- funding progress;
- fiscalizer status;
- visible warnings;
- complaints;
- evidence labels;
- reputation summaries.

### Private signal

Partial, noisy information available to some agents.

Examples:

- local citizen knowledge;
- beneficiary experience;
- planner inspection signal;
- fiscalizer field observation;
- evidence producer report.

### Manipulated information

Information shaped by adversarial agents.

Examples:

- exaggerated value claim;
- input metric disguised as outcome metric;
- staged photo;
- duplicated invoice;
- salience packaging;
- false beneficiary count.

### Reviewed information

Information that has been evaluated by a process or role.

Examples:

- fiscalizer report;
- complaint review;
- evidence sufficiency status;
- corrected metric;
- verified discovery.

### Verified information

Information treated by the architecture as sufficient for a specific formal effect.

Examples:

- accepted milestone evidence;
- confirmed diversion;
- founded complaint;
- reviewed responsibility event.

## Citizen decisions

### Attentive evaluator

Attentive citizens inspect a limited sample of projects and choose according to perceived value.

Decision process:

```text
1. sample K visible projects
2. observe noisy value signal for each
3. compute perceived utility
4. allocate to the best project or softmax over top projects
```

Possible utility:

```text
U_i = perceived_value_i
    + preference_match_i
    + territory_match_i
    - risk_penalty_i
    - unresolved_warning_penalty_i
```

Where:

```text
perceived_value_i = latent_value_i + Normal(0, information_noise)
```

The architecture affects `information_noise` and `risk_penalty` through evidence visibility, deliberation context, warnings, fiscalizer status, and project maturity.

### Salience follower

Salience followers allocate according to visibility rather than evaluated value.

Decision process:

```text
1. observe top visible projects
2. compute visibility score
3. choose probabilistically by softmax
```

Visibility score:

```text
visibility_i = salience_i
             + social_proof_weight * funding_progress_i
             + urgency_boost_i
             + recommendation_boost_i
```

Architecture affects visibility through discovery rules, funding caps, visible ordering modes, urgent highlight constraints, random rotation, and discovery explainability.

### Passive citizen

Passive citizens do not actively inspect projects.

Depending on architecture, their allocation may:

- remain unused;
- follow a public default;
- follow a selected automatic profile;
- follow a delegate;
- flow to a protected assignable lane;
- return to available balance.

Decision process:

```text
if architecture.hasDefaultLayer:
    use default/profile/delegation rule
else:
    no active allocation or salience spillover depending on architecture
```

### Profile-driven citizen

Profile-driven citizens allocate through configured preferences.

Possible score:

```text
profile_score_i = value_match_i
                + territory_match_i
                + project_state_match_i
                + control_quality_i
                + near_completion_i
                - unresolved_complaint_penalty_i
                - missing_fiscalizer_penalty_i
```

They may allocate to the highest-scoring project or use softmax over eligible projects.

### Delegating citizen

Delegating citizens choose delegates according to perceived alignment and trust.

Possible delegate score:

```text
delegate_score_i = value_alignment_i
                 + role_reputation_i
                 + visibility_i
                 - concentration_warning_i
                 - related_party_warning_i
```

If the architecture does not expose concentration, the concentration warning term is absent.

## Proposer decisions

### Honest proposer

The honest proposer attempts to create a project whose declared value, metrics, evidence needs, and milestones match the real project.

Decision quality depends on:

- design competence;
- administrative burden;
- AI/form assistance where implemented;
- value-catalog clarity;
- metric requirements;
- evidence-contract requirements.

### Opportunistic proposer

The opportunistic proposer selects the strategy with the highest expected payoff.

Possible strategies:

```text
honest_design
salience_packaging
metric_gaming
milestone_gaming
evidence_light_design
hidden_relationship
```

Expected payoff:

```text
payoff_s = funding_probability_s
         * extraction_opportunity_s
         - validation_block_risk_s
         - correction_cost_s
         - expected_reputation_cost_s
         - expected_detection_cost_s
```

Strategy choice may use softmax:

```text
P(strategy s) = exp(payoff_s / tau) / sum(exp(payoff_j / tau))
```

Architecture affects payoff by increasing validation risk, evidence requirements, fiscalization, visibility of conflicts, and reputational consequences.

## Executor decisions

### Honest executor

Honest executors attempt delivery, but may fail due to difficulty, capacity, cost, or random shock.

Delivery probability:

```text
P(deliver) = sigmoid(
  ability
  - execution_difficulty
  - resource_constraint
  + support_quality
)
```

### Opportunistic executor

Opportunistic executors decide whether to deliver or divert.

Diversion probability:

```text
P(divert) = sigmoid(
  beta0
  + beta1 * fraud_gain
  - beta2 * detection_probability
  - beta3 * retained_funds
  - beta4 * guarantee
  - beta5 * reputation_loss
  - beta6 * recovery_probability
  - beta7 * future_selection_loss
)
```

Interpretation:

```text
higher fraud gain increases diversion
higher detection decreases diversion
higher retention decreases diversion
higher guarantee decreases diversion
higher reputation memory decreases diversion
```

This makes the same executor behave differently under status quo, weak PB, and Core v0.

## Fiscalizer decisions

### Honest competent fiscalizer

Detects problems with relatively high probability.

Detection probability:

```text
P(detect) = base_detection
          * competence
          * evidence_quality
          * independence
          * corroboration_factor
          * market_depth_factor
```

### Honest weak fiscalizer

Reviews sincerely but with low competence, low capacity, or weak methods.

Detection probability is lower due to lower `competence`, `capacity`, or `evidence_quality`.

### Capturable fiscalizer

May collude if expected bribe value exceeds expected loss.

Collusion probability:

```text
P(collude) = sigmoid(
  bribe_offer
  - reputation_stake
  - discovery_probability
  - legal_penalty
  - future_fee_loss
  + repeat_pairing_trust
)
```

Architecture affects collusion through:

- protocolized assignment;
- repeat-pairing visibility;
- k-corroboration;
- reputation stake;
- verified discovery;
- complaint paths.

## Evidence producer decisions

Evidence producers may be honest, weak, biased, or captured.

Evidence quality may depend on:

```text
method quality
qualification
independence
cost pressure
verification difficulty
capture pressure
```

Evidence quality:

```text
evidence_quality = producer_competence
                 * method_strength
                 * independence
                 * coverage
                 - manipulation_noise
```

Manipulated evidence probability:

```text
P(manipulated_evidence) = sigmoid(
  expected_gain
  + fraud_opportunity
  + weak_traceability
  - detection_probability
  - contradiction_probability
)
```

## Authority / planner decisions

The authority or planner constructs scopes, weights, eligibility, or project selections depending on architecture.

Planner signal:

```text
planner_signal_i = latent_value_i + Normal(0, planner_noise) + bias_i
```

Planner bandwidth:

```text
planner inspects K projects deeply
uninspected projects receive prior/default estimate
```

Agenda capture probability:

```text
P(exclude_project_i) = sigmoid(
  political_discomfort_i
  + threat_to_incumbent_i
  + aligned_competitor_pressure_i
  - visibility_cost_of_exclusion_i
)
```

Architecture affects visibility cost through public scope records, governance resolutions, timeout records, and incumbent-resistance indicators.

## Adversarial cluster decisions

Some attacks require coordinated actors rather than isolated agents.

### Clientelist broker

A broker coordinates delegation, funding, or signals.

Broker success may depend on:

```text
bloc_size
coercion_strength
proof_of_allocation_availability
protected_identity_rules
delegation_visibility
related_party_visibility
```

If individual allocations are non-exportable and preference secrecy is strong, coercive proof-based brokerage is harder.

### Collusion cluster

A proposer/executor/fiscalizer/evidence cluster coordinates to approve weak delivery.

Cluster success depends on:

```text
repeat_pairing_probability
relationship_visibility
corroboration_count
bribe_payoff
discovery_probability
```

## Choice functions

The first engine should support three generic choice functions.

### Bernoulli decision

Used for yes/no events.

```text
rng() < p
```

Examples:

- does executor divert?
- does fiscalizer detect?
- does citizen become active?

### Logistic decision

Used when probability depends on incentives.

```text
sigmoid(x) = 1 / (1 + exp(-x))
```

Examples:

- diversion;
- collusion;
- agenda exclusion;
- evidence manipulation.

### Softmax choice

Used when selecting among multiple projects, strategies, or delegates.

```text
P(i) = exp(score_i / tau) / sum(exp(score_j / tau))
```

Examples:

- salience follower choosing among visible projects;
- proposer choosing manipulation strategy;
- delegator choosing delegate.

## Architecture-dependent behavior

Agents should not have fixed behavior independent of institutional design.

Example:

```text
same opportunistic executor
+ weak audit
+ no reputation
+ high advance payment
= high diversion probability
```

But:

```text
same opportunistic executor
+ milestone gating
+ retention
+ independent fiscalization
+ reputation memory
= low diversion probability
```

This is the core purpose of the simulator.

## Decision logging

For debugging and paper transparency, the engine should optionally log sampled decisions.

Example trace:

```text
Executor E-17
Project P-09
fraud_gain: 0.42
detection_probability: 0.18
retention: 0.05
reputation_loss: 0.02
P(divert): 0.71
outcome: diverted
```

Decision traces should be optional because logging every agent at scale may be expensive.

## Design rule

> Agents should be simple enough to inspect but strategic enough to attack weak institutions.
