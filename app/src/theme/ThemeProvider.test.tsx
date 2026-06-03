import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider, useTheme } from './ThemeProvider';

function Probe() {
  const { theme, toggle } = useTheme();
  return <button onClick={toggle}>theme:{theme}</button>;
}

beforeEach(() => { localStorage.clear(); document.documentElement.className = ''; });

test('defaults to light and applies no dark class', () => {
  render(<ThemeProvider><Probe /></ThemeProvider>);
  expect(screen.getByText('theme:light')).toBeInTheDocument();
  expect(document.documentElement).not.toHaveClass('dark');
});

test('toggles to dark, sets html class, and persists', async () => {
  render(<ThemeProvider><Probe /></ThemeProvider>);
  await userEvent.click(screen.getByRole('button'));
  expect(screen.getByText('theme:dark')).toBeInTheDocument();
  expect(document.documentElement).toHaveClass('dark');
  expect(localStorage.getItem('posture-theme')).toBe('dark');
});
