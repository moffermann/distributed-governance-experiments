"""Core v0 behavioral adoption agent-based model.

This executable version is intentionally dependency-light. If Mesa is
installed, agents and the model inherit from Mesa's Agent/Model classes. If
Mesa is not installed, a tiny fallback shim keeps the experiment runnable with
only Python's standard library. Either way the model draws every random number
from one `random.Random(seed)` stream, so results are byte-identical with and
without Mesa.

Core v0 conformance notes (see CORE_V0_CONFORMANCE_AUDIT.md):

- Delegation is modeled first as trusted microdelegation (citizen -> willing
  person in their own social circle), with a small institutional delegate pool
  as the stress channel, following the planning-vector experiment's
  TRUSTED_MICRODELEGATION_MODEL.md.
- Citizens who do nothing are not lost allocation signal: their share follows
  the public default rule (docs/101, "What you, a citizen, actually do"), so
  project funding always receives the default-routed remainder.
- Reputation informs delegate choice; nothing in the model excludes any actor
  from being chosen (docs/107).
- Social signals expose only what neighbors voluntarily self-disclose
  (registered / active / abandoned / recommending). Allocation targets are
  never observable by other agents (docs/108).
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

try:  # Optional dependency for native Mesa execution.
    import mesa  # type: ignore
except Exception:  # pragma: no cover - used only when Mesa is absent.
    class _FallbackAgent:
        _next_id = 1

        def __init__(self, model):
            self.model = model
            self.random = model.random
            self.unique_id = _FallbackAgent._next_id
            _FallbackAgent._next_id += 1

    class _FallbackModel:
        def __init__(self, seed=None, rng=None):
            source = seed if seed is not None else rng
            self.random = source if isinstance(source, random.Random) else random.Random(source)

    class _MesaFallback:
        Agent = _FallbackAgent
        Model = _FallbackModel

    mesa = _MesaFallback()  # type: ignore


DEFAULT_CONFIG: Dict[str, Any] = {
    "scenario_id": "baseline",
    "description": "Synthetic baseline for Core v0 behavioral adoption.",
    "seed": 42,
    "ticks": 104,
    "population_size": 1000,
    "initial_awareness": 0.08,
    "initial_trust_mean": 0.48,
    "initial_trust_spread": 0.18,
    "campaign_intensity": 0.025,
    "awareness_ceiling": 0.90,
    "social_influence_strength": 0.060,
    "negative_word_of_mouth_strength": 0.080,
    "recommendation_strength": 0.070,
    "onboarding_friction": 0.38,
    "interface_complexity": 0.35,
    "ai_tutor_quality": 0.45,
    "privacy_guarantee_strength": 0.55,
    "public_legitimacy": 0.45,
    "perceived_benefit": 0.50,
    "decision_clarity": 0.46,
    "registration_reconsideration_rate": 0.030,
    "permanent_rejection_rate": 0.35,
    "activation_consideration_rate": 0.25,
    "mode_reconsideration_rate": 0.12,
    "shock_reconsideration_boost": 0.30,
    "visible_success_rate": 0.030,
    "bad_outcome_rate": 0.018,
    "platform_outage_rate": 0.005,
    "public_controversy_rate": 0.007,
    "trust_recovery_event_rate": 0.020,
    "trust_recovery_strength": 0.020,
    "micro_delegate_willingness": 0.25,
    "institutional_delegate_count": 24,
    "institutional_delegation_propensity": 0.25,
    "project_count": 80,
    "executor_count": 60,
    "fiscalizer_count": 35,
    "evidence_producer_count": 45,
    "executor_incentive_strength": 0.50,
    "fiscalizer_compensation": 0.45,
    "evidence_compensation": 0.42,
    "review_cost": 0.35,
    "evidence_cost": 0.35,
    "fiscalizer_capacity": 2.0,
    "evidence_producer_capacity": 1.5,
    "verification_requirement_per_project": 0.60,
    "evidence_requirement_per_project": 0.70,
    "role_entry_rate": 0.15,
    "role_exit_rate": 0.15,
    "funding_rate": 0.02,
    "default_routing_efficiency": 0.70,
    "planning_mode": "distributed",
    "planning_target_count": 16,
    "planning_round_interval": 4,
    "planning_attendance_scale": 1.0,
    "attentive_noise_base": 0.35,
    "attentive_salience_bias": 0.35,
    "micro_delegate_noise": 0.30,
    "micro_delegate_salience_bias": 0.20,
    "institutional_delegate_noise": 0.25,
    "salience_truth_mix": 0.25,
    "stale_signal_retention": 0.50,
    "central_planner_bandwidth_fraction": 0.30,
    "central_planner_noise": 0.25,
    # Attendance propensity per participation mode at planning rounds.
    # Calibratable from planning-behavior-calibration panel output.
    "planning_attendance_base": {
        "direct_active": 0.55,
        "hybrid": 0.40,
        "profile_driven": 0.15,
    },
    # Beta(a, b) priors for citizen traits. Synthetic defaults; replaceable by
    # llm-elicited or empirically fitted distributions (mark provenance in the
    # scenario file).
    "trait_distributions": {
        "digital_confidence": [2.2, 2.0],
        "civic_interest": [1.7, 2.3],
        "privacy_concern": [2.2, 2.1],
        "friction_tolerance": [2.0, 2.2],
        "social_influence_weight": [2.0, 2.0],
        "attention_budget": [1.6, 2.6],
        "need_relevance": [2.0, 2.5],
        "ideological_openness": [2.0, 1.8],
        "control_preference": [2.0, 2.0],
        "automation_trust": [1.8, 2.2],
    },
    "social_graph_degree": 8,
    "random_social_tie_probability": 0.015,
    "participation_temperature": 0.75,
    "delegate_temperature": 0.50,
    "reactivation_campaign_strength": 0.015,
}

INTEGRATION_KEYS = [
    "active_user_share",
    "registered_user_share",
    "registered_inactive_share",
    "aware_non_user_share",
    "permanent_rejection_share",
    "default_rule_share",
    "passive_delegated_share",
    "profile_driven_share",
    "direct_participation_share",
    "full_delegation_share",
    "partial_delegation_share",
    "delegator_share",
    "active_delegate_count",
    "delegation_concentration_hhi",
    "top_delegate_share",
    "micro_delegation_weight_share",
    "institutional_delegation_weight_share",
    "delegate_platform_use_rate",
    "delegate_switching_rate",
    "delegation_revocation_rate",
    "abandonment_share",
    "reactivation_rate",
    "mean_platform_trust",
    "mean_trust_registered",
    "executor_participation_rate",
    "honest_executor_share",
    "opportunistic_executor_share",
    "fiscalizer_supply_per_project",
    "evidence_supply_per_project",
    "verification_coverage_rate",
    "evidence_coverage_rate",
    "verification_market_depth",
    "thin_market_failure_rate",
    "negative_word_of_mouth_rate",
    "recommendation_rate",
    "attentive_share",
    "attentive_share_mean",
    "planning_representation_share",
    "planning_signal_coverage",
    "delegate_planning_coverage",
    "distributed_planning_correlation",
    "central_planning_correlation",
    "followed_planning_correlation",
    "value_delivered_share",
    "top_10_delegate_share",
    "sustained_active_user_share",
    "mean_awareness_to_registration_delay_ticks",
    "trust_p10",
    "trust_p50",
    "trust_p90",
]

# Minimum-viability thresholds (METRICS.md, "Minimum viability thresholds").
VIABILITY_THRESHOLDS = {
    "min_active_user_share": 0.10,
    "max_delegation_hhi": 0.15,
    "max_top_delegate_share": 0.20,
    "min_verification_coverage": 0.80,
    "min_evidence_coverage": 0.80,
    "min_executor_participation": 0.25,
    "max_abandonment_share": 0.25,
}


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def bernoulli(rng: random.Random, p: float) -> bool:
    return rng.random() < clamp(p)


def pearson(xs: List[float], ys: List[float]) -> float:
    n = len(xs)
    if n < 2 or n != len(ys):
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 0 or vy <= 0:
        return 0.0
    return cov / math.sqrt(vx * vy)


def quantile(sorted_values: List[float], q: float) -> float:
    if not sorted_values:
        return 0.0
    idx = q * (len(sorted_values) - 1)
    lo = int(math.floor(idx))
    hi = min(lo + 1, len(sorted_values) - 1)
    frac = idx - lo
    return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac


def softmax_choice(rng: random.Random, scores: Mapping[str, float], temperature: float) -> str:
    if not scores:
        raise ValueError("softmax_choice requires at least one option")
    tau = max(temperature, 1e-9)
    max_score = max(scores.values())
    weights = {k: math.exp((v - max_score) / tau) for k, v in scores.items()}
    total = sum(weights.values())
    threshold = rng.random() * total
    acc = 0.0
    last = next(iter(scores))
    for key, weight in weights.items():
        last = key
        acc += weight
        if acc >= threshold:
            return key
    return last


def _deep_update(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_update(result[key], value)
        else:
            result[key] = value
    return result


def normalize_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Accept legacy keys from earlier scenario files."""
    config = dict(config)
    if "delegate_count" in config:
        config.setdefault("institutional_delegate_count", config["delegate_count"])
        del config["delegate_count"]
    return config


