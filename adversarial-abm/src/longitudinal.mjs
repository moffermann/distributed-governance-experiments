#!/usr/bin/env node
// Experiment E — longitudinal engine (v0.6). Pre-registered design:
// ../EXPERIMENT_E_LONGITUDINAL_DESIGN.md.
//
// Extends the audited static engine with the dynamics that make the freezing
// failure mode expressible: a budget-release layer (the authority's policy —
// previously hard-coded as uniform monthly), Poisson project arrivals, the
// docs/104 funding-window expiry valve, multi-cycle execution with milestone
// escrow, bounded verification capacity (the fiscalizer bottleneck), and an
// executor pool with compounding reputation (docs/107: informs, never
// excludes — selection weights, no removal).
//
// Deterrence formulas, allocation channels, and world-draw shapes mirror the
// static engine (imported constants and primitives keep one source of truth);
// the reputation-compounding terms are normalized so an executor at the
// initial reputation (0.5) faces exactly the static engine's inequality.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import {
  ARCHITECTURES, mulberry32, clamp, sigmoid, normal, sampleDist, weightedPick, drawSample,
} from "./index.mjs";

export const LONG_ENGINE_VERSION = "0.6.0";
const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const DEFAULTS = {
  years: 4,
  cyclesPerYear: 12,
  citizens: 2000,          // annual budget = 12 * citizens (1 unit/citizen/cycle on average)
  initialProjects: 12,
  arrivalRate: 2.0,        // Poisson mean per cycle; with meanTarget gives ~1.2x demand/budget
  meanTarget: 1200,        // project targets drawn (0.5+u)*meanTarget, as in the static engine
  fundingTTL: 6,           // docs/104 expiry valve: cycles a project may sit sub-threshold
  verifyCapacity: 6,       // milestone verifications per cycle (fiscalizer capacity)
  milestones: 3,
  durationMin: 3,
  durationMax: 9,
  executorsCount: 40,
  executorExitRate: 0.15,  // per year
  reputationGain: 0.05,    // per successfully verified project (scaled by quality)
  reputationPenalty: 0.30, // on detected diversion
  selectionReputationWeight: 1.0, // funder preference: weight = 0.25 + w*reputation
};

const loadPopulation = () => {
  const base = JSON.parse(readFileSync(resolve(HERE, "../scenarios/behavioral-llm-calibrated.json"), "utf8"));
  return { population: base.population, projects: base.projects, executors: base.executors };
};

// ---------------------------------------------------------------------------
// Release policies. Each returns the amount to release this cycle.
// state exposes: treasury, releasedPool, frozenTotal(), activatedFundingPrev.
// ---------------------------------------------------------------------------

const POLICIES = {
  // P0: the whole year's budget on the year's first cycle.
  day_zero: () => (state, cfg) => (state.cycleOfYear === 0 ? state.treasury : 0),
  // P1: equal monthly tranches (the static engine's implicit behavior).
  uniform: () => (state, cfg) => Math.min(state.treasury, cfg.annualBudget / cfg.cyclesPerYear),
  // P2: geometric front-load within the year, decay parameter lambda.
  front_loaded: (lambda) => {
    return (state, cfg) => {
      const k = state.cycleOfYear;
      const weights = [];
      for (let i = 0; i < cfg.cyclesPerYear; i++) weights.push(Math.exp(-i / lambda));
      const total = weights.reduce((a, b) => a + b, 0);
      return Math.min(state.treasury, cfg.annualBudget * (weights[k] / total));
    };
  },
  // P3: pull (CONWIP): release only what keeps frozen capital at or below W.
  pull: (wipCapMonths) => (state, cfg) => {
    const cap = wipCapMonths * (cfg.annualBudget / cfg.cyclesPerYear);
    return clamp(cap - state.frozenTotal(), 0, state.treasury);
  },
  // P4: approval-conditioned commitment (the author's term — never "leverage"):
  // release follows the previous cycle's effective activations, with a small
  // bootstrap floor so the loop can start.
  approval_conditioned: (alpha) => (state, cfg) => {
    const floor = cfg.annualBudget / (2 * cfg.cyclesPerYear);
    return clamp(Math.max(floor, alpha * state.activatedFundingPrev), 0, state.treasury);
  },
};

// ---------------------------------------------------------------------------
// World pieces
// ---------------------------------------------------------------------------

