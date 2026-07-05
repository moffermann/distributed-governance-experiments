#!/usr/bin/env node
// Minimal adversarial ABM engine for public-resource allocation architecture stress testing.
//
// v0 goals:
// - dependency-free Node.js;
// - deterministic under seed;
// - common-world paired comparison;
// - three initial architectures;
// - two initial attack pressures: salience cascade and weak-verification diversion;
// - first result table for delivered value, verified value, leakage, visibility gap, and concentration.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

// -----------------------------------------------------------------------------
// CLI
// -----------------------------------------------------------------------------

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

const cli = parseArgs();
const scenarioPath = resolve(cli.scenario ?? "experiments/adversarial-abm/scenarios/baseline-medium.json");
const scenario = JSON.parse(readFileSync(scenarioPath, "utf8"));
if (cli.runs) scenario.runs = Number.parseInt(cli.runs, 10);
if (cli.seed) scenario.seed = Number.parseInt(cli.seed, 10);

// -----------------------------------------------------------------------------
// Deterministic random utilities
// -----------------------------------------------------------------------------

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

// Marsaglia-Tsang Gamma sampler; sufficient for synthetic parameter generation.
const gamma = (rng, shape, scale = 1) => {
  if (shape <= 0) throw new Error(`Gamma shape must be positive, got ${shape}`);
  if (shape < 1) {
    const u = rng();
    return gamma(rng, shape + 1, scale) * Math.pow(u, 1 / shape);
  }
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

// -----------------------------------------------------------------------------
// Stats
// -----------------------------------------------------------------------------

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

// -----------------------------------------------------------------------------
// Architectures
// -----------------------------------------------------------------------------

const ARCHITECTURES = {
  status_quo: {
    id: "status_quo",
    label: "Status quo / audit-after-fact",
    centralPlanner: true,
    citizenAllocation: false,
    defaultLayer: false,
    fundingCaps: true,
    informationNoise: 0.45,
    detectionBase: 0.15,
    reviewConfidence: 0.35,
    retention: 0.05,
    guarantee: 0.02,
    reputationLoss: 0.02,
    futureSelectionLoss: 0.02,
    socialProofDamping: 1.00,
    passiveUsesDefault: false,
  },
  participatory_weak_verification: {
    id: "participatory_weak_verification",
    label: "Participatory / weak verification",
    centralPlanner: false,
    citizenAllocation: true,
    defaultLayer: false,
    fundingCaps: false,
    informationNoise: 0.35,
    detectionBase: 0.20,
    reviewConfidence: 0.40,
    retention: 0.05,
    guarantee: 0.00,
    reputationLoss: 0.03,
    futureSelectionLoss: 0.03,
    socialProofDamping: 1.00,
    passiveUsesDefault: false,
  },
  core_v0_simple: {
    id: "core_v0_simple",
    label: "Core v0 simplified",
    centralPlanner: false,
    citizenAllocation: true,
    defaultLayer: true,
    fundingCaps: true,
    informationNoise: 0.18,
    detectionBase: 0.55,
    reviewConfidence: 0.85,
    retention: 0.25,
    guarantee: 0.15,
    reputationLoss: 0.20,
    futureSelectionLoss: 0.15,
    socialProofDamping: 0.60,
    passiveUsesDefault: true,
  },
};

const activeArchitectures = scenario.architectures.map((id) => {
  const arch = ARCHITECTURES[id];
  if (!arch) throw new Error(`Unknown architecture in scenario: ${id}`);
  return arch;
});

// -----------------------------------------------------------------------------
// World generation
// -----------------------------------------------------------------------------

const makeProject = (rng, id, scenario) => {
  const pCfg = scenario.projects;
  const latentValue = sampleDist(rng, pCfg.latentValue);
  const salienceNoise = rng();
  const planningNoise = rng();
  const salience = clamp(pCfg.salienceCorrelation * latentValue + (1 - pCfg.salienceCorrelation) * salienceNoise, 0.01, 0.99);
  const planningWeight = clamp(pCfg.planningWeightCorrelation * latentValue + (1 - pCfg.planningWeightCorrelation) * planningNoise, 0.01, 0.99);
  const verificationDifficulty = sampleDist(rng, pCfg.verificationDifficulty);
  const executionDifficulty = sampleDist(rng, pCfg.executionDifficulty);
  const fraudOpportunity = sampleDist(rng, pCfg.fraudOpportunity);
  const targetBase = (pCfg.scarcity * scenario.population.citizens * scenario.cycles) / pCfg.activePool;
  const budgetTarget = (0.5 + rng()) * targetBase;
  const opportunistic = rng() < scenario.executors.opportunisticShare;
  const ability = sampleDist(rng, scenario.executors.ability);
  return {
    id,
    latentValue,
    salience,
    planningWeight,
    verificationDifficulty,
    executionDifficulty,
    fraudOpportunity,
    budgetTarget,
    executorType: opportunistic ? "opportunistic" : "honest",
    executorAbility: ability,
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

// -----------------------------------------------------------------------------
// Allocation helpers
// -----------------------------------------------------------------------------

const openProjects = (sim) => sim.projects.filter((p) => !p.closed);

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

const visibilityScore = (p, sim, arch, scenario) => {
  const attack = scenario.attacks.salienceCascade ?? {};
  const socialProof = attack.enabled ? attack.socialProofWeight : 1.0;
  return p.salience * (1 + socialProof * arch.socialProofDamping * fundingProgress(p));
};

const allocateCentral = (sim, arch, scenario) => {
  let budget = scenario.population.citizens;
  const projects = openProjects(sim).sort((a, b) => b.planningWeight - a.planningWeight);
  for (const p of projects) {
    if (budget <= 0) break;
    const before = budget;
    const remainder = contribute(p, budget, arch);
    budget = remainder;
    if (before === budget) break;
  }
};

const allocateAttentive = (rng, sim, arch, scenario, count) => {
  const sampleSize = scenario.population.attentiveSampleSize ?? 8;
  for (let i = 0; i < count; i++) {
    const projects = openProjects(sim);
    if (!projects.length) return;
    const sample = [];
    for (let k = 0; k < Math.min(sampleSize, projects.length); k++) sample.push(projects[Math.floor(rng() * projects.length)]);
    sample.sort((a, b) => {
      const ua = a.latentValue + normal(rng, 0, arch.informationNoise) - 0.15 * a.verificationDifficulty;
      const ub = b.latentValue + normal(rng, 0, arch.informationNoise) - 0.15 * b.verificationDifficulty;
      return ub - ua;
    });
    let amount = 1;
    for (const p of sample) {
      amount = contribute(p, amount, arch);
      if (amount <= 0) break;
    }
  }
};

const allocateSalience = (rng, sim, arch, scenario, count) => {
  const slots = scenario.attacks.salienceCascade?.visibleSlots ?? 6;
  for (let i = 0; i < count; i++) {
    let amount = 1;
    const projects = openProjects(sim);
    if (!projects.length) return;
    const top = [...projects].sort((a, b) => visibilityScore(b, sim, arch, scenario) - visibilityScore(a, sim, arch, scenario)).slice(0, slots);
    for (let attempts = 0; attempts < Math.min(4, top.length) && amount > 0; attempts++) {
      const picked = weightedPick(rng, top, (p) => visibilityScore(p, sim, arch, scenario));
      amount = contribute(picked, amount, arch);
    }
  }
};

const allocateDefault = (sim, arch, scenario, count) => {
  if (count <= 0) return;
  let budget = count;
  const projects = openProjects(sim).sort((a, b) => b.planningWeight - a.planningWeight);
  for (const p of projects) {
    if (budget <= 0) break;
    const room = Math.max(0, p.budgetTarget - p.funded);
    const paid = Math.min(budget, room);
    p.funded += paid;
    budget -= paid;
  }
};

const allocateCitizen = (rng, sim, arch, scenario) => {
  const N = scenario.population.citizens;
  const attentive = Math.round(N * scenario.population.attentiveShare);
  const salience = Math.round(N * scenario.population.salienceShare);
  const remaining = N - attentive - salience;
  const defaultCount = arch.passiveUsesDefault ? remaining : 0;
  allocateAttentive(rng, sim, arch, scenario, attentive);
  allocateSalience(rng, sim, arch, scenario, salience);
  allocateDefault(sim, arch, scenario, defaultCount);
};

// -----------------------------------------------------------------------------
// Execution, review, disbursement proxy
// -----------------------------------------------------------------------------

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
    const pDivert = sigmoid(x);
    diverted = rng() < pDivert;
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
  for (const p of sim.projects) {
    if (!p.closed && p.funded >= p.budgetTarget) executeProject(rng, p, arch, scenario, cycle);
  }
};

// -----------------------------------------------------------------------------
// Simulation and metrics
// -----------------------------------------------------------------------------

const runArchitecture = (world, arch, scenario, runSeed, archIndex) => {
  const rng = mulberry32((runSeed ^ ((archIndex + 1) * 0x9e3779b9)) >>> 0);
  const sim = cloneWorld(world);
  for (let cycle = 0; cycle < scenario.cycles; cycle++) {
    if (!openProjects(sim).length) break;
    if (arch.centralPlanner) allocateCentral(sim, arch, scenario);
    else allocateCitizen(rng, sim, arch, scenario);
    closeAndExecuteFunded(rng, sim, arch, scenario, cycle);
  }

  // Expired/unfunded projects remain unexecuted in this v0 skeleton.
  return computeMetrics(sim, arch, scenario);
};

const computeMetrics = (sim, arch, scenario) => {
  const projects = sim.projects;
  const executed = projects.filter((p) => p.execution);
  const fundedFlag = projects.map((p) => p.execution ? 1 : 0);
  const values = projects.map((p) => p.latentValue);
  const saliences = projects.map((p) => p.salience);
  const fundedAmounts = projects.map((p) => p.funded);
  const budgetSpent = fundedAmounts.reduce((a, b) => a + b, 0);
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
    budgetSpent,
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
    fundedValueMean: mean(funded.map((p) => p.latentValue)),
    unfundedValueMean: mean(unfunded.map((p) => p.latentValue)),
    qualityGap: mean(funded.map((p) => p.latentValue)) - mean(unfunded.map((p) => p.latentValue)),
  };
};

const runScenario = (scenario) => {
  const rows = [];
  const raw = [];
  for (let r = 0; r < scenario.runs; r++) {
    const runSeed = scenario.seed + r * 7919;
    const world = generateWorld(runSeed, scenario);
    activeArchitectures.forEach((arch, archIndex) => {
      const metrics = runArchitecture(world, arch, scenario, runSeed, archIndex);
      const record = { scenario_id: scenario.scenario_id, run: r, seed: runSeed, ...metrics };
      raw.push(record);
    });
  }
  for (const arch of activeArchitectures) {
    const subset = raw.filter((r) => r.architecture === arch.id);
    rows.push({
      architecture: arch.id,
      label: arch.label,
      budgetSpent: summarize(subset, "budgetSpent"),
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
    });
  }
  return { raw, summary: rows };
};

// -----------------------------------------------------------------------------
// Output
// -----------------------------------------------------------------------------

const markdownTable = (summary) => {
  const lines = [];
  lines.push(`scenario: ${scenario.scenario_id} v${scenario.scenario_version ?? "n/a"}`);
  lines.push(`runs: ${scenario.runs}, base seed: ${scenario.seed}, cycles: ${scenario.cycles}, citizens: ${scenario.population.citizens}, projects: ${scenario.projects.activePool}`);
  lines.push(`architectures: ${scenario.architectures.join(", ")}`);
  lines.push("");
  lines.push("| architecture | budget spent | funded rate | actual value/budget | verified value/budget | reported value/budget | visibility gap | leakage | funding Gini | sel(value) |");
  lines.push("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|");
  for (const r of summary) {
    lines.push(`| ${r.architecture} | ${fmtMean(r.budgetSpent)} | ${fmtMean(r.fundedRate)} | ${fmtMean(r.actualValuePerBudget)} | ${fmtMean(r.verifiedValuePerBudget)} | ${fmtMean(r.reportedValuePerBudget)} | ${fmtMean(r.visibilityGapPerBudget)} | ${fmtMean(r.leakageRate)} | ${fmtMean(r.fundingGini)} | ${fmtMean(r.selectionValueCorrelation)} |`);
  }
  return lines.join("\n");
};

const csvTable = (summary) => {
  const fields = [
    "architecture",
    "budgetSpent_mean", "budgetSpent_sd",
    "fundedRate_mean", "fundedRate_sd",
    "actualValuePerBudget_mean", "actualValuePerBudget_sd",
    "verifiedValuePerBudget_mean", "verifiedValuePerBudget_sd",
    "reportedValuePerBudget_mean", "reportedValuePerBudget_sd",
    "visibilityGapPerBudget_mean", "visibilityGapPerBudget_sd",
    "leakageRate_mean", "leakageRate_sd",
    "fundingGini_mean", "fundingGini_sd",
    "selectionValueCorrelation_mean", "selectionValueCorrelation_sd",
  ];
  const rows = [fields.join(",")];
  for (const r of summary) {
    rows.push([
      r.architecture,
      r.budgetSpent.mean, r.budgetSpent.sd,
      r.fundedRate.mean, r.fundedRate.sd,
      r.actualValuePerBudget.mean, r.actualValuePerBudget.sd,
      r.verifiedValuePerBudget.mean, r.verifiedValuePerBudget.sd,
      r.reportedValuePerBudget.mean, r.reportedValuePerBudget.sd,
      r.visibilityGapPerBudget.mean, r.visibilityGapPerBudget.sd,
      r.leakageRate.mean, r.leakageRate.sd,
      r.fundingGini.mean, r.fundingGini.sd,
      r.selectionValueCorrelation.mean, r.selectionValueCorrelation.sd,
    ].map((x) => typeof x === "number" ? x.toFixed(8) : x).join(","));
  }
  return rows.join("\n");
};

const writeOutputs = ({ raw, summary }) => {
  const outDir = resolve("experiments/adversarial-abm/results", scenario.scenario_id);
  mkdirSync(outDir, { recursive: true });
  const base = `${scenario.scenario_id}-seed${scenario.seed}-runs${scenario.runs}`;
  if (scenario.outputs?.rawJson) writeFileSync(resolve(outDir, `${base}.raw.json`), JSON.stringify(raw, null, 2));
  if (scenario.outputs?.markdownTable) writeFileSync(resolve(outDir, `${base}.summary.md`), markdownTable(summary) + "\n");
  if (scenario.outputs?.csv) writeFileSync(resolve(outDir, `${base}.summary.csv`), csvTable(summary) + "\n");
  return outDir;
};

const result = runScenario(scenario);
const table = markdownTable(result.summary);
console.log(table);
const outDir = writeOutputs(result);
console.log(`\noutputs: ${outDir}`);

// Ensure parent path exists in case the script is launched from a different cwd.
void dirname;
