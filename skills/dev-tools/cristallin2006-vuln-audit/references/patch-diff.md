> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# 补丁比对与 N-day 分析（patch diff）

**分工边界**：本篇管"补丁前后两版差分 → 锁定改动函数 → 反推漏洞类型 → 规划 PoC 验证"。不管：漏洞模式清单本身（`references/vuln-patterns.md`）、ghidriff/version-track 命令参数细节（ghidra-core `references/headless.md` §8 与 SKILL.md §5）、拿到版本对之前的补丁获取（见 §2 步骤 0 简述，深度流程超出本 skill）、动态验证执行（re-dynamic）。

```bash
SK="$HOME/.dsh/skills/ghidra-core/scripts"
RD="$SK/rpc_driver.py"
GHIDRIFF="$HOME/Desktop/src/re-tools-venv/Scripts/ghidriff.exe"   # Windows
# WSL/Linux: GHIDRIFF="$HOME/re-tools-venv/bin/ghidriff"
```

## 1. 工具选型决策

| 工具 | 本机状态 | 何时用 |
|---|---|---|
| **ghidriff** | ✅ Tier B（re-tools-venv `ghidriff.exe`） | **默认首选**。纯 CLI、headless、输出 Markdown+JSON 可喂 agent；`--engine VersionTrackingDiff` 默认即 Ghidra VT |
| rpc `version-track` | ✅ ghidra-rpc 内置（Auto VT + BSim） | 两个版本已在 daemon 里、想要结构化 JSON、或要接 `function-diff` 逐函数对照时（§5） |
| BinDiff | ❌ 未装（GUI 依赖，doctor.py 无条目） | 仅当 ghidriff 匹配质量不可信且需要图形化 block 着色复核时，另行安装；非默认路径 |
| Diaphora | ❌ 未装（依赖 IDA Pro，本机无 IDA 许可） | 不装，不引用 |

决策规则：agent 流水线一律 ghidriff / rpc version-track；GUI 工具不进自动化链路。

## 2. 标准工作流