const poisson = (rng, lambda) => {
  const L = Math.exp(-lambda);
  let k = 0, p = 1;
  do { k++; p *= rng(); } while (p > L);
  return k - 1;
};

let projectSeq = 0;
const makeLongProject = (rng, cfg, cycle) => {
  const pCfg = cfg.projects;
  const latentValue = sampleDist(rng, pCfg.latentValue);
  const salience = clamp(pCfg.salienceCorrelation * latentValue + (1 - pCfg.salienceCorrelation) * rng(), 0.01, 0.99);
  const centralMix = pCfg.centralPlanningSignalMix ?? 0.15;
  const distributedMix = pCfg.distributedPlanningSignalMix ?? 0.70;
  return {
    id: `L-${String(++projectSeq).padStart(4, "0")}`,
    latentValue,
    salience,
    centralPlanningWeight: clamp(centralMix * latentValue + (1 - centralMix) * rng(), 0.01, 0.99),
    distributedPlanningWeight: clamp(distributedMix * latentValue + (1 - distributedMix) * rng(), 0.01, 0.99),
    verificationDifficulty: sampleDist(rng, pCfg.verificationDifficulty),
    executionDifficulty: sampleDist(rng, pCfg.executionDifficulty),
    fraudOpportunity: sampleDist(rng, pCfg.fraudOpportunity),
    budgetTarget: (0.5 + rng()) * cfg.meanTarget,
    arrivalCycle: cycle,
    status: "funding", // funding -> active -> done | expired | terminated
    funded: 0,
    escrow: 0,
    paidOut: 0,
    executor: null,
    duration: 0,
    milestoneCycles: [],
    milestonesDone: 0,
    milestonesVerified: 0,
    activationCycle: null,
    finishedCycle: null,
    // execution outcome (drawn at activation, mirroring the static engine)
    diverted: false,
    diversionShare: 0,
    executionQuality: 1,
    detectedAt: null,
    verifiedValue: 0,
    actualValue: 0,
    leakage: 0,
  };
};

const makeExecutor = (rng, cfg, id) => ({
  id,
  type: rng() < cfg.executors.opportunisticShare ? "opportunistic" : "honest",
  ability: sampleDist(rng, cfg.executors.ability),
  reputation: 0.5,
  tenureProjects: 0,
  active: true,
});

// ---------------------------------------------------------------------------
// Allocation (mirrors the static engine's channels, operating on the released
// pool instead of a fixed per-cycle citizen count; leftovers return to the
// pool — unallocated money is NOT frozen, committed money is).
// ---------------------------------------------------------------------------

const fundingProjects = (state) => state.projects.filter((p) => p.status === "funding");
const fundingProgress = (p) => Math.max(0, p.funded / Math.max(1, p.budgetTarget));

const contribute = (p, amount) => {
  const room = Math.max(0, p.budgetTarget - p.funded);
  const paid = Math.min(room, amount);
  p.funded += paid;
  return amount - paid;
};

const allocateInformedUnits = (rng, state, arch, cfg, units, { noiseScale = 1.0, nearCompletionBonus = 0.0, unitsPerActor = 1 } = {}) => {
  const sampleSize = cfg.population.attentiveSampleSize ?? 8;
  let leftover = 0;
  const actors = Math.floor(units / unitsPerActor);
  for (let i = 0; i < actors; i++) {
    const open = fundingProjects(state);
    if (!open.length) return leftover + (actors - i) * unitsPerActor;
    const sample = drawSample(rng, open, sampleSize);
    const scored = sample.map((p) => ({
      p,
      utility: p.latentValue
        + normal(rng, 0, arch.informationNoise * noiseScale)
        + nearCompletionBonus * fundingProgress(p)
        - 0.15 * p.verificationDifficulty,
    })).sort((a, b) => b.utility - a.utility);
    let amount = unitsPerActor;
    for (const { p } of scored) {
      amount = contribute(p, amount);
      if (amount <= 0) break;
    }
    leftover += amount;
  }
  return leftover + (units - actors * unitsPerActor);
};

const allocateSalienceUnits = (rng, state, arch, cfg, units) => {
  const slots = 6;
  let leftover = 0;
  const visibility = (p) => p.salience * (1 + arch.socialProofDamping * fundingProgress(p));
  for (let i = 0; i < units; i++) {
    const open = fundingProjects(state);
    if (!open.length) return leftover + (units - i);
    let amount = 1;
    const top = [...open].sort((a, b) => visibility(b) - visibility(a)).slice(0, slots);
    for (let attempts = 0; attempts < Math.min(4, top.length) && amount > 0; attempts++) {
      amount = contribute(weightedPick(rng, top, visibility), amount);
    }
    leftover += amount;
  }
  return leftover;
};

