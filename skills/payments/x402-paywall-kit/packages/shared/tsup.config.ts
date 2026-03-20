import { defineConfig } from "tsup";

export default defineConfig({
  entry: {
    index: "src/index.ts",
    "types/index": "src/types/index.ts",
    "policy/index": "src/policy/index.ts",
    "logger/index": "src/logger/index.ts",
  },
  format: ["cjs", "esm"],
  dts: {
    compilerOptions: {
      composite: false,
    },
  },
  outDir: "dist",
  outExtension({ format }) {
    return {
      js: format === "esm" ? ".mjs" : ".js",
      dts: format === "esm" ? ".d.mts" : ".d.ts",
    };
  },
  clean: true,
  splitting: false,
});
