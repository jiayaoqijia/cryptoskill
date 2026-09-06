import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const legacyEntrypoint = fileURLToPath(new URL('./market.mjs', import.meta.url));

test('the retired market.mjs entrypoint fails closed with a v3 migration hint', () => {
  const result = spawnSync(process.execPath, [
    legacyEntrypoint,
    'kline',
    '{"symbol":"BTC","period":"3600","limit":3}',
  ], { encoding: 'utf8' });

  assert.equal(result.status, 2);
  const body = JSON.parse(result.stdout);
  assert.equal(body.ok, false);
  assert.equal(body.error.code, 'legacy_entrypoint_retired');
  assert.match(body.error.message, /aicoin\.mjs market\/klines/);
  assert.match(body.error.message, /coin_key/);
  assert.doesNotMatch(result.stdout, /kline_data/);
});
