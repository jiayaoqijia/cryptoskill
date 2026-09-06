---
name: modern-tooling
description: Opinionated tooling and conventions for modern JavaScript/TypeScript projects. Use when setting up new projects, configuring ESLint/Prettier, monorepos, library publishing, or establishing coding standards.
version: 1.0.0
author: with-philia
license: MIT
tags: [TypeScript, JavaScript, Tooling, ESLint, Monorepo, Testing]
dependencies: [eslint, typescript, vitest, pnpm]
allowed-tools: Bash(ni, nr, nu)
---

# Modern Tooling & Standards

This skill provides a comprehensive guide to setting up and maintaining modern JavaScript and TypeScript projects. It covers coding practices, tooling choices, and configuration standards to ensure high code quality and developer productivity.

## Coding Practices

### Code Organization

- **Single Responsibility**: Each source file should have a clear, focused scope.
- **Modularization**: Break large files into smaller, manageable modules.
- **Type Separation**: Define types and interfaces in dedicated `types.ts` files or `types/` directories.
- **Constants**: Centralize constants in `constants.ts` to avoid magic numbers/strings.

### Runtime Environment

- **Isomorphic Code**: Strive for runtime-agnostic code that works across Node.js, browsers, and workers.
- **Environment Indicators**: Explicitly mark environment-specific code with comments:
  ```ts
  // @env node
  // @env browser
  ```

### TypeScript Best Practices

- **Explicit Returns**: Declare return types for functions to improve readability and catch errors early.
- **Type Definitions**: Avoid complex inline types; extract them into named `type` or `interface` definitions.
- **Strict Mode**: Always enable `strict: true` in `tsconfig.json`.

### Testing (Vitest)

- **Co-location**: Place test files next to source files (e.g., `foo.ts` → `foo.test.ts`).
- **BDD Style**: Use `describe` and `it` for structuring tests.
- **Snapshots**: Use `toMatchSnapshot` for complex object verification and `toMatchFileSnapshot` for large text outputs.

## Tooling Stack

### Package Management (`ni`)

We recommend using `ni` (npm i) to automatically detect and use the correct package manager (pnpm, yarn, npm).

| Command       | Description          | Equivalent (pnpm)          |
| :------------ | :------------------- | :------------------------- |
| `ni`          | Install dependencies | `pnpm i`                   |
| `ni <pkg>`    | Add dependency       | `pnpm add <pkg>`           |
| `ni -D <pkg>` | Add dev dependency   | `pnpm add -D <pkg>`        |
| `nr <script>` | Run script           | `pnpm run <script>`        |
| `nu`          | Upgrade dependencies | `pnpm update`              |
| `nun <pkg>`   | Uninstall dependency | `pnpm remove <pkg>`        |
| `nci`         | Clean install        | `pnpm i --frozen-lockfile` |

### TypeScript Configuration

Recommended `tsconfig.json` base:

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true
  }
}
```

### Linting & Formatting

We use a unified ESLint configuration that handles both linting and formatting (replacing Prettier).

```js
export default standardConfig();
```

**Workflow**: Run `nr lint --fix` to automatically format code and fix issues.

### Git Hooks

Automate checks before commit using `simple-git-hooks` and `lint-staged`.

```json
{
  "simple-git-hooks": {
    "pre-commit": "pnpm i --frozen-lockfile --ignore-scripts --offline && npx lint-staged"
  },
  "lint-staged": { "*": "eslint --fix" },
  "scripts": {
    "prepare": "npx simple-git-hooks"
  }
}
```

### Monorepo Management (pnpm)

Use `pnpm-workspace.yaml` with named catalogs for consistent dependency versions across packages.

| Catalog    | Purpose                                  |
| :--------- | :--------------------------------------- |
| `prod`     | Production dependencies (runtime)        |
| `dev`      | Development tools (build, test, lint)    |
| `frontend` | Frontend-specific libraries (React, Vue) |

## References

| Topic                   | Description                         | Reference                                                |
| :---------------------- | :---------------------------------- | :------------------------------------------------------- |
| **ESLint Config**       | Detailed rules and editor setup     | [eslint-config](references/eslint-config.md)             |
| **Project Setup**       | .gitignore, CI/CD, VS Code settings | [setting-up](references/setting-up.md)                   |
| **App Development**     | Patterns for Vue/Nuxt/React apps    | [app-development](references/app-development.md)         |
| **Library Development** | Bundling, publishing, ESM support   | [library-development](references/library-development.md) |
| **Monorepo**            | Workspace structure and tooling     | [monorepo](references/monorepo.md)                       |
