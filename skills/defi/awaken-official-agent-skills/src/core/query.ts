// ============================================================
// Core: Read-only DEX query functions (no I/O, pure logic)
// ============================================================

import axios from 'axios';
import BigNumber from 'bignumber.js';
import {
  callViewMethod,
  getBalance,
  getAllowance,
  getTokenInfo,
  divDecimals,
} from '../../lib/aelf-client';
import type {
  NetworkConfig,
  GetQuoteParams,
  QuoteResult,
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
} from '../../lib/types';

// ---- getQuote ----

export async function getQuote(
  config: NetworkConfig,
  params: GetQuoteParams,
): Promise<QuoteResult> {
  const { symbolIn, symbolOut, amountIn, amountOut } = params;

  if (!amountIn && !amountOut) {
    throw new Error('Either amountIn or amountOut is required');
  }

  const tokenInInfo = await getTokenInfo(config.rpcUrl, config.tokenContract, symbolIn);
  const tokenOutInfo = await getTokenInfo(config.rpcUrl, config.tokenContract, symbolOut);

  const apiParams: Record<string, any> = {
    ChainId: config.chainId,
    symbolIn,
    symbolOut,
    routeType: amountIn ? 0 : 1,
  };

  if (amountIn) {
    apiParams.amountIn = new BigNumber(amountIn)
      .times(new BigNumber(10).pow(tokenInInfo.decimals))
      .toFixed(0);
  }
  if (amountOut) {
    apiParams.amountOut = new BigNumber(amountOut)
      .times(new BigNumber(10).pow(tokenOutInfo.decimals))
      .toFixed(0);
  }

  const resp = await axios.get(`${config.apiBaseUrl}/api/app/route/best-swap-routes`, {
    params: apiParams,
  });
  const routeData = resp.data?.data;

  if (!routeData?.routes?.length) {
    throw new Error('No swap route found');
  }

  const route = routeData.routes[0];
  return {
    amountIn: divDecimals(route.amountIn, tokenInInfo.decimals).toFixed(),
    amountOut: divDecimals(route.amountOut, tokenOutInfo.decimals).toFixed(),
    splits: route.splits,
    distributions: route.distributions.map((d: any) => ({
      percent: d.percent,
      amountIn: divDecimals(d.amountIn, tokenInInfo.decimals).toFixed(),
      amountOut: divDecimals(d.amountOut, tokenOutInfo.decimals).toFixed(),
      tokens: d.tokens,
      feeRates: d.feeRates,
    })),
  };
}

// ---- getPair ----

export async function getPair(
  config: NetworkConfig,
  params: GetPairParams,
): Promise<TradePairItem> {
  const feeRate = params.feeRate ?? '0.3';
  const feeDecimal = new BigNumber(feeRate).div(100).toFixed();

  const resp = await axios.get(`${config.apiBaseUrl}/api/app/trade-pairs`, {
    params: {
      ChainId: config.chainId,
      Token0Symbol: params.token0,
      Token1Symbol: params.token1,
      FeeRate: feeDecimal,
    },
  });

  const items: TradePairItem[] = resp.data?.data?.items || resp.data?.items || [];
  if (!items.length) {
    throw new Error(`No trade pair found for ${params.token0}/${params.token1} @ ${feeRate}%`);
  }
  return items[0];
}

// ---- getTokenBalance ----

export async function getTokenBalance(
  config: NetworkConfig,
  params: GetBalanceParams,
): Promise<BalanceResult> {
  const tokenInfo = await getTokenInfo(config.rpcUrl, config.tokenContract, params.symbol);
  const rawBalance = await getBalance(config.rpcUrl, config.tokenContract, params.symbol, params.address);

  return {
    symbol: params.symbol,
    owner: params.address,
    balance: divDecimals(rawBalance, tokenInfo.decimals).toFixed(),
  };
}

// ---- getTokenAllowance ----

export async function getTokenAllowance(
  config: NetworkConfig,
  params: GetAllowanceParams,
): Promise<AllowanceResult> {
  const tokenInfo = await getTokenInfo(config.rpcUrl, config.tokenContract, params.symbol);
  const rawAllowance = await getAllowance(
    config.rpcUrl,
    config.tokenContract,
    params.symbol,
    params.owner,
    params.spender,
  );

  return {
    symbol: params.symbol,
    owner: params.owner,
    spender: params.spender,
    allowance: divDecimals(rawAllowance, tokenInfo.decimals).toFixed(),
  };
}

// ---- getLiquidityPositions ----

