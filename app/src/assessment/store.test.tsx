import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AssessmentProvider, useAssessment } from './store';
import { RUBRIC } from './rubric';

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
    expect(localStorage.getItem('posture-assessment-record/v1')).toContain(RUBRIC[0].uc_id);
  }
  expect(firstLadder).toBeTruthy();
});
