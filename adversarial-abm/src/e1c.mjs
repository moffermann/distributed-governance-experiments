#!/usr/bin/env node
// Experiment E-1c runner (pre-registered: ../EXPERIMENT_E1C_VERIFICATION_DESIGN.md).
// Release policy fixed at the E-1a winner (pull, W*=7 months). Core arm only:
// the verification package is a Core-side instrument; the dominance frontier
// compares AI-triage-core against pure-human-core.
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { LONG_ENGINE_VERSION, POLICIES, DEFAULTS, loadPopulation, runCell } from "./longitudinal.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const CORE = "core_v0_tutored_distributed_agenda";
const RUNS = 20, SEED = 1;
const shared = loadPopulation();
const base = (over = {}) => ({ ...DEFAULTS, ...shared, annualBudget: DEFAULTS.cyclesPerYear * DEFAULTS.citizens, ...over });
const pull7 = POLICIES.pull(7);
const cell = (cfg) => runCell(CORE, pull7, cfg, RUNS, SEED);

// --- Part A: AI triage grid --------------------------------------------------
const A = [];
for (const K of [6, 4]) {
  A.push({ K, pi: 0, falsePass: 0, s: 0, label: "pure human", m: cell(base({ verifyCapacity: K })) });
  console.error(`done baseline K=${K}`);
  for (const pi of [0.4, 0.7, 0.9]) {
    for (const falsePass of [0.01, 0.03, 0.05, 0.10, 0.20]) {
      for (const s of [0.05, 0.15]) {
        const m = cell(base({ verifyCapacity: K, ai: { pi, falsePass, falseFlag: 0.10, sampleRate: s, dossierBoost: 1.25 } }));
        A.push({ K, pi, falsePass, s, label: "ai", m });
      }
    }
    console.error(`done AI K=${K} pi=${pi}`);
  }
}

// --- Part B: verification windows -------------------------------------------
const B = [];
for (const pStall of [0.1, 0.25]) {
  for (const timeout of [null, 1, 2, 3]) {
    const m = cell(base({ stall: { pStall, stallCycles: 6, timeout } }));
    B.push({ pStall, timeout: timeout ?? "off", m });
  }
  console.error(`done windows pStall=${pStall}`);
}

// --- Part C: interaction + dossier sensitivity -------------------------------
const bestAI = A.filter((r) => r.label === "ai" && r.K === 6).sort((a, b) => b.m.verifiedValuePerBudgetYear.mean - a.m.verifiedValuePerBudgetYear.mean)[0];
const bestAiCfg = { pi: bestAI.pi, falsePass: bestAI.falsePass, falseFlag: 0.10, sampleRate: bestAI.s, dossierBoost: 1.25 };
const C = [
  { label: "smoothing only", m: cell(base({ smoothing: true })) },
  { label: `best AI (pi=${bestAI.pi}, fp=${bestAI.falsePass}, s=${bestAI.s})`, m: bestAI.m },
  { label: "best AI + smoothing", m: cell(base({ smoothing: true, ai: bestAiCfg })) },
  { label: "best AI, dossier=1.0", m: cell(base({ ai: { ...bestAiCfg, dossierBoost: 1.0 } })) },
  { label: "best AI, dossier=1.5", m: cell(base({ ai: { ...bestAiCfg, dossierBoost: 1.5 } })) },
];
console.error("done part C");

// --- Frontier: max falsePass where AI-V >= human baseline V ------------------
const frontier = [];
for (const K of [6, 4]) {
  const humanV = A.find((r) => r.K === K && r.label === "pure human").m.verifiedValuePerBudgetYear.mean;
  for (const pi of [0.4, 0.7, 0.9]) for (const s of [0.05, 0.15]) {
    const rowsFp = A.filter((r) => r.label === "ai" && r.K === K && r.pi === pi && r.s === s).sort((a, b) => a.falsePass - b.falsePass);
    let star = null;
    for (const r of rowsFp) if (r.m.verifiedValuePerBudgetYear.mean >= humanV) star = r.falsePass;
    frontier.push({ K, pi, s, humanV, star: star ?? "<0.01" });
  }
}

