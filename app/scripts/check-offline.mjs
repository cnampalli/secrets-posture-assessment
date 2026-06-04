// Fails if the built single-file HTML references any external URL or leaves
// un-inlined asset files — proving the deliverable is fully offline.
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const dist = new URL('../dist/', import.meta.url).pathname;
const html = readFileSync(join(dist, 'index.html'), 'utf8');

const externals = [...html.matchAll(/(?:src|href)\s*=\s*["'](https?:\/\/[^"']+)/g)].map(m => m[1]);
if (externals.length) {
  console.error('FAIL — external URLs in build:', externals);
  process.exit(1);
}
const stray = readdirSync(dist).filter(f => f !== 'index.html' && !f.startsWith('.'));
if (stray.length) {
  console.error('FAIL — un-inlined files in dist (expected only index.html):', stray);
  process.exit(1);
}
console.log('OK — single self-contained offline index.html');
