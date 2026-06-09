import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AssessmentProvider, useAssessment } from '../assessment/store';
import { DomainPicker } from './DomainPicker';

function Probe() { const a = useAssessment(); return <span data-testid="dom">{a.domainId}</span>; }

describe('DomainPicker', () => {
  beforeEach(() => localStorage.clear());

  it('lists both domains and switches the active domain', async () => {
    render(<AssessmentProvider><DomainPicker /><Probe /></AssessmentProvider>);
    const select = screen.getByLabelText(/assessment domain/i) as HTMLSelectElement;
    expect(select.value).toBe('secrets');
    expect(screen.getByRole('option', { name: /Privileged Access/ })).toBeInTheDocument();
    await userEvent.selectOptions(select, 'pam');
    expect(screen.getByTestId('dom').textContent).toBe('pam');
  });
});
