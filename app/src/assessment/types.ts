export type State = 'GAP' | 'PARTIAL' | 'MET' | 'PENDING' | 'NA';
export type Answer = 'yes' | 'no' | 'na';
export type InformsState = 'GAP_PARTIAL' | 'PARTIAL_MET';

export interface Question { qid: string; dimension: string; informs_state: InformsState; text: string; }
export interface SubCriterion { sub_id: string; sub_criterion: string; question: string; evidence: string; }
export interface UseCase {
  uc_id: string; title: string; category: 'Functional' | 'Non-functional';
  archetype: string; archetype_name: string; kind: 'ladder' | 'bespoke';
  questions?: Question[]; sub_criteria?: SubCriterion[];
}
export interface Response {
  answers: Record<string, Answer | boolean>;
  overridden: boolean; final_state: State | null; rationale: string;
  confidence: 'LOW' | 'MED' | 'HIGH';
}
export interface AssessmentRecord {
  schema: 'posture-assessment-record/v1'; generated: string;
  responses: Record<string, {
    archetype: string; answers: Record<string, Answer | boolean>;
    proposed_state: State | null; final_state: State; overridden: boolean;
    rationale: string; confidence: 'LOW' | 'MED' | 'HIGH';
  }>;
}
