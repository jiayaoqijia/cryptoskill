import type {
  PortkeyConfig,
  ChainId,
  TokenBalanceParams,
  TokenBalanceResult,
  TokenListParams,
  TokenListResult,
  NftCollectionParams,
  NftCollectionResult,
  NftItemParams,
  NftItemResult,
  TokenPriceParams,
  TokenPriceItem,
  TokenListDataSource,
  TokenListStrategy,
} from '../../lib/types.js';
import { createHttpClient, HttpError } from '../../lib/http.js';
import { callViewMethod } from '../../lib/aelf-client.js';
import { getChainInfoByChainId } from './account.js';

// ============================================================================
// getTokenBalance
// ============================================================================

/**
 * Get the balance of a specific token for a CA address on a specific chain.
 *
 * Uses on-chain view call: GetBalance({ symbol, owner })
 */
export async function getTokenBalance(
  config: PortkeyConfig,
  params: TokenBalanceParams,
): Promise<TokenBalanceResult> {
  if (!params.caAddress) throw new Error('caAddress is required');
  if (!params.chainId) throw new Error('chainId is required');
  if (!params.symbol) throw new Error('symbol is required');

  const chainInfo = await getChainInfoByChainId(config, params.chainId);

  // On aelf, ALL fungible tokens (ELF, USDT, etc.) live in the same MultiToken
  // contract. chainInfo.defaultToken.address IS the MultiToken contract address,
  // so this works for any symbol — not just the default token.
  const tokenContractAddress = chainInfo.defaultToken.address;

  const [result, tokenInfo] = await Promise.all([
    callViewMethod<{ symbol: string; owner: string; balance: string }>(
      chainInfo.endPoint,
      tokenContractAddress,
      'GetBalance',
      { symbol: params.symbol, owner: params.caAddress },
    ),
    // Fetch actual token info to get correct decimals (ELF=8, USDT=6, etc.)
    callViewMethod<{ symbol: string; decimals: number }>(
      chainInfo.endPoint,
      tokenContractAddress,
      'GetTokenInfo',
      { symbol: params.symbol },
    ).catch(() => null), // fallback to defaultToken.decimals if GetTokenInfo fails
  ]);

  return {
    symbol: result.symbol || params.symbol,
    balance: result.balance || '0',
    decimals: tokenInfo?.decimals ?? chainInfo.defaultToken.decimals,
    tokenContractAddress,
  };
}

// ============================================================================
// getTokenList
// ============================================================================

/**
 * Get all tokens with balances for the given CA addresses across chains.
 *
 * API: POST /api/app/user/assets/token
 */
export async function getTokenList(
  config: PortkeyConfig,
  params: TokenListParams,
): Promise<TokenListResult> {
  if (!params.caAddressInfos?.length) throw new Error('caAddressInfos is required');

  const strategy: TokenListStrategy = params.strategy || 'auto';
  if (!['aa', 'auto', 'eoa'].includes(strategy)) {
    throw new Error(`strategy must be one of: aa | auto | eoa`);
  }

  if (strategy === 'aa') {
    return getTokenListFromAa(config, params, 'aa');
  }

  if (strategy === 'eoa') {
    return getTokenListFromEoa(config, params, 'eoa-direct');
  }

  try {
    return await getTokenListFromAa(config, params, 'aa');
  } catch (err) {
    if (!isUnauthorizedError(err)) throw err;
    if (!isEoaFallbackEnabled(config)) {
      throw new Error(
        "AA token-list returned 401 and EOA fallback is disabled. Set PORTKEY_EOA_FALLBACK_ENABLED=true to enable fallback, or use strategy='eoa' to query EOA directly (or strategy='aa' for AA-only).",
      );
    }
    return getTokenListFromEoa(config, params, 'eoa-fallback');
  }
}

async function getTokenListFromAa(
  config: PortkeyConfig,
  params: TokenListParams,
  dataSource: TokenListDataSource,
): Promise<TokenListResult> {
  const http = createHttpClient(config);

  const result = await http.post<TokenListResult>('/api/app/user/assets/token', {
    data: {
      caAddressInfos: params.caAddressInfos,
      skipCount: params.skipCount || 0,
      maxResultCount: params.maxResultCount || 100,
    },
  });

  return { ...result, dataSource };
}

async function getTokenListFromEoa(
  config: PortkeyConfig,
  params: TokenListParams,
  dataSource: TokenListDataSource,
): Promise<TokenListResult> {
  const eoaConfig: PortkeyConfig = {
    ...config,
    apiUrl: resolveEoaApiUrl(config),
  };
  const eoaHttp = createHttpClient(eoaConfig);

  const chainIds = await getEoaAvailableChainIds(eoaConfig, eoaHttp, params.caAddressInfos);
  const uniqueAddresses = [...new Set(params.caAddressInfos.map((item) => item.caAddress))];
  const addressInfos = uniqueAddresses.flatMap((address) =>
    chainIds.map((chainId) => ({ chainId, address })),
  );

  const result = await withEoaRetry(
    eoaConfig,
    () => eoaHttp.post<TokenListResult & Record<string, unknown>>('/api/app/user/assets/token', {
      data: {
        addressInfos,
        skipCount: params.skipCount || 0,
        maxResultCount: params.maxResultCount || 100,
      },
    }),
    'EOA token-list',
  );

  return {
    ...result,
    dataSource,
  };
}

