#!/usr/bin/env node
// Experiment E-1b runner (pre-registered: ../EXPERIMENT_E1B_ADVERSARIES_DESIGN.md).
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { LONG_ENGINE_VERSION, POLICIES, DEFAULTS, loadPopulation, runCell } from "./longitudinal.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const CORE = "core_v0_tutored_distributed_agenda";
const RUNS = 20, SEED = 1;
const shared = loadPopulation();
const base = (over = {}) => ({ ...DEFAULTS, ...shared, annualBudget: DEFAULTS.cyclesPerYear * DEFAULTS.citizens, ...over });
const cell = (policy, cfg) => runCell(CORE, policy, cfg, RUNS, SEED);
const STALE = { rate: 0.06, floor: 0.4 };
const DEGRADED = { detectionBase: 0.15, retention: 0.05, guarantee: 0.02, reputationLoss: 0.02, futureSelectionLoss: 0.02, reviewConfidence: 0.35 };
const AI = { pi: 0.7, falsePass: 0.05, falseFlag: 0.10, sampleRate: 0.05, dossierBoost: 1.25 };

// --- Part A: congestion as attack surface ------------------------------------
const A = [];
for (const [pname, policy] of [["pull W=7", POLICIES.pull(7)], ["day_zero", POLICIES.day_zero()]]) {
  A.push({ pname, staleness: "off", adversary: "blind", m: cell(policy, base()) });
  A.push({ pname, staleness: "on", adversary: "blind", m: cell(policy, base({ staleness: STALE })) });
  A.push({ pname, staleness: "on", adversary: "timing-aware", m: cell(policy, base({ staleness: STALE, timingAware: true })) });
  console.error(`done A: ${pname}`);
}

// --- Part B: evidence gaming x stack integrity --------------------------------
const B = [];
for (const [sname, archOverride] of [["intact", null], ["degraded (docs/111 violation)", DEGRADED]]) {
  B.push({ sname, vname: "pure human", m: cell(POLICIES.pull(7), base({ archOverride })) });
  B.push({ sname, vname: "AI fp=0.05", m: cell(POLICIES.pull(7), base({ archOverride, ai: AI })) });
  B.push({ sname, vname: "AI + gaming 0.35", m: cell(POLICIES.pull(7), base({ archOverride, ai: AI, evidenceGaming: { skill: 0.35 } })) });
  B.push({ sname, vname: "AI + gaming 0.55", m: cell(POLICIES.pull(7), base({ archOverride, ai: AI, evidenceGaming: { skill: 0.55 } })) });
  console.error(`done B: ${sname}`);
}

// --- Part C: reputation compounding over 8 years ------------------------------
const YEARS = 8;
const C = [];
for (const compounding of [true, false]) {
  const m = cell(POLICIES.pull(7), base({ years: YEARS, reputationCompounding: compounding }));
  C.push({ compounding, m });
  console.error(`done C: compounding=${compounding}`);
}

// --- Report -------------------------------------------------------------------
const f = (x, d = 3) => x.toFixed(d);
const lines = [];
lines.push(`# Experiment E-1b: adaptive adversaries (engine v${LONG_ENGINE_VERSION})`);
lines.push(``);
lines.push(`core arm, pull W*=7 unless noted; staleness {rate 0.06, floor 0.4}; AI {pi 0.7, fp 0.05, s 0.05}; ${RUNS} runs, seed ${SEED}`);
lines.push(``);
lines.push(`## Part A: congestion as attack surface (release policy as security parameter)`);
lines.push(``);
lines.push(`| policy | staleness | adversary | V | leak | queue | detections |`);
lines.push(`|---|---|---|---:|---:|---:|---:|`);
for (const r of A) lines.push(`| ${r.pname} | ${r.staleness} | ${r.adversary} | ${f(r.m.verifiedValuePerBudgetYear.mean)}±${f(r.m.verifiedValuePerBudgetYear.sd)} | ${f(r.m.leakageRate.mean)} | ${f(r.m.meanQueue.mean, 1)} | ${f(r.m.detections.mean, 1)} |`);
const dmg = (pname) => {
  const blind = A.find((r) => r.pname === pname && r.staleness === "on" && r.adversary === "blind").m.verifiedValuePerBudgetYear.mean;
  const aware = A.find((r) => r.pname === pname && r.adversary === "timing-aware").m.verifiedValuePerBudgetYear.mean;
  return blind - aware;
};
lines.push(``);
lines.push(`Timing-awareness damage dV(blind - aware): pull = ${f(dmg("pull W=7"))}, day_zero = ${f(dmg("day_zero"))}`);
lines.push(``);
lines.push(`## Part B: evidence gaming x stack integrity`);
lines.push(``);
lines.push(`| stack | verification | V | leak | detections |`);
lines.push(`|---|---|---:|---:|---:|`);
for (const r of B) lines.push(`| ${r.sname} | ${r.vname} | ${f(r.m.verifiedValuePerBudgetYear.mean)}±${f(r.m.verifiedValuePerBudgetYear.sd)} | ${f(r.m.leakageRate.mean)} | ${f(r.m.detections.mean, 1)} |`);
lines.push(``);
lines.push(`## Part C: reputation compounding over ${YEARS} years (V and leak per year, per annual budget)`);
lines.push(``);
lines.push(`| compounding | ${Array.from({ length: YEARS }, (_, i) => `V y${i + 1}`).join(" | ")} |`);
lines.push(`|---|${"---:|".repeat(YEARS)}`);
for (const r of C) lines.push(`| ${r.compounding ? "on" : "off"} | ${Array.from({ length: YEARS }, (_, i) => f(r.m[`vy${i + 1}`].mean)).join(" | ")} |`);
lines.push(``);
lines.push(`| compounding | ${Array.from({ length: YEARS }, (_, i) => `leak y${i + 1}`).join(" | ")} |`);
lines.push(`|---|${"---:|".repeat(YEARS)}`);
for (const r of C) lines.push(`| ${r.compounding ? "on" : "off"} | ${Array.from({ length: YEARS }, (_, i) => f(r.m[`ly${i + 1}`].mean, 4)).join(" | ")} |`);
lines.push(``);
const report = lines.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/experiment-e");
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, "e1b-adversaries-seed1-runs20.md"), report + "\n");
const strip = (arr) => arr.map(({ m, ...rest }) => ({ ...rest, metrics: Object.fromEntries(Object.entries(m).map(([k, v]) => [k, v.mean])) }));
writeFileSync(resolve(outDir, "e1b-adversaries-seed1-runs20.json"), JSON.stringify({ engine_version: LONG_ENGINE_VERSION, partA: strip(A), partB: strip(B), partC: strip(C) }, null, 2) + "\n");
console.error(`outputs: ${outDir}`);
