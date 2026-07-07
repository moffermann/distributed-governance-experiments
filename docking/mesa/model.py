#!/usr/bin/env python3
"""Mesa-native docking replication of the adversarial ABM.

This is an INDEPENDENT reimplementation (different language, different paradigm,
different RNG) of the static architecture-comparison engine in
``adversarial-abm/src/index.mjs``. It is a MODEL DOCKING in the sense of
Axtell, Axelrod, Epstein & Cohen (1996): we do not reproduce the JavaScript
random stream, we reproduce the *distributions* the JS engine samples from and
the *mechanisms* it applies, then check that the aggregate metrics land in the
same place (distributional equivalence).

RNG policy (per the docking brief):
  - Python ``random.Random`` is used everywhere (never a mulberry32 clone).
  - The *world* is generated once per run seed (seeds 1..20) and shared across
    all architectures -- this mirrors the JS "common-world paired comparison"
    (``generateWorld`` once per run, then ``cloneWorld`` per architecture).
  - Each architecture then runs with its own derived ``random.Random`` so the
    five architectures are statistically independent given the shared world,
    exactly as the JS derives ``mulberry32(runSeed ^ ((archIndex+1)*...))``.

Distribution shapes mirror the JS ``sampleDist``: ``beta`` -> Beta(alpha,beta),
``uniform`` -> U(min,max). Python's ``random.betavariate`` / ``random.uniform``
draw from the identical marginal families, which is all distributional docking
requires. Gaussian noise mirrors JS ``normal`` (Box-Muller) with ``random.gauss``.

Section references in comments (e.g. "JS: executeProject") point at the
mirrored block of ``adversarial-abm/src/index.mjs``.
"""

from __future__ import annotations

import math
import random
from typing import Optional

import mesa


# --------------------------------------------------------------------------
# Small numeric primitives (JS: clamp / sigmoid / normal / sampleDist / ...)
# --------------------------------------------------------------------------

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def js_round(x: float) -> int:
    """Match JavaScript Math.round (round half UP toward +inf).

    Python's built-in round() uses banker's rounding; for the population splits
    here the products are effectively integral, but we match JS semantics
    exactly to be safe.
    """
    return int(math.floor(x + 0.5))


def sample_dist(rng: random.Random, spec: dict) -> float:
    """JS: sampleDist. Beta(alpha,beta) or U(min,max)."""
    dist = spec.get("dist")
    if dist == "beta":
        return rng.betavariate(spec["alpha"], spec["beta"])
    if dist == "uniform":
        return spec["min"] + rng.random() * (spec["max"] - spec["min"])
    raise ValueError(f"Unsupported distribution: {dist}")


def normal(rng: random.Random, mu: float = 0.0, sigma: float = 1.0) -> float:
    """JS: normal (Box-Muller). Distributionally == random.gauss."""
    return rng.gauss(mu, sigma)


def weighted_pick(rng: random.Random, items: list, weight_fn):
    """JS: weightedPick. Roulette selection; uniform fallback if all weights 0."""
    weights = [max(0.0, weight_fn(it)) for it in items]
    total = sum(weights)
    if total <= 0:
        return items[int(rng.random() * len(items))]
    roll = rng.random() * total
    for i, it in enumerate(items):
        roll -= weights[i]
        if roll <= 0:
            return it
    return items[-1]


def draw_sample(rng: random.Random, projects: list, k: int) -> list:
    """JS: drawSample (sample without replacement). random.sample is the
    distributional equivalent of the JS partial Fisher-Yates."""
    n = min(k, len(projects))
    return rng.sample(projects, n)


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _sd(xs):
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def pearson(xs, ys) -> float:
    """JS: pearson."""
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0
    mx, my = _mean(xs), _mean(ys)
    sxy = sxx = syy = 0.0
    for x, y in zip(xs, ys):
        dx, dy = x - mx, y - my
        sxy += dx * dy
        sxx += dx * dx
        syy += dy * dy
    den = math.sqrt(sxx * syy)
    return 0.0 if den == 0 else sxy / den


