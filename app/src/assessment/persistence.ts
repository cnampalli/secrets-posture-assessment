import type { Response, State, EvidenceMeta, UseCase } from './types';
import { blankResponse, buildRecord } from './record';
import { DEFAULT_DOMAIN, type DomainId } from './domains';

const PREFIX = 'posture-assessment-record/v1';
const LEGACY_KEY = PREFIX; // the old single, un-namespaced key
const SCHEMA = 'posture-assessment-record/v1';
const STATES: State[] = ['GAP', 'PARTIAL', 'MET', 'PENDING', 'NA'];

export function keyFor(domainId: DomainId): string { return `${PREFIX}/${domainId}`; }

/** One-shot: fold a legacy un-namespaced record into the secrets namespace. */
export function migrateLegacy(): void {
  try {
    const legacy = localStorage.getItem(LEGACY_KEY);
    if (legacy === null) return;
    if (localStorage.getItem(keyFor(DEFAULT_DOMAIN)) === null) {
      localStorage.setItem(keyFor(DEFAULT_DOMAIN), legacy);
    }
    localStorage.removeItem(LEGACY_KEY);
  } catch { /* storage unavailable — nothing to migrate */ }
}

function rebuildResponses(stored: Record<string, unknown>): Record<string, Response> {
  const out: Record<string, Response> = {};
  for (const [id, s] of Object.entries(stored || {})) {
    const entry = s as Record<string, unknown>;
    out[id] = {
      answers: (entry.answers && typeof entry.answers === 'object') ? entry.answers as Record<string, never> : {},
      overridden: !!entry.overridden,
      final_state: STATES.includes(entry.final_state as State) ? (entry.final_state as State) : null,
      rationale: (entry.rationale as string) || '', confidence: (entry.confidence as 'LOW' | 'MED' | 'HIGH') || 'MED',
    };
  }
  return out;
}

export function loadResponses(domainId: DomainId): Record<string, Response> {
  try {
    const raw = localStorage.getItem(keyFor(domainId));
    if (!raw) return {};
    const rec = JSON.parse(raw);
    return rec && rec.responses ? rebuildResponses(rec.responses) : {};
  } catch { return {}; }
}

export function saveResponses(
  domainId: DomainId, rubric: UseCase[],
  responses: Record<string, Response>, generated: string,
  evidence?: Record<string, EvidenceMeta[]>,
): void {
  try { localStorage.setItem(keyFor(domainId), JSON.stringify(buildRecord(rubric, responses, generated, evidence))); }
  catch { /* quota / unavailable — caller may toast */ }
}

export function loadEvidence(domainId: DomainId): Record<string, EvidenceMeta[]> {
  try {
    const raw = localStorage.getItem(keyFor(domainId));
    if (!raw) return {};
    const rec = JSON.parse(raw);
    const ev = rec && rec.evidence;
    if (!ev || typeof ev !== 'object') return {};
    const out: Record<string, EvidenceMeta[]> = {};
    for (const [id, list] of Object.entries(ev)) if (Array.isArray(list)) out[id] = list as EvidenceMeta[];
    return out;
  } catch { return {}; }
}

export function importRecord(
  current: Record<string, Response>, text: string, knownId: (id: string) => boolean,
): Record<string, Response> {
  const rec = JSON.parse(text) as Record<string, unknown>;
  if (!rec || rec['schema'] !== SCHEMA) throw new Error('unrecognised schema');
  const merged = { ...current };
  for (const [id, s] of Object.entries((rec['responses'] as Record<string, unknown>) || {})) {
    if (!knownId(id)) continue;
    const entry = s as Record<string, unknown>;
    merged[id] = { ...blankResponse(),
      answers: (entry.answers && typeof entry.answers === 'object') ? entry.answers as Record<string, never> : {},
      overridden: !!entry.overridden,
      final_state: STATES.includes(entry.final_state as State) ? (entry.final_state as State) : null,
      rationale: (entry.rationale as string) || '', confidence: (entry.confidence as 'LOW' | 'MED' | 'HIGH') || 'MED' };
  }
  return merged;
}
