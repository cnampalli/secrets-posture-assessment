import { describe, it, expect, test } from 'vitest';
import { proposedFor, finalFor, scoredCount, buildRecord, blankResponse } from './record';
import type { UseCase, Response } from './types';
import { RUBRIC } from './rubric';
import type { EvidenceMeta } from './types';

const ladder: UseCase = {
  uc_id: 'UC-F-001', title: 'X', category: 'Functional', archetype: 'A1', archetype_name: 'A1',
  kind: 'ladder', questions: [
    { qid: 'Q1', dimension: 'd', informs_state: 'GAP_PARTIAL', text: 't' },
    { qid: 'Q2', dimension: 'd', informs_state: 'PARTIAL_MET', text: 't' }],
};
const bespoke: UseCase = {
  uc_id: 'UC-N-001', title: 'Y', category: 'Non-functional', archetype: 'A0', archetype_name: 'A0',
  kind: 'bespoke', sub_criteria: [{ sub_id: 'S1', sub_criterion: 'c', question: 'q', evidence: 'e' }],
};
const resp = (o: Partial<Response> = {}): Response =>
  ({ ...blankResponse(), ...o });

describe('record model', () => {
  it('proposedFor: ladder derives, bespoke is null', () => {
    expect(proposedFor(ladder, resp({ answers: { Q1: 'yes', Q2: 'yes' } }))).toBe('MET');
    expect(proposedFor(bespoke, resp())).toBeNull();
  });
  it('finalFor: override wins; else proposed; else PENDING', () => {
    expect(finalFor(ladder, resp({ answers: { Q1: 'no', Q2: 'yes' } }))).toBe('GAP');
    expect(finalFor(ladder, resp({ overridden: true, final_state: 'MET', answers: { Q1: 'no', Q2: 'yes' } }))).toBe('MET');
    expect(finalFor(bespoke, resp())).toBe('PENDING');
    expect(finalFor(bespoke, resp({ final_state: 'MET' }))).toBe('MET');
  });
  it('scoredCount counts derived (non-pending) ladders + bespoke with final_state', () => {
    const responses = {
      'UC-F-001': resp({ answers: { Q1: 'yes', Q2: 'yes' } }),  // MET -> counts
      'UC-N-001': resp({ final_state: 'MET' }),                  // bespoke set -> counts
    };
    expect(scoredCount([ladder, bespoke], responses)).toBe(2);
    expect(scoredCount([ladder, bespoke], { 'UC-F-001': resp() })).toBe(0); // pending -> 0
  });
  it('buildRecord emits the v1 schema shape', () => {
    const rec = buildRecord([ladder], { 'UC-F-001': resp({ answers: { Q1: 'no', Q2: 'yes' }, rationale: 'r' }) }, '2026-01-01T00:00:00Z');
    expect(rec.schema).toBe('posture-assessment-record/v1');
    expect(rec.generated).toBe('2026-01-01T00:00:00Z');
    expect(rec.responses['UC-F-001']).toMatchObject({
      archetype: 'A1', proposed_state: 'GAP', final_state: 'GAP', overridden: false, rationale: 'r', confidence: 'MED',
    });
  });
});

test('buildRecord includes evidence metadata only when provided and non-empty', () => {
  const ev: Record<string, EvidenceMeta[]> = {
    [RUBRIC[0].uc_id]: [{ id: 'x', name: 'a.pdf', type: 'application/pdf', size: 5, added: '2026-06-05T00:00:00Z' }],
  };
  const withEv = buildRecord(RUBRIC, {}, 'T', ev);
  expect(withEv.evidence).toEqual(ev);
  expect('evidence' in buildRecord(RUBRIC, {}, 'T')).toBe(false);
  expect('evidence' in buildRecord(RUBRIC, {}, 'T', {})).toBe(false);
});
