"""Map an LLM calibration panel onto the behavioral adoption ABM.

Reads the panel output of experiments/planning-behavior-calibration
(`panel_summary.json` + `normalized_responses.jsonl`) and writes
`scenarios/llm_calibrated.json`: the baseline scenario with elicited
parameters substituted for synthetic ones, per OUTPUT_TO_BEHAVIORAL_ABM.md.

The result carries a provenance block; values are llm-elicited synthetic
priors, not empirical data.

Usage:
    python apply_llm_calibration.py --panel ../planning-behavior-calibration/results/<run_id>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from behavioral_adoption_abm.core import DEFAULT_CONFIG, clamp  # noqa: E402

MICRO_TYPES = ["family_member", "partner_or_spouse", "trusted_friend", "trusted_neighbor", "local_community_leader"]
INSTITUTIONAL_TYPES = ["technical_expert", "public_institution_or_ngo", "political_party_or_political_actor", "public_influencer"]


def beta_mean(params: list[float]) -> float:
    a, b = params
    return a / (a + b)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply LLM panel calibration to the behavioral ABM.")
    parser.add_argument("--panel", required=True, help="Panel results directory (contains panel_summary.json).")
    parser.add_argument("--output", default=None, help="Defaults to scenarios/llm_calibrated.json (or llm_calibrated_dist.json with --distributions).")
    parser.add_argument("--distributions", action="store_true",
                        help="Distribution-based calibration: planning attendance becomes a PERSISTENT per-citizen "
                             "propensity drawn from the panel's fitted Beta, instead of a mean base. For "
                             "Bernoulli-terminal parameters the mean is provably sufficient, so those stay scalar.")
    args = parser.parse_args()

    panel_dir = Path(args.panel)
    summary = json.loads((panel_dir / "panel_summary.json").read_text(encoding="utf-8"))
    pooled = summary["pooled"]
    meta = summary["metadata"]

    responses = [
        json.loads(line)
        for line in (panel_dir / "normalized_responses.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    civic_mean = beta_mean(DEFAULT_CONFIG["trait_distributions"]["civic_interest"])
    # Two different civic factors in the model: willingness uses (0.5 + civic),
    # planning attendance uses (0.5 + 0.5*civic).
    willingness_multiplier = 0.5 + civic_mean
    attendance_multiplier = 0.5 + 0.5 * civic_mean

    # micro_delegate_willingness: ABM expresses willingness with p = w * (0.5 + civic).
    would_accept = pooled["delegate_behavior.would_accept_delegation"]["mean"]
    micro_willingness = clamp(would_accept / willingness_multiplier)

    # institutional_delegation_propensity: institutional mass among those who would delegate.
    types = summary["pooled_preferred_delegate_type"]
    institutional_mass = sum(types[t] for t in INSTITUTIONAL_TYPES)
    would_not = types["would_not_delegate"]
    institutional_propensity = clamp(institutional_mass / (1.0 - would_not)) if would_not < 1.0 else 0.0

    # permanent_rejection_rate: share who would not even try, corrected for the
    # ABM's per-consideration rejection weighting E[0.6*(1-openness)+0.4*privacy].
    trials = [r["platform_behavior"]["platform_trial_probability"] for r in responses]
    share_refusing = sum(1 for t in trials if t < 0.2) / len(trials)
    openness_mean = beta_mean(DEFAULT_CONFIG["trait_distributions"]["ideological_openness"])
    privacy_mean = beta_mean(DEFAULT_CONFIG["trait_distributions"]["privacy_concern"])
    rejection_weight = 0.6 * (1.0 - openness_mean) + 0.4 * privacy_mean
    permanent_rejection_rate = clamp(share_refusing / rejection_weight if rejection_weight > 0 else share_refusing)

    # planning attendance: direct base inverted by its own civic factor; hybrid
    # and profile keep their synthetic ratios to direct.
    direct_planning = pooled["citizen_behavior.direct_planning_participation_probability"]["mean"]
    base = DEFAULT_CONFIG["planning_attendance_base"]
    direct_base = clamp(direct_planning / attendance_multiplier)
    attendance = {
        "direct_active": round(direct_base, 4),
        "hybrid": round(direct_base * base["hybrid"] / base["direct_active"], 4),
        "profile_driven": round(direct_base * base["profile_driven"] / base["direct_active"], 4),
    }

    # digital_confidence trait prior from perceived ease of use.
    ease_beta = pooled["friction.perceived_ease_of_use"]["beta_moments"]

    validation_targets = {
        field: pooled[field]["mean"]
        for field in (
            "citizen_behavior.delegation_probability",
            "platform_behavior.monthly_platform_use_probability",
            "delegate_behavior.delegate_platform_use_rate",
            "delegate_behavior.delegate_planning_coverage",
            "citizen_behavior.revocation_likelihood_after_misalignment",
        )
    }

    attendance_beta = pooled["citizen_behavior.direct_planning_participation_probability"]["beta_moments"]
    scenario_id = "llm_calibrated_dist" if args.distributions else "llm_calibrated"
    scenario = {
        "scenario_id": scenario_id,
        "description": (
            "Baseline behavioral parameters replaced, where mappable, by LLM-elicited synthetic priors "
            "from the planning-behavior-calibration panel (OUTPUT_TO_BEHAVIORAL_ABM.md). "
            + ("Distribution mode: planning attendance is a persistent per-citizen propensity drawn from "
               "the panel's fitted Beta. " if args.distributions else "")
            + "Not empirical data."
        ),
        "seed": 42,
        "ticks": 104,
        "population_size": 1000,
        "micro_delegate_willingness": round(micro_willingness, 4),
        "institutional_delegation_propensity": round(institutional_propensity, 4),
        "permanent_rejection_rate": round(permanent_rejection_rate, 4),
        "planning_attendance_base": attendance,
        **({"planning_attendance_distribution": attendance_beta} if args.distributions and attendance_beta else {}),
        **({"trait_distributions": {"digital_confidence": ease_beta}} if ease_beta else {}),
        "_provenance": {
            "source": "llm-elicited synthetic priors (not empirical data)",
            "panel_run_id": meta["run_id"],
            "model_name": meta["model_name"],
            "temperature": meta["temperature"],
            "prompt_version": meta["prompt_version"],
            "date": meta["date"],
            "n_responses": meta["n_ok"],
            "mapping": "experiments/planning-behavior-calibration/OUTPUT_TO_BEHAVIORAL_ABM.md",
            "validation_targets": validation_targets,
        },
    }

    out = Path(args.output) if args.output else ROOT / "scenarios" / f"{scenario_id}.json"
    out.write_text(json.dumps(scenario, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"wrote {out}")
    print(f"{'parameter':40s} {'synthetic':>10} {'llm-elicited':>13}")
    print("-" * 66)
    rows = [
        ("micro_delegate_willingness", DEFAULT_CONFIG["micro_delegate_willingness"], micro_willingness),
        ("institutional_delegation_propensity", DEFAULT_CONFIG["institutional_delegation_propensity"], institutional_propensity),
        ("permanent_rejection_rate", DEFAULT_CONFIG["permanent_rejection_rate"], permanent_rejection_rate),
        ("planning_attendance_base.direct_active", base["direct_active"], attendance["direct_active"]),
    ]
    if ease_beta:
        rows.append(("digital_confidence beta mean", beta_mean(DEFAULT_CONFIG["trait_distributions"]["digital_confidence"]), beta_mean(ease_beta)))
    for name, old, new in rows:
        print(f"{name:40s} {old:>10.3f} {new:>13.3f}")


if __name__ == "__main__":
    main()
