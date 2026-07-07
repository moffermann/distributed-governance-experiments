#!/usr/bin/env node
// Experiment E-1d runner: drift-detection latency of passive lane-c sampling
// (../RUN_2026_07_06_EXPERIMENT_E1D_RESULTS.md). AI false-pass drifts upward
// from startCycle; the question is whether lane-c ever notices.
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { LONG_ENGINE_VERSION, POLICIES, DEFAULTS, loadPopulation, runCell } from "./longitudinal.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const CORE = "core_v0_tutored_distributed_agenda";
const shared = loadPopulation();
const base = (o = {}) => ({ ...DEFAULTS, ...shared, annualBudget: DEFAULTS.cyclesPerYear * DEFAULTS.citizens, years: 6, ...o });
const AI = { pi: 0.7, falsePass: 0.05, falseFlag: 0.10, dossierBoost: 1.25 };
const DRIFT = { startCycle: 24, rate: 0.03 };

const rows = [];
for (const s of [0.02, 0.05, 0.15]) {
  const m = runCell(CORE, POLICIES.pull(7), base({ ai: { ...AI, sampleRate: s }, aiDrift: DRIFT }), 20, 1);
  rows.push({ s, latency: m.driftCatchLatency.mean, latencySd: m.driftCatchLatency.sd, V: m.verifiedValuePerBudgetYear.mean, leak: m.leakageRate.mean });
  console.error(`done s=${s}`);
}
const noDrift = runCell(CORE, POLICIES.pull(7), base({ ai: { ...AI, sampleRate: 0.05 } }), 20, 1);

const f = (x, d = 3) => x.toFixed(d);
const lines = [];
lines.push(`# E-1d: drift-detection latency of passive sampling (engine v${LONG_ENGINE_VERSION})`);
lines.push(``);
lines.push(`drift: falsePass +${DRIFT.rate}/cycle from cycle ${DRIFT.startCycle}; horizon 72 cycles (latency censored at 48); pull W=7; AI pi=${AI.pi} fp=${AI.falsePass}; 20 runs, seed 1`);
lines.push(``);
lines.push(`| sample rate s | latency (cycles, censored@48) | V | leak |`);
lines.push(`|---:|---:|---:|---:|`);
for (const r of rows) lines.push(`| ${r.s} | ${f(r.latency, 1)} ± ${f(r.latencySd, 1)} | ${f(r.V)} | ${f(r.leak, 4)} |`);
lines.push(`| no drift (s=0.05) | — | ${f(noDrift.verifiedValuePerBudgetYear.mean)} | ${f(noDrift.leakageRate.mean, 4)} |`);
lines.push(``);
const report = lines.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/experiment-e");
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, "e1d-drift-detection-seed1-runs20.md"), report + "\n");
writeFileSync(resolve(outDir, "e1d-drift-detection-seed1-runs20.json"), JSON.stringify({ engine_version: LONG_ENGINE_VERSION, drift: DRIFT, ai: AI, rows, noDrift: { V: noDrift.verifiedValuePerBudgetYear.mean, leak: noDrift.leakageRate.mean } }, null, 2) + "\n");
console.error(`outputs: ${outDir}`);
