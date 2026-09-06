// ============================================================
// Awaken Agent Kit - Package Entry
// ============================================================
// Import core functions directly for use in LangChain, LlamaIndex,
// or any TypeScript/JavaScript project.
//
// Usage:
//   import { getQuote, executeSwap, getNetworkConfig } from '@awaken-finance/agent-kit';

// ---- Core: Query ----
export { getQuote, getPair, getTokenBalance, getTokenAllowance, getLiquidityPositions } from './src/core/query';

// ---- Core: Trade ----
export { executeSwap, addLiquidity, removeLiquidity, approveTokenSpending } from './src/core/trade';

// ---- Core: K-Line ----
export { fetchKline, getKlineIntervals } from './src/core/kline';

// ---- Config ----
export { getNetworkConfig, getRouterAddress, DEFAULT_SLIPPAGE } from './lib/config';

// ---- aelf Client Utilities ----
export { getWalletByPrivateKey, getTokenInfo, timesDecimals, divDecimals } from './lib/aelf-client';
export { resolveSignerContext, SignerContextError } from './lib/signer-context';
export {
  readWalletContext,
  writeWalletContext,
  getActiveWalletProfile,
  setActiveWalletProfile,
} from './lib/wallet-context';

// ---- Types ----
export type {
  NetworkConfig,
  TokenInfo,
  GetQuoteParams,
  QuoteResult,
  SwapRouteDistribution,
  GetPairParams,
  TradePairItem,
  GetBalanceParams,
  BalanceResult,
  GetAllowanceParams,
  AllowanceResult,
  LiquidityQueryParams,
  LiquidityResult,
  LiquidityPosition,
  LiquidityPortfolioItem,
  KLineBar,
  FetchKlineParams,
  KlineResult,
  SwapParams,
  SwapResult,
  LiquidityAddParams,
  LiquidityAddResult,
  LiquidityRemoveParams,
  LiquidityRemoveResult,
  ApproveParams,
  ApproveResult,
  TxResult,
} from './lib/types';

export { KLINE_INTERVALS } from './lib/types';

export type {
  SignerMode,
  SignerProvider,
  SignerContextInput,
  WalletType,
  WalletSource,
  ActiveWalletProfile,
  WalletContextFile,
} from './lib/wallet-context';
