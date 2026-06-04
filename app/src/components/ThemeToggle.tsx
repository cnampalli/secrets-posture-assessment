import { useTheme } from '../theme/ThemeProvider';
import { Button } from './ui';
export function ThemeToggle() {
  const { theme, toggle } = useTheme();
  return <Button variant="outline" onClick={toggle} aria-label="Toggle theme">{theme === 'light' ? '◐ Light' : '◑ Dark'}</Button>;
}
