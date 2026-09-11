#!/usr/bin/env node
// news-sentiment CLI — 加密新闻抓取 + 关键词情绪统计（零依赖，Node >= 18，零 Key）
// 源：PANews flash（中文快讯）、CoinDesk RSS、Cointelegraph RSS（英文头条）
// 用法: node cli.mjs <command> [args...]
//   latest [n=20]        混合最新新闻
//   coin <SYM> [n=15]    按币种过滤
//   sentiment [n=40]     看多/看空/中性 统计 + 代表标题 + 高频币种

import process from "node:process";

const TIMEOUT_MS = 15_000;
const UA = { "User-Agent": "Mozilla/5.0 (BAZZ-AGENT news-sentiment)" };

async function raw(url) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, { headers: UA, signal: ctrl.signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.text();
  } finally { clearTimeout(timer); }
}

/* ---------------- 源适配 ---------------- */

async function fromPANews() {
  const txt = await raw("https://api.panewslab.com/newsweb/v1/flashlist?language=cn");
  const d = JSON.parse(txt);
  const list = d?.data?.list || d?.data?.List || d?.data || [];
  return (Array.isArray(list) ? list : []).slice(0, 40).map((x) => ({
    title: String(x.title || x.Content || x.content || "").replace(/<[^>]+>/g, "").trim().slice(0, 160),
    source: "PANews",
    ts: num(x.time || x.PublishTime || x.publish_time),
  }));
}

