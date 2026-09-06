#!/usr/bin/env node
// OKX DEX Token — search, info, trending, price info, hot tokens
import { okxGet, okxPost, resolveChain, resolveChains, cli } from '../lib/okx-api.mjs';

cli({
  // Search tokens by name/symbol/address
  search: ({ query, chains }) => {
    if (!query) return Promise.resolve({ error: 'query is required' });
    const chainIndexes = chains ? resolveChains(chains) : '1,501';
    return okxGet('/api/v6/dex/market/token/search', {
      chains: chainIndexes,
      search: query,
    });
  },

  // Token metadata: name, symbol, decimals, logo (POST, JSON array body)
  info: ({ address, chain }) => {
    if (!address) return Promise.resolve({ error: 'address is required' });
    return okxPost('/api/v6/dex/market/token/basic-info', [
      { chainIndex: resolveChain(chain), tokenContractAddress: address },
    ]);
  },

  // Trending token rankings
  trending: ({ chains, sort_by, time_frame }) => {
    return okxGet('/api/v6/dex/market/token/toplist', {
      chains: chains ? resolveChains(chains) : '1,501',
      sortBy: sort_by || '5',
      timeFrame: time_frame || '4',
    });
  },

  // Token price info: market cap, liquidity, 24h change (POST, JSON array body)
  price_info: ({ address, chain }) => {
    if (!address) return Promise.resolve({ error: 'address is required' });
    return okxPost('/api/v6/dex/market/price-info', [
      { chainIndex: resolveChain(chain), tokenContractAddress: address },
    ]);
  },

  // Hot tokens
  hot_tokens: ({ chains, ranking_type }) => {
    return okxGet('/api/v6/dex/market/token/hot-token', {
      rankingType: ranking_type || '4',
      chainIndex: chains ? resolveChains(chains) : '',
    });
  },

  // Token holders distribution
  holders: ({ address, chain }) => {
    if (!address) return Promise.resolve({ error: 'address is required' });
    return okxGet('/api/v6/dex/market/token/holder', {
      chainIndex: resolveChain(chain),
      tokenContractAddress: address,
    });
  },

  // Top liquidity pools for a token
  liquidity: ({ address, chain }) => {
    if (!address) return Promise.resolve({ error: 'address is required' });
    return okxGet('/api/v6/dex/market/token/top-liquidity', {
      chainIndex: resolveChain(chain),
      tokenContractAddress: address,
    });
  },

  // Advanced token info: risk, creator, dev stats
  advanced_info: ({ address, chain }) => {
    if (!address) return Promise.resolve({ error: 'address is required' });
    return okxGet('/api/v6/dex/market/token/advanced-info', {
      chainIndex: resolveChain(chain),
      tokenContractAddress: address,
    });
  },
});
