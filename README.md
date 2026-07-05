# Experiments Workspace

This folder contains research experiments that support, stress-test, or extend the master distributed-governance architecture without changing the architecture corpus directly.

The folder is intentionally separate from `docs/`, `knowledge/`, `attacks/`, and `defenses/`.

## Purpose

Use this workspace for:

- computational experiments;
- simulation designs;
- reproducibility packages in progress;
- scenario libraries;
- calibration notes;
- experimental protocols;
- paper-satellite preparation.

## Current experiments

- [`adversarial-abm/`](adversarial-abm/) — adversarial agent-based modeling framework for stress-testing public-resource allocation architectures.

## Repository boundary

Experiments may reference the master architecture, paper, formal models, and adversarial record, but they do not redefine Core v0 unless a later accepted resolution explicitly propagates a finding into the architecture corpus.

Experimental findings should be treated as:

```text
simulation evidence
not institutional proof
not legal authorization
not empirical pilot validation
```

## Migration rule

When an experiment becomes a publishable computational artifact, it may be extracted into a dedicated replication repository containing only:

- paper satellite;
- simulation code;
- synthetic or calibrated datasets;
- experiment definitions;
- result tables;
- figures;
- reproduction instructions;
- citation and license files.

Until then, experiments remain here so they can inherit context from the master research corpus.
