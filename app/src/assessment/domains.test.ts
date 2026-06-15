import { describe, it, expect } from 'vitest';
import { DOMAINS, DEFAULT_DOMAIN, getDomain } from './domains';
import { makeRubric } from './rubric';

describe('domain registry', () => {
  it('registers secrets, pam and iga', () => {
    expect(DOMAINS.map(d => d.id).sort()).toEqual(['iga', 'pam', 'secrets']);
    expect(DEFAULT_DOMAIN).toBe('secrets');
  });

  it('carries the right rubric per domain', () => {
    expect(getDomain('secrets').rubric.length).toBe(50);   // M3.2: +3 agentic secrets UCs
    expect(getDomain('pam').rubric.length).toBe(21);        // M3.3: +3 agentic privileged-access UCs
    expect(getDomain('iga').rubric.length).toBe(19);   // M3.1: +3 agentic governance UCs
  });

  it('falls back to the default domain on an unknown id', () => {
    // @ts-expect-error exercising the runtime fallback
    expect(getDomain('nope').id).toBe('secrets');
  });
});

describe('makeRubric factory', () => {
  it('indexes and groups the active domain', () => {
    const pam = makeRubric('pam');
    expect(pam.byId('UC-P-017')?.archetype).toBe('A8');
    expect(pam.byId('NOPE')).toBeUndefined();
    const groups = pam.byCategory();
    expect(Object.keys(groups).length).toBeGreaterThan(0);
    const total = Object.values(groups).reduce((n, l) => n + l.length, 0);
    expect(total).toBe(21);
  });
});
