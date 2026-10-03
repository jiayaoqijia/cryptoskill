---
name: gdex-ui-theming
description: CSS theming system for GDEX trading UIs — dark/light modes, trading colors, responsive breakpoints, and Tailwind CSS configuration
---

# GDEX: UI Theming

CSS theming system for building polished trading interfaces. Covers dark/light mode, trading-specific color semantics (long/short/PnL), responsive layouts, and Tailwind CSS integration.

## When to Use

- Setting up dark/light mode for a trading app
- Defining trading-specific color semantics (buy/sell, PnL, chains)
- Configuring responsive breakpoints for trading layouts
- Extending Tailwind CSS with trading theme tokens

## CSS Custom Properties

Define a base theme using CSS variables. Trading UIs need specialized color semantics beyond generic UI:

```css
/* styles/theme.css */

:root {
  /* Brand — Gemach (see assets/brand) */
  --color-brand: #704FF6;        /* Majorelle Blue (primary accent) */
  --color-brand-hover: #5A3FE0;
  --color-brand-2: #61B8FF;      /* Argentinian Blue (secondary accent) */

  /* Gemach product lines */
  --color-gbot: #DF2E2E;         /* Rojo */
  --color-loans: #61B8FF;        /* Argentinian Blue */
  --color-vaults: #704FF6;       /* Majorelle Blue */
  --color-index: #49B875;        /* Emerald */

  /* Trading — Long / Short */
  --color-long: #49B875;         /* Emerald */
  --color-long-bg: #49B8751A;
  --color-short: #DF2E2E;        /* Rojo */
  --color-short-bg: #DF2E2E1A;

  /* PnL */
  --color-pnl-positive: #49B875;
  --color-pnl-negative: #DF2E2E;
  --color-pnl-neutral: #697083;

  /* Order Status */
  --color-status-filled: #49B875;
  --color-status-pending: #61B8FF;
  --color-status-cancelled: #697083;
  --color-status-failed: #DF2E2E;

  /* Chain Colors (chain brand colors, not Gemach) */
  --color-chain-solana: #9945FF;
  --color-chain-ethereum: #627EEA;
  --color-chain-base: #0052FF;
  --color-chain-arbitrum: #2D374B;
  --color-chain-bsc: #F0B90B;
  --color-chain-sui: #4DA2FF;
  --color-chain-optimism: #FF0420;

  /* Surfaces (light mode) */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F9FAFB;
  --bg-tertiary: #F3F4F6;
  --bg-card: #FFFFFF;
  --bg-input: #F9FAFB;
  --border-primary: #E5E7EB;
  --border-secondary: #D1D5DB;

  /* Text (light mode) */
  --text-primary: #060A17;       /* Rich Black */
  --text-secondary: #4D5972;
  --text-tertiary: #81899F;
  --text-on-brand: #FFFFFF;

  /* Typography — Gemach uses Inter */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Spacing */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;
}

/* Dark Mode (Gemach default — Rich Black + navy ramp) */
[data-theme='dark'], .dark {
  --bg-primary: #060A17;         /* Rich Black */
  --bg-secondary: #0C1322;
  --bg-tertiary: #162139;
  --bg-card: #0D1424;
  --bg-input: #152037;
  --border-primary: #192843;
  --border-secondary: #2E4164;

  --text-primary: #FFFFFF;
  --text-secondary: #A1A5B3;
  --text-tertiary: #697083;
}
```

## Gemach brand palette (official)

From the Gemach brand guide. The dark theme above is the Gemach default.

| Token | Hex | Use |
|-------|-----|-----|
| Rich Black | `#060A17` | App background (dark) |
| Majorelle Blue | `#704FF6` | Primary brand accent (Vaults) |
| Argentinian Blue | `#61B8FF` | Secondary accent (Loans) |
| Emerald | `#49B875` | Long / positive (Index Funds) |
| Rojo | `#DF2E2E` | Short / negative (GBOT) |

Navy → white neutral ramp: `#161D2F #152037 #162139 #192843 #2E4164 #4D5972 #697083 #81899F #A1A5B3 #D5D9E1 #FFFFFF`

**Logo:** the white Gemach lion mark is at `assets/brand/gemach-lion.png`. Pair it with the
`GEMACH` / `GDEX` wordmark in **Inter** (700–800 weight). On dark, use the white mark; on
light, the black mark. **Font:** Inter (400/500/600/700/800) — load via Google Fonts or self-host.

## Dark / Light Mode Toggle

