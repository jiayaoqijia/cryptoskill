#!/usr/bin/env bun
// ============================================================
// Awaken Agent Kit - MCP Server Adapter
// ============================================================
// Exposes all Awaken DEX tools via Model Context Protocol.
// Runs on stdio transport for local use with Claude Desktop, Cursor, etc.
//
// Start: bun run src/mcp/server.ts
// Or:    bun run mcp

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import packageJson from '../../package.json';

import { getNetworkConfig } from '../../lib/config';
import { resolveSignerContext } from '../../lib/signer-context';
import { getQuote, getPair, getTokenBalance, getTokenAllowance, getLiquidityPositions } from '../core/query';
import { executeSwap, addLiquidity, removeLiquidity, approveTokenSpending } from '../core/trade';
import { fetchKline, getKlineIntervals } from '../core/kline';
import { fail } from './error';

const server = new McpServer({
  name: 'awaken-agent-kit',
  version: packageJson.version,
});

// Helper: wrap core call result as MCP tool response
function ok(data: any) {
  return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
}

type McpToolHandler = (input: Record<string, any>) => Promise<any> | any;

function registerTool(name: string, definition: any, handler: McpToolHandler) {
  return (server.registerTool as any)(name, definition, handler);
}

const READ_ONLY_ANNOTATIONS = {
  readOnlyHint: true,
  read_only_hint: true,
} as const;

const NETWORK_WRITE_ANNOTATIONS = {
  destructiveHint: true,
  destructive_hint: true,
  openWorldHint: true,
  side_effects_hint: true,
} as const;

const signerInputSchema = z
  .object({
    signerMode: z.enum(['auto', 'explicit', 'context', 'env', 'daemon']).optional(),
    walletType: z.enum(['EOA', 'CA']).optional(),
    address: z.string().optional(),
    password: z.string().optional(),
    privateKey: z.string().optional(),
    caHash: z.string().optional(),
    caAddress: z.string().optional(),
    network: z.enum(['mainnet', 'testnet']).optional(),
  })
  .optional()
  .describe(
    'Optional signer context input. signerMode=auto tries explicit → active context → env. daemon is reserved for future release.',
  );

// ============================================================
// Query Tools (read-only, no private key required)
// ============================================================

registerTool(
  'awaken_quote',
  {
    description:
      'Query the best swap route and price quote on Awaken DEX. Use this when you need to know how much tokenOut you will receive for a given tokenIn amount. Returns amountIn, amountOut, route splits, fee rates.',
    inputSchema: {
      symbolIn: z.string().describe('Input token symbol (e.g. ELF)'),
      symbolOut: z.string().describe('Output token symbol (e.g. USDT)'),
      amountIn: z.string().optional().describe('Human-readable amount of input token (e.g. "100")'),
      amountOut: z.string().optional().describe('Human-readable amount of output token for reverse quote'),
      network: z.enum(['mainnet', 'testnet']).default('mainnet').describe('Network environment'),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ symbolIn, symbolOut, amountIn, amountOut, network }) => {
    try {
      const config = getNetworkConfig(network);
      const result = await getQuote(config, { symbolIn, symbolOut, amountIn, amountOut });
      return ok(result);
    } catch (err) {
      return fail(err);
    }
  },
);

registerTool(
  'awaken_pair',
  {
    description:
      'Get detailed trade pair information from Awaken DEX. Returns pair ID, price, TVL, volume, and reserve data. The returned pair ID is needed for K-line queries.',
    inputSchema: {
      token0: z.string().describe('First token symbol (e.g. ELF)'),
      token1: z.string().describe('Second token symbol (e.g. USDT)'),
      feeRate: z.string().default('0.3').describe('Fee tier: 0.05, 0.1, 0.3, 3, or 5'),
      network: z.enum(['mainnet', 'testnet']).default('mainnet'),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ token0, token1, feeRate, network }) => {
    try {
      const config = getNetworkConfig(network);
      const result = await getPair(config, { token0, token1, feeRate });
      return ok(result);
    } catch (err) {
      return fail(err);
    }
  },
);

