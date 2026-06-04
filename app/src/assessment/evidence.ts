import { MAX_BYTES, ALLOWED_TYPES } from './types';
import type { UseCase, Response, AssessmentRecord, EvidenceMeta, EvidenceExport } from './types';
import { buildRecord } from './record';

const DB_NAME = 'posture-evidence';
const STORE = 'files';

function openDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      if (!req.result.objectStoreNames.contains(STORE)) req.result.createObjectStore(STORE, { keyPath: 'id' });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export async function putFile(id: string, blob: Blob): Promise<void> {
  const buffer = await blob.arrayBuffer();
  const db = await openDb();
  try {
    await new Promise<void>((res, rej) => {
      const t = db.transaction(STORE, 'readwrite');
      t.objectStore(STORE).put({ id, buffer, type: blob.type });
      t.oncomplete = () => res();
      t.onerror = () => rej(t.error);
      t.onabort = () => rej(t.error);
    });
  } finally { db.close(); }
}

export async function getBlob(id: string): Promise<Blob | null> {
  const db = await openDb();
  try {
    return await new Promise<Blob | null>((res, rej) => {
      const r = db.transaction(STORE, 'readonly').objectStore(STORE).get(id);
      r.onsuccess = () => {
        if (!r.result) { res(null); return; }
        res(new Blob([r.result.buffer as ArrayBuffer], { type: r.result.type as string }));
      };
      r.onerror = () => rej(r.error);
    });
  } finally { db.close(); }
}

export async function deleteFile(id: string): Promise<void> {
  const db = await openDb();
  try {
    await new Promise<void>((res, rej) => {
      const t = db.transaction(STORE, 'readwrite');
      t.objectStore(STORE).delete(id);
      t.oncomplete = () => res();
      t.onerror = () => rej(t.error);
    });
  } finally { db.close(); }
}

export function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.onerror = () => reject(fr.error);
    fr.onload = () => {
      const res = String(fr.result);
      const comma = res.indexOf(',');
      resolve(comma >= 0 ? res.slice(comma + 1) : res);
    };
    fr.readAsDataURL(blob);
  });
}

export function base64ToBlob(b64: string, type: string): Blob {
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return new Blob([bytes], { type });
}

export type Validation = { ok: true } | { ok: false; reason: string };
export function validateFile(file: File): Validation {
  if (file.size > MAX_BYTES) return { ok: false, reason: 'over 10 MB' };
  const ext = (file.name.split('.').pop() || '').toLowerCase();
  const ok = ALLOWED_TYPES.mime.includes(file.type) || ALLOWED_TYPES.ext.includes(ext);
  return ok ? { ok: true } : { ok: false, reason: 'unsupported type' };
}

export function humanSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function genId(): string {
  const c = (globalThis as { crypto?: Crypto }).crypto;
  if (c?.randomUUID) return c.randomUUID();
  if (c?.getRandomValues) {
    const b = c.getRandomValues(new Uint8Array(16));
    return Array.from(b, x => x.toString(16).padStart(2, '0')).join('');
  }
  return `${Date.now().toString(16)}-${Math.random().toString(16).slice(2)}`;
}

export type ExportRecord = Omit<AssessmentRecord, 'evidence'> & { evidence?: Record<string, EvidenceExport[]> };

export async function buildExportRecord(
  rubric: UseCase[], responses: Record<string, Response>,
  evidence: Record<string, EvidenceMeta[]>, generated: string,
  load: (id: string) => Promise<Blob | null> = getBlob,
): Promise<{ record: ExportRecord; skipped: number }> {
  const record = buildRecord(rubric, responses, generated) as ExportRecord;
  let skipped = 0;
  const ev: Record<string, EvidenceExport[]> = {};
  for (const [uc, list] of Object.entries(evidence)) {
    const out: EvidenceExport[] = [];
    for (const m of list) {
      const blob = await load(m.id);
      if (!blob) { skipped++; continue; }
      out.push({ ...m, data: await blobToBase64(blob) });
    }
    if (out.length) ev[uc] = out;
  }
  if (Object.keys(ev).length) record.evidence = ev;
  return { record, skipped };
}

export async function restoreEvidence(
  current: Record<string, EvidenceMeta[]>,
  parsed: unknown,
  knownId: (id: string) => boolean,
): Promise<{ evidence: Record<string, EvidenceMeta[]>; skipped: number }> {
  const merged: Record<string, EvidenceMeta[]> = { ...current };
  let skipped = 0;
  const src = (parsed && typeof parsed === 'object') ? parsed as Record<string, unknown> : {};
  for (const [uc, list] of Object.entries(src)) {
    if (!knownId(uc) || !Array.isArray(list)) continue;
    const metas: EvidenceMeta[] = [];
    for (const e of list as EvidenceExport[]) {
      if (!e || typeof e.data !== 'string' || typeof e.id !== 'string') { skipped++; continue; }
      try {
        await putFile(e.id, base64ToBlob(e.data, e.type || 'application/octet-stream'));
        metas.push({ id: e.id, name: String(e.name ?? e.id), type: String(e.type ?? ''), size: Number(e.size ?? 0), added: String(e.added ?? '') });
      } catch { skipped++; }
    }
    // Replace the uc's list only when we produced new metas, or the incoming list was
    // intentionally empty. A non-empty list that yielded nothing (all malformed) keeps
    // the existing evidence rather than silently destroying it.
    if (metas.length || list.length === 0) {
      for (const old of current[uc] ?? []) {
        if (!metas.some(m => m.id === old.id)) await deleteFile(old.id).catch(() => {});
      }
      merged[uc] = metas;
    }
  }
  return { evidence: merged, skipped };
}
