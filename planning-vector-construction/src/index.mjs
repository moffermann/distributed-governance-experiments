#!/usr/bin/env node
// Planning Vector Construction Experiment
//
// Generates a synthetic population, latent social value over planning targets,
// representative central planning vectors, generic distributed vectors, and
// Core v0 planning vectors built from attentive participation, auditable
// delegation, and optional authority mandate effects.

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
const scenarioPath = resolve(cli.scenario ?? "experiments/planning-vector-construction/scenarios/core-v0-planning-channels.json");
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
  return clamp(1 - components.reduce((acc, x) => acc * (1 - clamp(x ?? 0)), 1));
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
const hashName = (name) => {
  let h = 2166136261;
  for (let i = 0; i < name.length; i++) { h ^= name.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
};

const genPopulation = (rng, cfg) => {
  const citizens = [];
  for (let i = 0; i < cfg.citizens; i++) citizens.push({
    group: Math.floor(rng() * cfg.groups),
    territory: Math.floor(rng() * cfg.territories),
  });
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
    for (let g = 0; g < cfg.groups; g++) groupValues.push(clamp(base + normal(rng, 0, cfg.preferencePolarization) + (g === beneficiaryGroup ? cfg.beneficiaryConcentration : 0)));
    for (let t = 0; t < cfg.territories; t++) territoryValues.push(clamp(base + normal(rng, 0, cfg.territorialHeterogeneity) + (t === territory ? 0.12 : 0)));
    const salience = clamp(cfg.salienceCorrelation * base + (1 - cfg.salienceCorrelation) * rng());
    targets.push({ base, beneficiaryGroup, territory, groupValues, territoryValues, salience });
  }
  return targets;
};
const expectedValue = (citizen, target, rng, cfg, noisy = true) => clamp(
  0.25 * target.base
  + 0.50 * target.groupValues[citizen.group]
  + 0.25 * target.territoryValues[citizen.territory]
  + (citizen.territory === target.territory ? 0.06 : 0)
  + (noisy ? normal(rng, 0, cfg.individualNoise) : 0)
);
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
  return { seed, citizens, targets, values, latent: Array.from(latent), groupMeans, territoryMeans, salience };
};

