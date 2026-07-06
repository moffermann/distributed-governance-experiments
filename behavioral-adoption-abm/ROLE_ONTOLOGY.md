# Behavioral Role Ontology

## Purpose

This document converts Core v0 from a generic platform with users into a behavioral ecosystem of roles.

The goal is to identify which roles must be modeled as agents, which states each role can occupy, what motivates each role, which actions they can take, what incentives affect them, what risks they introduce, and what metrics the simulator should observe.

The central modeling rule is:

```text
role -> motivation -> state -> action -> incentive -> risk -> observable metric
```

## Role classes

The first behavioral model should distinguish at least six role classes:

1. citizen-side roles;
2. delegation-side roles;
3. project-side roles;
4. execution-side roles;
5. control and verification roles;
6. platform and governance roles.

A single real person may occupy more than one role, but the simulator should initially model roles separately for clarity.

## Citizen-side roles

### Unaware citizen

A person who has not meaningfully heard of Core.

Motivations:

- none yet;
- weak curiosity only after exposure.

Possible transitions:

- becomes aware through campaign, friend, organization, controversy, or media event.

Key variables:

- exposure probability;
- social network position;
- media exposure;
- baseline civic interest;
- baseline digital confidence.

Metrics:

- awareness rate;
- time to first exposure;
- exposure source.

### Aware non-user

A person who knows Core exists but does not register or participate.

Motivations for non-use:

- distrust;
- apathy;
- perceived complexity;
- low expected benefit;
- lack of time;
- fear of error;
- no social proof;
- ideological rejection;
- privacy concern.

Possible actions:

- ignore;
- investigate;
- register;
- reject permanently;
- share criticism.

Metrics:

- awareness-to-registration conversion;
- stated or modeled non-use reason;
- distrust share;
- friction loss.

### Registered inactive citizen

A person who created an account but does not use the system.

Motivations:

- initial curiosity;
- weak commitment;
- low urgency;
- unclear next step;
- onboarding failure.

Possible actions:

- remain inactive;
- configure a profile;
- delegate;
- make a direct allocation;
- abandon.

Metrics:

- registration-to-activation rate;
- inactive persistence;
- activation delay;
- onboarding drop-off.

### Direct active citizen

A person who actively inspects choices and directly allocates or participates.

Motivations:

- civic impact;
- personal relevance;
- local need;
- dissatisfaction with status quo;
- trust in own judgment;
- desire for control.

Possible actions:

- inspect projects;
- allocate;
- vote or rank;
- comment;
- report problems;
- revise prior choices;
- recommend Core.

Key variables:

- attention budget;
- perceived agency;
- information quality;
- decision confidence;
- trust in evidence;
- fatigue.

Metrics:

- active-use rate;
- average inspected projects;
- allocation frequency;
- decision revision rate;
- fatigue-driven inactivity.

### Profile-driven citizen

A person who configures automatic preferences and allows the system to allocate within a constrained profile.

Motivations:

- wants influence without constant attention;
- trusts rule-based automation more than personal inspection;
- wants control boundaries without daily participation.

Possible actions:

- create profile;
- update profile;
- pause profile;
- override allocation;
- abandon profile.

Key variables:

- automation trust;
- control preference;
- update frequency;
- perceived alignment;
- outcome satisfaction.

Metrics:

- profile adoption;
- profile persistence;
- override frequency;
- profile abandonment.

### Passive delegated citizen

A person who delegates participation to another actor.

Motivations:

- low attention;
- trust in another person or organization;
- identity alignment;
- expertise gap;
- convenience.

Possible actions:

- choose delegate;
- scope delegation;
- revoke delegation;
- change delegate;
- become active after bad outcome.

Key variables:

- trust in delegate;
- perceived alignment;
- concentration tolerance;
- revocation threshold;
- social proof.

Metrics:

- delegation rate;
- full versus partial delegation;
- delegate concentration;
- revocation rate;
- switching rate.

### Abandoned citizen

A person who tried Core and stopped using it.

Triggers:

- high friction;
- bad outcome;
- perceived unfairness;
- unresolved complaint;
- privacy concern;
- public controversy;
- no visible impact;
- cognitive overload.

Possible actions:

- stay abandoned;
- return after trust recovery;
- criticize publicly;
- influence others against adoption.

Metrics:

- churn;
- reason for abandonment;
- trust loss;
- reactivation probability;
- negative-word-of-mouth effect.

## Delegation-side roles

### Individual delegate

A person trusted by other citizens to allocate or decide within a scope.

Motivations:

- reputation;
- influence;
- civic impact;
- ideological alignment;
- possible compensation if allowed.

Actions:

- publish preference thesis;
- accept delegations;
- allocate delegated weight;
- explain decisions;
- respond to complaints;
- resign.

Risks:

- concentration of influence;
- hidden conflicts;
- poor performance;
- popularity without competence;
- capture.

Metrics:

- delegated weight;
- concentration index;
- performance of delegated allocations;
- revocation after bad outcomes;
- conflict-of-interest incidents.

### Organizational delegate

An organization that receives delegated authority from citizens.

Motivations:

- mission alignment;
- institutional influence;
- funding direction;
- legitimacy;
- constituency service.

Risks:

- bloc voting;
- agenda capture;
- hidden related-party preference;
- organizational self-dealing.

Metrics:

