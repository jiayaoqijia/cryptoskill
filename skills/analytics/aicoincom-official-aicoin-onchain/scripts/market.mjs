#!/usr/bin/env node
// OKX DEX Market — price, kline, index, signal
import { okxGet, okxPost, resolveChain, resolveChains, cli } from '../lib/okx-api.mjs';

cli({
  // Single token price
  price: ({ address, chain }) => {
    if (!address) return Promise.resolve({ error: 'address is required' });
    const body = [{ chainIndex: resolveChain(chain), tokenContractAddress: address }];
    return okxPost('/api/v6/dex/market/price', body);
  },

  // Batch price query
  prices: ({ tokens, chain }) => {
    if (!tokens) return Promise.resolve({ error: 'tokens is required (comma-separated chain:address pairs)' });
    const defaultChain = resolveChain(chain || 'ethereum');
    const items = tokens.split(',').map(pair => {
      const p = pair.trim();
      if (p.includes(':')) {
        const [c, addr] = p.split(':');
        return { chainIndex: resolveChain(c), tokenContractAddress: addr };
      }
      return { chainIndex: defaultChain, tokenContractAddress: p };
    });
    return okxPost('/api/v6/dex/market/price', items);
  },

  // K-line / candlestick data
  kline: ({ address, chain, bar, limit }) => {
    if (!address) return Promise.resolve({ error: 'address is required' });
    return okxGet('/api/v6/dex/market/candles', {
      chainIndex: resolveChain(chain),
      tokenContractAddress: address,
      bar: bar || '1H',
      limit: String(limit || 100),
    });
  },

  // Index price (aggregated from multiple sources)
  index: ({ address, chain }) => {
    if (!address) return Promise.resolve({ error: 'address is required' });
    const body = [{ chainIndex: resolveChain(chain), tokenContractAddress: address }];
    return okxPost('/api/v6/dex/index/current-price', body);
  },

  // Smart money / whale / KOL signal list
  signal_list: ({ chain, wallet_type, token_address, min_amount_usd }) => {
    if (!chain) return Promise.resolve({ error: 'chain is required' });
    return okxPost('/api/v6/dex/market/signal/list', {
      chainIndex: resolveChain(chain),
      walletType: wallet_type || '',
      tokenAddress: token_address || '',
      minAmountUsd: min_amount_usd || '',
    });
  },

  // Signal supported chains
  signal_chains: () => okxGet('/api/v6/dex/market/signal/supported/chain', {}),
});
