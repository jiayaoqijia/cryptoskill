#!/usr/bin/env node
// market-data CLI — 本地行情后端网关（零依赖，Node >= 18）
// 数据源：本机 BAZZ.AGENT 后端 /api/market/*（后端自带 5min 缓存 + 代理池出口）
// 用法: node cli.mjs <command> [args...]
//   klines <SYMBOL> [interval=1h] [limit=24] [market=spot]
//   bundle <SYMBOL> [market=futures]
//   fng
//   oi <SYM[,SYM...]>
//   longshort [SYMBOL]
//   liq [SYMBOL] [limit=60] [window=300]
//   overview

import process from "node:process";

const TIMEOUT_MS = 60_000;  // 后端冷缓存首扫（全市场快照/雷达）可达 30s+，10s 必超时
const PORTS = [process.env.BAZZ_PORT || "8080", "8081"];
const H = {};
if (process.env.BAZZ_AUTH_TOKEN) H["X-BAZZ-Token"] = process.env.BAZZ_AUTH_TOKEN;

async function jget(path) {
  let lastErr;
  for (const port of PORTS) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
    try {
      const res = await fetch(`http://127.0.0.1:${port}/api${path}`, { headers: H, signal: ctrl.signal });
      clearTimeout(timer);
      if (res.ok) return await res.json();
      // 非 200（401/404/5xx）也可能是「该端口被别的带鉴权服务占用」——换下一端口再试
      lastErr = new Error(`HTTP ${res.status}: ${(await res.text()).slice(0, 160)}`);
    } catch (e) {
      clearTimeout(timer);
      lastErr = e;
    }
  }
  throw Object.assign(new Error(`本地后端不可达(${PORTS.join("/")}): ${lastErr?.message || lastErr}`), { exitCode: 3 });
}

const num = (v, d = 6) => (v == null || !isFinite(Number(v)) ? null : Number(Number(v).toPrecision(d)));
const pct = (a, b) => (a && b ? Number((((a - b) / b) * 100).toFixed(2)) : null);

function kstat(closes) {
  if (!Array.isArray(closes) || closes.length < 2) return { n: closes?.length || 0, note: "数据不足" };
  const first = closes[0], last = closes[closes.length - 1];
  return {
    n: closes.length, first: num(first), last: num(last), chg_pct: pct(last, first),
    min: num(Math.min(...closes)), max: num(Math.max(...closes)),
    pos_in_range: Number((((last - Math.min(...closes)) / (Math.max(...closes) - Math.min(...closes) || 1)) * 100).toFixed(1)),
    pct_below: Number(((closes.filter((c) => c <= last).length / closes.length) * 100).toFixed(0)),
  };
}

const enc = encodeURIComponent;

