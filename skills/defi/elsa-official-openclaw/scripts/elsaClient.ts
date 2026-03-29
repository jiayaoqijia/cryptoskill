import { callElsaApi } from './x402Client.js';
import { getLogger } from './util.js';
import type {
  ElsaSearchTokenResponse,
  ElsaTokenPriceResponse,
  ElsaBalancesResponse,
  ElsaPortfolioResponse,
  ElsaAnalyzeWalletResponse,
  ElsaSwapQuoteResponse,
  ElsaExecuteSwapResponse,
  ElsaPipelineStatusResponse,
  ElsaSubmitTxHashResponse,
  ElsaGetLimitOrdersResponse,
  ElsaCreateLimitOrderResponse,
  ElsaCancelLimitOrderResponse,
  ElsaGetPerpPositionsResponse,
  ElsaOpenPerpPositionResponse,
  ElsaClosePerpPositionResponse,
  ElsaGetTransactionHistoryResponse,
} from './types.js';

// ============================================================================
// Elsa API Methods
// ============================================================================

export async function searchToken(query: string, limit: number = 10) {
  return callElsaApi<ElsaSearchTokenResponse>('/api/search_token', {
    symbol_or_address: query,
    limit,
  });
}

export async function getTokenPrice(tokenAddress: string, chain: string = 'base') {
  const logger = getLogger();

  // Try the dedicated price endpoint first
  const result = await callElsaApi<ElsaTokenPriceResponse>('/api/get_token_price', {
    token_address: tokenAddress,
    chain,
  });

  // Check if response has valid price data
  const data = result.data as unknown as Record<string, unknown>;
  const hasPrice = data.price_usd !== undefined && data.price_usd !== null && data.price_usd !== '';
  const hasSymbol = typeof data.symbol === 'string' && data.symbol.length > 0;

  if (hasPrice && hasSymbol) {
    return result;
  }

  // Fallback: Use search_token to get price data
  logger.info({ token_address: tokenAddress, chain }, 'get_token_price returned empty data, falling back to search_token');

  const searchResult = await callElsaApi<ElsaSearchTokenResponse>('/api/search_token', {
    symbol_or_address: tokenAddress,
    limit: 20,
  });

  // Find matching token by address (case-insensitive)
  const searchData = searchResult.data as { results?: Array<{ address: string; symbol: string; name: string; priceUSD?: string; decimals?: number }> };
  const normalizedAddress = tokenAddress.toLowerCase();
  const matchingToken = searchData.results?.find(
    (t) => t.address.toLowerCase() === normalizedAddress
  );

  if (matchingToken) {
    // Merge search data into price response format
    const enrichedData: ElsaTokenPriceResponse = {
      token_address: tokenAddress,
      chain,
      symbol: matchingToken.symbol,
      name: matchingToken.name,
      price_usd: matchingToken.priceUSD || '0',
      decimals: matchingToken.decimals,
      _fallback_used: true,
    };

    return {
      data: enrichedData,
      billing: {
        estimated_cost_usd: result.billing.estimated_cost_usd + searchResult.billing.estimated_cost_usd,
        payment_required: true,
        receipt: null,
        protocol: 'x402',
      },
      meta: {
        ...result.meta,
        fallback_used: true,
      },
    };
  }

  // No match found, return original (empty) result
  logger.warn({ token_address: tokenAddress, chain }, 'Fallback search did not find matching token');
  return result;
}

export async function getBalances(walletAddress: string) {
  return callElsaApi<ElsaBalancesResponse>('/api/get_balances', {
    wallet_address: walletAddress,
  });
}

export async function getPortfolio(walletAddress: string) {
  return callElsaApi<ElsaPortfolioResponse>('/api/get_portfolio', {
    wallet_address: walletAddress,
  });
}

export async function analyzeWallet(walletAddress: string) {
  return callElsaApi<ElsaAnalyzeWalletResponse>('/api/analyze_wallet', {
    wallet_address: walletAddress,
  });
}

export async function getSwapQuote(params: {
  from_chain: string;
  from_token: string;
  from_amount: string;
  to_chain: string;
  to_token: string;
  wallet_address: string;
  slippage: number;
}) {
  return callElsaApi<ElsaSwapQuoteResponse>('/api/get_swap_quote', params);
}

export async function executeSwap(params: {
  from_chain: string;
  from_token: string;
  from_amount: string;
  to_chain: string;
  to_token: string;
  wallet_address: string;
  slippage: number;
  dry_run: boolean;
}) {
  return callElsaApi<ElsaExecuteSwapResponse>('/api/execute_swap', params);
}

export async function getPipelineStatus(pipelineId: string) {
  return callElsaApi<ElsaPipelineStatusResponse>('/api/get_transaction_status', {
    pipeline_id: pipelineId,
  });
}

export async function submitTransactionHash(taskId: string, txHash: string) {
  return callElsaApi<ElsaSubmitTxHashResponse>('/api/submit_transaction_hash', {
    task_id: taskId,
    tx_hash: txHash,
  });
}

// ============================================================================
// Limit Order Methods
// ============================================================================

export async function getLimitOrders(walletAddress: string, chain: string = 'base') {
  return callElsaApi<ElsaGetLimitOrdersResponse>('/api/get_limit_orders', {
    wallet_address: walletAddress,
    chain,
  });
}

export async function createLimitOrder(params: {
  wallet_address: string;
  chain: string;
  from_token: string;
  to_token: string;
  from_amount: string;
  limit_price: string;
  expiry_hours: number;
}) {
  return callElsaApi<ElsaCreateLimitOrderResponse>('/api/create_limit_order', params);
}

export async function cancelLimitOrder(walletAddress: string, orderId: string, chain: string = 'base') {
  return callElsaApi<ElsaCancelLimitOrderResponse>('/api/cancel_limit_order', {
    wallet_address: walletAddress,
    order_id: orderId,
    chain,
  });
}

// ============================================================================
// Perpetuals Methods
// ============================================================================

export async function getPerpPositions(walletAddress: string) {
  return callElsaApi<ElsaGetPerpPositionsResponse>('/api/get_perp_positions', {
    wallet_address: walletAddress,
  });
}

export async function openPerpPosition(params: {
  wallet_address: string;
  market: string;
  side: 'long' | 'short';
  size_usd: string;
  leverage: number;
  take_profit?: string;
  stop_loss?: string;
}) {
  return callElsaApi<ElsaOpenPerpPositionResponse>('/api/open_perp_position', params);
}

export async function closePerpPosition(params: {
  wallet_address: string;
  position_id: string;
  close_percentage: number;
}) {
  return callElsaApi<ElsaClosePerpPositionResponse>('/api/close_perp_position', params);
}

// ============================================================================
// Transaction History Methods
// ============================================================================

export async function getTransactionHistory(walletAddress: string, chain?: string, limit: number = 20) {
  return callElsaApi<ElsaGetTransactionHistoryResponse>('/api/get_transaction_history', {
    wallet_address: walletAddress,
    chain,
    limit,
  });
}
