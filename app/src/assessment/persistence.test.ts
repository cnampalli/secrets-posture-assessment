import { describe, it, test, expect, beforeEach } from 'vitest';
import { keyFor, migrateLegacy, loadResponses, saveResponses, importRecord, loadEvidence } from './persistence';
import { blankResponse } from './record';
import { makeRubric } from './rubric';
import type { Response, EvidenceMeta } from './types';

const SECRETS = makeRubric('secrets').rubric;
const PAM = makeRubric('pam').rubric;

beforeEach(() => localStorage.clear());

describe('persistence (per-domain)', () => {
  it('round-trips responses through the domain-scoped key', () => {
    const responses: Record<string, Response> = { 'UC-F-001': { ...blankResponse(), rationale: 'hi' } };
    saveResponses('secrets', SECRETS, responses, '2026-01-01T00:00:00Z');
    expect(localStorage.getItem(keyFor('secrets'))).toContain('posture-assessment-record/v1');
    expect(loadResponses('secrets')['UC-F-001'].rationale).toBe('hi');
  });

  it('loads empty when nothing saved or corrupt', () => {
    expect(loadResponses('secrets')).toEqual({});
    localStorage.setItem(keyFor('secrets'), '{not json');
    expect(loadResponses('secrets')).toEqual({});
  });

  it('importRecord merges valid responses and rejects wrong schema', () => {
    const existing: Record<string, Response> = { 'UC-F-002': { ...blankResponse(), rationale: 'keep' } };
    const incoming = JSON.stringify({ schema: 'posture-assessment-record/v1', responses: {
      'UC-F-001': { answers: { Q1: 'no' }, final_state: 'GAP', overridden: true, rationale: 'r', confidence: 'HIGH' } } });
    const merged = importRecord(existing, incoming, id => id.startsWith('UC-'));
    expect(merged['UC-F-002'].rationale).toBe('keep');
    expect(merged['UC-F-001'].final_state).toBe('GAP');
    expect(() => importRecord(existing, JSON.stringify({ schema: 'wrong' }), () => true)).toThrow();
  });

  it('namespaces the storage key by domain', () => {
    expect(keyFor('secrets')).toBe('posture-assessment-record/v1/secrets');
    expect(keyFor('pam')).toBe('posture-assessment-record/v1/pam');
  });

  it('isolates domains: a PAM save is invisible to secrets', () => {
    const resp: Record<string, Response> = { 'UC-P-001': { ...blankResponse(), answers: { 'A4-Q1': 'yes' } } };
    saveResponses('pam', PAM, resp, '2026-01-01T00:00:00Z');
    expect(Object.keys(loadResponses('secrets'))).toHaveLength(0);
    expect(loadResponses('pam')['UC-P-001'].answers['A4-Q1']).toBe('yes');
  });

  it('migrates a legacy un-namespaced record into the secrets namespace', () => {
    localStorage.setItem('posture-assessment-record/v1', JSON.stringify({
      schema: 'posture-assessment-record/v1', generated: 'x',
      responses: { 'UC-F-001': { archetype: 'A1', answers: { 'A1-Q1': 'yes' }, proposed_state: 'PARTIAL', final_state: 'PARTIAL', overridden: false, rationale: '', confidence: 'MED' } },
    }));
    migrateLegacy();
    expect(localStorage.getItem(keyFor('secrets'))).toBeTruthy();
    expect(loadResponses('secrets')['UC-F-001'].answers['A1-Q1']).toBe('yes');
    expect(localStorage.getItem('posture-assessment-record/v1')).toBeNull();
  });

  it('migrateLegacy is a no-op when the secrets namespace already exists', () => {
    localStorage.setItem(keyFor('secrets'), JSON.stringify({ schema: 'posture-assessment-record/v1', generated: 'kept', responses: {} }));
    localStorage.setItem('posture-assessment-record/v1', JSON.stringify({ schema: 'posture-assessment-record/v1', generated: 'legacy', responses: {} }));
    migrateLegacy();
    expect(JSON.parse(localStorage.getItem(keyFor('secrets'))!).generated).toBe('kept');
  });
});

test('saveResponses persists evidence metadata; loadEvidence reads it back', () => {
  const ev: Record<string, EvidenceMeta[]> = {
    [SECRETS[0].uc_id]: [{ id: 'p1', name: 'a.pdf', type: 'application/pdf', size: 9, added: 'T' }],
  };
  saveResponses('secrets', SECRETS, {}, 'T', ev);
  expect(loadEvidence('secrets')).toEqual(ev);
});

test('loadEvidence returns {} when nothing stored', () => {
  localStorage.clear();
  expect(loadEvidence('secrets')).toEqual({});
});
