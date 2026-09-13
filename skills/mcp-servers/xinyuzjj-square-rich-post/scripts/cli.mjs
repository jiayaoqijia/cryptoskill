#!/usr/bin/env node
// square-rich-post 统一入口：合成（后端 /api/square/rich/compose）→ 发布（square-post cli.mjs）
//
// 用法：
//   node cli.mjs <SYMBOL> [market=futures]            # 只合成，打印产物路径与摘要
//   node cli.mjs <SYMBOL> [market] --publish          # 短贴多图发布：封面+24h图+全文（默认）
//   node cli.mjs <SYMBOL> [market] --publish --article # 长文+封面（contentType=2）
//   node cli.mjs <SYMBOL> [market] --publish --reuse <dir>   # 复用已合成目录（改稿后重发）
//
// 合成走本机后端（进程内 scanner 数据 + Pillow 画图）；发布走 square-post 技能
// （image --title-file --cover --text-file），密钥由 square-post 自行读取。

import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SQUARE_POST_CLI = path.join(__dirname, "..", "..", "square-post", "scripts", "cli.mjs");

const PORTS = [process.env.BAZZ_PORT || "8080", "8081"];
const TIMEOUT_MS = 120_000;   // 冷缓存首扫（futures_snapshot/多空板）可能 30s+

function usageExit(msg) {
  if (msg) console.error(`Error: ${msg}\n`);
  console.error(`Usage: node cli.mjs <SYMBOL> [market=futures] [--publish] [--reuse <dir>]`);
  process.exit(1);
}

async function backendGet(pathname) {
  let lastErr, httpErr;
  for (const port of PORTS) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
    try {
      const headers = {};
      if (process.env.BAZZ_AUTH_TOKEN) headers["X-BAZZ-Token"] = process.env.BAZZ_AUTH_TOKEN;
      const res = await fetch(`http://127.0.0.1:${port}/api${pathname}`, { headers, signal: ctrl.signal });
      clearTimeout(timer);
      const json = await res.json().catch(() => ({}));
      if (res.ok) return json;
      httpErr = new Error(`HTTP ${res.status}: ${json.error || res.statusText}`);   // 有明确响应：优先上报
      lastErr = httpErr;
    } catch (e) {
      clearTimeout(timer);
      lastErr = e;
    }
  }
  throw httpErr || lastErr;   // 401/500 等业务错误优先于连接错误
}

async function compose(sym, market) {
  const q = `symbol=${encodeURIComponent(sym)}&market=${encodeURIComponent(market)}`;
  const out = await backendGet(`/square/rich/compose?${q}`);
  if (!out || out.ok !== true) {
    throw new Error(out?.error || "compose 失败（后端不可达或数据不足）");
  }
  return out;
}

function printSummary(meta) {
  const s = meta.stats || {};
  const pct = (v) => (v == null ? "-" : `${Number(v) >= 0 ? "+" : ""}${Number(v).toFixed(2)}%`);
  console.log(`已合成 → ${meta.dir}`);
  console.log(`封面图: ${meta.cover}`);
  if (meta.extra_chart) console.log(`24h 图: ${meta.extra_chart}`);
  console.log(`标题: ${fs.readFileSync(meta.title_file, "utf8").trim()}`);
  console.log(`统计: 现价 ${s.price ?? "-"} | 90d ${pct(s.chg90)} | 24h ${pct(s.chg24)}` +
    (s.funding_rate != null ? ` | 费率 ${(s.funding_rate * 100).toFixed(4)}%` : "") +
    (s.oi ? ` | OI ${s.oi}` : "") + (s.fng?.value != null ? ` | 恐惧贪婪 ${s.fng.value}` : ""));
  if (meta.tags?.length) console.log(`标签: ${meta.tags.join(" ")}`);
}

