import axios from 'axios';

interface TokenPrice {
  usd: number;
}

interface PriceResponse {
  [key: string]: TokenPrice;
}

// Coingecko token IDs mapping
const COINGECKO_TOKEN_IDS: Record<string, string> = {
  'NEAR': 'near',
  'WNEAR': 'near',  // Wrapped NEAR maps to NEAR
  'WNear': 'near',
  'wNEAR': 'near',
  'USDC': 'usd-coin',
  'USDT': 'tether',
  'DAI': 'dai',
  'ETH': 'ethereum',
  'WETH': 'ethereum',
  'SOL': 'solana',
  'WSOL': 'solana',
  'wSOL': 'solana',
  'WBTC': 'wrapped-bitcoin',
  'BTC': 'bitcoin',
};

/**
 * Fetch prices from Coingecko API
 * @param tokenSymbols Array of token symbols (e.g., ['NEAR', 'USDC'])
 * @returns Map of token symbol to price in USD
 */
export async function getPrices(tokenSymbols: string[]): Promise<Map<string, number>> {
  try {
    // Map token symbols to Coingecko IDs
    const coingeckoIds: string[] = [];
    const symbolMap: Map<string, string> = new Map();

    for (const symbol of tokenSymbols) {
      const upperSymbol = symbol.toUpperCase();
      console.log(`[PriceService] Looking up token: ${upperSymbol}`);
      if (COINGECKO_TOKEN_IDS[upperSymbol]) {
        const coingeckoId = COINGECKO_TOKEN_IDS[upperSymbol];
        coingeckoIds.push(coingeckoId);
        symbolMap.set(coingeckoId, upperSymbol);
        console.log(`[PriceService] Mapped ${upperSymbol} -> ${coingeckoId}`);
      } else {
        console.log(`[PriceService] No Coingecko ID found for ${upperSymbol}`);
      }
    }

    if (coingeckoIds.length === 0) {
      console.log('[PriceService] No valid token IDs for Coingecko');
      return new Map();
    }

    // Fetch prices from Coingecko
    const response = await axios.get<PriceResponse>(
      `https://api.coingecko.com/api/v3/simple/price`,
      {
        params: {
          ids: coingeckoIds.join(','),
          vs_currencies: 'usd',
        },
        timeout: 10000,
      }
    );

    const data = response.data;
    const prices: Map<string, number> = new Map();

    for (const [coingeckoId, priceData] of Object.entries(data)) {
      const symbol = symbolMap.get(coingeckoId);
      if (symbol && priceData.usd) {
        prices.set(symbol, priceData.usd);
        console.log(`[PriceService] ${symbol}: $${priceData.usd}`);
      }
    }

    return prices;
  } catch (error: any) {
    console.error('[PriceService] Error fetching prices:', error.message);
    // Return empty map on error to not block execution
    return new Map();
  }
}

/**
 * Get price for a single token
 * @param tokenSymbol Token symbol (e.g., 'NEAR')
 * @returns Price in USD, or 0 if not found
 */
export async function getPrice(tokenSymbol: string): Promise<number> {
  const prices = await getPrices([tokenSymbol]);
  return prices.get(tokenSymbol.toUpperCase()) || 0;
}

/**
 * Calculate USD value of an amount
 * @param tokenSymbol Token symbol (e.g., 'NEAR')
 * @param amount Amount of tokens
 * @returns USD value
 */
export async function calculateUSDValue(
  tokenSymbol: string,
  amount: string
): Promise<number> {
  const price = await getPrice(tokenSymbol);
  const amountNum = parseFloat(amount);
  return price * amountNum;
}

/**
 * Check if amount meets minimum USD value
 * @param tokenSymbol Token symbol (e.g., 'NEAR')
 * @param amount Amount of tokens
 * @param minimumUSD Minimum USD value (default $0.2)
 * @returns Object with check result and details
 */
export async function checkMinimumUSDValue(
  tokenSymbol: string,
  amount: string,
  minimumUSD: number = 0.2
): Promise<{ valid: boolean; usdValue: number; minimumUSD: number }> {
  const usdValue = await calculateUSDValue(tokenSymbol, amount);
  return {
    valid: usdValue >= minimumUSD,
    usdValue,
    minimumUSD,
  };
}
