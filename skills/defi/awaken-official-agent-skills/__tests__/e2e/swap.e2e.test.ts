// ============================================================
// E2E Test: Real swap on mainnet (tiny amount)
// ============================================================
// REQUIRES: AELF_PRIVATE_KEY env var
// Safety: hard-coded max 0.01 ELF per swap

import { describe, test, expect, beforeAll } from 'bun:test';
import axios from 'axios';
import BigNumber from 'bignumber.js';
import { getNetworkConfig, getRouterAddress, getDeadline, CHANNEL_ID, E2E_MAX_AMOUNT, SWAP_LABS_FEE_RATE } from '../../lib/config';
import {
  getWalletByPrivateKey,
  getTokenInfo,
  getBalance,
  getAllowance,
  approveToken,
  callSendMethod,
  getTxResult,
  timesDecimals,
  divDecimals,
} from '../../lib/aelf-client';

const SKIP_REASON = 'AELF_PRIVATE_KEY not set - skipping E2E';
const hasPrivateKey = !!process.env.AELF_PRIVATE_KEY;

// Safety: max 0.01 ELF (= 1_000_000 in raw 8-decimal)
const MAX_RAW_AMOUNT = E2E_MAX_AMOUNT;
const SWAP_AMOUNT = '0.001'; // 0.001 ELF

describe('E2E: Swap (mainnet)', () => {
  let config: ReturnType<typeof getNetworkConfig>;
  let wallet: any;

  beforeAll(() => {
    if (!hasPrivateKey) return;
    config = getNetworkConfig('mainnet');
    wallet = getWalletByPrivateKey();
  });

  test('swaps 0.001 ELF -> USDT on mainnet', async () => {
    if (!hasPrivateKey) {
      console.warn(SKIP_REASON);
      return;
    }

    const account = wallet.address;
    console.log(`E2E swap account: ${account}`);

    // 1. Get token info
    const [elfInfo, usdtInfo] = await Promise.all([
      getTokenInfo(config.rpcUrl, config.tokenContract, 'ELF'),
      getTokenInfo(config.rpcUrl, config.tokenContract, 'USDT'),
    ]);

    const rawAmountIn = timesDecimals(SWAP_AMOUNT, elfInfo.decimals).toFixed(0);

    // Safety check
    if (new BigNumber(rawAmountIn).gt(MAX_RAW_AMOUNT)) {
      throw new Error(`SAFETY: amountIn ${rawAmountIn} exceeds max ${MAX_RAW_AMOUNT}`);
    }

    // 2. Check balance
    const elfBalance = await getBalance(config.rpcUrl, config.tokenContract, 'ELF', account);
    console.log(`ELF balance: ${divDecimals(elfBalance, elfInfo.decimals).toFixed()}`);

    if (new BigNumber(elfBalance).lt(rawAmountIn)) {
      console.warn(`Insufficient ELF balance (${elfBalance} < ${rawAmountIn}). Skipping swap.`);
      return;
    }

    // 3. Get best route
    const resp = await axios.get(`${config.apiBaseUrl}/api/app/route/best-swap-routes`, {
      params: {
        ChainId: config.chainId,
        symbolIn: 'ELF',
        symbolOut: 'USDT',
        routeType: 0,
        amountIn: rawAmountIn,
      },
    });

    const routeData = resp.data?.data;
    expect(routeData?.routes?.length).toBeGreaterThanOrEqual(1);

    const bestRoute = routeData.routes[0];
    const rawAmountOut = bestRoute.amountOut;
    const slippage = 0.01; // 1% for safety
    const amountOutMin = new BigNumber(rawAmountOut).times(1 - slippage).toFixed(0);

    console.log(`Estimated out: ${divDecimals(rawAmountOut, usdtInfo.decimals).toFixed()} USDT`);

    // 4. Build swap tokens (via SWAP_HOOK contract)
    const deadline = { seconds: getDeadline(), nanos: 0 };
    const swapTokens = bestRoute.distributions.map((dist: any) => ({
      amountIn: dist.amountIn,
      amountOutMin: new BigNumber(dist.amountOut).times(1 - slippage).toFixed(0),
      path: dist.tokens.map((t: any) => t.symbol),
      to: account,
      deadline,
      channel: CHANNEL_ID,
      feeRates: dist.feeRates.map((f: number) => Math.round(f * 10000)),
    }));

    // 5. Use SWAP_HOOK contract (not router)
    const swapHookAddress = config.swapHookContract;

    // 6. Approve to swap hook contract
    const currentAllowance = await getAllowance(config.rpcUrl, config.tokenContract, 'ELF', account, swapHookAddress);
    if (new BigNumber(currentAllowance).lt(rawAmountIn)) {
      console.log('Approving ELF...');
      const approveAmount = new BigNumber(rawAmountIn).times(100).toFixed(0);
      await approveToken(config, wallet, 'ELF', swapHookAddress, approveAmount);
      console.log('Approved.');
    }

    // 7. Execute swap via swap hook contract
    console.log('Executing swap...');
    const result = await callSendMethod(config.rpcUrl, swapHookAddress, 'SwapExactTokensForTokens', wallet, {
      swapTokens,
      labsFeeRate: SWAP_LABS_FEE_RATE,
    });

    const txId = result?.TransactionId || result?.transactionId;
    expect(txId).toBeDefined();
    console.log(`TX: ${txId}`);

    // 8. Wait for result
    const txResult = await getTxResult(config.rpcUrl, txId);
    expect(txResult.status).toBe('mined');
    console.log(`Swap mined: ${config.explorerUrl}/tx/${txId}`);
  }, 120000); // 2 min timeout for on-chain TX
});

function getFeeRateKey(feeRate: number): string {
  const pct = new BigNumber(feeRate).times(100);
  const candidates = ['0.05', '0.1', '0.3', '3', '5'];
  return candidates.find((c) => pct.eq(c)) || '0.3';
}
