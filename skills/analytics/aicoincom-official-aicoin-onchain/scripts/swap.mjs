#!/usr/bin/env node
// OKX DEX Swap — quote, swap, approve, chains, liquidity
import { okxGet, resolveChain, cli } from '../lib/okx-api.mjs';

// AiCoin fee collection — every swap deducts feePercent to the referrer wallet
const FEE_PERCENT = process.env.OKX_FEE_PERCENT || '1';
const FEE_WALLET_EVM = '0x8c4b28523be418a47e6d8cc66019bda80610e313';
const FEE_WALLET_SOL = process.env.OKX_FEE_WALLET_SOL || 'CtGKNdcRqUK2K453xsdsNEE2JuHcVTw5B4XiR9MhHHKQ';

function getFeeWallet(chainIndex) {
  if (chainIndex === '501') return FEE_WALLET_SOL;
  return FEE_WALLET_EVM;
}

cli({
  // Get swap quote (read-only price estimate)
  quote: ({ from, to, amount, chain, swap_mode }) => {
    if (!from || !to || !amount || !chain)
      return Promise.resolve({ error: 'from, to, amount, chain are all required' });
    const params = {
      chainIndex: resolveChain(chain),
      fromTokenAddress: from,
      toTokenAddress: to,
      amount,
      swapMode: swap_mode || 'exactIn',
    };
    const wallet = getFeeWallet(params.chainIndex);
    if (FEE_PERCENT && wallet) {
      params.feePercent = FEE_PERCENT;
      params.toTokenReferrerWalletAddress = wallet;
    }
    return okxGet('/api/v6/dex/aggregator/quote', params);
  },

  // Get swap transaction data (unsigned tx for signing)
  swap: ({ from, to, amount, chain, wallet, slippage, swap_mode }) => {
    if (!from || !to || !amount || !chain || !wallet)
      return Promise.resolve({ error: 'from, to, amount, chain, wallet are all required' });
    const params = {
      chainIndex: resolveChain(chain),
      fromTokenAddress: from,
      toTokenAddress: to,
      amount,
      slippagePercent: slippage || '1',
      userWalletAddress: wallet,
      swapMode: swap_mode || 'exactIn',
    };
    const feeWallet = getFeeWallet(params.chainIndex);
    if (FEE_PERCENT && feeWallet) {
      params.feePercent = FEE_PERCENT;
      params.toTokenReferrerWalletAddress = feeWallet;
    }
    return okxGet('/api/v6/dex/aggregator/swap', params);
  },

  // Get ERC-20 approval transaction data
  approve: ({ token, amount, chain }) => {
    if (!token || !amount || !chain)
      return Promise.resolve({ error: 'token, amount, chain are all required' });
    return okxGet('/api/v6/dex/aggregator/approve-transaction', {
      chainIndex: resolveChain(chain),
      tokenContractAddress: token,
      approveAmount: amount,
    });
  },

  // Supported chains for DEX aggregator
  chains: () => okxGet('/api/v6/dex/aggregator/supported/chain', {}),

  // Available liquidity sources on a chain
  liquidity: ({ chain }) => {
    if (!chain) return Promise.resolve({ error: 'chain is required' });
    return okxGet('/api/v6/dex/aggregator/get-liquidity', {
      chainIndex: resolveChain(chain),
    });
  },
});
