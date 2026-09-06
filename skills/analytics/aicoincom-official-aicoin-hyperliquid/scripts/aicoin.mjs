#!/usr/bin/env node
// AiCoin Open Data v3 — one entry point for every endpoint.
//
//   node scripts/aicoin.mjs <endpoint> ['<json params>']   call any v3 endpoint
//   node scripts/aicoin.mjs catalog [group|endpoint]        list endpoints (the live API menu)
//   node scripts/aicoin.mjs key                             show API key status + access probe
//   node scripts/aicoin.mjs set-key <id> <secret>           validate & save a new key to .env
//
// Endpoint = the path after /api/v3/ , e.g.  market/ticker  ,  hyperliquid/whales/open-positions
// Every call prints the v3 envelope {ok, data, error, meta}. Check `ok` first.
import { request, resolveMethod, fetchCatalog, saveKey, summarizeTimeseries, KEY, USING_OWN_KEY } from '../lib/client.mjs';

const out = (o) => console.log(JSON.stringify(o, null, 2));
const groupOf = (p) => p.replace(/^\/api\/v3\//, '').split('/')[0] || '_catalog';
const rel = (p) => p.replace(/^\/api\/v3\//, '');

function positiveEnvMs(name, fallback) {
  const value = Number(process.env[name]);
  return Number.isFinite(value) && value > 0 ? value : fallback;
}

function isTimeoutError(error) {
  return error?.name === 'TimeoutError'
    || error?.code === 'ABORT_ERR'
    || /aborted due to timeout|timed? ?out/i.test(error?.message || '');
}

function cleanEndpoint(endpoint) {
  return String(endpoint || '').replace(/^\/?api\/v3\//, '').replace(/^\//, '');
}

function endpointTimeoutMs(endpoint) {
  const configured = positiveEnvMs('AICOIN_REQUEST_TIMEOUT_MS', 0);
  if (configured > 0) return configured;
  return cleanEndpoint(endpoint) === 'derivatives/funding-rates' ? 10000 : 30000;
}

function timeoutEnvelope(error) {
  return {
    ok: false,
    data: null,
    error: { code: 'upstream_timeout', message: error?.message || 'upstream request timed out' },
    meta: {},
    _hint: '服务端/上游超时，不是 Key 失效。不要连续重试；继续使用已成功返回的行情/K线数据，并明确标注该项暂不可用。',
  };
}

function annotateEndpointResult(endpoint, body, httpStatus) {
  const ep = cleanEndpoint(endpoint);
  if (!body || typeof body !== 'object') return body;

  if (ep === 'market/orderbook/latest-depth' && httpStatus >= 500) {
    body._hint = '该交易对可能暂无深度快照覆盖，或深度上游暂时异常；这不是 Key 失效。不要连续重试，行情与 K 线仍可继续使用。';
  }

  if (ep === 'derivatives/funding-rates' && httpStatus >= 500) {
    body._hint = '资金费率服务端/上游异常，不是 Key 失效。不要连续重试；继续完成不依赖资金费率的分析。';
  }

  if ((ep === 'market/indicator-klines' || ep === 'market/indicator-pairs') && body.ok === true) {
    const series = ep === 'market/indicator-klines' ? body.data?.list : body.data?.items;
    if (Array.isArray(series) && series.length === 0) {
      body.meta = { ...(body.meta || {}), coverage: 'not_available' };
      body._hint = '当前指标与交易对暂无覆盖数据，不是请求失败。不要重试；改用已覆盖的数据项，并如实标注缺失。';
    }
  }

  return body;
}

const HINTS = {
  401: 'HTTP 401 — 签名或鉴权失败，检查 API key 是否正确。',
  403: 'HTTP 403 — 此接口当前 key 无权限。**先别断言「套餐不够」**：本地 host 最常见的坑是脚本 fallback 到了免费/旧 key —— 跑 `node scripts/aicoin.mjs key` 看 key_id 是不是你的专业版（key 应放 ~/.coinos/.env）。确属套餐不足，再让用户去 https://www.aicoin.com/opendata 升级。不要重试。',
  404: 'HTTP 404 — 资源不存在，检查 id / 参数是否对。',
  429: 'HTTP 429 — 触发限流，等 30-60 秒再试，或把多个查询合并成一次。',
  500: 'HTTP 500 — 服务端/上游故障，可隔 1-2 分钟重试；持续失败请联系 service@aicoin.com。',
  501: 'HTTP 501 — 该接口尚未实现（数据源未接通），换其他接口。',
  502: 'HTTP 502 — 网关临时故障，隔 1-2 分钟重试。',
  503: 'HTTP 503 — 服务暂时不可用，稍后重试。',
  504: 'HTTP 504 — 网关超时，稍后重试。',
};

async function callEndpoint(endpoint, rawParams) {
  let params = {};
  if (rawParams) {
    try { params = JSON.parse(rawParams); }
    catch { return out({ ok: false, error: { code: 'bad_params', message: `参数不是合法 JSON: ${rawParams}` }, _hint: "参数要用 JSON 对象，例: '{\"coin_key\":\"bitcoin\",\"market\":\"binance\"}'" }); }
  }
  const resolved = await resolveMethod(endpoint);
  if (!resolved) {
    return out({ ok: false, error: { code: 'unknown_endpoint', message: `未知接口: ${endpoint}` }, _hint: '跑 `node scripts/aicoin.mjs catalog` 看全部接口。' });
  }
  let res;
  try {
    res = await request(resolved.method, endpoint, params, fetch, {
      timeoutMs: endpointTimeoutMs(endpoint),
    });
  } catch (e) {
    if (isTimeoutError(e)) return out(timeoutEnvelope(e));
    return out({ ok: false, data: null, error: { code: 'network', message: e.message }, meta: {}, _hint: '网络连接失败；这不能证明 Key 无效。检查网络后再试一次。' });
  }
  const body = (res.body && typeof res.body === 'object') ? res.body : { raw: res.body };
  if (res.httpStatus !== 200 && HINTS[res.httpStatus]) body._hint = HINTS[res.httpStatus];
  annotateEndpointResult(endpoint, body, res.httpStatus);
  // 时序数组: 附一个 order-independent 的 latest, 防 agent 用 tail/arr[0] 猜错方向。
  if (body && body.ok) {
    let series = Array.isArray(body.data) ? body.data : null;
    let where = 'data';
    if (!series && body.data && typeof body.data === 'object') {
      for (const k of ['candles', 'list', 'items', 'records', 'rows', 'data']) {
        if (Array.isArray(body.data[k])) { series = body.data[k]; where = `data.${k}`; break; }
      }
    }
    if (series) { const ts = summarizeTimeseries(series); if (ts) body._timeseries = { in: where, ...ts }; }
  }
  out(body);
}

async function showCatalog(filter) {
  const { endpoints, live } = await fetchCatalog();
  endpoints.sort((a, b) => a.path.localeCompare(b.path));

  if (filter) {
    // Group match wins over a same-named bare endpoint (e.g. `indexes` is both
    // the group and the path /api/v3/indexes) — the group view is more useful.
    const inGroup = endpoints.filter((e) => groupOf(e.path) === filter);
    if (inGroup.length) {
      const lines = [`# ${filter} (${inGroup.length} 个接口)　来源: ${live ? '线上' : '本地快照'}\n`];
      for (const e of inGroup) {
        lines.push(`${e.method} ${rel(e.path)}  —  ${e.summary || ''}`);
        for (const p of e.params || []) {
          const bits = [p.in, p.required ? '必填' : '可选', p.type];
          if (p.enum) bits.push('枚举:' + p.enum.join('/'));
          if (p.example) bits.push('例:' + p.example);
          lines.push(`    ${p.name}  (${bits.filter(Boolean).join(', ')})  ${p.desc || ''}`);
        }
        lines.push('');
      }
      return console.log(lines.join('\n'));
    }
    // Not a group — treat the filter as a single endpoint path.
    const exact = endpoints.find((e) => rel(e.path) === filter || e.path === filter);
    if (exact) return out({ source: live ? 'live' : 'snapshot', endpoint: exact });
    return out({ ok: false, error: { code: 'no_match', message: `没有 "${filter}" 分组或接口` }, _hint: '不带参数跑 catalog 看全部分组。' });
  }

  // Full table of contents — grouped, paths + summaries (no params).
  const groups = {};
  for (const e of endpoints) (groups[groupOf(e.path)] ||= []).push(e);
  const lines = [
    `# AiCoin v3 接口清单 — ${endpoints.length} 个，${Object.keys(groups).length} 个分组　(来源: ${live ? '线上' : '本地快照'})`,
    `# 看某分组的参数:  node scripts/aicoin.mjs catalog <分组名>`,
    `# 调用:  node scripts/aicoin.mjs <接口> '<JSON 参数>'\n`,
  ];
  for (const [g, es] of Object.entries(groups)) {
    lines.push(`### ${g} (${es.length})`);
    for (const e of es) lines.push(`  ${e.method.padEnd(4)} ${rel(e.path).padEnd(46)} ${e.summary || ''}`);
    lines.push('');
  }
  console.log(lines.join('\n'));
}

async function showKey() {
  const probes = [
    ['coins/tickers', { coin_key: 'bitcoin' }],
    ['derivatives/funding-rates', { coin_key: 'bitcoin', market: 'binance' }],
    ['market/big-orders', { coin_key: 'bitcoin', market: 'binance' }],
    ['hyperliquid/whales/open-positions', { coin: 'BTC' }],
    ['treasuries/summary', { coin_key: 'bitcoin' }],
  ];
  const probeTimeoutMs = positiveEnvMs('AICOIN_KEY_PROBE_TIMEOUT_MS', 3000);
  const access = await Promise.all(probes.map(async ([ep, params], index) => {
    const affectsKeyValidity = index === 0;
    try {
      const { httpStatus, body } = await request('GET', ep, params, fetch, {
        timeoutMs: probeTimeoutMs,
      });
      return {
        endpoint: ep,
        http: httpStatus,
        ok: body?.ok === true,
        affects_key_validity: affectsKeyValidity,
      };
    } catch (e) {
      return {
        endpoint: ep,
        error_code: isTimeoutError(e) ? 'upstream_timeout' : 'network',
        error: e.message,
        affects_key_validity: affectsKeyValidity,
      };
    }
  }));
  const primary = access[0];
  const validity = primary?.http === 200 && primary?.ok === true
    ? 'valid'
    : primary?.http === 401
      ? 'invalid'
      : 'unknown';
  out({
    key_id: KEY ? KEY.slice(0, 6) + '…' : null,
    source: USING_OWN_KEY ? '用户自己的 key (.env)' : '内置免费 key',
    validity,
    access,
    note: 'Key 有效性只由基础行情探测判断。其他接口超时/5xx 表示该能力或上游异常；403 表示当前套餐不覆盖，均不等于 Key 失效。',
  });
}

const USAGE = `AiCoin Open Data v3
  node scripts/aicoin.mjs <接口> '<JSON参数>'   调任意 v3 接口，例:
      node scripts/aicoin.mjs market/ticker '{"coin_key":"bitcoin","market":"binance"}'
      node scripts/aicoin.mjs coins/tickers '{"coin_key":"bitcoin,ethereum"}'
      node scripts/aicoin.mjs hyperliquid/whales/open-positions '{"coin":"BTC"}'
  node scripts/aicoin.mjs catalog [分组]        看接口清单（不确定接口/参数时先跑这个）
  node scripts/aicoin.mjs key                   看 key 状态 + 权限探测
  node scripts/aicoin.mjs set-key <id> <secret> 校验并保存新 key`;

const [cmd, ...rest] = process.argv.slice(2);
(async () => {
  if (!cmd || cmd === 'help' || cmd === '-h' || cmd === '--help') return console.log(USAGE);
  if (cmd === 'catalog') return showCatalog(rest[0]);
  if (cmd === 'key') return showKey();
  if (cmd === 'set-key') {
    let id, secret;
    const raw = rest.join(' ').trim();
    if (raw.startsWith('{')) {
      // JSON 模式:兼容 AiCoin 后台直接拷下来的 {"api_key","access_key"}
      // 注意 AiCoin 后台命名反直觉 —— `api_key` 是公开 ID,`access_key` 才是 SECRET。
      // 也兼容 {"access_key_id","access_secret"} 等更直白的命名。
      try {
        const j = JSON.parse(raw);
        id = j.access_key_id || j.accessKeyId || j.key_id || j.api_key || j.key;
        secret = j.access_secret || j.accessSecret || j.secret_key || j.secret || j.access_key;
      } catch {
        return out({ ok: false, error: { code: 'bad_json', message: '参数不是合法 JSON' } });
      }
    } else if (rest.length >= 2) {
      id = rest[0];
      secret = rest[1];
    }
    if (!id || !secret) {
      return out({ ok: false, error: { code: 'bad_args', message: "用法: set-key <key_id> <secret>  或  set-key '<json>'(JSON 字段名兼容 api_key/access_key、access_key_id/access_secret 等;AiCoin 后台 api_key 是 ID、access_key 是 SECRET)" } });
    }
    const r = await saveKey(id, secret);
    return out(r.ok ? { ok: true, message: `key 已保存到 ${r.file}` } : { ok: false, error: { code: 'invalid_key', message: r.error } });
  }
  return callEndpoint(cmd, rest.join(' ').trim() || null);
})().catch((e) => { out({ ok: false, error: { code: 'fatal', message: e.message } }); process.exit(1); });
