#!/usr/bin/env node
// Freqtrade Dev Tools CLI
import { ftGet, ftPost, ftDelete, ftCli } from '../lib/freqtrade-api.mjs';

ftCli({
  backtest_start: (p) => ftPost('backtest', p),
  backtest_status: () => ftGet('backtest'),
  backtest_abort: () => ftDelete('backtest'),
  backtest_history: () => ftGet('backtest/history'),
  backtest_result: ({ id }) => ftGet(`backtest/history/result`, { id }),
  candles_live: ({ pair, timeframe, limit }) => ftGet('pair_candles', { pair, timeframe, limit }),
  candles_analyzed: ({ pair, timeframe, strategy }) => ftGet('pair_history', { pair, timeframe, strategy }),
  candles_available: () => ftGet('available_pairs'),
  whitelist: () => ftGet('whitelist'),
  blacklist: () => ftGet('blacklist'),
  blacklist_add: ({ add }) => ftPost('blacklist', { blacklist: add }),
  locks: () => ftGet('locks'),
  strategy_list: () => ftGet('strategies'),
  strategy_get: ({ name }) => ftGet(`strategy/${name}`),
});
