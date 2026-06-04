import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AssessmentProvider } from '../assessment/store';
import { ToastProvider } from './Toast';
import { EvidencePanel } from './EvidencePanel';

function setup() {
  localStorage.clear();
  return render(
    <ToastProvider><AssessmentProvider><EvidencePanel /></AssessmentProvider></ToastProvider>
  );
}

test('shows the dropzone and empty state', () => {
  setup();
  expect(screen.getByText(/click to browse/i)).toBeInTheDocument();
});

test('attaching a file shows a chip with its name; remove clears it', async () => {
  setup();
  const input = screen.getByTestId('evidence-input') as HTMLInputElement;
  const file = new File([new Uint8Array([1, 2, 3])], 'policy.pdf', { type: 'application/pdf' });
  fireEvent.change(input, { target: { files: [file] } });
  await waitFor(() => expect(screen.getByText('policy.pdf')).toBeInTheDocument());
  fireEvent.click(screen.getByRole('button', { name: /remove policy.pdf/i }));
  await waitFor(() => expect(screen.queryByText('policy.pdf')).not.toBeInTheDocument());
});
