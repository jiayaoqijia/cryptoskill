#!/usr/bin/env bun
// ============================================================
// Awaken Query Skill - CLI Adapter (thin shell)
// ============================================================
// Commands: quote, pair, balance, allowance, liquidity
// Core logic lives in src/core/query.ts

import { Command } from 'commander';
import packageJson from './package.json';
import { getNetworkConfig } from './lib/config';
import { outputSuccess, outputError } from './cli-helpers';
import { getQuote, getPair, getTokenBalance, getTokenAllowance, getLiquidityPositions } from './src/core/query';

const program = new Command();

program
  .name('awaken-query')
  .description('Awaken DEX read-only query tool')
  .version(packageJson.version)
  .option('--network <network>', 'Network: mainnet or testnet', process.env.AWAKEN_NETWORK || 'mainnet');

// ---- quote ----
program
  .command('quote')
  .description('Get best swap route and price quote')
  .requiredOption('--symbol-in <symbol>', 'Input token symbol (e.g. ELF)')
  .requiredOption('--symbol-out <symbol>', 'Output token symbol (e.g. USDT)')
  .option('--amount-in <amount>', 'Amount of input token (human-readable)')
  .option('--amount-out <amount>', 'Amount of output token (human-readable)')
  .action(async (opts) => {
    try {
      const config = getNetworkConfig(program.opts().network);
      const result = await getQuote(config, {
        symbolIn: opts.symbolIn,
        symbolOut: opts.symbolOut,
        amountIn: opts.amountIn,
        amountOut: opts.amountOut,
      });
      outputSuccess(result);
    } catch (err: any) {
      outputError(err.message || 'Quote failed');
    }
  });

// ---- pair ----
program
  .command('pair')
  .description('Get trade pair information')
  .requiredOption('--token0 <symbol>', 'Token 0 symbol')
  .requiredOption('--token1 <symbol>', 'Token 1 symbol')
  .option('--fee-rate <rate>', 'Fee rate (e.g. 0.3)', '0.3')
  .action(async (opts) => {
    try {
      const config = getNetworkConfig(program.opts().network);
      const result = await getPair(config, {
        token0: opts.token0,
        token1: opts.token1,
        feeRate: opts.feeRate,
      });
      outputSuccess(result);
    } catch (err: any) {
      outputError(err.message || 'Pair query failed');
    }
  });

// ---- balance ----
program
  .command('balance')
  .description('Query token balance for an address')
  .requiredOption('--address <address>', 'Wallet address')
  .requiredOption('--symbol <symbol>', 'Token symbol (e.g. ELF)')
  .action(async (opts) => {
    try {
      const config = getNetworkConfig(program.opts().network);
      const result = await getTokenBalance(config, {
        address: opts.address,
        symbol: opts.symbol,
      });
      outputSuccess(result);
    } catch (err: any) {
      outputError(err.message || 'Balance query failed');
    }
  });

// ---- allowance ----
program
  .command('allowance')
  .description('Query token allowance')
  .requiredOption('--owner <address>', 'Token owner address')
  .requiredOption('--spender <address>', 'Spender contract address')
  .requiredOption('--symbol <symbol>', 'Token symbol')
  .action(async (opts) => {
    try {
      const config = getNetworkConfig(program.opts().network);
      const result = await getTokenAllowance(config, {
        owner: opts.owner,
        spender: opts.spender,
        symbol: opts.symbol,
      });
      outputSuccess(result);
    } catch (err: any) {
      outputError(err.message || 'Allowance query failed');
    }
  });

// ---- liquidity ----
program
  .command('liquidity')
  .description('Query liquidity positions for an address, including USD value')
  .requiredOption('--address <address>', 'Wallet address')
  .option('--token0 <symbol>', 'Filter by token0 symbol (e.g. ELF)')
  .option('--token1 <symbol>', 'Filter by token1 symbol (e.g. USDT)')
  .action(async (opts) => {
    try {
      const config = getNetworkConfig(program.opts().network);
      const result = await getLiquidityPositions(config, {
        address: opts.address,
        token0: opts.token0,
        token1: opts.token1,
      });
      outputSuccess(result);
    } catch (err: any) {
      outputError(err.message || 'Liquidity query failed');
    }
  });

program.parse();