const allocateDefaultUnits = (state, arch, amount) => {
  const score = (p) => (arch.planningSource === "distributed" ? p.distributedPlanningWeight : p.centralPlanningWeight);
  const open = fundingProjects(state).sort((a, b) => score(b) - score(a));
  let budget = amount;
  for (const p of open) {
    if (budget <= 0) break;
    budget = contribute(p, budget);
  }
  return budget;
};

const allocateCycle = (rng, state, arch, cfg) => {
  const pool = Math.floor(state.releasedPool);
  if (pool <= 0) return;
  let leftover = 0;
  if (arch.centralPlanner) {
    leftover = allocateDefaultUnits(state, arch, pool);
  } else {
    const pop = cfg.population;
    const hasDefaultLayer = arch.passiveAllocationMode === "planning";
    const attentive = Math.round(pool * pop.attentiveShare);
    const salience = Math.round(pool * pop.salienceShare);
    const profile = hasDefaultLayer ? Math.round(pool * (pop.profileShare ?? 0)) : 0;
    const delegated = hasDefaultLayer ? Math.round(pool * (pop.delegatorShare ?? 0)) : 0;
    const remaining = pool - attentive - salience - profile - delegated;
    let lo = 0;
    lo += allocateInformedUnits(rng, state, arch, cfg, attentive);
    lo += allocateSalienceUnits(rng, state, arch, cfg, salience);
    if (profile > 0) lo += allocateInformedUnits(rng, state, arch, cfg, profile, { noiseScale: 1.5, nearCompletionBonus: 0.20 });
    if (delegated > 0) {
      const blockSize = Math.max(1, Math.round(pop.delegationBlockSize ?? 3));
      lo += allocateInformedUnits(rng, state, arch, cfg, delegated, { unitsPerActor: blockSize });
    }
    if (hasDefaultLayer) leftover = allocateDefaultUnits(state, arch, remaining + lo);
    else leftover = remaining + lo; // no default layer: passive money stays unallocated
  }
  state.releasedPool = state.releasedPool - pool + leftover;
};

// ---------------------------------------------------------------------------
// Activation, execution, verification
// ---------------------------------------------------------------------------

const detectionProbability = (p, arch) => clamp(arch.detectionBase * (1 - 0.55 * p.verificationDifficulty), 0.01, 0.98);

const activateReady = (rng, state, arch, cfg, cycle) => {
  let activated = 0;
  for (const p of fundingProjects(state)) {
    if (p.funded < p.budgetTarget) continue;
    p.status = "active";
    p.activationCycle = cycle;
    p.escrow = p.funded;
    activated += p.funded;
    // Executor selection: reputation informs (weights), never excludes.
    const pool = state.executors.filter((e) => e.active);
    p.executor = arch.futureSelectionLoss > 0.05
      ? weightedPick(rng, pool, (e) => 0.25 + cfg.selectionReputationWeight * e.reputation)
      : pool[Math.floor(rng() * pool.length)];
    p.executor.tenureProjects++;
    p.duration = cfg.durationMin + Math.floor(rng() * (cfg.durationMax - cfg.durationMin + 1));
    p.milestoneCycles = [];
    for (let m = 1; m <= cfg.milestones; m++) p.milestoneCycles.push(cycle + Math.ceil((p.duration * m) / cfg.milestones));
    // Diversion/quality decision at activation (static engine's formulas; the
    // reputation terms scale with the executor's stake, normalized to 1 at the
    // initial reputation 0.5 so t=0 matches the static inequality).
    const ex = p.executor;
    const stakeScale = ex.reputation / 0.5;
    if (ex.type === "opportunistic") {
      const fraudGain = p.fraudOpportunity * (1 - arch.retention);
      const x = -1.0
        + 4.0 * fraudGain
        + 2.0 * p.verificationDifficulty
        - 5.0 * detectionProbability(p, arch)
        - 3.0 * arch.retention
        - 2.0 * arch.guarantee
        - 3.0 * arch.reputationLoss * stakeScale
        - 2.0 * arch.futureSelectionLoss * stakeScale;
      p.diverted = rng() < sigmoid(x);
      if (p.diverted) {
        p.diversionShare = clamp(0.20 + 0.60 * p.fraudOpportunity + normal(rng, 0, 0.05), 0.05, 0.95);
        p.executionQuality = clamp((1 - p.diversionShare) * (0.55 + 0.45 * ex.ability), 0.02, 1);
      } else {
        p.executionQuality = clamp(0.70 + 0.30 * ex.ability - 0.20 * p.executionDifficulty, 0.20, 1);
      }
    } else {
      const good = rng() < sigmoid(1.5 + 2.5 * ex.ability - 3.0 * p.executionDifficulty);
      p.executionQuality = good
        ? clamp(0.75 + 0.25 * ex.ability, 0.30, 1)
        : clamp(0.35 + 0.35 * ex.ability - 0.20 * p.executionDifficulty, 0.05, 0.85);
    }
  }
  return activated;
};

