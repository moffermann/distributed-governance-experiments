# Implemented Architecture Variants

## Purpose

This document records the architecture variants currently implemented by the executable v0 ABM engine.

The broader conceptual comparison map remains in `ARCHITECTURES.md`. This file tracks what the first runnable simulator actually supports.

## Current variants

## 1. `status_quo`

Centralized allocation with central low-information planning and audit-after-the-fact.

Simplified traits:

```text
centralPlanner = true
planningSource = central
citizenAllocation = false
fundingCaps = true
low detection
low review confidence
weak retention / guarantee / reputation memory
passiveAllocationMode = none
```

Interpretation:

This variant tests the incumbent public-allocation pattern where a central planner selects projects using a planning signal that is only weakly related to latent public value.

It is not modeled as an incompetent random planner. It is modeled as an information-loss planner: the plan may be internally coherent but weakly connected to beneficiary value.

## 2. `participatory_weak_verification`

Participatory allocation with weak verification and low budget absorption.

Simplified traits:

```text
planningSource = none
citizenAllocation = true
fundingCaps = false
weak detection
weak review confidence
weak retention / no guarantee / weak reputation memory
passiveAllocationMode = none
```

Interpretation:

This variant shows what happens when only active or salience-following citizens allocate and there is no default/profile/delegation layer to absorb passive allocation.

It is useful for testing participation decay and low absorption, but it should not be the only participatory comparison.

## 3. `participatory_weak_verification_full_budget`

Participatory allocation with weak verification but full-budget absorption through salience routing.

Simplified traits:

```text
planningSource = none
citizenAllocation = true
fundingCaps = false
weak detection
weak review confidence
weak retention / no guarantee / weak reputation memory
passiveAllocationMode = salience
```

Interpretation:

This variant isolates weak selection and weak verification from low budget absorption.

It forces the passive share into salience-driven allocation so that the model can distinguish:

```text
failure because the budget was not spent
from
failure because the budget was spent through weak rules
```

## 4. `core_v0_tutored_central_planning`

Simplified Core v0 downstream controls with a central low-information default planning layer.

Simplified traits:

```text
planningSource = central
citizenAllocation = true
fundingCaps = true
stronger detection
higher review confidence
retention
guarantee
reputation memory
future selection loss
passiveAllocationMode = planning
```

Interpretation:

This approximates a tutored Core v0 deployment where the authority still supplies the planning/default vector, but the downstream project lifecycle has stronger controls.

This variant is important because it shows how much Core v0 can improve accountability even when planning remains centrally weak.

## 5. `core_v0_tutored_distributed_planning`

Simplified Core v0 downstream controls with a distributed parallel planning/default layer.

Simplified traits:

```text
planningSource = distributed
citizenAllocation = true
fundingCaps = true
stronger detection
higher review confidence
retention
guarantee
reputation memory
future selection loss
passiveAllocationMode = planning
```

Interpretation:

This approximates a tutored or semi-open Core v0 deployment where society constructs a more informative planning/default vector in parallel to the central plan.

It is not full open mode. It is a simplified proxy for distributed planning information being closer to latent public value than central planning.

## Legacy alias: `core_v0_simple`

`core_v0_simple` remains as a legacy alias for a distributed-planning Core v0 simplification, but the baseline scenario should now prefer the explicit names:

```text
core_v0_tutored_central_planning
core_v0_tutored_distributed_planning
```

## Current known simplifications

The v0 executable does not yet implement:

- real project spawning/replacement after closure;
- full milestone objects;
- explicit evidence producer agents;
- explicit fiscalizer assignment pools;
- full distributed signal elicitation;
- strategic signal manipulation;
- fiscalizer collusion;
- complaint paths;
- agenda capture;
- reputation decay over multiple projects;
- ablation variants;
- calibration from audit evidence;
- country/legal effects.

## Design rule

> Executable variants should remain named honestly. A simplified variant must not be presented as the full architecture.
