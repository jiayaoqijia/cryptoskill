---
name: gdex-ui-portfolio-dashboard
description: React component patterns for GDEX portfolio dashboards — token balances, trade history, chain selectors, and live data polling
---

# GDEX: Portfolio Dashboard Components

React component patterns for building portfolio dashboards with the GDEX SDK. Covers balance displays, trade history with pagination, and live data polling.

## When to Use

- Displaying cross-chain token balances
- Building paginated trade history tables
- Creating chain selector dropdowns with balance summaries
- Implementing auto-refresh for live portfolio data

## Prerequisites

- GDEX SDK context provider set up — see **gdex-ui-install-setup**
- Authenticated via `loginWithApiKey()` — see **gdex-authentication**

## Portfolio Overview

```typescript
import type { SupportedChain } from '@gemachdao/gdex-skill';
// components/PortfolioOverview.tsx
'use client';

import { useState, useEffect, useCallback } from 'react';
import { useGdex } from '@/providers/GdexProvider';
import { useAuth } from '@/providers/AuthProvider';

export function PortfolioOverview({ chain = 8453, pollInterval = 30000 }: { chain?: SupportedChain; pollInterval?: number }) {
  const { skill, isReady } = useGdex();
  const { walletAddress } = useAuth();
  const [portfolio, setPortfolio] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    if (!isReady || !walletAddress) return;
    try {
      const data = await skill.getPortfolio({ walletAddress, chain });
      setPortfolio(data);
    } finally {
      setLoading(false);
    }
  }, [skill, isReady, walletAddress]);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, pollInterval);
    return () => clearInterval(id);
  }, [refresh, pollInterval]);

  if (loading) return <div className="animate-pulse h-24 bg-gray-200 rounded" />;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatCard label="Total Value" value={`$${portfolio?.totalValue?.toFixed(2) ?? '0.00'}`} />
      <StatCard label="24h PnL" value={portfolio?.pnl24h}
        className={portfolio?.pnl24h >= 0 ? 'text-green-500' : 'text-red-500'} />
      <StatCard label="Chains" value={portfolio?.chains?.length ?? 0} />
      <StatCard label="Tokens" value={portfolio?.tokens?.length ?? 0} />
    </div>
  );
}

function StatCard({ label, value, className = '' }: { label: string; value: any; className?: string }) {
  return (
    <div className="border rounded-lg p-4">
      <p className="text-xs text-gray-500">{label}</p>
      <p className={`text-xl font-bold ${className}`}>{value}</p>
    </div>
  );
}
```

**SDK method called:** `skill.getPortfolio()`

## Token Balance Grid

```typescript
// components/TokenBalanceGrid.tsx
'use client';

import { useState, useEffect } from 'react';
import { useGdex } from '@/providers/GdexProvider';
import { useAuth } from '@/providers/AuthProvider';
import type { SupportedChain } from '@gemachdao/gdex-skill';

interface Token {
  symbol: string;
  name: string;
  balance: string;
  valueUsd: number;
  chain: string;
  address: string;
  logoUrl?: string;
}

export function TokenBalanceGrid({ chain }: { chain: SupportedChain }) {
  const { skill, isReady } = useGdex();
  const { walletAddress } = useAuth();
  const [tokens, setTokens] = useState<Token[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isReady || !walletAddress) return;
    setLoading(true);
    skill.getPortfolio({ walletAddress, chain })
      .then(data => {
        setTokens(data?.tokens ?? []);
      })
      .finally(() => setLoading(false));
  }, [skill, isReady, chain]);

  if (loading) return <div className="animate-pulse h-48 bg-gray-200 rounded" />;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
      {tokens.map((token, i) => (
        <div key={i} className="border rounded-lg p-3 flex items-center gap-3">
          {token.logoUrl && <img src={token.logoUrl} alt={token.symbol} className="w-8 h-8 rounded-full" />}
          <div className="flex-1">
            <div className="flex justify-between">
              <span className="font-bold">{token.symbol}</span>
              <span className="text-sm text-gray-500">{token.chain}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>{token.balance}</span>
              <span className="text-gray-600">${token.valueUsd?.toFixed(2)}</span>
            </div>
          </div>
        </div>
      ))}
      {!tokens.length && <p className="text-gray-500 col-span-full">No tokens found</p>}
    </div>
  );
}
```

