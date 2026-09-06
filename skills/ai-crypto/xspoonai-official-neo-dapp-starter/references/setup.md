# Setup & Deployment

## Environment Setup

```bash
# .env (production)
NEXT_PUBLIC_ENVIRONMENT=production

# .env.development (development)
NEXT_PUBLIC_ENVIRONMENT=development
```

## Deployment

### Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy (auto-detects Next.js)
vercel

# Configuration is in vercel.json
# { "buildCommand": "next build" }
```

### Cloudflare Pages

```bash
# Build for Cloudflare
pnpm build

# Start locally with Wrangler
pnpm start

# Deploy to Cloudflare Pages
wrangler pages deploy .vercel/output/static
```

Configuration in `wrangler.toml`:

```toml
name = "neo-dapp-starter"
compatibility_date = "2024-09-23"
compatibility_flags = ["nodejs_compat"]
pages_build_output_dir = ".vercel/output/static"
```

### Environment Variables for Deployment

| Variable                  | Required | Description                   |
| ------------------------- | -------- | ----------------------------- |
| `NEXT_PUBLIC_ENVIRONMENT` | Yes      | `production` or `development` |

## Development Tooling

### NPM Scripts

| Script      | Command                     | Description                       |
| ----------- | --------------------------- | --------------------------------- |
| `dev`       | `next dev`                  | Start development server          |
| `build`     | `pnpm exec next-on-pages`   | Build for Cloudflare Pages        |
| `start`     | `wrangler pages dev`        | Start production build locally    |
| `lint`      | `eslint --max-warnings 0 .` | Run ESLint (zero warnings policy) |
| `test`      | `vitest run`                | Run tests                         |
| `typecheck` | `tsc`                       | TypeScript type checking          |
| `storybook` | `storybook dev -p 6006`     | Start Storybook                   |
| `prepare`   | `husky`                     | Install Git hooks                 |

### Storybook

Component development environment at `http://localhost:6006`:

```bash
pnpm storybook
```

Example story (`src/ui/shadcn/button.stories.tsx`):

```typescript
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./button";

const meta: Meta<typeof Button> = {
  component: Button,
};
export default meta;

type Story = StoryObj<typeof Button>;
export const Primary: Story = {
  args: { children: "Click me" },
};
```

### Testing with Vitest

```bash
pnpm test
```

### Code Quality

- **ESLint 9** (flat config) with plugins: next, react, react-hooks, import, check-file, prettier, storybook, tanstack-query
- **Prettier 3.4** with `prettier-plugin-tailwindcss` for consistent class ordering
- **Husky 9** + **lint-staged 15** for pre-commit checks
- **Zero warnings policy**: `eslint --max-warnings 0`
