# Implemented Architecture Variants

## Purpose

This document records the architecture variants currently implemented by the executable v0 ABM engine.

The broader conceptual comparison map remains in `ARCHITECTURES.md`. This file tracks what the first runnable simulator actually supports.

## Current variants

## 1. `status_quo`

Centralized allocation with audit-after-the-fact.

Simplified traits:

```text
centralPlanner = true
citizenAllocation = false
fundingCaps = true
low detection
low review confidence
weak retention / guarantee / reputation memory
passiveAllocationMode = none
```

Interpretation:

This variant tests a competent-enough central planner with weak delivery verification and weak persistent consequences.

## 2. `participatory_weak_verification`

Participatory allocation with weak verification and low budget absorption.

Simplified traits:

```text
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

## 4. `core_v0_simple`

Simplified Core v0 with default planning layer, funding caps, stronger detection, milestone-like delivery control, retention, guarantee, and reputation memory.

Simplified traits:

```text
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

This is not full Core v0. It is a first executable approximation to test whether verification, retention, reputation, funding caps, and default routing improve delivered and verified value under medium adversarial pressure.

## Current known simplifications

The v0 executable does not yet implement:

- real project spawning/replacement after closure;
- full milestone objects;
- explicit evidence producer agents;
- explicit fiscalizer assignment pools;
- fiscalizer collusion;
- complaint paths;
- agenda capture;
- reputation decay over multiple projects;
- ablation variants;
- calibration from audit evidence;
- country/legal effects.

## Design rule

> Executable variants should remain named honestly. A simplified variant must not be presented as the full architecture.
