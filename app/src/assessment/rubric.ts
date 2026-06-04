import type { UseCase } from './types';
import data from '../data/rubric.json';

export const RUBRIC = data as unknown as UseCase[];
const INDEX = new Map(RUBRIC.map(uc => [uc.uc_id, uc]));

export function byId(uc_id: string): UseCase | undefined { return INDEX.get(uc_id); }

export function byCategory(): Record<string, UseCase[]> {
  const out: Record<string, UseCase[]> = {};
  for (const uc of RUBRIC) (out[uc.category] ||= []).push(uc);
  return out;
}