```typescript
// components/ThemeToggle.tsx
'use client';

import { useEffect, useState } from 'react';

export function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('gdex-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setDark(saved ? saved === 'dark' : prefersDark);
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    document.documentElement.classList.toggle('dark', dark);
    localStorage.setItem('gdex-theme', dark ? 'dark' : 'light');
  }, [dark]);

  return (
    <button onClick={() => setDark(!dark)}
      className="p-2 rounded-lg border border-[var(--border-primary)] hover:bg-[var(--bg-tertiary)]">
      {dark ? '☀️' : '🌙'}
    </button>
  );
}
```

## Tailwind CSS Configuration

Extend Tailwind with GDEX trading theme tokens:

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class',
  content: ['./src/**/*.{ts,tsx}', './app/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: 'var(--color-brand)',
        'brand-hover': 'var(--color-brand-hover)',
        long: 'var(--color-long)',
        'long-bg': 'var(--color-long-bg)',
        short: 'var(--color-short)',
        'short-bg': 'var(--color-short-bg)',
        'pnl-positive': 'var(--color-pnl-positive)',
        'pnl-negative': 'var(--color-pnl-negative)',
        'pnl-neutral': 'var(--color-pnl-neutral)',
        'surface-primary': 'var(--bg-primary)',
        'surface-secondary': 'var(--bg-secondary)',
        'surface-card': 'var(--bg-card)',
      },
      fontFamily: {
        sans: ['var(--font-sans)'],
        mono: ['var(--font-mono)'],
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
      },
    },
  },
};

export default config;
```

### Usage in Components

```tsx
{/* Trading colors via Tailwind */}
<span className="text-long">+$420.69</span>     {/* green — long position / profit */}
<span className="text-short">-$69.42</span>      {/* red — short position / loss */}
<div className="bg-long-bg p-2">Long highlight</div>
<div className="bg-surface-card border border-[var(--border-primary)]">Card</div>
```

## Responsive Breakpoints

Trading UIs have unique layout needs — the primary trading view should maximize horizontal space:

```css
/* Trading layout breakpoints */
@media (min-width: 768px) {
  /* Tablet: stack chart above order form */
  .trading-layout { grid-template-columns: 1fr; }
}

@media (min-width: 1024px) {
  /* Desktop: chart + order form side by side */
  .trading-layout { grid-template-columns: 1fr 360px; }
}

@media (min-width: 1440px) {
  /* Wide: chart + orderbook + order form */
  .trading-layout { grid-template-columns: 280px 1fr 360px; }
}
```

```tsx
{/* Responsive trading grid */}
<div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] xl:grid-cols-[280px_1fr_360px] gap-4">
  <aside className="hidden xl:block">{/* Orderbook */}</aside>
  <main>{/* Chart + Positions */}</main>
  <aside>{/* Order Form */}</aside>
</div>
```

## Component Styling Patterns

### Trading Buttons

```tsx
{/* Long / Short buttons */}
<button className="w-full py-3 rounded-lg font-bold text-white bg-long hover:opacity-90">
  Long BTC
</button>
<button className="w-full py-3 rounded-lg font-bold text-white bg-short hover:opacity-90">
  Short BTC
</button>
```

### PnL with Color

```tsx
function PnL({ value }: { value: number }) {
  const color = value > 0 ? 'text-pnl-positive' : value < 0 ? 'text-pnl-negative' : 'text-pnl-neutral';
  const sign = value > 0 ? '+' : '';
  return <span className={`font-mono font-bold ${color}`}>{sign}${value.toFixed(2)}</span>;
}
```

### Chain Badge

```tsx
const CHAIN_COLORS: Record<string, string> = {
  solana: 'var(--color-chain-solana)',
  ethereum: 'var(--color-chain-ethereum)',
  base: 'var(--color-chain-base)',
  arbitrum: 'var(--color-chain-arbitrum)',
  bsc: 'var(--color-chain-bsc)',
  sui: 'var(--color-chain-sui)',
};

function ChainBadge({ chain }: { chain: string }) {
  return (
    <span className="px-2 py-0.5 rounded-full text-xs font-medium text-white"
      style={{ backgroundColor: CHAIN_COLORS[chain] ?? '#6B7280' }}>
      {chain}
    </span>
  );
}
```

## Related Skills

- **gdex-ui-install-setup** — Project setup (includes Tailwind setup)
- **gdex-ui-page-layouts** — Full page layouts using these theme tokens
- **gdex-ui-trading-components** — Trading components that use theme colors
