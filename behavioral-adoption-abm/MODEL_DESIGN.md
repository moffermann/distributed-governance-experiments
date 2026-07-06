# Model Design

## Purpose

This document defines the first technical design for the behavioral adoption ABM.

The goal is to model how people and role-bearing actors move through Core v0 states: awareness, registration, activation, participation, delegation, role adoption, trust change, abandonment, and reactivation.

## Modeling boundary

This experiment is not the architecture-performance model. It is the behavioral parameter generator that should eventually feed that model.

The model should answer:

```text
Given a platform design, friction profile, trust environment, social network, incentives, and outcome history,
what behavioral population emerges?
```

## Candidate implementation stack

Recommended first implementation:

```text
Python
Mesa or a lightweight custom ABM engine
pandas for result tables
numpy for deterministic random sampling
matplotlib or plotly for figures
YAML/JSON scenario configuration
```

Mesa is a strong candidate because it provides a natural structure for explicit agents, model scheduling, data collection, and experiment sweeps. The first implementation should avoid overengineering and prioritize inspectability.

## Core entities

### BehavioralModel

The top-level simulation model.

Responsibilities:

- initialize population;
- initialize social graph;
- initialize projects and role markets;
- load scenario parameters;
- run ticks;
- collect metrics;
- export integration outputs.

### CitizenAgent

Represents a potential or actual Core user.

State variables:

```text
awareness_state: unaware | aware
registration_state: unregistered | registered
use_state: inactive | direct_active | profile_driven | delegated | hybrid | abandoned
trust_core: float
trust_delegates: dict
trust_evidence: float
trust_fiscalization: float
digital_confidence: float
civic_interest: float
risk_aversion: float
privacy_concern: float
friction_tolerance: float
social_influence_weight: float
attention_budget: float
need_relevance: float
ideological_openness: float
```

Actions:

```text
become_aware()
decide_register()
decide_activate()
decide_participation_mode()
choose_delegate()
configure_profile()
participate_directly()
update_trust()
decide_abandon()
decide_reactivate()
recommend_or_discourage()
```

### DelegateAgent

Represents a person or organization that can receive delegated participation.

State variables:

```text
reputation
visibility
alignment_vector
competence
conflict_risk
capture_risk
delegated_weight
performance_history
explanation_quality
```

Actions:

```text
publish_thesis()
receive_delegation()
allocate_delegated_weight()
lose_delegation()
update_reputation()
```

### ProjectAgent

Represents a proposal or project visible inside Core.

State variables:

```text
latent_value
perceived_value
salience
category
territory
claim_quality
metric_quality
evidence_requirement
fiscalization_requirement
funding_progress
controversy_level
outcome_state
```

Actions:

```text
be_discovered()
receive_allocation()
progress_milestone()
generate_outcome()
trigger_complaint_or_confirmation()
```

### ExecutorAgent

Represents actors willing to execute projects.

State variables:

```text
honesty_type: honest | opportunistic | mixed
ability
cost_structure
liquidity_constraint
reputation_stake
future_selection_value
opportunism_gain
detection_belief
```

Actions:

```text
decide_participate()
bid_or_accept_project()
deliver()
delay()
divert()
update_reputation()
```

### FiscalizerAgent

Represents verification and control actors.

State variables:

```text
competence
independence
capacity
cost
capture_risk
reputation_stake
detection_probability
false_positive_tendency
false_negative_tendency
```

Actions:

```text
decide_participate()
accept_review()
inspect_evidence()
approve_or_flag()
collude_or_refuse()
update_reputation()
```

### EvidenceProducerAgent

Represents actors who produce evidence, counter-evidence, field reports, measurements, beneficiary confirmations, or technical reports.

State variables:

```text
method_quality
independence
coverage
cost
qualification
capture_risk
false_evidence_risk
```

Actions:

```text
decide_participate()
produce_evidence()
produce_counter_evidence()
corroborate()
manipulate_or_refuse()
update_reputation()
```

### PlatformAgent / Environment

Represents platform-level conditions rather than a person.

State variables:

```text
onboarding_friction
interface_complexity
ai_tutor_quality
privacy_guarantee_strength
public_legitimacy
outage_rate
controversy_rate
communication_quality
incentive_strength
rule_change_frequency
```

Actions:

```text
run_campaign()
create_public_event()
apply_outage()
apply_rule_change()
apply_trust_recovery_event()
```

## Time step

A tick should initially represent one week.

Rationale:

- awareness and registration do not usually change minute by minute;
- trust and abandonment need repeated experience;
- project execution and evidence cycles are slower than UI interactions;
- weekly ticks allow multi-year simulations without excessive runtime.

Alternative tick sizes can be tested later.

## Scheduling order

Recommended first scheduling order per tick:

```text
1. Platform events occur
2. Unaware citizens may become aware
3. Aware non-users decide whether to register
4. Registered inactive users decide whether to activate
5. Active users choose/update participation mode
6. Delegators choose/update/revoke delegates
7. Delegates allocate delegated weight
8. Project-side demand appears
9. Executors decide whether to participate and deliver
10. Fiscalizers and evidence producers decide whether to participate
11. Evidence and verification outcomes are generated
12. Citizens observe public/private/social signals
13. Trust updates
14. Abandonment/reactivation decisions occur
15. Metrics are collected
```

## Decision model

Use simple inspectable probabilistic functions before adding complexity.

