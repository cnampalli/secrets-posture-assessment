import { describe, test, expect, beforeEach } from 'vitest';
import { indexedDB } from 'fake-indexeddb';
import {
  putFile, getBlob, deleteFile, blobToBase64, base64ToBlob,
  validateFile, humanSize, genId,
  buildExportRecord, restoreEvidence,
} from './evidence';
import { RUBRIC } from './rubric';

function fileOf(name: string, type: string, bytes = 10): File {
  return new File([new Uint8Array(bytes).fill(65)], name, { type });
}

beforeEach(async () => {
  await new Promise<void>(res => { const r = indexedDB.deleteDatabase('posture-evidence'); r.onsuccess = r.onerror = () => res(); });
});

test('putFile/getBlob/deleteFile round-trip', async () => {
  const blob = new Blob([new Uint8Array([1, 2, 3, 4])], { type: 'application/pdf' });
  await putFile('id1', blob);
  const got = await getBlob('id1');
  expect(got).not.toBeNull();
  expect(new Uint8Array(await got!.arrayBuffer())).toEqual(new Uint8Array([1, 2, 3, 4]));
  expect(got!.type).toBe('application/pdf');
  await deleteFile('id1');
  expect(await getBlob('id1')).toBeNull();
});

test('blobToBase64 / base64ToBlob preserve bytes', async () => {
  const bytes = new Uint8Array([0, 1, 250, 99, 7, 255]);
  const b64 = await blobToBase64(new Blob([bytes]));
  const round = new Uint8Array(await base64ToBlob(b64, 'application/octet-stream').arrayBuffer());
  expect(round).toEqual(bytes);
});

test('validateFile accepts allowed types and rejects oversize + unsupported', () => {
  expect(validateFile(fileOf('a.pdf', 'application/pdf')).ok).toBe(true);
  expect(validateFile(fileOf('a.docx', '')).ok).toBe(true);
  const big = new File([new Uint8Array(2)], 'big.pdf', { type: 'application/pdf' });
  Object.defineProperty(big, 'size', { value: 10 * 1024 * 1024 + 1 });
  const r1 = validateFile(big); expect(r1.ok).toBe(false); if (!r1.ok) expect(r1.reason).toMatch(/10 MB/);
  const r2 = validateFile(fileOf('evil.zip', 'application/zip')); expect(r2.ok).toBe(false);
});

test('humanSize formats bytes/KB/MB', () => {
  expect(humanSize(512)).toBe('512 B');
  expect(humanSize(2048)).toBe('2 KB');
  expect(humanSize(1572864)).toBe('1.5 MB');
});

test('genId returns a unique non-empty string', () => {
  const a = genId(), b = genId();
  expect(a).toBeTruthy(); expect(typeof a).toBe('string'); expect(a).not.toBe(b);
});

test('buildExportRecord embeds base64 for stored blobs and reports skips', async () => {
  const uc = RUBRIC[0].uc_id;
  await putFile('e1', new Blob([new Uint8Array([9, 9, 9])], { type: 'application/pdf' }));
  const evidence = { [uc]: [
    { id: 'e1', name: 'a.pdf', type: 'application/pdf', size: 3, added: 'T' },
    { id: 'missing', name: 'gone.pdf', type: 'application/pdf', size: 3, added: 'T' },
  ]};
  const { record, skipped } = await buildExportRecord(RUBRIC, {}, evidence, 'T', getBlob);
  expect(skipped).toBe(1);
  expect(record.evidence![uc]).toHaveLength(1);
  expect(typeof (record.evidence![uc][0] as { data: string }).data).toBe('string');
});

test('restoreEvidence writes blobs to IDB, strips data, replaces per uc, returns skipped', async () => {
  const uc = RUBRIC[0].uc_id;
  const data = await blobToBase64(new Blob([new Uint8Array([1, 2])], { type: 'application/pdf' }));
  const parsed = { [uc]: [{ id: 'r1', name: 'a.pdf', type: 'application/pdf', size: 2, added: 'T', data }] };
  const { evidence, skipped } = await restoreEvidence({}, parsed, (id) => id === uc);
  expect(skipped).toBe(0);
  expect(evidence[uc]).toEqual([{ id: 'r1', name: 'a.pdf', type: 'application/pdf', size: 2, added: 'T' }]);
  expect(await getBlob('r1')).not.toBeNull();
  const res2 = await restoreEvidence({}, { 'NOPE': parsed[uc] }, (id) => id === uc);
  expect(res2.evidence['NOPE']).toBeUndefined();
});

test('restoreEvidence keeps existing evidence when an incoming non-empty list is all malformed', async () => {
  const uc = RUBRIC[0].uc_id;
  await putFile('keep1', new Blob([new Uint8Array([5, 5])], { type: 'application/pdf' }));
  const current = { [uc]: [{ id: 'keep1', name: 'keep.pdf', type: 'application/pdf', size: 2, added: 'T' }] };
  const parsed = { [uc]: [{ id: 'bad', name: 'b.pdf', type: 'application/pdf', size: 1, added: 'T' /* no data */ }] };
  const { evidence, skipped } = await restoreEvidence(current, parsed, (id) => id === uc);
  expect(skipped).toBe(1);
  expect(evidence[uc]).toEqual(current[uc]);        // prior evidence retained
  expect(await getBlob('keep1')).not.toBeNull();    // prior blob NOT deleted
});
