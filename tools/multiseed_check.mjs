#!/usr/bin/env node
// Multi-base-seed robustness check (review round 1, statistician objection:
// all CIs were conditional on base seed 1). Reruns the two headline cells —
// the static architecture comparison and the longitudinal pull-W*=7 cell —
// across five independent base seeds and reports the between-seed spread of
// the 20-run means. Writes results/multiseed/multiseed-check.md.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { runScenario } from "../adversarial-abm/src/index.mjs";
import { POLICIES, DEFAULTS, loadPopulation, runCell } from "../adversarial-abm/src/longitudinal.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const SEEDS = [1, 101, 202, 303, 404];

const scenario = JSON.parse(readFileSync(resolve(HERE, "../adversarial-abm/scenarios/behavioral-llm-calibrated.json"), "utf8"));
scenario.outputs = {};
scenario.architectures = ["status_quo", "core_v0_tutored_distributed_agenda"];

const staticRows = [];
for (const seed of SEEDS) {
  const { summary } = runScenario({ ...scenario, seed, scenario_id: `multiseed-${seed}` });
  const core = summary.find((r) => r.architecture === "core_v0_tutored_distributed_agenda").verifiedValuePerBudget.mean;
  const sq = summary.find((r) => r.architecture === "status_quo").verifiedValuePerBudget.mean;
  staticRows.push({ seed, core, sq, ratio: core / sq });
  console.error(`static seed ${seed} done`);
}

const shared = loadPopulation();
const cfg = { ...DEFAULTS, ...shared, annualBudget: DEFAULTS.cyclesPerYear * DEFAULTS.citizens };
const longRows = [];
for (const seed of SEEDS) {
  const m = runCell("core_v0_tutored_distributed_agenda", POLICIES.pull(7), cfg, 20, seed);
  longRows.push({ seed, V: m.verifiedValuePerBudgetYear.mean });
  console.error(`longitudinal seed ${seed} done`);
}

const stats = (vals) => {
  const m = vals.reduce((a, b) => a + b, 0) / vals.length;
  const sd = Math.sqrt(vals.reduce((a, b) => a + (b - m) ** 2, 0) / vals.length);
  return { m, sd, min: Math.min(...vals), max: Math.max(...vals) };
};
const f = (x, d = 3) => x.toFixed(d);
const cs = stats(staticRows.map((r) => r.core));
const ss = stats(staticRows.map((r) => r.sq));
const rs = stats(staticRows.map((r) => r.ratio));
const ls = stats(longRows.map((r) => r.V));

const lines = [];
lines.push(`# Multi-base-seed robustness check`);
lines.push(``);
lines.push(`Five independent base seeds (${SEEDS.join(", ")}), 20 runs each; between-seed spread of the 20-run means for the two headline cells.`);
lines.push(``);
lines.push(`## Static architecture comparison (behavioral-llm-calibrated)`);
lines.push(``);
lines.push(`| base seed | V core distributed | V status quo | ratio |`);
lines.push(`|---:|---:|---:|---:|`);
for (const r of staticRows) lines.push(`| ${r.seed} | ${f(r.core)} | ${f(r.sq)} | ${f(r.ratio, 2)}x |`);
lines.push(`| **between-seed** | ${f(cs.m)} ± ${f(cs.sd)} [${f(cs.min)}, ${f(cs.max)}] | ${f(ss.m)} ± ${f(ss.sd)} [${f(ss.min)}, ${f(ss.max)}] | ${f(rs.m, 2)}x ± ${f(rs.sd, 2)} [${f(rs.min, 2)}, ${f(rs.max, 2)}] |`);
lines.push(``);
lines.push(`## Longitudinal pull W*=7 (E-1a headline cell)`);
lines.push(``);
lines.push(`| base seed | V per budget-year |`);
lines.push(`|---:|---:|`);
for (const r of longRows) lines.push(`| ${r.seed} | ${f(r.V)} |`);
lines.push(`| **between-seed** | ${f(ls.m)} ± ${f(ls.sd)} [${f(ls.min)}, ${f(ls.max)}] |`);
lines.push(``);
const report = lines.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/multiseed");
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, "multiseed-check.md"), report + "\n");
