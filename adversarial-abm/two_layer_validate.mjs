import { readFileSync } from "node:fs";
const { runScenario } = await import("file:///C:/devel/claude-projects/distributed-governance-experiments/adversarial-abm/src/index.mjs");
const BASE = JSON.parse(readFileSync("C:/devel/claude-projects/distributed-governance-experiments/adversarial-abm/scenarios/behavioral-llm-calibrated.json", "utf8"));
function runPartition(partitionSource, inc) {
  const scenario = { ...BASE, scenario_id: `tl-${partitionSource}`, seed: 1, runs: 30,
    architectures: ["core_v0_tutored_distributed_agenda"],
    population: { ...BASE.population, incidentalProfileShare: inc },
    twoLayer: { enabled: true, numCategories: 6, misalignedShare: 0.35, misalignedValueCap: 0.30 },
    architectureOverrides: { core_v0_tutored_distributed_agenda: { partitionSource } } };
  return runScenario(scenario).summary[0].verifiedValuePerBudget.mean;
}
console.log("=== two-layer ON: central vs distributed partition (30 runs) ===");
console.log("incidental\tV central\tV distrib\tgain(#1)");
for (const inc of [0.1, 0.5, 0.9]) {
  const c = runPartition("central", inc), d = runPartition("distributed", inc);
  console.log(`${inc.toFixed(1)}\t\t${c.toFixed(4)}\t\t${d.toFixed(4)}\t\t${(d-c).toFixed(4)}`);
}
