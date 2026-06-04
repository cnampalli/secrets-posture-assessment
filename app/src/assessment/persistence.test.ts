import { describe, it, test, expect, beforeEach } from 'vitest';
import { loadResponses, saveResponses, importRecord, loadEvidence, STORE_KEY } from './persistence';
import { blankResponse } from './record';
import { RUBRIC } from './rubric';
import type { Response, EvidenceMeta } from './types';

beforeEach(() => localStorage.clear());

describe('persistence', () => {
  it('round-trips responses through localStorage', () => {
    const responses: Record<string, Response> = { 'UC-F-001': { ...blankResponse(), rationale: 'hi' } };
    saveResponses(responses, '2026-01-01T00:00:00Z');
    expect(localStorage.getItem(STORE_KEY)).toContain('posture-assessment-record/v1');
    expect(loadResponses()['UC-F-001'].rationale).toBe('hi');
  });
  it('loads empty when nothing saved or corrupt', () => {
    expect(loadResponses()).toEqual({});
    localStorage.setItem(STORE_KEY, '{not json');
    expect(loadResponses()).toEqual({});
  });
  it('importRecord merges valid responses and rejects wrong schema', () => {
    const existing: Record<string, Response> = { 'UC-F-002': { ...blankResponse(), rationale: 'keep' } };
    const incoming = JSON.stringify({ schema: 'posture-assessment-record/v1', responses: {
      'UC-F-001': { answers: { Q1: 'no' }, final_state: 'GAP', overridden: true, rationale: 'r', confidence: 'HIGH' } } });
    const merged = importRecord(existing, incoming, id => id.startsWith('UC-'));
    expect(merged['UC-F-002'].rationale).toBe('keep');      // existing kept
    expect(merged['UC-F-001'].final_state).toBe('GAP');     // incoming merged
    expect(() => importRecord(existing, JSON.stringify({ schema: 'wrong' }), () => true)).toThrow();
  });
});

test('saveResponses persists evidence metadata; loadEvidence reads it back', () => {
  const ev: Record<string, EvidenceMeta[]> = {
    [RUBRIC[0].uc_id]: [{ id: 'p1', name: 'a.pdf', type: 'application/pdf', size: 9, added: 'T' }],
  };
  saveResponses({}, 'T', ev);
  expect(loadEvidence()).toEqual(ev);
});

test('loadEvidence returns {} when nothing stored', () => {
  localStorage.clear();
  expect(loadEvidence()).toEqual({});
});
