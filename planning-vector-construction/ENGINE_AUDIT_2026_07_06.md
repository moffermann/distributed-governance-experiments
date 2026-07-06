# Engine Audit — 2026-07-06

## Purpose

Full audit of the planning-vector construction engine (`src/index.mjs`), the last of the four experiment engines to receive one. It matters disproportionately: its correlation table calibrated the adversarial ABM's planning-signal mixes, which in turn parameterize scenarios feeding the master paper's evidence chain.

## Findings and corrections

### PV-1 — Attentive participants sampled with replacement (minor, corrected)

`sampleIndexes` drew participant indices with replacement, so a repeated citizen contributed their signal twice. Corrected to a without-replacement partial Fisher-Yates draw.

### PV-2 — Per-citizen review set silently shrank on collisions (minor, corrected)

Each attentive citizen reviews `attentiveSampleSize` targets via salience-and-value-weighted draws; duplicate draws were skipped without retry, so the effective review set was smaller than configured, concentrated on high-weight targets. Corrected to a guarded retry loop that fills the configured count with distinct targets.

### Checked and found sound (recorded so the next auditor need not re-derive them)

- **Metric semantics**: `normalize01` before Pearson is harmless (Pearson is affine-invariant); MSE is defined over min-max-normalized vectors and labeled as such.
- **Sub-RNG derivation**: each variant's stream is `seed ^ hashName(name)`, and the Core v0 constructor spawns independent sub-streams per channel — variant isolation holds.
- **Delegate weight law**: the Zipf-like `alpha = 0.10 + 0.85·concentration^1.2` reproduces the documented top-1/top-10 shares (near-uniform at microdelegation concentrations, 0.074/0.363 at the concentrated stress case).
- **Honest-signal boundary**: attentive signals are own-value plus noise; the docs/87 elicitation problem is out of scope by declaration, consistent with every other experiment in this repository.
- **Representative machinery**: the information-loss chain (approval sorting against a candidate vector, agenda compression, program fidelity, bounded institutional distortion with normalized component weights) matches `REPRESENTATIVE_PLANNING_MODEL.md` and `CENTRAL_APPROVAL_CALIBRATION.md`.

## Impact on the committed calibration

Re-run at the committed settings (200 runs, seed 42) after both fixes: every variant moves ≤ 0.001 in corr(latent) — e.g. `core_v0_open_mandated_participation` 0.938 → 0.939, `trusted_microdelegation` 0.861 → 0.861, the central family and the salience vector unchanged. **The adversarial ABM's planning-mix calibration ranges taken from this table remain fully valid**; no downstream recalibration is required.

## Certification

The engine conforms to its own design documents and to the honest-signal boundary shared across the repository; both defects found were corrected and are immaterial to all published numbers. Results in `results/` were regenerated with the corrected engine.