registerTool(
  'awaken_balance',
  {
    description: 'Query the token balance of an aelf address on-chain. Returns human-readable balance.',
    inputSchema: {
      address: z.string().describe('aelf wallet address'),
      symbol: z.string().describe('Token symbol (e.g. ELF, USDT)'),
      network: z.enum(['mainnet', 'testnet']).default('mainnet'),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ address, symbol, network }) => {
    try {
      const config = getNetworkConfig(network);
      const result = await getTokenBalance(config, { address, symbol });
      return ok(result);
    } catch (err) {
      return fail(err);
    }
  },
);

registerTool(
  'awaken_allowance',
  {
    description:
      'Query the token spending allowance between an owner and a spender contract. Returns human-readable allowance amount.',
    inputSchema: {
      owner: z.string().describe('Token holder address'),
      spender: z.string().describe('Approved contract address'),
      symbol: z.string().describe('Token symbol'),
      network: z.enum(['mainnet', 'testnet']).default('mainnet'),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ owner, spender, symbol, network }) => {
    try {
      const config = getNetworkConfig(network);
      const result = await getTokenAllowance(config, { owner, spender, symbol });
      return ok(result);
    } catch (err) {
      return fail(err);
    }
  },
);

registerTool(
  'awaken_liquidity',
  {
    description:
      'Query all liquidity positions for an aelf address on Awaken DEX, including USD value. Returns list of positions with lpTokenAmount, token amounts, assetUSD, pairPrice, feeRate, and portfolio detail with positionValueUSD, feeEarnedUSD, APR when available.',
    inputSchema: {
      address: z.string().describe('Wallet address'),
      token0: z.string().optional().describe('Filter by token symbol'),
      token1: z.string().optional().describe('Filter by token symbol'),
      network: z.enum(['mainnet', 'testnet']).default('mainnet'),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ address, token0, token1, network }) => {
    try {
      const config = getNetworkConfig(network);
      const result = await getLiquidityPositions(config, { address, token0, token1 });
      return ok(result);
    } catch (err) {
      return fail(err);
    }
  },
);

// ============================================================
// Trade Tools (require AELF_PRIVATE_KEY or PORTKEY_PRIVATE_KEY + CA env vars)
// ============================================================

registerTool(
  'awaken_swap',
  {
    description:
      'Execute a token swap on Awaken DEX. Signer resolution order: explicit signer input, active wallet context, then env fallback. Sends a real on-chain transaction. Auto-queries route, approves if needed, then executes swap.',
    inputSchema: {
      symbolIn: z.string().describe('Token to sell (e.g. ELF)'),
      symbolOut: z.string().describe('Token to buy (e.g. USDT)'),
      amountIn: z.string().describe('Human-readable amount to sell (e.g. "1.5")'),
      slippage: z.string().default('0.005').describe('Slippage tolerance (0.005 = 0.5%)'),
      network: z.enum(['mainnet', 'testnet']).default('mainnet'),
      signer: signerInputSchema,
    },
    annotations: NETWORK_WRITE_ANNOTATIONS,
  },
  async ({ symbolIn, symbolOut, amountIn, slippage, network, signer }) => {
    try {
      const config = getNetworkConfig(network);
      const resolved = resolveSignerContext({
        signerMode: 'auto',
        ...signer,
      });
      const result = await executeSwap(config, resolved.signer, { symbolIn, symbolOut, amountIn, slippage });
      return ok(result);
    } catch (err) {
      return fail(err);
    }
  },
);

registerTool(
  'awaken_add_liquidity',
  {
    description:
      'Add liquidity to an Awaken DEX trading pair. Signer resolution order: explicit signer input, active wallet context, then env fallback.',
    inputSchema: {
      tokenA: z.string().describe('Token A symbol (e.g. ELF)'),
      tokenB: z.string().describe('Token B symbol (e.g. USDT)'),
      amountA: z.string().describe('Human-readable amount of token A'),
      amountB: z.string().describe('Human-readable amount of token B'),
      feeRate: z.string().default('0.3').describe('Pool fee tier (0.05, 0.1, 0.3, 3, or 5)'),
      slippage: z.string().default('0.005').describe('Slippage tolerance'),
      network: z.enum(['mainnet', 'testnet']).default('mainnet'),
      signer: signerInputSchema,
    },
    annotations: NETWORK_WRITE_ANNOTATIONS,
  },
  async ({ tokenA, tokenB, amountA, amountB, feeRate, slippage, network, signer }) => {
    try {
      const config = getNetworkConfig(network);
      const resolved = resolveSignerContext({
        signerMode: 'auto',
        ...signer,
      });
      const result = await addLiquidity(config, resolved.signer, { tokenA, tokenB, amountA, amountB, feeRate, slippage });
      return ok(result);
    } catch (err) {
      return fail(err);
    }
  },
);