const vectorMean = (values, citizenIndexes, T) => {
  const out = new Array(T).fill(0);
  if (!citizenIndexes.length) return out.map(() => 0.5);
  for (const i of citizenIndexes) { const row = values[i]; for (let j = 0; j < T; j++) out[j] += row[j]; }
  return out.map((x) => x / citizenIndexes.length);
};
const compressAgenda = (vec, salience, rng, bandwidth = 0.25, offAgendaResponsiveness = 0.12) => {
  const T = vec.length;
  const k = Math.max(1, Math.min(T, Math.round(T * bandwidth)));
  const top = new Set(Array.from({ length: T }, (_, j) => j).sort((a, b) => vec[b] - vec[a]).slice(0, k));
  return normalize01(vec.map((x, j) => top.has(j) ? x : offAgendaResponsiveness * x + (1 - offAgendaResponsiveness) * (0.50 * salience[j] + 0.50 * rng())));
};
const buildCandidateVector = (world, rng) => {
  const { groupMeans, territoryMeans, targets } = world;
  const G = groupMeans.length, R = territoryMeans.length, T = targets.length;
  const groups = new Set(), territories = new Set();
  while (groups.size < Math.max(1, Math.round(0.30 * G))) groups.add(Math.floor(rng() * G));
  while (territories.size < Math.max(1, Math.round(0.20 * R))) territories.add(Math.floor(rng() * R));
  const out = new Array(T).fill(0);
  let weight = 0;
  for (const g of groups) { for (let j = 0; j < T; j++) out[j] += groupMeans[g][j]; weight++; }
  for (const t of territories) { for (let j = 0; j < T; j++) out[j] += territoryMeans[t][j]; weight++; }
  return normalize01(out.map((x) => x / Math.max(1, weight)));
};
const representativePlan = (world, rng, p, name) => {
  const T = world.targets.length, N = world.citizens.length;
  const candidateVector = buildCandidateVector(world, rng);
  const alignments = [];
  for (let i = 0; i < N; i++) alignments.push({ i, score: pearson(Array.from(world.values[i]), candidateVector) + normal(rng, 0, 0.10) });
  alignments.sort((a, b) => b.score - a.score);
  const approvedN = Math.max(1, Math.min(N - 1, Math.round(p.approvalRate * N)));
  const supporters = alignments.slice(0, approvedN).map((x) => x.i);
  const nonSupporters = alignments.slice(approvedN).map((x) => x.i);
  const supporterVector = compressAgenda(vectorMean(world.values, supporters, T), world.salience, rng, p.agendaBandwidth, p.offAgendaResponsiveness);
  const nonSupporterVector = compressAgenda(vectorMean(world.values, nonSupporters, T), world.salience, rng, Math.max(0.05, 0.5 * p.agendaBandwidth), 0.5 * p.offAgendaResponsiveness);
  const representativePreference = normalize01(supporterVector.map((x, j) => p.supporterAlignment * p.approvalRate * x + p.nonSupporterAlignment * (1 - p.approvalRate) * nonSupporterVector[j]));
  const politicalDrift = normalize01(world.salience.map((s) => 0.65 * s + 0.35 * rng()));
  const programVector = normalize01(representativePreference.map((x, j) => p.programFidelity * x + (1 - p.programFidelity) * politicalDrift[j]));
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
  const plan = normalize01(programVector.map((_, j) => (weights.program * programVector[j] + weights.tech * technocraticSignal[j] + weights.lobbying * organizedInterest[j] + weights.bureaucratic * inertia[j] + weights.coalition * coalitionCompromise[j] + weights.distance * remoteNoise[j]) / denom));
  return { name, class: "representative", plan, distortion, electoralMandateShare: p.turnoutRate * p.winnerVoteShare };
};

const maybeSignal = (rng, trueValue, coverage, noise) => rng() < coverage ? clamp(trueValue + normal(rng, 0, noise)) : null;
const distributedPlan = (world, rng, p, name) => {
  const T = world.targets.length;
  const raw = new Array(T).fill(0);
  for (let j = 0; j < T; j++) {
    const target = world.targets[j];
    const vals = [], weights = [];
    const add = (v, w) => { if (v !== null) { vals.push(v); weights.push(w); } };
    add(maybeSignal(rng, world.latent[j], p.generalSignalCoverage, p.generalSignalNoise), p.wGeneral);
    add(maybeSignal(rng, world.groupMeans[target.beneficiaryGroup][j], p.beneficiarySignalCoverage, p.beneficiarySignalNoise), p.wBeneficiary);
    add(maybeSignal(rng, world.latent[j], p.affectedPartyCoverage, p.affectedPartySignalNoise), p.wAffected);
    add(maybeSignal(rng, world.territoryMeans[target.territory][j], p.localOrgCoverage, p.localOrgSignalNoise), p.wLocal);
    add(maybeSignal(rng, world.latent[j], p.expertSignalCoverage, p.expertSignalNoise), p.wExpert);
    const denom = weights.reduce((a, b) => a + b, 0);
    raw[j] = denom > 0 ? vals.reduce((a, v, k) => a + v * weights[k], 0) / denom : 0.5;
  }
  const biased = raw.map((x, j) => (1 - p.participationBias) * x + p.participationBias * world.salience[j]);
  const manipulatedSet = new Set(Array.from({ length: T }, (_, j) => j).sort((a, b) => (world.salience[b] * (1 - world.latent[b])) - (world.salience[a] * (1 - world.latent[a]))).slice(0, Math.max(0, Math.round(p.strategicSignalShare * T))));
  const plan = normalize01(biased.map((x, j) => x + p.salienceBiasStrength * (1 - p.deliberationCorrectionStrength) * world.salience[j] + (manipulatedSet.has(j) ? p.manipulationIntensity * (1 - p.antiCaptureFilterStrength) * (1 - 0.5 * p.deliberationCorrectionStrength) : 0)));
  return { name, class: "generic_distributed", plan, strategicTargets: manipulatedSet.size };
};

