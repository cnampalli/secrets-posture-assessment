import { describe, it, expect, beforeEach, test } from 'vitest';
import { render, screen, act, renderHook } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { ReactNode } from 'react';
import { AssessmentProvider, useAssessment } from './store';
import { RUBRIC } from './rubric';
import { keyFor } from './persistence';

beforeEach(() => localStorage.clear());

function Probe() {
  const a = useAssessment();
  const uc = a.current;
  return (
    <div>
      <span data-testid="id">{uc.uc_id}</span>
      <span data-testid="final">{a.finalOf(uc.uc_id)}</span>
      <span data-testid="scored">{a.scored}</span>
      {uc.kind === 'ladder' && uc.questions!.map(q => (
        <button key={q.qid} onClick={() => a.answer(q.qid, 'no')}>{`ans-${q.qid}`}</button>
      ))}
    </div>
  );
}

function pdf(name = 'a.pdf') {
  return new File([new Uint8Array([1, 2, 3])], name, { type: 'application/pdf' });
}
const wrapper = ({ children }: { children: ReactNode }) => <AssessmentProvider>{children}</AssessmentProvider>;

test('addEvidence stores a file under the current uc; evidenceFor returns it; removeEvidence clears it', async () => {
  localStorage.clear();
  const { result } = renderHook(() => useAssessment(), { wrapper });
  const uc = result.current.current.uc_id;
  let res: { added: number; rejected: string[] };
  await act(async () => { res = await result.current.addEvidence([pdf()] as unknown as FileList); });
  expect(res!.added).toBe(1);
  expect(result.current.evidenceFor(uc)).toHaveLength(1);
  const id = result.current.evidenceFor(uc)[0].id;
  await act(async () => { await result.current.removeEvidence(id); });
  expect(result.current.evidenceFor(uc)).toHaveLength(0);
});

test('addEvidence rejects an oversize file with a reason', async () => {
  localStorage.clear();
  const big = new File([new Uint8Array(2)], 'big.pdf', { type: 'application/pdf' });
  Object.defineProperty(big, 'size', { value: 11 * 1024 * 1024 });
  const { result } = renderHook(() => useAssessment(), { wrapper });
  let res: { added: number; rejected: string[] };
  await act(async () => { res = await result.current.addEvidence([big] as unknown as FileList); });
  expect(res!.added).toBe(0);
  expect(res!.rejected[0]).toMatch(/10 MB/);
});

test('export then import round-trips evidence', async () => {
  localStorage.clear();
  const { result } = renderHook(() => useAssessment(), { wrapper });
  const uc = result.current.current.uc_id;
  await act(async () => { await result.current.addEvidence([pdf('round.pdf')] as unknown as FileList); });
  let text = '';
  await act(async () => { text = (await result.current.exportRecord()).text; });
  const fresh = renderHook(() => useAssessment(), { wrapper });
  await act(async () => { await fresh.result.current.importText(text); });
  expect(fresh.result.current.evidenceFor(uc).map(m => m.name)).toEqual(['round.pdf']);
});

it('answering a ladder question updates derived state + persists', async () => {
  render(<AssessmentProvider><Probe /></AssessmentProvider>);
  const firstLadder = RUBRIC.find(u => u.kind === 'ladder')!;
  expect(screen.getByTestId('id').textContent).toBe(RUBRIC[0].uc_id);
  // Answer all questions of the first UC with 'no' — a GAP_PARTIAL 'no' resolves to GAP
  if (RUBRIC[0].kind === 'ladder') {
    for (const q of RUBRIC[0].questions!) {
      await userEvent.click(screen.getByText(`ans-${q.qid}`));
    }
    expect(['GAP', 'PARTIAL', 'MET', 'NA']).toContain(screen.getByTestId('final').textContent);
    expect(localStorage.getItem(keyFor('secrets'))).toContain(RUBRIC[0].uc_id);
  }
  expect(firstLadder).toBeTruthy();
});

describe('domain-aware store', () => {
  beforeEach(() => localStorage.clear());

  function probe() {
    const api: { current: ReturnType<typeof useAssessment> | null } = { current: null };
    function Probe() { api.current = useAssessment(); return null; }
    render(<AssessmentProvider><Probe /></AssessmentProvider>);
    return api;
  }

  it('defaults to secrets and exposes its rubric', () => {
    const api = probe();
    expect(api.current!.domainId).toBe('secrets');
    expect(api.current!.rubric.length).toBe(47);
  });

  it('setDomain swaps to PAM and its 17-UC rubric', () => {
    const api = probe();
    act(() => api.current!.setDomain('pam'));
    expect(api.current!.domainId).toBe('pam');
    expect(api.current!.rubric.length).toBe(17);
    expect(api.current!.current.uc_id.startsWith('UC-P-')).toBe(true);
    const total = Object.values(api.current!.byCategory()).reduce((n, l) => n + l.length, 0);
    expect(total).toBe(17);
  });

  it('isolates responses across domains', () => {
    const api = probe();
    act(() => { api.current!.go('UC-F-001'); api.current!.answer('A1-Q1', 'yes'); });
    act(() => api.current!.setDomain('pam'));
    expect(Object.keys(api.current!.responses)).toHaveLength(0);
    act(() => api.current!.setDomain('secrets'));
    expect(api.current!.responses['UC-F-001'].answers['A1-Q1']).toBe('yes');
  });

  it('persists the selected domain across remounts', () => {
    const a1 = probe();
    act(() => a1.current!.setDomain('pam'));
    const a2 = probe();
    expect(a2.current!.domainId).toBe('pam');
  });
});
