import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import commonjs from '@rollup/plugin-commonjs'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), commonjs()],
  resolve: {
    alias: [
      {
        find: './runtimeConfig',
        replacement: './runtimeConfig.browser', // ensures browser-compatible version of AWS JS SDK is used
      },
    ],
  },
  optimizeDeps: {
    include: ['i18n-iso-countries'], // explicitly include the module in optimized deps
  },
  build: {
    commonjsOptions: {
      include: [/node_modules/], // include all node_modules for commonjs
      transformMixedEsModules: true, // allow mixed esmodules and commonjs
    },
  },
})