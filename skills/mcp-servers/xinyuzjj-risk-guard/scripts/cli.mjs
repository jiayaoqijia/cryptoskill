#!/usr/bin/env node
// risk-guard CLI — 下单前风险护栏（零依赖，Node >= 18）
// 用法:
//   node cli.mjs plan <capitalUsd> <riskPct> <entry> <stop> [lev=1]
//   node cli.mjs check [symbol]
// 数据：本机后端 /api/wallet/cex/*（只读）、/api/orders/track

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

function plan(rest) {
  const [capital0, risk0, entry0, stop0, lev0] = rest;
  const capital = Number(capital0), riskPct = Number(risk0), entry = Number(entry0), stop = Number(stop0), lev = Math.max(1, Number(lev0) || 1);
  if (!isFinite(capital) || capital <= 0) throw Object.assign(new Error("plan: capitalUsd 无效"), { exitCode: 1 });
  if (!isFinite(riskPct) || riskPct <= 0 || riskPct > 10) throw Object.assign(new Error("plan: riskPct 无效（0 < risk ≤ 10）"), { exitCode: 1 });
  if (!isFinite(entry) || entry <= 0 || !isFinite(stop) || stop <= 0 || stop === entry)
    throw Object.assign(new Error("plan: entry/stop 无效或相等"), { exitCode: 1 });

  const riskUsd = capital * riskPct / 100;
  const stopDistPct = Number((Math.abs(entry - stop) / entry * 100).toFixed(3));
  const qty = riskUsd / Math.abs(entry - stop);
  const notional = qty * entry;
  const margin = notional / lev;
  const liqEstPct = Number((100 / lev).toFixed(2));

  const warnings = [];
  if (riskPct > 2) warnings.push(`单笔风险 ${riskPct}% 偏高（建议 ≤1%，激进 ≤2%）`);
  if (lev > 1 && stopDistPct >= liqEstPct) warnings.push(`止损距离 ${stopDistPct}% ≥ 强平估算 ${liqEstPct}%（lev=${lev}）：止损前可能已接近强平，降低杠杆或收紧仓位`);
  if (lev > 20) warnings.push(`杠杆 ${lev}x 过高，多数场景不建议`);
  if (stopDistPct < 0.5) warnings.push(`止损距离仅 ${stopDistPct}%，极易被插针扫掉，考虑放宽止损或减仓`);

  return { input: { capital_usd: capital, risk_pct: riskPct, entry, stop, leverage: lev },
           risk_usd: Number(riskUsd.toFixed(2)), stop_dist_pct: stopDistPct,
           qty: num(qty, 8), notional_usd: num(notional, 4), margin_usd: num(margin, 2),
           liq_est_pct: lev > 1 ? liqEstPct : null, warnings };
}

async function check(rest) {
  const sym = (rest[0] || "").toUpperCase();
  const enc = encodeURIComponent;
  const out = {};
  for (const [key, path] of [
    ["summary", "/wallet/cex/summary"],
    ["open_orders", `/wallet/cex/openorders${sym ? `?symbol=${enc(sym)}` : ""}`],
    ["tracked_orders", "/orders/track"],
  ]) {
    try { out[key] = await jget(path); }
    catch (e) { out[key] = { error: e?.message || String(e) }; }
  }
  const s = out.summary;
  if (s && (s.error || s.status === "error" || s.code === "not_configured")) out.hint = "CEX 未连接或请求失败：先在「Binance CEX」页连接只读 API Key 再查敞口。";
  // 压缩输出体积
  const cut = (v, n = 2600) => { const t = JSON.stringify(v); return t && t.length > n ? { truncated: t.slice(0, n) } : v; };
  return { symbol: sym || null, summary: cut(s), open_orders: cut(out.open_orders), tracked_orders: cut(out.tracked_orders), hint: out.hint ?? null };
}

const [cmd, ...rest] = process.argv.slice(2);
const fn = cmd === "plan" ? () => plan(rest) : cmd === "check" ? () => check(rest) : null;
if (!fn) {
  console.log(JSON.stringify({ error: cmd ? `未知命令 "${cmd}"` : "用法: plan ... | check [symbol]", available: ["plan", "check"] }));
  process.exit(1);
}
Promise.resolve(fn())
  .then((out) => console.log(JSON.stringify(out)))
  .catch((e) => { console.log(JSON.stringify({ error: e?.message || String(e) })); process.exit(e?.exitCode || 1); });
