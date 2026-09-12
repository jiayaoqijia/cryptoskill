#!/usr/bin/env node
// market-data CLI — 本地行情后端网关（零依赖，Node >= 18）
// 数据源：本机 BAZZ.AGENT 后端 /api/market/*（后端自带 5min 缓存 + 代理池出口）
// 用法: node cli.mjs <command> [args...]
//   klines <SYMBOL> [interval=1h] [limit=24] [market=spot]
//   bundle <SYMBOL> [market=futures]
//   fng
//   funding [SYM[,SYM...]]        ← v1.5.31 新增（此前描述宣传 funding 却无此命令）
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

  // v1.5.31 新增：资金费率查询。
  // 此前 SKILL.md 的 description 把「资金费率 / funding」列为触发词，但 CLI 并无该子命令，
  // 模型据此调用 `market-data funding BTCUSDT` 只会得到「未知命令」。资金费率当时只在
  // bundle 里出现过 —— 为了拿单个币的费率要跑完整个分析包（90d K线 + 24h + FNG + OI + 多空比），
  // 代价过高且容易超时。
  async funding(rest) {
    const syms = (rest.join(",") || "").split(",").map((s) => s.trim().toUpperCase()).filter(Boolean);
    const d = await jget("/market/futures");
    const rows = d.futures || [];
    const pick = (r) => {
      const fr = Number(r.funding_rate || 0);
      return {
        symbol: r.symbol, price: num(r.price), change_pct: r.change_pct,
        funding_rate: num(fr, 6),
        funding_pct_8h: Number((fr * 100).toFixed(4)),          // 每 8 小时费率（百分比）
        annualized_pct: Number((fr * 3 * 365 * 100).toFixed(2)), // 年化（百分比）
        quote_volume: num(r.quote_volume, 8),
      };
    };
    if (syms.length) {
      const bySym = new Map(rows.map((r) => [r.symbol, r]));
      const items = syms.filter((s) => bySym.has(s)).map((s) => pick(bySym.get(s)));
      const missing = syms.filter((s) => !bySym.has(s));
      if (!items.length) {
        throw Object.assign(new Error(
          `funding: 未找到 ${syms.join(",")} 的 USDT 永续合约。` +
          `现货没有资金费率，现货标的请改用 bundle <SYM> spot；也可能是符号拼写错误或合约已下架`),
          { exitCode: 1 });
      }
      const out = { items };
      if (missing.length) out.missing = missing;
      out.note = "funding_pct_8h >0.05 多头拥挤 / <-0.05 空头拥挤；annualized_pct 为年化";
      return out;
    }
    // 无参数：返回资金费率两端极值（谁在多付钱）
    const ranked = rows.slice().sort((a, b) => Number(b.funding_rate || 0) - Number(a.funding_rate || 0));
    return {
      long_crowded: ranked.slice(0, 10).map(pick),
      short_crowded: ranked.slice(-10).reverse().map(pick),
      total: rows.length,
      note: "long_crowded = 费率最高 10 个（多头付费、多头拥挤）；short_crowded = 费率最低 10 个（空头拥挤）",
    };
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
  // v1.5.31：只回 available 列表不足以纠正 —— 模型常把 description 里的「名词」
  // 直接当子命令用（典型就是 funding）。这里把最可能的替代写法点出来。
  console.log(JSON.stringify({
    error: `未知命令 "${cmd}"`,
    available: Object.keys(CMDS),
    hint: "资金费率用 `funding <SYM>`（单个，或逗号分隔多个）或 `bundle <SYM>`（完整分析包）；" +
          "K线用 `klines <SYM> [interval] [limit] [market]`；恐惧贪婪用 `fng`；" +
          "持仓量用 `oi <SYM,...>`；爆仓用 `liq [SYM]`。",
  }));
  process.exit(1);
}
fn(rest)
  .then((out) => console.log(JSON.stringify(out)))
  .catch((e) => { console.log(JSON.stringify({ error: e?.message || String(e) })); process.exit(e?.exitCode || 1); });
