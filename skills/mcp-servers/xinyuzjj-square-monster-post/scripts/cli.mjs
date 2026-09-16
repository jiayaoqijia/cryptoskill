#!/usr/bin/env node
// square-monster-post 统一入口：合成（后端 /api/square/monster/compose）→ 发布（square-post cli.mjs）
//
// 与 square-rich-post 的关系：**同样的命令形态，不同的分析引擎**。
// rich = 代币引擎（SMC：结构/BOS・CHoCH/OB/FVG），monster = 妖币引擎（位阶/控盘/燃料）。
// 这条分叉是刻意的：妖币是控盘盘，K 线结构是画出来的，用 SMC 分析等于拿散户的地图找庄家的门。
//
// 用法：
//   node cli.mjs <SYMBOL> [market=futures]              # 只合成，打印产物路径与本币位阶/合议结论
//   node cli.mjs <SYMBOL> [market] --publish            # 短贴多图：封面+竖版剧本卡+全文（默认）
//   node cli.mjs <SYMBOL> [market] --publish --article  # 长文+封面（contentType=2）
//   node cli.mjs <SYMBOL> [market] --publish --reuse <dir>  # 复用已合成目录（改稿后重发）

import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SQUARE_POST_CLI = path.join(__dirname, "..", "..", "square-post", "scripts", "cli.mjs");

const PORTS = [process.env.BAZZ_PORT || "8080", "8081"];
const TIMEOUT_MS = 180_000;   // 妖币引擎要等雷达全量扫描（冷缓存首扫可能 30s+）

function usageExit(msg) {
  if (msg) console.error(`Error: ${msg}\n`);
  console.error(`Usage: node cli.mjs <SYMBOL> [market=futures] [--publish] [--article] [--reuse <dir>]`);
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
      httpErr = new Error(`HTTP ${res.status}: ${json.error || res.statusText}`);
      lastErr = httpErr;
    } catch (e) {
      clearTimeout(timer);
      lastErr = e;
    }
  }
  throw httpErr || lastErr;
}

async function compose(sym, market) {
  const q = `symbol=${encodeURIComponent(sym)}&market=${encodeURIComponent(market)}`;
  const out = await backendGet(`/square/monster/compose?${q}`);
  if (!out || out.ok !== true) {
    throw new Error(out?.error || "compose 失败（后端不可达、数据不足，或该币不在妖币雷达视野内）");
  }
  return out;
}

function printSummary(meta) {
  const s = meta.stats || {};
  const pct = (v) => (v == null ? "-" : `${Number(v) >= 0 ? "+" : ""}${Number(v).toFixed(2)}%`);
  console.log(`已合成 → ${meta.dir}`);
  console.log(`封面图: ${meta.cover}`);
  if (meta.extra_chart) console.log(`剧本卡: ${meta.extra_chart}`);
  console.log(`标题: ${fs.readFileSync(meta.title_file, "utf8").trim()}`);
  // 妖币引擎的核心读数：位阶 / 控盘 / 燃料 / 合议结论。这四个是发出去之前该看的。
  console.log(`位阶: ${s.stage_label ?? "-"}${s.stage_seq != null ? `（第 ${s.stage_seq + 1}/7 格）` : "（旁支）"}` +
    ` | 控盘: ${s.control ?? "-"}` + (s.control_flags?.length ? `（${s.control_flags.join("/")}）` : "") +
    ` | 燃料: ${s.fuel ?? "-"}`);
  console.log(`合议: ${s.verdict_label ?? "-"}` +
    (s.late ? " ⚠️ 已晚" : "") + (s.warm ? " · 暖启动" : ""));
  console.log(`统计: 现价 ${s.price ?? "-"} | 24h ${pct(s.chg24)} | 雷达分 ${s.score ?? "-"}`);
  if (s.missing?.length) console.log(`⚠️ 数据缺失（稿中已如实标注）: ${s.missing.join("；")}`);
  if (meta.plan) {
    console.log(`计划: 只做多 · 入场 ${meta.plan.entry} / 止损 ${meta.plan.stop}（−${meta.plan.stop_pct}%）/ 止盈目标 ${meta.plan.tp}`);
  } else {
    console.log("计划: 本次不给点位（位阶不在允许进场的窗口）");
  }
  if (meta.tags?.length) console.log(`标签: ${meta.tags.join(" ")}`);
}

async function main() {
  const argv = process.argv.slice(2);
  const publish = argv.includes("--publish");
  const ri = argv.indexOf("--reuse");
  const reuse = ri !== -1 ? argv[ri + 1] : undefined;
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
  if (!sym) usageExit("缺少 SYMBOL（如 RAVEUSDT）");

  let meta;
  if (reuse) {
    let rdir = reuse;
    const tried = [rdir];
    if (!fs.existsSync(path.join(rdir, "article.txt"))) {
      const ws = process.env.BAZZ_WORKSPACE || "";
      const cands = [];
      if (ws) cands.push(path.join(ws, rdir));
      const base = path.basename(rdir);
      if (base && base !== rdir) {
        if (ws) cands.push(path.join(ws, "square_monster", base));
        cands.push(path.join("workspace", "square_monster", base));
      }
      for (const c of cands) {
        tried.push(c);
        if (fs.existsSync(path.join(c, "article.txt"))) { rdir = c; break; }
      }
    }
    if (!fs.existsSync(path.join(rdir, "article.txt"))) usageExit(`--reuse 目录无效: ${reuse}（尝试过: ${tried.join(" , ")}）`);
    let saved = {};
    try { saved = JSON.parse(fs.readFileSync(path.join(rdir, "meta.json"), "utf8")); } catch { }
    meta = {
      dir: rdir, title_file: path.join(rdir, "title.txt"), text_file: path.join(rdir, "article.txt"),
      cover: path.join(rdir, "cover.png"), extra_chart: path.join(rdir, "chart_playbook.png"),
      tags: saved.tags || [], stats: saved.stats || {}, plan: saved.plan || null,
    };
  } else {
    meta = await compose(sym, market);
  }
  printSummary(meta);

  if (!publish) {
    console.log("\n(预览模式：加 --publish 发布到广场)");
    return;
  }

  let res;
  if (argv.includes("--article")) {
    res = spawnSync(process.execPath, [SQUARE_POST_CLI, "image",
      "--title-file", meta.title_file, "--cover", meta.cover, "--text-file", meta.text_file,
    ], { encoding: "utf8", timeout: 240_000, maxBuffer: 16 * 1024 * 1024 });
  } else {
    const imgs = [meta.cover, meta.extra_chart]
      .filter((p, i, a) => p && fs.existsSync(p) && a.indexOf(p) === i)
      .slice(0, 4);
    if (!imgs.length) usageExit("短贴至少需要 1 张图（cover.png）");
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
