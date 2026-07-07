# Headline ratio confidence intervals (Fieller + paired bootstrap)

Core-distributed vs status-quo verified-value ratio, per population. Paired by seed; n=20.

| scenario | ratio of means | Fieller 95% CI | bootstrap 95% CI |
|---|---:|---|---|
| baseline-medium | 2.05x | [1.86, 2.26] | [1.88, 2.24] |
| behavioral-baseline | 2.42x | [2.29, 2.55] | [2.30, 2.54] |
| behavioral-llm-calibrated | 2.19x | [2.02, 2.37] | [2.03, 2.34] |
| behavioral-high-friction | 2.69x | [2.54, 2.84] | [2.55, 2.82] |
| behavioral-delegation-first | 2.35x | [2.20, 2.53] | [2.21, 2.51] |

Every ratio CI excludes 1.0 by a wide margin — the architecture advantage is not an artifact of ratio noise. The Fieller and bootstrap intervals agree; the ranking claim F1 is interval-robust.