### Registration probability

```text
P(register) = sigmoid(
    beta0
  + beta1 * perceived_benefit
  + beta2 * social_proof
  + beta3 * trust_core
  + beta4 * need_relevance
  + beta5 * ai_tutor_quality
  - beta6 * onboarding_friction
  - beta7 * privacy_concern
  - beta8 * ideological_resistance
)
```

### Activation probability

```text
P(activate) = sigmoid(
    beta0
  + beta1 * decision_clarity
  + beta2 * perceived_agency
  + beta3 * trust_core
  + beta4 * visible_successes
  + beta5 * ai_tutor_quality
  - beta6 * interface_complexity
  - beta7 * attention_cost
)
```

### Participation-mode choice

Use softmax over modes:

```text
direct_active
profile_driven
partial_delegation
full_delegation
inactive
```

Mode score examples:

```text
direct_score = civic_interest + control_preference + attention_budget + information_quality - complexity_cost
profile_score = automation_trust + preference_clarity + convenience_need - control_anxiety
delegation_score = trusted_delegate_available + low_attention + alignment_signal - concentration_warning
inactive_score = apathy + complexity_cost + distrust - urgency
```

### Abandonment probability

```text
P(abandon) = sigmoid(
    beta0
  + beta1 * unresolved_complaints
  + beta2 * bad_outcome_exposure
  + beta3 * platform_friction
  + beta4 * perceived_capture
  + beta5 * privacy_concern
  - beta6 * trust_core
  - beta7 * visible_successes
  - beta8 * social_support
)
```

### Fiscalizer participation probability

```text
P(fiscalizer_participates) = sigmoid(
    beta0
  + beta1 * compensation
  + beta2 * reputation_gain
  + beta3 * mission_alignment
  + beta4 * professional_fit
  - beta5 * review_cost
  - beta6 * legal_or_reputation_risk
)
```

### Evidence producer participation probability

```text
P(evidence_producer_participates) = sigmoid(
    beta0
  + beta1 * compensation
  + beta2 * reputation_gain
  + beta3 * method_fit
  + beta4 * beneficiary_access
  - beta5 * production_cost
  - beta6 * intimidation_or_capture_pressure
)
```

## Social graph

The first model should use a synthetic graph.

Recommended options:

1. random graph for baseline;
2. small-world graph for social diffusion;
3. scale-free graph for influencer/delegate concentration risk;
4. segmented graph for territorial or ideological clusters.

The social graph affects:

- awareness diffusion;
- social proof;
- trust updates;
- delegate discovery;
- negative word of mouth;
- recommendation cascades;
- controversy spread.

## Scenario parameters

Each scenario should define:

```text
population_size
initial_awareness
initial_trust_distribution
onboarding_friction
interface_complexity
ai_tutor_quality
privacy_guarantee_strength
campaign_intensity
social_influence_strength
initial_delegate_supply
initial_project_supply
executor_incentive_strength
fiscalizer_compensation
evidence_compensation
platform_failure_rate
bad_outcome_rate
public_controversy_rate
trust_recovery_strength
```

## Scenario families

Initial scenario families:

### S1 — High-friction launch

Core is technically available but hard to understand.

Expected risk:

- many aware non-users;
- low activation;
- high registered inactivity.

### S2 — AI-assisted onboarding

Strong tutor layer reduces friction.

Expected test:

- whether activation rises without creating overtrust.

### S3 — Delegation-first adoption

Users are encouraged to delegate rather than directly inspect projects.

Expected risk:

- fast adoption but high delegation concentration.

### S4 — Evidence-market bottleneck

Citizens adopt, but fiscalizer/evidence supply is thin.

Expected risk:

- verification delays;
- loss of trust;
- project bottlenecks.

### S5 — Early public failure

A visible project fails or is manipulated early.

Expected test:

- trust shock;
- abandonment;
- recovery capacity.

### S6 — Strong local success

Early projects produce visible local wins.

Expected test:

- trust growth;
- recommendation cascades;
- role-market formation.

## Integration with architecture experiment

The behavioral model should export a compact result object:

```json
{
  "scenario_id": "S2-ai-assisted-onboarding",
  "active_user_share": 0.0,
  "registered_user_share": 0.0,
  "registered_inactive_share": 0.0,
  "profile_driven_share": 0.0,
  "direct_participation_share": 0.0,
  "full_delegation_share": 0.0,
  "partial_delegation_share": 0.0,
  "delegation_concentration_hhi": 0.0,
  "abandonment_share": 0.0,
  "mean_platform_trust": 0.0,
  "executor_participation_rate": 0.0,
  "fiscalizer_supply_per_project": 0.0,
  "evidence_supply_per_project": 0.0,
  "thin_market_failure_rate": 0.0
}
```

These outputs can then be used as inputs into the existing institutional architecture simulation.

## Calibration plan

The first version can use synthetic parameters.

Later calibration sources:

- landing page conversion;
- onboarding prototype tests;
- surveys;
- interviews;
- small pilot usage;
- delegation experiments;
- fiscalizer recruitment experiments;
- evidence producer recruitment experiments;
- comparable civic-tech adoption data;
- participatory budgeting participation data.

## Design rule

> Behavioral realism matters more than making Core look successful.

A failed scenario is useful if it identifies a real adoption, trust, delegation, or role-supply bottleneck before implementation.
