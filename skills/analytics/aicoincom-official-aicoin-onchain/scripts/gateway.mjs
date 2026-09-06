#!/usr/bin/env node
// OKX Onchain Gateway — gas, simulate, broadcast, orders
import { okxGet, okxPost, resolveChain, cli } from '../lib/okx-api.mjs';

cli({
  // Supported chains
  chains: () => okxGet('/api/v6/dex/pre-transaction/supported/chain', {}),

  // Current gas prices
  gas: ({ chain }) => {
    if (!chain) return Promise.resolve({ error: 'chain is required' });
    return okxGet('/api/v6/dex/pre-transaction/gas-price', {
      chainIndex: resolveChain(chain),
    });
  },

  // Estimate gas limit
  gas_limit: ({ from, to, amount, data, chain }) => {
    if (!from || !to || !chain) return Promise.resolve({ error: 'from, to, chain are required' });
    const body = {
      chainIndex: resolveChain(chain),
      fromAddress: from,
      toAddress: to,
      txAmount: amount || '0',
    };
    if (data) body.extJson = JSON.stringify({ inputData: data });
    return okxPost('/api/v6/dex/pre-transaction/gas-limit', body);
  },

  // Simulate transaction (dry-run)
  simulate: ({ from, to, amount, data, chain }) => {
    if (!from || !to || !data || !chain)
      return Promise.resolve({ error: 'from, to, data, chain are required' });
    return okxPost('/api/v6/dex/pre-transaction/simulate', {
      chainIndex: resolveChain(chain),
      fromAddress: from,
      toAddress: to,
      txAmount: amount || '0',
      extJson: JSON.stringify({ inputData: data }),
    });
  },

  // Broadcast signed transaction
  broadcast: ({ signed_tx, address, chain }) => {
    if (!signed_tx || !address || !chain)
      return Promise.resolve({ error: 'signed_tx, address, chain are required' });
    return okxPost('/api/v6/dex/pre-transaction/broadcast-transaction', {
      signedTx: signed_tx,
      chainIndex: resolveChain(chain),
      address,
    });
  },

  // Track broadcast order status
  orders: ({ address, chain, order_id }) => {
    if (!address || !chain) return Promise.resolve({ error: 'address and chain are required' });
    const params = {
      address,
      chainIndex: resolveChain(chain),
    };
    if (order_id) params.orderId = order_id;
    return okxGet('/api/v6/dex/post-transaction/orders', params);
  },
});
