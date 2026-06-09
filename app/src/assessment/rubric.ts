import type { UseCase } from './types';
import { getDomain, DEFAULT_DOMAIN, type DomainId } from './domains';

export interface RubricView {
  rubric: UseCase[];
  byId: (uc_id: string) => UseCase | undefined;
  byCategory: () => Record<string, UseCase[]>;
}

export function makeRubric(domainId: DomainId): RubricView {
  const rubric = getDomain(domainId).rubric;
  const index = new Map(rubric.map(uc => [uc.uc_id, uc]));
  return {
    rubric,
    byId: (uc_id) => index.get(uc_id),
    byCategory: () => {
      const out: Record<string, UseCase[]> = {};
      for (const uc of rubric) (out[uc.category] ||= []).push(uc);
      return out;
    },
  };
}

// --- Back-compat shims (default domain). Removed in the final task once every
// consumer reads the active rubric from the store. ---
const DEFAULT_VIEW = makeRubric(DEFAULT_DOMAIN);
export const RUBRIC = DEFAULT_VIEW.rubric;
export const byId = DEFAULT_VIEW.byId;
export function byCategory(): Record<string, UseCase[]> { return DEFAULT_VIEW.byCategory(); }
