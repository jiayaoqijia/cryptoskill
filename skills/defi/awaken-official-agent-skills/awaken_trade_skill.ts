#!/usr/bin/env bun
// ============================================================
// Awaken Trade Skill - CLI Adapter (thin shell)
// ============================================================
// Commands: swap, add-liquidity, remove-liquidity, approve
// Requires: AELF_PRIVATE_KEY (EOA) or PORTKEY_PRIVATE_KEY + CA env vars
// Core logic lives in src/core/trade.ts

import { Command } from 'commander';
import packageJson from './package.json';
import { createSignerFromEnv } from '@portkey/aelf-signer';
import { getNetworkConfig, DEFAULT_SLIPPAGE } from './lib/config';
import { outputSuccess, outputError } from './cli-helpers';
import { executeSwap, addLiquidity, removeLiquidity, approveTokenSpending } from './src/core/trade';

const program = new Command();

program
  .name('awaken-trade')
  .description('Awaken DEX trading tool (requires AELF_PRIVATE_KEY or Portkey CA env vars)')
  .version(packageJson.version)
  .option('--network <network>', 'Network: mainnet or testnet', process.env.AWAKEN_NETWORK || 'mainnet');

// ---- swap ----
program
  .command('swap')
  .description('Execute a token swap')
  .requiredOption('--symbol-in <symbol>', 'Input token symbol (e.g. ELF)')
  .requiredOption('--symbol-out <symbol>', 'Output token symbol (e.g. USDT)')
  .requiredOption('--amount-in <amount>', 'Amount of input token (human-readable)')
  .option('--slippage <slippage>', 'Slippage tolerance (e.g. 0.005 = 0.5%)', DEFAULT_SLIPPAGE)
  .action(async (opts) => {
    try {
      const config = getNetworkConfig(program.opts().network);
      const signer = createSignerFromEnv();
      const result = await executeSwap(config, signer, {
        symbolIn: opts.symbolIn,
        symbolOut: opts.symbolOut,
        amountIn: opts.amountIn,
        slippage: opts.slippage,
      });
      outputSuccess(result);
    } catch (err: any) {
      outputError(err.message || 'Swap failed');
    }
  });

// ---- add-liquidity ----
program
  .command('add-liquidity')
  .description('Add liquidity to a trading pair')
  .requiredOption('--token-a <symbol>', 'Token A symbol')
  .requiredOption('--token-b <symbol>', 'Token B symbol')
  .requiredOption('--amount-a <amount>', 'Amount of token A (human-readable)')
  .requiredOption('--amount-b <amount>', 'Amount of token B (human-readable)')
  .option('--fee-rate <rate>', 'Fee rate tier (e.g. 0.3)', '0.3')
  .option('--slippage <slippage>', 'Slippage tolerance', DEFAULT_SLIPPAGE)
  .action(async (opts) => {
    try {
      const config = getNetworkConfig(program.opts().network);
      const signer = createSignerFromEnv();
      const result = await addLiquidity(config, signer, {
        tokenA: opts.tokenA,
        tokenB: opts.tokenB,
        amountA: opts.amountA,
        amountB: opts.amountB,
        feeRate: opts.feeRate,
        slippage: opts.slippage,
      });
      outputSuccess(result);
    } catch (err: any) {
      outputError(err.message || 'Add liquidity failed');
    }
  });

// ---- remove-liquidity ----
program
  .command('remove-liquidity')
  .description('Remove liquidity from a trading pair')
  .requiredOption('--token-a <symbol>', 'Token A symbol')
  .requiredOption('--token-b <symbol>', 'Token B symbol')
  .requiredOption('--lp-amount <amount>', 'LP token amount to remove (human-readable)')
  .option('--fee-rate <rate>', 'Fee rate tier', '0.3')
  .option('--slippage <slippage>', 'Slippage tolerance', DEFAULT_SLIPPAGE)
  .action(async (opts) => {
    try {
      const config = getNetworkConfig(program.opts().network);
      const signer = createSignerFromEnv();
      const result = await removeLiquidity(config, signer, {
        tokenA: opts.tokenA,
        tokenB: opts.tokenB,
        lpAmount: opts.lpAmount,
        feeRate: opts.feeRate,
        slippage: opts.slippage,
      });
      outputSuccess(result);
    } catch (err: any) {
      outputError(err.message || 'Remove liquidity failed');
    }
  });

// ---- approve ----
program
  .command('approve')
  .description('Approve token spending for a contract')
  .requiredOption('--symbol <symbol>', 'Token symbol')
  .requiredOption('--spender <address>', 'Spender contract address')
  .requiredOption('--amount <amount>', 'Amount to approve (human-readable)')
  .action(async (opts) => {
    try {
      const config = getNetworkConfig(program.opts().network);
      const signer = createSignerFromEnv();
      const result = await approveTokenSpending(config, signer, {
        symbol: opts.symbol,
        spender: opts.spender,
        amount: opts.amount,
      });
      outputSuccess(result);
    } catch (err: any) {
      outputError(err.message || 'Approve failed');
    }
  });

program.parse();