def gini(values) -> float:
    """JS: gini."""
    v = sorted(values)
    n = len(v)
    total = sum(v)
    if not n or total == 0:
        return 0.0
    cum = 0.0
    lorenz = 0.0
    for x in v:
        cum += x
        lorenz += cum
    return 1.0 + 1.0 / n - (2.0 * lorenz) / (n * total)


# --------------------------------------------------------------------------
# Architecture parameter blocks (JS: coreBase + ARCHITECTURES)
# --------------------------------------------------------------------------

_CORE_BASE = {
    "centralPlanner": False,
    "citizenAllocation": True,
    "fundingCaps": True,
    "informationNoise": 0.18,
    "detectionBase": 0.55,
    "reviewConfidence": 0.85,
    "retention": 0.25,
    "guarantee": 0.15,
    "reputationLoss": 0.20,
    "futureSelectionLoss": 0.15,
    "socialProofDamping": 0.60,
    "passiveAllocationMode": "planning",
}

ARCHITECTURES = {
    "status_quo": {
        "id": "status_quo",
        "label": "Status quo / central low-information planning / audit-after-fact",
        "centralPlanner": True,
        "planningSource": "central",
        "citizenAllocation": False,
        "fundingCaps": True,
        "informationNoise": 0.45,
        "detectionBase": 0.15,
        "reviewConfidence": 0.35,
        "retention": 0.05,
        "guarantee": 0.02,
        "reputationLoss": 0.02,
        "futureSelectionLoss": 0.02,
        "socialProofDamping": 1.00,
        "passiveAllocationMode": "none",
    },
    "participatory_weak_verification": {
        "id": "participatory_weak_verification",
        "label": "Participatory / weak verification / low absorption",
        "centralPlanner": False,
        "planningSource": "none",
        "citizenAllocation": True,
        "fundingCaps": False,
        "informationNoise": 0.35,
        "detectionBase": 0.20,
        "reviewConfidence": 0.40,
        "retention": 0.05,
        "guarantee": 0.00,
        "reputationLoss": 0.03,
        "futureSelectionLoss": 0.03,
        "socialProofDamping": 1.00,
        "passiveAllocationMode": "none",
    },
    "participatory_weak_verification_full_budget": {
        "id": "participatory_weak_verification_full_budget",
        "label": "Participatory / weak verification / full budget via salience",
        "centralPlanner": False,
        "planningSource": "none",
        "citizenAllocation": True,
        "fundingCaps": False,
        "informationNoise": 0.35,
        "detectionBase": 0.20,
        "reviewConfidence": 0.40,
        "retention": 0.05,
        "guarantee": 0.00,
        "reputationLoss": 0.03,
        "futureSelectionLoss": 0.03,
        "socialProofDamping": 1.00,
        "passiveAllocationMode": "salience",
    },
    "core_v0_tutored_mandated_agenda": {
        "id": "core_v0_tutored_mandated_agenda",
        "label": "Core v0 - tutored regime, mandated agenda (transition scaffold: incumbent default vector)",
        **_CORE_BASE,
        "planningSource": "central",
    },
    "core_v0_tutored_distributed_agenda": {
        "id": "core_v0_tutored_distributed_agenda",
        "label": "Core v0 - tutored regime, distributed agenda",
        **_CORE_BASE,
        "planningSource": "distributed",
    },
}


def resolve_architectures(scenario: dict) -> list:
    """JS: resolveArchitectures (with architectureOverrides support)."""
    out = []
    overrides = scenario.get("architectureOverrides", {}) or {}
    for arch_id in scenario["architectures"]:
        arch = ARCHITECTURES.get(arch_id)
        if arch is None:
            raise ValueError(f"Unknown architecture in scenario: {arch_id}")
        ov = overrides.get(arch_id)
        out.append({**arch, **ov} if ov else dict(arch))
    return out


# --------------------------------------------------------------------------
# World generation (JS: makeProject / generateWorld)
# --------------------------------------------------------------------------

