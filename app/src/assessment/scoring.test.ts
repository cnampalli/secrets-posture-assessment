import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { deriveState } from './scoring';
import type { Question, Answer } from './types';

// Single source of truth: the canonical vectors that pin JS↔Py scoring.
// Resolve from process.cwd() (app/) up to repo-root questionnaire/.
const vectorsPath = resolve(process.cwd(), '../questionnaire/scoring-vectors.json');
const vectors = JSON.parse(readFileSync(vectorsPath, 'utf8')) as Array<{
  name: string; questions: Pick<Question, 'qid' | 'informs_state'>[];
  answers: Record<string, Answer | null>; expected: string;
}>;

describe('deriveState parity', () => {
  for (const v of vectors) {
    it(v.name, () => {
      expect(deriveState(v.questions as Question[], v.answers as Record<string, Answer>)).toBe(v.expected);
    });
  }
  it('covers all 8 canonical vectors', () => { expect(vectors.length).toBe(8); });
  it('empty questions throws (H6: no silent MET on empty input)', () => {
    expect(() => deriveState([], {})).toThrow();
  });
});
