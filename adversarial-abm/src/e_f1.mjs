#!/usr/bin/env node
// Experiment F-1 runner: layers vs confidence under the common-cause
// correlation model (../EXPERIMENT_F_LAYERED_VERIFICATION_DESIGN.md).
// Usage: node e_f1.mjs [--rho-measured 0.XX]   (adds the F-0 measured cell)
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { LONG_ENGINE_VERSION, POLICIES, DEFAULTS, loadPopulation, runCell } from "./longitudinal.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const CORE = "core_v0_tutored_distributed_agenda";
const RUNS = 20, SEED = 1;
const shared = loadPopulation();
const base = (o = {}) => ({ ...DEFAULTS, ...shared, annualBudget: DEFAULTS.cyclesPerYear * DEFAULTS.citizens, ...o });
const AI = { pi: 0.7, falsePass: 0.05, falseFlag: 0.10, sampleRate: 0.05, dossierBoost: 1.25 };

const argIdx = process.argv.indexOf("--rho-measured");
const rhoMeasured = argIdx > -1 ? Number(process.argv[argIdx + 1]) : null;
const rhos = [0, 0.3, 0.6, ...(rhoMeasured !== null ? [rhoMeasured] : [])];

const rows = [];
for (const K of [6, 4]) {
  rows.push({ K, k: 0, rho: "-", gaming: "-", label: "pure human", m: runCell(CORE, POLICIES.pull(7), base({ verifyCapacity: K }), RUNS, SEED) });
  for (const rho of rhos) {
    for (const k of [1, 2, 3, 4]) {
      for (const gaming of [null, { skill: 0.35 }]) {
        const cfg = base({ verifyCapacity: K, ai: { ...AI, layers: { k, rho } }, evidenceGaming: gaming });
        const m = runCell(CORE, POLICIES.pull(7), cfg, RUNS, SEED);
        rows.push({ K, k, rho, gaming: gaming ? gaming.skill : "off", label: `k=${k} rho=${rho}`, m });
      }
    }
    console.error(`done K=${K} rho=${rho}`);
  }
}

const f = (x, d = 3) => (typeof x === "number" ? x.toFixed(d) : x);
const lines = [];
lines.push(`# Experiment F-1: layers vs confidence (engine v${LONG_ENGINE_VERSION})`);
lines.push(``);
lines.push(`common-cause model: P(clear|diverted) = rho + (1-rho)*fp^k, fp=${AI.falsePass}/layer, falseFlag=${AI.falseFlag}/layer (any-flag refers); gaming adds to the shared mass; pull W*=7; ${RUNS} runs, seed ${SEED}${rhoMeasured !== null ? `; rho-measured=${rhoMeasured} (F-0)` : ""}`);
lines.push(``);
lines.push(`| K | rho | gaming | k | V | leak | auto-share | humanload |`);
lines.push(`|---:|---:|---:|---:|---:|---:|---:|---:|`);
for (const r of rows) {
  lines.push(`| ${r.K} | ${r.rho} | ${r.gaming} | ${r.k} | ${f(r.m.verifiedValuePerBudgetYear.mean)}±${f(r.m.verifiedValuePerBudgetYear.sd)} | ${f(r.m.leakageRate.mean, 4)} | ${f(r.m.autoReleasedShare.mean, 2)} | ${f(r.m.humanLoadPerCycle.mean, 1)} |`);
}
lines.push(``);
const report = lines.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/experiment-f");
mkdirSync(outDir, { recursive: true });
const suffix = rhoMeasured !== null ? "-with-measured" : "";
writeFileSync(resolve(outDir, `f1-layers-seed1-runs20${suffix}.md`), report + "\n");
writeFileSync(resolve(outDir, `f1-layers-seed1-runs20${suffix}.json`), JSON.stringify({
  engine_version: LONG_ENGINE_VERSION, ai: AI, rhoMeasured,
  rows: rows.map(({ m, ...rest }) => ({ ...rest, V: m.verifiedValuePerBudgetYear.mean, Vsd: m.verifiedValuePerBudgetYear.sd, leak: m.leakageRate.mean, auto: m.autoReleasedShare.mean, humanLoad: m.humanLoadPerCycle.mean })),
}, null, 2) + "\n");
console.error(`outputs: ${outDir}`);
