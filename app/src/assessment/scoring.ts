import type { Question, Answer, State } from './types';

const VALID: Answer[] = ['yes', 'no', 'na'];

export function deriveState(
  questions: Pick<Question, 'qid' | 'informs_state'>[],
  answers: Record<string, Answer | null | undefined>,
): State {
  // Empty is a programming error (archetype UCs always have questions; bespoke is
  // scored manually and never reaches here) — throw rather than silently fall
  // through to MET, which would mark an unassessed use case as fully covered.
  if (questions.length === 0) throw new Error('deriveState requires at least one question');
  const vals = questions.map(q => [q.informs_state, answers[q.qid] ?? null] as const);
  if (vals.length && vals.every(([, v]) => v === 'na')) return 'NA';
  if (vals.some(([, v]) => v == null || !VALID.includes(v as Answer))) return 'PENDING';
  if (vals.some(([inf, v]) => inf === 'GAP_PARTIAL' && v === 'no')) return 'GAP';
  if (vals.some(([inf, v]) => inf === 'PARTIAL_MET' && v === 'no')) return 'PARTIAL';
  return 'MET';
}
