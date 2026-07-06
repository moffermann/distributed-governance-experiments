#!/usr/bin/env node
// Minimal adversarial ABM engine for public-resource allocation architecture stress testing.
//
// v0.3 goals:
// - dependency-free Node.js;
// - deterministic under seed;
// - common-world paired comparison;
// - explicit separation between central planning information and distributed planning information;
// - weak participatory variants plus Core v0 tutored-central and tutored-distributed variants;
// - result table for actual, verified, and reported value; leakage; visibility gap;
//   unspent budget; concentration; and effective planning-signal correlations.
//
// v0.4 (2026-07-06 engine audit — see ENGINE_AUDIT_2026_07_06.md):
// - attentive perception is computed once per sampled project, then ranked
//   (the previous comparator drew fresh noise on every comparison — a
//   non-transitive sort that distorted informationNoise semantics);
// - profileShare and delegatorShare are implemented as the distinct channels
//   AGENT_DECISION_MODEL.md specifies, active where the architecture provides
//   a default layer; previously both were silently folded into the passive block;
// - attentive samples are drawn without replacement;
// - unabsorbed active-citizen allocation follows the public default rule under
//   passiveAllocationMode "planning" (docs/101), instead of evaporating.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const parseArgs = () => {
  const args = process.argv.slice(2);
  const out = {};
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (!a.startsWith("--")) continue;
    const key = a.slice(2);
    const next = args[i + 1];
    if (!next || next.startsWith("--")) out[key] = true;
    else { out[key] = next; i++; }
  }
  return out;
};

const ENGINE_VERSION = "0.4.1"; // bump on any behavior-affecting engine change

const cli = parseArgs();
const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const scenarioPath = resolve(cli.scenario ?? resolve(HERE, "../scenarios/baseline-medium.json"));
const scenario = JSON.parse(readFileSync(scenarioPath, "utf8"));
if (cli.runs) scenario.runs = Number.parseInt(cli.runs, 10);
if (cli.seed) scenario.seed = Number.parseInt(cli.seed, 10);
if (cli.centralPlanningSignalMix) scenario.projects.centralPlanningSignalMix = Number.parseFloat(cli.centralPlanningSignalMix);
if (cli.distributedPlanningSignalMix) scenario.projects.distributedPlanningSignalMix = Number.parseFloat(cli.distributedPlanningSignalMix);

const clamp = (x, lo = 0, hi = 1) => Math.max(lo, Math.min(hi, x));
const sigmoid = (x) => 1 / (1 + Math.exp(-x));

