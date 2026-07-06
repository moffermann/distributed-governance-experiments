# Post-Audit Run Results — 2026-07-06

## Execution

All four scenarios were re-run after the corrections recorded in [`CORE_V0_CONFORMANCE_AUDIT.md`](CORE_V0_CONFORMANCE_AUDIT.md), using `run_sweep.py`:

- replications: 10 seeds per scenario (seeds 42–51);
- horizon: 104 ticks (weeks);
- population: 1,000 citizens;
- verified byte-identical between Mesa 3.5.1 and the stdlib fallback for the same seed.

Status of the six recommended changes from the first Mesa run: #1 registration recalibration — done; #2 awareness saturation limits — done; #3 profile-state split — still open; #4 fiscalizer/evidence market dynamics — recruitment, dropout, capacity, and compensation elasticity done, queueing still open; #5 viability flags — done; #6 Mesa integer-seed initialization — done.

## Mean final results (10 seeds)

| Metric | baseline | high_friction_launch | ai_assisted_onboarding | delegation_first |
|---|---:|---:|---:|---:|
| Registered users | 51.3% | 34.5% | 61.8% | 54.3% |
| Active users | 32.8% | 15.5% | 40.7% | 36.8% |
| Default-rule share | 67.2% | 84.5% | 59.3% | 63.2% |
| Direct participation (of registered) | 23.6% | 19.5% | 17.6% | 25.6% |
| Profile-driven (of registered) | 15.9% | 9.7% | 27.2% | 21.3% |
| Full delegation (of registered) | 18.6% | 11.3% | 15.7% | 15.6% |
| Partial delegation (of registered) | 5.5% | 4.3% | 5.3% | 4.4% |
| Delegator share (of population) | 12.5% | 5.4% | 13.0% | 11.1% |
| Active delegates | 77 | 42 | 82 | 33 |
| Delegation HHI | 0.017 | 0.030 | 0.017 | 0.073 |
| Top delegate share | 4.2% | 5.8% | 3.8% | 16.7% |
| Micro-delegation weight share | 64.5% | 54.1% | 67.2% | 25.0% |
| Delegate platform-use rate | 0.85 | 0.72 | 0.85 | 0.97 |
| Abandonment (of registered) | 12.7% | 18.6% | 16.2% | 13.9% |
| Mean platform trust | 0.64 | 0.52 | 0.59 | 0.66 |
| Verification coverage | 0.85 | 0.79 | 0.79 | 0.81 |
| Evidence coverage | 0.55 | 0.62 | 0.59 | 0.65 |
| Thin-market failure risk | 0.45 | 0.38 | 0.41 | 0.35 |
| Recommendation rate | 0.72 | 0.57 | 0.61 | 0.73 |

Viability flags raised (share of seeds): every scenario raises `evidence_undersupplied` in 10/10 seeds and `verification_undersupplied` in 4–6/10; `high_friction_launch` additionally raises `active_signal_low` and `abandonment_high` in 2/10; `delegation_first` raises `delegation_overconcentrated` in 2/10.

## Interpretation

**Adoption no longer saturates, and friction now has first-order effects.** The first run registered ~100% of the population in every scenario; the recalibrated model produces 51% baseline registration, 35% under high friction, and 62% with AI-assisted onboarding, with permanent rejection around 30% of the population. Registered inactivity, non-registration, and abandonment behave as the normal outcomes the design rule demands.

**The default rule is now visible.** Between 59% and 85% of the population allocates through the public default rule rather than through active choice. This is the single most important number this experiment hands to the architecture experiments: Core v0's allocation signal at launch is dominated by the default layer's informational quality, exactly as the corpus's E3/E4 findings assume — not by attentive citizens.

**The verification bottleneck survives recalibration.** The first run's central finding — adoption is not the binding constraint, verification-market depth is — holds after all corrections, now expressed against the configured per-project requirements: evidence coverage stays near 0.55–0.65 and the undersupply flag fires in every seed of every scenario. Fiscalizer/evidence capacity priors are synthetic and are the first parameters that need empirical grounding.

**AI-assisted onboarding shapes mode, not just volume — and does not protect trust.** The tutor scenario again shifts participation toward profile-driven use (27% vs. 16% baseline) while raising adoption. Its mean trust is slightly *below* baseline: pulling more marginal users in exposes more of them to outcome-driven trust shocks. The tutor layer is an adoption and mode-shaping mechanism, not a legitimacy mechanism.

**Delegation now behaves like the corpus expects.** Baseline delegation is trusted microdelegation: ~77 active delegates, two-thirds of delegated weight held by known persons, HHI 0.017, top delegate 4%. The institutional-stress scenario (`delegation_first`, rewritten per the audit) produces the expected degradation: delegated weight collapses onto ~33 delegates, HHI quadruples to 0.073, the top delegate holds 17%, and the overconcentration flag begins to fire. These outputs now map directly onto the planning-vector experiment's `delegatorShare` / `delegateCount` / `delegateConcentration` / `delegatePlatformUseRate` parameters.

**Trust dynamics are live.** Mean trust ranges 0.52–0.66 with wide cross-seed variance (single-seed minima below 0.35), reactivation is high while success stocks are positive, and the monotonic-decline flag fires in ~10–20% of seeds. Trust is now an actual state variable, not a saturated constant.

## Caveats

All coefficients remain synthetic; these numbers characterize the model's behavior, not any real population. The comparison against the first run's table is directional only: the first run's Mesa results were produced by a code path whose seeding differed between environments (audit finding F4) and are not reproducible under the corrected engine.
