#!/usr/bin/env node
// E-1a sensitivity: does the optimal pull WIP cap W* track verification
// capacity K (the Little's-Law claim behind prediction P2), or the budget?
import { POLICIES, DEFAULTS, loadPopulation, runCell } from "./longitudinal.mjs";

const shared = loadPopulation();
const CORE = "core_v0_tutored_distributed_agenda";
const rows = [];
for (const K of [4, 6, 9]) {
  const cfg = { ...DEFAULTS, ...shared, verifyCapacity: K, annualBudget: DEFAULTS.cyclesPerYear * DEFAULTS.citizens };
  for (const W of [3, 5, 7, 9, 11]) {
    const m = runCell(CORE, POLICIES.pull(W), cfg, 20, 1);
    rows.push({ K, W, V: m.verifiedValuePerBudgetYear.mean, queue: m.meanQueue.mean, wip: m.meanFrozenWip.mean });
    console.error(`done K=${K} W=${W}`);
  }
}
console.log("| K | W (mo) | V/budget-year | queue | WIP (mo) |");
console.log("|---:|---:|---:|---:|---:|");
for (const r of rows) console.log(`| ${r.K} | ${r.W} | ${r.V.toFixed(3)} | ${r.queue.toFixed(1)} | ${r.wip.toFixed(1)} |`);
for (const K of [4, 6, 9]) {
  const best = rows.filter((r) => r.K === K).sort((a, b) => b.V - a.V)[0];
  console.log(`K=${K}: best W=${best.W}mo (V=${best.V.toFixed(3)})`);
}
