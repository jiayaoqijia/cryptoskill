# Caffeine frontend template

The frontend of a Caffeine app is a React + Vite + Tailwind project served as an
"assets" canister. The files below are the **canonical Caffeine frontend starter**,
reproduced from the build template and **verified** — a from-scratch app using them
passed `caffeine build` and deployed a draft.

> **These dependency versions drift.** They are a current snapshot of the Caffeine
> template, which bumps them over time (e.g. the `@dfinity/*` → `@icp-sdk/*` migration,
> and `@caffeineai/core-infrastructure` 0.x → 1.x). For the latest, scaffold via Caffeine
> or `caffeine projects clone` a recent project and copy its `src/frontend/package.json`.
> The stable part is the *shape*: Vite + Tailwind + Biome, the
> `@caffeineai/core-infrastructure` integration, and the `useActor(createActor)` call
> pattern.

`index.css` and `App.tsx` here are deliberately **minimal** so a from-scratch app builds
immediately. The full template additionally ships a richer `index.css` (the `oklch` color
tokens and the `--font-*` / `--radius` variables that `tailwind.config.js` references),
a `src/components/ui/` set of shadcn-style components, and a `lib/utils.ts`. Layer those
in as the app grows; the minimal versions below render with stock Tailwind.

All files live under `src/frontend/` (relative paths are noted per file).

