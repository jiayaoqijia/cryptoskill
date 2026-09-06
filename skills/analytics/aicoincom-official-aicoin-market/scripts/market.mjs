#!/usr/bin/env node

// This path was removed during the v3 migration, but CoinClaw workspaces may
// retain an older copy on persistent volumes. Keep a fail-closed tombstone in
// the distribution so image/workspace syncs overwrite that unsafe copy.
console.log(JSON.stringify({
  ok: false,
  data: null,
  error: {
    code: 'legacy_entrypoint_retired',
    message: '旧版 market.mjs 已停用，不能再用于行情或 K 线。请改用 node scripts/aicoin.mjs market/klines \'{"coin_key":"bitcoin","market":"binance","interval":"1h","limit":3}\'；先检查 ok，再使用返回的时间戳。',
  },
  meta: {
    migration_required: true,
  },
}, null, 2));

process.exitCode = 2;
