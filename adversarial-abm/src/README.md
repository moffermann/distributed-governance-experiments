# Source — Adversarial ABM

This folder contains the first executable simulator for the adversarial ABM satellite project.

## Current implementation

The initial implementation is intentionally compact:

```text
index.mjs
```

It is a dependency-free Node.js script that:

- reads a scenario JSON file;
- generates a seeded common project world;
- runs the same world through multiple institutional architectures;
- applies salience and weak-verification pressures;
- simulates allocation, execution, review, leakage, and visibility gaps;
- prints a Markdown summary table;
- optionally writes raw JSON, CSV, and Markdown table outputs.

## Why a single file first?

The design documents describe the future modular architecture. The first executable engine stays in one file so the baseline can be inspected and debugged before refactoring into modules.

The intended migration path is:

```text
index.mjs
→ core/
→ world/
→ agents/
→ architectures/
→ attacks/
→ metrics/
→ experiments/
```

## Run command

From the repository root:

```bash
node experiments/adversarial-abm/src/index.mjs \
  --scenario experiments/adversarial-abm/scenarios/baseline-medium.json
```

Optional overrides:

```bash
node experiments/adversarial-abm/src/index.mjs \
  --scenario experiments/adversarial-abm/scenarios/baseline-medium.json \
  --runs 50 \
  --seed 42
```

## Evidence status

This first engine produces simulation evidence only.

It is not a real-world empirical validation, legal feasibility proof, or final calibration.

## Design rule

> Make the first simulator runnable before making it elegant.
