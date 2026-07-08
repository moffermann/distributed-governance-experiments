const m = await import("file:///C:/devel/claude-projects/distributed-governance-experiments/adversarial-abm/src/longitudinal.mjs");
const s = m.loadPopulation();
function run(part, inc) {
  const c = { ...m.DEFAULTS, ...s, annualBudget: 24000,
    population: { ...s.population, incidentalProfileShare: inc },
    twoLayer: { enabled: true, numCategories: 6, misalignedShare: 0.35, misalignedValueCap: 0.30 },
    archOverride: { partitionSource: part } };
  return m.runCell('core_v0_tutored_distributed_agenda', m.POLICIES.pull(7), c, 20, 1).verifiedValuePerBudgetYear.mean;
}
console.log("=== longitudinal two-layer ON (central vs distributed partition) ===");
console.log("incidental\tV central\tV distrib\tratio");
for (const inc of [0.1, 0.5, 0.9]) {
  const cc = run('central', inc), dd = run('distributed', inc);
  console.log(`${inc.toFixed(1)}\t\t${cc.toFixed(4)}\t\t${dd.toFixed(4)}\t\t${(dd/cc).toFixed(2)}x`);
}