export async function getLiquidityPositions(
  config: NetworkConfig,
  params: LiquidityQueryParams,
): Promise<LiquidityResult> {
  // 1. Get all user liquidity positions from API (includes USD values)
  const apiResp = await axios.get(`${config.apiBaseUrl}/api/app/liquidity/user-liquidity`, {
    params: {
      chainId: config.chainId,
      address: params.address,
      skipCount: 0,
      maxResultCount: 100,
    },
  });

  let items: any[] = apiResp.data?.data?.items || apiResp.data?.items || [];

  // 2. Filter by token symbols if specified
  if (params.token0) {
    items = items.filter(
      (item: any) =>
        item.tradePair?.token0?.symbol === params.token0 ||
        item.tradePair?.token1?.symbol === params.token0,
    );
  }
  if (params.token1) {
    items = items.filter(
      (item: any) =>
        item.tradePair?.token0?.symbol === params.token1 ||
        item.tradePair?.token1?.symbol === params.token1,
    );
  }

  // 3. For each position, also query on-chain LP balance from factory contract
  const positions: LiquidityPosition[] = await Promise.all(
    items.map(async (item: any) => {
      const pair = item.tradePair;
      const t0 = pair?.token0?.symbol || '';
      const t1 = pair?.token1?.symbol || '';
      const feeRatePercent = new BigNumber(pair?.feeRate || 0).times(100).toFixed();
      const factoryAddress = config.factory[feeRatePercent];

      let onChainLpBalance: string | number = '0';
      if (factoryAddress) {
        try {
          const lpSymbol = `ALP ${[t0, t1].sort().join('-')}`;
          const balResult = await callViewMethod(config.rpcUrl, factoryAddress, 'GetBalance', {
            symbol: lpSymbol,
            owner: params.address,
          });
          onChainLpBalance = balResult?.amount ?? '0';
        } catch {
          // factory might not have GetBalance - fallback to API value
        }
      }

      // Get pair price for context
      let pairPrice: number | null = null;
      try {
        const pairResp = await axios.get(`${config.apiBaseUrl}/api/app/trade-pairs`, {
          params: {
            ChainId: config.chainId,
            Token0Symbol: t0,
            Token1Symbol: t1,
            FeeRate: pair?.feeRate,
          },
        });
        const pairItems = pairResp.data?.data?.items || pairResp.data?.items || [];
        if (pairItems.length > 0) {
          pairPrice = pairItems[0].price;
        }
      } catch {
        // ignore
      }

      return {
        pairId: pair?.id,
        token0: { symbol: t0, decimals: pair?.token0?.decimals },
        token1: { symbol: t1, decimals: pair?.token1?.decimals },
        feeRate: feeRatePercent + '%',
        lpTokenAmount: item.lpTokenAmount || '0',
        lpTokenAmountOnChain: onChainLpBalance,
        token0Amount: item.token0Amount || '0',
        token1Amount: item.token1Amount || '0',
        assetUSD: item.assetUSD ?? null,
        pairPrice: pairPrice,
      };
    }),
  );

  // 4. Also fetch portfolio-level position data (richer: fees, APR, IL)
  let portfolioPositions: LiquidityPortfolioItem[] = [];
  try {
    const posResp = await axios.get(`${config.apiBaseUrl}/api/app/liquidity/user-positions`, {
      params: {
        chainId: config.chainId,
        address: params.address,
        skipCount: 0,
        maxResultCount: 100,
      },
    });
    portfolioPositions = (posResp.data?.data?.items || posResp.data?.items || []).map((p: any) => ({
      pairId: p.tradePairInfo?.id,
      pair: `${p.tradePairInfo?.token0?.symbol}/${p.tradePairInfo?.token1?.symbol}`,
      feeRate: new BigNumber(p.tradePairInfo?.feeRate || 0).times(100).toFixed() + '%',
      lpTokenAmount: p.lpTokenAmount,
      lpTokenPercent: p.lpTokenPercent,
      positionValueUSD: p.position?.valueInUsd,
      token0Amount: p.position?.token0Amount,
      token0ValueUSD: p.position?.token0AmountInUsd,
      token1Amount: p.position?.token1Amount,
      token1ValueUSD: p.position?.token1AmountInUsd,
      feeEarnedUSD: p.fee?.valueInUsd,
      impermanentLossUSD: p.impermanentLossInUSD,
      estimatedAPR: p.estimatedAPR,
      dynamicAPR: p.dynamicAPR,
    }));
  } catch {
    // portfolio API optional
  }

  return {
    address: params.address,
    totalPositions: positions.length,
    positions,
    portfolioDetail: portfolioPositions.length > 0 ? portfolioPositions : undefined,
  };
}
