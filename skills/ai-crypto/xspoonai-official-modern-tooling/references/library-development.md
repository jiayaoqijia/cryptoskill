---
name: library-development
description: Guidelines for building and publishing modern TypeScript libraries. Covers bundling, ESM support, and release management.
---

# Library Development Standards

## Bundling Strategy

We recommend using modern bundlers like **tsdown**, **tsup**, or **unbuild** for efficient TypeScript compilation.

| Aspect          | Recommendation                                                |
| :-------------- | :------------------------------------------------------------ |
| **Format**      | Pure ESM (`.mjs`) is preferred for modern compatibility.      |
| **CJS Support** | Optional. Only include if supporting legacy Node.js versions. |
| **Types**       | Always generate `.d.ts` declaration files.                    |
| **Source Maps** | Enable for better debugging experience.                       |

## Configuration (tsdown / tsup)

### Using `tsdown` (Recommended)

`tsdown` is optimized for zero-config usage and automatic `exports` generation.

```ts
// tsdown.config.ts
import { defineConfig } from "tsdown";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["esm"],
  dts: true,
  clean: true,
  // Automatically updates package.json exports
  exports: true,
});
```

### Using `tsup`

`tsup` is a popular alternative powered by esbuild.

```ts
// tsup.config.ts
import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["esm", "cjs"], // Dual build example
  dts: true,
  clean: true,
});
```

## Package Configuration (`package.json`)

Ensure your `package.json` is configured for modern module resolution.

```json
{
  "name": "my-library",
  "version": "1.0.0",
  "type": "module",
  "main": "./dist/index.mjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.mts",
  "files": ["dist"],
  "exports": {
    ".": {
      "types": "./dist/index.d.mts",
      "import": "./dist/index.mjs"
    }
  },
  "scripts": {
    "build": "tsdown",
    "dev": "tsdown --watch",
    "prepack": "pnpm build",
    "test": "vitest",
    "release": "bumpp"
  }
}
```

### Key Scripts

- **`prepack`**: Runs `pnpm build` automatically before publishing to ensure artifacts are fresh.
- **`release`**: Uses `bumpp` for interactive versioning, tagging, and pushing to Git.

## Release Workflow

We recommend using **bumpp** to streamline the release process.

```bash
pnpm release
# Interactive prompts:
# 1. Select version increment (patch/minor/major)
# 2. Update package.json
# 3. Create git tag
# 4. Commit changes
# 5. Push to remote
```