const progressExecution = (state, cycle) => {
  for (const p of state.projects) {
    if (p.status !== "active") continue;
    while (p.milestonesDone < p.milestoneCycles.length && p.milestoneCycles[p.milestonesDone] <= cycle) {
      p.milestonesDone++;
      state.verifyQueue.push({ p, milestone: p.milestonesDone, completedCycle: cycle });
    }
  }
};

const verifyCycle = (rng, state, arch, cfg, cycle) => {
  let capacity = cfg.verifyCapacity;
  while (capacity > 0 && state.verifyQueue.length) {
    const { p, milestone } = state.verifyQueue.shift();
    capacity--;
    if (p.status !== "active") continue; // terminated while queued
    const M = cfg.milestones;
    const tranche = p.budgetTarget / M;
    const potentialValue = p.budgetTarget * p.latentValue;
    if (p.diverted && p.detectedAt === null && rng() < detectionProbability(p, arch)) {
      // Milestone gating does its job: detection stops the remaining tranches.
      p.detectedAt = cycle;
      p.status = "terminated";
      p.finishedCycle = cycle;
      p.leakage = p.diversionShare * p.paidOut + p.diversionShare * tranche; // taken from paid + current tranche
      const recovered = Math.max(0, p.escrow - tranche) + arch.guarantee * p.budgetTarget;
      state.releasedPool += recovered;             // unpaid escrow + guarantee recycle
      state.recoveredTotal += recovered;
      p.escrow = 0;
      p.executor.reputation = clamp(p.executor.reputation - cfg.reputationPenalty, 0, 1);
      state.detections++;
      continue;
    }
    // Verified milestone: tranche disburses; value accrues.
    const reviewConfidence = clamp(arch.reviewConfidence * (1 - 0.35 * p.verificationDifficulty), 0.05, 1);
    p.escrow -= tranche;
    p.paidOut += tranche;
    p.actualValue += (potentialValue * p.executionQuality) / M;
    p.verifiedValue += (potentialValue * p.executionQuality * reviewConfidence) / M;
    p.milestonesVerified++;
    if (p.milestonesVerified >= M) {
      p.status = "done";
      p.finishedCycle = cycle;
      if (p.diverted) p.leakage = p.diversionShare * p.budgetTarget; // never caught
      state.releasedPool += Math.max(0, p.escrow); // rounding residue recycles
      p.escrow = 0;
      p.executor.reputation = clamp(p.executor.reputation + cfg.reputationGain * p.executionQuality, 0, 1);
    }
  }
};

const expireStale = (state, cfg, cycle) => {
  for (const p of fundingProjects(state)) {
    if (cycle - p.arrivalCycle > cfg.fundingTTL) {
      p.status = "expired";
      state.releasedPool += p.funded;   // docs/104: commitments return
      state.expiredDemand += p.budgetTarget;
      state.expiredCount++;
      p.funded = 0;
    }
  }
};

const turnoverExecutors = (rng, state, cfg) => {
  for (const e of state.executors) {
    if (e.active && rng() < cfg.executorExitRate) {
      e.active = false;
      state.executors.push(makeExecutor(rng, cfg, `E-${state.executors.length + 1}`));
    }
  }
};

// ---------------------------------------------------------------------------
// One run
// ---------------------------------------------------------------------------

