import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { promisify } from 'node:util';
import test from 'node:test';

const execFileAsync = promisify(execFile);
const here = dirname(fileURLToPath(import.meta.url));
const cli = resolve(here, 'aicoin.mjs');

async function withServer(handler, run) {
  const server = createServer(handler);
  await new Promise((resolveListen) => server.listen(0, '127.0.0.1', resolveListen));
  const { port } = server.address();
  try {
    return await run(`http://127.0.0.1:${port}`);
  } finally {
    server.closeAllConnections?.();
    await new Promise((resolveClose) => server.close(resolveClose));
  }
}

function json(res, status, body) {
  res.writeHead(status, { 'content-type': 'application/json' });
  res.end(JSON.stringify(body));
}

async function runCLI(baseURL, args, extraEnv = {}, timeout = 800) {
  try {
    const result = await execFileAsync(process.execPath, [cli, ...args], {
      env: {
        ...process.env,
        AICOIN_BASE_URL: baseURL,
        ...extraEnv,
      },
      timeout,
      maxBuffer: 1024 * 1024,
    });
    return { body: JSON.parse(result.stdout), elapsedError: null };
  } catch (error) {
    return { body: null, elapsedError: error };
  }
}

test('key self-check is bounded and separates an upstream timeout from key validity', async () => {
  await withServer((req, res) => {
    if (req.url.startsWith('/api/v3/derivatives/funding-rates')) return;
    json(res, 200, { ok: true, data: {}, error: null, meta: {} });
  }, async (baseURL) => {
    const { body, elapsedError } = await runCLI(baseURL, ['key'], {
      AICOIN_KEY_PROBE_TIMEOUT_MS: '40',
    });

    assert.ok(body, `key self-check exceeded its probe budget: ${elapsedError?.message}`);
    assert.equal(body.validity, 'valid');
    const funding = body.access.find((item) => item.endpoint === 'derivatives/funding-rates');
    assert.equal(funding.error_code, 'upstream_timeout');
    assert.equal(funding.affects_key_validity, false);
  });
});

test('key self-check reports invalid only when the primary authentication probe returns 401', async () => {
  await withServer((req, res) => {
    if (req.url.startsWith('/api/v3/coins/tickers')) {
      return json(res, 401, {
        ok: false,
        data: null,
        error: { code: '401', message: 'unauthorized' },
        meta: {},
      });
    }
    json(res, 500, {
      ok: false,
      data: null,
      error: { code: 'internal_error', message: 'upstream failed' },
      meta: {},
    });
  }, async (baseURL) => {
    const { body } = await runCLI(baseURL, ['key']);

    assert.equal(body.validity, 'invalid');
    assert.equal(body.access[0].affects_key_validity, true);
    assert.ok(body.access.slice(1).every((item) => item.affects_key_validity === false));
  });
});

test('funding-rates timeout is reported as upstream_timeout, not a key or generic network error', async () => {
  await withServer(() => {}, async (baseURL) => {
    const { body, elapsedError } = await runCLI(
      baseURL,
      ['derivatives/funding-rates', '{"coin_key":"hype","market":"binance"}'],
      { AICOIN_REQUEST_TIMEOUT_MS: '40' },
    );

    assert.ok(body, `funding-rates call exceeded its request budget: ${elapsedError?.message}`);
    assert.equal(body.error.code, 'upstream_timeout');
    assert.match(body._hint, /不是 Key|非 Key/);
    assert.match(body._hint, /不要连续重试/);
  });
});

test('latest-depth 500 explains pair coverage without claiming the key is invalid', async () => {
  await withServer((req, res) => {
    json(res, 500, {
      ok: false,
      data: null,
      error: { code: 'internal_error', message: 'failed to get latest depth' },
      meta: {},
    });
  }, async (baseURL) => {
    const { body } = await runCLI(
      baseURL,
      ['market/orderbook/latest-depth', '{"coin_key":"hype","market":"binance","contract_type":"perpetual"}'],
    );

    assert.equal(body.error.code, 'internal_error');
    assert.match(body._hint, /深度.*覆盖|覆盖.*深度/);
    assert.match(body._hint, /不是 Key|非 Key/);
  });
});

test('empty indicator series is explicitly marked as unavailable coverage', async () => {
  await withServer((req, res) => {
    json(res, 200, {
      ok: true,
      data: { indicator_key: 'fr', list: [], mapping: [], pair: { coin_key: 'hype' } },
      error: null,
      meta: { count: 0 },
    });
  }, async (baseURL) => {
    const { body } = await runCLI(
      baseURL,
      ['market/indicator-klines', '{"coin_key":"hype","market":"binance","indicator_key":"fr"}'],
    );

    assert.equal(body.ok, true);
    assert.equal(body.meta.coverage, 'not_available');
    assert.match(body._hint, /没有覆盖|暂无覆盖/);
    assert.match(body._hint, /不要重试/);
  });
});

test('empty indicator pair coverage is explicitly marked as unavailable', async () => {
  await withServer((req, res) => {
    json(res, 200, {
      ok: true,
      data: { indicator_key: 'fr', items: [] },
      error: null,
      meta: { count: 0 },
    });
  }, async (baseURL) => {
    const { body } = await runCLI(
      baseURL,
      ['market/indicator-pairs', '{"coin_key":"hype","indicator_key":"fr"}'],
    );

    assert.equal(body.ok, true);
    assert.equal(body.meta.coverage, 'not_available');
    assert.match(body._hint, /暂无覆盖/);
  });
});

test('market/klines CLI exposes an order-independent latest candle', async () => {
  await withServer((req, res) => {
    const url = new URL(req.url, 'http://localhost');
    if (url.pathname === '/api/v3/market/ticker') {
      return json(res, 200, {
        ok: true,
        data: {
          pair: { coin_key: 'bitcoin', market: 'binance' },
          ticker: { key: 'btcusdt:binance' },
        },
        error: null,
        meta: {},
      });
    }
    if (url.pathname === '/api/v2/commonKline/dataRecords') {
      return json(res, 200, {
        success: true,
        errorCode: 200,
        error: '',
        data: {
          kline_data: [
            [1787032800, 10, 12, 9, 11, 100],
            [1787036400, 11, 13, 10, 12, 120],
          ],
        },
      });
    }
    json(res, 404, { ok: false });
  }, async (baseURL) => {
    const { body } = await runCLI(
      baseURL,
      ['market/klines', '{"coin_key":"bitcoin","market":"binance","interval":"1h","limit":2}'],
      {
        AICOIN_ACCESS_KEY_ID: 'test-key',
        AICOIN_ACCESS_SECRET: 'test-secret',
      },
      2000,
    );

    assert.equal(body._timeseries.in, 'data.candles');
    assert.equal(body._timeseries.latest.timestamp, 1787036400000);
    assert.match(body._timeseries.order, /最新在末尾/);
  });
});
