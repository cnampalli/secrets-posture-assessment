import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test-setup.ts'],
    pool: 'forks',
    typecheck: { tsconfig: './tsconfig.test.json' },
    environmentOptions: {
      jsdom: {
        url: 'http://localhost/',
      },
    },
  },
});