def load_config(path: str | Path | None = None, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    if path:
        with Path(path).open("r", encoding="utf-8") as fh:
            config = _deep_update(config, normalize_config(json.load(fh)))
    if overrides:
        config = _deep_update(config, normalize_config(overrides))
    return config


class CitizenAgent(mesa.Agent):  # type: ignore[misc]
    """Potential or actual Core user. Can also act as a trusted micro-delegate."""

    def __init__(self, model: "BehavioralAdoptionModel", citizen_id: int):
        super().__init__(model)
        rng = self.random
        cfg = model.config
        self.citizen_id = citizen_id
        self.aware = bernoulli(rng, cfg["initial_awareness"])
        self.registered = False
        self.use_state = "aware_non_user" if self.aware else "unaware"
        self.delegate_ref: Optional[Tuple[str, int]] = None  # ("c", citizen_id) | ("i", delegate_id)
        self.first_awareness_tick: Optional[int] = 0 if self.aware else None
        self.first_registration_tick: Optional[int] = None
        self.last_activation_tick: Optional[int] = None
        self.last_abandonment_tick: Optional[int] = None
        self.considered_registration = False
        self.permanently_rejected = False

        self.trust_core = clamp(rng.gauss(cfg["initial_trust_mean"], cfg["initial_trust_spread"]))
        self.trust_evidence = clamp(rng.gauss(0.48, 0.18))
        self.trust_fiscalization = clamp(rng.gauss(0.46, 0.18))
        traits = cfg["trait_distributions"]
        self.digital_confidence = clamp(rng.betavariate(*traits["digital_confidence"]))
        self.civic_interest = clamp(rng.betavariate(*traits["civic_interest"]))
        self.privacy_concern = clamp(rng.betavariate(*traits["privacy_concern"]))
        self.friction_tolerance = clamp(rng.betavariate(*traits["friction_tolerance"]))
        self.social_influence_weight = clamp(rng.betavariate(*traits["social_influence_weight"]))
        self.attention_budget = clamp(rng.betavariate(*traits["attention_budget"]))
        self.need_relevance = clamp(rng.betavariate(*traits["need_relevance"]))
        self.ideological_openness = clamp(rng.betavariate(*traits["ideological_openness"]))
        self.control_preference = clamp(rng.betavariate(*traits["control_preference"]))
        self.automation_trust = clamp(rng.betavariate(*traits["automation_trust"]))
        self.values_position = rng.random()
        # Media reach limit for campaign-driven awareness (launch-stage ceiling).
        self.media_reachable = bernoulli(rng, cfg["awareness_ceiling"])
        # Latent willingness to act as a trusted micro-delegate for one's circle.
        self.micro_delegate_willing = bernoulli(
            rng, cfg["micro_delegate_willingness"] * (0.5 + self.civic_interest)
        )
        self.delegated_weight = 0.0  # weight received from other citizens
        self.consecutive_active_ticks = 0

    @property
    def is_active(self) -> bool:
        return self.use_state in {"direct_active", "profile_driven", "delegated", "hybrid"}

    @property
    def is_delegating(self) -> bool:
        return self.use_state in {"delegated", "hybrid"} and self.delegate_ref is not None

    def can_receive_delegation(self) -> bool:
        return self.micro_delegate_willing and self.registered and self.use_state != "abandoned"

    def social_signal(self) -> Dict[str, float]:
        neighbors = self.model.social_graph.get(self.citizen_id, [])
        if not neighbors:
            return {"active": 0.0, "registered": 0.0, "abandoned": 0.0, "recommending": 0.0}
        agents = [self.model.citizens[n] for n in neighbors]
        n = len(agents)
        return {
            "active": sum(a.is_active for a in agents) / n,
            "registered": sum(a.registered for a in agents) / n,
            "abandoned": sum(a.use_state == "abandoned" for a in agents) / n,
            "recommending": sum(a.is_active and a.trust_core >= 0.62 for a in agents) / n,
        }

    def awareness_step(self) -> None:
        if self.aware:
            return
        cfg = self.model.config
        s = self.social_signal()
        p = (
            (cfg["campaign_intensity"] if self.media_reachable else 0.0)
            + cfg["social_influence_strength"] * self.social_influence_weight * s["registered"]
            + 0.01 * self.civic_interest
            + 0.01 * self.need_relevance
        )
        if bernoulli(self.random, p):
            self.aware = True
            self.use_state = "aware_non_user"
            self.first_awareness_tick = self.model.tick

    def registration_step(self) -> None:
        if not self.aware or self.registered or self.permanently_rejected or self.use_state == "abandoned":
            return
        cfg = self.model.config
        s = self.social_signal()
        # Registration is considered seriously once, on first exposure; afterwards
        # only occasionally, mostly re-triggered by social proof. This prevents a
        # constant weekly hazard from saturating registration over long horizons.
        if self.considered_registration:
            p_consider = cfg["registration_reconsideration_rate"] + 0.25 * s["recommending"]
            if not bernoulli(self.random, p_consider):
                return
        self.considered_registration = True
        x = (
            -2.40
            + 1.35 * cfg["perceived_benefit"]
            + 12.0 * cfg["recommendation_strength"] * s["recommending"] * self.social_influence_weight
            + 1.25 * self.trust_core
            + 0.85 * self.need_relevance
            + 0.55 * cfg["ai_tutor_quality"]
            + 0.45 * cfg["public_legitimacy"]
            - 1.60 * cfg["onboarding_friction"] * (1.0 - self.friction_tolerance)
            - 1.25 * self.privacy_concern * (1.0 - cfg["privacy_guarantee_strength"])
            - 0.85 * (1.0 - self.ideological_openness)
            - 10.0 * cfg["negative_word_of_mouth_strength"] * s["abandoned"] * self.social_influence_weight
        )
        if bernoulli(self.random, sigmoid(x)):
            self.registered = True
            self.use_state = "registered_inactive"
            self.first_registration_tick = self.model.tick
        elif bernoulli(
            self.random,
            cfg["permanent_rejection_rate"] * clamp(0.6 * (1.0 - self.ideological_openness) + 0.4 * self.privacy_concern),
        ):
            # ROLE_ONTOLOGY.md, aware non-user: "reject permanently".
            self.permanently_rejected = True
            self.use_state = "rejected"

    def activation_step(self) -> None:
        if not self.registered or self.use_state == "abandoned":
            return
        cfg = self.model.config
        if self.use_state == "registered_inactive":
            if not bernoulli(self.random, cfg["activation_consideration_rate"]):
                return
            s = self.social_signal()
            x = (
                -1.25
                + 1.10 * cfg["decision_clarity"]
                + 0.85 * self.trust_core
                + 0.65 * self.civic_interest
                + 0.55 * self.need_relevance
                + 0.70 * self.digital_confidence
                + 0.70 * cfg["ai_tutor_quality"]
                + 0.55 * self.model.visible_success_stock
                + 0.50 * s["active"]
                - 1.00 * cfg["interface_complexity"] * (1.0 - self.digital_confidence)
                - 0.75 * (1.0 - self.attention_budget)
            )
            if not bernoulli(self.random, sigmoid(x)):
                return
            self.last_activation_tick = self.model.tick
            self.set_participation_mode()
            return
        # Active users keep their mode unless they reconsider it; shocks raise
        # the reconsideration probability (revocation elasticity, METRICS.md).
        shock = max(
            self.model.current_outage,
            self.model.current_controversy,
            1.0 if self.model.visible_failure_stock > 0.30 else 0.0,
        )
        p_reconsider = cfg["mode_reconsideration_rate"] + cfg["shock_reconsideration_boost"] * shock
        if bernoulli(self.random, p_reconsider):
            self.set_participation_mode()

    def set_participation_mode(self) -> None:
        cfg = self.model.config
        s = self.social_signal()
        micro_available = any(
            self.model.citizens[n].can_receive_delegation()
            for n in self.model.social_graph.get(self.citizen_id, [])
        )
        institutional_quality = self.model.average_delegate_reputation()
        delegate_quality = max(institutional_quality, 0.80 if micro_available else 0.0)
        concentration = self.model.delegation_concentration_hhi()
        complexity_cost = cfg["interface_complexity"] * (1.0 - self.digital_confidence)
        scores = {
            "direct_active": self.civic_interest + self.control_preference + self.attention_budget + self.trust_evidence - complexity_cost,
            "profile_driven": self.automation_trust + cfg["ai_tutor_quality"] + cfg["decision_clarity"] + 0.35 * self.need_relevance - 0.35 * self.control_preference,
            "delegated": delegate_quality + s["active"] + 0.65 * (1.0 - self.attention_budget) + 0.45 * (1.0 - self.control_preference) - 0.75 * concentration,
            "hybrid": 0.50 * self.civic_interest + 0.45 * self.control_preference + 0.45 * delegate_quality + 0.35 * cfg["ai_tutor_quality"] - 0.25 * complexity_cost,
            "registered_inactive": 0.80 * (1.0 - self.trust_core) + 0.55 * complexity_cost + 0.35 * (1.0 - self.need_relevance),
        }
        new_state = softmax_choice(self.random, scores, cfg["participation_temperature"])
        if self.delegate_ref is not None and new_state not in {"delegated", "hybrid"}:
            self.model.release_delegation(self, revocation=True)
        self.use_state = new_state
        if self.use_state in {"delegated", "hybrid"}:
            self.choose_delegate()

    def choose_delegate(self) -> None:
        cfg = self.model.config
        total_weight = self.model.total_delegated_weight()
        # Trusted microdelegation channel: willing, registered, non-abandoned
        # people in the citizen's own social circle (TRUSTED_MICRODELEGATION_MODEL.md).
        micro_scores: Dict[str, float] = {}
        for n in self.model.social_graph.get(self.citizen_id, []):
            cand = self.model.citizens[n]
            if not cand.can_receive_delegation():
                continue
            if cand.delegate_ref == ("c", self.citizen_id):
                continue  # avoid trivial two-cycles
            alignment = 1.0 - abs(self.values_position - cand.values_position)
            weight_share = (cand.delegated_weight / total_weight) if total_weight else 0.0
            micro_scores[f"c{cand.citizen_id}"] = (
                1.05 * alignment
                + 0.45 * cand.civic_interest
                + 0.45  # proximity-trust premium: known person, visible acts, one-click revocation
                - 0.60 * weight_share
            )
        # Institutional channel: remains available but carries a propensity
        # penalty — the corpus treats broker/institutional delegation as the
        # stress channel, not the baseline.
        inst_scores: Dict[str, float] = {}
        for d in self.model.delegates:
            alignment = 1.0 - abs(self.values_position - d.alignment_vector)
            weight_share = (d.delegated_weight / total_weight) if total_weight else 0.0
            inst_scores[f"i{d.delegate_id}"] = (
                0.95 * alignment
                + 1.15 * d.reputation
                + 0.50 * d.visibility
                - 0.70 * d.conflict_risk
                - 0.60 * weight_share
                - (1.0 - cfg["institutional_delegation_propensity"])
            )
        # Two-stage choice: pick the channel by comparing the best option in
        # each, then pick the delegate inside the chosen channel. A single
        # softmax over both pools would let the institutional channel win by
        # sheer candidate count, inverting the corpus's microdelegation baseline.
        if micro_scores and inst_scores:
            channel = softmax_choice(
                self.random,
                {"micro": max(micro_scores.values()), "inst": max(inst_scores.values())},
                cfg["delegate_temperature"],
            )
            scores = micro_scores if channel == "micro" else inst_scores
        elif micro_scores:
            scores = micro_scores
        elif inst_scores and bernoulli(self.random, cfg["institutional_delegation_propensity"]):
            # No trusted person available: only propensity-many citizens hand
            # weight to an impersonal delegate; the rest fall back to the
            # public default rule (docs/101).
            scores = inst_scores
        else:
            self.use_state = "registered_inactive"
            return
        chosen_key = softmax_choice(self.random, scores, cfg["delegate_temperature"])
        chosen_ref = (chosen_key[0], int(chosen_key[1:]))
        if self.delegate_ref == chosen_ref:
            return
        if self.delegate_ref is not None:
            self.model.release_delegation(self, revocation=False)
            self.model.switches_cum += 1
        self.delegate_ref = chosen_ref
        self.model.delegation_target(chosen_ref).delegated_weight += 1.0

    def trust_step(self) -> None:
        if not self.aware:
            return  # unaware citizens hold their prior; they have nothing to update on
        cfg = self.model.config
        s = self.social_signal()
        delta = 0.020 * self.model.visible_success_stock
        delta -= 0.025 * self.model.visible_failure_stock
        delta -= 0.020 * self.model.current_outage
        delta -= 0.030 * self.model.current_controversy
        delta += 0.010 * s["active"] * self.social_influence_weight
        delta -= 0.018 * s["abandoned"] * self.social_influence_weight
        delta += cfg["trust_recovery_strength"] * self.model.current_recovery_event
        if self.is_active:
            delta += self.random.gauss(0.0015, 0.008)
        self.trust_core = clamp(self.trust_core + delta)

    def churn_step(self) -> None:
        cfg = self.model.config
        if self.registered and self.use_state != "abandoned":
            s = self.social_signal()
            x = (
                -5.20
                + 1.25 * self.model.visible_failure_stock
                + 1.00 * self.model.current_controversy
                + 0.85 * self.model.current_outage
                + 0.70 * cfg["interface_complexity"] * (1.0 - self.friction_tolerance)
                + 1.90 * (1.0 - self.trust_core)
                + 0.45 * s["abandoned"]
                - 0.55 * self.model.visible_success_stock
            )
            if bernoulli(self.random, sigmoid(x)):
                if self.delegate_ref is not None:
                    self.model.release_delegation(self, revocation=True)
                self.use_state = "abandoned"
                self.last_abandonment_tick = self.model.tick
                self.model.abandonments_cum += 1
                contributors = {
                    "failure_exposure": 1.25 * self.model.visible_failure_stock,
                    "controversy_or_outage": 1.00 * self.model.current_controversy + 0.85 * self.model.current_outage,
                    "friction": 0.70 * cfg["interface_complexity"] * (1.0 - self.friction_tolerance),
                    "low_trust": 1.90 * (1.0 - self.trust_core),
                    "negative_social_signal": 0.45 * s["abandoned"],
                }
                reason = max(contributors, key=lambda k: contributors[k])
                self.model.abandonment_reasons[reason] = self.model.abandonment_reasons.get(reason, 0) + 1
            return
        if self.use_state == "abandoned":
            x = -3.00 + 1.20 * self.model.visible_success_stock + 0.80 * cfg["reactivation_campaign_strength"] + 0.65 * self.trust_core - 0.85 * self.model.visible_failure_stock
            if bernoulli(self.random, sigmoid(x)):
                self.use_state = "registered_inactive"
                self.trust_core = clamp(self.trust_core + 0.08)
                self.model.reactivations_cum += 1


class DelegateAgent(mesa.Agent):  # type: ignore[misc]
    """Institutional / high-visibility delegate (the stress channel, not the baseline)."""

    def __init__(self, model: "BehavioralAdoptionModel", delegate_id: int):
        super().__init__(model)
        rng = self.random
        self.delegate_id = delegate_id
        self.reputation = clamp(rng.gauss(0.55, 0.18))
        self.visibility = clamp(rng.betavariate(1.5, 3.0))
        self.alignment_vector = clamp(rng.random())
        self.competence = clamp(rng.gauss(0.55, 0.18))
        self.conflict_risk = clamp(rng.betavariate(1.3, 5.0))
        self.delegated_weight = 0.0

    def step(self) -> None:
        if self.delegated_weight <= 0:
            self.reputation = clamp(self.reputation + self.random.gauss(0.0, 0.005))
            return
        performance = clamp(0.55 * self.competence + 0.35 * self.model.visible_success_stock - 0.45 * self.conflict_risk)
        self.reputation = clamp(0.96 * self.reputation + 0.04 * performance)


class ProjectAgent(mesa.Agent):  # type: ignore[misc]
    def __init__(self, model: "BehavioralAdoptionModel", project_id: int):
        super().__init__(model)
        rng = self.random
        self.project_id = project_id
        self.latent_value = clamp(rng.betavariate(2.0, 2.0))
        self.salience = clamp(rng.betavariate(1.5, 2.5))
        self.category = rng.randrange(int(model.config["planning_target_count"]))
        # Shared public perception of quality: what active citizens route on.
        self.perceived_quality = clamp(self.latent_value + rng.gauss(0.0, 0.20))
        self.funding_progress = 0.0
        self.outcome_state = "pending"


class ExecutorAgent(mesa.Agent):  # type: ignore[misc]
    def __init__(self, model: "BehavioralAdoptionModel", executor_id: int):
        super().__init__(model)
        rng = self.random
        self.executor_id = executor_id
        self.honesty_type = "opportunistic" if bernoulli(rng, 0.28) else "honest"
        self.ability = clamp(rng.gauss(0.58, 0.17))
        self.cost_structure = clamp(rng.betavariate(2.0, 2.0))
        self.liquidity_constraint = clamp(rng.betavariate(2.2, 2.0))
        self.reputation_stake = clamp(rng.betavariate(2.0, 2.0))
        self.participating = False

    def propensity(self) -> float:
        cfg = self.model.config
        x = -0.60 + 1.15 * cfg["executor_incentive_strength"] + 0.65 * self.reputation_stake + 0.40 * self.ability - 0.75 * self.cost_structure - 0.35 * self.liquidity_constraint
        return sigmoid(x)

    def step(self) -> None:
        self.participating = self.model.role_market_step(self.participating, self.propensity(), self.random)


class FiscalizerAgent(mesa.Agent):  # type: ignore[misc]
    def __init__(self, model: "BehavioralAdoptionModel", fiscalizer_id: int):
        super().__init__(model)
        rng = self.random
        self.fiscalizer_id = fiscalizer_id
        self.competence = clamp(rng.gauss(0.58, 0.18))
        self.independence = clamp(rng.gauss(0.60, 0.18))
        self.capture_risk = clamp(rng.betavariate(1.3, 4.5))
        self.reputation_stake = clamp(rng.betavariate(2.0, 2.0))
        self.participating = False

    def propensity(self) -> float:
        cfg = self.model.config
        x = -0.85 + 1.05 * cfg["fiscalizer_compensation"] + 0.70 * self.reputation_stake + 0.55 * self.competence + 0.45 * self.independence - 0.85 * cfg["review_cost"] - 0.40 * self.capture_risk
        return sigmoid(x)

    def step(self) -> None:
        self.participating = self.model.role_market_step(self.participating, self.propensity(), self.random)


class EvidenceProducerAgent(mesa.Agent):  # type: ignore[misc]
    def __init__(self, model: "BehavioralAdoptionModel", producer_id: int):
        super().__init__(model)
        rng = self.random
        self.producer_id = producer_id
        self.method_quality = clamp(rng.gauss(0.56, 0.18))
        self.independence = clamp(rng.gauss(0.58, 0.18))
        self.coverage = clamp(rng.betavariate(2.0, 2.2))
        self.capture_risk = clamp(rng.betavariate(1.3, 4.5))
        self.participating = False

    def propensity(self) -> float:
        cfg = self.model.config
        x = -0.80 + 1.05 * cfg["evidence_compensation"] + 0.55 * self.method_quality + 0.45 * self.independence + 0.35 * self.coverage - 0.85 * cfg["evidence_cost"] - 0.45 * self.capture_risk
        return sigmoid(x)

    def step(self) -> None:
        self.participating = self.model.role_market_step(self.participating, self.propensity(), self.random)


class BehavioralAdoptionModel(mesa.Model):  # type: ignore[misc]
    """Simulates adoption, delegation, trust, abandonment, and role-market supply."""

    def __init__(self, config: Dict[str, Any]):
        self.config = _deep_update(DEFAULT_CONFIG, normalize_config(config))
        self.seed = int(self.config.get("seed", 42))
        try:
            super().__init__(rng=self.seed)  # Mesa 3.x: integer seed, not a Random object
        except TypeError:  # pragma: no cover - older base-class signatures
            try:
                super().__init__(seed=self.seed)
            except TypeError:
                super().__init__()
        # One seeded stream for everything, regardless of Mesa presence/version,
        # so runs are byte-identical across environments.
        self.random = random.Random(self.seed)
        self.tick = 0
        self.current_outage = 0.0
        self.current_controversy = 0.0
        self.current_recovery_event = 0.0
        self.visible_success_stock = 0.0
        self.visible_failure_stock = 0.0
        self.revocations_cum = 0
        self.switches_cum = 0
        self.abandonments_cum = 0
        self.reactivations_cum = 0
        self.delegator_ticks_cum = 0
        self.abandonment_reasons: Dict[str, int] = {}
        self.history: List[Dict[str, float]] = []

        cfg = self.config
        # Planning world: latent public needs and their (only partially truthful)
        # visibility. Salience is what herding and planner attention see.
        j_count = int(cfg["planning_target_count"])
        raw_need = [self.random.gammavariate(2.0, 1.0) for _ in range(j_count)]
        need_total = sum(raw_need)
        self.true_need = [v / need_total for v in raw_need]
        raw_vis = [self.random.gammavariate(2.0, 1.0) for _ in range(j_count)]
        vis_total = sum(raw_vis)
        truth_mix = cfg["salience_truth_mix"]  # visibility is mostly not need
        mixed = [truth_mix * self.true_need[j] + (1.0 - truth_mix) * raw_vis[j] / vis_total for j in range(j_count)]
        mix_total = sum(mixed)
        self.target_salience = [v / mix_total for v in mixed]
        uniform = 1.0 / j_count
        self.distributed_vector = [uniform] * j_count
        self.central_vector = [uniform] * j_count
        self.attentive_share_last = 0.0
        self.attentive_shares: List[float] = []
        self.planning_representation_last = 0.0
        self.planning_coverage_last = 0.0
        self.delegate_coverage_last = 0.0
        self.delivered_value_cum = 0.0

        self.citizens = [CitizenAgent(self, i) for i in range(int(cfg["population_size"]))]
        self.delegates = [DelegateAgent(self, i) for i in range(int(cfg["institutional_delegate_count"]))]
        self.projects = [ProjectAgent(self, i) for i in range(int(cfg["project_count"]))]
        self.executors = [ExecutorAgent(self, i) for i in range(int(cfg["executor_count"]))]
        self.fiscalizers = [FiscalizerAgent(self, i) for i in range(int(cfg["fiscalizer_count"]))]
        self.evidence_producers = [EvidenceProducerAgent(self, i) for i in range(int(cfg["evidence_producer_count"]))]
        # need_weight scales value so the portfolio-average category is worth 1.
        self.total_potential_value = sum(p.latent_value * self.need_weight(p.category) for p in self.projects)
        self.social_graph = self._build_social_graph()
        self.collect_metrics()

    def need_weight(self, category: int) -> float:
        return self.true_need[category] * len(self.true_need)

    # ------------------------------------------------------------------ setup

    def _build_social_graph(self) -> Dict[int, List[int]]:
        n = len(self.citizens)
        degree = max(2, int(self.config["social_graph_degree"]))
        half = max(1, degree // 2)
        graph: Dict[int, set[int]] = {i: set() for i in range(n)}
        for i in range(n):
            for offset in range(1, half + 1):
                for j in ((i + offset) % n, (i - offset) % n):
                    graph[i].add(j)
                    graph[j].add(i)
        for i in range(n):
            for _ in range(degree):
                if bernoulli(self.random, self.config["random_social_tie_probability"]):
                    j = self.random.randrange(n)
                    if i != j:
                        graph[i].add(j)
                        graph[j].add(i)
        return {i: sorted(v) for i, v in graph.items()}

    # ------------------------------------------------------------ delegation

    def delegation_target(self, ref: Tuple[str, int]):
        kind, idx = ref
        return self.citizens[idx] if kind == "c" else self.delegates[idx]

    def release_delegation(self, citizen: CitizenAgent, revocation: bool) -> None:
        if citizen.delegate_ref is None:
            return
        target = self.delegation_target(citizen.delegate_ref)
        target.delegated_weight = max(0.0, target.delegated_weight - 1.0)
        citizen.delegate_ref = None
        if revocation:
            self.revocations_cum += 1

    def _validate_delegations(self) -> None:
        """Revoke delegations whose micro-delegate is no longer a valid target."""
        for c in self.citizens:
            if c.delegate_ref is None or c.delegate_ref[0] != "c":
                continue
            target = self.citizens[c.delegate_ref[1]]
            if not target.can_receive_delegation():
                self.release_delegation(c, revocation=True)
                if c.use_state in {"delegated", "hybrid"}:
                    c.choose_delegate()

    def total_delegated_weight(self) -> float:
        return sum(c.delegated_weight for c in self.citizens) + sum(d.delegated_weight for d in self.delegates)

    # ------------------------------------------------------------ role market

    def role_market_step(self, participating: bool, propensity: float, rng: random.Random) -> bool:
        """Sticky recruitment/dropout instead of an i.i.d. weekly redraw."""
        cfg = self.config
        if participating:
            if bernoulli(rng, cfg["role_exit_rate"]) and not bernoulli(rng, propensity):
                return False
            return True
        if bernoulli(rng, cfg["role_entry_rate"]) and bernoulli(rng, propensity):
            return True
        return False

    # ------------------------------------------------------------------- step

    def step(self) -> None:
        self.tick += 1
        self._platform_events()
        for c in self.citizens:
            c.awareness_step()
        for c in self.citizens:
            c.registration_step()
        for c in self.citizens:
            c.activation_step()
        self._validate_delegations()
        for d in self.delegates:
            d.step()
        if self.tick % int(self.config["planning_round_interval"]) == 0:
            self._planning_round()
        self._fund_projects()
        for e in self.executors:
            e.step()
        for f in self.fiscalizers:
            f.step()
        for ep in self.evidence_producers:
            ep.step()
        self._project_outcomes()
        for c in self.citizens:
            c.trust_step()
        for c in self.citizens:
            c.churn_step()
        for c in self.citizens:
            c.consecutive_active_ticks = c.consecutive_active_ticks + 1 if c.is_active else 0
        self.delegator_ticks_cum += sum(c.is_delegating for c in self.citizens)
        self.collect_metrics()

    def run(self, ticks: Optional[int] = None) -> None:
        for _ in range(int(ticks if ticks is not None else self.config["ticks"])):
            self.step()

    # ------------------------------------------------------------- planning

    def _planning_round(self) -> None:
        """Construct the distributed and central planning vectors for this cycle.

        Attentive citizens and active delegates contribute noisy, partial-coverage
        signals about latent public needs (CORE_V0_PLANNING_CHANNEL_MODEL.md);
        allocation profiles and passive default routing contribute nothing.
        The central comparator is a bandwidth-limited, salience-guided planner.
        """
        cfg = self.config
        j_count = len(self.true_need)
        sums = [0.0] * j_count
        weights = [0.0] * j_count
        attentive = 0
        represented_weight = 0.0
        attendance = cfg["planning_attendance_base"]
        for c in self.citizens:
            base = attendance.get(c.use_state)
            if base is None:
                continue
            p_attend = base * (0.5 + 0.5 * c.civic_interest) * cfg["planning_attendance_scale"]
            if not bernoulli(self.random, p_attend):
                continue
            attentive += 1
            represented_weight += 1.0
            k = max(1, round(0.5 * c.attention_budget * j_count))
            noise_sd = cfg["attentive_noise_base"] * (1.0 - 0.4 * c.civic_interest)
            bias = cfg["attentive_salience_bias"]
            # Coverage bias: attention clusters on visible needs, so invisible
            # ones can stay unreviewed (the sibling experiment's
            # attentiveCoverageBias / attentiveSalienceBias distortion family).
            sample_weights = [0.4 + 0.6 * s * j_count for s in self.target_salience]
            for j in set(self.random.choices(range(j_count), weights=sample_weights, k=k)):
                perceived = (1.0 - bias) * self.true_need[j] + bias * self.target_salience[j]
                sums[j] += max(0.0, perceived * (1.0 + self.random.gauss(0.0, noise_sd)))
                weights[j] += 1.0
        # Delegated planning signals: delegates carry their delegators' weight,
        # gated by their own platform activity and partial planning coverage.
        coverage_num = 0.0
        coverage_den = 0.0
        for c in self.citizens:
            if c.delegated_weight <= 0 or not c.is_active:
                continue
            frac = 0.30 + 0.45 * c.attention_budget
            coverage_num += frac * c.delegated_weight
            coverage_den += c.delegated_weight
            represented_weight += c.delegated_weight
            k = max(1, round(frac * j_count))
            noise_sd = cfg["micro_delegate_noise"] * (1.0 - 0.3 * c.civic_interest)
            bias = cfg["micro_delegate_salience_bias"]  # they know their circle's real needs better
            for j in self.random.sample(range(j_count), k):
                perceived = (1.0 - bias) * self.true_need[j] + bias * self.target_salience[j]
                sums[j] += c.delegated_weight * max(0.0, perceived * (1.0 + self.random.gauss(0.0, noise_sd)))
                weights[j] += c.delegated_weight
        for d in self.delegates:
            if d.delegated_weight <= 0:
                continue
            frac = 0.70  # active professionals, broad but politically packaged review
            coverage_num += frac * d.delegated_weight
            coverage_den += d.delegated_weight
            represented_weight += d.delegated_weight
            k = max(1, round(frac * j_count))
            for j in self.random.sample(range(j_count), k):
                packaged = 0.8 * self.true_need[j] + 0.2 * self.target_salience[j]
                sums[j] += d.delegated_weight * max(0.0, packaged * (1.0 + self.random.gauss(0.0, cfg["institutional_delegate_noise"])))
                weights[j] += d.delegated_weight
        uniform = 1.0 / j_count
        retention = cfg["stale_signal_retention"]
        new_vector = [
            sums[j] / weights[j] if weights[j] > 0
            else retention * self.distributed_vector[j] + (1.0 - retention) * uniform
            for j in range(j_count)
        ]
        total = sum(new_vector)
        self.distributed_vector = [v / total for v in new_vector] if total > 0 else [uniform] * j_count
        # Central comparator: reviews the most salient targets with bounded
        # bandwidth; unreviewed targets default to visibility itself.
        k_central = max(1, round(cfg["central_planner_bandwidth_fraction"] * j_count))
        by_salience = sorted(range(j_count), key=lambda j: self.target_salience[j], reverse=True)
        reviewed = set(by_salience[:k_central])
        central = [
            max(0.0, self.true_need[j] * (1.0 + self.random.gauss(0.0, cfg["central_planner_noise"])))
            if j in reviewed else self.target_salience[j]
            for j in range(j_count)
        ]
        total_c = sum(central)
        self.central_vector = [v / total_c for v in central] if total_c > 0 else [uniform] * j_count

        population = len(self.citizens)
        self.attentive_share_last = attentive / population if population else 0.0
        self.attentive_shares.append(self.attentive_share_last)
        self.planning_representation_last = represented_weight / population if population else 0.0
        self.planning_coverage_last = sum(1 for w in weights if w > 0) / j_count
        self.delegate_coverage_last = coverage_num / coverage_den if coverage_den else 0.0

    def followed_vector(self) -> List[float]:
        return self.central_vector if self.config["planning_mode"] == "central" else self.distributed_vector

    def _fund_projects(self) -> None:
        cfg = self.config
        pending = [p for p in self.projects if p.outcome_state == "pending"]
        if not pending:
            return
        vector = self.followed_vector()
        category_counts = Counter(p.category for p in pending)
        # Active citizens route on visibility and perceived quality; the
        # non-active remainder allocates through the public default rule,
        # which tracks the published planning priorities (docs/101).
        active = self.active_user_share()
        active_raw = [0.5 * p.salience + 0.5 * p.perceived_quality for p in pending]
        default_raw = [vector[p.category] / category_counts[p.category] for p in pending]
        mean_a = sum(active_raw) / len(active_raw)
        mean_d = sum(default_raw) / len(default_raw)
        for p, a_raw, d_raw in zip(pending, active_raw, default_raw):
            a_hat = a_raw / mean_a if mean_a > 0 else 1.0
            d_hat = d_raw / mean_d if mean_d > 0 else 1.0
            flow = active * a_hat + (1.0 - active) * cfg["default_routing_efficiency"] * d_hat
            p.funding_progress = clamp(p.funding_progress + cfg["funding_rate"] * 0.4 * flow)

    def _platform_events(self) -> None:
        cfg = self.config
        self.current_outage = 1.0 if bernoulli(self.random, cfg["platform_outage_rate"]) else 0.0
        self.current_controversy = 1.0 if bernoulli(self.random, cfg["public_controversy_rate"]) else 0.0
        self.current_recovery_event = 1.0 if bernoulli(self.random, cfg["trust_recovery_event_rate"]) else 0.0
        if bernoulli(self.random, cfg["visible_success_rate"]):
            self.visible_success_stock = clamp(self.visible_success_stock + 0.08)
        if bernoulli(self.random, cfg["bad_outcome_rate"]):
            self.visible_failure_stock = clamp(self.visible_failure_stock + 0.10)
        self.visible_success_stock = clamp(self.visible_success_stock * 0.975)
        self.visible_failure_stock = clamp(self.visible_failure_stock * 0.970)

    def _project_outcomes(self) -> None:
        n_projects = max(1, len(self.projects))
        verification_coverage = self.verification_coverage_rate()
        evidence_coverage = self.evidence_coverage_rate()
        executor_rate = self.executor_participation_rate()
        honest_share = self.honest_executor_share()
        for project in self.projects:
            if project.funding_progress < 0.75 or project.outcome_state != "pending":
                continue
            p_success = clamp(
                0.15
                + 0.35 * project.latent_value
                + 0.15 * executor_rate
                + 0.10 * honest_share
                + 0.125 * verification_coverage
                + 0.125 * evidence_coverage
            )
            if bernoulli(self.random, p_success):
                project.outcome_state = "successful"
                self.delivered_value_cum += project.latent_value * self.need_weight(project.category)
                self.visible_success_stock = clamp(self.visible_success_stock + 2.4 / n_projects)
            else:
                project.outcome_state = "failed"
                self.visible_failure_stock = clamp(self.visible_failure_stock + 3.2 / n_projects)

    # ---------------------------------------------------------------- metrics

    def collect_metrics(self) -> Dict[str, float]:
        metrics = self.metrics()
        self.history.append(metrics)
        return metrics

    def final_metrics(self) -> Dict[str, float]:
        return self.history[-1]

    def viability_flags(self) -> Dict[str, bool]:
        m = self.final_metrics()
        t = VIABILITY_THRESHOLDS
        third = max(1, len(self.history) // 3)
        trust_series = [h["mean_platform_trust"] for h in self.history]
        trust_declining = (
            len(trust_series) >= 3
            and trust_series[-1] < trust_series[-third] < trust_series[-2 * third]
        )
        return {
            "active_signal_low": m["active_user_share"] < t["min_active_user_share"],
            "delegation_overconcentrated": (
                m["delegation_concentration_hhi"] > t["max_delegation_hhi"]
                or m["top_delegate_share"] > t["max_top_delegate_share"]
            ),
            "verification_undersupplied": m["verification_coverage_rate"] < t["min_verification_coverage"],
            "evidence_undersupplied": m["evidence_coverage_rate"] < t["min_evidence_coverage"],
            "executor_supply_low": m["executor_participation_rate"] < t["min_executor_participation"],
            "abandonment_high": m["abandonment_share"] > t["max_abandonment_share"],
            "trust_declining": trust_declining,
            # The behavioral population failed to out-inform the bandwidth-limited planner.
            "distributed_planning_weak": m["distributed_planning_correlation"] < m["central_planning_correlation"],
        }

    def integration_outputs(self) -> Dict[str, Any]:
        m = self.final_metrics()
        return {
            "scenario_id": self.config["scenario_id"],
            **{k: m.get(k, 0.0) for k in INTEGRATION_KEYS},
            "viability": self.viability_flags(),
        }

    def metrics(self) -> Dict[str, float]:
        total = len(self.citizens)
        registered = [c for c in self.citizens if c.registered]
        active = [c for c in self.citizens if c.is_active]
        counts = Counter(c.use_state for c in self.citizens)
        reg_n = len(registered)
        aware_n = sum(c.aware for c in self.citizens)
        delegators = sum(c.is_delegating for c in self.citizens)
        fs = self.fiscalizer_supply_per_project()
        es = self.evidence_supply_per_project()
        vc = self.verification_coverage_rate()
        ec = self.evidence_coverage_rate()
        active_share = len(active) / total if total else 0.0
        return {
            "tick": float(self.tick),
            "awareness_rate": aware_n / total if total else 0.0,
            "registered_user_share": reg_n / total if total else 0.0,
            "registration_rate_among_aware": reg_n / aware_n if aware_n else 0.0,
            "permanent_rejection_share": counts["rejected"] / total if total else 0.0,
            "activation_rate_registered": len(active) / reg_n if reg_n else 0.0,
            "active_user_share": active_share,
            # docs/101: the non-active remainder allocates via the public default rule.
            "default_rule_share": 1.0 - active_share,
            "registered_inactive_share": counts["registered_inactive"] / reg_n if reg_n else 0.0,
            "aware_non_user_share": counts["aware_non_user"] / total if total else 0.0,
            "direct_participation_share": counts["direct_active"] / reg_n if reg_n else 0.0,
            "profile_driven_share": counts["profile_driven"] / reg_n if reg_n else 0.0,
            "passive_delegated_share": counts["delegated"] / reg_n if reg_n else 0.0,
            "hybrid_participation_share": counts["hybrid"] / reg_n if reg_n else 0.0,
            "full_delegation_share": counts["delegated"] / reg_n if reg_n else 0.0,
            "partial_delegation_share": counts["hybrid"] / reg_n if reg_n else 0.0,
            "delegation_rate": delegators / reg_n if reg_n else 0.0,
            "delegator_share": delegators / total if total else 0.0,
            "active_delegate_count": float(self.active_delegate_count()),
            "delegation_concentration_hhi": self.delegation_concentration_hhi(),
            "top_delegate_share": self.top_delegate_share(),
            "micro_delegation_weight_share": self.micro_delegation_weight_share(),
            "institutional_delegation_weight_share": 1.0 - self.micro_delegation_weight_share() if self.total_delegated_weight() else 0.0,
            "delegate_platform_use_rate": self.delegate_platform_use_rate(),
            "delegate_switching_rate": self.switches_cum / self.delegator_ticks_cum if self.delegator_ticks_cum else 0.0,
            "delegation_revocation_rate": self.revocations_cum / self.delegator_ticks_cum if self.delegator_ticks_cum else 0.0,
            "abandonment_share": counts["abandoned"] / reg_n if reg_n else 0.0,
            "reactivation_rate": self.reactivations_cum / self.abandonments_cum if self.abandonments_cum else 0.0,
            "mean_platform_trust": sum(c.trust_core for c in self.citizens) / total if total else 0.0,
            "mean_trust_registered": sum(c.trust_core for c in registered) / reg_n if reg_n else 0.0,
            "executor_participation_rate": self.executor_participation_rate(),
            "honest_executor_share": self.honest_executor_share(),
            "opportunistic_executor_share": self.opportunistic_executor_share(),
            "fiscalizer_supply_per_project": fs,
            "evidence_supply_per_project": es,
            "verification_coverage_rate": vc,
            "evidence_coverage_rate": ec,
            "verification_market_depth": min(vc, ec),
            "thin_market_failure_rate": clamp(1.0 - min(vc, ec)),
            "negative_word_of_mouth_rate": self.negative_word_of_mouth_rate(),
            "recommendation_rate": self.recommendation_rate(),
            "visible_success_stock": self.visible_success_stock,
            "visible_failure_stock": self.visible_failure_stock,
            "attentive_share": self.attentive_share_last,
            "attentive_share_mean": sum(self.attentive_shares) / len(self.attentive_shares) if self.attentive_shares else 0.0,
            "planning_representation_share": self.planning_representation_last,
            "planning_signal_coverage": self.planning_coverage_last,
            "delegate_planning_coverage": self.delegate_coverage_last,
            "distributed_planning_correlation": pearson(self.distributed_vector, self.true_need),
            "central_planning_correlation": pearson(self.central_vector, self.true_need),
            "followed_planning_correlation": pearson(self.followed_vector(), self.true_need),
            "value_delivered_share": self.delivered_value_cum / self.total_potential_value if self.total_potential_value else 0.0,
            "top_10_delegate_share": self.top_10_delegate_share(),
            "sustained_active_user_share": sum(c.consecutive_active_ticks >= 12 for c in self.citizens) / total if total else 0.0,
            "mean_awareness_to_registration_delay_ticks": self.mean_awareness_to_registration_delay(),
            "trust_p10": quantile(sorted(c.trust_core for c in self.citizens), 0.10),
            "trust_p50": quantile(sorted(c.trust_core for c in self.citizens), 0.50),
            "trust_p90": quantile(sorted(c.trust_core for c in self.citizens), 0.90),
        }

    def active_user_share(self) -> float:
        return sum(c.is_active for c in self.citizens) / len(self.citizens)

    def average_delegate_reputation(self) -> float:
        return sum(d.reputation for d in self.delegates) / len(self.delegates) if self.delegates else 0.0

    def _delegate_weights(self) -> List[float]:
        weights = [c.delegated_weight for c in self.citizens if c.delegated_weight > 0]
        weights.extend(d.delegated_weight for d in self.delegates if d.delegated_weight > 0)
        return weights

    def active_delegate_count(self) -> int:
        return len(self._delegate_weights())

    def delegation_concentration_hhi(self) -> float:
        weights = self._delegate_weights()
        total = sum(weights)
        return sum((w / total) ** 2 for w in weights) if total else 0.0

    def top_delegate_share(self) -> float:
        weights = self._delegate_weights()
        total = sum(weights)
        return max(weights) / total if total else 0.0

    def top_10_delegate_share(self) -> float:
        weights = sorted(self._delegate_weights(), reverse=True)
        total = sum(weights)
        return sum(weights[:10]) / total if total else 0.0

    def mean_awareness_to_registration_delay(self) -> float:
        delays = [
            c.first_registration_tick - c.first_awareness_tick
            for c in self.citizens
            if c.first_registration_tick is not None and c.first_awareness_tick is not None
        ]
        return sum(delays) / len(delays) if delays else 0.0

    def trust_by_state(self) -> Dict[str, float]:
        groups: Dict[str, List[float]] = {}
        for c in self.citizens:
            groups.setdefault(c.use_state, []).append(c.trust_core)
        return {state: sum(vals) / len(vals) for state, vals in sorted(groups.items())}

    def micro_delegation_weight_share(self) -> float:
        micro = sum(c.delegated_weight for c in self.citizens)
        total = self.total_delegated_weight()
        return micro / total if total else 0.0

    def delegate_platform_use_rate(self) -> float:
        """Weight-weighted share of delegated weight held by an actively-using
        delegate. Institutional delegates are treated as active professionals."""
        micro_active = sum(c.delegated_weight for c in self.citizens if c.delegated_weight > 0 and c.is_active)
        institutional = sum(d.delegated_weight for d in self.delegates)
        total = self.total_delegated_weight()
        return (micro_active + institutional) / total if total else 0.0

    def executor_participation_rate(self) -> float:
        return sum(e.participating for e in self.executors) / len(self.executors) if self.executors else 0.0

    def honest_executor_share(self) -> float:
        participating = [e for e in self.executors if e.participating]
        return sum(e.honesty_type == "honest" for e in participating) / len(participating) if participating else 0.0

    def opportunistic_executor_share(self) -> float:
        participating = [e for e in self.executors if e.participating]
        return sum(e.honesty_type == "opportunistic" for e in participating) / len(participating) if participating else 0.0

    def fiscalizer_supply_per_project(self) -> float:
        return sum(f.participating for f in self.fiscalizers) / len(self.projects) if self.projects else 0.0

    def evidence_supply_per_project(self) -> float:
        return sum(e.participating for e in self.evidence_producers) / len(self.projects) if self.projects else 0.0

    def verification_coverage_rate(self) -> float:
        cfg = self.config
        required = len(self.projects) * cfg["verification_requirement_per_project"]
        if required <= 0:
            return 1.0
        capacity = sum(f.participating for f in self.fiscalizers) * cfg["fiscalizer_capacity"]
        return clamp(capacity / required)

    def evidence_coverage_rate(self) -> float:
        cfg = self.config
        required = len(self.projects) * cfg["evidence_requirement_per_project"]
        if required <= 0:
            return 1.0
        capacity = sum(e.participating for e in self.evidence_producers) * cfg["evidence_producer_capacity"]
        return clamp(capacity / required)

    def negative_word_of_mouth_rate(self) -> float:
        registered = [c for c in self.citizens if c.registered]
        return sum(c.use_state == "abandoned" for c in registered) / len(registered) if registered else 0.0

    def recommendation_rate(self) -> float:
        active = [c for c in self.citizens if c.is_active]
        return sum(c.trust_core >= 0.62 for c in active) / len(active) if active else 0.0


def write_csv(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    rows = list(rows)
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")


def run_scenario(config: Dict[str, Any], output_dir: str | Path) -> BehavioralAdoptionModel:
    model = BehavioralAdoptionModel(config)
    model.run(int(model.config["ticks"]))
    out = Path(output_dir)
    write_csv(out / "timeseries.csv", model.history)
    total_abandonments = sum(model.abandonment_reasons.values())
    write_json(
        out / "final_metrics.json",
        {
            **model.final_metrics(),
            "viability": model.viability_flags(),
            "trust_by_state": model.trust_by_state(),
            "abandonment_reason_distribution": {
                reason: count / total_abandonments for reason, count in sorted(model.abandonment_reasons.items())
            } if total_abandonments else {},
            "planning_mode": model.config["planning_mode"],
        },
    )
    write_json(out / "integration_outputs.json", model.integration_outputs())
    return model
