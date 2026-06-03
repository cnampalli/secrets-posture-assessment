import type { UseCase, Response, State, AssessmentRecord } from './types';
import { deriveState } from './scoring';

const SCHEMA = 'posture-assessment-record/v1' as const;

export function blankResponse(): Response {
  return { answers: {}, overridden: false, final_state: null, rationale: '', confidence: 'MED' };
}

export function proposedFor(uc: UseCase, r: Response): State | null {
  if (uc.kind === 'bespoke') return null;
  return deriveState(uc.questions ?? [], r.answers as Record<string, never>);
}

export function finalFor(uc: UseCase, r: Response): State {
  if (r.overridden && r.final_state) return r.final_state;
  return proposedFor(uc, r) ?? r.final_state ?? 'PENDING';
}

export function scoredCount(rubric: UseCase[], responses: Record<string, Response>): number {
  return rubric.filter(uc => {
    const r = responses[uc.uc_id];
    const p = r ? proposedFor(uc, r) : null;
    return (p && p !== 'PENDING') || (uc.kind === 'bespoke' && r && r.final_state);
  }).length;
}

export function buildRecord(
  rubric: UseCase[], responses: Record<string, Response>, generated: string,
): AssessmentRecord {
  const out: AssessmentRecord = { schema: SCHEMA, generated, responses: {} };
  for (const uc of rubric) {
    const r = responses[uc.uc_id];
    if (!r) continue;
    out.responses[uc.uc_id] = {
      archetype: uc.archetype, answers: r.answers,
      proposed_state: proposedFor(uc, r), final_state: finalFor(uc, r),
      overridden: !!r.overridden, rationale: r.rationale || '', confidence: r.confidence || 'MED',
    };
  }
  return out;
}
