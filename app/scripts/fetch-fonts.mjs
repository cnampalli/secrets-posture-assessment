import { mkdirSync, writeFileSync } from 'node:fs';
const dir = new URL('../src/assets/fonts/', import.meta.url).pathname;
mkdirSync(dir, { recursive: true });
const base = 'https://cdn.jsdelivr.net/npm/@fontsource-variable';
const files = {
  'fraunces.woff2': 'fraunces@latest/files/fraunces-latin-wght-normal.woff2',
  'inter.woff2': 'inter@latest/files/inter-latin-wght-normal.woff2',
  'jetbrains-mono.woff2': 'jetbrains-mono@latest/files/jetbrains-mono-latin-wght-normal.woff2',
};
for (const [name, path] of Object.entries(files)) {
  const r = await fetch(`${base}/${path}`);
  if (!r.ok) throw new Error(`${name}: HTTP ${r.status}`);
  const buf = Buffer.from(await r.arrayBuffer());
  if (buf.slice(0, 4).toString('latin1') !== 'wOF2') throw new Error(`${name}: not woff2`);
  writeFileSync(dir + name, buf);
  console.log('OK', name, buf.length, 'bytes');
}
