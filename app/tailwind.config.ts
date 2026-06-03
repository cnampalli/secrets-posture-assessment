import type { Config } from 'tailwindcss';

const c = (name: string) => `var(--${name})`;
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: { display: c('font-display'), body: c('font-body'), mono: c('font-mono') },
      borderRadius: { xs: c('radius-xs'), sm: c('radius-sm'), md: c('radius-md'), lg: c('radius-lg'), pill: c('radius-pill') },
      colors: {
        bg: c('bg'), bg2: c('bg2'), card: c('card'),
        ink: c('ink'), ink2: c('ink2'), muted: c('muted'), faint: c('faint'),
        border: c('border'), 'border-strong': c('border-strong'),
        accent: { DEFAULT: c('accent'), fg: c('accent-fg'), soft: c('accent-soft'), bd: c('accent-bd') },
        met: { DEFAULT: c('met'), soft: c('met-soft') },
        partial: { DEFAULT: c('partial'), soft: c('partial-soft') },
        gap: { DEFAULT: c('gap'), soft: c('gap-soft') },
        pending: { DEFAULT: c('pending'), soft: c('pending-soft') },
        na: { DEFAULT: c('na'), soft: c('na-soft') },
      },
    },
  },
  plugins: [],
} satisfies Config;
