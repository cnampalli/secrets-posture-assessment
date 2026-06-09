import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AssessmentProvider } from '../assessment/store';
import { UseCaseView } from './UseCaseView';
import { makeRubric } from '../assessment/rubric';
import { DEFAULT_DOMAIN } from '../assessment/domains';

const RUBRIC = makeRubric(DEFAULT_DOMAIN).rubric;

beforeEach(() => localStorage.clear());

it('answering ladder questions updates the proposed state chip', async () => {
  // pick the first ladder UC and render directly
  const ladder = RUBRIC.find(u => u.kind === 'ladder')!;
  render(<AssessmentProvider><UseCaseView startId={ladder.uc_id} /></AssessmentProvider>);
  expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
  // answer every question "yes" -> MET appears in the panel
  const yesButtons = screen.getAllByRole('button', { name: 'Yes' });
  for (const b of yesButtons) await userEvent.click(b);
  expect(screen.getAllByText(/MET/).length).toBeGreaterThan(0);
});

it('offers an Export affordance on the last use case instead of a dead-end next', () => {
  const last = RUBRIC[RUBRIC.length - 1];
  render(<AssessmentProvider><UseCaseView startId={last.uc_id} /></AssessmentProvider>);
  // the misleading disabled "Save & next" is replaced by an enabled export action
  expect(screen.queryByRole('button', { name: /save & next/i })).toBeNull();
  expect(screen.getByRole('button', { name: /export record/i })).toBeEnabled();
});

it('keeps Save & next on a non-last use case', () => {
  render(<AssessmentProvider><UseCaseView startId={RUBRIC[0].uc_id} /></AssessmentProvider>);
  expect(screen.getByRole('button', { name: /save & next/i })).toBeInTheDocument();
  expect(screen.queryByRole('button', { name: /export record/i })).toBeNull();
});

it('lists unscored use cases on the last screen and lets you jump to one', async () => {
  const last = RUBRIC[RUBRIC.length - 1];
  render(<AssessmentProvider><UseCaseView startId={last.uc_id} /></AssessmentProvider>);
  // nothing scored yet -> the first UC shows as an unscored jump link
  const first = RUBRIC[0];
  const link = screen.getByRole('button', { name: new RegExp(first.uc_id) });
  await userEvent.click(link);
  expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(first.title || first.uc_id);
});
