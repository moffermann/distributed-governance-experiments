"""Core v0 behavioral adoption agent-based model.

This first executable version is intentionally dependency-light. If Mesa is
installed, agents and the model inherit from Mesa's Agent/Model classes. If Mesa
is not installed, a tiny fallback shim keeps the experiment runnable with only
Python's standard library.
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

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
        def __init__(self, rng=None):
            self.random = rng if isinstance(rng, random.Random) else random.Random(rng)

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
    "visible_success_rate": 0.030,
    "bad_outcome_rate": 0.018,
    "platform_outage_rate": 0.005,
    "public_controversy_rate": 0.007,
    "trust_recovery_strength": 0.020,
    "delegate_count": 24,
    "project_count": 80,
    "executor_count": 60,
    "fiscalizer_count": 35,
    "evidence_producer_count": 45,
    "executor_incentive_strength": 0.50,
    "fiscalizer_compensation": 0.45,
    "evidence_compensation": 0.42,
    "review_cost": 0.35,
    "evidence_cost": 0.35,
    "verification_requirement_per_project": 0.60,
    "evidence_requirement_per_project": 0.70,
    "social_graph_degree": 8,
    "random_social_tie_probability": 0.015,
    "participation_temperature": 0.75,
    "delegate_temperature": 0.50,
    "abandonment_threshold": 0.30,
    "reactivation_campaign_strength": 0.015,
}

INTEGRATION_KEYS = [
    "active_user_share",
    "registered_user_share",
    "registered_inactive_share",
    "aware_non_user_share",
    "passive_delegated_share",
    "profile_driven_share",
    "direct_participation_share",
    "full_delegation_share",
    "partial_delegation_share",
    "delegation_concentration_hhi",
    "top_delegate_share",
    "abandonment_share",
    "mean_platform_trust",
    "executor_participation_rate",
    "honest_executor_share",
    "opportunistic_executor_share",
    "fiscalizer_supply_per_project",
    "evidence_supply_per_project",
    "verification_market_depth",
    "thin_market_failure_rate",
    "negative_word_of_mouth_rate",
    "recommendation_rate",
]


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


def load_config(path: str | Path | None = None, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    if path:
        with Path(path).open("r", encoding="utf-8") as fh:
            config = _deep_update(config, json.load(fh))
    if overrides:
        config = _deep_update(config, overrides)
    return config


class CitizenAgent(mesa.Agent):  # type: ignore[misc]
    """Potential or actual Core user."""

    def __init__(self, model: "BehavioralAdoptionModel", citizen_id: int):
        super().__init__(model)
        rng = self.random
        cfg = model.config
        self.citizen_id = citizen_id
        self.aware = bernoulli(rng, cfg["initial_awareness"])
        self.registered = False
        self.use_state = "aware_non_user" if self.aware else "unaware"
        self.delegate_id: Optional[int] = None
        self.first_awareness_tick: Optional[int] = 0 if self.aware else None
        self.first_registration_tick: Optional[int] = None
        self.last_activation_tick: Optional[int] = None
        self.last_abandonment_tick: Optional[int] = None

        self.trust_core = clamp(rng.gauss(cfg["initial_trust_mean"], cfg["initial_trust_spread"]))
        self.trust_evidence = clamp(rng.gauss(0.48, 0.18))
        self.trust_fiscalization = clamp(rng.gauss(0.46, 0.18))
        self.digital_confidence = clamp(rng.betavariate(2.2, 2.0))
        self.civic_interest = clamp(rng.betavariate(1.7, 2.3))
        self.privacy_concern = clamp(rng.betavariate(2.2, 2.1))
        self.friction_tolerance = clamp(rng.betavariate(2.0, 2.2))
        self.social_influence_weight = clamp(rng.betavariate(2.0, 2.0))
        self.attention_budget = clamp(rng.betavariate(1.6, 2.6))
        self.need_relevance = clamp(rng.betavariate(2.0, 2.5))
        self.ideological_openness = clamp(rng.betavariate(2.0, 1.8))
        self.control_preference = clamp(rng.betavariate(2.0, 2.0))
        self.automation_trust = clamp(rng.betavariate(1.8, 2.2))

    @property
    def is_active(self) -> bool:
        return self.use_state in {"direct_active", "profile_driven", "delegated", "hybrid"}

    @property
    def is_delegating(self) -> bool:
        return self.use_state in {"delegated", "hybrid"} and self.delegate_id is not None

    def social_signal(self) -> Dict[str, float]:
        neighbors = self.model.social_graph.get(self.citizen_id, [])
        if not neighbors:
            return {"active": 0.0, "registered": 0.0, "abandoned": 0.0}
        agents = [self.model.citizens[n] for n in neighbors]
        return {
            "active": sum(a.is_active for a in agents) / len(agents),
            "registered": sum(a.registered for a in agents) / len(agents),
            "abandoned": sum(a.use_state == "abandoned" for a in agents) / len(agents),
        }

    def awareness_step(self) -> None:
        if self.aware:
            return
        cfg = self.model.config
        s = self.social_signal()
        p = (
            cfg["campaign_intensity"]
            + cfg["social_influence_strength"] * self.social_influence_weight * s["registered"]
            + 0.01 * self.civic_interest
            + 0.01 * self.need_relevance
        )
        if bernoulli(self.random, p):
            self.aware = True
            self.use_state = "aware_non_user"
            self.first_awareness_tick = self.model.tick

    def registration_step(self) -> None:
        if not self.aware or self.registered or self.use_state == "abandoned":
            return
        cfg = self.model.config
        s = self.social_signal()
        x = (
            -1.55
            + 1.35 * cfg["perceived_benefit"]
            + 1.10 * s["active"] * self.social_influence_weight
            + 1.25 * self.trust_core
            + 0.85 * self.need_relevance
            + 0.55 * cfg["ai_tutor_quality"]
            + 0.45 * cfg["public_legitimacy"]
            - 1.10 * cfg["onboarding_friction"] * (1.0 - self.friction_tolerance)
            - 0.90 * self.privacy_concern * (1.0 - cfg["privacy_guarantee_strength"])
            - 0.75 * (1.0 - self.ideological_openness)
            - cfg["negative_word_of_mouth_strength"] * s["abandoned"]
        )
        if bernoulli(self.random, sigmoid(x)):
            self.registered = True
            self.use_state = "registered_inactive"
            self.first_registration_tick = self.model.tick

    def activation_step(self) -> None:
        if not self.registered or self.use_state == "abandoned":
            return
        cfg = self.model.config
        if self.use_state == "registered_inactive":
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

    def set_participation_mode(self) -> None:
        cfg = self.model.config
        s = self.social_signal()
        delegate_quality = self.model.average_delegate_reputation()
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
        if self.delegate_id is not None and new_state not in {"delegated", "hybrid"}:
            self.model.delegates[self.delegate_id].delegated_weight = max(0.0, self.model.delegates[self.delegate_id].delegated_weight - 1.0)
            self.delegate_id = None
        self.use_state = new_state
        if self.use_state in {"delegated", "hybrid"}:
            self.choose_delegate()

    def choose_delegate(self) -> None:
        if not self.model.delegates:
            self.use_state = "registered_inactive"
            return
        cfg = self.model.config
        concentration = self.model.delegation_concentration_hhi()
        scores: Dict[str, float] = {}
        for d in self.model.delegates:
            alignment = 1.0 - abs(self.civic_interest - d.alignment_vector)
            scores[str(d.delegate_id)] = 0.95 * alignment + 1.15 * d.reputation + 0.50 * d.visibility - 0.70 * d.conflict_risk - 0.45 * concentration
        chosen_id = int(softmax_choice(self.random, scores, cfg["delegate_temperature"]))
        if self.delegate_id == chosen_id:
            return
        if self.delegate_id is not None:
            self.model.delegates[self.delegate_id].delegated_weight = max(0.0, self.model.delegates[self.delegate_id].delegated_weight - 1.0)
        self.delegate_id = chosen_id
        self.model.delegates[chosen_id].delegated_weight += 1.0

    def trust_step(self) -> None:
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
            delta += self.random.gauss(0.003, 0.010)
        self.trust_core = clamp(self.trust_core + delta)

    def churn_step(self) -> None:
        cfg = self.model.config
        if self.registered and self.use_state != "abandoned":
            s = self.social_signal()
            x = (
                -2.10
                + 1.20 * self.model.visible_failure_stock
                + 1.00 * self.model.current_controversy
                + 0.85 * self.model.current_outage
                + 0.75 * cfg["interface_complexity"]
                + 0.55 * (1.0 - self.trust_core)
                + 0.40 * s["abandoned"]
                - 0.90 * self.trust_core
                - 0.45 * self.model.visible_success_stock
            )
            if self.trust_core < cfg["abandonment_threshold"] and bernoulli(self.random, sigmoid(x)):
                if self.delegate_id is not None:
                    self.model.delegates[self.delegate_id].delegated_weight = max(0.0, self.model.delegates[self.delegate_id].delegated_weight - 1.0)
                    self.delegate_id = None
                self.use_state = "abandoned"
                self.last_abandonment_tick = self.model.tick
            return
        if self.use_state == "abandoned":
            x = -3.00 + 1.20 * self.model.visible_success_stock + 0.80 * cfg["reactivation_campaign_strength"] + 0.65 * self.trust_core - 0.85 * self.model.visible_failure_stock
            if bernoulli(self.random, sigmoid(x)):
                self.use_state = "registered_inactive"
                self.trust_core = clamp(self.trust_core + 0.08)


class DelegateAgent(mesa.Agent):  # type: ignore[misc]
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
        self.funding_progress = 0.0
        self.outcome_state = "pending"

    def step(self) -> None:
        self.funding_progress = clamp(self.funding_progress + 0.02 * self.model.active_user_share() * self.salience)


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

    def step(self) -> None:
        cfg = self.model.config
        x = -0.60 + 1.15 * cfg["executor_incentive_strength"] + 0.65 * self.reputation_stake + 0.40 * self.ability - 0.75 * self.cost_structure - 0.35 * self.liquidity_constraint
        self.participating = bernoulli(self.random, sigmoid(x))


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

    def step(self) -> None:
        cfg = self.model.config
        x = -0.85 + 1.05 * cfg["fiscalizer_compensation"] + 0.70 * self.reputation_stake + 0.55 * self.competence + 0.45 * self.independence - 0.85 * cfg["review_cost"] - 0.40 * self.capture_risk
        self.participating = bernoulli(self.random, sigmoid(x))


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

    def step(self) -> None:
        cfg = self.model.config
        x = -0.80 + 1.05 * cfg["evidence_compensation"] + 0.55 * self.method_quality + 0.45 * self.independence + 0.35 * self.coverage - 0.85 * cfg["evidence_cost"] - 0.45 * self.capture_risk
        self.participating = bernoulli(self.random, sigmoid(x))


class BehavioralAdoptionModel(mesa.Model):  # type: ignore[misc]
    """Simulates adoption, delegation, trust, abandonment, and role-market supply."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.seed = int(config.get("seed", 42))
        rng = random.Random(self.seed)
        try:
            super().__init__(rng=rng)
        except TypeError:
            super().__init__()
            self.random = rng
        else:
            self.random = getattr(self, "random", rng)
        self.tick = 0
        self.current_outage = 0.0
        self.current_controversy = 0.0
        self.current_recovery_event = 0.0
        self.visible_success_stock = 0.0
        self.visible_failure_stock = 0.0
        self.history: List[Dict[str, float]] = []

        self.citizens = [CitizenAgent(self, i) for i in range(int(config["population_size"]))]
        self.delegates = [DelegateAgent(self, i) for i in range(int(config["delegate_count"]))]
        self.projects = [ProjectAgent(self, i) for i in range(int(config["project_count"]))]
        self.executors = [ExecutorAgent(self, i) for i in range(int(config["executor_count"]))]
        self.fiscalizers = [FiscalizerAgent(self, i) for i in range(int(config["fiscalizer_count"]))]
        self.evidence_producers = [EvidenceProducerAgent(self, i) for i in range(int(config["evidence_producer_count"]))]
        self.social_graph = self._build_social_graph()
        self.collect_metrics()

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

    def step(self) -> None:
        self.tick += 1
        self._platform_events()
        for c in self.citizens:
            c.awareness_step()
        for c in self.citizens:
            c.registration_step()
        for c in self.citizens:
            c.activation_step()
        for d in self.delegates:
            d.step()
        for p in self.projects:
            p.step()
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
        self.collect_metrics()

    def run(self, ticks: Optional[int] = None) -> None:
        for _ in range(int(ticks if ticks is not None else self.config["ticks"])):
            self.step()

    def _platform_events(self) -> None:
        cfg = self.config
        self.current_outage = 1.0 if bernoulli(self.random, cfg["platform_outage_rate"]) else 0.0
        self.current_controversy = 1.0 if bernoulli(self.random, cfg["public_controversy_rate"]) else 0.0
        self.current_recovery_event = 1.0 if bernoulli(self.random, cfg["trust_recovery_strength"]) else 0.0
        if bernoulli(self.random, cfg["visible_success_rate"]):
            self.visible_success_stock = clamp(self.visible_success_stock + 0.10)
        if bernoulli(self.random, cfg["bad_outcome_rate"]):
            self.visible_failure_stock = clamp(self.visible_failure_stock + 0.12)
        self.visible_success_stock = clamp(self.visible_success_stock * 0.985)
        self.visible_failure_stock = clamp(self.visible_failure_stock * 0.975)

    def _project_outcomes(self) -> None:
        fiscalizer_depth = self.fiscalizer_supply_per_project()
        evidence_depth = self.evidence_supply_per_project()
        executor_rate = self.executor_participation_rate()
        for project in self.projects:
            if project.funding_progress < 0.75 or project.outcome_state != "pending":
                continue
            p_success = clamp(0.25 + 0.35 * project.latent_value + 0.20 * executor_rate + 0.15 * min(fiscalizer_depth, 1.0) + 0.15 * min(evidence_depth, 1.0))
            if bernoulli(self.random, p_success):
                project.outcome_state = "successful"
                self.visible_success_stock = clamp(self.visible_success_stock + 0.05)
            else:
                project.outcome_state = "failed"
                self.visible_failure_stock = clamp(self.visible_failure_stock + 0.07)

    def collect_metrics(self) -> Dict[str, float]:
        metrics = self.metrics()
        self.history.append(metrics)
        return metrics

    def final_metrics(self) -> Dict[str, float]:
        return self.history[-1]

    def integration_outputs(self) -> Dict[str, float | str]:
        m = self.final_metrics()
        return {"scenario_id": self.config["scenario_id"], **{k: m.get(k, 0.0) for k in INTEGRATION_KEYS}}

    def metrics(self) -> Dict[str, float]:
        total = len(self.citizens)
        registered = [c for c in self.citizens if c.registered]
        active = [c for c in self.citizens if c.is_active]
        counts = Counter(c.use_state for c in self.citizens)
        reg_n = len(registered)
        aware_n = sum(c.aware for c in self.citizens)
        fs = self.fiscalizer_supply_per_project()
        es = self.evidence_supply_per_project()
        return {
            "tick": float(self.tick),
            "awareness_rate": aware_n / total if total else 0.0,
            "registered_user_share": reg_n / total if total else 0.0,
            "registration_rate_among_aware": reg_n / aware_n if aware_n else 0.0,
            "activation_rate_registered": len(active) / reg_n if reg_n else 0.0,
            "active_user_share": len(active) / total if total else 0.0,
            "registered_inactive_share": counts["registered_inactive"] / reg_n if reg_n else 0.0,
            "aware_non_user_share": counts["aware_non_user"] / total if total else 0.0,
            "direct_participation_share": counts["direct_active"] / reg_n if reg_n else 0.0,
            "profile_driven_share": counts["profile_driven"] / reg_n if reg_n else 0.0,
            "passive_delegated_share": counts["delegated"] / reg_n if reg_n else 0.0,
            "hybrid_participation_share": counts["hybrid"] / reg_n if reg_n else 0.0,
            "full_delegation_share": counts["delegated"] / reg_n if reg_n else 0.0,
            "partial_delegation_share": counts["hybrid"] / reg_n if reg_n else 0.0,
            "delegation_rate": sum(c.is_delegating for c in registered) / reg_n if reg_n else 0.0,
            "delegation_concentration_hhi": self.delegation_concentration_hhi(),
            "top_delegate_share": self.top_delegate_share(),
            "abandonment_share": counts["abandoned"] / reg_n if reg_n else 0.0,
            "mean_platform_trust": sum(c.trust_core for c in self.citizens) / total if total else 0.0,
            "executor_participation_rate": self.executor_participation_rate(),
            "honest_executor_share": self.honest_executor_share(),
            "opportunistic_executor_share": self.opportunistic_executor_share(),
            "fiscalizer_supply_per_project": fs,
            "evidence_supply_per_project": es,
            "verification_market_depth": min(fs, es),
            "thin_market_failure_rate": self.thin_market_failure_rate(),
            "negative_word_of_mouth_rate": self.negative_word_of_mouth_rate(),
            "recommendation_rate": self.recommendation_rate(),
            "visible_success_stock": self.visible_success_stock,
            "visible_failure_stock": self.visible_failure_stock,
        }

    def active_user_share(self) -> float:
        return sum(c.is_active for c in self.citizens) / len(self.citizens)

    def average_delegate_reputation(self) -> float:
        return sum(d.reputation for d in self.delegates) / len(self.delegates) if self.delegates else 0.0

    def delegation_concentration_hhi(self) -> float:
        total = sum(d.delegated_weight for d in self.delegates)
        return sum((d.delegated_weight / total) ** 2 for d in self.delegates) if total else 0.0

    def top_delegate_share(self) -> float:
        total = sum(d.delegated_weight for d in self.delegates)
        return max((d.delegated_weight for d in self.delegates), default=0.0) / total if total else 0.0

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

    def thin_market_failure_rate(self) -> float:
        return clamp((max(0.0, 1.0 - self.fiscalizer_supply_per_project()) + max(0.0, 1.0 - self.evidence_supply_per_project())) / 2.0)

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
    model.run(int(config["ticks"]))
    out = Path(output_dir)
    write_csv(out / "timeseries.csv", model.history)
    write_json(out / "final_metrics.json", model.final_metrics())
    write_json(out / "integration_outputs.json", model.integration_outputs())
    return model
