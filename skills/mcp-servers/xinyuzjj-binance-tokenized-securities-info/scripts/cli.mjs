#!/usr/bin/env node
// binance-tokenized-securities-info CLI — self-contained, zero-dep, Node >= 22
// Usage: node cli.mjs <command> '<json_params>'
//
// Ondo 代币化美股 RWA 数据（币安 Web3）。全部为公开 GET 接口，无需鉴权。
//
// Commands:
//   symbol-list   列出全部代币化股票（Ondo）。params: { type? }  → type=1 仅 Ondo（默认）
//   meta          个股元数据（公司信息 / 审计报告）。params: { chainId, contractAddress }
//   market-status 整体市场开闭状态。params: {}（无需参数）
//   asset-status  单资产交易状态 / 公司行动。params: { chainId, contractAddress }
//   dynamic       实时链上 + 美股基本面。params: { chainId, contractAddress }
//   kline         K 线。params: { chainId, contractAddress, interval, limit?, startTime?, endTime? }
//                   interval: 1m | 5m | 15m | 1h | 4h | 12h | 1d   limit: 默认 300，上限 300
//
// Windows 直跑判定用 realpath 比较（官方 `file://` + argv[1] 拼接在反斜杠路径下必失败），
// 因此本脚本可被 import 也可被 node 直接执行。

import { realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const TIMEOUT_MS = 15_000;
const UA = { 'Accept-Encoding': 'identity', 'User-Agent': 'binance-web3/1.1 (Skill)' };

// API 5 用 v2，其余 v1；动态接口也可在响应里携带 statusInfo（同 asset-status schema）
const API1_SYMBOL_LIST = 'https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai';
const API2_RWA_META = 'https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/meta/ai';
const API3_MARKET_STATUS = 'https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/market/status/ai';
const API4_ASSET_STATUS = 'https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/asset/market/status/ai';
const API5_RWA_DYNAMIC = 'https://www.binance.com/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/rwa/dynamic/ai';
const API6_KLINE = 'https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/dex/market/token/kline/ai';

const KLINE_INTERVALS = ['1m', '5m', '15m', '1h', '4h', '12h', '1d'];

const qs = (p) => Object.entries(p)
  .filter(([, v]) => v !== undefined && v !== null && v !== '')
  .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
  .join('&');

async function call({ url, method = 'GET', body, headers = {} }) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  const opts = { method, headers: { ...UA, ...headers }, signal: ctrl.signal };
  if (method === 'POST') {
    opts.headers['content-type'] = 'application/json';
    opts.body = JSON.stringify(body || {});
  }
  let res;
  try { res = await fetch(url, opts); }
  catch { clearTimeout(timer); throw Object.assign(new Error('Network request failed'), { exitCode: 3 }); }
  clearTimeout(timer);
  const data = await res.json();
  if (res.status >= 400) throw Object.assign(new Error(`HTTP ${res.status}`), { exitCode: 1, body: data });
  return data;
}

function requireParam(p, name, command) {
  if (p[name] === undefined || p[name] === null || p[name] === '') {
    throw Object.assign(new Error(`${command}: missing required param "${name}"`), { exitCode: 1 });
  }
  return p[name];
}

// 常用个股合约（ETH/BSC）查询可由调用方先跑 symbol-list 得到；这里不强依赖硬编码。
const COMMANDS = {
  'symbol-list': (p) => {
    // type=1 → 仅 Ondo Finance（当前唯一代币化美股供应商，推荐过滤）
    const type = p.type === undefined || p.type === null || p.type === '' ? 1 : p.type;
    return { url: `${API1_SYMBOL_LIST}?${qs({ type })}` };
  },
  meta: (p) => ({
    url: `${API2_RWA_META}?${qs({
      chainId: requireParam(p, 'chainId', 'meta'),
      contractAddress: requireParam(p, 'contractAddress', 'meta'),
    })}`,
  }),
  'market-status': () => ({ url: API3_MARKET_STATUS }),
  'asset-status': (p) => ({
    url: `${API4_ASSET_STATUS}?${qs({
      chainId: requireParam(p, 'chainId', 'asset-status'),
      contractAddress: requireParam(p, 'contractAddress', 'asset-status'),
    })}`,
  }),
  dynamic: (p) => ({
    url: `${API5_RWA_DYNAMIC}?${qs({
      chainId: requireParam(p, 'chainId', 'dynamic'),
      contractAddress: requireParam(p, 'contractAddress', 'dynamic'),
    })}`,
  }),
  kline: (p) => {
    const interval = requireParam(p, 'interval', 'kline');
    if (!KLINE_INTERVALS.includes(interval)) {
      throw Object.assign(
        new Error(`kline: unsupported interval "${interval}". Supported: ${KLINE_INTERVALS.join(', ')}`),
        { exitCode: 1 },
      );
    }
    let limit = p.limit;
    if (limit !== undefined && limit !== null && limit !== '') {
      limit = Number(limit);
      if (!Number.isFinite(limit) || limit < 1) {
        throw Object.assign(new Error(`kline: invalid limit "${p.limit}" (must be >= 1)`), { exitCode: 1 });
      }
      limit = Math.min(Math.floor(limit), 300); // 服务端上限 300
    }
    return {
      url: `${API6_KLINE}?${qs({
        chainId: requireParam(p, 'chainId', 'kline'),
        contractAddress: requireParam(p, 'contractAddress', 'kline'),
        interval,
        ...(limit !== undefined ? { limit } : {}),
        startTime: p.startTime,
        endTime: p.endTime,
      })}`,
    };
  },
};

const COMMAND_DESC = {
  'symbol-list': 'list all tokenized stocks (params: {type?} type=1 Ondo)',
  meta: 'tokenized stock metadata / company info (params: chainId, contractAddress)',
  'market-status': 'overall Ondo market open/close state (no params)',
  'asset-status': 'per-asset trading status & corporate actions (params: chainId, contractAddress)',
  dynamic: 'real-time on-chain data + US stock fundamentals (params: chainId, contractAddress)',
  kline: 'token K-Line candles (params: chainId, contractAddress, interval, limit?)',
};

export { COMMANDS, call, qs, UA, TIMEOUT_MS, API1_SYMBOL_LIST };

function isDirectExecution() {
  if (!process.argv[1]) return false;
  try {
    return realpathSync(fileURLToPath(import.meta.url)) === realpathSync(process.argv[1]);
  } catch {
    return false;
  }
}

if (isDirectExecution()) {
  const [cmd, paramsStr] = process.argv.slice(2);

  if (!cmd || cmd === '--help' || cmd === '-h') {
    console.log("Usage: node cli.mjs <command> '<json_params>'\n\nCommands:");
    for (const [name, desc] of Object.entries(COMMAND_DESC)) console.log(`  ${name.padEnd(14)} ${desc}`);
    process.exit(0);
  }

  const builder = COMMANDS[cmd];
  if (!builder) { console.error(`Unknown command: ${cmd}\nRun with --help to see available commands.`); process.exit(1); }

  let params = {};
  if (paramsStr) {
    try { params = JSON.parse(paramsStr); }
    catch { console.error('Invalid JSON params'); process.exit(1); }
  }

  try {
    const result = await call(builder(params));
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error(err.message);
    if (err.body) console.log(JSON.stringify(err.body, null, 2));
    process.exit(err.exitCode || 1);
  }
}
