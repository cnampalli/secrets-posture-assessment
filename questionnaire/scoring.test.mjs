import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
// Load scoring.js by evaluating its source (it is a plain script, not ESM).
const src = readFileSync(join(here, "scoring.js"), "utf8");
const deriveState = new Function(src + "\nreturn deriveState;")();
const vectors = JSON.parse(readFileSync(join(here, "scoring-vectors.json"), "utf8"));

let failed = 0;
for (const v of vectors) {
  const got = deriveState(v.questions, v.answers);
  if (got !== v.expected) { console.error(`FAIL ${v.name}: got ${got}, want ${v.expected}`); failed++; }
}
if (failed) { console.error(`${failed} vector(s) failed`); process.exit(1); }
console.log(`scoring.js: ${vectors.length} vectors OK`);
