import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5203,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8203',
        changeOrigin: true
      }
    }
  },
  preview: {
    port: 6203,
    strictPort: true
  }
});
