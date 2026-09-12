#!/usr/bin/env node
// portfolio-review CLI — 资产快照 + 周期复盘（零依赖，Node >= 18）
// 数据源：本机 BAZZ.AGENT 后端 /api/wallet/cex/*、/api/orders/track（只读）
// 用法: node cli.mjs <command> [args...]
//   snap            资产快照（余额 TOP + 总估值）
//   week [days=7]   复盘统计 + 写 Markdown 周报到 复盘/资产周报_*.md

import process from "node:process";
import fs from "node:fs";
import path from "node:path";

const TIMEOUT_MS = 60_000;  // 后端冷缓存（CEX 快照/成交聚合）可能较慢
const PORTS = [process.env.BAZZ_PORT || "8080", "8081"];
const H = {};
if (process.env.BAZZ_AUTH_TOKEN) H["X-BAZZ-Token"] = process.env.BAZZ_AUTH_TOKEN;

async function jget(pathname) {
  const errs = [];
  for (const port of PORTS) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
    try {
      const res = await fetch(`http://127.0.0.1:${port}/api${pathname}`, { headers: H, signal: ctrl.signal });
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

const num = (v) => { const n = Number(v); return isFinite(n) ? n : 0; };
const fmtU = (v) => `$${num(v).toLocaleString("en-US", { maximumFractionDigits: 2 })}`;
const fmtT = (ts) => new Date(Number(ts)).toLocaleString("zh-CN", { hour12: false });

async function getSummary() {
  const d = await jget("/wallet/cex/summary");
  if (d?.status === "error" || d?.configured === false) {
    throw Object.assign(new Error(`CEX 未连接：${d.message || "请先在「设置 → 币安 CEX」连接 API Key"}`), { exitCode: 1, code: d.code });
  }
  return d;
}

async function getTrades(limit = 200) {
  const d = await jget(`/wallet/cex/trades?limit=${limit}`);
  if (d?.status === "error") {
    throw Object.assign(new Error(`成交记录获取失败：${d.message || d.code}`), { exitCode: 1, code: d.code });
  }
  return Array.isArray(d?.trades) ? d.trades : [];
}

const CMDS = {
  async snap() {
    const d = await getSummary();
    const rows = (d.balances || d.holdings || [])
      .map((b) => ({ asset: b.asset ?? b.coin, free: num(b.free ?? b.available), locked: num(b.locked ?? b.frozen),
                     usdt: num(b.usdt ?? b.value_usdt), no_pair: b.no_usdt_pair === true }))
      .sort((a, b) => b.usdt - a.usdt);
    const total = num(d.total_usdt ?? rows.reduce((s, r) => s + r.usdt, 0));
    return {
      total_usdt: total,
      updated_at: d.updated_at ?? d.ts ?? null,
      holdings: rows.slice(0, 15),
      holdings_count: rows.length,
      note: rows.length > 15 ? `仅显示估值前 15 / 共 ${rows.length} 项` : undefined,
    };
  },

  async week(rest) {
    const days = Math.max(1, Math.min(90, parseInt(rest[0] || "7", 10) || 7));
    const [sum, trades] = await Promise.all([getSummary(), getTrades(200)]);
    const since = Date.now() - days * 86_400_000;
    const recent = trades.filter((t) => num(t.time) >= since);

    // 分币种聚合
    const bySym = new Map();
    let buyN = 0, sellN = 0, buyQ = 0, sellQ = 0;
    for (const t of recent) {
      const sym = t.symbol || "?";
      const q = num(t.quoteQty ?? (num(t.price) * num(t.qty)));
      const isBuy = t.isBuyer === true || String(t.side || "").toUpperCase() === "BUY";
      const m = bySym.get(sym) || { symbol: sym, buy_n: 0, sell_n: 0, buy_quote: 0, sell_quote: 0 };
      if (isBuy) { m.buy_n++; m.buy_quote += q; buyN++; buyQ += q; }
      else { m.sell_n++; m.sell_quote += q; sellN++; sellQ += q; }
      bySym.set(sym, m);
    }
    const perSym = [...bySym.values()]
      .map((m) => ({ ...m, net_quote: m.buy_quote - m.sell_quote, trades: m.buy_n + m.sell_n }))
      .sort((a, b) => (a.buy_quote + a.sell_quote) > (b.buy_quote + b.sell_quote) ? -1 : 1);

    // 挂单 / 订单跟踪概况（失败不阻塞报告）
    let open = { open_orders: null, tracked: null };
    try {
      const oo = await jget("/wallet/cex/openorders");
      open.open_orders = Array.isArray(oo?.orders) ? oo.orders.length : (oo?.total ?? null);
    } catch { /* ignore */ }
    try {
      const ot = await jget("/orders/track");
      const rows = ot?.rows ?? ot?.orders ?? ot?.items ?? (Array.isArray(ot) ? ot : []);
      open.tracked = Array.isArray(rows) ? rows.length : null;
    } catch { /* ignore */ }

    const total_usdt = num(sum.total_usdt ?? 0);
    const ts = new Date();
    const stamp = ts.toISOString().slice(0, 10);
    const dir = path.resolve("复盘");
    fs.mkdirSync(dir, { recursive: true });
    const file = path.join(dir, `资产周报_${stamp}.md`);
    const L = [];
    L.push(`# 资产周报（近 ${days} 天）`, "");
    L.push(`- 生成时间：${ts.toLocaleString("zh-CN", { hour12: false })}`);
    L.push(`- 当前总估值：${fmtU(total_usdt)}`);
    if (open.open_orders != null) L.push(`- 当前挂单：${open.open_orders} 笔`);
    if (open.tracked != null) L.push(`- 订单跟踪：${open.tracked} 条`, "");
    L.push(`## 成交统计（近 ${days} 天）`, "");
    L.push(`| 指标 | 数值 |`, `|---|---|`);
    L.push(`| 成交笔数 | ${recent.length}（买 ${buyN} / 卖 ${sellN}）|`);
    L.push(`| 买入金额 | ${fmtU(buyQ)} |`);
    L.push(`| 卖出金额 | ${fmtU(sellQ)} |`);
    L.push(`| 净流向（买-卖）| ${fmtU(buyQ - sellQ)} |`, "");
    if (perSym.length) {
      L.push(`## 分币种明细`, "", `| 交易对 | 笔数 | 买入 | 卖出 | 净流向 |`, `|---|---|---|---|---|`);
      for (const m of perSym.slice(0, 15)) {
        L.push(`| ${m.symbol} | ${m.trades} | ${fmtU(m.buy_quote)} | ${fmtU(m.sell_quote)} | ${fmtU(m.net_quote)} |`);
      }
      if (perSym.length > 15) L.push(`| … 共 ${perSym.length} 个交易对 | | | | |`);
      L.push("", `最近一笔成交：${recent.length ? fmtT(recent[0].time) : "—"}`);
    } else {
      L.push(`近 ${days} 天无成交记录。`);
    }
    L.push("", "## 分析与建议", "", "（由 Agent 基于以上事实填写）", "");
    fs.writeFileSync(file, L.join("\n"), "utf8");
    return {
      days, report_file: file, total_usdt,
      trades: recent.length, buy_n: buyN, sell_n: sellN,
      buy_quote: Number(buyQ.toFixed(2)), sell_quote: Number(sellQ.toFixed(2)),
      net_quote: Number((buyQ - sellQ).toFixed(2)),
      per_symbol: perSym.slice(0, 10), open_orders: open.open_orders, tracked: open.tracked,
    };
  },
};

const [cmd, ...rest] = process.argv.slice(2);
const fn = CMDS[cmd];
if (!fn) {
  console.error(`未知命令 ${cmd || "(空)"}。可用: ${Object.keys(CMDS).join(" | ")}`);
  process.exit(1);
}
fn(rest).then((out) => { console.log(JSON.stringify(out, null, 2)); })
  .catch((e) => { console.error(`[portfolio-review] ${e.message}`); process.exit(e?.exitCode || 1); });
