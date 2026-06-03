import { render, screen } from '@testing-library/react';
import { Button } from './Button';

test('renders default (primary) button with accent background', () => {
  render(<Button>Save</Button>);
  const b = screen.getByRole('button', { name: 'Save' });
  expect(b).toHaveClass('bg-accent');
});

test('outline variant uses border, not accent fill', () => {
  render(<Button variant="outline">Import</Button>);
  const b = screen.getByRole('button', { name: 'Import' });
  expect(b).toHaveClass('border-border');
  expect(b).not.toHaveClass('bg-accent');
});
