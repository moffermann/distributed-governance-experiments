#!/usr/bin/env node
// Semi-open regime: first quantification (master docs/110).
//
// The semi-open regime is a FISCAL parallel: the authority mandates a bounded
// envelope — share e of the budget over a disjoint slice of the project
// ontology — inside which projects run on Core v0's distributed machinery
// with automatic protocol approval; the complement (1−e) stays with the
// incumbent status quo. This runner traces the full transition path
// V(blended) as e sweeps from 0 (pure status quo) to 1 (open-equivalent).
//
// Honest boundary, declared: this engine has never modeled a per-project
// authority veto stage, so the tutored and semi-open regimes differ here only
// in envelope structure; the decision-layer difference (veto vs automatic
// approval) is not priced by this experiment. The ontological frontier is
// represented by partitioning budget and project pool proportionally into
// disjoint sub-worlds — exact for per-budget metrics, which blend linearly
// by budget share.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { ENGINE_VERSION, runScenario } from "./index.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const CORE = "core_v0_tutored_distributed_agenda";
const SQ = "status_quo";

const base = JSON.parse(readFileSync(resolve(HERE, "../scenarios/behavioral-llm-calibrated.json"), "utf8"));
base.outputs = {};

const deep = (obj) => JSON.parse(JSON.stringify(obj));
const scaled = (share, architectures, idSuffix) => {
  const s = deep(base);
  s.scenario_id = `semi-open-${idSuffix}`;
  s.population.citizens = Math.max(100, Math.round(base.population.citizens * share));
  s.projects.activePool = Math.max(2, Math.round(base.projects.activePool * share));
  s.architectures = architectures;
  return s;
};
const verified = (scenario, archId) => {
  const { summary } = runScenario(scenario);
  const row = summary.find((r) => r.architecture === archId);
  return { mean: row.verifiedValuePerBudget.mean, sd: row.verifiedValuePerBudget.sd };
};

const ENVELOPES = [0, 0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.0];
const rows = [];
for (const e of ENVELOPES) {
  let vCore = { mean: 0, sd: 0 }, vSq = { mean: 0, sd: 0 };
  if (e > 0) vCore = verified(scaled(e, [CORE], `env-${e}`), CORE);
  if (e < 1) vSq = verified(scaled(1 - e, [SQ], `rest-${e}`), SQ);
  const blended = e * vCore.mean + (1 - e) * vSq.mean;
  rows.push({ envelope: e, vCore: vCore.mean, vSq: vSq.mean, blended });
}
const sqPure = rows[0].blended;

const f = (x, d = 3) => x.toFixed(d);
const lines = [];
lines.push(`# Semi-open regime: the transition path (first quantification)`);
lines.push(``);
lines.push(`engine v${ENGINE_VERSION}, population: behavioral-llm-calibrated (envelope side), 20 runs, seed 1`);
lines.push(`Blend: V = e*V(core distributed | envelope slice) + (1-e)*V(status quo | complement); per-budget metrics blend exactly by budget share.`);
lines.push(``);
lines.push(`| envelope share e | V(envelope) | V(complement) | V(blended) | vs pure status quo |`);
lines.push(`|---:|---:|---:|---:|---:|`);
for (const r of rows) lines.push(`| ${(r.envelope * 100).toFixed(0)}% | ${r.envelope > 0 ? f(r.vCore) : "—"} | ${r.envelope < 1 ? f(r.vSq) : "—"} | ${f(r.blended)} | ${f(r.blended / sqPure, 2)}x |`);
lines.push(``);
const report = lines.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/semi-open");
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, "semi-open-transition-seed1-runs20.md"), report + "\n");
writeFileSync(resolve(outDir, "semi-open-transition-seed1-runs20.json"), JSON.stringify({ engine_version: ENGINE_VERSION, rows }, null, 2) + "\n");
console.log(`\noutputs: ${outDir}`);