## Trade History Table

```typescript
import type { SupportedChain } from '@gemachdao/gdex-skill';
// components/TradeHistoryTable.tsx
'use client';

import { useState, useEffect } from 'react';
import { useGdex } from '@/providers/GdexProvider';
import { useAuth } from '@/providers/AuthProvider';

export function TradeHistoryTable({ chain, pageSize = 20 }: { chain: SupportedChain; pageSize?: number }) {
  const { skill, isReady } = useGdex();
  const { walletAddress } = useAuth();
  const [trades, setTrades] = useState<any[]>([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isReady || !walletAddress) return;
    setLoading(true);
    skill.getTradeHistory({ walletAddress, chain, page, limit: pageSize })
      .then(data => {
        setTrades(data?.trades ?? []);
        setHasMore((data?.trades?.length ?? 0) >= pageSize);
      })
      .finally(() => setLoading(false));
  }, [skill, isReady, page, pageSize]);

  return (
    <div>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left border-b text-gray-500">
            <th className="py-2">Date</th>
            <th>Type</th>
            <th>Token</th>
            <th>Amount</th>
            <th>Chain</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr><td colSpan={6} className="text-center py-8">Loading...</td></tr>
          ) : (
            trades.map((trade, i) => (
              <tr key={i} className="border-b hover:bg-gray-50">
                <td className="py-2">{new Date(trade.timestamp).toLocaleDateString()}</td>
                <td className={trade.side === 'buy' ? 'text-green-600' : 'text-red-600'}>
                  {trade.side?.toUpperCase()}
                </td>
                <td className="font-mono">{trade.symbol ?? trade.tokenAddress?.slice(0, 8)}</td>
                <td>{trade.amount}</td>
                <td>{trade.chain}</td>
                <td>
                  <span className={`px-2 py-0.5 rounded text-xs ${
                    trade.status === 'completed' ? 'bg-green-100 text-green-800' :
                    trade.status === 'failed' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {trade.status}
                  </span>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      {/* Pagination */}
      <div className="flex justify-between items-center mt-4">
        <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}
          className="px-3 py-1 border rounded disabled:opacity-50">
          Previous
        </button>
        <span className="text-sm text-gray-500">Page {page}</span>
        <button onClick={() => setPage(p => p + 1)} disabled={!hasMore}
          className="px-3 py-1 border rounded disabled:opacity-50">
          Next
        </button>
      </div>
    </div>
  );
}
```

**SDK method called:** `skill.getTradeHistory()`

## Chain Selector

```typescript
// components/ChainSelector.tsx
const CHAINS = [
  { id: 'all', name: 'All Chains', icon: '🌐' },
  { id: 'solana', name: 'Solana', icon: '◎' },
  { id: '1', name: 'Ethereum', icon: 'Ξ' },
  { id: '8453', name: 'Base', icon: '🔵' },
  { id: '42161', name: 'Arbitrum', icon: '🔷' },
  { id: '56', name: 'BSC', icon: '🟡' },
  { id: '10', name: 'Optimism', icon: '🔴' },
  { id: 'sui', name: 'Sui', icon: '💧' },
];

interface ChainSelectorProps {
  value: string;
  onChange: (chain: string) => void;
}