function resolveEoaApiUrl(config: PortkeyConfig): string {
  const eoaApiUrl = String(config.eoaApiUrl || '').trim();
  if (!eoaApiUrl) {
    throw new Error(
      `EOA fallback is enabled but eoaApiUrl is missing for network "${config.network}". Set PORTKEY_EOA_API_URL.`,
    );
  }
  return eoaApiUrl;
}

async function getEoaAvailableChainIds(
  config: PortkeyConfig,
  http: ReturnType<typeof createHttpClient>,
  caAddressInfos: TokenListParams['caAddressInfos'],
): Promise<string[]> {
  try {
    const chainInfo = await withEoaRetry(
      config,
      () => http.get<{ items?: Array<{ chainId?: string }> }>('/api/app/search/chainsinfoindex'),
      'EOA chainsinfoindex',
    );
    const chainIds = [...new Set((chainInfo.items || []).map((item) => item.chainId).filter(Boolean))] as string[];
    if (chainIds.length > 0) return chainIds;
  } catch {
    // Fall back to user-provided chains below.
  }

  const fallbackChainIds = [...new Set(caAddressInfos.map((item) => item.chainId))];
  if (fallbackChainIds.length === 0) {
    throw new Error('Unable to resolve chain IDs for EOA token-list fallback');
  }
  return fallbackChainIds;
}

async function withEoaRetry<T>(
  config: PortkeyConfig,
  fn: () => Promise<T>,
  operationName: string,
): Promise<T> {
  const configuredAttempts = Number(config.eoaFallbackRetryCount);
  const attempts = Number.isInteger(configuredAttempts) && configuredAttempts >= 1
    ? configuredAttempts
    : 1;
  const configuredDelay = Number(config.eoaFallbackRetryDelayMs);
  const delayUnitMs = Number.isFinite(configuredDelay) && configuredDelay >= 1
    ? configuredDelay
    : 200;
  let lastError: unknown;

  for (let i = 1; i <= attempts; i += 1) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      const canRetry = i < attempts && isRetryableEoaError(err);
      if (!canRetry) break;
      const delayMs = delayUnitMs * i;
      await sleep(delayMs);
    }
  }

  if (lastError instanceof Error) {
    throw new Error(`${operationName} failed after ${attempts} attempt(s): ${lastError.message}`);
  }
  throw new Error(`${operationName} failed after ${attempts} attempt(s).`);
}

function isRetryableEoaError(err: unknown): boolean {
  if (err instanceof HttpError) {
    if (err.statusCode === 408 || err.statusCode === 429) return true;
    if (err.statusCode >= 500) return true;
    return false;
  }
  return true;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isEoaFallbackEnabled(config: PortkeyConfig): boolean {
  return config.eoaFallbackEnabled !== false;
}

function isUnauthorizedError(err: unknown): boolean {
  if (err instanceof HttpError && err.statusCode === 401) return true;
  if (err instanceof Error && /HTTP 401|Unauthorized/i.test(err.message)) return true;
  return false;
}

// ============================================================================
// getNftCollections
// ============================================================================

/**
 * Get NFT collections for the given CA addresses.
 *
 * API: POST /api/app/user/assets/nftCollections
 */
export async function getNftCollections(
  config: PortkeyConfig,
  params: NftCollectionParams,
): Promise<NftCollectionResult> {
  if (!params.caAddressInfos?.length) throw new Error('caAddressInfos is required');

  const http = createHttpClient(config);

  const result = await http.post<NftCollectionResult>('/api/app/user/assets/nftCollections', {
    data: {
      caAddressInfos: params.caAddressInfos,
      skipCount: params.skipCount || 0,
      maxResultCount: params.maxResultCount || 100,
    },
  });

  return result;
}

// ============================================================================
// getNftItems
// ============================================================================

/**
 * Get NFT items within a collection.
 *
 * API: POST /api/app/user/assets/nftItems
 */
export async function getNftItems(
  config: PortkeyConfig,
  params: NftItemParams,
): Promise<NftItemResult> {
  if (!params.caAddressInfos?.length) throw new Error('caAddressInfos is required');
  if (!params.symbol) throw new Error('symbol is required');

  const http = createHttpClient(config);

  const result = await http.post<NftItemResult>('/api/app/user/assets/nftItems', {
    data: {
      caAddressInfos: params.caAddressInfos,
      symbol: params.symbol,
      skipCount: params.skipCount || 0,
      maxResultCount: params.maxResultCount || 100,
    },
  });

  return result;
}

// ============================================================================
// getTokenPrice
// ============================================================================

/**
 * Get token prices in USD.
 *
 * API: GET /api/app/tokens/prices
 */
export async function getTokenPrice(
  config: PortkeyConfig,
  params: TokenPriceParams,
): Promise<TokenPriceItem[]> {
  if (!params.symbols?.length) throw new Error('symbols is required');

  const http = createHttpClient(config);

  const result = await http.get<{ items: TokenPriceItem[] }>('/api/app/tokens/prices', {
    params: { symbols: params.symbols.join(',') },
  });

  return result.items || [];
}
