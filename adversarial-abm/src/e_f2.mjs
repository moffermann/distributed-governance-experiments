#!/usr/bin/env node
// Experiment F-2: the control-cost frontier
// (../EXPERIMENT_F_LAYERED_VERIFICATION_DESIGN.md). The engines price
// verification as CAPACITY; F-2 adds the missing budget line and reports
// verified value per TOTAL budget (delivery + control + evidence premium)
// across three regimes: pure human, single-layer triage (E-1c), layered k=2.
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { LONG_ENGINE_VERSION, POLICIES, DEFAULTS, loadPopulation, runCell } from "./longitudinal.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const CORE = "core_v0_tutored_distributed_agenda";
const RUNS = 20, SEED = 1;
const shared = loadPopulation();
const base = (o = {}) => ({ ...DEFAULTS, ...shared, annualBudget: DEFAULTS.cyclesPerYear * DEFAULTS.citizens, ...o });
const AI = { pi: 0.7, falsePass: 0.05, falseFlag: 0.10, sampleRate: 0.05, dossierBoost: 1.25 };
const RHO_DEFAULT = 0.3; // overridden by --rho-measured
const argIdx = process.argv.indexOf("--rho-measured");
const rho = argIdx > -1 ? Number(process.argv[argIdx + 1]) : RHO_DEFAULT;

// Cost model (declared in the design):
//   human verification cost per milestone  = h * tranche, h in {3%, 6%, 10%}
//     (anchored to real-world supervision at 3-10% of project cost)
//   machine verification cost per milestone = 0.1% * tranche (declared)
//   court-grade evidence premium per milestone = e * tranche, e in {0.5%, 2%, 5%}
// tranche ~= meanTarget / milestones. Total verifications reconstructed from
// the engine's humanLoadPerCycle and autoReleasedShare metrics.

const REGIMES = [
  { name: "pure human", cfg: () => base() },
  { name: "triage 1-layer (E-1c)", cfg: () => base({ ai: AI }) },
  { name: `layered k=2 (rho=${rho})`, cfg: () => base({ ai: { ...AI, layers: { k: 2, rho } } }) },
];

const cells = [];
for (const K of [6, 4]) {
  for (const regime of REGIMES) {
    const m = runCell(CORE, POLICIES.pull(7), { ...regime.cfg(), verifyCapacity: K }, RUNS, SEED);
    cells.push({ K, regime: regime.name, m });
    console.error(`done K=${K} ${regime.name}`);
  }
}

const cfg0 = base();
const cycles = cfg0.years * cfg0.cyclesPerYear;
const totalBudget = cfg0.annualBudget * cfg0.years;
const tranche = cfg0.meanTarget / cfg0.milestones;

const f = (x, d = 3) => x.toFixed(d);
const lines = [];
lines.push(`# Experiment F-2: the control-cost frontier (engine v${LONG_ENGINE_VERSION})`);
lines.push(``);
lines.push(`V_total = verifiedValue / (delivery budget + human cost + machine cost + evidence premium); tranche=${tranche.toFixed(0)}, rho=${rho}; pull W*=7; ${RUNS} runs, seed ${SEED}.`);
lines.push(`Machine cost swept over {0.1%/milestone (hosted-API stipulation), 0 (open-weights local: energy/hardware are sunk or marginal — author correction 2026-07-07)}.`);
lines.push(``);
lines.push(`| K | regime | h (human %/milestone) | e (evidence %/milestone) | machine cost | V plain | control+evidence cost (% of budget) | V per TOTAL budget |`);
lines.push(`|---:|---|---:|---:|---:|---:|---:|---:|`);
const summary = [];
for (const { K, regime, m } of cells) {
  const humanVerifs = m.humanLoadPerCycle.mean * cycles;
  const autoShare = m.autoReleasedShare.mean;
  const aiVerifs = autoShare > 0 ? (autoShare / (1 - autoShare)) * humanVerifs : 0;
  const milestones = humanVerifs + aiVerifs; // audits double-count slightly; declared conservative
  const verifiedValue = m.verifiedValuePerBudgetYear.mean * totalBudget;
  for (const h of [0.03, 0.06, 0.10]) {
    for (const e of [0.005, 0.02, 0.05]) {
      for (const mc of [0.001, 0]) {
        const controlCost = h * tranche * humanVerifs + mc * tranche * aiVerifs + e * tranche * milestones;
        const vTotal = verifiedValue / (totalBudget + controlCost);
        lines.push(`| ${K} | ${regime} | ${(h * 100).toFixed(0)}% | ${(e * 100).toFixed(1)}% | ${mc === 0 ? "0 (local)" : "0.1%"} | ${f(m.verifiedValuePerBudgetYear.mean)} | ${f(100 * controlCost / totalBudget, 1)}% | ${f(vTotal)} |`);
        summary.push({ K, regime, h, e, mc, vTotal, controlShare: controlCost / totalBudget });
      }
    }
  }
}
lines.push(``);
// Crossover analysis (PF2-3): at each (K, h), the evidence premium where layered stops dominating triage.
lines.push(`## Dominance notes`);
for (const K of [6, 4]) {
  for (const h of [0.03, 0.06, 0.10]) {
    const get = (regime, e) => summary.find((s) => s.K === K && s.regime.startsWith(regime) && s.h === h && s.e === e && s.mc === 0)?.vTotal ?? 0;
    const doms = [0.005, 0.02, 0.05].map((e) => `e=${(e * 100).toFixed(1)}%: ${get("layered", e) >= get("triage", e) ? "layered>=triage" : "triage>layered"}`);
    lines.push(`- K=${K}, h=${(h * 100).toFixed(0)}%: ${doms.join("; ")}`);
  }
}
lines.push(``);
const report = lines.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/experiment-f");
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, "f2-control-cost-seed1-runs20.md"), report + "\n");
writeFileSync(resolve(outDir, "f2-control-cost-seed1-runs20.json"), JSON.stringify({ engine_version: LONG_ENGINE_VERSION, rho, tranche, rows: summary }, null, 2) + "\n");
console.error(`outputs: ${outDir}`);
