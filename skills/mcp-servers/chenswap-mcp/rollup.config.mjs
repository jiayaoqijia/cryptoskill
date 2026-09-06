import typescript from '@rollup/plugin-typescript';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import json from '@rollup/plugin-json';

export default {
  input: 'src/index.ts',
  output: {
    file: 'dist/index.js',
    format: 'esm',
    banner: '#!/usr/bin/env node',
    sourcemap: false,
    inlineDynamicImports: true,
  },
  external: [
    // Keep Node built-ins external
    /^node:/,
  ],
  plugins: [
    json(),
    resolve({ preferBuiltins: true, exportConditions: ['node'] }),
    commonjs(),
    typescript({ tsconfig: './tsconfig.json' }),
  ],
};