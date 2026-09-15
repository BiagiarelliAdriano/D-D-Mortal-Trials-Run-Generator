import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
    esbuild: {
        loader: 'jsx',
        include: /src\/.*\.[jt]sx?$/,
        exclude: []
    },
    optimizeDeps: {
        esbuildOptions: {
            loader: {
                '.js': 'jsx'
            }
        }
    },
    build: {
        outDir: 'build',
        rollupOptions: {
            output: {
                manualChunks: {
                    router: ['react-router-dom'],
                    grid: ['react-grid-layout', 'react-resizable', 'react-draggable'],
                    utilities: ['dompurify', 'lodash']
                }
            }
        }
    },
    server: {
        host: '127.0.0.1',
        port: 3000,
        proxy: {
            '/api': 'http://localhost:5000',
            '/auth': 'http://localhost:5000'
        }
    },
    test: {
        environment: 'jsdom',
        setupFiles: './src/setupTests.js',
        globals: true
    }
});
