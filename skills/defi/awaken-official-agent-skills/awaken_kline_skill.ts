#!/usr/bin/env bun
// ============================================================
// Awaken K-Line Skill - CLI Adapter (thin shell)
// ============================================================
// Commands: fetch, intervals
// Core logic lives in src/core/kline.ts

import { Command } from 'commander';
import packageJson from './package.json';
import { getNetworkConfig } from './lib/config';
import { outputSuccess, outputError } from './cli-helpers';
import { fetchKline, getKlineIntervals } from './src/core/kline';

const program = new Command();

program
  .name('awaken-kline')
  .description('Awaken DEX K-line (candlestick) data tool')
  .version(packageJson.version)
  .option('--network <network>', 'Network: mainnet or testnet', process.env.AWAKEN_NETWORK || 'mainnet');

// ---- fetch ----
program
  .command('fetch')
  .description('Fetch historical K-line data via SignalR')
  .requiredOption('--pair-id <id>', 'Trade pair ID (UUID from pair query)')
  .option('--interval <interval>', 'Time interval: 1m, 15m, 30m, 1h, 4h, 1D, 1W', '1D')
  .option('--from <date>', 'Start date (ISO string or unix ms)', String(Date.now() - 7 * 24 * 60 * 60 * 1000))
  .option('--to <date>', 'End date (ISO string or unix ms)', String(Date.now()))
  .option('--timeout <ms>', 'Max wait time in ms', '15000')
  .action(async (opts) => {
    try {
      const config = getNetworkConfig(program.opts().network);
      const result = await fetchKline(config, {
        tradePairId: opts.pairId,
        interval: opts.interval,
        from: opts.from,
        to: opts.to,
        timeout: parseInt(opts.timeout, 10),
      });
      outputSuccess(result);
    } catch (err: any) {
      outputError(err.message || 'K-line fetch failed');
    }
  });

// ---- intervals ----
program
  .command('intervals')
  .description('List supported K-line intervals')
  .action(() => {
    outputSuccess(getKlineIntervals());
  });

program.parse();