export const runLongitudinal = (archId, policyFn, cfg, seed) => {
  const rng = mulberry32(seed >>> 0);
  projectSeq = 0;
  const arch = ARCHITECTURES[archId];
  const cycles = cfg.years * cfg.cyclesPerYear;
  const state = {
    projects: [],
    executors: [],
    verifyQueue: [],
    treasury: 0,
    releasedPool: 0,
    releasedCum: 0,
    activatedFundingPrev: 0,
    expiredDemand: 0,
    expiredCount: 0,
    detections: 0,
    recoveredTotal: 0,
    cycleOfYear: 0,
    frozenTotal() {
      let f = 0;
      for (const p of this.projects) {
        if (p.status === "funding") f += p.funded;
        else if (p.status === "active") f += p.escrow;
      }
      return f;
    },
  };
  for (let i = 0; i < cfg.executorsCount; i++) state.executors.push(makeExecutor(rng, cfg, `E-${i + 1}`));
  for (let i = 0; i < cfg.initialProjects; i++) state.projects.push(makeLongProject(rng, cfg, 0));

  const series = { frozenSub: [], frozenWip: [], queue: [], released: [] };
  for (let cycle = 0; cycle < cycles; cycle++) {
    state.cycleOfYear = cycle % cfg.cyclesPerYear;
    if (state.cycleOfYear === 0) {
      state.treasury += cfg.annualBudget;
      turnoverExecutors(rng, state, cfg);
    }
    const arrivals = poisson(rng, cfg.arrivalRate);
    for (let i = 0; i < arrivals; i++) state.projects.push(makeLongProject(rng, cfg, cycle));
    expireStale(state, cfg, cycle);
    const release = Math.min(state.treasury, Math.max(0, policyFn(state, cfg)));
    state.treasury -= release;
    state.releasedPool += release;
    state.releasedCum += release;
    allocateCycle(rng, state, arch, cfg);
    state.activatedFundingPrev = activateReady(rng, state, arch, cfg, cycle);
    progressExecution(state, cycle);
    verifyCycle(rng, state, arch, cfg, cycle);
    let sub = 0, wip = 0;
    for (const p of state.projects) {
      if (p.status === "funding") sub += p.funded;
      else if (p.status === "active") wip += p.escrow;
    }
    series.frozenSub.push(sub);
    series.frozenWip.push(wip);
    series.queue.push(state.verifyQueue.length);
    series.released.push(state.releasedCum);
  }

  const done = state.projects.filter((p) => p.status === "done" || p.status === "terminated");
  const verifiedValue = state.projects.reduce((a, p) => a + p.verifiedValue, 0);
  const leakage = state.projects.reduce((a, p) => a + p.leakage, 0);
  const paidOut = state.projects.reduce((a, p) => a + p.paidOut, 0);
  const latencies = done.filter((p) => p.finishedCycle !== null).map((p) => p.finishedCycle - p.arrivalCycle);
  const totalBudget = cfg.annualBudget * cfg.years;
  const meanFrozenRatio = series.frozenSub.reduce((a, b, i) => a + (b + series.frozenWip[i]) / Math.max(1, series.released[i]), 0) / cycles;
  return {
    verifiedValuePerBudgetYear: verifiedValue / totalBudget,
    verifiedValuePerPaid: verifiedValue / Math.max(1, paidOut),
    leakageRate: leakage / Math.max(1, paidOut),
    meanFrozenRatio,
    endFrozen: (series.frozenSub.at(-1) + series.frozenWip.at(-1)) / Math.max(1, state.releasedCum),
    meanFrozenSub: series.frozenSub.reduce((a, b) => a + b, 0) / cycles / (cfg.annualBudget / cfg.cyclesPerYear),
    meanFrozenWip: series.frozenWip.reduce((a, b) => a + b, 0) / cycles / (cfg.annualBudget / cfg.cyclesPerYear),
    meanQueue: series.queue.reduce((a, b) => a + b, 0) / cycles,
    meanLatency: latencies.length ? latencies.reduce((a, b) => a + b, 0) / latencies.length : 0,
    delivered: done.filter((p) => p.status === "done").length,
    terminated: state.projects.filter((p) => p.status === "terminated").length,
    expired: state.expiredCount,
    expiredDemandRatio: state.expiredDemand / Math.max(1, totalBudget),
    detections: state.detections,
    unreleasedEnd: state.treasury / totalBudget,
  };
};

export { POLICIES, DEFAULTS, loadPopulation };

