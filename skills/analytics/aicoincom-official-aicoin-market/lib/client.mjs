#!/usr/bin/env node
// AiCoin Open Data v3 API client — HMAC-SHA1 signed, header auth.
// One unified envelope {ok, data, error, meta}; see catalog for all endpoints.
import { createHmac, randomBytes } from 'node:crypto';
import { readFileSync, existsSync, writeFileSync, mkdirSync, chmodSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { loadEnv, writeEnvPath } from './env-loader.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));

// .env auto-load (宿主可能不向子进程注入 env)。共享 loader,见 lib/env-loader.mjs。
loadEnv();

const defaults = JSON.parse(readFileSync(resolve(__dirname, 'defaults.json'), 'utf-8'));
export const BASE = process.env.AICOIN_BASE_URL || 'https://open.aicoin.com';
export const KEY = process.env.AICOIN_ACCESS_KEY_ID || defaults.accessKeyId;
const SECRET = process.env.AICOIN_ACCESS_SECRET || defaults.accessSecret;
export const USING_OWN_KEY = !!(process.env.AICOIN_ACCESS_KEY_ID && process.env.AICOIN_ACCESS_SECRET);

// HMAC-SHA1(signStr, secret) → hex → base64. The 4 values ride in X-Aic-* headers.
function authHeaders(keyId = KEY, secret = SECRET) {
  const nonce = randomBytes(8).toString('hex');
  const ts = Math.floor(Date.now() / 1000).toString();
  const signStr = `AccessKeyId=${keyId}&SignatureNonce=${nonce}&Timestamp=${ts}`;
  const hex = createHmac('sha1', secret).update(signStr).digest('hex');
  return {
    'X-Aic-AccessKey-Id': keyId,
    'X-Aic-Signature-Nonce': nonce,
    'X-Aic-Timestamp': ts,
    'X-Aic-Signature': Buffer.from(hex).toString('base64'),
  };
}

// Normalize a user-supplied endpoint to a full /api/v3/... path.
//   "market/ticker" / "/market/ticker" / "/api/v3/market/ticker"  → "/api/v3/market/ticker"
export function normalizePath(ep) {
  let p = String(ep || '').trim().replace(/^https?:\/\/[^/]+/, '');
  if (p.startsWith('/api/v3/') || p === '/api/v3') return p;
  p = p.replace(/^\/?(api\/v3\/?)?/, '');
  return '/api/v3/' + p;
}

const KLINE_INTERVAL_SECONDS = Object.freeze({
  '1m': 60,
  '3m': 180,
  '5m': 300,
  '15m': 900,
  '30m': 1800,
  '1h': 3600,
  '2h': 7200,
  '4h': 14400,
  '6h': 21600,
  '8h': 28800,
  '12h': 43200,
  '1d': 86400,
  '3d': 259200,
  '1w': 604800,
});

function legacyAuthParams() {
  const headers = authHeaders();
  return {
    AccessKeyId: headers['X-Aic-AccessKey-Id'],
    SignatureNonce: headers['X-Aic-Signature-Nonce'],
    Timestamp: headers['X-Aic-Timestamp'],
    Signature: headers['X-Aic-Signature'],
  };
}

async function readJsonResponse(res) {
  const text = await res.text();
  try { return JSON.parse(text); }
  catch { return { ok: false, error: { code: 'bad_response', message: text.slice(0, 300) } }; }
}

async function requestV3(method, full, params, fetchImpl = fetch, options = {}) {
  const m = (method || 'GET').toUpperCase();
  const headers = authHeaders();
  let url = `${BASE}${full}`;
  const configuredTimeout = Number(options?.timeoutMs);
  const timeoutMs = Number.isFinite(configuredTimeout) && configuredTimeout > 0
    ? configuredTimeout
    : 30000;
  const init = { method: m, headers, signal: AbortSignal.timeout(timeoutMs) };
  if (m === 'GET' || m === 'DELETE') {
    const qs = new URLSearchParams();
    for (const [k, v] of Object.entries(params || {})) {
      if (v === undefined || v === null || v === '') continue;
      qs.set(k, Array.isArray(v) ? v.join(',') : String(v));
    }
    const s = qs.toString();
    if (s) url += `?${s}`;
  } else {
    headers['Content-Type'] = 'application/json';
    init.body = JSON.stringify(params || {});
  }
  const res = await fetchImpl(url, init);
  let body = await readJsonResponse(res);
  // v3 business endpoints answer with {ok,...}. Auth / quota errors from the
  // gateway are still legacy-shaped ({success:false,errorCode,error}); fold them
  // into the same envelope so callers only ever branch on `ok`.
  if (body && typeof body === 'object' && typeof body.ok !== 'boolean' && (res.status >= 400 || body.success === false)) {
    body = {
      ok: false,
      data: null,
      error: {
        code: body.errorCode != null ? String(body.errorCode) : String(res.status),
        message: body.error || body.message || body.msg || `HTTP ${res.status}`,
      },
      meta: {},
    };
  }
  return { httpStatus: res.status, body };
}

/**
 * The v3 K-line gateway currently returns an empty series after a long wait
 * for pairs that the v2 commonKline endpoint serves immediately. Resolve the
 * canonical dbkey through the fast v3 ticker, then use the documented v2
 * endpoint and normalize it back to the v3 envelope. The same user credential
 * signs both calls; no platform/global key is introduced here.
 */
async function requestLegacyKlines(params, fetchImpl = fetch) {
  const period = KLINE_INTERVAL_SECONDS[params?.interval || '15m'];
  if (!period) return null;

  const tickerParams = {
    coin_key: params?.coin_key,
    market: params?.market,
    quote_coin_key: params?.quote_coin_key,
    contract_type: params?.contract_type,
  };
  const ticker = await requestV3('GET', '/api/v3/market/ticker', tickerParams, fetchImpl);
  const symbol = ticker.body?.ok === true ? ticker.body?.data?.ticker?.key : null;
  if (!symbol || typeof symbol !== 'string') return null;

  const size = Math.max(1, Math.min(500, Number(params?.limit) || 100));
  const endTime = Number(params?.end_time);
  const query = new URLSearchParams({
    symbol,
    period: String(period),
    size: String(size),
    ...(Number.isFinite(endTime) && endTime > 0
      ? { since: String(Math.floor(endTime / 1000)) }
      : {}),
    ...legacyAuthParams(),
  });
  const res = await fetchImpl(`${BASE}/api/v2/commonKline/dataRecords?${query}`, {
    method: 'GET',
    signal: AbortSignal.timeout(15000),
  });
  const body = await readJsonResponse(res);
  const rows = body?.success === true && Array.isArray(body?.data?.kline_data)
    ? body.data.kline_data
    : null;
  if (!res.ok || !rows?.length) return null;

  const startTime = Number(params?.start_time);
  const candles = rows
    .map((row) => ({
      timestamp: Number(row?.[0]) * 1000,
      open: Number(row?.[1]),
      high: Number(row?.[2]),
      low: Number(row?.[3]),
      close: Number(row?.[4]),
      volume: Number(row?.[5]),
    }))
    .filter((candle) => Number.isFinite(candle.timestamp)
      && (!Number.isFinite(startTime) || startTime <= 0 || candle.timestamp >= startTime))
    .sort((a, b) => a.timestamp - b.timestamp)
    .slice(-size);
  if (!candles.length) return null;

  return {
    httpStatus: 200,
    body: {
      ok: true,
      data: {
        candles,
        pair: ticker.body?.data?.pair || null,
      },
      error: null,
      meta: {
        count: candles.length,
        interval: params?.interval || '15m',
        start_time: candles[0].timestamp,
        end_time: candles[candles.length - 1].timestamp,
        source: 'v2_common_kline_fallback',
      },
    },
  };
}

// endpoints.json — a bundled catalog snapshot. Drives GET/POST selection and
// offline `catalog`. Live catalog is still the source of truth (see fetchCatalog).
let _snapshot = null;
export function snapshotEndpoints() {
  if (_snapshot) return _snapshot;
  try {
    const j = JSON.parse(readFileSync(resolve(__dirname, 'endpoints.json'), 'utf-8'));
    _snapshot = j.endpoints || [];
  } catch { _snapshot = []; }
  return _snapshot;
}

// Pull the live catalog. Falls back to the bundled snapshot when offline.
export async function fetchCatalog() {
  try {
    const { httpStatus, body } = await request('GET', '/api/v3/_catalog');
    if (httpStatus === 200 && body?.data?.endpoints) return { endpoints: body.data.endpoints, live: true };
  } catch { /* fall through to snapshot */ }
  return { endpoints: snapshotEndpoints(), live: false };
}

// Core request. Returns { httpStatus, body }; body is the parsed envelope.
export async function request(method, path, params = {}, fetchImpl = fetch, options = {}) {
  const full = normalizePath(path);
  const m = (method || 'GET').toUpperCase();
  if (m === 'GET' && full === '/api/v3/market/klines') {
    try {
      const legacy = await requestLegacyKlines(params, fetchImpl);
      if (legacy) return legacy;
    } catch {
      // Preserve the v3 behavior if pair resolution or the documented v2
      // fallback is temporarily unavailable.
    }
  }
  return requestV3(m, full, params, fetchImpl, options);
}

// Resolve which HTTP method an endpoint uses, from snapshot then live catalog.
export async function resolveMethod(path) {
  const full = normalizePath(path);
  let hit = snapshotEndpoints().find(e => e.path === full);
  if (hit) return { method: hit.method, spec: hit };
  // 快照里没有 → 查 live catalog。
  const { endpoints, live } = await fetchCatalog();
  hit = endpoints.find(e => e.path === full);
  if (hit) return { method: hit.method, spec: hit };
  // live catalog 可达且确实无此端点 → 真·未知端点,硬失败。
  if (live) return null;
  // catalog 不可达(离线/抖动):别误杀可能有效的新端点 —— 默认按 GET 尝试,
  // 让请求本身的 HTTP 状态(404/405)做最终判定,而不是 pre-flight 拒绝。
  return { method: 'GET', spec: null, _assumed: true, _note: 'catalog unreachable; assuming GET' };
}

// 给"时序数组"返回算一个**跟数组正序/倒序无关**的最新值,防止 agent 用 tail / arr[0]
// 猜错方向(history-long-ratio 等接口曾因倒序被 tail 读到 2 天前旧值,误判"大户边际加空")。
// 找一个所有元素都有、能解析成时间戳(秒/毫秒 epoch 或可解析日期串)的字段, latest=时间戳最大那条。
// 识别不出时间字段就返回 null(不附 _timeseries, 退回 SKILL.md 文档约定)。
export function summarizeTimeseries(arr) {
  if (!Array.isArray(arr) || arr.length < 2) return null;
  if (!arr.every(e => e && typeof e === 'object' && !Array.isArray(e))) return null;
  const PREF = ['timestamp', 'time', 'ts', 't', 'date', 'datetime', 'create_time', 'created_at', 'update_time', 'updated_at'];
  const toTs = (v) => {
    if (typeof v === 'number' && isFinite(v)) {
      if (v >= 1e12 && v < 4e12) return v;        // 毫秒 epoch
      if (v >= 1e9 && v < 4e9) return v * 1000;   // 秒 epoch
      return null;
    }
    if (typeof v === 'string') {
      if (/^\d{13}$/.test(v)) return Number(v);
      if (/^\d{10}$/.test(v)) return Number(v) * 1000;
      const d = Date.parse(v);
      return isNaN(d) ? null : d;
    }
    return null;
  };
  const keys = Object.keys(arr[0]);
  // 只把"名字像时间"且值能解析成时间戳的字段当时间列 —— 否则十亿级的 volume/market_cap/OI、
  // 万亿级的 total mcap 等纯数值列会被误判成 epoch,给排名/持仓类列表错附 _timeseries
  // (latest 会指向数值最大那行而非最新)。名字 + 值双重 gate。
  const isTimeName = (k) => {
    const s = k.toLowerCase();
    return PREF.includes(s) || /time|date/.test(s) || /_at$/.test(s) || s === 'ts' || s === 't';
  };
  const candidates = keys.filter(k => isTimeName(k) && arr.every(e => toTs(e[k]) != null));
  if (!candidates.length) return null;
  candidates.sort((a, b) => {
    const ia = PREF.indexOf(a.toLowerCase()), ib = PREF.indexOf(b.toLowerCase());
    return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
  });
  let field = null, order = 'unsorted';
  for (const k of candidates) {
    const ts = arr.map(e => toTs(e[k]));
    let asc = true, desc = true;
    for (let i = 1; i < ts.length; i++) { if (ts[i] < ts[i - 1]) asc = false; if (ts[i] > ts[i - 1]) desc = false; }
    if (asc || desc) { field = k; order = asc ? 'ascending (最新在末尾)' : 'descending (最新在开头 arr[0])'; break; }
  }
  // 没有任何"时间列"单调 → 这多半不是真时序,而是带逐行时间戳的排名/快照列表(volume/OI/榜单等)。
  // 此时 latest=时间戳最大那行会指向"最近更新的那一行"而非榜首,误导性强 —— 干脆不附 _timeseries,
  // 退回 SKILL.md 文档约定。真正的时序数据一定按时间单调(asc/desc),会在上面命中。
  if (!field) return null;
  let li = 0, oi = 0, lv = toTs(arr[0][field]), ov = lv;
  arr.forEach((e, i) => { const v = toTs(e[field]); if (v > lv) { lv = v; li = i; } if (v < ov) { ov = v; oi = i; } });
  return {
    count: arr.length, field, order, latest: { ...arr[li] }, oldest: { ...arr[oi] },
    _note: '_timeseries.latest = 时间戳最大那条(与数组顺序无关);取"最新/当前"值用它,别默认数组末尾或开头。做"边际变化/趋势"用 latest vs oldest 或自行按 field 排序。',
  };
}

// Persist a new key pair to the workspace .env (validates before writing).
export async function saveKey(keyId, secret) {
  const headers = authHeaders(keyId, secret);
  const res = await fetch(`${BASE}/api/v3/coins/tickers?coin_key=bitcoin`, { headers, signal: AbortSignal.timeout(15000) });
  if (res.status === 401 || res.status === 403) return { ok: false, error: `key 验证失败 (HTTP ${res.status})` };
  if (!res.ok) return { ok: false, error: `验证请求失败 (HTTP ${res.status})` };
  const target = writeEnvPath();
  let lines = existsSync(target) ? readFileSync(target, 'utf-8').split('\n') : [];
  const set = (k, v) => {
    const i = lines.findIndex(l => l.trim().startsWith(k + '='));
    if (i >= 0) lines[i] = `${k}=${v}`; else lines.push(`${k}=${v}`);
  };
  set('AICOIN_ACCESS_KEY_ID', keyId);
  set('AICOIN_ACCESS_SECRET', secret);
  try { mkdirSync(dirname(target), { recursive: true }); } catch {}
  writeFileSync(target, lines.join('\n'));
  try { chmodSync(target, 0o600); } catch {}
  return { ok: true, file: target };
}
