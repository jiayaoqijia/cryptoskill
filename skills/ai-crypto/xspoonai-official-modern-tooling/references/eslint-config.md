---
name: eslint-config
description: Configuring the unified ESLint setup for framework support, formatters, and rule overrides. Use when adding React/Vue/Svelte/Astro support, customizing rules, or setting up VS Code integration.
---

# Unified ESLint Configuration

This configuration handles both linting and formatting (replacing Prettier) in a single pass. It auto-detects TypeScript, Vue, and other frameworks.

**Style Philosophy**: Single quotes, no semicolons, sorted imports, dangling commas.

## Configuration Options

```js
export default standardConfig({
  // Project type: 'lib' for libraries, 'app' (default) for applications
  type: "lib",

  // Global ignores (extends defaults, doesn't override)
  ignores: ["**/fixtures", "**/dist"],

  // Stylistic options
  stylistic: {
    indent: 2, // 2, 4, or 'tab'
    quotes: "single", // or 'double'
  },

  // Framework support (auto-detected, but can be explicit)
  typescript: true,
  vue: true,

  // Disable specific language support
  jsonc: false,
  yaml: false,
});
```

## Framework Support

### Vue

Enable Vue accessibility rules:

```js
export default standardConfig({
  vue: {
    a11y: true,
  },
});
// Requires: pnpm add -D eslint-plugin-vuejs-accessibility
```

### React

```js
export default standardConfig({
  react: true,
});
// Requires: pnpm add -D @eslint-react/eslint-plugin eslint-plugin-react-hooks eslint-plugin-react-refresh
```

### Next.js

```js
export default standardConfig({
  nextjs: true,
});
// Requires: pnpm add -D @next/eslint-plugin-next
```

### Svelte

```js
export default standardConfig({
  svelte: true,
});
// Requires: pnpm add -D eslint-plugin-svelte
```

### Astro

```js
export default standardConfig({
  astro: true,
});
// Requires: pnpm add -D eslint-plugin-astro
```

### Solid

```js
export default standardConfig({
  solid: true,
});
// Requires: pnpm add -D eslint-plugin-solid
```

### UnoCSS

```js
export default standardConfig({
  unocss: true,
});
// Requires: pnpm add -D @unocss/eslint-plugin
```

## Formatters (CSS, HTML, Markdown)

For files ESLint doesn't handle natively, enable formatters:

```js
export default standardConfig({
  formatters: {
    css: true, // Format CSS, LESS, SCSS (uses Prettier)
    html: true, // Format HTML (uses Prettier)
    markdown: "prettier", // or 'dprint'
  },
});
// Requires: pnpm add -D eslint-plugin-format
```

## Rule Overrides

### Global overrides

```js
export default standardConfig(
  {
    // First argument: config options
  },
  // Additional arguments: ESLint flat configs
  {
    rules: {
      "style/semi": ["error", "never"],
    },
  },
);
```

### Per-integration overrides

```js
export default standardConfig({
  vue: {
    overrides: {
      "vue/operator-linebreak": ["error", "before"],
    },
  },
  typescript: {
    overrides: {
      "ts/consistent-type-definitions": ["error", "interface"],
    },
  },
});
```

### File-specific overrides

```js
export default standardConfig(
  { vue: true, typescript: true },
  {
    files: ["**/*.vue"],
    rules: {
      "vue/operator-linebreak": ["error", "before"],
    },
  },
);
```

## Plugin Prefix Renaming

The config renames plugin prefixes for consistency:

| New Prefix | Original               |
| ---------- | ---------------------- |
| `ts/*`     | `@typescript-eslint/*` |
| `style/*`  | `@stylistic/*`         |
| `import/*` | `import-lite/*`        |
| `node/*`   | `n/*`                  |
| `yaml/*`   | `yml/*`                |
| `test/*`   | `vitest/*`             |
| `next/*`   | `@next/next`           |

Use the new prefix when overriding or disabling rules:

```ts
// eslint-disable-next-line ts/consistent-type-definitions
type Foo = { bar: 2 };
```

## Type-Aware Rules

Enable TypeScript type checking:

```js
export default standardConfig({
  typescript: {
    tsconfigPath: "tsconfig.json",
  },
});
```

## VS Code Settings

Add to `.vscode/settings.json` to disable Prettier and enable ESLint formatting:

```jsonc
{
  "prettier.enable": false,
  "editor.formatOnSave": false,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "never",
  },
  "eslint.rules.customizations": [
    { "rule": "style/*", "severity": "off", "fixable": true },
    { "rule": "format/*", "severity": "off", "fixable": true },
    { "rule": "*-indent", "severity": "off", "fixable": true },
    { "rule": "*-spacing", "severity": "off", "fixable": true },
    { "rule": "*-spaces", "severity": "off", "fixable": true },
    { "rule": "*-order", "severity": "off", "fixable": true },
    { "rule": "*-dangle", "severity": "off", "fixable": true },
    { "rule": "*-newline", "severity": "off", "fixable": true },
    { "rule": "*quotes", "severity": "off", "fixable": true },
    { "rule": "*semi", "severity": "off", "fixable": true },
  ],
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact",
    "vue",
    "html",
    "markdown",
    "json",
    "jsonc",
    "yaml",
    "toml",
    "xml",
    "astro",
    "svelte",
    "css",
    "less",
    "scss",
  ],
}
```