async function fromRSS(url, source) {
  const xml = await raw(url);
  const items = [...xml.matchAll(/<item>([\s\S]*?)<\/item>/gi)].slice(0, 30);
  return items.map((m) => {
    const b = m[1];
    const pick = (tag) => { const r = b.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`, "i")); return r ? r[1].trim() : ""; };
    const title = pick("title").replace(/<!\[CDATA\[|\]\]>/g, "").replace(/<[^>]+>/g, "").slice(0, 160);
    const ts = Date.parse(pick("pubDate") || pick("published") || "") || 0;
    return { title, source, ts };
  });
}

const SOURCES = [
  { name: "PANews", fn: fromPANews },
  { name: "CoinDesk", fn: () => fromRSS("https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml", "CoinDesk") },
  { name: "Cointelegraph", fn: () => fromRSS("https://cointelegraph.com/rss", "Cointelegraph") },
];

async function fetchAll() {
  const rs = await Promise.allSettled(SOURCES.map((s) => s.fn()));
  const items = []; const failed = [];
  rs.forEach((r, i) => {
    if (r.status === "fulfilled") items.push(...r.value.filter((x) => x.title));
    else failed.push(SOURCES[i].name);
  });
  // 去重（同标题）+ 新→旧
  const seen = new Set();
  const uniq = items.filter((x) => { const k = x.title.toLowerCase(); if (seen.has(k)) return false; seen.add(k); return true; })
    .sort((a, b) => (b.ts || 0) - (a.ts || 0));
  return { items: uniq, failed };
}

/* ---------------- 情绪（关键词启发式） ---------------- */

const BULL = ["涨", "突破", "利好", "看多", "买入", "增持", "上涨", "新高", "反弹", "飙升", "流入", "获批", "上线",
  "bullish", "surge", "rally", "gain", "soar", "jump", "record", "inflow", "adopt", "approve", "upgrade", "breakout", "all-time"];
const BEAR = ["跌", "暴跌", "崩", "利空", "看空", "卖出", "抛售", "清算", "爆仓", "下跌", "新低", "流出", "被查", "盗",
  "bearish", "plunge", "crash", "dump", "liquidat", "hack", "exploit", "lawsuit", "ban", "sell-off", "selloff", "outflow", "decline", "fraud"];

function hitWord(text, word) {
  const w = word.toLowerCase();
  if (/[\u4e00-\u9fff]/.test(w)) return text.includes(w);          // 中文按子串
  return new RegExp(`\\b${w.replace(/[^a-z-]/g, "\\$&")}`, "i").test(text); // 英文按词边界（前缀）
}

const COIN_MAP = {
  BTC: ["bitcoin", "比特币"], ETH: ["ethereum", "以太"], SOL: ["solana"], BNB: [], XRP: ["ripple", "瑞波"],
  DOGE: ["dogecoin", "狗狗"], ADA: ["cardano"], LINK: ["chainlink"], TON: ["toncoin"], TRX: ["tron", "波场"],
  WLD: ["worldcoin"], RAY: ["raydium"], PEPE: [], SUI: [], AVAX: ["avalanche"], DOT: ["polkadot", "波卡"],
};

function score(title) {
  const s = title.toLowerCase();
  const b = BULL.filter((w) => hitWord(s, w)).length;
  const r = BEAR.filter((w) => hitWord(s, w)).length;
  return b > r ? "bull" : r > b ? "bear" : "neutral";
}

function matchCoin(title, sym) {
  const s = title.toLowerCase();
  if (hitWord(s, sym)) return true;
  for (const alias of (COIN_MAP[sym.toUpperCase()] || [])) if (hitWord(s, alias)) return true;
  return false;
}

function coinsIn(title) {
  const s = title.toLowerCase(); const out = [];
  for (const sym of Object.keys(COIN_MAP)) {
    if (hitWord(s, sym) || (COIN_MAP[sym] || []).some((a) => hitWord(s, a))) out.push(sym);
  }
  return out;
}

const num = (v) => { const n = Number(v); return isFinite(n) && n > 0 ? n : 0; };
const fmtT = (ts) => (ts ? new Date(ts).toLocaleString("zh-CN", { hour12: false }) : "—");

async function getItems() {
  const { items, failed } = await fetchAll();
  if (!items.length) throw Object.assign(new Error(`全部新闻源失败${failed.length ? `（${failed.join(", ")}）` : ""}，请检查网络/代理`), { exitCode: 3 });
  return { items, failed };
}

const CMDS = {
  async latest(rest) {
    const n = Math.max(1, Math.min(60, parseInt(rest[0] || "20", 10) || 20));
    const { items, failed } = await getItems();
    return { count: Math.min(n, items.length), failed_sources: failed,
             items: items.slice(0, n).map((x) => ({ title: x.title, source: x.source, time: fmtT(x.ts), sentiment: score(x.title), coins: coinsIn(x.title) })) };
  },

  async coin(rest) {
    const sym = String(rest[0] || "").toUpperCase().replace(/USDT$/, "");
    if (!sym) throw Object.assign(new Error("coin: 需要 SYMBOL，如 coin BTC"), { exitCode: 1 });
    const n = Math.max(1, Math.min(40, parseInt(rest[1] || "15", 10) || 15));
    const { items, failed } = await getItems();
    const hit = items.filter((x) => matchCoin(x.title, sym));
    return { symbol: sym, count: hit.length, failed_sources: failed,
             items: hit.slice(0, n).map((x) => ({ title: x.title, source: x.source, time: fmtT(x.ts), sentiment: score(x.title) })) };
  },

  async sentiment(rest) {
    const n = Math.max(10, Math.min(100, parseInt(rest[0] || "40", 10) || 40));
    const { items, failed } = await getItems();
    const sample = items.slice(0, n);
    let bull = 0, bear = 0, neutral = 0;
    const freq = new Map();
    const bullEx = [], bearEx = [];
    for (const x of sample) {
      const s = score(x.title);
      if (s === "bull") { bull++; if (bullEx.length < 3) bullEx.push(x.title); }
      else if (s === "bear") { bear++; if (bearEx.length < 3) bearEx.push(x.title); }
      else neutral++;
      for (const c of coinsIn(x.title)) freq.set(c, (freq.get(c) || 0) + 1);
    }
    const total = sample.length;
    return {
      sample: total, failed_sources: failed,
      bull_pct: Math.round((bull / total) * 100), bear_pct: Math.round((bear / total) * 100),
      neutral_pct: Math.round((neutral / total) * 100),
      bias: bull > bear * 1.5 ? "偏多" : bear > bull * 1.5 ? "偏空" : "均衡",
      bull_examples: bullEx, bear_examples: bearEx,
      top_coins: [...freq.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8).map(([sym, c]) => ({ symbol: sym, mentions: c })),
      note: "关键词启发式，粗粒度参考，非投资建议",
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
  .catch((e) => { console.error(`[news-sentiment] ${e.message}`); process.exit(e?.exitCode || 1); });
