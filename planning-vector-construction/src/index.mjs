#!/usr/bin/env node
// Planning Vector Construction Experiment
//
// Generates a synthetic population, latent social value over planning targets,
// representative central planning vectors, distributed planning vectors, and
// compares their correlations with latent public value.

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

const cli = parseArgs();
const scenarioPath = resolve(cli.scenario ?? "experiments/planning-vector-construction/scenarios/baseline-comparison.json");
const scenario = JSON.parse(readFileSync(scenarioPath, "utf8"));
if (cli.runs) scenario.runs = Number.parseInt(cli.runs, 10);
if (cli.seed) scenario.seed = Number.parseInt(cli.seed, 10);

const clamp = (x, lo = 0, hi = 1) => Math.max(lo, Math.min(hi, x));
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
const beta = (rng, a, b) => {
  const x = gamma(rng, a);
  const y = gamma(rng, b);
  return x / (x + y);
};

const mean = (xs) => xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0;
const sd = (xs) => {
  if (xs.length < 2) return 0;
  const m = mean(xs);
  return Math.sqrt(xs.reduce((a, x) => a + (x - m) ** 2, 0) / (xs.length - 1));
};
const pearson = (xs, ys) => {
  if (xs.length !== ys.length || xs.length < 2) return 0;
  const mx = mean(xs), my = mean(ys);
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
const mse = (xs, ys) => mean(xs.map((x, i) => (x - ys[i]) ** 2));
const normalize01 = (xs) => {
  const lo = Math.min(...xs);
  const hi = Math.max(...xs);
  if (hi - lo < 1e-12) return xs.map(() => 0.5);
  return xs.map((x) => (x - lo) / (hi - lo));
};
const boundedInstitutionalDistortion = (p) => {
  const components = [p.bureaucraticDistortion, p.coalitionDistortion, p.lobbyingDistortion, p.beneficiaryDistance];
  return clamp(1 - components.reduce((acc, x) => acc * (1 - clamp(x)), 1));
};
const topMean = (plan, latent, share = 0.2) => {
  const n = Math.max(1, Math.round(plan.length * share));
  const top = Array.from({ length: plan.length }, (_, i) => i).sort((a, b) => plan[b] - plan[a]).slice(0, n);
  return mean(top.map((i) => latent[i]));
};
const priorityGap = (plan, latent, share = 0.2) => {
  const n = Math.max(1, Math.round(plan.length * share));
  const idx = Array.from({ length: plan.length }, (_, i) => i).sort((a, b) => plan[b] - plan[a]);
  const top = idx.slice(0, n);
  const bottom = idx.slice(-n);
  return mean(top.map((i) => latent[i])) - mean(bottom.map((i) => latent[i]));
};

const genPopulation = (rng, cfg) => {
  const citizens = [];
  for (let i = 0; i < cfg.citizens; i++) {
    citizens.push({
      group: Math.floor(rng() * cfg.groups),
      territory: Math.floor(rng() * cfg.territories),
    });
  }
  return citizens;
};

const genTargets = (rng, cfg) => {
  const targets = [];
  for (let j = 0; j < cfg.targets; j++) {
    const base = beta(rng, 2, 2);
    const beneficiaryGroup = Math.floor(rng() * cfg.groups);
    const territory = Math.floor(rng() * cfg.territories);
    const groupValues = [];
    const territoryValues = [];
    for (let g = 0; g < cfg.groups; g++) {
      groupValues.push(clamp(base + normal(rng, 0, cfg.preferencePolarization) + (g === beneficiaryGroup ? cfg.beneficiaryConcentration : 0)));
    }
    for (let t = 0; t < cfg.territories; t++) {
      territoryValues.push(clamp(base + normal(rng, 0, cfg.territorialHeterogeneity) + (t === territory ? 0.12 : 0)));
    }
    const salience = clamp(cfg.salienceCorrelation * base + (1 - cfg.salienceCorrelation) * rng());
    targets.push({ base, beneficiaryGroup, territory, groupValues, territoryValues, salience });
  }
  return targets;
};

const expectedValue = (citizen, target, rng, cfg, noisy = true) => {
  const x = 0.25 * target.base
    + 0.50 * target.groupValues[citizen.group]
    + 0.25 * target.territoryValues[citizen.territory]
    + (citizen.territory === target.territory ? 0.06 : 0)
    + (noisy ? normal(rng, 0, cfg.individualNoise) : 0);
  return clamp(x);
};

const genWorld = (seed, scenario) => {
  const rng = mulberry32(seed);
  const cfg = scenario.population;
  const citizens = genPopulation(rng, cfg);
  const targets = genTargets(rng, cfg);
  const T = cfg.targets;
  const N = cfg.citizens;
  const values = Array.from({ length: N }, () => new Float64Array(T));
  const latent = new Float64Array(T);
  const groupMeans = Array.from({ length: cfg.groups }, () => new Float64Array(T));
  const groupCounts = new Int32Array(cfg.groups);
  const territoryMeans = Array.from({ length: cfg.territories }, () => new Float64Array(T));
  const territoryCounts = new Int32Array(cfg.territories);

  for (let i = 0; i < N; i++) {
    const c = citizens[i];
    groupCounts[c.group]++;
    territoryCounts[c.territory]++;
    for (let j = 0; j < T; j++) {
      const v = expectedValue(c, targets[j], rng, cfg, true);
      values[i][j] = v;
      latent[j] += v;
      groupMeans[c.group][j] += v;
      territoryMeans[c.territory][j] += v;
    }
  }
  for (let j = 0; j < T; j++) latent[j] /= N;
  for (let g = 0; g < cfg.groups; g++) for (let j = 0; j < T; j++) groupMeans[g][j] /= Math.max(1, groupCounts[g]);
  for (let t = 0; t < cfg.territories; t++) for (let j = 0; j < T; j++) territoryMeans[t][j] /= Math.max(1, territoryCounts[t]);

  const salience = targets.map((t) => t.salience);
  return { seed, rng, citizens, targets, values, latent: Array.from(latent), groupMeans, territoryMeans, salience };
};

const vectorMean = (values, citizenIndexes, T) => {
  const out = new Array(T).fill(0);
  if (!citizenIndexes.length) return out.map(() => 0.5);
  for (const i of citizenIndexes) {
    const row = values[i];
    for (let j = 0; j < T; j++) out[j] += row[j];
  }
  return out.map((x) => x / citizenIndexes.length);
};

const compressAgenda = (vec, salience, rng, bandwidth = 0.25, offAgendaResponsiveness = 0.12) => {
  const T = vec.length;
  const k = Math.max(1, Math.min(T, Math.round(T * bandwidth)));
  const top = new Set(Array.from({ length: T }, (_, j) => j).sort((a, b) => vec[b] - vec[a]).slice(0, k));
  const out = vec.map((x, j) => {
    if (top.has(j)) return x;
    const lowInfoPrior = 0.50 * salience[j] + 0.50 * rng();
    return offAgendaResponsiveness * x + (1 - offAgendaResponsiveness) * lowInfoPrior;
  });
  return normalize01(out);
};

const buildCandidateVector = (world, rng) => {
  const { groupMeans, territoryMeans, targets } = world;
  const G = groupMeans.length;
  const R = territoryMeans.length;
  const T = targets.length;
  const coalitionGroups = new Set();
  const coalitionTerritories = new Set();
  const groupCount = Math.max(1, Math.round(0.30 * G));
  const territoryCount = Math.max(1, Math.round(0.20 * R));
  while (coalitionGroups.size < groupCount) coalitionGroups.add(Math.floor(rng() * G));
  while (coalitionTerritories.size < territoryCount) coalitionTerritories.add(Math.floor(rng() * R));
  const out = new Array(T).fill(0);
  let weight = 0;
  for (const g of coalitionGroups) { for (let j = 0; j < T; j++) out[j] += groupMeans[g][j]; weight++; }
  for (const t of coalitionTerritories) { for (let j = 0; j < T; j++) out[j] += territoryMeans[t][j]; weight++; }
  return normalize01(out.map((x) => x / Math.max(1, weight)));
};

const cosineLike = (a, b) => pearson(a, b);

const representativePlan = (world, rng, p, name) => {
  const T = world.targets.length;
  const N = world.citizens.length;
  const candidateVector = buildCandidateVector(world, rng);
  const alignments = [];
  for (let i = 0; i < N; i++) alignments.push({ i, score: cosineLike(Array.from(world.values[i]), candidateVector) + normal(rng, 0, 0.10) });
  alignments.sort((a, b) => b.score - a.score);
  const approvedN = Math.max(1, Math.min(N - 1, Math.round(p.approvalRate * N)));
  const supporters = alignments.slice(0, approvedN).map((x) => x.i);
  const nonSupporters = alignments.slice(approvedN).map((x) => x.i);

  const supporterVector = vectorMean(world.values, supporters, T);
  const nonSupporterVector = vectorMean(world.values, nonSupporters, T);
  const compressedSupporterVector = compressAgenda(supporterVector, world.salience, rng, p.agendaBandwidth, p.offAgendaResponsiveness);
  const compressedNonSupporterVector = compressAgenda(nonSupporterVector, world.salience, rng, Math.max(0.05, 0.5 * p.agendaBandwidth), 0.5 * p.offAgendaResponsiveness);
  const representativePreference = normalize01(compressedSupporterVector.map((x, j) =>
    p.supporterAlignment * p.approvalRate * x + p.nonSupporterAlignment * (1 - p.approvalRate) * compressedNonSupporterVector[j]
  ));

  const politicalDrift = normalize01(world.salience.map((s) => 0.65 * s + 0.35 * rng()));
  const programVector = normalize01(representativePreference.map((x, j) =>
    p.programFidelity * x + (1 - p.programFidelity) * politicalDrift[j]
  ));

  const distortion = boundedInstitutionalDistortion(p);
  const techNoise = Math.max(0.05, 0.40 * (1 - p.technocraticCapacity));
  const technocraticSignal = normalize01(world.latent.map((x) => clamp(x + normal(rng, 0, techNoise))));
  const organizedInterest = normalize01(world.salience.map((s, j) => 0.75 * s + 0.25 * politicalDrift[j]));
  const inertia = normalize01(world.salience.map((s) => 0.35 * s + 0.65 * rng()));
  const coalitionCompromise = normalize01(programVector.map((x, j) => 0.60 * x + 0.40 * candidateVector[j]));
  const remoteNoise = normalize01(Array.from({ length: T }, () => rng()));

  const weights = {
    program: Math.max(0.01, 1 - distortion),
    tech: p.technocraticCapacity,
    lobbying: p.lobbyingDistortion,
    bureaucratic: p.bureaucraticDistortion,
    coalition: p.coalitionDistortion,
    distance: p.beneficiaryDistance,
  };
  const denom = Object.values(weights).reduce((a, b) => a + b, 0);
  const plan = normalize01(programVector.map((_, j) => (
    weights.program * programVector[j]
    + weights.tech * technocraticSignal[j]
    + weights.lobbying * organizedInterest[j]
    + weights.bureaucratic * inertia[j]
    + weights.coalition * coalitionCompromise[j]
    + weights.distance * remoteNoise[j]
  ) / denom));

  return { name, class: "representative", plan, distortion, electoralMandateShare: p.turnoutRate * p.winnerVoteShare };
};

const maybeSignal = (rng, trueValue, coverage, noise) => rng() < coverage ? clamp(trueValue + normal(rng, 0, noise)) : null;
const distributedPlan = (world, rng, p, name) => {
  const T = world.targets.length;
  const raw = new Array(T).fill(0);
  for (let j = 0; j < T; j++) {
    const target = world.targets[j];
    const vals = [];
    const weights = [];
    const general = maybeSignal(rng, world.latent[j], p.generalSignalCoverage, p.generalSignalNoise);
    if (general !== null) { vals.push(general); weights.push(p.wGeneral); }
    const beneficiary = maybeSignal(rng, world.groupMeans[target.beneficiaryGroup][j], p.beneficiarySignalCoverage, p.beneficiarySignalNoise);
    if (beneficiary !== null) { vals.push(beneficiary); weights.push(p.wBeneficiary); }
    const affected = maybeSignal(rng, world.latent[j], p.affectedPartyCoverage, p.affectedPartySignalNoise);
    if (affected !== null) { vals.push(affected); weights.push(p.wAffected); }
    const local = maybeSignal(rng, world.territoryMeans[target.territory][j], p.localOrgCoverage, p.localOrgSignalNoise);
    if (local !== null) { vals.push(local); weights.push(p.wLocal); }
    const expert = maybeSignal(rng, world.latent[j], p.expertSignalCoverage, p.expertSignalNoise);
    if (expert !== null) { vals.push(expert); weights.push(p.wExpert); }
    const denom = weights.reduce((a, b) => a + b, 0);
    raw[j] = denom > 0 ? vals.reduce((a, v, k) => a + v * weights[k], 0) / denom : 0.5;
  }

  const participationBiased = raw.map((x, j) => (1 - p.participationBias) * x + p.participationBias * world.salience[j]);
  const manipulatedSet = new Set(
    Array.from({ length: T }, (_, j) => j)
      .sort((a, b) => (world.salience[b] * (1 - world.latent[b])) - (world.salience[a] * (1 - world.latent[a])))
      .slice(0, Math.max(0, Math.round(p.strategicSignalShare * T)))
  );
  const plan = normalize01(participationBiased.map((x, j) => {
    const salienceTerm = p.salienceBiasStrength * (1 - p.deliberationCorrectionStrength) * world.salience[j];
    const strategicTerm = manipulatedSet.has(j)
      ? p.manipulationIntensity * (1 - p.antiCaptureFilterStrength) * (1 - 0.5 * p.deliberationCorrectionStrength)
      : 0;
    return x + salienceTerm + strategicTerm;
  }));
  return { name, class: "distributed", plan, strategicTargets: manipulatedSet.size };
};

const measure = (world, result) => {
  const plan = result.plan;
  const latent = world.latent;
  return {
    name: result.name,
    class: result.class,
    corrWithLatent: pearson(plan, latent),
    mseToLatent: mse(plan, normalize01(latent)),
    top20LatentMean: topMean(plan, latent, 0.2),
    priorityGap: priorityGap(plan, latent, 0.2),
    salienceCorrWithLatent: pearson(world.salience, latent),
    electoralMandateShare: result.electoralMandateShare ?? null,
    distortion: result.distortion ?? null,
    strategicTargets: result.strategicTargets ?? null,
  };
};

const hashName = (name) => {
  let h = 2166136261;
  for (let i = 0; i < name.length; i++) {
    h ^= name.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
};

const runOnce = (seed, scenario) => {
  const world = genWorld(seed, scenario);
  const records = [];
  for (const [name, p] of Object.entries(scenario.representativeVariants ?? {})) {
    records.push(measure(world, representativePlan(world, mulberry32(seed ^ hashName(name)), p, name)));
  }
  for (const [name, p] of Object.entries(scenario.distributedVariants ?? {})) {
    records.push(measure(world, distributedPlan(world, mulberry32(seed ^ hashName(name)), p, name)));
  }
  const repPlans = {};
  const distPlans = {};
  for (const [name, p] of Object.entries(scenario.representativeVariants ?? {})) repPlans[name] = representativePlan(world, mulberry32(seed ^ hashName(`rep:${name}`)), p, name).plan;
  for (const [name, p] of Object.entries(scenario.distributedVariants ?? {})) distPlans[name] = distributedPlan(world, mulberry32(seed ^ hashName(`dist:${name}`)), p, name).plan;
  for (const [name, h] of Object.entries(scenario.hybridVariants ?? {})) {
    const c = repPlans[h.centralVariant];
    const d = distPlans[h.distributedVariant];
    if (!c || !d) continue;
    const plan = normalize01(c.map((x, j) => (1 - h.correctionWeight) * x + h.correctionWeight * d[j]));
    records.push(measure(world, { name, class: "hybrid", plan }));
  }
  records.push(measure(world, { name: "salience_vector", class: "salience", plan: normalize01(world.salience) }));
  return records;
};

const summarise = (rows, key) => ({ mean: mean(rows.map((r) => r[key])), sd: sd(rows.map((r) => r[key])) });
const summariseNullable = (rows, key) => {
  const xs = rows.map((r) => r[key]).filter((x) => x !== null && x !== undefined && Number.isFinite(x));
  return xs.length ? { mean: mean(xs), sd: sd(xs) } : { mean: null, sd: null };
};
const runScenario = (scenario) => {
  const raw = [];
  for (let r = 0; r < scenario.runs; r++) {
    const seed = scenario.seed + r * 7919;
    for (const rec of runOnce(seed, scenario)) raw.push({ scenario_id: scenario.scenario_id, run: r, seed, ...rec });
  }
  const keys = [...new Set(raw.map((r) => r.name))];
  const summary = keys.map((name) => {
    const rows = raw.filter((r) => r.name === name);
    return {
      name,
      class: rows[0]?.class,
      corrWithLatent: summarise(rows, "corrWithLatent"),
      mseToLatent: summarise(rows, "mseToLatent"),
      top20LatentMean: summarise(rows, "top20LatentMean"),
      priorityGap: summarise(rows, "priorityGap"),
      salienceCorrWithLatent: summarise(rows, "salienceCorrWithLatent"),
      electoralMandateShare: summariseNullable(rows, "electoralMandateShare"),
      distortion: summariseNullable(rows, "distortion"),
    };
  });
  return { raw, summary };
};
const fmt = (x, digits = 3) => x === null || x === undefined || !Number.isFinite(x) ? "" : x.toFixed(digits);
const fmtMean = (s) => s.mean === null ? "" : `${fmt(s.mean)}±${fmt(s.sd)}`;

const markdownTable = (summary) => {
  const lines = [];
  lines.push(`# Planning Vector Construction Results`);
  lines.push("");
  lines.push(`scenario: ${scenario.scenario_id} v${scenario.scenario_version}`);
  lines.push(`runs: ${scenario.runs}, base seed: ${scenario.seed}, citizens: ${scenario.population.citizens}, targets: ${scenario.population.targets}`);
  lines.push("");
  lines.push("| vector | class | corr(latent) | top20 latent mean | priority gap | MSE normalized | mandate share | distortion |");
  lines.push("|---|---|---:|---:|---:|---:|---:|---:|");
  for (const r of summary) {
    lines.push(`| ${r.name} | ${r.class} | ${fmtMean(r.corrWithLatent)} | ${fmtMean(r.top20LatentMean)} | ${fmtMean(r.priorityGap)} | ${fmtMean(r.mseToLatent)} | ${fmtMean(r.electoralMandateShare)} | ${fmtMean(r.distortion)} |`);
  }
  return lines.join("\n");
};
const csvTable = (summary) => {
  const fields = ["name","class","corr_mean","corr_sd","top20_mean","top20_sd","priority_gap_mean","priority_gap_sd","mse_mean","mse_sd","mandate_share_mean","mandate_share_sd","distortion_mean","distortion_sd"];
  const rows = [fields.join(",")];
  for (const r of summary) rows.push([
    r.name, r.class,
    r.corrWithLatent.mean, r.corrWithLatent.sd,
    r.top20LatentMean.mean, r.top20LatentMean.sd,
    r.priorityGap.mean, r.priorityGap.sd,
    r.mseToLatent.mean, r.mseToLatent.sd,
    r.electoralMandateShare.mean ?? "", r.electoralMandateShare.sd ?? "",
    r.distortion.mean ?? "", r.distortion.sd ?? "",
  ].map((x) => typeof x === "number" ? x.toFixed(8) : x).join(","));
  return rows.join("\n");
};

const writeOutputs = ({ raw, summary }) => {
  const outDir = resolve("experiments/planning-vector-construction/results", scenario.scenario_id);
  mkdirSync(outDir, { recursive: true });
  const base = `${scenario.scenario_id}-seed${scenario.seed}-runs${scenario.runs}`;
  if (scenario.outputs?.rawJson) writeFileSync(resolve(outDir, `${base}.raw.json`), JSON.stringify(raw, null, 2));
  if (scenario.outputs?.markdownTable) writeFileSync(resolve(outDir, `${base}.summary.md`), markdownTable(summary) + "\n");
  if (scenario.outputs?.csv) writeFileSync(resolve(outDir, `${base}.summary.csv`), csvTable(summary) + "\n");
  return outDir;
};

const result = runScenario(scenario);
console.log(markdownTable(result.summary));
const outDir = writeOutputs(result);
console.log(`\noutputs: ${outDir}`);