export function ChainSelector({ value, onChange }: ChainSelectorProps) {
  return (
    <div className="flex gap-2 flex-wrap">
      {CHAINS.map(chain => (
        <button key={chain.id} onClick={() => onChange(chain.id)}
          className={`px-3 py-1.5 rounded-full text-sm border transition ${
            value === chain.id ? 'bg-blue-600 text-white border-blue-600' : 'border-gray-300 hover:border-gray-400'
          }`}>
          {chain.icon} {chain.name}
        </button>
      ))}
    </div>
  );
}
```

## Data Fetching Pattern: SWR / React Query

For production apps, wrap SDK calls with a caching library:

```typescript
// hooks/usePortfolioQuery.ts (React Query example)
import { useQuery } from '@tanstack/react-query';
import type { SupportedChain } from '@gemachdao/gdex-skill';
import { useGdex } from '@/providers/GdexProvider';

export function usePortfolioQuery(walletAddress: string, chain: SupportedChain) {
  const { skill, isReady } = useGdex();

  return useQuery({
    queryKey: ['portfolio', walletAddress, chain],
    queryFn: () => skill.getPortfolio({ walletAddress, chain }),
    enabled: isReady && !!walletAddress,
    refetchInterval: 30_000,      // poll every 30s
    staleTime: 10_000,            // consider fresh for 10s
  });
}
```

```typescript
import type { SupportedChain } from '@gemachdao/gdex-skill';
// hooks/useTradeHistoryQuery.ts
import { useQuery } from '@tanstack/react-query';
import { useGdex } from '@/providers/GdexProvider';

export function useTradeHistoryQuery(walletAddress: string, chain: SupportedChain, page: number, limit = 20) {
  const { skill, isReady } = useGdex();

  return useQuery({
    queryKey: ['tradeHistory', walletAddress, chain, page, limit],
    queryFn: () => skill.getTradeHistory({ walletAddress, chain, page, limit }),
    enabled: isReady && !!walletAddress,
    keepPreviousData: true,       // smooth pagination
  });
}
```

## Backend Quirk: SDK Methods Need Raw Client (Live-Tested)

> **Note:** `skill.getPortfolio()`, `getBalances()` and `getTradeHistory()` are managed-account reads: pass the control `walletAddress`, the session (`sessionPrivateKey` + `apiKey`, or `data`) and a `chain` on every call. The examples above omit them for brevity. Holdings are returned under `holdings[]`; history pages with `cursor`. See **gdex-portfolio**.

**For frontend React Query hooks, use raw client instead:**

```typescript
// hooks/usePortfolioQuery.ts — CORRECT for managed custody
import { useQuery } from '@tanstack/react-query';
import { useGdex } from '@/providers/GdexProvider';
import { buildGdexUserSessionData } from '@gemachdao/gdex-skill';

export function usePortfolioQuery(userId: string, sessionKey: string, apiKey: string, chainId: number) {
  const { skill, isReady } = useGdex();
  const data = buildGdexUserSessionData(sessionKey, apiKey);

  return useQuery({
    queryKey: ['portfolio', userId, chainId],
    queryFn: () => skill.client.get('/v1/portfolio', {
      params: { userId, chainId, data }
    }),
    enabled: isReady,
    refetchInterval: 30_000,
  });
}
```

## Component → SDK Method Reference

| Component | SDK Method | Skill |
|-----------|------------|-------|
| `PortfolioOverview` | `skill.client.get('/v1/portfolio', ...)` | gdex-portfolio |
| `TokenBalanceGrid` | `skill.client.get('/v1/portfolio', ...)` (balances embedded under `portfolio.balances[]`) | gdex-portfolio |
| `TradeHistoryTable` | `skill.client.get('/v1/user_history', ...)` | gdex-portfolio |
| `ChainSelector` | (UI only) | — |

## Related Skills

- **gdex-ui-install-setup** — Project setup and SDK context provider
- **gdex-ui-trading-components** — Trading forms and order entry components
- **gdex-ui-page-layouts** — Full page layouts using these dashboard components
- **gdex-portfolio** — Portfolio SDK API details and raw client workarounds
