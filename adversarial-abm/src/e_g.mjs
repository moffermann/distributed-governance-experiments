#!/usr/bin/env node
// Experiment G runner (../EXPERIMENT_G_COLLUSIVE_ADVERSARY_DESIGN.md):
// collusive, multi-period, adaptive adversary vs the intact stack.
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { LONG_ENGINE_VERSION, POLICIES, DEFAULTS, loadPopulation, runCell } from "./longitudinal.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const CORE = "core_v0_tutored_distributed_agenda";
const SQ = "status_quo";
const RUNS = 20, SEED = 1;
const shared = loadPopulation();
const base = (o = {}) => ({ ...DEFAULTS, ...shared, annualBudget: DEFAULTS.cyclesPerYear * DEFAULTS.citizens, ...o });
const AI = { pi: 0.7, falsePass: 0.05, falseFlag: 0.10, sampleRate: 0.05, dossierBoost: 1.25 };
const f = (x, d = 3) => x.toFixed(d);

const sqRef = runCell(SQ, POLICIES.pull(7), base(), RUNS, SEED).verifiedValuePerBudgetYear.mean;

const lines = [];
lines.push(`# Experiment G: collusive/adaptive adversary (engine v${LONG_ENGINE_VERSION})`);
lines.push(``);
lines.push(`core arm w/ AI triage (pi 0.7, fp 0.05) + contraposition 50%; pull W*=7; ${RUNS} runs, seed ${SEED}; status-quo reference V=${f(sqRef)}`);
lines.push(``);

// PG2/PG3/PG6: collusion sweep on intact stack, with contraposition on (the F-4 rescue) to test PG3.
lines.push(`## Collusion sweep (intact stack, AI triage + 50% contraposition)`);
lines.push(``);
lines.push(`| collusion rate | V | leak | diversion attempts | V vs status quo |`);
lines.push(`|---:|---:|---:|---:|---:|`);
const collRows = [];
for (const rate of [0, 0.05, 0.1, 0.2, 0.35, 0.5]) {
  const cfg = base({ ai: AI, contraposition: { coverage: 0.5, catch: 0.8 }, adversary: rate > 0 ? { collusion: { rate } } : null });
  const r = runCell(CORE, POLICIES.pull(7), cfg, RUNS, SEED);
  const ratio = r.verifiedValuePerBudgetYear.mean / sqRef;
  collRows.push({ rate, V: r.verifiedValuePerBudgetYear.mean, leak: r.leakageRate.mean, ratio });
  lines.push(`| ${(rate * 100).toFixed(0)}% | ${f(r.verifiedValuePerBudgetYear.mean)} | ${f(r.leakageRate.mean, 4)} | ${f(r.diversionAttempts.mean, 1)} | ${f(ratio, 2)}x |`);
  console.error(`done collusion ${rate}`);
}
// PG6: locate the collusion rate where the advantage inverts (ratio crosses 1).
let crossover = null;
for (let i = 1; i < collRows.length; i++) {
  if (collRows[i - 1].ratio >= 1 && collRows[i].ratio < 1) {
    const a = collRows[i - 1], b = collRows[i];
    crossover = a.rate + (b.rate - a.rate) * (a.ratio - 1) / (a.ratio - b.ratio);
    break;
  }
}
lines.push(``);
lines.push(`**PG6 crossover (advantage inverts, ratio→1):** ${crossover === null ? "not reached in [0, 0.5] — advantage survives the whole range" : `collusion rate ≈ ${(crossover * 100).toFixed(0)}%`}`);
lines.push(``);

// PG3: does contraposition still rescue a DEGRADED stack under collusion?
const DEGRADED = { detectionBase: 0.15, retention: 0.05, guarantee: 0.02, reputationLoss: 0.02, futureSelectionLoss: 0.02, reviewConfidence: 0.35 };
lines.push(`## PG3: contraposition rescue of a broken stack — non-colluding vs colluding`);
lines.push(``);
lines.push(`| stack | contraposition | collusion | V | leak |`);
lines.push(`|---|---|---:|---:|---:|`);
for (const [cov, coll] of [[0, 0], [0.5, 0], [0.5, 0.2], [1.0, 0.2]]) {
  const cfg = base({ archOverride: DEGRADED, ai: AI, contraposition: cov > 0 ? { coverage: cov, catch: 0.8 } : null, adversary: coll > 0 ? { collusion: { rate: coll } } : null });
  const r = runCell(CORE, POLICIES.pull(7), cfg, RUNS, SEED);
  lines.push(`| degraded | ${(cov * 100).toFixed(0)}% | ${(coll * 100).toFixed(0)}% | ${f(r.verifiedValuePerBudgetYear.mean)} | ${f(r.leakageRate.mean, 4)} |`);
  console.error(`done PG3 cov=${cov} coll=${coll}`);
}
lines.push(``);

// PG1/PG4: adaptive targeting and anchor poisoning (intact stack, no collusion).
lines.push(`## PG1 adaptive targeting & PG4 anchor poisoning (intact stack)`);
lines.push(``);
lines.push(`| attack | param | V | leak |`);
lines.push(`|---|---|---:|---:|`);
for (const g of [0.1, 0.25, 0.4]) {
  const r = runCell(CORE, POLICIES.pull(7), base({ ai: AI, adversary: { adaptiveGain: g } }), RUNS, SEED);
  lines.push(`| adaptive targeting | gain ${g} | ${f(r.verifiedValuePerBudgetYear.mean)} | ${f(r.leakageRate.mean, 4)} |`);
}
for (const ap of [0.25, 0.5, 0.75]) {
  const r = runCell(CORE, POLICIES.pull(7), base({ ai: AI, adversary: { anchorPoison: ap } }), RUNS, SEED);
  lines.push(`| anchor poisoning | ${(ap * 100).toFixed(0)}% detection loss | ${f(r.verifiedValuePerBudgetYear.mean)} | ${f(r.leakageRate.mean, 4)} |`);
}
console.error("done PG1/PG4");
lines.push(``);

const report = lines.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/experiment-g");
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, "g-collusive-adversary-seed1-runs20.md"), report + "\n");
writeFileSync(resolve(outDir, "g-collusive-adversary-seed1-runs20.json"), JSON.stringify({ engine_version: LONG_ENGINE_VERSION, sqRef, collRows, crossover }, null, 2) + "\n");
console.error(`outputs: ${outDir}`);
