#!/usr/bin/env node
// query-token-audit CLI — self-contained, zero-dep, Node >= 22
// Usage: node cli.mjs <command> '<json_params>'
//
// Commands:
//   audit   Token security audit — detect honeypot / rug-pull / scam / malicious
//           functions BEFORE trading.  (POST bapi token/audit)
//
// audit params: { binanceChainId, contractAddress }
//   binanceChainId: "1"(Ethereum) | "56"(BSC) | "8453"(Base) | "CT_501"(Solana)
//   contractAddress: 要审计的代币合约地址
//   requestId: 可选，默认由本 CLI 自动生成 UUID v4（每次请求必须唯一）
//   兼容别名: chainId → binanceChainId
//
// Windows 直跑判定用 realpath 比较（官方 `file://` + argv[1] 拼接在反斜杠路径下必失败），
// 因此本脚本可被 import 也可被 node 直接执行。

import { realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { randomUUID } from 'node:crypto';

const TIMEOUT_MS = 15_000;
const AUDIT_URL = 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/security/token/audit';
const UA = {
  'Accept-Encoding': 'identity',
  'User-Agent': 'binance-web3/1.4 (Skill)',
  'source': 'agent',
};
const CHAIN_HINT = { '1': 'Ethereum', '56': 'BSC', '8453': 'Base', CT_501: 'Solana' };

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

// ---- commands: (params) => { url, method?, body?, headers? } ----
const COMMANDS = {
  audit: (p) => {
    const binanceChainId = p.binanceChainId ?? p.chainId; // 兼容别名
    const chain = requireParam({ binanceChainId }, 'binanceChainId', 'audit');
    const contractAddress = requireParam(p, 'contractAddress', 'audit');
    if (!(chain in CHAIN_HINT)) {
      throw Object.assign(
        new Error(`audit: unsupported binanceChainId "${chain}". Supported: 1(Ethereum), 56(BSC), 8453(Base), CT_501(Solana)`),
        { exitCode: 1 },
      );
    }
    return {
      url: AUDIT_URL,
      method: 'POST',
      body: {
        binanceChainId: chain,
        contractAddress,
        requestId: p.requestId || randomUUID(),
      },
    };
  },
};

export { COMMANDS, call, AUDIT_URL, UA };

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
    console.log("  audit   token security audit (params: binanceChainId|chainId, contractAddress)");
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
