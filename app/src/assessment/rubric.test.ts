import { describe, it, expect } from 'vitest';
import { makeRubric } from './rubric';
import { DEFAULT_DOMAIN } from './domains';

const view = makeRubric(DEFAULT_DOMAIN);
const RUBRIC = view.rubric;

describe('rubric', () => {
  it('loads 47 use cases', () => { expect(RUBRIC.length).toBe(47); });
  it('every use case has the required shape', () => {
    for (const uc of RUBRIC) {
      expect(uc.uc_id).toBeTruthy();
      expect(['Functional', 'Non-functional']).toContain(uc.category);
      expect(['bespoke', 'ladder']).toContain(uc.kind);
      if (uc.kind === 'ladder') expect(uc.questions!.length).toBeGreaterThan(0);
      else expect(Array.isArray(uc.sub_criteria)).toBe(true);
    }
  });
  it('groups by category and indexes by id', () => {
    const g = view.byCategory();
    expect(Object.keys(g)).toEqual(expect.arrayContaining(['Functional', 'Non-functional']));
    expect(view.byId(RUBRIC[0].uc_id)).toBe(RUBRIC[0]);
  });
});