registerTool(
  'awaken_remove_liquidity',
  {
    description:
      'Remove liquidity from an Awaken DEX trading pair. Signer resolution order: explicit signer input, active wallet context, then env fallback.',
    inputSchema: {
      tokenA: z.string().describe('Token A symbol'),
      tokenB: z.string().describe('Token B symbol'),
      lpAmount: z.string().describe('LP token amount to burn (human-readable)'),
      feeRate: z.string().default('0.3').describe('Pool fee tier'),
      network: z.enum(['mainnet', 'testnet']).default('mainnet'),
      signer: signerInputSchema,
    },
    annotations: NETWORK_WRITE_ANNOTATIONS,
  },
  async ({ tokenA, tokenB, lpAmount, feeRate, network, signer }) => {
    try {
      const config = getNetworkConfig(network);
      const resolved = resolveSignerContext({
        signerMode: 'auto',
        ...signer,
      });
      const result = await removeLiquidity(config, resolved.signer, { tokenA, tokenB, lpAmount, feeRate });
      return ok(result);
    } catch (err) {
      return fail(err);
    }
  },
);

registerTool(
  'awaken_approve',
  {
    description:
      'Approve a contract to spend your tokens. Signer resolution order: explicit signer input, active wallet context, then env fallback.',
    inputSchema: {
      symbol: z.string().describe('Token to approve (e.g. ELF)'),
      spender: z.string().describe('Contract address to approve'),
      amount: z.string().describe('Human-readable amount to approve'),
      network: z.enum(['mainnet', 'testnet']).default('mainnet'),
      signer: signerInputSchema,
    },
    annotations: NETWORK_WRITE_ANNOTATIONS,
  },
  async ({ symbol, spender, amount, network, signer }) => {
    try {
      const config = getNetworkConfig(network);
      const resolved = resolveSignerContext({
        signerMode: 'auto',
        ...signer,
      });
      const result = await approveTokenSpending(config, resolved.signer, { symbol, spender, amount });
      return ok(result);
    } catch (err) {
      return fail(err);
    }
  },
);

// ============================================================
// K-Line Tools
// ============================================================

registerTool(
  'awaken_kline_fetch',
  {
    description:
      'Fetch historical K-line (candlestick) data for a trading pair via SignalR. Use awaken_pair first to get the pair ID. Returns array of OHLCV bars.',
    inputSchema: {
      tradePairId: z.string().describe('Trade pair UUID (from awaken_pair result)'),
      interval: z.string().default('1D').describe('Time interval: 1m, 15m, 30m, 1h, 4h, 1D, 1W'),
      from: z.string().optional().describe('Start date (ISO string or unix ms)'),
      to: z.string().optional().describe('End date (ISO string or unix ms)'),
      timeout: z.number().default(15000).describe('Max wait time in ms'),
      network: z.enum(['mainnet', 'testnet']).default('mainnet'),
    },
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async ({ tradePairId, interval, from, to, timeout, network }) => {
    try {
      const config = getNetworkConfig(network);
      const result = await fetchKline(config, { tradePairId, interval, from, to, timeout });
      return ok(result);
    } catch (err) {
      return fail(err);
    }
  },
);

registerTool(
  'awaken_kline_intervals',
  {
    description: 'List all supported K-line time intervals with their period in seconds.',
    inputSchema: {},
    annotations: READ_ONLY_ANNOTATIONS,
  },
  async () => {
    return ok(getKlineIntervals());
  },
);

// ============================================================
// Start server
// ============================================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Awaken Agent Kit MCP Server running on stdio');
}

main().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
