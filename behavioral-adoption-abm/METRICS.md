# Metrics

## Purpose

This document defines the first observable metrics for the behavioral adoption ABM.

The experiment exists because prior architecture simulations had to impose participation, delegation, activation, and role-supply assumptions as external parameters. This model should instead generate those values endogenously.

## Metric classes

The simulator should produce metrics across nine classes:

1. awareness and registration;
2. activation and continued use;
3. participation mode;
4. delegation;
5. trust and legitimacy;
6. role supply;
7. verification capacity;
8. retention and abandonment;
9. integration outputs for the institutional architecture experiment.

## 1. Awareness and registration metrics

### awareness_rate

Share of simulated citizens who have become aware of Core.

```text
aware_citizens / total_citizens
```

### awareness_source_distribution

Distribution of first awareness source.

Possible sources:

- direct campaign;
- friend or family;
- organization;
- delegate;
- media;
- controversy;
- project beneficiary;
- employer or professional network.

### registration_rate

Share of citizens who register after becoming aware.

```text
registered_citizens / aware_citizens
```

### awareness_to_registration_delay

Average number of simulation ticks between awareness and registration.

### non_registration_reason_distribution

Modeled reason for not registering.

Possible reasons:

- distrust;
- low benefit;
- high friction;
- ideological rejection;
- privacy concern;
- low digital confidence;
- no social proof;
- no urgent need.

## 2. Activation and continued-use metrics

### activation_rate

Share of registered citizens who perform a meaningful first action.

```text
activated_citizens / registered_citizens
```

Meaningful first actions may include:

- direct allocation;
- profile creation;
- delegation;
- project review;
- evidence contribution;
- complaint;
- fiscalization application.

### registered_inactive_share

Share of registered users who remain inactive.

```text
registered_inactive_citizens / registered_citizens
```

### active_user_share

Share of all citizens who are active during a given period.

```text
period_active_citizens / total_citizens
```

### sustained_active_user_share

Share of citizens active across multiple periods.

```text
citizens_active_in_n_of_last_m_periods / total_citizens
```

### activity_decay_rate

Rate at which active users become inactive over time.

## 3. Participation-mode metrics

### direct_participation_share

Share of registered citizens who directly inspect and allocate.

### profile_driven_share

Share of registered citizens using automated profiles.

### passive_delegated_share

Share of registered citizens who delegate and otherwise remain passive.

### hybrid_participation_share

Share of citizens who combine direct participation with profile or delegation.

### inactive_without_delegation_share

Share of registered citizens who neither participate nor delegate.

This is a critical risk metric because it identifies democratic surface area that does not translate into usable allocation signal.

## 4. Delegation metrics

### delegation_rate

Share of registered citizens who delegate some scope.

### full_delegation_share

Share of registered citizens who delegate all relevant participation.

### partial_delegation_share

Share of registered citizens who delegate only a bounded scope.

### delegation_concentration_hhi

Herfindahl-Hirschman Index of delegated weight concentration.

```text
sum(delegate_share_i^2)
```

### top_delegate_share

Share of all delegated weight controlled by the largest delegate.

### top_10_delegate_share

Share of all delegated weight controlled by the ten largest delegates.

### delegate_switching_rate

Share of delegators who change delegate during a period.

### delegation_revocation_rate

Share of delegators who revoke delegation during a period.

### poor_outcome_revocation_elasticity

Sensitivity of delegation revocation to bad outcomes.

## 5. Trust and legitimacy metrics

### mean_platform_trust

Average trust in Core across all citizens.

### trust_distribution

Full distribution of trust scores, not only the mean.

### trust_by_user_state

Trust segmented by:

- unaware;
- aware non-user;
- registered inactive;
- direct active;
- profile-driven;
- delegating;
- abandoned.

### trust_change_after_success

Average trust delta after a positive experience.

### trust_change_after_failure

Average trust delta after a negative experience.

### trust_recovery_rate

Rate at which trust recovers after platform fixes, successful outcomes, or public corrections.

### perceived_fairness

Average perceived fairness of allocation, verification, and dispute resolution.

### legitimacy_threshold_crossing

Tick at which mean or median legitimacy crosses a defined threshold.

## 6. Role-supply metrics

### executor_participation_rate

Share of eligible executors willing to participate.

### honest_executor_share

Share of participating executors modeled as honest or primarily delivery-oriented.

### opportunistic_executor_share

