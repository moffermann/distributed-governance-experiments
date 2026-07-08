#!/usr/bin/env node
// Experiment H — Project Allocation Rules (the two-layer decomposition).
// Renamed from the mis-named "agenda-setting study": it studies how PROJECTS
// are allocated, not a fixed planning agenda. The two-layer static engine
// (TWO_LAYER_ALLOCATION_REDESIGN.md) separates, for the first time, the macro
// categorization (#1: central vs distributed partition) from the project
// allocation profiles (#2: value-targeted vs attribute-incidental routing).
// Three results: (a) the incidental-leak sweep, (b) the categorization-
// misalignment "ceiling" sweep — where distributing #1 goes from irrelevant to
// decisive, and (c) the architecture comparison — Core v0's advantage over a
// central status quo grows as central planning worsens, because the distributed
// arm re-categorizes to value while the central arm is stuck with its categories.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { runScenario } from "./index.mjs";

const HERE = decodeURIComponent(new URL(".", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
const BASE = JSON.parse(readFileSync(resolve(HERE, "../scenarios/behavioral-llm-calibrated.json"), "utf8"));
const RUNS = 40, SEED = 1, CATS = 6, CAP = 0.30, INC = 0.2;

const scen = (id, archs, mis, inc, overrides) => ({
  ...BASE, scenario_id: id, seed: SEED, runs: RUNS, architectures: archs,
  population: { ...BASE.population, incidentalProfileShare: inc },
  twoLayer: { enabled: true, numCategories: CATS, misalignedShare: mis, misalignedValueCap: CAP },
  architectureOverrides: overrides,
});
const coreV = (part, mis, inc) => runScenario(scen(`h-core-${part}-${mis}-${inc}`, ["core_v0_tutored_distributed_agenda"], mis, inc,
  { core_v0_tutored_distributed_agenda: { partitionSource: part } })).summary[0].verifiedValuePerBudget.mean;
const f = (x) => x.toFixed(4);

const L = [];
L.push("# Experiment H: Project Allocation Rules — the two-layer decomposition");
L.push("");
L.push(`Two-layer static engine; core arm unless noted; ${RUNS} runs, seed ${SEED}; ${CATS} categories, value cap ${CAP}. Verified value per budget.`);
L.push("");

// (a) incidental-leak sweep (at moderate misalignment 0.35)
L.push("## (a) The incidental leak — marginal at realistic profile compositions");
L.push("");
L.push("| incidental share of profiles | V central | V distributed | ratio |");
L.push("|---:|---:|---:|---:|");
for (const inc of [0.0, 0.1, 0.2, 0.3, 0.5, 0.9]) {
  const c = coreV("central", 0.35, inc), d = coreV("distributed", 0.35, inc);
  L.push(`| ${inc.toFixed(1)} | ${f(c)} | ${f(d)} | ${(d / c).toFixed(2)}× |`);
}
L.push("");
L.push("At a moderately-misaligned categorization (35% of the pool), value-targeted profile rules self-correct and only attribute-incidental rules leak; distributing the partition is marginal (≈1.05–1.16× at realistic incidental shares). A misaligned project's leaked funding is small because \"near me\" is one weighted rule balanced by value-aligned ones (\"pending funding\" tracks the attentive minority; thematic rules track value).");
L.push("");

// (b) categorization-misalignment "ceiling" sweep (incidental fixed realistic 0.2)
L.push("## (b) The ceiling — distributing #1 goes from irrelevant to decisive as the central categorization worsens");
L.push("");
L.push(`| central categorization misaligned | V central | V distributed | advantage of distributing #1 |`);
L.push("|---:|---:|---:|---:|");
for (const mis of [0.0, 0.2, 0.35, 0.5, 0.65, 0.8, 0.9]) {
  const c = coreV("central", mis, INC), d = coreV("distributed", mis, INC);
  L.push(`| ${(mis * 100).toFixed(0)}% | ${f(c)} | ${f(d)} | ${(d / c).toFixed(2)}× |`);
}
L.push("");
L.push("The distributed arm is **flat** across categorization quality (it re-categorizes to value); the central arm collapses. So distributing the categorization is **irrelevant** when it is well-drawn (1.00×), **marginal** under moderate misalignment (~1.06–1.15×; citizens' profiles route around bad categories), and **decisive** when the categorization is mostly bad (1.75×→2.46×; the good projects are not even eligible, and #2 cannot route to what is absent). Delivered value is **robust to a bad central categorization** under distribution and **fragile to it** under central planning.");
L.push("");

// (c) architecture comparison — Core v0 vs central status quo
L.push("## (c) Core v0 vs the central status quo — the advantage grows as central planning worsens");
L.push("");
L.push("| central categorization misaligned | status quo V | Core v0 V | Core v0 / status quo |");
L.push("|---:|---:|---:|---:|");
const archRows = [];
for (const mis of [0.0, 0.2, 0.35, 0.5, 0.65, 0.8, 0.9]) {
  const s = runScenario(scen(`h-arch-${mis}`, ["status_quo", "core_v0_tutored_distributed_agenda"], mis, INC,
    { status_quo: { partitionSource: "central" }, core_v0_tutored_distributed_agenda: { partitionSource: "distributed" } })).summary;
  const sq = s.find((a) => a.architecture === "status_quo").verifiedValuePerBudget.mean;
  const core = s.find((a) => a.architecture === "core_v0_tutored_distributed_agenda").verifiedValuePerBudget.mean;
  archRows.push({ mis, sq, core, ratio: core / sq });
  L.push(`| ${(mis * 100).toFixed(0)}% | ${f(sq)} | ${f(core)} | ${(core / sq).toFixed(2)}× |`);
}
L.push("");
L.push(`**The combined effect.** Comparing architectures, Core v0's advantage over a central status quo is **not fixed** — it is a function of central-planning quality, rising from ${archRows[0].ratio.toFixed(2)}× (well-drawn categorization) to **${archRows[archRows.length - 1].ratio.toFixed(2)}×** (mostly-bad). Two effects compound: the *advantage of choosing* (#2 routes to higher-value projects) and *avoiding an imposed bad central plan* (#1 re-categorizes rather than being stuck with the authority's categories). The fused single-weight model could express neither; the two-layer model shows both, and that they multiply. (The base ratio here is scenario-specific with two-layer on, not the cross-population 2.0–2.7× headline; the finding is the trend, not the base.)`);
L.push("");
L.push("Boundary: allocation-quality layer only; the verification/deterrence/release pipeline is downstream and unchanged. Simulation evidence about a model.");

const report = L.join("\n");
console.log(report);
const outDir = resolve(HERE, "../results/experiment-h");
mkdirSync(outDir, { recursive: true });
writeFileSync(resolve(outDir, "h-project-allocation-seed1-runs40.md"), report + "\n");
writeFileSync(resolve(outDir, "h-project-allocation-seed1-runs40.json"), JSON.stringify({ runs: RUNS, seed: SEED, incidental: INC, archComparison: archRows }, null, 2) + "\n");
console.error(`outputs: ${outDir}`);