export const runCell = (archId, policyFn, cfg, runs, baseSeed) => {
  const acc = {};
  for (let r = 0; r < runs; r++) {
    const m = runLongitudinal(archId, policyFn, cfg, (baseSeed + r * 7919) >>> 0);
    for (const [k, v] of Object.entries(m)) (acc[k] ??= []).push(v);
  }
  const out = {};
  for (const [k, arr] of Object.entries(acc)) {
    const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
    const sd = Math.sqrt(arr.reduce((a, b) => a + (b - mean) ** 2, 0) / arr.length);
    out[k] = { mean, sd };
  }
  return out;
};

// ---------------------------------------------------------------------------
// E-1a runner: policy grid + refinement + Pareto frontier
// ---------------------------------------------------------------------------

const isMain = process.argv[1] && resolve(process.argv[1]) === resolve(HERE, "longitudinal.mjs");
if (isMain) {
  const shared = loadPopulation();
  const cfg = {
    ...DEFAULTS,
    ...shared,
    annualBudget: DEFAULTS.cyclesPerYear * DEFAULTS.citizens,
  };
  const RUNS = 20;
  const SEED = 1;
  const CORE = "core_v0_tutored_distributed_agenda";
  const SQ = "status_quo";

  const grid = [
    { family: "P0 day_zero", param: "", fn: POLICIES.day_zero() },
    { family: "P1 uniform", param: "", fn: POLICIES.uniform() },
    { family: "P2 front_loaded", param: "lambda=2", fn: POLICIES.front_loaded(2) },
    { family: "P2 front_loaded", param: "lambda=4", fn: POLICIES.front_loaded(4) },
    { family: "P2 front_loaded", param: "lambda=6", fn: POLICIES.front_loaded(6) },
    { family: "P3 pull", param: "W=2mo", fn: POLICIES.pull(2) },
    { family: "P3 pull", param: "W=4mo", fn: POLICIES.pull(4) },
    { family: "P3 pull", param: "W=6mo", fn: POLICIES.pull(6) },
    { family: "P3 pull", param: "W=8mo", fn: POLICIES.pull(8) },
    { family: "P4 approval_conditioned", param: "alpha=0.8", fn: POLICIES.approval_conditioned(0.8) },
    { family: "P4 approval_conditioned", param: "alpha=1.0", fn: POLICIES.approval_conditioned(1.0) },
    { family: "P4 approval_conditioned", param: "alpha=1.2", fn: POLICIES.approval_conditioned(1.2) },
    { family: "P4 approval_conditioned", param: "alpha=1.5", fn: POLICIES.approval_conditioned(1.5) },
  ];

  const rows = [];
  for (const cell of grid) {
    const core = runCell(CORE, cell.fn, cfg, RUNS, SEED);
    const sq = runCell(SQ, cell.fn, cfg, RUNS, SEED);
    rows.push({ ...cell, core, sq });
    console.error(`done: ${cell.family} ${cell.param}`);
  }

  // Refinement: golden-section-ish sweep on the best pull W and best alpha.
  const V = (r) => r.core.verifiedValuePerBudgetYear.mean;
  const bestPull = rows.filter((r) => r.family === "P3 pull").sort((a, b) => V(b) - V(a))[0];
  const bestW = Number(bestPull.param.slice(2, -2));
  const refineW = [bestW - 1, bestW - 0.5, bestW + 0.5, bestW + 1].filter((w) => w >= 0.5);
  for (const w of refineW) {
    const fn = POLICIES.pull(w);
    rows.push({ family: "P3 pull (refine)", param: `W=${w}mo`, fn, core: runCell(CORE, fn, cfg, RUNS, SEED), sq: runCell(SQ, fn, cfg, RUNS, SEED) });
    console.error(`done refine: W=${w}`);
  }
  const bestAlphaRow = rows.filter((r) => r.family === "P4 approval_conditioned").sort((a, b) => V(b) - V(a))[0];
  const bestAlpha = Number(bestAlphaRow.param.slice(6));
  for (const a of [bestAlpha - 0.1, bestAlpha + 0.1].filter((a) => a >= 0.5)) {
    const fn = POLICIES.approval_conditioned(a);
    rows.push({ family: "P4 approval_conditioned (refine)", param: `alpha=${a.toFixed(1)}`, fn, core: runCell(CORE, fn, cfg, RUNS, SEED), sq: runCell(SQ, fn, cfg, RUNS, SEED) });
    console.error(`done refine: alpha=${a.toFixed(1)}`);
  }

  // Pareto frontier over (maximize V, minimize meanFrozenRatio, minimize latency), core arm.
  const dominated = (a, b) => // b dominates a
    V(b) >= V(a) && b.core.meanFrozenRatio.mean <= a.core.meanFrozenRatio.mean && b.core.meanLatency.mean <= a.core.meanLatency.mean
    && (V(b) > V(a) || b.core.meanFrozenRatio.mean < a.core.meanFrozenRatio.mean || b.core.meanLatency.mean < a.core.meanLatency.mean);
  const pareto = rows.filter((a) => !rows.some((b) => b !== a && dominated(a, b)));

  const f = (x, d = 3) => x.toFixed(d);
  const lines = [];
  lines.push(`# Experiment E-1a: budget-release policies (longitudinal engine v${LONG_ENGINE_VERSION})`);
  lines.push(``);
  lines.push(`config: ${cfg.years}y x ${cfg.cyclesPerYear} cycles, citizens ${cfg.citizens}, annual budget ${cfg.annualBudget}, arrivals ${cfg.arrivalRate}/cycle, mean target ${cfg.meanTarget}, TTL ${cfg.fundingTTL}, verify capacity ${cfg.verifyCapacity}/cycle, milestones ${cfg.milestones}, runs ${RUNS}, seed ${SEED}`);
  lines.push(``);
  lines.push(`## Core v0 tutored-distributed arm`);
  lines.push(``);
  lines.push(`| policy | param | V/budget-year | frozen ratio (mean) | frozen sub (mo) | frozen WIP (mo) | queue | latency | leak | delivered | expired | unreleased@end | vs SQ |`);
  lines.push(`|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|`);
  for (const r of rows) {
    const c = r.core;
    lines.push(`| ${r.family} | ${r.param} | ${f(c.verifiedValuePerBudgetYear.mean)}±${f(c.verifiedValuePerBudgetYear.sd)} | ${f(c.meanFrozenRatio.mean)} | ${f(c.meanFrozenSub.mean, 1)} | ${f(c.meanFrozenWip.mean, 1)} | ${f(c.meanQueue.mean, 1)} | ${f(c.meanLatency.mean, 1)} | ${f(c.leakageRate.mean)} | ${f(c.delivered.mean, 1)} | ${f(c.expired.mean, 1)} | ${f(c.unreleasedEnd.mean, 2)} | ${f(c.verifiedValuePerBudgetYear.mean / Math.max(1e-9, r.sq.verifiedValuePerBudgetYear.mean), 2)}x |`);
  }
  lines.push(``);
  lines.push(`## Status-quo arm (same policies)`);
  lines.push(``);
  lines.push(`| policy | param | V/budget-year | frozen ratio | latency |`);
  lines.push(`|---|---|---:|---:|---:|`);
  for (const r of rows) lines.push(`| ${r.family} | ${r.param} | ${f(r.sq.verifiedValuePerBudgetYear.mean)} | ${f(r.sq.meanFrozenRatio.mean)} | ${f(r.sq.meanLatency.mean, 1)} |`);
  lines.push(``);
  lines.push(`## Pareto frontier (core arm: max V, min frozen ratio, min latency)`);
  lines.push(``);
  for (const r of pareto.sort((a, b) => V(b) - V(a))) lines.push(`- ${r.family} ${r.param}: V=${f(V(r))}, frozen=${f(r.core.meanFrozenRatio.mean)}, latency=${f(r.core.meanLatency.mean, 1)}`);
  lines.push(``);
  const report = lines.join("\n");
  console.log(report);
  const outDir = resolve(HERE, "../results/experiment-e");
  mkdirSync(outDir, { recursive: true });
  writeFileSync(resolve(outDir, "e1a-release-policies-seed1-runs20.md"), report + "\n");
  const serializable = rows.map(({ fn, ...rest }) => rest);
  writeFileSync(resolve(outDir, "e1a-release-policies-seed1-runs20.json"), JSON.stringify({ engine_version: LONG_ENGINE_VERSION, config: { ...cfg, population: undefined, projects: undefined, executors: undefined }, rows: serializable, pareto: pareto.map((r) => `${r.family} ${r.param}`) }, null, 2) + "\n");
  console.error(`outputs: ${outDir}`);
}
