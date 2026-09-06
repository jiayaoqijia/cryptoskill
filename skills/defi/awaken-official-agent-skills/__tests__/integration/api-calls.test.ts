// ============================================================
// Integration Test: Awaken HTTP API calls (mainnet, read-only)
// ============================================================

import { describe, test, expect } from 'bun:test';
import axios from 'axios';
import { getNetworkConfig } from '../../lib/config';
import BigNumber from 'bignumber.js';

const config = getNetworkConfig('mainnet');

describe('GET /api/app/trade-pairs (mainnet)', () => {
  test('fetches ELF/USDT pair', async () => {
    const resp = await axios.get(`${config.apiBaseUrl}/api/app/trade-pairs`, {
      params: {
        ChainId: config.chainId,
        Token0Symbol: 'ELF',
        Token1Symbol: 'USDT',
        FeeRate: 0.003, // 0.3%
      },
    });

    const items = resp.data?.data?.items || resp.data?.items || [];
    expect(items.length).toBeGreaterThanOrEqual(1);

    const pair = items[0];
    expect(pair.id).toBeDefined();
    expect(pair.token0).toBeDefined();
    expect(pair.token1).toBeDefined();
    expect(pair.feeRate).toBeDefined();
  }, 15000);
});

describe('GET /api/app/route/best-swap-routes (mainnet)', () => {
  test('gets swap route for 1 ELF -> USDT', async () => {
    // First get ELF decimals
    const amountIn = new BigNumber(1).times(1e8).toFixed(0); // 1 ELF = 1e8

    const resp = await axios.get(`${config.apiBaseUrl}/api/app/route/best-swap-routes`, {
      params: {
        ChainId: config.chainId,
        symbolIn: 'ELF',
        symbolOut: 'USDT',
        routeType: 0,
        amountIn,
      },
    });

    const data = resp.data?.data;
    expect(data).toBeDefined();
    expect(data.routes).toBeDefined();
    expect(data.routes.length).toBeGreaterThanOrEqual(1);

    const route = data.routes[0];
    expect(route.amountIn).toBeDefined();
    expect(route.amountOut).toBeDefined();
    expect(new BigNumber(route.amountOut).gt(0)).toBe(true);
    expect(route.distributions).toBeDefined();
    expect(route.distributions.length).toBeGreaterThanOrEqual(1);
  }, 15000);
});

describe('GET /api/app/liquidity/user-liquidity (mainnet)', () => {
  const testAddress = 'vc6sUvrJUutTLR6JsW7Am3wDpSnWyg5UtbuVsStKRVTeLmS9b';

  test('returns user liquidity positions with structure', async () => {
    const resp = await axios.get(`${config.apiBaseUrl}/api/app/liquidity/user-liquidity`, {
      params: {
        chainId: config.chainId,
        address: testAddress,
        skipCount: 0,
        maxResultCount: 100,
      },
    });

    const data = resp.data?.data || resp.data;
    expect(data).toBeDefined();
    expect(data.totalCount).toBeDefined();
    expect(data.items).toBeInstanceOf(Array);

    if (data.items.length > 0) {
      const item = data.items[0];
      expect(item.tradePair).toBeDefined();
      expect(item.tradePair.token0).toBeDefined();
      expect(item.tradePair.token1).toBeDefined();
      expect(item.lpTokenAmount).toBeDefined();
      expect(item.assetUSD).toBeDefined();
      expect(item.token0Amount).toBeDefined();
      expect(item.token1Amount).toBeDefined();
    }
  }, 15000);

  test('user-positions API returns portfolio detail with USD values', async () => {
    const resp = await axios.get(`${config.apiBaseUrl}/api/app/liquidity/user-positions`, {
      params: {
        chainId: config.chainId,
        address: testAddress,
        skipCount: 0,
        maxResultCount: 100,
      },
    });

    const data = resp.data?.data || resp.data;
    expect(data).toBeDefined();
    expect(data.totalCount).toBeDefined();
    expect(data.items).toBeInstanceOf(Array);

    if (data.items.length > 0) {
      const item = data.items[0];
      expect(item.tradePairInfo).toBeDefined();
      expect(item.lpTokenAmount).toBeDefined();
      expect(item.position).toBeDefined();
      expect(item.position.valueInUsd).toBeDefined();
      expect(item.fee).toBeDefined();
    }
  }, 15000);
});
