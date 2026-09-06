// ============================================================
// Awaken Agent Kit - Shared Types
// ============================================================

/** Standard CLI output envelope */
export interface SkillOutput<T = unknown> {
  status: 'success' | 'error';
  data?: T;
  error?: string;
}

// ---- Network & Config ----

export interface NetworkConfig {
  chainId: string;
  rpcUrl: string;
  apiBaseUrl: string;
  socketUrl: string;
  explorerUrl: string;
  tokenContract: string;
  swapHookContract: string;
  router: Record<string, string>;
  factory: Record<string, string>;
}

// ---- Token ----

export interface TokenInfo {
  symbol: string;
  decimals: number;
  address?: string;
  id?: string;
}

// ---- Swap / Quote ----

export interface GetQuoteParams {
  symbolIn: string;
  symbolOut: string;
  amountIn?: string;
  amountOut?: string;
}

export interface QuoteParams {
  symbolIn: string;
  symbolOut: string;
  amountIn?: string;
  amountOut?: string;
  routeType: 0 | 1; // 0 = exact in, 1 = exact out
}

export interface QuoteResult {
  amountIn: string;
  amountOut: string;
  splits: number;
  distributions: SwapRouteDistribution[];
}

export interface SwapRouteDistribution {
  percent: number;
  amountIn: string;
  amountOut: string;
  tokens: TokenInfo[];
  feeRates: number[];
}

// ---- Trade Pair ----

export interface GetPairParams {
  token0: string;
  token1: string;
  feeRate?: string; // e.g. "0.3"
}

export interface TradePairParams {
  token0Symbol?: string;
  token1Symbol?: string;
  feeRate?: string;
  chainId?: string;
}

export interface TradePairItem {
  id: string;
  address: string;
  token0: TokenInfo;
  token1: TokenInfo;
  feeRate: number;
  price: number;
  priceUSD: number;
  tvl: number;
  volume24h: number;
  valueLocked0: string;
  valueLocked1: string;
}

// ---- Balance / Allowance ----

export interface GetBalanceParams {
  address: string;
  symbol: string;
}

export interface BalanceResult {
  symbol: string;
  owner: string;
  balance: string;
}

export interface GetAllowanceParams {
  owner: string;
  spender: string;
  symbol: string;
}

export interface AllowanceResult {
  symbol: string;
  owner: string;
  spender: string;
  allowance: string;
}

// ---- Liquidity Query ----

export interface LiquidityQueryParams {
  address: string;
  token0?: string;
  token1?: string;
}

export interface LiquidityPosition {
  pairId: string;
  token0: { symbol: string; decimals: number };
  token1: { symbol: string; decimals: number };
  feeRate: string;
  lpTokenAmount: string;
  lpTokenAmountOnChain: string | number;
  token0Amount: string;
  token1Amount: string;
  assetUSD: number | null;
  pairPrice: number | null;
}

export interface LiquidityPortfolioItem {
  pairId: string;
  pair: string;
  feeRate: string;
  lpTokenAmount: string;
  lpTokenPercent: string;
  positionValueUSD: string;
  token0Amount: string;
  token0ValueUSD: string;
  token1Amount: string;
  token1ValueUSD: string;
  feeEarnedUSD: string;
  impermanentLossUSD: string;
  estimatedAPR: any[];
  dynamicAPR: string;
}

export interface LiquidityResult {
  address: string;
  totalPositions: number;
  positions: LiquidityPosition[];
  portfolioDetail?: LiquidityPortfolioItem[];
}

// ---- K-Line ----

export interface KLineParams {
  chainId: string;
  tradePairId: string;
  type: number; // period in seconds
  from: number; // unix ms
  to: number;   // unix ms
}

export interface KLineBar {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export const KLINE_INTERVALS: Record<string, number> = {
  '1m': 60,
  '15m': 60 * 15,
  '30m': 60 * 30,
  '1h': 3600,
  '4h': 3600 * 4,
  '1D': 3600 * 24,
  '1W': 3600 * 24 * 7,
};

export interface FetchKlineParams {
  tradePairId: string;
  interval?: string; // "1m", "15m", "1D", etc.
  from?: string | number; // ISO date or unix ms
  to?: string | number;
  timeout?: number;
}

export interface KlineResult {
  pairId: string;
  interval: string;
  periodSeconds: number;
  from: string;
  to: string;
  count: number;
  bars: KLineBar[];
}

// ---- Swap Execution ----

export interface SwapParams {
  symbolIn: string;
  symbolOut: string;
  amountIn: string;
  slippage?: string; // e.g. "0.005" = 0.5%
}

export interface SwapResult extends TxResult {
  symbolIn: string;
  symbolOut: string;
  amountIn: string;
  estimatedAmountOut: string;
  minAmountOut: string;
  explorerUrl: string;
}

// ---- Liquidity Execution ----

export interface LiquidityAddParams {
  tokenA: string;
  tokenB: string;
  amountA: string;
  amountB: string;
  feeRate?: string;
  slippage?: string;
}

export interface LiquidityAddResult extends TxResult {
  tokenA: string;
  tokenB: string;
  amountA: string;
  amountB: string;
  feeRate: string;
  explorerUrl: string;
}

export interface LiquidityRemoveParams {
  tokenA: string;
  tokenB: string;
  lpAmount: string;
  feeRate?: string;
  slippage?: string;
}

export interface LiquidityRemoveResult extends TxResult {
  tokenA: string;
  tokenB: string;
  lpAmount: string;
  explorerUrl: string;
}

// ---- Approve ----

export interface ApproveParams {
  symbol: string;
  spender: string;
  amount: string;
}

export interface ApproveResult extends TxResult {
  symbol: string;
  spender: string;
  amount: string;
  explorerUrl: string;
}

// ---- Transaction ----

export interface TxResult {
  transactionId: string;
  status: string;
}
