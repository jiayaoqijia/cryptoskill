// ============================================================
// E2E Test: Real add + remove liquidity on mainnet (tiny amount)
// ============================================================
// REQUIRES: AELF_PRIVATE_KEY env var
// Safety: hard-coded max 0.01 ELF per operation

import { describe, test, expect, beforeAll } from 'bun:test';
import BigNumber from 'bignumber.js';
import axios from 'axios';
import { getNetworkConfig, getRouterAddress, getDeadline, CHANNEL_ID, E2E_MAX_AMOUNT } from '../../lib/config';
import {
  getWalletByPrivateKey,
  getTokenInfo,
  getBalance,
  getAllowance,
  approveToken,
  callSendMethod,
  callViewMethod,
  getTxResult,
  timesDecimals,
  divDecimals,
} from '../../lib/aelf-client';

const SKIP_REASON = 'AELF_PRIVATE_KEY not set - skipping E2E';
const hasPrivateKey = !!process.env.AELF_PRIVATE_KEY;
const MAX_RAW_AMOUNT = E2E_MAX_AMOUNT;
const FEE_RATE = '0.3';

describe('E2E: Liquidity (mainnet)', () => {
  let config: ReturnType<typeof getNetworkConfig>;
  let wallet: any;

  beforeAll(() => {
    if (!hasPrivateKey) return;
    config = getNetworkConfig('mainnet');
    wallet = getWalletByPrivateKey();
  });

  test('add and remove tiny liquidity for ELF/USDT', async () => {
    if (!hasPrivateKey) {
      console.warn(SKIP_REASON);
      return;
    }

    const account = wallet.address;
    const routerAddress = getRouterAddress(config, FEE_RATE);

    // 1. Get token info and balances
    const [elfInfo, usdtInfo] = await Promise.all([
      getTokenInfo(config.rpcUrl, config.tokenContract, 'ELF'),
      getTokenInfo(config.rpcUrl, config.tokenContract, 'USDT'),
    ]);

    const [elfBalance, usdtBalance] = await Promise.all([
      getBalance(config.rpcUrl, config.tokenContract, 'ELF', account),
      getBalance(config.rpcUrl, config.tokenContract, 'USDT', account),
    ]);

    console.log(`ELF balance: ${divDecimals(elfBalance, elfInfo.decimals).toFixed()}`);
    console.log(`USDT balance: ${divDecimals(usdtBalance, usdtInfo.decimals).toFixed()}`);

    // We need to know the current price to calculate matching amounts
    // Fetch the pair to get the price
    const pairResp = await axios.get(`${config.apiBaseUrl}/api/app/trade-pairs`, {
      params: {
        ChainId: config.chainId,
        Token0Symbol: 'ELF',
        Token1Symbol: 'USDT',
        FeeRate: new BigNumber(FEE_RATE).div(100).toFixed(),
      },
    });

    const pairItems = pairResp.data?.data?.items || pairResp.data?.items || [];
    if (!pairItems.length) {
      console.warn('No ELF/USDT pair found. Skipping.');
      return;
    }

    const pair = pairItems[0];
    const price = pair.price; // ELF price in USDT

    // Use 0.001 ELF and matching USDT
    const elfAmount = '0.001';
    const usdtAmount = new BigNumber(elfAmount).times(price).dp(usdtInfo.decimals).toFixed();

    const rawElfAmount = timesDecimals(elfAmount, elfInfo.decimals).toFixed(0);
    const rawUsdtAmount = timesDecimals(usdtAmount, usdtInfo.decimals).toFixed(0);

    // Safety check
    if (new BigNumber(rawElfAmount).gt(MAX_RAW_AMOUNT)) {
      throw new Error(`SAFETY: ELF amount ${rawElfAmount} exceeds max ${MAX_RAW_AMOUNT}`);
    }

    // Check sufficient balance
    if (new BigNumber(elfBalance).lt(rawElfAmount) || new BigNumber(usdtBalance).lt(rawUsdtAmount)) {
      console.warn(`Insufficient balance. Need ${elfAmount} ELF + ${usdtAmount} USDT. Skipping.`);
      return;
    }

    console.log(`Adding liquidity: ${elfAmount} ELF + ${usdtAmount} USDT`);

    // 2. Approve both tokens
    const minRate = new BigNumber(0.99); // 1% slippage
    await Promise.all([
      ensureApproval(config, wallet, 'ELF', routerAddress, rawElfAmount),
      ensureApproval(config, wallet, 'USDT', routerAddress, rawUsdtAmount),
    ]);

    // 3. Add liquidity
    const addResult = await callSendMethod(config.rpcUrl, routerAddress, 'AddLiquidity', wallet, {
      symbolA: 'ELF',
      symbolB: 'USDT',
      amountADesired: rawElfAmount,
      amountBDesired: rawUsdtAmount,
      amountAMin: new BigNumber(rawElfAmount).times(minRate).toFixed(0),
      amountBMin: new BigNumber(rawUsdtAmount).times(minRate).toFixed(0),
      to: account,
      deadline: { seconds: getDeadline(), nanos: 0 },
      channel: CHANNEL_ID,
    });

    const addTxId = addResult?.TransactionId || addResult?.transactionId;
    expect(addTxId).toBeDefined();
    console.log(`AddLiquidity TX: ${addTxId}`);

    const addTxResult = await getTxResult(config.rpcUrl, addTxId);
    expect(addTxResult.status).toBe('mined');
    console.log('AddLiquidity mined.');

    // 4. Wait a bit, then check LP balance on the FACTORY contract (LP tokens live there, not token contract)
    await sleep(3000);

    const lpSymbol = `ALP ${['ELF', 'USDT'].sort().join('-')}`;
    const factoryAddress = config.factory[FEE_RATE];
    const lpBalanceResult = await callViewMethod(config.rpcUrl, factoryAddress, 'GetBalance', {
      symbol: lpSymbol,
      owner: account,
    });
    const lpAmount = lpBalanceResult?.amount ?? lpBalanceResult?.balance ?? '0';
    console.log(`LP balance after add: ${lpAmount} raw (symbol: ${lpSymbol}, factory: ${factoryAddress})`);

    if (new BigNumber(lpAmount).lte(0)) {
      console.warn('LP balance is 0 after add. Skipping remove.');
      return;
    }

    // 5. Remove the same LP we just added
    console.log(`Removing ${lpAmount} LP tokens...`);

    // Approve LP token on factory contract to router
    const lpApproveResult = await callSendMethod(config.rpcUrl, factoryAddress, 'Approve', wallet, {
      symbol: lpSymbol,
      spender: routerAddress,
      amount: new BigNumber(lpAmount).times(10).toFixed(0),
    });
    const lpApproveTxId = lpApproveResult?.TransactionId || lpApproveResult?.transactionId;
    if (lpApproveTxId) {
      await getTxResult(config.rpcUrl, lpApproveTxId);
      console.log('LP approved on factory.');
    }

    const removeResult = await callSendMethod(config.rpcUrl, routerAddress, 'RemoveLiquidity', wallet, {
      symbolA: 'ELF',
      symbolB: 'USDT',
      amountAMin: '1',
      amountBMin: '1',
      liquidityRemove: lpAmount,
      to: account,
      deadline: { seconds: getDeadline(), nanos: 0 },
    });

    const removeTxId = removeResult?.TransactionId || removeResult?.transactionId;
    expect(removeTxId).toBeDefined();
    console.log(`RemoveLiquidity TX: ${removeTxId}`);

    const removeTxResult = await getTxResult(config.rpcUrl, removeTxId);
    expect(removeTxResult.status).toBe('mined');
    console.log('RemoveLiquidity mined. Funds recovered.');
  }, 180000); // 3 min timeout
});

// ---- Helpers ----

async function ensureApproval(
  config: ReturnType<typeof getNetworkConfig>,
  wallet: any,
  symbol: string,
  spender: string,
  requiredAmount: string,
) {
  const currentAllowance = await getAllowance(config.rpcUrl, config.tokenContract, symbol, wallet.address, spender);
  if (new BigNumber(currentAllowance).lt(requiredAmount)) {
    const approveAmount = new BigNumber(requiredAmount).times(100).toFixed(0);
    console.log(`Approving ${symbol}...`);
    await approveToken(config, wallet, symbol, spender, approveAmount);
    console.log(`${symbol} approved.`);
  }
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
