import type { UseCase } from './types';
import secrets from '../data/rubric.secrets.json';
import pam from '../data/rubric.pam.json';
import iga from '../data/rubric.iga.json';

export type DomainId = 'secrets' | 'pam' | 'iga';

export interface Domain { id: DomainId; label: string; rubric: UseCase[]; }

export const DOMAINS: Domain[] = [
  { id: 'secrets', label: 'Secrets Management', rubric: secrets as unknown as UseCase[] },
  { id: 'pam', label: 'Privileged Access (PAM)', rubric: pam as unknown as UseCase[] },
  { id: 'iga', label: 'Identity Governance (IGA)', rubric: iga as unknown as UseCase[] },
];

export const DEFAULT_DOMAIN: DomainId = 'secrets';

const BY_ID = new Map(DOMAINS.map(d => [d.id, d]));

/** Never throws into render: unknown ids resolve to the default domain. */
export function getDomain(id: DomainId): Domain {
  return BY_ID.get(id) ?? BY_ID.get(DEFAULT_DOMAIN)!;
}

export function isDomainId(v: unknown): v is DomainId {
  return typeof v === 'string' && BY_ID.has(v as DomainId);
}