const mulberry32 = (seed) => () => {
  seed |= 0;
  seed = (seed + 0x6d2b79f5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};

const normal = (rng, mu = 0, sigma = 1) => {
  let u1 = rng();
  if (u1 < 1e-12) u1 = 1e-12;
  const u2 = rng();
  return mu + sigma * Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
};

const gamma = (rng, shape, scale = 1) => {
  if (shape <= 0) throw new Error(`Gamma shape must be positive, got ${shape}`);
  if (shape < 1) return gamma(rng, shape + 1, scale) * Math.pow(rng(), 1 / shape);
  const d = shape - 1 / 3;
  const c = 1 / Math.sqrt(9 * d);
  while (true) {
    let x = normal(rng);
    let v = 1 + c * x;
    if (v <= 0) continue;
    v = v ** 3;
    const u = rng();
    if (u < 1 - 0.0331 * x ** 4) return scale * d * v;
    if (Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return scale * d * v;
  }
};

const beta = (rng, alpha, betaParam) => {
  const x = gamma(rng, alpha, 1);
  const y = gamma(rng, betaParam, 1);
  return x / (x + y);
};

const sampleDist = (rng, spec) => {
  if (!spec || typeof spec !== "object") throw new Error(`Invalid distribution spec: ${JSON.stringify(spec)}`);
  if (spec.dist === "beta") return beta(rng, spec.alpha, spec.beta);
  if (spec.dist === "uniform") return spec.min + rng() * (spec.max - spec.min);
  throw new Error(`Unsupported distribution: ${spec.dist}`);
};

const weightedPick = (rng, items, weightFn) => {
  let total = 0;
  const weights = items.map((item) => {
    const w = Math.max(0, weightFn(item));
    total += w;
    return w;
  });
  if (total <= 0) return items[Math.floor(rng() * items.length)];
  let roll = rng() * total;
  for (let i = 0; i < items.length; i++) {
    roll -= weights[i];
    if (roll <= 0) return items[i];
  }
  return items[items.length - 1];
};

const mean = (xs) => xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0;
const sd = (xs) => {
  if (xs.length < 2) return 0;
  const m = mean(xs);
  return Math.sqrt(xs.reduce((a, x) => a + (x - m) ** 2, 0) / (xs.length - 1));
};

const pearson = (xs, ys) => {
  if (xs.length !== ys.length || xs.length < 2) return 0;
  const mx = mean(xs);
  const my = mean(ys);
  let sxy = 0, sxx = 0, syy = 0;
  for (let i = 0; i < xs.length; i++) {
    const dx = xs[i] - mx;
    const dy = ys[i] - my;
    sxy += dx * dy;
    sxx += dx * dx;
    syy += dy * dy;
  }
  const den = Math.sqrt(sxx * syy);
  return den === 0 ? 0 : sxy / den;
};

const gini = (values) => {
  const v = [...values].sort((a, b) => a - b);
  const n = v.length;
  const total = v.reduce((a, b) => a + b, 0);
  if (!n || total === 0) return 0;
  let cum = 0;
  let lorenz = 0;
  for (let i = 0; i < n; i++) {
    cum += v[i];
    lorenz += cum;
  }
  return 1 + 1 / n - (2 * lorenz) / (n * total);
};

const summarize = (rows, key) => {
  const xs = rows.map((r) => r[key]);
  return { mean: mean(xs), sd: sd(xs) };
};
const fmt = (x, digits = 3) => Number.isFinite(x) ? x.toFixed(digits) : "NaN";
const fmtMean = (s) => `${fmt(s.mean)}±${fmt(s.sd)}`;

const coreBase = {
  centralPlanner: false,
  citizenAllocation: true,
  fundingCaps: true,
  informationNoise: 0.18,
  detectionBase: 0.55,
  reviewConfidence: 0.85,
  retention: 0.25,
  guarantee: 0.15,
  reputationLoss: 0.20,
  futureSelectionLoss: 0.15,
  socialProofDamping: 0.60,
  passiveAllocationMode: "planning",
};

const ARCHITECTURES = {
  status_quo: {
    id: "status_quo",
    label: "Status quo / central low-information planning / audit-after-fact",
    centralPlanner: true,
    planningSource: "central",
    citizenAllocation: false,
    fundingCaps: true,
    informationNoise: 0.45,
    detectionBase: 0.15,
    reviewConfidence: 0.35,
    retention: 0.05,
    guarantee: 0.02,
    reputationLoss: 0.02,
    futureSelectionLoss: 0.02,
    socialProofDamping: 1.00,
    passiveAllocationMode: "none",
  },
  participatory_weak_verification: {
    id: "participatory_weak_verification",
    label: "Participatory / weak verification / low absorption",
    centralPlanner: false,
    planningSource: "none",
    citizenAllocation: true,
    fundingCaps: false,
    informationNoise: 0.35,
    detectionBase: 0.20,
    reviewConfidence: 0.40,
    retention: 0.05,
    guarantee: 0.00,
    reputationLoss: 0.03,
    futureSelectionLoss: 0.03,
    socialProofDamping: 1.00,
    passiveAllocationMode: "none",
  },
  participatory_weak_verification_full_budget: {
    id: "participatory_weak_verification_full_budget",
    label: "Participatory / weak verification / full budget via salience",
    centralPlanner: false,
    planningSource: "none",
    citizenAllocation: true,
    fundingCaps: false,
    informationNoise: 0.35,
    detectionBase: 0.20,
    reviewConfidence: 0.40,
    retention: 0.05,
    guarantee: 0.00,
    reputationLoss: 0.03,
    futureSelectionLoss: 0.03,
    socialProofDamping: 1.00,
    passiveAllocationMode: "salience",
  },
  core_v0_tutored_central_planning: {
    id: "core_v0_tutored_central_planning",
    label: "Core v0 tutored / central planning default",
    ...coreBase,
    planningSource: "central",
  },
  core_v0_tutored_distributed_planning: {
    id: "core_v0_tutored_distributed_planning",
    label: "Core v0 tutored / distributed parallel planning default",
    ...coreBase,
    planningSource: "distributed",
  },
  core_v0_simple: {
    id: "core_v0_simple",
    label: "Core v0 simplified / legacy alias for distributed planning default",
    ...coreBase,
    planningSource: "distributed",
  },
};

const activeArchitectures = scenario.architectures.map((id) => {
  const arch = ARCHITECTURES[id];
  if (!arch) throw new Error(`Unknown architecture in scenario: ${id}`);
  return arch;
});

const makeProject = (rng, id, scenario) => {
  const pCfg = scenario.projects;
  const latentValue = sampleDist(rng, pCfg.latentValue);
  const salience = clamp(pCfg.salienceCorrelation * latentValue + (1 - pCfg.salienceCorrelation) * rng(), 0.01, 0.99);

  const centralMix = pCfg.centralPlanningSignalMix ?? pCfg.planningWeightCorrelation ?? 0.15;
  const distributedMix = pCfg.distributedPlanningSignalMix ?? 0.70;
  const centralPlanningWeight = clamp(centralMix * latentValue + (1 - centralMix) * rng(), 0.01, 0.99);
  const distributedPlanningWeight = clamp(distributedMix * latentValue + (1 - distributedMix) * rng(), 0.01, 0.99);

  const verificationDifficulty = sampleDist(rng, pCfg.verificationDifficulty);
  const executionDifficulty = sampleDist(rng, pCfg.executionDifficulty);
  const fraudOpportunity = sampleDist(rng, pCfg.fraudOpportunity);
  const targetBase = (pCfg.scarcity * scenario.population.citizens * scenario.cycles) / pCfg.activePool;
  const budgetTarget = (0.5 + rng()) * targetBase;
  const opportunistic = rng() < scenario.executors.opportunisticShare;
  return {
    id,
    latentValue,
    salience,
    centralPlanningWeight,
    distributedPlanningWeight,
    verificationDifficulty,
    executionDifficulty,
    fraudOpportunity,
    budgetTarget,
    executorType: opportunistic ? "opportunistic" : "honest",
    executorAbility: sampleDist(rng, scenario.executors.ability),
    funded: 0,
    closed: false,
    cycleClosed: null,
    execution: null,
  };
};

const generateWorld = (seed, scenario) => {
  const rng = mulberry32(seed);
  const projects = [];
  for (let i = 0; i < scenario.projects.activePool; i++) projects.push(makeProject(rng, `P-${String(i + 1).padStart(3, "0")}`, scenario));
  return { seed, projects };
};

const cloneWorld = (world) => ({
  seed: world.seed,
  projects: world.projects.map((p) => ({ ...p, funded: 0, closed: false, cycleClosed: null, execution: null })),
});

const openProjects = (sim) => sim.projects.filter((p) => !p.closed);
const availableBudget = (scenario) => scenario.population.citizens * scenario.cycles;
const planningScore = (p, arch) => arch.planningSource === "distributed" ? p.distributedPlanningWeight : p.centralPlanningWeight;

const contribute = (project, amount, arch) => {
  if (amount <= 0 || project.closed) return amount;
  if (!arch.fundingCaps) {
    project.funded += amount;
    return 0;
  }
  const room = Math.max(0, project.budgetTarget - project.funded);
  const paid = Math.min(room, amount);
  project.funded += paid;
  return amount - paid;
};

const fundingProgress = (p) => Math.max(0, p.funded / Math.max(1, p.budgetTarget));
const visibilityScore = (p, arch, scenario) => {
  const attack = scenario.attacks.salienceCascade ?? {};
  const socialProof = attack.enabled ? attack.socialProofWeight : 1.0;
  return p.salience * (1 + socialProof * arch.socialProofDamping * fundingProgress(p));
};

// Sample without replacement (partial Fisher-Yates over an index array).
const drawSample = (rng, projects, k) => {
  const idx = projects.map((_, i) => i);
  const n = Math.min(k, idx.length);
  for (let i = 0; i < n; i++) {
    const j = i + Math.floor(rng() * (idx.length - i));
    [idx[i], idx[j]] = [idx[j], idx[i]];
  }
  const out = [];
  for (let i = 0; i < n; i++) out.push(projects[idx[i]]);
  return out;
};

const allocateCentral = (sim, arch, scenario) => {
  let budget = scenario.population.citizens;
  const projects = openProjects(sim).sort((a, b) => planningScore(b, arch) - planningScore(a, arch));
  for (const p of projects) {
    if (budget <= 0) break;
    const before = budget;
    budget = contribute(p, budget, arch);
    if (before === budget) break;
  }
};

// Informed choice shared by attentive citizens and delegates: perceive each
// sampled project ONCE with noise, rank, then contribute down the ranking.
const allocateInformed = (rng, sim, arch, scenario, count, { noiseScale = 1.0, nearCompletionBonus = 0.0, unitsPerActor = 1 } = {}) => {
  const sampleSize = scenario.population.attentiveSampleSize ?? 8;
  let leftover = 0;
  for (let i = 0; i < count; i++) {
    const projects = openProjects(sim);
    if (!projects.length) return leftover + (count - i) * unitsPerActor;
    const sample = drawSample(rng, projects, sampleSize);
    const scored = sample.map((p) => ({
      p,
      utility: p.latentValue
        + normal(rng, 0, arch.informationNoise * noiseScale)
        + nearCompletionBonus * fundingProgress(p)
        - 0.15 * p.verificationDifficulty,
    })).sort((a, b) => b.utility - a.utility);
    let amount = unitsPerActor;
    for (const { p } of scored) {
      amount = contribute(p, amount, arch);
      if (amount <= 0) break;
    }
    leftover += amount;
  }
  return leftover;
};

const allocateAttentive = (rng, sim, arch, scenario, count) =>
  allocateInformed(rng, sim, arch, scenario, count);

// Profile-driven citizens (AGENT_DECISION_MODEL, "Profile-driven citizen"):
// configured preferences act as a noisier value proxy with a near-completion
// preference; no personal inspection.
const allocateProfile = (rng, sim, arch, scenario, count) =>
  allocateInformed(rng, sim, arch, scenario, count, { noiseScale: 1.5, nearCompletionBonus: 0.20 });

// Delegating citizens (AGENT_DECISION_MODEL, "Delegating citizen"): delegates
// allocate represented weight in blocks with attentive-grade information — the
// trusted-microdelegation proxy (many small delegates, informed review).
const allocateDelegated = (rng, sim, arch, scenario, count) => {
  const blockSize = Math.max(1, Math.round(scenario.population.delegationBlockSize ?? 3));
  const blocks = Math.floor(count / blockSize);
  const remainder = count - blocks * blockSize;
  let leftover = allocateInformed(rng, sim, arch, scenario, blocks, { unitsPerActor: blockSize });
  if (remainder > 0) leftover += allocateInformed(rng, sim, arch, scenario, 1, { unitsPerActor: remainder });
  return leftover;
};

const allocateSalience = (rng, sim, arch, scenario, count) => {
  const slots = scenario.attacks.salienceCascade?.visibleSlots ?? 6;
  let leftover = 0;
  for (let i = 0; i < count; i++) {
    let amount = 1;
    const projects = openProjects(sim);
    if (!projects.length) return leftover + (count - i);
    const top = [...projects].sort((a, b) => visibilityScore(b, arch, scenario) - visibilityScore(a, arch, scenario)).slice(0, slots);
    for (let attempts = 0; attempts < Math.min(4, top.length) && amount > 0; attempts++) {
      const picked = weightedPick(rng, top, (p) => visibilityScore(p, arch, scenario));
      amount = contribute(picked, amount, arch);
    }
    leftover += amount;
  }
  return leftover;
};

const allocateDefault = (sim, arch, scenario, count) => {
  if (count <= 0) return;
  let budget = count;
  const projects = openProjects(sim).sort((a, b) => planningScore(b, arch) - planningScore(a, arch));
  for (const p of projects) {
    if (budget <= 0) break;
    const room = arch.fundingCaps ? Math.max(0, p.budgetTarget - p.funded) : Infinity;
    const paid = Math.min(budget, room);
    p.funded += paid;
    budget -= paid;
  }
};

const allocateCitizen = (rng, sim, arch, scenario) => {
  const pop = scenario.population;
  const N = pop.citizens;
  const attentive = Math.round(N * pop.attentiveShare);
  const salience = Math.round(N * pop.salienceShare);
  // Profile and delegated channels exist only where the platform provides a
  // default layer (AGENT_DECISION_MODEL, passive citizen: "if
  // architecture.hasDefaultLayer"); elsewhere those shares stay in the passive block.
  const hasDefaultLayer = arch.passiveAllocationMode === "planning";
  const profile = hasDefaultLayer ? Math.round(N * (pop.profileShare ?? 0)) : 0;
  const delegated = hasDefaultLayer ? Math.round(N * (pop.delegatorShare ?? 0)) : 0;
  const remaining = N - attentive - salience - profile - delegated;
  let leftover = 0;
  leftover += allocateAttentive(rng, sim, arch, scenario, attentive);
  leftover += allocateSalience(rng, sim, arch, scenario, salience);
  if (profile > 0) leftover += allocateProfile(rng, sim, arch, scenario, profile);
  if (delegated > 0) leftover += allocateDelegated(rng, sim, arch, scenario, delegated);
  if (arch.passiveAllocationMode === "planning") {
    // docs/101: unexercised allocation follows the public default rule.
    allocateDefault(sim, arch, scenario, remaining + leftover);
  } else if (arch.passiveAllocationMode === "salience") {
    allocateSalience(rng, sim, arch, scenario, remaining);
  }
  // passiveAllocationMode "none": remaining and leftover stay unallocated — the
  // low-absorption failure the weak participatory variant exists to show.
};

const detectionProbability = (project, arch, scenario) => {
  const weak = scenario.attacks.weakVerificationDiversion ?? {};
  const shock = weak.enabled ? weak.detectionShock ?? 1.0 : 1.0;
  const p = arch.detectionBase * shock * (1 - 0.55 * project.verificationDifficulty);
  return clamp(p, 0.01, 0.98);
};

const executeProject = (rng, project, arch, scenario, cycle) => {
  const fundedBudget = project.funded;
  const targetBudget = project.budgetTarget;
  const potentialValue = targetBudget * project.latentValue;
  const detection = detectionProbability(project, arch, scenario);
  let diverted = false;
  let diversionShare = 0;
  let executionQuality = 1;

  if (project.executorType === "opportunistic") {
    const fraudGain = project.fraudOpportunity * (1 - arch.retention);
    const x = -1.0
      + 4.0 * fraudGain
      + 2.0 * project.verificationDifficulty
      - 5.0 * detection
      - 3.0 * arch.retention
      - 2.0 * arch.guarantee
      - 3.0 * arch.reputationLoss
      - 2.0 * arch.futureSelectionLoss;
    diverted = rng() < sigmoid(x);
    if (diverted) {
      diversionShare = clamp(0.20 + 0.60 * project.fraudOpportunity + normal(rng, 0, 0.05), 0.05, 0.95);
      executionQuality = clamp((1 - diversionShare) * (0.55 + 0.45 * project.executorAbility), 0.02, 1);
    } else {
      executionQuality = clamp(0.70 + 0.30 * project.executorAbility - 0.20 * project.executionDifficulty, 0.20, 1);
    }
  } else {
    const pGoodDelivery = sigmoid(1.5 + 2.5 * project.executorAbility - 3.0 * project.executionDifficulty);
    const good = rng() < pGoodDelivery;
    executionQuality = good
      ? clamp(0.75 + 0.25 * project.executorAbility, 0.30, 1)
      : clamp(0.35 + 0.35 * project.executorAbility - 0.20 * project.executionDifficulty, 0.05, 0.85);
  }

  const detected = diverted ? rng() < detection : false;
  const reportedCompletion = diverted && !detected ? 1 : executionQuality;
  const reviewConfidence = detected ? 1 : clamp(arch.reviewConfidence * (1 - 0.35 * project.verificationDifficulty), 0.05, 1);
  const actualValue = potentialValue * executionQuality;
  const verifiedValue = actualValue * reviewConfidence;
  const reportedValue = potentialValue * reportedCompletion;
  const leakage = diverted ? fundedBudget * diversionShare : 0;

  project.closed = true;
  project.cycleClosed = cycle;
  project.execution = {
    fundedBudget,
    targetBudget,
    potentialValue,
    actualValue,
    verifiedValue,
    reportedValue,
    executionQuality,
    diverted,
    diversionShare,
    leakage,
    detected,
    detection,
    reviewConfidence,
  };
};

const closeAndExecuteFunded = (rng, sim, arch, scenario, cycle) => {
  for (const p of sim.projects) if (!p.closed && p.funded >= p.budgetTarget) executeProject(rng, p, arch, scenario, cycle);
};

const runArchitecture = (world, arch, scenario, runSeed, archIndex) => {
  const rng = mulberry32((runSeed ^ ((archIndex + 1) * 0x9e3779b9)) >>> 0);
  const sim = cloneWorld(world);
  for (let cycle = 0; cycle < scenario.cycles; cycle++) {
    if (!openProjects(sim).length) break;
    if (arch.centralPlanner) allocateCentral(sim, arch, scenario);
    else allocateCitizen(rng, sim, arch, scenario);
    closeAndExecuteFunded(rng, sim, arch, scenario, cycle);
  }
  return computeMetrics(sim, arch, scenario);
};

const computeMetrics = (sim, arch, scenario) => {
  const projects = sim.projects;
  const executed = projects.filter((p) => p.execution);
  const fundedFlag = projects.map((p) => p.execution ? 1 : 0);
  const values = projects.map((p) => p.latentValue);
  const saliences = projects.map((p) => p.salience);
  const centralPlanningWeights = projects.map((p) => p.centralPlanningWeight);
  const distributedPlanningWeights = projects.map((p) => p.distributedPlanningWeight);
  const fundedAmounts = projects.map((p) => p.funded);
  const budgetSpent = fundedAmounts.reduce((a, b) => a + b, 0);
  const totalAvailableBudget = availableBudget(scenario);
  const safeBudget = budgetSpent || 1;
  const actualValue = executed.reduce((a, p) => a + p.execution.actualValue, 0);
  const verifiedValue = executed.reduce((a, p) => a + p.execution.verifiedValue, 0);
  const reportedValue = executed.reduce((a, p) => a + p.execution.reportedValue, 0);
  const leakage = executed.reduce((a, p) => a + p.execution.leakage, 0);
  const detectedDiversions = executed.filter((p) => p.execution.diverted && p.execution.detected).length;
  const diversions = executed.filter((p) => p.execution.diverted).length;
  const topSalience = [...projects].sort((a, b) => b.salience - a.salience).slice(0, Math.max(1, Math.ceil(projects.length * 0.05)));
  const topSalienceFunding = topSalience.reduce((a, p) => a + p.funded, 0);
  const funded = projects.filter((p) => p.execution);
  const unfunded = projects.filter((p) => !p.execution);
  return {
    architecture: arch.id,
    architectureLabel: arch.label,
    planningSource: arch.planningSource,
    totalAvailableBudget,
    budgetSpent,
    unspentBudget: Math.max(0, totalAvailableBudget - budgetSpent),
    budgetUtilizationRate: budgetSpent / totalAvailableBudget,
    unspentBudgetRate: Math.max(0, totalAvailableBudget - budgetSpent) / totalAvailableBudget,
    executedProjects: executed.length,
    fundedRate: executed.length / projects.length,
    actualValuePerBudget: actualValue / safeBudget,
    verifiedValuePerBudget: verifiedValue / safeBudget,
    reportedValuePerBudget: reportedValue / safeBudget,
    visibilityGapPerBudget: (reportedValue - actualValue) / safeBudget,
    leakageRate: leakage / safeBudget,
    diversionRateAmongExecuted: executed.length ? diversions / executed.length : 0,
    detectionRateAmongDiversions: diversions ? detectedDiversions / diversions : 0,
    fundingGini: gini(fundedAmounts),
    topSalienceFundingShare: budgetSpent ? topSalienceFunding / budgetSpent : 0,
    selectionValueCorrelation: pearson(fundedFlag, values),
    selectionSalienceCorrelation: pearson(fundedFlag, saliences),
    salienceValueCorrelation: pearson(saliences, values),
    centralPlanningValueCorrelation: pearson(centralPlanningWeights, values),
    distributedPlanningValueCorrelation: pearson(distributedPlanningWeights, values),
    fundedValueMean: mean(funded.map((p) => p.latentValue)),
    unfundedValueMean: mean(unfunded.map((p) => p.latentValue)),
    qualityGap: mean(funded.map((p) => p.latentValue)) - mean(unfunded.map((p) => p.latentValue)),
  };
};

const runScenario = (scenario) => {
  const raw = [];
  for (let r = 0; r < scenario.runs; r++) {
    const runSeed = scenario.seed + r * 7919;
    const world = generateWorld(runSeed, scenario);
    activeArchitectures.forEach((arch, archIndex) => raw.push({
      scenario_id: scenario.scenario_id,
      run: r,
      seed: runSeed,
      ...runArchitecture(world, arch, scenario, runSeed, archIndex),
    }));
  }
  const summary = activeArchitectures.map((arch) => {
    const subset = raw.filter((r) => r.architecture === arch.id);
    return {
      architecture: arch.id,
      label: arch.label,
      budgetSpent: summarize(subset, "budgetSpent"),
      budgetUtilizationRate: summarize(subset, "budgetUtilizationRate"),
      unspentBudgetRate: summarize(subset, "unspentBudgetRate"),
      fundedRate: summarize(subset, "fundedRate"),
      actualValuePerBudget: summarize(subset, "actualValuePerBudget"),
      verifiedValuePerBudget: summarize(subset, "verifiedValuePerBudget"),
      reportedValuePerBudget: summarize(subset, "reportedValuePerBudget"),
      visibilityGapPerBudget: summarize(subset, "visibilityGapPerBudget"),
      leakageRate: summarize(subset, "leakageRate"),
      diversionRateAmongExecuted: summarize(subset, "diversionRateAmongExecuted"),
      detectionRateAmongDiversions: summarize(subset, "detectionRateAmongDiversions"),
      fundingGini: summarize(subset, "fundingGini"),
      topSalienceFundingShare: summarize(subset, "topSalienceFundingShare"),
      selectionValueCorrelation: summarize(subset, "selectionValueCorrelation"),
      qualityGap: summarize(subset, "qualityGap"),
      salienceValueCorrelation: summarize(subset, "salienceValueCorrelation"),
      centralPlanningValueCorrelation: summarize(subset, "centralPlanningValueCorrelation"),
      distributedPlanningValueCorrelation: summarize(subset, "distributedPlanningValueCorrelation"),
    };
  });
  return { raw, summary };
};

const markdownTable = (summary) => {
  const lines = [];
  lines.push(`scenario: ${scenario.scenario_id} v${scenario.scenario_version ?? "n/a"} | engine: v${ENGINE_VERSION}`);
  lines.push(`runs: ${scenario.runs}, base seed: ${scenario.seed}, cycles: ${scenario.cycles}, citizens: ${scenario.population.citizens}, projects: ${scenario.projects.activePool}`);
  lines.push(`centralPlanningSignalMix: ${scenario.projects.centralPlanningSignalMix ?? scenario.projects.planningWeightCorrelation ?? "n/a"}, distributedPlanningSignalMix: ${scenario.projects.distributedPlanningSignalMix ?? "n/a"}`);
  lines.push(`architectures: ${scenario.architectures.join(", ")}`);
  lines.push("");
  lines.push("| architecture | budget spent | unspent | funded rate | actual value/budget | verified value/budget | reported value/budget | visibility gap | leakage | funding Gini | sel(value) | central plan corr | distributed plan corr | salience corr |");
  lines.push("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|");
  for (const r of summary) lines.push(`| ${r.architecture} | ${fmtMean(r.budgetSpent)} | ${fmtMean(r.unspentBudgetRate)} | ${fmtMean(r.fundedRate)} | ${fmtMean(r.actualValuePerBudget)} | ${fmtMean(r.verifiedValuePerBudget)} | ${fmtMean(r.reportedValuePerBudget)} | ${fmtMean(r.visibilityGapPerBudget)} | ${fmtMean(r.leakageRate)} | ${fmtMean(r.fundingGini)} | ${fmtMean(r.selectionValueCorrelation)} | ${fmtMean(r.centralPlanningValueCorrelation)} | ${fmtMean(r.distributedPlanningValueCorrelation)} | ${fmtMean(r.salienceValueCorrelation)} |`);
  return lines.join("\n");
};

const csvTable = (summary) => {
  const fields = [
    "architecture",
    "budgetSpent_mean", "budgetSpent_sd",
    "budgetUtilizationRate_mean", "budgetUtilizationRate_sd",
    "unspentBudgetRate_mean", "unspentBudgetRate_sd",
    "fundedRate_mean", "fundedRate_sd",
    "actualValuePerBudget_mean", "actualValuePerBudget_sd",
    "verifiedValuePerBudget_mean", "verifiedValuePerBudget_sd",
    "reportedValuePerBudget_mean", "reportedValuePerBudget_sd",
    "visibilityGapPerBudget_mean", "visibilityGapPerBudget_sd",
    "leakageRate_mean", "leakageRate_sd",
    "fundingGini_mean", "fundingGini_sd",
    "selectionValueCorrelation_mean", "selectionValueCorrelation_sd",
    "centralPlanningValueCorrelation_mean", "centralPlanningValueCorrelation_sd",
    "distributedPlanningValueCorrelation_mean", "distributedPlanningValueCorrelation_sd",
    "salienceValueCorrelation_mean", "salienceValueCorrelation_sd",
  ];
  const rows = [fields.join(",")];
  for (const r of summary) rows.push([
    r.architecture,
    r.budgetSpent.mean, r.budgetSpent.sd,
    r.budgetUtilizationRate.mean, r.budgetUtilizationRate.sd,
    r.unspentBudgetRate.mean, r.unspentBudgetRate.sd,
    r.fundedRate.mean, r.fundedRate.sd,
    r.actualValuePerBudget.mean, r.actualValuePerBudget.sd,
    r.verifiedValuePerBudget.mean, r.verifiedValuePerBudget.sd,
    r.reportedValuePerBudget.mean, r.reportedValuePerBudget.sd,
    r.visibilityGapPerBudget.mean, r.visibilityGapPerBudget.sd,
    r.leakageRate.mean, r.leakageRate.sd,
    r.fundingGini.mean, r.fundingGini.sd,
    r.selectionValueCorrelation.mean, r.selectionValueCorrelation.sd,
    r.centralPlanningValueCorrelation.mean, r.centralPlanningValueCorrelation.sd,
    r.distributedPlanningValueCorrelation.mean, r.distributedPlanningValueCorrelation.sd,
    r.salienceValueCorrelation.mean, r.salienceValueCorrelation.sd,
  ].map((x) => typeof x === "number" ? x.toFixed(8) : x).join(","));
  return rows.join("\n");
};

const writeOutputs = ({ raw, summary }) => {
  const outDir = resolve(HERE, "../results", scenario.scenario_id);
  mkdirSync(outDir, { recursive: true });
  const base = `${scenario.scenario_id}-seed${scenario.seed}-runs${scenario.runs}`;
  if (scenario.outputs?.rawJson) writeFileSync(resolve(outDir, `${base}.raw.json`), JSON.stringify(raw, null, 2));
  if (scenario.outputs?.markdownTable) writeFileSync(resolve(outDir, `${base}.summary.md`), markdownTable(summary) + "\n");
  if (scenario.outputs?.csv) writeFileSync(resolve(outDir, `${base}.summary.csv`), csvTable(summary) + "\n");
  writeFileSync(resolve(outDir, `${base}.meta.json`), JSON.stringify({
    engine_version: ENGINE_VERSION,
    scenario_id: scenario.scenario_id,
    scenario_version: scenario.scenario_version ?? null,
    seed: scenario.seed,
    runs: scenario.runs,
    architectures: scenario.architectures,
  }, null, 2) + "\n");
  return outDir;
};

const result = runScenario(scenario);
const table = markdownTable(result.summary);
console.log(table);
const outDir = writeOutputs(result);
console.log(`\noutputs: ${outDir}`);