> Reminder: `src/frontend/src/backend.ts` and `src/frontend/src/declarations/` are
> **generated** by `caffeine-bindgen` during the build (see SKILL.md → "The build
> loop"). Do not create or edit them by hand.

## `src/frontend/package.json`

The full Caffeine starter (the "kitchen sink" — most apps use only a subset; prune unused
deps once the app works). Verified to install with pnpm and build with Vite.

```json
{
  "name": "@caffeine/template-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build && pnpm copy:env",
    "copy:env": "cp env.json dist/",
    "typecheck": "tsc --noEmit",
    "check": "biome check src",
    "fix": "biome check --write src"
  },
  "devDependencies": {
    "@biomejs/biome": "^1.9.0",
    "@tailwindcss/container-queries": "^0.1.1",
    "@types/node": "^20.9.0",
    "@types/react": "~19.1.0",
    "@types/react-dom": "~19.1.0",
    "@types/three": "0.176.0",
    "@vitejs/plugin-react": "^4.3.1",
    "autoprefixer": "^10.4.20",
    "dotenv": "^16.5.0",
    "dotenv-cli": "^8.0.0",
    "postcss": "^8.4.41",
    "tailwindcss": "^3.4.17",
    "@tailwindcss/typography": "0.5.10",
    "tailwindcss-animate": "^1.0.7",
    "typescript": "^5.8.3",
    "vite": "^5.4.1",
    "vite-plugin-environment": "^1.1.3"
  },
  "dependencies": {
    "@caffeineai/core-infrastructure": "^1.0.0",
    "@icp-sdk/auth": "^7.1.0",
    "@icp-sdk/core": "^5.3.0",
    "@react-three/cannon": "~6.6.0",
    "@react-three/drei": "~10.0.8",
    "@react-three/fiber": "~9.1.2",
    "@tanstack/react-query": "^5.24.0",
    "@tanstack/react-router": "~1.131.8",
    "lucide-react": "0.511.0",
    "react-icons": "^5.4.0",
    "@radix-ui/react-slot": "^1.1.0",
    "@radix-ui/react-dialog": "^1.1.1",
    "@radix-ui/react-dropdown-menu": "^2.1.1",
    "@radix-ui/react-label": "^2.1.0",
    "@radix-ui/react-select": "^2.1.2",
    "@radix-ui/react-tabs": "^1.1.0",
    "@radix-ui/react-tooltip": "^1.1.2",
    "@radix-ui/react-scroll-area": "^1.2.0",
    "@radix-ui/react-popover": "^1.1.1",
    "@radix-ui/react-checkbox": "^1.1.1",
    "@radix-ui/react-switch": "^1.1.1",
    "@radix-ui/react-separator": "^1.1.0",
    "@radix-ui/react-avatar": "^1.1.0",
    "@radix-ui/react-accordion": "^1.1.2",
    "@radix-ui/react-alert-dialog": "^1.1.2",
    "@radix-ui/react-aspect-ratio": "^1.1.0",
    "@radix-ui/react-hover-card": "^1.1.2",
    "@radix-ui/react-menubar": "^1.1.1",
    "@radix-ui/react-navigation-menu": "^1.2.0",
    "@radix-ui/react-progress": "^1.1.0",
    "@radix-ui/react-radio-group": "^1.2.0",
    "@radix-ui/react-slider": "^1.2.0",
    "@radix-ui/react-toggle": "^1.1.0",
    "@radix-ui/react-toggle-group": "^1.1.0",
    "@radix-ui/react-collapsible": "^1.1.0",
    "@radix-ui/react-context-menu": "^2.2.15",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.5.2",
    "react-day-picker": "^9.5.0",
    "date-fns": "^3.6.0",
    "embla-carousel-react": "^8.2.1",
    "recharts": "^2.15.1",
    "cmdk": "^1.0.0",
    "vaul": "^1.1.2",
    "react-hook-form": "^7.53.0",
    "input-otp": "^1.4.1",
    "react-resizable-panels": "^2.1.7",
    "sonner": "^1.7.4",
    "next-themes": "~0.4.6",
    "react": "~19.1.0",
    "react-use": "~17.6.0",
    "react-dom": "~19.1.0",
    "react-quill-new": "3.4.6",
    "three": "^0.176.0",
    "zustand": "~5.0.5",
    "motion": "^12.34.3"
  }
}
```

## `src/frontend/vite.config.js`

Verbatim. The `declarations` alias and `dedupe: ["@icp-sdk/core"]` matter — the generated
backend client imports from `./declarations` and from `@icp-sdk` packages, and deduping
`@icp-sdk/core` avoids "multiple agent instances" runtime issues.

```javascript
import { fileURLToPath, URL } from "url";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import environment from "vite-plugin-environment";

const ii_url =
  process.env.DFX_NETWORK === "local"
    ? `http://uqzsh-gqaaa-aaaaq-qaada-cai.localhost:8081/authorize`
    : `https://id.ai/authorize`;

process.env.II_URL = process.env.II_URL || ii_url;
process.env.STORAGE_GATEWAY_URL =
  process.env.STORAGE_GATEWAY_URL || "https://blob.caffeine.ai";

export default defineConfig({
  logLevel: "error",
  build: {
    emptyOutDir: true,
    sourcemap: false,
    minify: false,
  },
  css: {
    postcss: "./postcss.config.js",
  },
  optimizeDeps: {
    esbuildOptions: {
      define: {
        global: "globalThis",
      },
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:4943",
        changeOrigin: true,
      },
    },
  },
  plugins: [
    environment("all", { prefix: "CANISTER_" }),
    environment("all", { prefix: "DFX_" }),
    environment(["II_URL"]),
    environment(["STORAGE_GATEWAY_URL"]),
    react(),
  ],
  resolve: {
    alias: [
      {
        find: "declarations",
        replacement: fileURLToPath(new URL("../declarations", import.meta.url)),
      },
      {
        find: "@",
        replacement: fileURLToPath(new URL("./src", import.meta.url)),
      },
    ],
    dedupe: ["@icp-sdk/core"]
  },
});
```

## `src/frontend/tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "useDefineForClassFields": true,
    "lib": ["DOM", "DOM.Iterable", "ESNext"],
    "allowJs": false,
    "skipLibCheck": true,
    "esModuleInterop": false,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "noImplicitAny": false,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "incremental": true,
    "tsBuildInfoFile": "./node_modules/.cache/tsbuildinfo",
    "jsx": "react-jsx",
    "types": ["vite/client", "node"],
    "paths": {
      "declarations/*": ["../declarations/*"],
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "exclude": [
    "node_modules",
    "dist",
    "build",
    "*.config.js"
  ]
}
```

## `src/frontend/biome.json`

Note the `files.ignore` entries for the generated `backend.ts` / `backend.d.ts` /
`declarations/` — those are bindgen output and must not be linted or formatted.

```json
{
  "$schema": "./node_modules/@biomejs/biome/configuration_schema.json",
  "files": {
    "ignore": [
      "**/backend.ts",
      "**/backend.d.ts",
      "dist/**",
      "node_modules/**",
      "build/**",
      "*.config.js",
      "src/declarations/**",
      "src/config.ts"
    ]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "correctness": {
        "useHookAtTopLevel": "error",
        "noUnusedVariables": "error"
      },
      "suspicious": {
        "noExplicitAny": "off"
      },
      "style": {
        "useConst": "off",
        "noNonNullAssertion": "off"
      }
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "semicolons": "always"
    }
  }
}
```

## `src/frontend/postcss.config.js`

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

## `src/frontend/tailwind.config.js`

Verbatim from the starter. It references `oklch(var(--…))` color tokens and `--font-*` /
`--radius` variables; define those in `index.css` to use the semantic colors
(`bg-card`, `text-primary`, `font-display`, …). Stock Tailwind utilities work without
them.

```javascript
import typography from "@tailwindcss/typography";
import containerQueries from "@tailwindcss/container-queries";
import animate from "tailwindcss-animate";

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: ["index.html", "src/**/*.{js,ts,jsx,tsx,html,css}"],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "oklch(var(--border))",
        input: "oklch(var(--input))",
        ring: "oklch(var(--ring) / <alpha-value>)",
        background: "oklch(var(--background))",
        foreground: "oklch(var(--foreground))",
        primary: {
          DEFAULT: "oklch(var(--primary) / <alpha-value>)",
          foreground: "oklch(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "oklch(var(--secondary) / <alpha-value>)",
          foreground: "oklch(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "oklch(var(--destructive) / <alpha-value>)",
          foreground: "oklch(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "oklch(var(--muted) / <alpha-value>)",
          foreground: "oklch(var(--muted-foreground) / <alpha-value>)",
        },
        accent: {
          DEFAULT: "oklch(var(--accent) / <alpha-value>)",
          foreground: "oklch(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "oklch(var(--popover))",
          foreground: "oklch(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "oklch(var(--card))",
          foreground: "oklch(var(--card-foreground))",
        },
      },
      fontFamily: {
        display: ["var(--font-display)", "serif"],
        body: ["var(--font-body)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [typography, containerQueries, animate],
};
```

## `src/frontend/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>App</title>
    <meta name="description" content="Built with caffeine.ai" />
    <meta property="og:title" content="App" />
    <meta property="og:description" content="Built with caffeine.ai" />
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="./src/main.tsx"></script>
  </body>
</html>
```

## `src/frontend/env.json`

Placeholders only — Caffeine injects real values when it serves the app. The `build`
script copies this file into `dist/` (the `copy:env` step). Keep all five keys.

```json
{
  "backend_host": "undefined",
  "backend_canister_id": "undefined",
  "project_id": "undefined",
  "ii_derivation_origin": "undefined",
  "storage_gateway_url": "undefined"
}
```

## `src/frontend/src/main.tsx`

Verbatim entry point. It installs the two providers every Caffeine app expects:
`InternetIdentityProvider` (from `@caffeineai/core-infrastructure`, for IC auth) and the
TanStack Query client. The `BigInt.prototype.toJSON` shim lets the Candid `Nat`/`Int`
values (which deserialize to `bigint`) be JSON-serialized.

```tsx
import { InternetIdentityProvider } from "@caffeineai/core-infrastructure";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

BigInt.prototype.toJSON = function () {
  return this.toString();
};

declare global {
  interface BigInt {
    toJSON(): string;
  }
}

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <QueryClientProvider client={queryClient}>
    <InternetIdentityProvider>
      <App />
    </InternetIdentityProvider>
  </QueryClientProvider>,
);
```

## `src/frontend/src/index.css`

Minimal — the three Tailwind layers. (The full starter additionally defines the
`:root` / `.dark` `oklch` color tokens and `--font-*` / `--radius` variables referenced
by `tailwind.config.js`; add them when you adopt the semantic color classes.)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## `src/frontend/src/App.tsx`

A minimal, self-contained starting point (stock Tailwind utilities, no design-system
tokens, no backend calls). Replace it with your UI.

```tsx
export default function App() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-white text-gray-900">
      <h1 className="text-4xl font-bold">Hello from Caffeine</h1>
      <p className="text-gray-600">Edit src/frontend/src/App.tsx to build your app.</p>
    </div>
  );
}
```

## Calling the backend from the frontend

`@caffeineai/core-infrastructure` ships the **entire** backend-integration layer, so you
do NOT hand-write an actor/config/storage layer. It exports:

- `InternetIdentityProvider`, `useInternetIdentity` — IC auth (the provider wraps your app
  in `main.tsx`, above).
- `useActor(createActor)` — a TanStack-Query hook that builds the actor (anonymous, or
  with the signed-in identity) and returns `{ actor, isFetching }`.
- `createActorWithConfig(createActor, options?)`, `loadConfig()` — the non-hook equivalents.

You pass the **generated** `createActor` (from `./backend`) into `useActor` /
`createActorWithConfig`; they supply the canister id (from `env.json`), the HTTP agent, and
the `uploadFile`/`downloadFile` blob handlers internally. That is why you never call the
generated `createActor` yourself or work out its `_uploadFile`/`_downloadFile` params.

The generated client signature, for reference only (do not call it directly, do not edit
the file):

```ts
// src/frontend/src/backend.ts (generated by caffeine-bindgen)
export function createActor(
  canisterId: string,
  _uploadFile: (file: ExternalBlob) => Promise<Uint8Array>,
  _downloadFile: (file: Uint8Array) => Promise<ExternalBlob>,
  options?: CreateActorOptions,
): Backend; // Backend exposes one method per public function in main.mo
```

**Worked example** (validated end-to-end: a button that calls a backend query and shows
the result). Backend — write it with the **`writing-motoko` skill**:

```motoko
import MixinViews "mo:caffeineai-data-viewer/MixinViews";
import Time "mo:core/Time";

