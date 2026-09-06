#!/usr/bin/env node
// Freqtrade REST API client — shared helper.
//
// 在 CoinClaw 三引擎(OpenClaw / Hermes / Claude Code)容器里,
// freqtrade 是 supervisord 管的常驻 daemon 跑在 :8080, Basic auth
// 用户名 'freqtrade', 密码写在容器内的 .ft_api_pass 文件 (PVC 持久化).
// 这个 helper 自动从那里读 — agent / skill 不需要在 .env 里再配
// FREQTRADE_USERNAME / FREQTRADE_PASSWORD. 用户也可以通过 .env 覆盖.
//
// 在容器外(用户本地 macOS / Linux), 退到 .env 里读 — 走老的 host 模式,
// ft-deploy.mjs deploy 时把 FREQTRADE_PASSWORD 写到 .env.
import { readFileSync, existsSync } from 'node:fs';
import { coinclawEnv, readFtApiPass, envFileCandidates } from './coinclaw-env.mjs';

// Auto-load .env files (CoinClaw 容器优先 /workspace/.env 或 OpenClaw 的等价路径).
function loadEnv() {
  for (const file of envFileCandidates()) {
    if (!existsSync(file)) continue;
    try {
      for (const line of readFileSync(file, 'utf-8').split('\n')) {
        const t = line.trim();
        if (!t || t.startsWith('#')) continue;
        const eq = t.indexOf('=');
        if (eq < 1) continue;
        const key = t.slice(0, eq).trim();
        let val = t.slice(eq + 1).trim();
        if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) val = val.slice(1, -1);
        if (!process.env[key]) process.env[key] = val;
      }
    } catch {}
  }
}
loadEnv();

const env = coinclawEnv();

// 优先级有两条路径:
//   - CoinClaw 容器内 (env 非空): 信 daemon 真实密码 (.ft_api_pass 文件
//     + 容器 entrypoint 注入的 FT_API_USER), 完全忽略 .env 里的
//     FREQTRADE_USERNAME/PASSWORD. 后者可能是早期 ft-deploy.mjs deploy
//     流程 appendEnv 写的过时值, daemon 重启后密码会变, .env 没跟新 →
//     401. 端到端测试在 OpenClaw pod 重现过这个 bug.
//   - host 模式 (env=null): 信用户的 .env 配置, 因为本地 freqtrade 不是
//     supervisord 管的, 没有 .ft_api_pass 文件这个权威来源.
let BASE, USER, PASS;
if (env) {
  BASE = env.ftApiUrl;
  USER = env.ftApiUser;
  PASS = readFtApiPass(env) || '';
} else {
  BASE = process.env.FREQTRADE_URL || 'http://localhost:8080';
  USER = process.env.FREQTRADE_USERNAME || 'freqtrade';
  PASS = process.env.FREQTRADE_PASSWORD || '';
}

const auth = 'Basic ' + Buffer.from(`${USER}:${PASS}`).toString('base64');

export async function ftGet(path, params = {}) {
  const url = new URL(`/api/v1/${path}`, BASE);
  for (const [k, v] of Object.entries(params)) {
    if (v != null) url.searchParams.set(k, String(v));
  }
  const res = await fetch(url, { headers: { Authorization: auth }, signal: AbortSignal.timeout(30000) });
  if (!res.ok) throw new Error(`Freqtrade ${res.status}: ${await res.text()}`);
  return res.json();
}

export async function ftPost(path, body = {}) {
  const res = await fetch(new URL(`/api/v1/${path}`, BASE), {
    method: 'POST',
    headers: { Authorization: auth, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(30000),
  });
  if (!res.ok) throw new Error(`Freqtrade ${res.status}: ${await res.text()}`);
  return res.json();
}

export async function ftDelete(path) {
  const res = await fetch(new URL(`/api/v1/${path}`, BASE), {
    method: 'DELETE',
    headers: { Authorization: auth },
    signal: AbortSignal.timeout(30000),
  });
  if (!res.ok) throw new Error(`Freqtrade ${res.status}: ${await res.text()}`);
  return res.json();
}

// CLI helper
export function ftCli(handlers) {
  const [action, ...rest] = process.argv.slice(2);
  if (!action || !handlers[action]) {
    console.log(`Usage: node <script> <action> [json-params]\nActions: ${Object.keys(handlers).join(', ')}`);
    process.exit(1);
  }
  let params = {};
  if (rest.length) {
    try {
      params = JSON.parse(rest.join(' '));
    } catch {
      console.log(JSON.stringify({ error: '参数不是合法 JSON: ' + rest.join(' '), hint: "参数要用 JSON 对象, 例: '{\"strategy\":\"MyStrat\"}'" }));
      process.exit(1);
    }
  }
  handlers[action](params).then(r => console.log(JSON.stringify(r, null, 2))).catch(e => {
    console.error(e.message); process.exit(1);
  });
}
