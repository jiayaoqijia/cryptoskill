#!/usr/bin/env node
// track-monitor CLI — 妖币追踪定时复查（零依赖，Node >= 18）
// 用法: node cli.mjs check [threshold_pct=15]
// 数据：本机后端 /api/market/radar/tracks + /api/market/klines（逐币现价）

import process from "node:process";

const TIMEOUT_MS = 60_000;  // 后端冷缓存首扫可达 30s+
const PORTS = [process.env.BAZZ_PORT || "8080", "8081"];
const H = {};
if (process.env.BAZZ_AUTH_TOKEN) H["X-BAZZ-Token"] = process.env.BAZZ_AUTH_TOKEN;

async function jget(path) {
  const errs = [];
  for (const port of PORTS) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
    try {
      const res = await fetch(`http://127.0.0.1:${port}/api${path}`, { headers: H, signal: ctrl.signal });
      clearTimeout(timer);
      if (res.ok) return await res.json();
      // 非 200（401/404/5xx）也可能是「该端口被别的带鉴权服务占用」——换下一端口再试
      errs.push(`:${port} HTTP ${res.status}: ${(await res.text()).slice(0, 120)}`);
    } catch (e) {
      clearTimeout(timer);
      errs.push(`:${port} ${e.message}`);
    }
  }
  // v1.5.30：逐端口错误全部保留。旧实现只留最后一个（通常是未监听端口的连接错误），
  // 会把真正的原因（如 :8080 HTTP 401 令牌缺失）掩盖成「不可达」，极难排查。
  throw Object.assign(
    new Error(`本地后端不可达(${PORTS.join("/")}) — ${errs.join(" | ")}`),
    { exitCode: 3 });
}

const num = (v, d = 6) => (v == null || !isFinite(Number(v)) ? null : Number(Number(v).toPrecision(d)));

async function check(rest) {
  const th = Math.abs(Number(rest[0]) || 15);
  const tr = await jget("/market/radar/tracks");
  const pending = tr.pending || [];
  const enc = encodeURIComponent;

  const rows = await Promise.all(pending.map(async (r) => {
    let now = null;
    try {
      const k = await jget(`/market/klines?symbol=${enc(r.symbol)}&interval=1h&limit=1&market=spot`);
      now = (k.closes || [])[0] ?? null;
    } catch { /* 单币失败不阻塞整体 */ }
    const chg = now && r.found_price ? Number((((now - r.found_price) / r.found_price) * 100).toFixed(2)) : null;
    return {
      symbol: r.symbol, stage: r.stage, found_price: num(r.found_price), now: num(now),
      chg_pct: chg, max_gain_pct: r.max_gain_pct, max_drop_pct: r.max_drop_pct,
      found_ago_h: r.found_at ? Number(((Date.now() / 1000 - r.found_at) / 3600).toFixed(1)) : null,
      alert: chg == null ? null : chg >= th ? "moon" : chg <= -th ? "dump" : null,
    };
  }));
  rows.sort((a, b) => Math.abs(b.chg_pct ?? 0) - Math.abs(a.chg_pct ?? 0));
  return { threshold_pct: th, summary: { pending: pending.length, alerts: rows.filter((r) => r.alert).length }, rows };
}

const [cmd, ...rest] = process.argv.slice(2);
if (cmd !== "check") {
  console.log(JSON.stringify({ error: cmd ? `未知命令 "${cmd}"` : "用法: check [threshold_pct=15]", available: ["check"] }));
  process.exit(1);
}
check(rest)
  .then((out) => console.log(JSON.stringify(out)))
  .catch((e) => { console.log(JSON.stringify({ error: e?.message || String(e) })); process.exit(e?.exitCode || 1); });
