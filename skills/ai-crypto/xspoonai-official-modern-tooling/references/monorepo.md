---
name: monorepo
description: Guide to setting up and managing monorepos using pnpm workspaces and Turborepo.
---

# Monorepo Architecture

## Workspace Management (pnpm)

We recommend **pnpm workspaces** for efficient dependency management and disk space usage.

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
  - "tooling/*"
```

## Task Orchestration (Turborepo)

For large monorepos, use **Turborepo** to cache build artifacts and parallelize tasks.

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "lint": {},
    "test": {},
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

## Centralized Alias Strategy

To ensure consistent module resolution across different tools (Vite, Vitest, Nuxt, TypeScript), maintain a single source of truth for aliases.

### 1. Create `alias.ts`

```ts
// alias.ts
import { fileURLToPath } from "node:url";
import { resolve } from "node:path";

const r = (p: string) => fileURLToPath(new URL(p, import.meta.url));

export const alias = {
  "@myorg/core": r("./packages/core/src/index.ts"),
  "@myorg/utils": r("./packages/utils/src/index.ts"),
  "@myorg/ui": r("./packages/ui/src/index.ts"),
};
```

### 2. Use in Configs

**Vite / Vitest**:

```ts
// vite.config.ts
import { alias } from "./alias";

export default defineConfig({
  resolve: { alias },
});
```

**Nuxt**:

```ts
// nuxt.config.ts
import { alias } from "./alias";

export default defineNuxtConfig({
  alias,
});
```

### 3. Sync with TypeScript

You can automate the update of `tsconfig.json` paths using a script that reads `alias.ts`, or manually maintain `tsconfig.paths.json`.

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@myorg/core": ["packages/core/src/index.ts"],
      "@myorg/utils": ["packages/utils/src/index.ts"],
      "@myorg/ui": ["packages/ui/src/index.ts"]
    }
  }
}
```

## Best Practices

- **Shared Configs**: Create a `tooling/` or `packages/config` workspace to share ESLint, TypeScript, and Tailwind configurations.
- **Scoped Packages**: Use `@org/package-name` naming convention.
- **Consistent Scripts**: Ensure all packages have standard scripts like `build`, `test`, `lint`.
