import { render, screen } from '@testing-library/react';
import { Badge } from './Badge';

test('state badge maps state to its colour token class', () => {
  render(<Badge state="gap">GAP</Badge>);
  expect(screen.getByText('GAP')).toHaveClass('text-gap');
});
