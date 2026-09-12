#!/usr/bin/env node
// coin-report CLI — 标准代币研报生成（零依赖，Node >= 18）
// 用法: node cli.mjs report <SYMBOL> [market=futures]
// 数据：本机后端 /api/market/*（K线/费率/OI/多空/恐惧贪婪/追踪战绩）
// 产出：workspace/妖币/<SYMBOL>_研报_<YYYYMMDD-HHmm>.md；stdout 输出路径 + 摘要

import process from "node:process";
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

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
const usd = (v) => {
  if (v == null) return "—";
  const a = Math.abs(v);
  if (a >= 1e9) return `$${(v / 1e9).toFixed(2)}B`;
  if (a >= 1e6) return `$${(v / 1e6).toFixed(2)}M`;
  if (a >= 1e3) return `$${(v / 1e3).toFixed(1)}K`;
  return `$${v.toFixed(2)}`;
};

async function report(rest) {
  const [sym0, mkt0] = rest;
  if (!sym0) throw Object.assign(new Error("report: 需要 SYMBOL"), { exitCode: 1 });
  // 已带常见计价后缀（含中文展示名代币如 牛来USDT）则原样；否则补 USDT
  const sym = /(USDT|USDC|FDUSD|TUSD|BUSD|TRY|BRL)$/i.test(sym0)
    ? sym0.toUpperCase() : `${sym0.toUpperCase()}USDT`;
  const market = mkt0 === "spot" ? "spot" : "futures";
  const enc = encodeURIComponent;

  const [k90, k24, fngD] = await Promise.all([
    jget(`/market/klines?symbol=${enc(sym)}&interval=1d&limit=90&market=${market}`),
    jget(`/market/klines?symbol=${enc(sym)}&interval=1h&limit=25&market=${market}`),
    jget("/market/fng"),
  ]);
  const closes = k90.closes || [];
  if (closes.length < 10) throw Object.assign(new Error(`report: ${sym} 90d K线数据不足（${closes.length} 根）`), { exitCode: 1 });
  const last = closes[closes.length - 1];
  const mn = Math.min(...closes), mx = Math.max(...closes);
  const s = {
    price: num(last),
    chg_24h: pct(last, (k24.closes || [])[0] || last),
    chg_7d: pct(last, closes[Math.max(0, closes.length - 8)]),
    chg_30d: pct(last, closes[Math.max(0, closes.length - 31)]),
    range_90d: [num(mn), num(mx)],
    pos_in_range: Number((((last - mn) / (mx - mn || 1)) * 100).toFixed(1)),
    pct_below: Number(((closes.filter((c) => c <= last).length / closes.length) * 100).toFixed(0)),
    from_90d_high: pct(last, mx), from_90d_low: pct(last, mn),
  };

  let funding_rate = null, oi = null, longshort = null;
  if (market === "futures") {
    const [fs, ls, oiD] = await Promise.all([jget("/market/futures"), jget("/market/longshort"), jget(`/market/oi?symbols=${enc(sym)}`)]);
    const row = (fs.futures || []).find((r) => r.symbol === sym);
    if (row) funding_rate = row.funding_rate;
    const l = (ls.rows || []).find((r) => r.symbol === sym);
    if (l) longshort = { top_ratio: l.top_ratio, global_ratio: l.global_ratio, divergence: l.divergence };
    const it = (oiD.items || [])[0];
    if (it) oi = { oi: num(it.oi, 10), notional_usd: it.notional != null ? num(it.notional, 8) : null };
  }

  let track = null;
  try {
    const tr = await jget("/market/radar/tracks");
    const hit = [...(tr.pending || []), ...(tr.history || [])].filter((r) => r.symbol === sym)
      .sort((a, b) => (b.updated_at || 0) - (a.updated_at || 0))[0];
    if (hit) track = { status: hit.status, outcome: hit.outcome || "—", found_price: num(hit.found_price),
                       max_gain_pct: hit.max_gain_pct, max_drop_pct: hit.max_drop_pct,
                       found_at: hit.found_at ? new Date(hit.found_at * 1000).toISOString().slice(0, 16).replace("T", " ") : "—" };
  } catch { /* 追踪不可用不阻塞报告 */ }

  const now = new Date();
  const stamp = now.toISOString().slice(0, 16).replace("T", " ");
  const f = (v, suf = "") => (v == null ? "—" : `${v}${suf}`);
  const md = `# ${sym} 研报 · ${stamp}

> 自动生成 by coin-report（数据：本机行情后端，market=${market}）。
> 「结论与计划」由分析 agent 填写，必须区分 **事实**（上文数字）与 **推测**（判断）。

## 一、快照（事实）
- 现价：**${s.price}** USDT
- 24h：${f(s.chg_24h, "%")} ｜ 7d：${f(s.chg_7d, "%")} ｜ 30d：${f(s.chg_30d, "%")}

## 二、90 日结构（事实）
- 区间：${s.range_90d[0]} — ${s.range_90d[1]}
- 区间位置：**${s.pos_in_range}%**（<33% 低位 / >66% 高位）
- 收盘分位：**${s.pct_below}%**（90 天里收在现价之下的占比）
- 距 90d 高点：${f(s.from_90d_high, "%")} ｜ 距 90d 低点：${f(s.from_90d_low, "%")}

## 三、衍生品（事实，${market === "futures" ? "U 本位永续" : "现货无此项"}）
- 资金费率：${funding_rate == null ? "—" : `${(funding_rate * 100).toFixed(4)}% / 8h`}
- 持仓量 OI：${oi ? `${oi.oi} 枚（名义 ${usd(oi.notional_usd)}）` : "—"}
- 大户多空比：${longshort ? `${longshort.top_ratio ?? "—"}（全球 ${longshort.global_ratio ?? "—"}${longshort.divergence ? "，⚠️ 背离" : ""}）` : "—"}

## 四、市场环境（事实）
- 恐惧贪婪指数：${fngD.value ?? "—"}（${fngD.classification ?? "—"}）

## 五、妖币追踪战绩${track ? "（事实）" : ""}
${track ? `- 状态：${track.status}（结局：${track.outcome}）；发现价 ${track.found_price}（${track.found_at}）；最大涨幅 ${f(track.max_gain_pct, "%")} / 最大回撤 ${f(track.max_drop_pct, "%")}` : "该币不在追踪记录中。"}

## 六、结论与计划（由 agent 填写）
- 趋势方向（事实依据 → 判断）：
- 关键位：支撑 / 阻力：
- 入场思路（含触发条件）：
- 失效条件（作废价）：
- 风险提示：
`;
  const dir = join(process.cwd(), "妖币");
  mkdirSync(dir, { recursive: true });
  const file = join(dir, `${sym}_研报_${stamp.replace(/[- :]/g, "").slice(0, 12)}.md`);
  writeFileSync(file, md, "utf8");
  return { report: file, summary: { ...s, funding_rate, oi, longshort, fng: fngD.value, track } };
}

const [cmd0, ...rest0] = process.argv.slice(2);
// 兼容裸 SYMBOL（如 `cli.mjs WLDUSDT`）—— 技能页预设与 agent 常省略 "report" 前缀。
// 注意：裸 SYMBOL 时 cmd0 本身就是标的，必须挪进 rest，否则 report 收到空参数报"需要 SYMBOL"。
const bare = cmd0 !== "report" && !!(cmd0 || "").trim() && /^[A-Z0-9]{2,20}(USDT|USDC|BUSD|FDUSD|TRY|BRL)?$/i.test(cmd0);
const cmd = cmd0 === "report" || !(cmd0 || "").trim() || bare ? "report" : cmd0;
if (cmd !== "report") {
  console.log(JSON.stringify({ error: cmd0 ? `未知命令 "${cmd0}"` : "用法: report <SYMBOL> [market=futures]", available: ["report"] }));
  process.exit(1);
}
report(bare ? [cmd0, ...rest0] : rest0)
  .then((out) => console.log(JSON.stringify(out)))
  .catch((e) => { console.log(JSON.stringify({ error: e?.message || String(e) })); process.exit(e?.exitCode || 1); });