// --- Report -------------------------------------------------------------------
const f = (x, d = 3) => (typeof x === "number" ? x.toFixed(d) : x);
const row = (m) => `${f(m.verifiedValuePerBudgetYear.mean)}±${f(m.verifiedValuePerBudgetYear.sd)} | ${f(m.leakageRate.mean)} | ${f(m.meanQueue.mean, 1)} | ${f(m.meanLatency.mean, 1)} | ${f(m.expired.mean, 1)} | ${f(m.autoReleasedShare.mean, 2)} | ${f(m.humanLoadPerCycle.mean, 1)}`;
const lines = [];
lines.push(`# Experiment E-1c: verification throughput (engine v${LONG_ENGINE_VERSION})`);
lines.push(``);
lines.push(`release policy: pull W*=7mo (E-1a winner); core arm; falseFlag=0.10, dossierBoost=1.25 unless noted; ${RUNS} runs, seed ${SEED}`);
lines.push(``);
lines.push(`## Part A: AI triage grid (V | leak | queue | latency | expired | auto-share | human-load/cycle)`);
lines.push(``);
lines.push(`| K | pi | falsePass | sample s | V | leak | queue | latency | expired | auto | humanload |`);
lines.push(`|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|`);
for (const r of A) lines.push(`| ${r.K} | ${r.pi} | ${r.falsePass} | ${r.s} | ${row(r.m)} |`);
lines.push(``);
lines.push(`## Dominance frontier aiFalsePass* (max falsePass where AI >= pure human)`);
lines.push(``);
lines.push(`| K | pi | s | human V | falsePass* |`);
lines.push(`|---:|---:|---:|---:|---:|`);
for (const r of frontier) lines.push(`| ${r.K} | ${r.pi} | ${r.s} | ${f(r.humanV)} | ${r.star} |`);
lines.push(``);
lines.push(`## Part B: verification windows (pStall x timeout; stallCycles=6, pure human, K=6)`);
lines.push(``);
lines.push(`| pStall | timeout | V | leak | queue | latency | expired |`);
lines.push(`|---:|---:|---:|---:|---:|---:|---:|`);
for (const r of B) lines.push(`| ${r.pStall} | ${r.timeout} | ${f(r.m.verifiedValuePerBudgetYear.mean)}±${f(r.m.verifiedValuePerBudgetYear.sd)} | ${f(r.m.leakageRate.mean)} | ${f(r.m.meanQueue.mean, 1)} | ${f(r.m.meanLatency.mean, 1)} | ${f(r.m.expired.mean, 1)} |`);
lines.push(``);
lines.push(`## Part C: interaction and dossier sensitivity (K=6)`);
lines.push(``);
lines.push(`| cell | V | leak | queue | latency | expired | auto | humanload |`);
lines.push(`|---|---:|---:|---:|---:|---:|---:|---:|`);
for (const r of C) lines.push(`| ${r.label} | ${row(r.m)} |`);
lines.push(``);
const report = lines.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/experiment-e");
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, "e1c-verification-seed1-runs20.md"), report + "\n");
const strip = (arr) => arr.map(({ m, ...rest }) => ({ ...rest, V: m.verifiedValuePerBudgetYear.mean, Vsd: m.verifiedValuePerBudgetYear.sd, leak: m.leakageRate.mean, queue: m.meanQueue.mean, latency: m.meanLatency.mean, expired: m.expired.mean, auto: m.autoReleasedShare.mean, humanLoad: m.humanLoadPerCycle.mean }));
writeFileSync(resolve(outDir, "e1c-verification-seed1-runs20.json"), JSON.stringify({ engine_version: LONG_ENGINE_VERSION, partA: strip(A), frontier, partB: strip(B), partC: strip(C) }, null, 2) + "\n");
console.error(`outputs: ${outDir}`);
