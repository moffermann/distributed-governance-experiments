#!/usr/bin/env node
// F-3: does the deterrence cascade cover the MEASURED AI verification
// failures (author question 2026-07-07)? Cells use the F-0 v2 measured
// operating points, on the intact vs the degraded (docs/111 K10) stack.
// F-4: contraposed independent evidence — how much does fraud drop as
// coverage grows? (author design, engine v0.10)
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { LONG_ENGINE_VERSION, POLICIES, DEFAULTS, loadPopulation, runCell } from "./longitudinal.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const CORE = "core_v0_tutored_distributed_agenda";
const RUNS = 20, SEED = 1;
const shared = loadPopulation();
const base = (o = {}) => ({ ...DEFAULTS, ...shared, annualBudget: DEFAULTS.cyclesPerYear * DEFAULTS.citizens, ...o });
const DEGRADED = { detectionBase: 0.15, retention: 0.05, guarantee: 0.02, reputationLoss: 0.02, futureSelectionLoss: 0.02, reviewConfidence: 0.35 };

// Measured operating points (F-0 v2, evidence-rich bundles):
//   claude single:      fp 0.083, ff 0.050
//   deepseek (worst):   fp 0.217, ff 0.317
//   deepseek+claude pair: measured joint fp 0.067 (indep 0.018 -> rho_eff 0.05)
//     engine equivalent: fp/layer = sqrt(0.018) = 0.134, k=2, rho = 0.05,
//     ff/layer such that any-flag = 0.351 -> 0.195
const MEASURED = [
  { name: "claude single (best measured)", ai: { pi: 0.7, falsePass: 0.083, falseFlag: 0.05, sampleRate: 0.05, dossierBoost: 1.25 } },
  { name: "deepseek single (worst measured)", ai: { pi: 0.7, falsePass: 0.217, falseFlag: 0.317, sampleRate: 0.05, dossierBoost: 1.25 } },
  { name: "deepseek+claude pair (measured rho)", ai: { pi: 0.7, falsePass: 0.134, falseFlag: 0.195, sampleRate: 0.05, dossierBoost: 1.25, layers: { k: 2, rho: 0.05 } } },
];

const f = (x, d = 3) => x.toFixed(d);
const lines = [];
lines.push(`# F-3 / F-4: the cascade vs measured AI failures; contraposition coverage (engine v${LONG_ENGINE_VERSION})`);
lines.push(``);
lines.push(`pull W*=7, ${RUNS} runs, seed ${SEED}; operating points from F-0 v2 (evidence-rich bundles)`);
lines.push(``);
lines.push(`## F-3: measured operating points x stack integrity`);
lines.push(``);
lines.push(`| stack | verifier (measured) | V | leak | diversion attempts | detections |`);
lines.push(`|---|---|---:|---:|---:|---:|`);
for (const [sname, over] of [["intact", null], ["degraded (docs/111 violation)", DEGRADED]]) {
  const bh = runCell(CORE, POLICIES.pull(7), base({ archOverride: over }), RUNS, SEED);
  lines.push(`| ${sname} | pure human (reference) | ${f(bh.verifiedValuePerBudgetYear.mean)} | ${f(bh.leakageRate.mean, 4)} | ${f(bh.diversionAttempts.mean, 1)} | ${f(bh.detections.mean, 1)} |`);
  for (const m of MEASURED) {
    const r = runCell(CORE, POLICIES.pull(7), base({ archOverride: over, ai: m.ai }), RUNS, SEED);
    lines.push(`| ${sname} | ${m.name} | ${f(r.verifiedValuePerBudgetYear.mean)} | ${f(r.leakageRate.mean, 4)} | ${f(r.diversionAttempts.mean, 1)} | ${f(r.detections.mean, 1)} |`);
  }
  console.error(`done F-3 ${sname}`);
}
lines.push(``);
lines.push(`## F-4: contraposed independent evidence (coverage sweep; catch=0.8 declared)`);
lines.push(``);
lines.push(`| coverage | verifier | V | leak | diversion attempts |`);
lines.push(`|---:|---|---:|---:|---:|`);
const CLAUDE = MEASURED[0].ai;
for (const coverage of [0, 0.1, 0.25, 0.5, 0.75, 1.0]) {
  const cfgC = base({ ai: CLAUDE, contraposition: coverage > 0 ? { coverage, catch: 0.8 } : null });
  const r = runCell(CORE, POLICIES.pull(7), cfgC, RUNS, SEED);
  lines.push(`| ${(coverage * 100).toFixed(0)}% | claude single | ${f(r.verifiedValuePerBudgetYear.mean)} | ${f(r.leakageRate.mean, 4)} | ${f(r.diversionAttempts.mean, 1)} |`);
  console.error(`done F-4 c=${coverage}`);
}
// F-4 on the DEGRADED stack: does contraposition rescue a broken cascade?
lines.push(``);
lines.push(`| coverage | verifier (degraded stack) | V | leak | diversion attempts |`);
lines.push(`|---:|---|---:|---:|---:|`);
for (const coverage of [0, 0.5, 1.0]) {
  const cfgC = base({ archOverride: DEGRADED, ai: CLAUDE, contraposition: coverage > 0 ? { coverage, catch: 0.8 } : null });
  const r = runCell(CORE, POLICIES.pull(7), cfgC, RUNS, SEED);
  lines.push(`| ${(coverage * 100).toFixed(0)}% | claude single | ${f(r.verifiedValuePerBudgetYear.mean)} | ${f(r.leakageRate.mean, 4)} | ${f(r.diversionAttempts.mean, 1)} |`);
  console.error(`done F-4deg c=${coverage}`);
}
lines.push(``);
const report = lines.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/experiment-f");
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, "f34-cascade-contraposition-seed1-runs20.md"), report + "\n");
console.error(`outputs: ${outDir}`);
