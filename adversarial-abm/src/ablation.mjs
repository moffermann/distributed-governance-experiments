#!/usr/bin/env node
// Ablation and sensitivity program (pre-registered in
// ../ABLATION_AND_SENSITIVITY_DESIGN.md). Runs mechanism knock-outs, parameter
// cliff-hunting sweeps, and the three attack families against the
// behavioral-llm-calibrated population, and writes the vulnerability tables.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { ENGINE_VERSION, runScenario } from "./index.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const CORE = "core_v0_tutored_distributed_agenda";
const SQ = "status_quo";

const base = JSON.parse(readFileSync(resolve(HERE, "../scenarios/behavioral-llm-calibrated.json"), "utf8"));
base.architectures = [SQ, CORE];
base.outputs = {};

const deep = (obj) => JSON.parse(JSON.stringify(obj));
const cell = (mutate, label) => {
  const s = deep(base);
  s.scenario_id = `ablation-${label}`;
  mutate(s);
  const { summary } = runScenario(s);
  const core = summary.find((r) => r.architecture === CORE);
  const sq = summary.find((r) => r.architecture === SQ);
  return {
    label,
    V: core.verifiedValuePerBudget.mean,
    Vsd: core.verifiedValuePerBudget.sd,
    leak: core.leakageRate.mean,
    visGap: core.visibilityGapPerBudget.mean,
    sel: core.selectionValueCorrelation.mean,
    Vsq: sq.verifiedValuePerBudget.mean,
    ratio: core.verifiedValuePerBudget.mean / sq.verifiedValuePerBudget.mean,
  };
};
const over = (fields) => (s) => { s.architectureOverrides = { [CORE]: fields }; };

// --- Axis 1: mechanism knock-outs -------------------------------------------
const intact = cell(() => {}, "intact");
const knockouts = [
  ["K1 fundingCaps OFF", over({ fundingCaps: false })],
  ["K2 detection -> status quo (0.15)", over({ detectionBase: 0.15 })],
  ["K3 financial terms -> status quo", over({ retention: 0.05, guarantee: 0.02 })],
  ["K4 reputational memory OFF", over({ reputationLoss: 0.02, futureSelectionLoss: 0.02 })],
  ["K5 default layer -> salience", over({ passiveAllocationMode: "salience" })],
  ["K6 planning vector -> central", over({ prioritizationSource: "central" })],
  ["K7 delegation channel OFF", (s) => { s.population.passiveShare += s.population.delegatorShare; s.population.delegatorShare = 0; }],
  ["K8 profile channel OFF", (s) => { s.population.passiveShare += s.population.profileShare; s.population.profileShare = 0; }],
  ["K9 herding brake OFF", over({ socialProofDamping: 1.0 })],
  // P3 follow-up cell (pre-announced in the design): the deterrence stack is
  // expected to be redundant term-by-term; this removes ALL of it at once.
  ["K10 ALL deterrence -> status quo", over({ detectionBase: 0.15, reviewConfidence: 0.35, retention: 0.05, guarantee: 0.02, reputationLoss: 0.02, futureSelectionLoss: 0.02 })],
].map(([label, mutate]) => cell(mutate, label.split(" ")[0]));

const kLabels = ["K1 fundingCaps OFF", "K2 detection -> status quo (0.15)", "K3 financial terms -> status quo",
  "K4 reputational memory OFF", "K5 default layer -> salience", "K6 planning vector -> central",
  "K7 delegation channel OFF", "K8 profile channel OFF", "K9 herding brake OFF", "K10 ALL deterrence -> status quo"];

