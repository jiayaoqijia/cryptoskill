import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts"],
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
  external: ["express", "@x402-kit/shared"],
});
