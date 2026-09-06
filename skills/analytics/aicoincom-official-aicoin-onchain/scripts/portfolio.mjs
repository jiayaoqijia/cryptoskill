#!/usr/bin/env node
// OKX Wallet Portfolio — balance, total value, token balances
import { okxGet, okxPost, resolveChains, resolveChain, cli } from '../lib/okx-api.mjs';

cli({
  // Supported chains
  chains: () => okxGet('/api/v6/dex/balance/supported/chain', {}),

  // Total portfolio value
  total_value: ({ address, chains, asset_type, exclude_risk }) => {
    if (!address || !chains) return Promise.resolve({ error: 'address and chains are required' });
    return okxGet('/api/v6/dex/balance/total-value-by-address', {
      address,
      chains: resolveChains(chains),
      assetType: asset_type || '0',
      excludeRiskToken: exclude_risk || 'true',
    });
  },

  // All token balances
  all_balances: ({ address, chains, exclude_risk }) => {
    if (!address || !chains) return Promise.resolve({ error: 'address and chains are required' });
    return okxGet('/api/v6/dex/balance/all-token-balances-by-address', {
      address,
      chains: resolveChains(chains),
      excludeRiskToken: exclude_risk || '0',
    });
  },

  // Specific token balances (POST)
  token_balances: ({ address, tokens, exclude_risk }) => {
    if (!address || !tokens) return Promise.resolve({ error: 'address and tokens are required (comma-separated chainName:address pairs)' });
    const tokenList = tokens.split(',').map(pair => {
      const [chain, addr] = pair.trim().split(':');
      return { chainIndex: resolveChain(chain), tokenContractAddress: addr || '' };
    });
    const body = { address, tokenContractAddresses: tokenList };
    if (exclude_risk) body.excludeRiskToken = exclude_risk;
    return okxPost('/api/v6/dex/balance/token-balances-by-address', body);
  },
});
