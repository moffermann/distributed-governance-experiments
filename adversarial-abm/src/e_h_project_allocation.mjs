#!/usr/bin/env node
// Experiment H — Project Allocation Rules (the two-layer decomposition).
// Renamed from the mis-named "agenda-setting study": it studies how PROJECTS
// are allocated, not a fixed planning agenda. Uses the two-layer static engine
// (TWO_LAYER_ALLOCATION_REDESIGN.md) to separate, for the first time, the
// contribution of the macro categorization (#1: central vs distributed
// partition) from the project allocation profiles (#2: value-targeted vs
// attribute-incidental routing) — a decomposition the fused single-weight
// model could not express.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { runScenario } from "./index.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const BASE = JSON.parse(readFileSync(resolve(HERE, "../scenarios/behavioral-llm-calibrated.json"), "utf8"));
const RUNS = 40, SEED = 1;
const CATS = 6, MIS = 0.35, CAP = 0.30;

const V = (partitionSource, incidentalShare) => {
  const scenario = {
    ...BASE, scenario_id: `H-${partitionSource}-${incidentalShare}`, seed: SEED, runs: RUNS,
    architectures: ["core_v0_tutored_distributed_agenda"],
    population: { ...BASE.population, incidentalProfileShare: incidentalShare },
    twoLayer: { enabled: true, numCategories: CATS, misalignedShare: MIS, misalignedValueCap: CAP },
    architectureOverrides: { core_v0_tutored_distributed_agenda: { partitionSource } },
  };
  return runScenario(scenario).summary[0].verifiedValuePerBudget.mean;
};

const f = (x) => x.toFixed(4);
const lines = [];
lines.push("# Experiment H: Project Allocation Rules — the two-layer decomposition");
lines.push("");
lines.push(`Two-layer static engine; core arm; ${RUNS} runs, seed ${SEED}; ${CATS} categories, misaligned share ${MIS}, value cap ${CAP}. Verified value per budget.`);
lines.push("");
lines.push("## Distributing the macro partition (#1) across profile compositions (#2)");
lines.push("");
lines.push("| incidental share of profiles (#2) | V, central partition | V, distributed partition | advantage of distributing #1 |");
lines.push("|---:|---:|---:|---:|");
const rows = [];
for (const inc of [0.0, 0.1, 0.3, 0.5, 0.7, 0.9]) {
  const c = V("central", inc), d = V("distributed", inc);
  rows.push({ inc, c, d, ratio: d / c });
  lines.push(`| ${inc.toFixed(1)} | ${f(c)} | ${f(d)} | ${(d / c).toFixed(2)}× |`);
}
lines.push("");
const lo = rows[1], hi = rows[rows.length - 1];
lines.push(`**Finding (PL1, ratio form).** The advantage of distributing the macro categorization (#1) grows with the share of attribute-incidental profile rules: ${lo.ratio.toFixed(2)}× at ${lo.inc.toFixed(1)} incidental, ${hi.ratio.toFixed(2)}× at ${hi.inc.toFixed(1)}. When the inattentive majority routes by value-orthogonal rules ("near me"), only distributing #1 removes the misaligned projects they would otherwise leak into; when profiles are value-targeted, they self-correct and #1 matters less. This decomposition is impossible in the fused single-weight model.`);
lines.push("");
lines.push("## #1-vs-#2 contribution decomposition (at a mixed profile composition, incidental 0.5)");
lines.push("");
const base = V("central", 0.5);           // bad #1, mixed #2
const only1 = V("distributed", 0.5);      // good #1, mixed #2
const only2 = V("central", 0.0);          // bad #1, all-targeted #2
const both = V("distributed", 0.0);       // good #1, all-targeted #2
lines.push("| configuration | V |");
lines.push("|---|---:|");
lines.push(`| central #1, mixed #2 (baseline) | ${f(base)} |`);
lines.push(`| **distribute #1 only** (distributed partition, mixed #2) | ${f(only1)}  (Δ ${(only1 - base >= 0 ? "+" : "")}${f(only1 - base)}) |`);
lines.push(`| **improve #2 only** (central partition, all-targeted profiles) | ${f(only2)}  (Δ ${(only2 - base >= 0 ? "+" : "")}${f(only2 - base)}) |`);
lines.push(`| both | ${f(both)}  (Δ ${(both - base >= 0 ? "+" : "")}${f(both - base)}) |`);
lines.push("");
lines.push(`**Decomposition.** From the central/mixed baseline, distributing #1 alone adds ${f(only1 - base)} and improving #2 alone (value-targeted profiles) adds ${f(only2 - base)}; the two are ${(only1 - base) > (only2 - base) ? "#1-dominant" : "#2-dominant"} here and combine to ${f(both - base)}. The point is that the two-layer model **can attribute** the advantage to a layer; the fused model reported one number.`);
lines.push("");
lines.push("Boundary: this is the allocation-quality layer only; the pipeline (verification, deterrence, release) is downstream and unchanged. Simulation evidence about a model.");

const report = lines.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/experiment-h");
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, "h-project-allocation-seed1-runs40.md"), report + "\n");
writeFileSync(resolve(outDir, "h-project-allocation-seed1-runs40.json"), JSON.stringify({ runs: RUNS, seed: SEED, rows, decomposition: { base, only1, only2, both } }, null, 2) + "\n");
console.error(`outputs: ${outDir}`);
