"""Distribution analysis for panel runs (DISTRIBUTION_FITTING.md).

For each key field of a panel:

- fits a Beta by method of moments and reports fit quality (KS distance
  between the empirical CDF and the fitted Beta CDF);
- flags archetype-mixture structure (spread of per-archetype means) that a
  single Beta cannot represent;
- renders a histogram figure with the fitted Beta overlay (and, optionally, a
  comparison panel's histogram outline);
- when a comparison panel is given, computes where its pooled mean falls
  inside this panel's empirical distribution (percentile), the z-score against
  the sampling distribution of the mean, and the overlap coefficient between
  both empirical distributions.

Writes figures to <panel>/figures/ and a machine-readable
<panel>/distribution_analysis.json. Requires matplotlib.

Usage:
    python src/analyze_distributions.py --panel results/<run> [--compare results/<other_run>]
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

KEY_FIELDS = [
    ("platform_behavior", "platform_trial_probability"),
    ("platform_behavior", "monthly_platform_use_probability"),
    ("citizen_behavior", "direct_planning_participation_probability"),
    ("citizen_behavior", "delegation_probability"),
    ("delegate_behavior", "would_accept_delegation"),
    ("delegate_behavior", "delegate_platform_use_rate"),
    ("delegate_behavior", "delegate_planning_coverage"),
]

BINS = 25


def load(panel_dir: Path) -> list[dict]:
    lines = (panel_dir / "normalized_responses.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def values(responses, section, field):
    return [r[section][field] for r in responses]


def mean(xs):
    return sum(xs) / len(xs)


def variance(xs):
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1) if len(xs) > 1 else 0.0


def beta_moments(xs):
    m, v = mean(xs), variance(xs)
    if not (0.0 < m < 1.0) or not (0.0 < v < m * (1 - m)):
        return None
    common = m * (1 - m) / v - 1
    return (m * common, (1 - m) * common)


def beta_pdf(x, a, b):
    if x <= 0.0 or x >= 1.0:
        return 0.0
    log_pdf = (a - 1) * math.log(x) + (b - 1) * math.log(1 - x) + math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    return math.exp(log_pdf)


def beta_cdf(x, a, b, steps: int = 2000):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    # Simpson-free trapezoid on the pdf: adequate for KS reporting at 3 decimals.
    n = max(2, int(steps * x))
    h = x / n
    total = 0.5 * (beta_pdf(1e-9, a, b) + beta_pdf(x, a, b))
    for i in range(1, n):
        total += beta_pdf(i * h, a, b)
    return min(1.0, total * h)


def ks_distance(xs, a, b):
    xs_sorted = sorted(xs)
    n = len(xs_sorted)
    worst = 0.0
    for i, x in enumerate(xs_sorted):
        cdf = beta_cdf(x, a, b)
        worst = max(worst, abs((i + 1) / n - cdf), abs(i / n - cdf))
    return worst


def histogram(xs, bins=BINS):
    counts = [0] * bins
    for x in xs:
        counts[min(bins - 1, int(x * bins))] += 1
    return [c / len(xs) for c in counts]  # probability mass per bin


def overlap_coefficient(xs, ys, bins=BINS):
    hx, hy = histogram(xs, bins), histogram(ys, bins)
    return sum(min(a, b) for a, b in zip(hx, hy))


def empirical_percentile(xs, value):
    return sum(1 for x in xs if x <= value) / len(xs)


def archetype_mixture_spread(responses, section, field):
    per = {}
    for r in responses:
        per.setdefault(r["archetype_id"], []).append(r[section][field])
    means = sorted(mean(v) for v in per.values())
    return means[-1] - means[0], means


def main() -> None:
    parser = argparse.ArgumentParser(description="Fit and plot panel distributions.")
    parser.add_argument("--panel", required=True)
    parser.add_argument("--compare", default=None, help="Second panel whose distribution/mean is tested against the first.")
    args = parser.parse_args()

    panel_dir = Path(args.panel)
    responses = load(panel_dir)
    compare = load(Path(args.compare)) if args.compare else None
    compare_name = Path(args.compare).name if args.compare else None
    fig_dir = panel_dir / "figures"
    fig_dir.mkdir(exist_ok=True)

    report = {"panel": panel_dir.name, "n": len(responses), "compare": compare_name, "fields": {}}
    print(f"panel: {panel_dir.name} (n={len(responses)})" + (f"  vs  {compare_name} (n={len(compare)})" if compare else ""))
    header = f"{'field':52s}{'mean':>7}{'sd':>7}{'beta(a,b)':>14}{'KS':>7}{'mix':>6}"
    if compare:
        header += f"{'m(b)':>7}{'pct':>6}{'z-mean':>8}{'ovl':>6}"
    print(header)

    for section, field in KEY_FIELDS:
        xs = values(responses, section, field)
        m, sd = mean(xs), math.sqrt(variance(xs))
        fit = beta_moments(xs)
        ks = ks_distance(xs, *fit) if fit else float("nan")
        mix_spread, _ = archetype_mixture_spread(responses, section, field)

        entry = {
            "mean": round(m, 4), "sd": round(sd, 4),
            "beta": [round(fit[0], 3), round(fit[1], 3)] if fit else None,
            "ks_distance": round(ks, 4),
            "archetype_mean_spread": round(mix_spread, 4),
        }

        row = f"{section + '.' + field:52s}{m:7.3f}{sd:7.3f}"
        row += f"  ({fit[0]:5.2f},{fit[1]:5.2f})" if fit else f"{'—':>14}"
        row += f"{ks:7.3f}{mix_spread:6.2f}"

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(xs, bins=BINS, range=(0, 1), density=True, alpha=0.55, label=f"{panel_dir.name} (n={len(xs)})")
        if fit:
            grid = [i / 400 for i in range(1, 400)]
            ax.plot(grid, [beta_pdf(x, *fit) for x in grid], linewidth=2,
                    label=f"Beta({fit[0]:.2f}, {fit[1]:.2f})  KS={ks:.3f}")
        ax.axvline(m, linestyle="--", linewidth=1, label=f"media {m:.3f}")

        if compare:
            ys = values(compare, section, field)
            mb = mean(ys)
            pct = empirical_percentile(xs, mb)
            se_mean = sd / math.sqrt(len(xs))
            z = (mb - m) / se_mean if se_mean > 0 else float("inf")
            ovl = overlap_coefficient(xs, ys)
            entry.update({
                "compare_mean": round(mb, 4),
                "compare_mean_percentile_in_panel": round(pct, 4),
                "compare_mean_z_vs_sampling_dist": round(z, 1),
                "distribution_overlap_coefficient": round(ovl, 4),
            })
            row += f"{mb:7.3f}{pct:6.2f}{z:8.1f}{ovl:6.2f}"
            ax.hist(ys, bins=BINS, range=(0, 1), density=True, histtype="step", linewidth=2,
                    label=f"{compare_name} (n={len(ys)})")
            ax.axvline(mb, linestyle=":", linewidth=1.5, label=f"media comp. {mb:.3f}")

        ax.set_xlabel(field)
        ax.set_ylabel("densidad")
        ax.set_xlim(0, 1)
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(fig_dir / f"{field}.png", dpi=120)
        plt.close(fig)

        report["fields"][f"{section}.{field}"] = entry
        print(row)

    with (panel_dir / "distribution_analysis.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
        fh.write("\n")
    print(f"\nfiguras: {fig_dir}")
    print("mix = rango de medias por arquetipo (mezcla que una Beta única no representa)")
    if compare:
        print("pct = percentil de la media del panel comparado dentro de la distribución empírica del panel base")
        print("z-mean = desvíos de la media comparada respecto de la distribución muestral de la media del panel base")
        print("ovl = coeficiente de solapamiento entre ambas distribuciones empíricas (1 = idénticas)")


if __name__ == "__main__":
    main()
