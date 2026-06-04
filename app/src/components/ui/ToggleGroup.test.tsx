import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { useState } from 'react';
import { ToggleGroup } from './ToggleGroup';

function Harness() {
  const [v, setV] = useState<string | null>('no');
  return <ToggleGroup value={v} onChange={setV}
    options={[{ value: 'yes', label: 'Yes' }, { value: 'no', label: 'No' }, { value: 'na', label: 'N/A' }]} />;
}

test('marks the selected option pressed and changes on click', async () => {
  render(<Harness />);
  expect(screen.getByRole('button', { name: 'No' })).toHaveAttribute('aria-pressed', 'true');
  await userEvent.click(screen.getByRole('button', { name: 'Yes' }));
  expect(screen.getByRole('button', { name: 'Yes' })).toHaveAttribute('aria-pressed', 'true');
});

test('clicking the active option clears it (toggle off)', async () => {
  render(<Harness />);
  await userEvent.click(screen.getByRole('button', { name: 'No' }));
  expect(screen.getByRole('button', { name: 'No' })).toHaveAttribute('aria-pressed', 'false');
});