const CMDS = {
  async klines(rest) {
    const [sym, interval = "1h", limit = "24", market = "spot"] = rest;
    if (!sym) throw Object.assign(new Error("klines: 需要 SYMBOL"), { exitCode: 1 });
    const d = await jget(`/market/klines?symbol=${enc(sym.toUpperCase())}&interval=${interval}&limit=${limit}&market=${market}`);
    const closes = (d.closes || []).map((c) => num(c));
    // v1.5.21：空数据直接报错退出（此前返回 n:0 的 OK，模型把垃圾参数当成功继续跑）
    if (!closes.length) {
      throw Object.assign(new Error(
        `klines: ${sym.toUpperCase()} 无数据（interval=${interval} market=${market}）。` +
        `检查符号拼写、interval 合法值（1h/4h/1d 等）与 market（spot/futures）；合约下架币试试 spot`),
        { exitCode: 1 });
    }
    return { symbol: sym.toUpperCase(), interval, market, stat: kstat(d.closes), closes };
  },

  async fng() {
    const d = await jget("/market/fng");
    return { value: d.value, classification: d.classification,
             history: (d.history || []).map((h) => h.value) };
  },

  async oi(rest) {
    const syms = (rest.join(",") || "").split(",").map((s) => s.trim().toUpperCase()).filter(Boolean);
    if (!syms.length) throw Object.assign(new Error("oi: 需要 SYMBOL 列表，如 BTCUSDT,ETHUSDT"), { exitCode: 1 });
    const d = await jget(`/market/oi?symbols=${enc(syms.join(","))}`);
    return { items: (d.items || []).map((it) => ({ symbol: it.symbol, oi: num(it.oi, 10), price: num(it.price), notional_usd: it.notional != null ? num(it.notional, 8) : null })) };
  },

  async longshort(rest) {
    const d = await jget("/market/longshort");
    const pick = (r) => ({ symbol: r.symbol, price: num(r.price), change_pct: r.change_pct,
                           top_ratio: r.top_ratio, global_ratio: r.global_ratio, divergence: r.divergence });
    const sym = (rest[0] || "").toUpperCase();
    const rows = (d.rows || []).filter((r) => !sym || r.symbol === sym).map(pick);
    return { rows: rows.slice(0, sym ? 5 : 40), total: (d.rows || []).length };
  },

  async liq(rest) {
    const [sym, limit = "60", window = "300"] = rest;
    const d = await jget(`/market/liquidations?limit=${limit}&window=${window}`);
    const f = (sym || "").toUpperCase();
    return {
      stats: d.stats || null,
      recent: (d.recent || []).filter((r) => !f || r.symbol === f)
        .map((r) => ({ ago_s: Math.max(0, Math.round(Date.now() / 1000 - r.ts)), symbol: r.symbol,
                       kind: r.kind, price: num(r.price), quote_usd: num(r.quote, 6) })).slice(0, 60),
    };
  },

  async overview() {
    const d = await jget("/market/overview");
    return {
      breadth: d.breadth || null,
      funding_extremes: (d.funding?.extremes ?? d.funding?.long_crowded ?? []).slice(0, 8)
        .map((r) => ({ symbol: r.symbol, funding_rate: r.funding_rate, change_pct: r.change_pct, crowded: r.crowded, extreme: r.extreme })),
      flips: (d.funding?.flips ?? []).slice(0, 8),
      volume_top: (d.volume_top ?? []).slice(0, 10).map((r) => ({ symbol: r.symbol, price: num(r.price), change_pct: r.change_pct, quote_usd: num(r.quote_volume, 8) })),
    };
  },

  async bundle(rest) {
    const [sym0, mkt0] = rest;
    if (!sym0) throw Object.assign(new Error("bundle: 需要 SYMBOL"), { exitCode: 1 });
    const sym = sym0.toUpperCase();
    const market = mkt0 === "spot" ? "spot" : "futures";
    const [k90, k24, fngD] = await Promise.all([
      jget(`/market/klines?symbol=${enc(sym)}&interval=1d&limit=90&market=${market}`),
      jget(`/market/klines?symbol=${enc(sym)}&interval=1h&limit=25&market=${market}`),
      jget("/market/fng"),
    ]);
    const out = { symbol: sym, market, d90: kstat(k90.closes), h24: kstat(k24.closes),
                  fng: { value: fngD.value, classification: fngD.classification } };
    if (market === "futures") {
      const [fs, ls, oiD] = await Promise.all([jget("/market/futures"), jget("/market/longshort"), jget(`/market/oi?symbols=${enc(sym)}`)]);
      const row = (fs.futures || []).find((r) => r.symbol === sym);
      if (row) out.funding_rate = row.funding_rate;
      const l = (ls.rows || []).find((r) => r.symbol === sym);
      if (l) out.longshort = { top_ratio: l.top_ratio, global_ratio: l.global_ratio, divergence: l.divergence };
      const it = (oiD.items || [])[0];
      if (it) out.oi = { oi: num(it.oi, 10), notional_usd: it.notional != null ? num(it.notional, 8) : null };
    }
    return out;
  },
};

const [cmd, ...rest] = process.argv.slice(2);
const fn = CMDS[cmd];
if (!fn) {
  console.log(JSON.stringify({ error: `未知命令 "${cmd}"`, available: Object.keys(CMDS) }));
  process.exit(1);
}
fn(rest)
  .then((out) => console.log(JSON.stringify(out)))
  .catch((e) => { console.log(JSON.stringify({ error: e?.message || String(e) })); process.exit(e?.exitCode || 1); });