- delegated share by organization;
- related-party exposure;
- allocation diversity;
- revocation rate;
- performance by domain.

## Project-side roles

### Project proposer

An actor who proposes a project or initiative to be funded or supported.

Motivations:

- solve a real problem;
- obtain funding;
- gain reputation;
- serve a constituency;
- extract resources.

States:

- honest;
- low-capacity honest;
- opportunistic;
- captured;
- incompetent.

Actions:

- submit project;
- define claims;
- define metrics;
- propose evidence contract;
- respond to validation;
- revise project.

Metrics:

- proposal rate;
- validation pass rate;
- claim quality;
- metric quality;
- detected manipulation.

### Beneficiary / affected user

A person or group affected by a project outcome.

Motivations:

- receive benefit;
- report success;
- report failure;
- avoid retaliation;
- obtain future service.

Actions:

- confirm outcome;
- file complaint;
- produce testimonial;
- provide counter-evidence;
- remain silent.

Metrics:

- beneficiary confirmation rate;
- complaint rate;
- silence under pressure;
- contradiction between claimed and experienced outcome.

## Execution-side roles

### Honest executor

An actor who attempts to deliver the project sincerely.

Motivations:

- payment;
- reputation;
- mission;
- future selection;
- professional pride.

Risks:

- failure due to capacity;
- cost overruns;
- liquidity shortage;
- delay;
- external shocks.

Metrics:

- delivery rate;
- delivery quality;
- delay rate;
- cost deviation;
- repeat selection.

### Opportunistic executor

An actor who may underdeliver, divert funds, inflate costs, or manipulate milestones.

Motivations:

- extraction gain;
- low detection expectation;
- weak penalties;
- low reputation stake.

Actions:

- deliver honestly;
- delay;
- underdeliver;
- divert;
- collude with fiscalizer;
- manipulate evidence.

Metrics:

- diversion rate;
- underdelivery rate;
- detection rate;
- expected versus actual penalty;
- repeated opportunism.

## Control and verification roles

### Fiscalizer

An actor who reviews execution, evidence, milestones, or complaints.

States:

- honest competent;
- honest weak;
- overloaded;
- biased;
- capturable;
- captured.

Motivations:

- compensation;
- reputation;
- independence;
- professional duty;
- civic contribution.

Actions:

- accept review task;
- inspect evidence;
- request more evidence;
- approve;
- reject;
- flag manipulation;
- collude.

Metrics:

- fiscalizer supply;
- review capacity;
- detection probability;
- false positive rate;
- false negative rate;
- capture rate;
- market depth.

### Evidence producer

An actor who generates evidence, counter-evidence, reports, audits, observations, measurements, or beneficiary confirmations.

States:

- independent;
- low-quality;
- biased;
- captured;
- professional;
- volunteer.

Motivations:

- compensation;
- reputation;
- mission;
- affiliation;
- pressure from project actors.

Actions:

- produce evidence;
- refuse weak evidence;
- manipulate evidence;
- provide counter-evidence;
- corroborate another source.

Metrics:

- evidence supply;
- evidence quality;
- evidence cost;
- corroboration depth;
- contradiction rate;
- manipulation rate.

### Reviewer / resolver

An actor who resolves disputes, admissibility issues, appeals, or contested evidence.

Motivations:

- procedural correctness;
- legitimacy;
- speed;
- consistency;
- protection from capture.

Actions:

- review complaint;
- uphold decision;
- reverse decision;
- require new evidence;
- sanction actor;
- create precedent.

Metrics:

- resolution time;
- reversal rate;
- consistency;
- unresolved backlog;
- perceived fairness.

## Platform and governance roles

### AI tutor / assistant layer

A non-human system that reduces friction, explains options, helps configure profiles, detects inconsistencies, and guides users through decisions.

Functions:

- onboarding help;
- project explanation;
- profile construction;
- risk explanation;
- evidence guidance;
- complaint drafting;
- delegate comparison.

Risks:

- overtrust;
- hallucinated explanation;
- biased guidance;
- opacity;
- excessive dependence.

Metrics:

- friction reduction;
- activation lift;
- profile quality;
- user confidence;
- error rate;
- override rate.

### Protocol administrator

A role that maintains rules, parameters, eligibility, default settings, and governance updates.

Risks:

- agenda capture;
- parameter manipulation;
- incumbent protection;
- opaque rule changes;
- default-layer capture.

Metrics:

- parameter-change frequency;
- public challenge rate;
- rollback rate;
- default concentration;
- trust effect after rule changes.

## First implementation boundary

The first Mesa/Python version should not model every role at full fidelity.

Minimum viable behavioral model:

1. citizens with awareness, registration, activation, delegation, profile use, direct use, abandonment;
2. delegates with reputation and concentration;
3. projects with perceived and latent quality;
4. executors with honest/opportunistic behavior;
5. fiscalizers with limited supply and detection quality;
6. evidence producers with supply, quality, and manipulation risk;
7. platform friction and trust feedback.

## Output required for integration

This behavioral experiment should output parameter distributions for the architecture experiment:

```text
active_user_share
registered_inactive_share
passive_delegated_share
profile_driven_share
full_delegation_share
partial_delegation_share
abandonment_share
fiscalizer_supply_per_project
evidence_supply_per_project
executor_participation_rate
trust_distribution
delegation_concentration
negative_word_of_mouth_rate
```
