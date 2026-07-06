# Mesa Run Results — 2026-07-06

> Follow-up: the recommended changes below were implemented the same day as part of a Core v0 conformance audit; see [`CORE_V0_CONFORMANCE_AUDIT.md`](CORE_V0_CONFORMANCE_AUDIT.md) and the re-run in [`RUN_2026_07_06_POST_AUDIT_RESULTS.md`](RUN_2026_07_06_POST_AUDIT_RESULTS.md). The numbers in this document were produced by the pre-audit engine and are kept as a dated record.

## Execution

The behavioral adoption ABM was executed locally with Mesa 3.5.1.

Mesa compatibility note: the first executable prototype must initialize Mesa with an integer seed, not a `random.Random` object. The run used:

```python
super().__init__(rng=self.seed)
```

instead of passing a `random.Random` instance to Mesa's `rng` argument.

## Run design

- scenarios: baseline, high-friction launch, AI-assisted onboarding, delegation-first;
- replications: 10 seeds per scenario;
- horizon: 104 ticks, interpreted as weeks;
- population: 1,000 citizens;
- outputs inspected: final integration metrics and one representative time series per scenario.

## Mean final results

| Scenario | Registered users | Active users | Registered inactive | Direct participation | Profile-driven | Full delegation | Partial delegation | Delegation HHI | Top delegate share | Abandonment | Mean trust | Fiscalizers per project | Evidence producers per project | Thin-market failure risk | Recommendation rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 99.6% | 93.5% | 6.1% | 29.0% | 19.4% | 37.2% | 8.3% | 5.3% | 9.0% | 0.1% | 95.3% | 22.5% | 28.2% | 74.6% | 97.5% |
| high_friction_launch | 99.8% | 87.0% | 11.1% | 28.2% | 12.3% | 39.2% | 7.5% | 5.3% | 9.1% | 1.7% | 86.0% | 23.9% | 26.9% | 74.6% | 87.6% |
| ai_assisted_onboarding | 99.6% | 94.3% | 4.8% | 23.6% | 34.6% | 29.2% | 7.3% | 5.3% | 9.5% | 0.4% | 90.1% | 23.1% | 27.1% | 74.9% | 92.8% |
| delegation_first | 100.0% | 94.4% | 4.2% | 29.1% | 22.0% | 37.5% | 5.9% | 11.3% | 19.4% | 1.4% | 90.3% | 23.2% | 29.2% | 73.8% | 91.5% |

## Interpretation

The MVP produces adoption that is probably too optimistic. Registration saturates near the full population in every scenario, even under high friction. That means the registration equation is currently too permissive and should be recalibrated before using its adoption outputs as institutional inputs.

The high-friction scenario behaves directionally correctly: active use falls, registered inactivity rises, abandonment rises, and trust declines relative to baseline. The effect is present but too weak because registration still saturates.

AI-assisted onboarding shifts participation mode rather than merely increasing adoption. Profile-driven participation becomes much larger, direct participation drops, and inactivity falls. This is useful because it suggests the tutor layer should be modeled as a mode-shaping mechanism, not only an activation booster.

The delegation-first scenario exposes the expected concentration risk. It produces similar active use to baseline, but delegation concentration roughly doubles and the largest delegate share rises materially. That is a governance-risk signal even when adoption looks strong.

The clearest bottleneck is not adoption. The clearest bottleneck is verification-market depth. Fiscalizer and evidence supply remain far below one actor per project, so the thin-market failure risk stays around 74%. The next model iteration should focus on fiscalizer and evidence-producer recruitment, compensation, capacity, and assignment rules.

## Recommended next changes

1. Lower registration probability by recalibrating the registration intercept and increasing friction/privacy penalties.
2. Add explicit launch-stage saturation limits so awareness does not become near-universal too quickly.
3. Split profile-driven activity into `configured_but_unverified`, `profile_active`, and `profile_overridden`.
4. Add fiscalizer/evidence market dynamics: recruitment, dropout, queueing, capacity, and compensation elasticity.
5. Add viability flags for scenarios where adoption is high but verification supply is structurally insufficient.
6. Patch Mesa initialization in the executable code to use an integer seed for Mesa 3.x compatibility.