def make_project(rng: random.Random, pid: str, scenario: dict) -> dict:
    """JS: makeProject. Draw order follows the JS source (irrelevant to the
    marginals but kept for readability)."""
    p_cfg = scenario["projects"]
    latent_value = sample_dist(rng, p_cfg["latentValue"])

    salience = clamp(
        p_cfg["salienceCorrelation"] * latent_value
        + (1 - p_cfg["salienceCorrelation"]) * rng.random(),
        0.01, 0.99,
    )

    central_mix = p_cfg.get("centralPlanningSignalMix",
                            p_cfg.get("planningWeightCorrelation", 0.15))
    distributed_mix = p_cfg.get("distributedPlanningSignalMix", 0.70)
    central_planning_weight = clamp(
        central_mix * latent_value + (1 - central_mix) * rng.random(), 0.01, 0.99)
    distributed_planning_weight = clamp(
        distributed_mix * latent_value + (1 - distributed_mix) * rng.random(), 0.01, 0.99)

    verification_difficulty = sample_dist(rng, p_cfg["verificationDifficulty"])
    execution_difficulty = sample_dist(rng, p_cfg["executionDifficulty"])
    fraud_opportunity = sample_dist(rng, p_cfg["fraudOpportunity"])

    target_base = (p_cfg["scarcity"] * scenario["population"]["citizens"]
                   * scenario["cycles"]) / p_cfg["activePool"]
    budget_target = (0.5 + rng.random()) * target_base
    opportunistic = rng.random() < scenario["executors"]["opportunisticShare"]

    return {
        "id": pid,
        "latentValue": latent_value,
        "salience": salience,
        "centralPlanningWeight": central_planning_weight,
        "distributedPlanningWeight": distributed_planning_weight,
        "verificationDifficulty": verification_difficulty,
        "executionDifficulty": execution_difficulty,
        "fraudOpportunity": fraud_opportunity,
        "budgetTarget": budget_target,
        "executorType": "opportunistic" if opportunistic else "honest",
        "executorAbility": sample_dist(rng, scenario["executors"]["ability"]),
    }


def generate_world(seed: int, scenario: dict) -> dict:
    """JS: generateWorld. Attacks in the docked scenario are all disabled, so
    capturedSet / biasSet are None (they only consume RNG when enabled)."""
    rng = random.Random(seed)
    projects = [make_project(rng, f"P-{i + 1:03d}", scenario)
                for i in range(scenario["projects"]["activePool"])]
    return {"seed": seed, "projects": projects}


# --------------------------------------------------------------------------
# Mesa entities
# --------------------------------------------------------------------------

class ProjectAgent(mesa.Agent):
    """A single public project. The JS engine keeps projects as plain records;
    here each is a Mesa Agent so the model's AgentSet holds the population and
    the cycle logic reads/writes agent state idiomatically."""

    def __init__(self, model: "GovernanceModel", tpl: dict):
        super().__init__(model)
        # Static, world-level attributes (shared across architectures).
        self.latentValue = tpl["latentValue"]
        self.salience = tpl["salience"]
        self.centralPlanningWeight = tpl["centralPlanningWeight"]
        self.distributedPlanningWeight = tpl["distributedPlanningWeight"]
        self.verificationDifficulty = tpl["verificationDifficulty"]
        self.executionDifficulty = tpl["executionDifficulty"]
        self.fraudOpportunity = tpl["fraudOpportunity"]
        self.budgetTarget = tpl["budgetTarget"]
        self.executorType = tpl["executorType"]
        self.executorAbility = tpl["executorAbility"]
        self.pid = tpl["id"]
        # Dynamic per-architecture state (JS: cloneWorld reset).
        self.funded = 0.0
        self.closed = False
        self.execution: Optional[dict] = None

    def funding_progress(self) -> float:
        return max(0.0, self.funded / max(1.0, self.budgetTarget))