const sampleIndexes = (rng, n, count) => {
  const out = [];
  for (let i = 0; i < count; i++) out.push(Math.floor(rng() * n));
  return out;
};
const weightedTargetPick = (rng, world, citizenIndex, salienceBias) => {
  const row = world.values[citizenIndex];
  let total = 0;
  const weights = Array.from({ length: world.targets.length }, (_, j) => {
    const w = Math.max(0.001, (1 - salienceBias) * row[j] + salienceBias * world.salience[j]);
    total += w;
    return w;
  });
  let roll = rng() * total;
  for (let j = 0; j < weights.length; j++) { roll -= weights[j]; if (roll <= 0) return j; }
  return weights.length - 1;
};
const attentiveSignal = (world, rng, p) => {
  const N = world.citizens.length, T = world.targets.length;
  const share = clamp((p.attentivePlanningShare ?? 0) + (p.mandatoryParticipationBoost ?? 0));
  const participants = sampleIndexes(rng, N, Math.max(0, Math.round(share * N)));
  const sums = new Array(T).fill(0), counts = new Array(T).fill(0);
  const sampleSize = p.attentiveSampleSize ?? 8;
  for (const i of participants) {
    const seen = new Set();
    for (let k = 0; k < sampleSize; k++) {
      const j = weightedTargetPick(rng, world, i, p.attentiveSalienceBias ?? 0.25);
      if (seen.has(j)) continue;
      seen.add(j);
      sums[j] += clamp(world.values[i][j] + normal(rng, 0, p.attentiveSignalNoise ?? 0.22));
      counts[j]++;
    }
  }
  const neutral = world.salience.map((s) => 0.35 * s + 0.65 * 0.5);
  return normalize01(sums.map((x, j) => counts[j] ? x / counts[j] : neutral[j]));
};
const delegateWeights = (count, concentration) => {
  const alpha = 0.05 + 2.5 * clamp(concentration);
  const raw = Array.from({ length: count }, (_, r) => 1 / Math.pow(r + 1, alpha));
  const total = raw.reduce((a, b) => a + b, 0);
  return raw.map((x) => x / total);
};
const effectiveDelegateQuality = (p) => clamp(
  (p.delegateInformationQuality ?? 0.65)
  * (0.5 + 0.5 * (p.delegateAuditability ?? 0.75))
  * (0.5 + 0.5 * (p.delegateRevocationResponsiveness ?? 0.70))
  * (0.5 + 0.5 * (p.delegateScopeGranularity ?? 0.70))
  * (1 - 0.5 * (p.delegateConcentration ?? 0.25))
  * (p.delegateAlignment ?? 0.75)
  * (0.5 + 0.5 * (p.delegateReportQuality ?? 0.75))
);
const delegateSignal = (world, rng, p) => {
  const T = world.targets.length;
  const D = Math.max(1, Math.round(p.delegateCount ?? 100));
  const weights = delegateWeights(D, p.delegateConcentration ?? 0.25);
  const q = effectiveDelegateQuality(p);
  const out = new Array(T).fill(0);
  for (let d = 0; d < D; d++) {
    const group = Math.floor(rng() * world.groupMeans.length);
    const territory = Math.floor(rng() * world.territoryMeans.length);
    const organizedBias = normalize01(world.salience.map((s) => 0.70 * s + 0.30 * rng()));
    for (let j = 0; j < T; j++) {
      const localValue = clamp(0.45 * world.groupMeans[group][j] + 0.35 * world.territoryMeans[territory][j] + 0.20 * world.latent[j]);
      const signal = clamp(q * localValue + (1 - q) * organizedBias[j] + normal(rng, 0, Math.max(0.03, 0.20 * (1 - q))));
      out[j] += weights[d] * signal;
    }
  }
  return normalize01(out);
};
const authorityMandateSignal = (world, rng, p) => {
  const quality = clamp(p.authorityScopeSignalQuality ?? 0);
  if ((p.mandateConstraintWeight ?? 0) <= 0) return new Array(world.targets.length).fill(0.5);
  return normalize01(world.latent.map((x, j) => clamp(quality * x + (1 - quality) * (0.5 * world.salience[j] + 0.5 * rng()))));
};
const coreV0PlanningVector = (world, rng, p, name) => {
  const att = attentiveSignal(world, mulberry32(rng() * 0xffffffff >>> 0), p);
  const del = delegateSignal(world, mulberry32(rng() * 0xffffffff >>> 0), p);
  const mandate = authorityMandateSignal(world, mulberry32(rng() * 0xffffffff >>> 0), p);
  const attWeight = Math.max(0.001, (p.attentivePlanningShare ?? 0) + (p.mandatoryParticipationBoost ?? 0));
  const delWeight = Math.max(0.001, ((p.delegatorShare ?? 0) + (p.mandatoryDelegationBoost ?? 0)) * (0.4 + 0.6 * effectiveDelegateQuality(p)));
  const mandateWeight = Math.max(0, p.mandateConstraintWeight ?? 0);
  const denom = attWeight + delWeight + mandateWeight;
  const plan = normalize01(att.map((_, j) => (attWeight * att[j] + delWeight * del[j] + mandateWeight * mandate[j]) / denom));
  return {
    name,
    class: "core_v0_planning",
    mode: p.mode,
    authorityMandateMode: p.authorityMandateMode,
    plan,
    attentivePlanningShare: p.attentivePlanningShare ?? 0,
    delegatorShare: p.delegatorShare ?? 0,
    delegateCount: p.delegateCount ?? null,
    delegateConcentration: p.delegateConcentration ?? null,
    effectiveDelegateQuality: effectiveDelegateQuality(p),
    mandateConstraintWeight: p.mandateConstraintWeight ?? 0,
  };
};