// --- Axis 2: parameter sweeps ------------------------------------------------
const sweeps = [];
const sweep = (name, values, mutate) => {
  for (const v of values) sweeps.push({ name, value: v, ...cell((s) => mutate(s, v), `${name}-${v}`) });
};
sweep("detectionBase", [0.15, 0.25, 0.35, 0.55, 0.75], (s, v) => { s.architectureOverrides = { [CORE]: { detectionBase: v } }; });
sweep("opportunisticShare", [0.1, 0.3, 0.5, 0.7], (s, v) => { s.executors.opportunisticShare = v; s.executors.honestShare = 1 - v; });
sweep("distributedPrioritizationSignalMix", [0.2, 0.4, 0.66, 0.8], (s, v) => { s.projects.distributedPrioritizationSignalMix = v; });
sweep("delegationBlockSize", [1, 3, 10, 50], (s, v) => { s.population.delegationBlockSize = v; });
sweep("socialProofWeight", [1, 3, 6], (s, v) => { s.attacks.salienceCascade.socialProofWeight = v; });

// --- Axis 3: attacks ----------------------------------------------------------
const attacks = [];
const attack = (name, key, param, values) => {
  for (const v of values) attacks.push({ name, value: v, ...cell((s) => { s.attacks[key] = { enabled: true, [param]: v }; }, `${name}-${v}`) });
};
attack("fiscalizerCollusion", "fiscalizerCollusion", "collusionRate", [0.15, 0.30, 0.50]);
attack("agendaCapture", "agendaCapture", "severity", [0.15, 0.30, 0.50]);
attack("coordinatedSignalBias", "coordinatedSignalBias", "share", [0.10, 0.30, 0.50]);

// --- Report -------------------------------------------------------------------
const f = (x, d = 3) => x.toFixed(d);
const lines = [];
lines.push(`# Ablation and sensitivity results`);
lines.push(``);
lines.push(`engine v${ENGINE_VERSION}, population: behavioral-llm-calibrated, 20 runs, seed 1, arms: ${SQ} + ${CORE}`);
lines.push(`intact reference: V=${f(intact.V)}±${f(intact.Vsd)}, leak=${f(intact.leak)}, visGap=${f(intact.visGap)}, sel=${f(intact.sel)}, ratio vs status quo=${f(intact.ratio, 2)}x`);
lines.push(``);
lines.push(`## Mechanism knock-outs (sorted by verified-value loss)`);
lines.push(``);
lines.push(`| knock-out | V | dV vs intact | leak | visGap | sel(theta) | ratio vs SQ |`);
lines.push(`|---|---:|---:|---:|---:|---:|---:|`);
const sorted = knockouts.map((k, i) => ({ ...k, label: kLabels[i] })).sort((a, b) => a.V - b.V);
for (const k of sorted) lines.push(`| ${k.label} | ${f(k.V)} | ${f(k.V - intact.V)} | ${f(k.leak)} | ${f(k.visGap)} | ${f(k.sel)} | ${f(k.ratio, 2)}x |`);
lines.push(``);
lines.push(`## Parameter sweeps (cliff-hunting)`);
lines.push(``);
lines.push(`| parameter | value | V | leak | ratio vs SQ |`);
lines.push(`|---|---:|---:|---:|---:|`);
for (const s of sweeps) lines.push(`| ${s.name} | ${s.value} | ${f(s.V)} | ${f(s.leak)} | ${f(s.ratio, 2)}x |`);
lines.push(``);
lines.push(`## Attacks`);
lines.push(``);
lines.push(`| attack | severity | V | dV vs intact | leak | sel(theta) | ratio vs SQ |`);
lines.push(`|---|---:|---:|---:|---:|---:|---:|`);
for (const a of attacks) lines.push(`| ${a.name} | ${a.value} | ${f(a.V)} | ${f(a.V - intact.V)} | ${f(a.leak)} | ${f(a.sel)} | ${f(a.ratio, 2)}x |`);
lines.push(``);
const report = lines.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/ablation");
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, "ablation-behavioral-llm-calibrated-seed1-runs20.md"), report + "\n");
writeFileSync(resolve(outDir, "ablation-behavioral-llm-calibrated-seed1-runs20.json"), JSON.stringify({ engine_version: ENGINE_VERSION, intact, knockouts: sorted, sweeps, attacks }, null, 2) + "\n");
console.log(`\noutputs: ${outDir}`);