class GovernanceModel(mesa.Model):
    """One architecture playing out over ``scenario.cycles`` on a shared world.

    Mirrors JS ``runArchitecture``: a stepping loop over cycles, each cycle
    allocating a budget of ``citizens`` units through either central planning
    (status_quo) or the multi-channel citizen allocation, then closing and
    executing every project that has reached its budget target.
    """

    def __init__(self, world: dict, arch: dict, scenario: dict, seed: int):
        super().__init__()
        # Fully control the RNG: a private random.Random per (run, architecture).
        # (`scenario` is a reserved Model property in Mesa 3.5, so the scenario
        # dict is stored as ``self.scn``.)
        self.random = random.Random(seed)
        self.arch = arch
        self.scn = scenario
        self.projects = [ProjectAgent(self, tpl) for tpl in world["projects"]]
        self.attacks = scenario.get("attacks", {})

    # -- helpers -----------------------------------------------------------

    def open_projects(self) -> list:
        return [p for p in self.projects if not p.closed]

    def planning_score(self, p: ProjectAgent) -> float:
        """JS: planningScore (agendaCapture disabled -> plain base weight)."""
        if self.arch["planningSource"] == "distributed":
            return p.distributedPlanningWeight
        return p.centralPlanningWeight

    def visibility_score(self, p: ProjectAgent) -> float:
        """JS: visibilityScore."""
        attack = self.attacks.get("salienceCascade", {}) or {}
        social_proof = attack.get("socialProofWeight", 1.0) if attack.get("enabled") else 1.0
        return p.salience * (1.0 + social_proof * self.arch["socialProofDamping"] * p.funding_progress())

    def contribute(self, p: ProjectAgent, amount: float) -> float:
        """JS: contribute. Returns the unabsorbed remainder."""
        if amount <= 0 or p.closed:
            return amount
        if not self.arch["fundingCaps"]:
            p.funded += amount
            return 0.0
        room = max(0.0, p.budgetTarget - p.funded)
        paid = min(room, amount)
        p.funded += paid
        return amount - paid

    # -- allocation channels ----------------------------------------------

    def allocate_central(self):
        """JS: allocateCentral. Central planner spends citizens/cycle down the
        planning-score ranking; stops when it can make no further progress."""
        budget = self.scn["population"]["citizens"]
        projects = sorted(self.open_projects(), key=self.planning_score, reverse=True)
        for p in projects:
            if budget <= 0:
                break
            before = budget
            budget = self.contribute(p, budget)
            if before == budget:  # no room here; central has no default mop-up
                break

    def allocate_informed(self, count: int, noise_scale: float = 1.0,
                          near_completion_bonus: float = 0.0, units_per_actor: int = 1) -> float:
        """JS: allocateInformed. Each actor perceives a sample of projects ONCE
        with noise, ranks, and pours its units down that private ranking."""
        rng = self.random
        arch = self.arch
        sample_size = self.scn["population"].get("attentiveSampleSize", 8)
        info_noise = arch["informationNoise"] * noise_scale
        leftover = 0.0
        for i in range(count):
            projects = self.open_projects()
            if not projects:
                return leftover + (count - i) * units_per_actor
            sample = draw_sample(rng, projects, sample_size)
            scored = sorted(
                sample,
                key=lambda p: (p.latentValue + normal(rng, 0.0, info_noise)
                               + near_completion_bonus * p.funding_progress()
                               - 0.15 * p.verificationDifficulty),
                reverse=True,
            )
            amount = units_per_actor
            for p in scored:
                amount = self.contribute(p, amount)
                if amount <= 0:
                    break
            leftover += amount
        return leftover

    def allocate_attentive(self, count: int) -> float:
        return self.allocate_informed(count)

    def allocate_profile(self, count: int) -> float:
        """JS: allocateProfile (noisier value proxy + near-completion pull)."""
        return self.allocate_informed(count, noise_scale=1.5, near_completion_bonus=0.20)

    def allocate_delegated(self, count: int) -> float:
        """JS: allocateDelegated (informed allocation in delegate blocks)."""
        block_size = max(1, js_round(self.scn["population"].get("delegationBlockSize", 3)))
        blocks = count // block_size
        remainder = count - blocks * block_size
        leftover = self.allocate_informed(blocks, units_per_actor=block_size)
        if remainder > 0:
            leftover += self.allocate_informed(1, units_per_actor=remainder)
        return leftover

    def allocate_salience(self, count: int) -> float:
        """JS: allocateSalience. Visibility-ranked top slots, roulette-picked."""
        rng = self.random
        slots = (self.attacks.get("salienceCascade", {}) or {}).get("visibleSlots", 6)
        leftover = 0.0
        for i in range(count):
            amount = 1.0
            projects = self.open_projects()
            if not projects:
                return leftover + (count - i)
            top = sorted(projects, key=self.visibility_score, reverse=True)[:slots]
            for _ in range(min(4, len(top))):
                if amount <= 0:
                    break
                picked = weighted_pick(rng, top, self.visibility_score)
                amount = self.contribute(picked, amount)
            leftover += amount
        return leftover

    def allocate_default(self, count: float):
        """JS: allocateDefault. Deterministic public-default fill down the
        planning ranking (no RNG)."""
        if count <= 0:
            return
        budget = count
        projects = sorted(self.open_projects(), key=self.planning_score, reverse=True)
        for p in projects:
            if budget <= 0:
                break
            room = max(0.0, p.budgetTarget - p.funded) if self.arch["fundingCaps"] else math.inf
            paid = min(budget, room)
            p.funded += paid
            budget -= paid

    def allocate_citizen(self):
        """JS: allocateCitizen. The five-way population split, folding profile /
        delegated into the passive block where there is no default layer, then
        the passiveAllocationMode disposition of the remainder."""
        pop = self.scn["population"]
        arch = self.arch
        N = pop["citizens"]
        attentive = js_round(N * pop["attentiveShare"])
        salience = js_round(N * pop["salienceShare"])

        has_default_layer = arch["passiveAllocationMode"] == "planning"
        profile = js_round(N * pop.get("profileShare", 0)) if has_default_layer else 0
        delegated = js_round(N * pop.get("delegatorShare", 0)) if has_default_layer else 0
        remaining = N - attentive - salience - profile - delegated

        # coordinatedSignalBias attack is disabled in the docked scenario, so
        # all attentive citizens allocate honestly (no biasSet branch / no draws).
        leftover = 0.0
        leftover += self.allocate_attentive(attentive)
        leftover += self.allocate_salience(salience)
        if profile > 0:
            leftover += self.allocate_profile(profile)
        if delegated > 0:
            leftover += self.allocate_delegated(delegated)

        mode = arch["passiveAllocationMode"]
        if mode == "planning":
            self.allocate_default(remaining + leftover)
        elif mode == "salience":
            self.allocate_salience(remaining)
        # mode == "none": remaining + leftover stay unallocated (the low-absorption
        # failure the weak participatory variant exists to demonstrate).

    # -- execution ---------------------------------------------------------

    def detection_probability(self, p: ProjectAgent) -> float:
        """JS: detectionProbability."""
        weak = self.attacks.get("weakVerificationDiversion", {}) or {}
        shock = weak.get("detectionShock", 1.0) if weak.get("enabled") else 1.0
        prob = self.arch["detectionBase"] * shock * (1 - 0.55 * p.verificationDifficulty)
        return clamp(prob, 0.01, 0.98)

    def execute_project(self, p: ProjectAgent, cycle: int):
        """JS: executeProject. fiscalizerCollusion is disabled in the docked
        scenario, so collusionRate == 0 (no collusion RNG draws)."""
        rng = self.random
        arch = self.arch
        funded_budget = p.funded
        target_budget = p.budgetTarget
        potential_value = target_budget * p.latentValue
        detection = self.detection_probability(p)
        eff_detection = detection  # collusionRate == 0

        diverted = False
        diversion_share = 0.0
        execution_quality = 1.0

        if p.executorType == "opportunistic":
            fraud_gain = p.fraudOpportunity * (1 - arch["retention"])
            x = (-1.0 + 4.0 * fraud_gain + 2.0 * p.verificationDifficulty
                 - 5.0 * eff_detection - 3.0 * arch["retention"] - 2.0 * arch["guarantee"]
                 - 3.0 * arch["reputationLoss"] - 2.0 * arch["futureSelectionLoss"])
            diverted = rng.random() < sigmoid(x)
            if diverted:
                diversion_share = clamp(0.20 + 0.60 * p.fraudOpportunity + normal(rng, 0.0, 0.05), 0.05, 0.95)
                execution_quality = clamp((1 - diversion_share) * (0.55 + 0.45 * p.executorAbility), 0.02, 1)
            else:
                execution_quality = clamp(0.70 + 0.30 * p.executorAbility - 0.20 * p.executionDifficulty, 0.20, 1)
        else:
            p_good_delivery = sigmoid(1.5 + 2.5 * p.executorAbility - 3.0 * p.executionDifficulty)
            good = rng.random() < p_good_delivery
            execution_quality = (clamp(0.75 + 0.25 * p.executorAbility, 0.30, 1) if good
                                 else clamp(0.35 + 0.35 * p.executorAbility - 0.20 * p.executionDifficulty, 0.05, 0.85))

        # collusionRate == 0 short-circuits before any RNG draw (JS parity).
        colluded = False
        detected = (rng.random() < detection) if diverted and not colluded else False
        reported_completion = 1.0 if (diverted and not detected) else execution_quality
        review_confidence = 1.0 if detected else clamp(
            arch["reviewConfidence"] * (1 - 0.35 * p.verificationDifficulty), 0.05, 1)
        actual_value = potential_value * execution_quality
        verified_value = actual_value * review_confidence
        reported_value = potential_value * reported_completion
        leakage = funded_budget * diversion_share if diverted else 0.0

        p.closed = True
        p.execution = {
            "fundedBudget": funded_budget,
            "actualValue": actual_value,
            "verifiedValue": verified_value,
            "reportedValue": reported_value,
            "executionQuality": execution_quality,
            "diverted": diverted,
            "diversionShare": diversion_share,
            "leakage": leakage,
            "detected": detected,
        }

    def close_and_execute(self, cycle: int):
        """JS: closeAndExecuteFunded."""
        for p in self.projects:
            if not p.closed and p.funded >= p.budgetTarget:
                self.execute_project(p, cycle)

    # -- driver ------------------------------------------------------------

    def step(self):
        """One cycle (JS: the body of runArchitecture's loop)."""
        if not self.open_projects():
            return
        if self.arch["centralPlanner"]:
            self.allocate_central()
        else:
            self.allocate_citizen()
        self.close_and_execute(self._cycle)

    def run(self) -> dict:
        """JS: runArchitecture -> computeMetrics."""
        for cycle in range(self.scn["cycles"]):
            if not self.open_projects():
                break
            self._cycle = cycle
            self.step()
        return self.compute_metrics()

    # -- metrics -----------------------------------------------------------

    def compute_metrics(self) -> dict:
        """JS: computeMetrics. verifiedValuePerBudget = sum(verifiedValue) over
        executed projects / total funded (budgetSpent, floored to 1)."""
        projects = self.projects
        executed = [p for p in projects if p.execution]
        funded_flag = [1 if p.execution else 0 for p in projects]
        values = [p.latentValue for p in projects]
        funded_amounts = [p.funded for p in projects]
        budget_spent = sum(funded_amounts)
        total_available = self.scn["population"]["citizens"] * self.scn["cycles"]
        safe_budget = budget_spent or 1.0

        actual_value = sum(p.execution["actualValue"] for p in executed)
        verified_value = sum(p.execution["verifiedValue"] for p in executed)
        reported_value = sum(p.execution["reportedValue"] for p in executed)
        leakage = sum(p.execution["leakage"] for p in executed)
        diversions = sum(1 for p in executed if p.execution["diverted"])
        detected_div = sum(1 for p in executed if p.execution["diverted"] and p.execution["detected"])

        return {
            "architecture": self.arch["id"],
            "budgetSpent": budget_spent,
            "budgetUtilizationRate": budget_spent / total_available,
            "unspentBudgetRate": max(0.0, total_available - budget_spent) / total_available,
            "executedProjects": len(executed),
            "fundedRate": len(executed) / len(projects),
            "actualValuePerBudget": actual_value / safe_budget,
            "verifiedValuePerBudget": verified_value / safe_budget,
            "reportedValuePerBudget": reported_value / safe_budget,
            "visibilityGapPerBudget": (reported_value - actual_value) / safe_budget,
            "leakageRate": leakage / safe_budget,
            "diversionRateAmongExecuted": (diversions / len(executed)) if executed else 0.0,
            "detectionRateAmongDiversions": (detected_div / diversions) if diversions else 0.0,
            "fundingGini": gini(funded_amounts),
            "selectionValueCorrelation": pearson(funded_flag, values),
        }
