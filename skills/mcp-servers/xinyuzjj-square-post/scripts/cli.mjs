#!/usr/bin/env node
// square-post 统一执行入口（桌面 Agent 技能桥）
//
// 币安官方 square-post 只有 post-text/post-image/post-video 三个底层脚本，
// 没有 Agent 习惯的 cli.mjs 入口。本文件补上这一层：按内容类型分发到底层脚本，
// 使 exec_sandbox.run_skill_cmd / skills_client.run_skill 都能真实发布到币安广场。
//
// 用法（首个位置参数为类型，其余参数原样透传到底层脚本）：
//   node cli.mjs text --text "内容" [--title "标题"]
//   node cli.mjs image --text "内容" --images a.png,b.png        # 图文
//   node cli.mjs image --title "标题" --cover c.png --text "内容" # 文章+封面
//   node cli.mjs video --video x.mp4 [--duration 12] [--text "内容"]
//   node cli.mjs "纯文本内容"                                    # 省略 type → 短文
//
// 不传 --video/--images/--cover 时自动按 title 有无选择 文章/短文。
// 密钥只从 BINANCE_SQUARE_OPENAPI_KEY 或 ~/.config/binance-square/openapi-key 读取，
// 绝不接受命令行传 key。

import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SCRIPTS = {
  text: "post-text.mjs",
  image: "post-image.mjs",
  video: "post-video.mjs",
};

const USAGE = `Usage: node cli.mjs <text|image|video> [args...]

  text   --text <内容> [--title <标题>]          短文 / 文章（有 title 即文章）
  image  --text <内容> --images <a.png,b.png>    图文短文（≤4 图）
         --title <标题> --cover <图> --text <内容>  文章 + 封面
  video  --video <文件> [--duration <秒>] [--text <内容>]
  省略类型时也可直接 node cli.mjs "正文内容"

密钥读取顺序：BINANCE_SQUARE_OPENAPI_KEY → ~/.config/binance-square/openapi-key`;

function usageExit(msg) {
  if (msg) console.error(`Error: ${msg}\n`);
  console.error(USAGE);
  process.exit(1);
}

function hasFlag(args, name) {
  return args.includes(`--${name}`) || args.some((a) => a.startsWith(`--${name}=`));
}

function detectKind(tokens) {
  // 显式类型
  const first = (tokens[0] || "").toLowerCase();
  if (first === "text" || first === "article" || first === "image" || first === "video") {
    if (first === "article") return "text"; // article = 带 title 的 text
    return first;
  }
  // 隐式：按携带的媒体参数推断
  if (hasFlag(tokens, "video")) return "video";
  if (hasFlag(tokens, "images") || hasFlag(tokens, "cover")) return "image";
  return "text"; // 纯文本（含 --title 文章也走 text 脚本）
}

function pickFlag(tokens, name) {
  const i = tokens.indexOf(`--${name}`);
  if (i !== -1 && i + 1 < tokens.length) return tokens[i + 1];
  const pref = tokens.find((t) => t.startsWith(`--${name}=`));
  if (pref) return pref.slice(name.length + 3);
  return undefined;
}

// --text-file <path> / --title-file <path>：从文件读正文/标题，替换为 --text/--title。
// 长文（多段落、含引号/换行）经命令行传参极易被 shlex/引号解析冲掉，走文件最稳。
function resolveFileFlags(tokens) {
  const out = [];
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i];
    let flag = "", inline = "";
    if (t === "--text-file" || t === "--title-file") {
      flag = t.slice(2, -5); // text / title
      if (i + 1 >= tokens.length) usageExit(`--${flag}-file 缺少文件路径`);
      inline = tokens[++i];
    } else if (t.startsWith("--text-file=") || t.startsWith("--title-file=")) {
      flag = t.slice(2, t.indexOf("=") - 5);
      inline = t.slice(t.indexOf("=") + 1);
    } else {
      out.push(t);
      continue;
    }
    let content = "";
    try {
      content = fs.readFileSync(inline, "utf8").trim();
    } catch (e) {
      usageExit(`读取 --${flag}-file 失败: ${inline} (${e.message})`);
    }
    if (!content) usageExit(`--${flag}-file 文件为空: ${inline}`);
    out.push(`--${flag}`, content);
  }
  return out;
}

const argv = process.argv.slice(2);
const help = argv.includes("--help") || argv.includes("-h");
if (help || argv.length === 0) usageExit(help ? undefined : "缺少内容与类型（发空帖会被币安拒绝）");

// 自动探测 ffprobe 时长（video 未给 --duration 时）
function probeDuration(file) {
  const r = spawnSync("ffprobe", [
    "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", file,
  ], { encoding: "utf8" });
  if (r.status !== 0 || !r.stdout) return null;
  const sec = parseFloat(r.stdout.trim());
  return Number.isFinite(sec) && sec > 0 ? Math.round(sec) : null;
}

// 处理 "node cli.mjs 正文" 的省略类型快捷方式
let tokens = [...argv];
let kind = detectKind(tokens);
if (kind === "text") {
  const first = (tokens[0] || "").toLowerCase();
  const known = new Set(["text", "article", "image", "video"]);
  if (!known.has(first)) {
    // 无类型词 + 无 --text → 把整个首个参数当正文
    if (!hasFlag(tokens, "text") && tokens.length > 0 && !tokens[0].startsWith("--")) {
      tokens = ["--text", tokens.join(" ").trim()];
    }
  } else {
    tokens = tokens.slice(1); // 去掉类型词，纯透传底层脚本
  }
} else {
  tokens = tokens.slice(1);
}

// 长文本走文件：--text-file/--title-file → --text/--title（在 --text 必填检查前解析）
tokens = resolveFileFlags(tokens);

if (!hasFlag(tokens, "text") && kind !== "video") {
  // text/image 必须有正文；video 的 --text 可选
  usageExit(`${kind} 类型缺少 --text 正文`);
}

if (kind === "video" && !hasFlag(tokens, "video")) {
  usageExit("video 类型缺少 --video <文件路径>");
}
if (kind === "video" && !hasFlag(tokens, "duration")) {
  const videoPath = pickFlag(tokens, "video");
  if (videoPath && fs.existsSync(videoPath)) {
    const sec = probeDuration(videoPath);
    if (sec) tokens = tokens.concat(["--duration", String(sec)]);
  }
}

const script = path.join(__dirname, SCRIPTS[kind]);
if (!fs.existsSync(script)) usageExit(`找不到底层脚本 ${SCRIPTS[kind]}`);

// Windows：node 已可直接执行 .mjs（本脚本自身即 node 运行），spawn 原样转发参数
const res = spawnSync(process.execPath, [script, ...tokens], { encoding: "utf8" });
if (res.stdout) process.stdout.write(res.stdout);
if (res.stderr) process.stderr.write(res.stderr);
process.exit(res.status ?? 1);
