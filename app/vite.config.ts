import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { viteSingleFile } from 'vite-plugin-singlefile';

export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: {
    cssCodeSplit: false,
    assetsInlineLimit: 100_000_000, // inline ALL assets (fonts) as base64
    chunkSizeWarningLimit: 100_000,
    // viteSingleFile already disables code-splitting, so inlineDynamicImports
    // would be a redundant no-op (and emits a warning) — intentionally omitted.
  },
});