0. **取版本对**：真题场景最稳输入是月度安全更新（Windows  cumulative `.msu`：`expand -F:*` 解两层 cab，目标二进制在 `amd64_microsoft-windows-<组件>_*\` 下；Linux 用 `apt download` 相邻两版 deb + `dpkg-deb -x`）。历史 LPE 高发组件（clfs.sys / afd.sys / win32kfull.sys / spoolsv）优先作为 diff 目标——CVE 复现与 SRC 溯源同理：锁定" vendor 发了补丁但没公开细节"的版本差。
1. `python "$RD" ensure <old.exe>` + `python "$RD" ensure <new.exe>`：两版各自完成导入与全量分析（铁律 2）。
2. **跑 diff**（大文件防 OOM 参数照抄）：
   ```bash
   "$GHIDRIFF" old.exe new.exe -o ./diff_out/ --json-format --engine VersionTrackingDiff \
     --threaded --max-section-funcs-analyze 8000 --max-section-funcs-full 800
   ```
   产物三件套：Markdown 报告（人读）/ JSON（喂下游）/ Ghidra 项目（可 `ensure` 继续查）。
3. **按 score 排序锁定改动函数**：读 JSON 报告——similarity 1.0 跳过；0.5–0.95 是重点（多半是修 bug）；unmatched 新增函数看是否为新增的 sanitize/mitigation。**灵敏度坑**：单字节 patch 级差异在默认阈值下可能被判 identical——`changed_functions: 0` 不等于没改动，去掉 `--changed-only` 看全量 similarity 分数，或调低 `--min-similarity`（ghidra-core SKILL.md §5 注）。
4. **反编译对照**：对每个候选函数 `python "$RD" function-diff old.exe <f1> new.exe <f2>`（伪码归一化 diff，滤掉变量重命名噪声）；名字对不上时 `match-function`（BSim 匹配 `FUN_xxx`）。
5. 每个候选 `ledger.py observe <new.exe> --region <func> --tool ghidriff --note "diff similarity=0.7"`；判定后 `conclude`。

## 3. 根因分析：改动模式 → 漏洞类型反推

看 before/after 伪码，按下表归类，再回 vuln-patterns.md 对应条目取证：

| 补丁新增的改动 | 反推漏洞类型 | vuln-patterns.md 对应条目 |
|---|---|---|
| `if (a > MAX - b) goto err` / `__builtin_add_overflow` | 整数溢出（分配前算术）→ 分配过小 + 后续拷贝溢出 | §4 整数溢出 |
| 新增 `if (idx >= size)` / `if (len > sizeof(buf))` 边界检查 | 越界读/写、栈/堆溢出 | §1 栈溢出 / §3 堆问题 |
| 新增加锁 / `InterlockedIncrement` / 引用计数原子化 | 竞争条件（TOCTOU）、UAF | §3 堆问题 |
| `memset(buf,0,…)` / `RtlZeroMemory` / 清 padding 字段 | 未初始化内存信息泄漏（内核地址泄露） | vuln-patterns.md 无独立条目，记为 info-leak 类观察 |
| 新增 `ProbeForRead/Write` / `access_ok` / `__try/__except` | 用户态指针未校验 → 任意地址读写 | §1/§3（按落点归类） |
| format 参数从变量改为字面量 | 格式化字符串 | §2 格式化字符串 |
| 危险 API 换安全版（`strcpy`→`strncpy`/`snprintf`） | 直接点名旧 API 的病 | §1 栈溢出 |
| 输入长度/类型校验加强、system() 参数加引号/白名单 | 命令注入 | §5 命令注入 |

反推后必须回答：被守护的后续操作是什么（memcpy？数组下标？），旧版传什么值能越过——这决定 PoC 的输入形态。

## 4. 从 diff 到 PoC：可利用信号

| 信号 | 含义 | 动作 |
|---|---|---|
| 新增边界检查守护 memcpy/数组下标 | 旧版可传超长 length / 越界 idx | 构造输入使 length = 旧版无检查、新版被拒的临界值 |
| 新增溢出检查在分配前 | 乘法/加法回绕 → 小分配大拷贝 | 边界值：`a=0xFFFFFFF0, b=0x100`（32 位）类 |
| 加锁 / 引用计数改动 | 竞争窗口存在 | 双线程 hammer（一线程 free/close，一线程 use），绑核提高命中率 |
| 清零 padding | 旧版泄漏内核/栈残留 | 反复调用读 output，按 8 字节解析找 `0xFFFF…` 形态指针 |
| 修补不完整（只修一个调用点） | **变体仍在**：`xrefs-to <new.exe> <patched_func>` 查其余调用者，`search-decompiled` 搜同模式 | 变体分析 = 新 CVE 的最常见来源 |

构造触发路径：`xrefs-to` 从改动函数反追到用户输入入口（IOCTL/recv/argv/文件解析），确认可达性优先于一切（SKILL.md 审计流程第 4 条）。PoC 骨架：WSL 侧 pwntools（gdb(wsl)/pwntools(wsl) 均已装），Windows 侧 Frida hook 验证触发。

## 5. 版本追踪能力（rpc version-track）

`version-track` / `function-diff` / `match-function` 已内置 ghidra-rpc，会自动把 B load 进 A 的项目（VT 要求同项目）。大样本对的全函数关联是长任务，**用后台跑 + `@out` 落盘**（ghidra-core SKILL.md §2 长任务约定）：

```bash
# 后台跑，结果落 JSON
python "$RD" "@$HOME/.dsh/ghidra-workspace/out/vt.json" version-track old.exe new.exe --changed-only
python "$RD" "@$HOME/.dsh/ghidra-workspace/out/fd.json" function-diff old.exe FUN_00401234 new.exe FUN_00401390
```

`--changed-only` 只看 similarity<1.0；覆盖统计看 `summary`（matched/changed/unmatched）。与 ghidriff 的关系：同底座（Auto VT），ghidriff 出一站式报告，rpc 版适合已 load 过、要逐函数钻取的迭代场景——两者结论不一致时以 `function-diff` 的归一化伪码 diff 为裁决。

## 6. 纪律

- **diff 结果是假设不是结论**（铁律 10）：similarity 分数和"疑似整数溢出修复"都只是假设；只有 PoC 在旧版上真实触发崩溃/越界、且在新版上被拒，才算数。验证 harness 先用已知输入自检，"偶发命中"复跑 ≥100 次。
- 补丁里引用的关键常量（新边界值、新结构体大小）按铁律 8 走 `read_views.py` 权威读数，禁止从反编译渲染文本转录。
- 静态反推 15 分钟无可达路径 → 转动态（铁律 6：Frida/gdb(wsl) 验证触发点）。
- 每步 `ledger.py observe` 落账区域级观察，判定落 `conclude` 并标 `--source`；无独立来源（未 PoC 验证）的结论带 ⚠UNVERIFIED，禁止原样交付。

---

借鉴声明：本文改写自 zhaoxuya520/reverse-skill（MIT License）的 `skills/patch-diff-exploit/references/patch-tuesday-workflow.md`、`diff-tools-comparison.md`、`root-cause-and-poc.md` 及 `skills/binary-diff/references/prompt-template.md` 的结构与模式表。
