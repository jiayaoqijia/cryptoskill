<!--
  Imported from: https://github.com/rollysys/use_cninfo
  Source Path: skill/SKILL.md
  Status: Upstream repo (rollysys/use_cninfo) removed/private as of 2026-11; retained as local archived mirror.
  Curated for awesome-quant-skills
-->

---
name: cninfo
description: 按需抓取 A 股上市公司公告。覆盖巨潮资讯网(cninfo.com.cn)所有 category(年报/季报/中报/三季报/临时公告/减持/重组等),输出 PDF + PyMuPDF 提取的全文 Markdown,并可选用 announcement_filter 做精准类目分类。命中本地缓存时秒级返回。当用户说"年报 / 季报 / 半年报 / 中报 / 三季报 / 公告 / 临时公告 / 巨潮 / cninfo / 披露 / 减持 / 重大资产重组"等触发本 skill。
---

# cninfo skill — A 股公告按需抓取

本 skill 是对 `cninfo-cli` 命令的入口,把巨潮资讯网的所有公开公告(法定披露)按需变成本地 PDF + 全文 md。**纯按需,不做后台调度**。

## 触发场景

- "拿 600519 的 2024 年报"
- "茅台 2024 年第一季度报告"
- "贵州茅台最近 30 天的公告"
- "4/29 全市场所有年报"
- "搜含'减持'的公告 / 找重大资产重组类公告"

## 前置依赖(用户机器上必须先装好)

> 注意：原上游仓库已于 2026-11 下线/转私，此处完整保留本地归档 SKILL.md 供离线参考与历史溯源。

```bash
# 1. 本工具
git clone https://github.com/rollysys/use_cninfo.git
cd use_cninfo && uv tool install -e .            # 装上 `cninfo` 命令

# 2. (可选)公告分类器 — 提供 search 的 --type/--sub-type 标签精准过滤
git clone https://github.com/rollysys/announcement_filter.git
cd announcement_filter && pip install -e .
```

不装 announcement_filter 时:`cninfo search --type ... --sub-type ...` 会报错并提示安装命令;其它 5 个命令不受影响。

## 缓存

默认 `~/.cache/cninfo/`(可被 `$CNINFO_CACHE_DIR` 覆盖):

```
<root>/
├── orgid_map.json                                    # secCode → orgId
├── pdf/<ts_code>/<ann_date>__<ann_id>.pdf
├── md/<ts_code>/<ann_date>__<ann_id>.md              # 含 YAML frontmatter
└── meta/<ann_id>.json
```

**命中即秒级返回**,不发网络。强制重下用 `--force`。

## 6 个命令(给 agent 自己选)

### 1. 单股指定定期报告(最常用)

```bash
cninfo fetch-report 600519 --year 2024 --kind annual
# kind: annual / q1 / h1 / q3
# 输出 JSON: {ann_id, ann_date, title, pdf_path, md_path, total_pages, extracted_pages, text_chars, cache_hit}
```

板块(sz/sh/bj)默认按代码推测;把握不准时显式 `--plate sh`。

### 2. 单股时间窗全公告

```bash
cninfo fetch-stock 600519 --since 2024-04-01 --until 2024-04-30          # 仅列表
cninfo fetch-stock 600519 --since 2024-04-01 --until 2024-04-30 --download  # 同时落 PDF+md
cninfo fetch-stock 600519 --since 2024-04-01 --until 2024-04-30 --json      # JSON 输出
```

### 3. 全市场切片

```bash
# 4/29 当天 sz plate 全部年报
cninfo list --plate sz --category annual --date 2024-04-29
# 时间窗 + 单只关键词
cninfo list --plate sh --since 2024-04-01 --until 2024-04-30 --keyword "重大资产重组"
# 加 --download 才下载;--limit 50 限制条数
```

### 4. 标签搜索(走 announcement_filter)

```bash
# 单股 + 时间窗 + 标签
cninfo search --stock 600519 --since 2024-01-01 --until 2024-12-31 \
              --type shareholder --sub-type reduce_plan
# 全市场 + 单日 + 标签
cninfo search --plate sz --date 2024-04-29 --type shareholder --sub-type reduce_plan
# 不带标签时退化为 cninfo searchkey 模糊匹配 title
cninfo search --plate sh --date 2024-04-29 --keyword "重组"
```

`--type` / `--sub-type` 取值见 `announcement_filter` 的 ontology(11 大类 / 82 子类)。

### 5. 缓存管理

```bash
cninfo cache stats                       # 命中率/占用空间(JSON)
cninfo cache verify                      # 检查 pdf/md/meta 三件套一致性
cninfo cache prune --older-than 365d     # 删 365 天前的条目
```

### 6. orgId 辅助

```bash
cninfo orgid 600519                      # cache 命中即返回,缺失自动回源
cninfo orgid 600519 --refresh            # 强制重拉
cninfo orgid 600519 --cache-only         # 只查 cache,不回源
```

## 给 Agent 的小贴士

- **优先 `fetch-report`** 而不是 `fetch-stock --download` — 前者只下一个 PDF,几秒就好;后者会下整个时间窗内所有附件,可能几十个。
- **未指定 `--plate` 时** 我们按代码首位推测(0/3=sz, 6=sh, 4/8=bj)。极少数 ST 股 / 老代码可能猜错,显式传 `--plate` 最稳。
- **全市场切片有 pageSize=30 硬限**,翻页自动跑;`--limit 50` 等显式限流可省请求。
- **PDF 是扫描件时** `extracted_pages=0`,正文 md 是空的,但 PDF 本身已落盘 — 用户可以自己跑 OCR。
- **agent 拿到 md_path 后**:用 Read 工具读全文,文件含 YAML frontmatter + 正文。100+ 页年报会比较大,精读时建议先 head/grep 关键章节。

## 不做的事

- **不做后台增量同步 / 全量回补** — 那是另一种架构,本 skill 故意只覆盖按需场景
- **不做本地全文检索** — 想搜全文用 `grep -r ~/.cache/cninfo/md/` 即可
- **不做 OCR** — 扫描件保留 PDF 让用户自决
- **不衔接其它 skill** — `dossier-fin` 等下游若要复用本地缓存,自行读 `~/.cache/cninfo/md/<ts_code>/`

## 故障排查

| 症状 | 排查 |
|---|---|
| `OrgIdNotFound: orgId not found for sec_code=XXX` | 代码错 / 已退市 / cninfo 接口变了。试 `cninfo orgid XXX --refresh` |
| `no annual report body found ... year=YYYY` | 报告期窗口外?显式传 `--plate`?是不是只有摘要而无本体? |
| `announcement_filter not installed` | 按上面"前置依赖"装它 |
| 网络超时 / 503 | cninfo 短期 throttle,等几分钟重试;长跑用 `--limit` 减压 |
| `cninfo cache verify` 报不一致 | 一般是上次中断导致;看具体 ann_id 后 `--force` 重抓 |
