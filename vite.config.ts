import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
const base = process.env.VITE_DEPLOY_BASE ?? '/';
export default defineConfig({ base, plugins: [react()], build: { target: 'es2022', emptyOutDir: true } });