const measure = (world, result) => ({
  name: result.name,
  class: result.class,
  mode: result.mode ?? null,
  authorityMandateMode: result.authorityMandateMode ?? null,
  corrWithLatent: pearson(result.plan, world.latent),
  mseToLatent: mse(result.plan, normalize01(world.latent)),
  top20LatentMean: topMean(result.plan, world.latent, 0.2),
  priorityGap: priorityGap(result.plan, world.latent, 0.2),
  salienceCorrWithLatent: pearson(world.salience, world.latent),
  electoralMandateShare: result.electoralMandateShare ?? null,
  distortion: result.distortion ?? null,
  attentivePlanningShare: result.attentivePlanningShare ?? null,
  delegatorShare: result.delegatorShare ?? null,
  delegateCount: result.delegateCount ?? null,
  delegateConcentration: result.delegateConcentration ?? null,
  effectiveDelegateQuality: result.effectiveDelegateQuality ?? null,
  mandateConstraintWeight: result.mandateConstraintWeight ?? null,
});

const runOnce = (seed, scenario) => {
  const world = genWorld(seed, scenario);
  const records = [];
  for (const [name, p] of Object.entries(scenario.representativeVariants ?? {})) records.push(measure(world, representativePlan(world, mulberry32(seed ^ hashName(name)), p, name)));
  for (const [name, p] of Object.entries(scenario.distributedVariants ?? {})) records.push(measure(world, distributedPlan(world, mulberry32(seed ^ hashName(name)), p, name)));
  for (const [name, p] of Object.entries(scenario.coreV0PlanningVariants ?? {})) records.push(measure(world, coreV0PlanningVector(world, mulberry32(seed ^ hashName(name)), p, name)));
  records.push(measure(world, { name: "salience_vector", class: "salience", plan: normalize01(world.salience) }));
  return records;
};
const summarise = (rows, key) => ({ mean: mean(rows.map((r) => r[key])), sd: sd(rows.map((r) => r[key])) });
const summariseNullable = (rows, key) => {
  const xs = rows.map((r) => r[key]).filter((x) => x !== null && x !== undefined && Number.isFinite(x));
  return xs.length ? { mean: mean(xs), sd: sd(xs) } : { mean: null, sd: null };
};
const firstNonNull = (rows, key) => rows.map((r) => r[key]).find((x) => x !== null && x !== undefined) ?? "";
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
      mode: firstNonNull(rows, "mode"),
      authorityMandateMode: firstNonNull(rows, "authorityMandateMode"),
      corrWithLatent: summarise(rows, "corrWithLatent"),
      mseToLatent: summarise(rows, "mseToLatent"),
      top20LatentMean: summarise(rows, "top20LatentMean"),
      priorityGap: summarise(rows, "priorityGap"),
      salienceCorrWithLatent: summarise(rows, "salienceCorrWithLatent"),
      electoralMandateShare: summariseNullable(rows, "electoralMandateShare"),
      distortion: summariseNullable(rows, "distortion"),
      attentivePlanningShare: summariseNullable(rows, "attentivePlanningShare"),
      delegatorShare: summariseNullable(rows, "delegatorShare"),
      delegateCount: summariseNullable(rows, "delegateCount"),
      delegateConcentration: summariseNullable(rows, "delegateConcentration"),
      effectiveDelegateQuality: summariseNullable(rows, "effectiveDelegateQuality"),
      mandateConstraintWeight: summariseNullable(rows, "mandateConstraintWeight"),
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
  lines.push("| vector | class | mode | mandate | corr(latent) | top20 latent mean | priority gap | MSE normalized | attentive | delegator | delegates | concentration | delegate quality | mandate weight |");
  lines.push("|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|");
  for (const r of summary) lines.push(`| ${r.name} | ${r.class} | ${r.mode} | ${r.authorityMandateMode} | ${fmtMean(r.corrWithLatent)} | ${fmtMean(r.top20LatentMean)} | ${fmtMean(r.priorityGap)} | ${fmtMean(r.mseToLatent)} | ${fmtMean(r.attentivePlanningShare)} | ${fmtMean(r.delegatorShare)} | ${fmtMean(r.delegateCount)} | ${fmtMean(r.delegateConcentration)} | ${fmtMean(r.effectiveDelegateQuality)} | ${fmtMean(r.mandateConstraintWeight)} |`);
  return lines.join("\n");
};
const csvTable = (summary) => {
  const fields = ["name","class","mode","mandate","corr_mean","corr_sd","top20_mean","top20_sd","priority_gap_mean","priority_gap_sd","mse_mean","mse_sd","attentive_mean","delegator_mean","delegate_count_mean","delegate_concentration_mean","delegate_quality_mean","mandate_weight_mean","mandate_share_mean","distortion_mean"];
  const rows = [fields.join(",")];
  for (const r of summary) rows.push([
    r.name, r.class, r.mode, r.authorityMandateMode,
    r.corrWithLatent.mean, r.corrWithLatent.sd,
    r.top20LatentMean.mean, r.top20LatentMean.sd,
    r.priorityGap.mean, r.priorityGap.sd,
    r.mseToLatent.mean, r.mseToLatent.sd,
    r.attentivePlanningShare.mean ?? "", r.delegatorShare.mean ?? "", r.delegateCount.mean ?? "", r.delegateConcentration.mean ?? "", r.effectiveDelegateQuality.mean ?? "", r.mandateConstraintWeight.mean ?? "",
    r.electoralMandateShare.mean ?? "", r.distortion.mean ?? "",
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
