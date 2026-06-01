import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const src = readFileSync(join(here, "exec-summary.js"), "utf8");
const { groupByQuadrant, sortItems, filterItems } =
  new Function(src + "\nreturn { groupByQuadrant, sortItems, filterItems };")();

const items = [
  { uc_id: "UC-A", quadrant: "Quick wins",     risk_band: "High", effort_band: "Med",  state: "GAP" },
  { uc_id: "UC-B", quadrant: "Quick wins",     risk_band: "Med",  effort_band: "Low",  state: "PARTIAL" },
  { uc_id: "UC-C", quadrant: "Major projects", risk_band: "High", effort_band: "High", state: "GAP" },
  { uc_id: "UC-D", quadrant: "Fill-ins",       risk_band: "Low",  effort_band: "Low",  state: "PARTIAL" },
];

let failed = 0;
const check = (name, cond) => { if (!cond) { console.error(`FAIL ${name}`); failed++; } };

const g = groupByQuadrant(items);
check("group quick wins", g["Quick wins"].length === 2);
check("group major", g["Major projects"].length === 1);
check("group fill-ins", g["Fill-ins"].length === 1);
check("group hard slogs empty", (g["Hard slogs"] || []).length === 0);
check("filter quadrant", filterItems(items, { quadrant: "Quick wins" }).map(i => i.uc_id).join() === "UC-A,UC-B");
check("filter state", filterItems(items, { state: "GAP" }).map(i => i.uc_id).join() === "UC-A,UC-C");
check("filter none returns all", filterItems(items, {}).length === 4);
check("sort by risk", sortItems(items, "risk").map(i => i.uc_id).join() === "UC-A,UC-C,UC-B,UC-D");
check("sort by effort", sortItems(items, "effort").map(i => i.uc_id).join() === "UC-B,UC-D,UC-A,UC-C");

if (failed) { console.error(`${failed} check(s) failed`); process.exit(1); }
console.log("exec-summary.js: all logic checks OK");