actor {
  include MixinViews();

  public query func getCurrentTime() : async Int {
    Time.now();
  };
};
```

After a build, bindgen exposes `getCurrentTime(): Promise<bigint>` on the client. The
frontend calls it through `useActor` + TanStack Query:

```tsx
import { useActor } from "@caffeineai/core-infrastructure";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { createActor } from "./backend";

export default function App() {
  const [requested, setRequested] = useState(false);
  const { actor, isFetching } = useActor(createActor);
  const { data, refetch, isFetching: querying } = useQuery({
    queryKey: ["currentTime"],
    queryFn: async () => {
      if (!actor) throw new Error("Actor not ready");
      return actor.getCurrentTime(); // bigint: nanoseconds since the Unix epoch
    },
    enabled: requested && !!actor && !isFetching,
  });

  const formatted =
    data != null ? new Date(Number(data / 1_000_000n)).toLocaleString() : null;

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-6">
      <h1 className="text-4xl font-bold">Caffeine time demo</h1>
      <button
        type="button"
        className="rounded bg-black px-4 py-2 text-white"
        onClick={() => {
          setRequested(true);
          void refetch();
        }}
      >
        Get backend time
      </button>
      {querying && <p>Loading…</p>}
      {formatted && <p className="text-lg">Backend time: {formatted}</p>}
    </div>
  );
}
```

Notes:

- **Method names and types come from your `main.mo`** and only exist after a build
  regenerates the client. Add the backend function, run `caffeine build` to regenerate
  `backend.ts`, then write the frontend call (see "Generation ordering" in SKILL.md).
- **Candid `Int`/`Nat` deserialize to `bigint`** (hence `data / 1_000_000n`); the
  `BigInt.prototype.toJSON` shim in `main.tsx` keeps them JSON-serializable.
- At local `caffeine build` time the `backend_canister_id` in `env.json` is still
  `"undefined"` — that is fine, because `caffeine build` only typechecks and bundles.
  Caffeine injects the real canister id when it serves the deployed draft, so the call
  resolves there (or against a local replica).
- `index.html` references `/favicon.ico`; drop a `favicon.ico` in `src/frontend/public/`
  or remove the `<link rel="icon">` line (a missing favicon is a 404 at runtime, not a
  build error).
