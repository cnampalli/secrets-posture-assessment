import { describe, test, expect, beforeEach } from 'vitest';
import { indexedDB } from 'fake-indexeddb';
import {
  putFile, getBlob, deleteFile, blobToBase64, base64ToBlob,
  validateFile, humanSize, genId,
} from './evidence';

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
