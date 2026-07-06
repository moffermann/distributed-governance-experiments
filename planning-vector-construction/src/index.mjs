#!/usr/bin/env node
// Planning Vector Construction Experiment
//
// Builds representative central planning vectors and Core v0 planning vectors.
// Core v0 planning is constructed from attentive citizens, delegated pluralism,
// delegate platform use, delegate planning coverage, and optional mandate effects.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const args = process.argv.slice(2);
const cli = {};
for (let i = 0; i < args.length; i++) {
  if (!args[i].startsWith("--")) continue;
  const key = args[i].slice(2);
  const next = args[i + 1];
  if (!next || next.startsWith("--")) cli[key] = true;
  else { cli[key] = next; i++; }
}

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
const gamma = (rng, shape) => {
  if (shape < 1) return gamma(rng, shape + 1) * Math.pow(rng(), 1 / shape);
  const d = shape - 1 / 3;
  const c = 1 / Math.sqrt(9 * d);
  while (true) {
    let x = normal(rng);
    let v = 1 + c * x;
    if (v <= 0) continue;
    v = v ** 3;
    const u = rng();
    if (u < 1 - 0.0331 * x ** 4) return d * v;
    if (Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return d * v;
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
const normalize01 = (xs) => {
  const lo = Math.min(...xs);
  const hi = Math.max(...xs);
  if (hi - lo < 1e-12) return xs.map(() => 0.5);
  return xs.map((x) => (x - lo) / (hi - lo));
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
const mse = (xs, ys) => {
  const nx = normalize01(xs);
  const ny = normalize01(ys);
  return mean(nx.map((x, i) => (x - ny[i]) ** 2));
};
const topMean = (plan, latent, share = 0.2) => {
  const n = Math.max(1, Math.round(plan.length * share));
  const top = Array.from({ length: plan.length }, (_, i) => i).sort((a, b) => plan[b] - plan[a]).slice(0, n);
  return mean(top.map((i) => latent[i]));
};
const priorityGap = (plan, latent, share = 0.2) => {
  const n = Math.max(1, Math.round(plan.length * share));
  const idx = Array.from({ length: plan.length }, (_, i) => i).sort((a, b) => plan[b] - plan[a]);
  return mean(idx.slice(0, n).map((i) => latent[i])) - mean(idx.slice(-n).map((i) => latent[i]));
};
const hashName = (name) => {
  let h = 2166136261;
  for (let i = 0; i < name.length; i++) { h ^= name.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
};
const boundedInstitutionalDistortion = (p) => {
  const c = [p.bureaucraticDistortion, p.coalitionDistortion, p.lobbyingDistortion, p.beneficiaryDistance];
  return clamp(1 - c.reduce((acc, x) => acc * (1 - clamp(x ?? 0)), 1));
};

const generateWorld = (seed, scenario) => {
  const rng = mulberry32(seed);
  const cfg = scenario.population;
  const N = cfg.citizens;
  const G = cfg.groups;
  const R = cfg.territories;
  const T = cfg.targets;
  const citizens = Array.from({ length: N }, () => ({ group: Math.floor(rng() * G), territory: Math.floor(rng() * R) }));
  const targets = [];
  for (let j = 0; j < T; j++) {
    const base = beta(rng, 2, 2);
    const beneficiaryGroup = Math.floor(rng() * G);
    const territory = Math.floor(rng() * R);
    const groupValues = Array.from({ length: G }, (_, g) => clamp(base + normal(rng, 0, cfg.preferencePolarization) + (g === beneficiaryGroup ? cfg.beneficiaryConcentration : 0)));
    const territoryValues = Array.from({ length: R }, (_, t) => clamp(base + normal(rng, 0, cfg.territorialHeterogeneity) + (t === territory ? 0.12 : 0)));
    const salience = clamp(cfg.salienceCorrelation * base + (1 - cfg.salienceCorrelation) * rng());
    targets.push({ base, beneficiaryGroup, territory, groupValues, territoryValues, salience });
  }
  const values = Array.from({ length: N }, () => new Float64Array(T));
  const latent = new Array(T).fill(0);
  const groupMeans = Array.from({ length: G }, () => new Array(T).fill(0));
  const territoryMeans = Array.from({ length: R }, () => new Array(T).fill(0));
  const groupCounts = new Array(G).fill(0);
  const territoryCounts = new Array(R).fill(0);
  for (let i = 0; i < N; i++) {
    const c = citizens[i];
    groupCounts[c.group]++;
    territoryCounts[c.territory]++;
    for (let j = 0; j < T; j++) {
      const target = targets[j];
      const v = clamp(
        0.25 * target.base
        + 0.50 * target.groupValues[c.group]
        + 0.25 * target.territoryValues[c.territory]
        + (c.territory === target.territory ? 0.06 : 0)
        + normal(rng, 0, cfg.individualNoise)
      );
      values[i][j] = v;
      latent[j] += v;
      groupMeans[c.group][j] += v;
      territoryMeans[c.territory][j] += v;
    }
  }
  for (let j = 0; j < T; j++) latent[j] /= N;
  for (let g = 0; g < G; g++) for (let j = 0; j < T; j++) groupMeans[g][j] /= Math.max(1, groupCounts[g]);
  for (let t = 0; t < R; t++) for (let j = 0; j < T; j++) territoryMeans[t][j] /= Math.max(1, territoryCounts[t]);
  const salience = targets.map((t) => t.salience);
  return { seed, citizens, targets, values, latent, groupMeans, territoryMeans, salience };
};

const vectorMean = (values, indexes, T) => {
  if (!indexes.length) return new Array(T).fill(0.5);
  const out = new Array(T).fill(0);
  for (const i of indexes) for (let j = 0; j < T; j++) out[j] += values[i][j];
  return out.map((x) => x / indexes.length);
};
const compressAgenda = (vec, salience, rng, bandwidth, offAgendaResponsiveness) => {
  const T = vec.length;
  const k = Math.max(1, Math.min(T, Math.round(T * bandwidth)));
  const top = new Set(Array.from({ length: T }, (_, j) => j).sort((a, b) => vec[b] - vec[a]).slice(0, k));
  return normalize01(vec.map((x, j) => top.has(j) ? x : offAgendaResponsiveness * x + (1 - offAgendaResponsiveness) * (0.5 * salience[j] + 0.5 * rng())));
};
const buildCandidateVector = (world, rng) => {
  const G = world.groupMeans.length;
  const R = world.territoryMeans.length;
  const T = world.targets.length;
  const groups = new Set();
  const territories = new Set();
  while (groups.size < Math.max(1, Math.round(0.30 * G))) groups.add(Math.floor(rng() * G));
  while (territories.size < Math.max(1, Math.round(0.20 * R))) territories.add(Math.floor(rng() * R));
  const out = new Array(T).fill(0);
  let n = 0;
  for (const g of groups) { for (let j = 0; j < T; j++) out[j] += world.groupMeans[g][j]; n++; }
  for (const t of territories) { for (let j = 0; j < T; j++) out[j] += world.territoryMeans[t][j]; n++; }
  return normalize01(out.map((x) => x / Math.max(1, n)));
};
const representativePlan = (world, rng, p, name) => {
  const T = world.targets.length;
  const N = world.citizens.length;
  const candidateVector = buildCandidateVector(world, rng);
  const scores = [];
  for (let i = 0; i < N; i++) scores.push({ i, score: pearson(Array.from(world.values[i]), candidateVector) + normal(rng, 0, 0.10) });
  scores.sort((a, b) => b.score - a.score);
  const approvedN = Math.max(1, Math.min(N - 1, Math.round(p.approvalRate * N)));
  const supporters = scores.slice(0, approvedN).map((x) => x.i);
  const nonSupporters = scores.slice(approvedN).map((x) => x.i);
  const supporterVector = compressAgenda(vectorMean(world.values, supporters, T), world.salience, rng, p.agendaBandwidth, p.offAgendaResponsiveness);
  const nonSupporterVector = compressAgenda(vectorMean(world.values, nonSupporters, T), world.salience, rng, Math.max(0.05, 0.5 * p.agendaBandwidth), 0.5 * p.offAgendaResponsiveness);
  const representativePreference = normalize01(supporterVector.map((x, j) => p.supporterAlignment * p.approvalRate * x + p.nonSupporterAlignment * (1 - p.approvalRate) * nonSupporterVector[j]));
  const politicalDrift = normalize01(world.salience.map((s) => 0.65 * s + 0.35 * rng()));
  const programVector = normalize01(representativePreference.map((x, j) => p.programFidelity * x + (1 - p.programFidelity) * politicalDrift[j]));
  const distortion = boundedInstitutionalDistortion(p);
  const technocraticSignal = normalize01(world.latent.map((x) => clamp(x + normal(rng, 0, Math.max(0.05, 0.40 * (1 - p.technocraticCapacity))))));
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
  const den = Object.values(weights).reduce((a, b) => a + b, 0);
  const plan = normalize01(programVector.map((_, j) => (
    weights.program * programVector[j]
    + weights.tech * technocraticSignal[j]
    + weights.lobbying * organizedInterest[j]
    + weights.bureaucratic * inertia[j]
    + weights.coalition * coalitionCompromise[j]
    + weights.distance * remoteNoise[j]
  ) / den));
  return { name, class: "representative", plan, distortion, electoralMandateShare: p.turnoutRate * p.winnerVoteShare };
};

const sampleIndexes = (rng, n, count) => Array.from({ length: count }, () => Math.floor(rng() * n));
const attentiveSignal = (world, rng, p) => {
  const N = world.citizens.length;
  const T = world.targets.length;
  const share = clamp((p.attentivePlanningShare ?? 0) + (p.mandatoryParticipationBoost ?? 0));
  const participants = sampleIndexes(rng, N, Math.round(share * N));
  const sums = new Array(T).fill(0);
  const counts = new Array(T).fill(0);
  const sampleSize = p.attentiveSampleSize ?? 8;
  const salienceBias = p.attentiveSalienceBias ?? 0.25;
  for (const i of participants) {
    const weights = Array.from({ length: T }, (_, j) => Math.max(0.001, (1 - salienceBias) * world.values[i][j] + salienceBias * world.salience[j]));
    const total = weights.reduce((a, b) => a + b, 0);
    const seen = new Set();
    for (let k = 0; k < sampleSize; k++) {
      let roll = rng() * total;
      let j = T - 1;
      for (let x = 0; x < T; x++) { roll -= weights[x]; if (roll <= 0) { j = x; break; } }
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
  const alpha = 0.10 + 0.85 * Math.pow(clamp(concentration), 1.2);
  const raw = Array.from({ length: count }, (_, i) => 1 / Math.pow(i + 1, alpha));
  const total = raw.reduce((a, b) => a + b, 0);
  return raw.map((x) => x / total);
};
const delegateWeightStats = (count, concentration) => {
  const w = delegateWeights(count, concentration).sort((a, b) => b - a);
  const sumTop = (n) => w.slice(0, Math.min(n, w.length)).reduce((a, b) => a + b, 0);
  return { top1: sumTop(1), top10: sumTop(10) };
};
const effectiveDelegateQuality = (p) => {
  const base =
    0.30 * (p.delegateInformationQuality ?? 0.65)
    + 0.25 * (p.delegateAlignment ?? 0.75)
    + 0.15 * (p.delegateAuditability ?? 0.75)
    + 0.12 * (p.delegateRevocationResponsiveness ?? 0.70)
    + 0.10 * (p.delegateScopeGranularity ?? 0.70)
    + 0.08 * (p.delegateReportQuality ?? 0.75);
  return clamp(base * (1 - 0.20 * (p.delegateConcentration ?? 0.25)));
};
const delegateSignal = (world, rng, p) => {
  const T = world.targets.length;
  const D = Math.max(1, Math.round(p.delegateCount ?? 100));
  const weights = delegateWeights(D, p.delegateConcentration ?? 0.25);
  const q = effectiveDelegateQuality(p);
  const platformUse = p.delegatePlatformUseRate ?? 0.75;
  const planningCoverage = p.delegatePlanningCoverage ?? 0.50;
  const out = new Array(T).fill(0);
  for (let d = 0; d < D; d++) {
    const active = rng() < platformUse;
    const coverage = active ? planningCoverage : Math.max(0.03, 0.25 * planningCoverage);
    const activeQ = active ? q : 0.45 * q;
    const group = Math.floor(rng() * world.groupMeans.length);
    const territory = Math.floor(rng() * world.territoryMeans.length);
    const localValue = world.latent.map((x, j) => clamp(0.45 * world.groupMeans[group][j] + 0.35 * world.territoryMeans[territory][j] + 0.20 * x));
    const organizedBias = normalize01(world.salience.map((s) => 0.70 * s + 0.30 * rng()));
    for (let j = 0; j < T; j++) {
      const reviewed = rng() < coverage;
      const activeSignal = clamp(activeQ * localValue[j] + (1 - activeQ) * organizedBias[j] + normal(rng, 0, Math.max(0.03, 0.20 * (1 - activeQ))));
      const staleSignal = clamp(0.35 * localValue[j] + 0.40 * world.salience[j] + 0.25 * rng() + normal(rng, 0, 0.12));
      out[j] += weights[d] * (reviewed ? activeSignal : staleSignal);
    }
  }
  return normalize01(out);
};
const authorityMandateSignal = (world, rng, p) => {
  if ((p.mandateConstraintWeight ?? 0) <= 0) return new Array(world.targets.length).fill(0.5);
  const quality = clamp(p.authorityScopeSignalQuality ?? 0);
  return normalize01(world.latent.map((x, j) => clamp(quality * x + (1 - quality) * (0.5 * world.salience[j] + 0.5 * rng()))));
};
const coreV0PlanningVector = (world, rng, p, name) => {
  const att = attentiveSignal(world, mulberry32((rng() * 0xffffffff) >>> 0), p);
  const del = delegateSignal(world, mulberry32((rng() * 0xffffffff) >>> 0), p);
  const mandate = authorityMandateSignal(world, mulberry32((rng() * 0xffffffff) >>> 0), p);
  const q = effectiveDelegateQuality(p);
  const attWeight = Math.max(0.001, (p.attentivePlanningShare ?? 0) + (p.mandatoryParticipationBoost ?? 0));
  const delWeight = Math.max(0.001, ((p.delegatorShare ?? 0) + (p.mandatoryDelegationBoost ?? 0)) * (0.55 + 0.45 * q));
  const mandateWeight = Math.max(0, p.mandateConstraintWeight ?? 0);
  const den = attWeight + delWeight + mandateWeight;
  const plan = normalize01(att.map((_, j) => (attWeight * att[j] + delWeight * del[j] + mandateWeight * mandate[j]) / den));
  const stats = delegateWeightStats(Math.max(1, Math.round(p.delegateCount ?? 100)), p.delegateConcentration ?? 0.25);
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
    effectiveDelegateQuality: q,
    delegatePlatformUseRate: p.delegatePlatformUseRate ?? null,
    delegatePlanningCoverage: p.delegatePlanningCoverage ?? null,
    delegateTop1Weight: stats.top1,
    delegateTop10Weight: stats.top10,
    mandateConstraintWeight: p.mandateConstraintWeight ?? 0,
  };
};
const measure = (world, result) => ({
  name: result.name,
  class: result.class,
  mode: result.mode ?? null,
  authorityMandateMode: result.authorityMandateMode ?? null,
  corrWithLatent: pearson(result.plan, world.latent),
  mseToLatent: mse(result.plan, world.latent),
  top20LatentMean: topMean(result.plan, world.latent),
  priorityGap: priorityGap(result.plan, world.latent),
  electoralMandateShare: result.electoralMandateShare ?? null,
  distortion: result.distortion ?? null,
  attentivePlanningShare: result.attentivePlanningShare ?? null,
  delegatorShare: result.delegatorShare ?? null,
  delegateCount: result.delegateCount ?? null,
  delegateConcentration: result.delegateConcentration ?? null,
  effectiveDelegateQuality: result.effectiveDelegateQuality ?? null,
  delegatePlatformUseRate: result.delegatePlatformUseRate ?? null,
  delegatePlanningCoverage: result.delegatePlanningCoverage ?? null,
  delegateTop1Weight: result.delegateTop1Weight ?? null,
  delegateTop10Weight: result.delegateTop10Weight ?? null,
});
const runOnce = (seed, scenario) => {
  const world = generateWorld(seed, scenario);
  const records = [];
  for (const [name, p] of Object.entries(scenario.representativeVariants ?? {})) records.push(measure(world, representativePlan(world, mulberry32(seed ^ hashName(name)), p, name)));
  for (const [name, p] of Object.entries(scenario.coreV0PlanningVariants ?? {})) records.push(measure(world, coreV0PlanningVector(world, mulberry32(seed ^ hashName(name)), p, name)));
  records.push(measure(world, { name: "salience_vector", class: "salience", plan: normalize01(world.salience) }));
  return records;
};
const summarize = (rows, key) => {
  const xs = rows.map((r) => r[key]).filter((x) => x !== null && x !== undefined && Number.isFinite(x));
  return xs.length ? { mean: mean(xs), sd: sd(xs) } : { mean: null, sd: null };
};
const runScenario = (scenario) => {
  const raw = [];
  for (let r = 0; r < scenario.runs; r++) {
    const seed = scenario.seed + r * 7919;
    for (const rec of runOnce(seed, scenario)) raw.push({ scenario_id: scenario.scenario_id, run: r, seed, ...rec });
  }
  const names = [...new Set(raw.map((r) => r.name))];
  const summary = names.map((name) => {
    const rows = raw.filter((r) => r.name === name);
    const first = rows[0];
    return {
      name,
      class: first.class,
      mode: first.mode ?? "",
      mandate: first.authorityMandateMode ?? "",
      corr: summarize(rows, "corrWithLatent"),
      top20: summarize(rows, "top20LatentMean"),
      gap: summarize(rows, "priorityGap"),
      mse: summarize(rows, "mseToLatent"),
      attentive: summarize(rows, "attentivePlanningShare"),
      delegator: summarize(rows, "delegatorShare"),
      delegates: summarize(rows, "delegateCount"),
      concentration: summarize(rows, "delegateConcentration"),
      quality: summarize(rows, "effectiveDelegateQuality"),
      platform: summarize(rows, "delegatePlatformUseRate"),
      coverage: summarize(rows, "delegatePlanningCoverage"),
      top1: summarize(rows, "delegateTop1Weight"),
      top10: summarize(rows, "delegateTop10Weight"),
      mandateShare: summarize(rows, "electoralMandateShare"),
      distortion: summarize(rows, "distortion"),
    };
  }).sort((a, b) => (b.corr.mean ?? -Infinity) - (a.corr.mean ?? -Infinity));
  return { raw, summary };
};
const fmt = (s) => s.mean === null ? "" : `${s.mean.toFixed(3)}±${s.sd.toFixed(3)}`;
const markdownTable = (summary) => {
  const lines = [];
  lines.push("# Planning Vector Construction Results");
  lines.push("");
  lines.push(`scenario: ${scenario.scenario_id} v${scenario.scenario_version}`);
  lines.push(`runs: ${scenario.runs}, base seed: ${scenario.seed}, citizens: ${scenario.population.citizens}, targets: ${scenario.population.targets}`);
  lines.push("");
  lines.push("| vector | class | mode | mandate | corr(latent) | top20 latent mean | priority gap | MSE | attentive | delegator | delegates | concentration | delegate quality | platform use | planning coverage | top1 delegate | top10 delegates |");
  lines.push("|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|");
  for (const r of summary) lines.push(`| ${r.name} | ${r.class} | ${r.mode} | ${r.mandate} | ${fmt(r.corr)} | ${fmt(r.top20)} | ${fmt(r.gap)} | ${fmt(r.mse)} | ${fmt(r.attentive)} | ${fmt(r.delegator)} | ${fmt(r.delegates)} | ${fmt(r.concentration)} | ${fmt(r.quality)} | ${fmt(r.platform)} | ${fmt(r.coverage)} | ${fmt(r.top1)} | ${fmt(r.top10)} |`);
  return lines.join("\n");
};
const csvTable = (summary) => {
  const fields = ["name","class","mode","mandate","corr_mean","corr_sd","top20_mean","top20_sd","gap_mean","gap_sd","mse_mean","mse_sd","attentive_mean","delegator_mean","delegates_mean","concentration_mean","quality_mean","platform_mean","coverage_mean","top1_mean","top10_mean","mandate_share_mean","distortion_mean"];
  const rows = [fields.join(",")];
  for (const r of summary) rows.push([
    r.name, r.class, r.mode, r.mandate,
    r.corr.mean, r.corr.sd, r.top20.mean, r.top20.sd, r.gap.mean, r.gap.sd, r.mse.mean, r.mse.sd,
    r.attentive.mean ?? "", r.delegator.mean ?? "", r.delegates.mean ?? "", r.concentration.mean ?? "", r.quality.mean ?? "", r.platform.mean ?? "", r.coverage.mean ?? "", r.top1.mean ?? "", r.top10.mean ?? "", r.mandateShare.mean ?? "", r.distortion.mean ?? "",
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