async function main() {
  const argv = process.argv.slice(2);
  const publish = argv.includes("--publish");
  const ri = argv.indexOf("--reuse");
  const reuse = ri !== -1 ? argv[ri + 1] : undefined;
  // 位置参数 = 不带 -- 的 token（--reuse 的取值除外）
  const pos = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      if (argv[i] === "--reuse") i++;
      continue;
    }
    pos.push(argv[i]);
  }
  const sym = (pos[0] || "").toUpperCase();
  const market = pos[1] === "spot" ? "spot" : "futures";
  if (!sym) usageExit("缺少 SYMBOL（如 RAYUSDT）");

  let meta;
  if (reuse) {
    // v1.5.21：相对/被吞反斜杠的路径兜底锚定 workspace（技能执行 cwd 不一定在安装根）
    let rdir = reuse;
    const tried = [rdir];
    if (!fs.existsSync(path.join(rdir, "article.txt"))) {
      const ws = process.env.BAZZ_WORKSPACE || "";
      const cands = [];
      if (ws) cands.push(path.join(ws, rdir));
      const base = path.basename(rdir);
      if (base && base !== rdir) { if (ws) cands.push(path.join(ws, "square_rich", base)); cands.push(path.join("workspace", "square_rich", base)); }
      for (const c of cands) {
        tried.push(c);
        if (fs.existsSync(path.join(c, "article.txt"))) { rdir = c; break; }
      }
    }
    if (!fs.existsSync(path.join(rdir, "article.txt"))) usageExit(`--reuse 目录无效: ${reuse}（尝试过: ${tried.join(" , ")}；也可传绝对路径并保留反斜杠）`);
    let saved = {};
    try { saved = JSON.parse(fs.readFileSync(path.join(rdir, "meta.json"), "utf8")); } catch { }
    meta = {
      dir: rdir, title_file: path.join(rdir, "title.txt"), text_file: path.join(rdir, "article.txt"),
      cover: path.join(rdir, "cover.png"), tags: saved.tags || [], stats: saved.stats || {},
    };
  } else {
    meta = await compose(sym, market);
  }
  printSummary(meta);

  if (!publish) {
    console.log("\n(预览模式：加 --publish 发布到广场)");
    return;
  }

  // 发布（v1.5.22 默认短贴多图：contentType=1，封面+24h 图最多 4 张，正文里能看到图）；
  // --article 走长文+封面（contentType=2，OpenAPI 不支持正文插图）
  let res;
  if (argv.includes("--article")) {
    res = spawnSync(process.execPath, [SQUARE_POST_CLI, "image",
      "--title-file", meta.title_file, "--cover", meta.cover, "--text-file", meta.text_file,
    ], { encoding: "utf8", timeout: 240_000, maxBuffer: 16 * 1024 * 1024 });
  } else {
    const imgs = [meta.cover, path.join(meta.dir, "chart_24h.png"), path.join(meta.dir, "chart_4h.png")]
      .filter((p, i, a) => p && fs.existsSync(p) && a.indexOf(p) === i)
      .slice(0, 4);
    if (!imgs.length) usageExit("短贴至少需要 1 张图（cover.png / chart_24h.png）");
    const bodyText = fs.readFileSync(meta.text_file, "utf8").trim();
    const titleTxt = fs.existsSync(meta.title_file) ? fs.readFileSync(meta.title_file, "utf8").trim() : "";
    const body = titleTxt ? `${titleTxt}\n\n${bodyText}` : bodyText;
    res = spawnSync(process.execPath, [SQUARE_POST_CLI, "image", "--text", body, "--images", imgs.join(",")],
      { encoding: "utf8", timeout: 240_000, maxBuffer: 16 * 1024 * 1024 });
  }
  if (res.stdout) process.stdout.write(res.stdout);
  if (res.stderr) process.stderr.write(res.stderr);
  process.exit(res.status ?? 1);
}

main().catch((e) => {
  console.error(`Failed: ${e.message}`);
  process.exit(1);
});
