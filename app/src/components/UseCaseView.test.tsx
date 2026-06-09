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