Share of participating executors modeled as opportunistic.

### fiscalizer_supply

Number of fiscalizers available per project, category, region, or budget unit.

### evidence_producer_supply

Number of evidence producers available per project, category, region, or budget unit.

### reviewer_capacity

Dispute or admissibility review capacity per period.

### role_market_depth

Composite measure of whether there are enough non-captured, competent actors in each control role.

Possible formula:

```text
role_market_depth = available_independent_role_agents / required_role_agents
```

## 7. Verification-capacity metrics

### fiscalizer_coverage_rate

Share of projects or milestones with adequate fiscalizer coverage.

### evidence_coverage_rate

Share of projects or milestones with adequate evidence coverage.

### corroboration_depth

Average number of independent evidence sources per verified claim.

### detection_rate

Share of manipulated, weak, or failed execution events detected.

### false_positive_rate

Share of honest or adequate events incorrectly flagged.

### false_negative_rate

Share of problematic events not detected.

### verification_delay

Average delay added by verification before release, correction, or decision.

### thin_market_failure_rate

Share of projects where verification fails due to insufficient fiscalizers or evidence producers.

## 8. Retention and abandonment metrics

### churn_rate

Share of active users who become abandoned or long-term inactive.

### abandonment_share

Share of all registered users who abandon the platform.

### abandonment_reason_distribution

Modeled cause of abandonment.

Possible reasons:

- onboarding friction;
- no visible impact;
- bad project outcome;
- perceived capture;
- privacy concern;
- platform outage;
- excessive complexity;
- unresolved complaint;
- public scandal;
- delegate disappointment.

### reactivation_rate

Share of abandoned users who return.

### negative_word_of_mouth_rate

Rate at which abandoned or distrustful users reduce adoption probability among connected agents.

### recommendation_rate

Rate at which satisfied users increase adoption probability among connected agents.

## 9. Integration outputs for architecture experiments

The behavioral ABM should generate scenario-level outputs that can be passed into architecture-comparison experiments.

Required integration outputs:

```text
active_user_share
registered_user_share
registered_inactive_share
aware_non_user_share
permanent_rejection_share
default_rule_share
passive_delegated_share
profile_driven_share
direct_participation_share
full_delegation_share
partial_delegation_share
delegator_share
active_delegate_count
delegation_concentration_hhi
top_delegate_share
micro_delegation_weight_share
institutional_delegation_weight_share
delegate_platform_use_rate
delegate_switching_rate
delegation_revocation_rate
abandonment_share
reactivation_rate
mean_platform_trust
mean_trust_registered
trust_distribution
executor_participation_rate
honest_executor_share
opportunistic_executor_share
fiscalizer_supply_per_project
evidence_supply_per_project
verification_coverage_rate
evidence_coverage_rate
verification_market_depth
thin_market_failure_rate
negative_word_of_mouth_rate
recommendation_rate
```

Denominator note: `*_share` metrics over participation modes and abandonment use registered citizens as the base; `active_user_share`, `default_rule_share`, `delegator_share`, `aware_non_user_share`, and `permanent_rejection_share` use the total population. `default_rule_share` exists because in Core v0 a citizen who does nothing is not lost signal — their allocation follows the public default rule (docs/101).

The delegation outputs map onto the planning-vector experiment's parameters: `delegator_share` → `delegatorShare`, `active_delegate_count` → `delegateCount`, `delegation_concentration_hhi` → `delegateConcentration`, `delegate_platform_use_rate` → `delegatePlatformUseRate`. `delegatePlanningCoverage` is not produced here; use the documented priors.

## Interpretation discipline

The simulator should not report adoption as success by itself.

High registration can coexist with:

- low activation;
- high passive inactivity;
- excessive delegation concentration;
- thin fiscalizer markets;
- poor evidence supply;
- low trust;
- high churn.

The core behavioral success condition is not registration. It is sustained, role-complete, trust-preserving use.

## Minimum viability thresholds

A scenario should be flagged as behaviorally non-viable if any of the following occur:

1. active use remains too low to generate meaningful allocation signal;
2. delegation concentrates beyond a defined threshold;
3. fiscalizer supply is insufficient for verification coverage;
4. evidence producer supply is insufficient for corroboration;
5. executor participation is too low for project delivery;
6. abandonment grows faster than new activation;
7. trust declines monotonically after early failures;
8. the system depends on a single role class behaving unrealistically well.
