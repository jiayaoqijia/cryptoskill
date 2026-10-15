# Headless 执行模型详解（driver.py / PyGhidra · Windows · Ghidra 12.1.3）

> ⚠ 执行模型已迁移：本 skill 的 `.py` 脚本是 **PyGhidra（Python 3）**，由 `scripts/driver.py` 驱动。
> `analyzeHeadless.bat` 只在两处内部使用：`driver.py export`（持久化项目）和 `.java` 脚本。
> **不要把 `.py` 脚本交给 analyzeHeadless**——会报 `Ghidra was not started with PyGhidra` / Jython 缺失。

## 1. driver.py 子命令（日常唯一入口）

```bash
PY="$HOME/Desktop/src/ghidra-bridge/pyghidra-venv/Scripts/python.exe"
SK="$HOME/.dsh/skills/ghidra-core/scripts"

"$PY" "$SK/driver.py" export <binary> [--force] [--overwrite] [--max-cpu N] [--analysis <超时秒>]  # 建可复用项目（analyzeHeadless -import，一次性）
"$PY" "$SK/driver.py" import <binary> [--force] [--analysis minimal|default]  # 进程内导入+分析+triage（不落盘）
"$PY" "$SK/driver.py" list <binary>                             # 列项目内程序
"$PY" "$SK/driver.py" exec   <binary> <script.py> [args...]     # 只读执行
"$PY" "$SK/driver.py" exec-w <binary> <script.py> [args...]     # 执行后保存项目（写操作必须用它）
# 全局选项：-v / --verbose = verbose JVM 输出（排障时加在子命令前）
# ⚠ import 与 export 的 --analysis 撞名不同义：import=分析器档位，export=单文件分析超时秒
```

- 项目名：`dsh_<sha256(binary)前16>`，与二进制路径无关。
- 分工：**export 负责持久化**（PyGhidra 存不下自己 load 的程序，SKILL.md §7「持久化限制」），**import 负责一次性的进程内分析+分诊**。常规流程：`export` 一次建项目，之后全部 `exec`/`exec-w`。
- 脚本名解析顺序：skill scripts 目录 → 当前目录 → `<ws>/scripts`。脚本参数原样透传，`@out` 约定照旧。
- 环境变量：`GHIDRA_INSTALL_DIR`（Ghidra 安装目录）、`DSH_GHIDRA_WS`（工作区，默认 `~/.dsh/ghidra-workspace`）、`DSH_GHIDRA_WS_LINK`（无点 junction，默认 `~/dsh-ghidra-workspace`）、`PYGHIDRA_JAVA_HOME` / `JAVA_HOME`（必须是 JDK 不是 JRE）。

## 2. 项目生命周期与缓存

- 项目 = `<junction>/projects/<项目名>.gpr` + 同名 `.rep` 目录。
- `export` 建的项目持久可复用；`import` 建的项目**只活在当次进程**（程序在只读 DomainFileProxy 后面，save 会 ReadOnlyException）。
- 重分析：`--force`（删 `.gpr` + `.rep` 重建）。
- 项目留着别删：GUI（`ghidraRun.bat`）打开同一项目可接着手工深挖，headless 的标注/改名都在。
- 并发：同一项目同时只能一个进程打开（项目锁）；批量多样本（不同项目）可以并行。

## 3. 脚本参数与输出协议

- 脚本内 `getScriptArgs()` 拿参数（PyGhidra 下仍可用，脚本 globals 由 GhidraScript 实例懒取）。
- **`@out` 约定**：首个参数 `@绝对路径` = 完整结果写该文件（JSON，`json.dumps` 默认 ensure_ascii 纯 ASCII 安全；伪代码等文本用 utf-8 errors=replace）；stdout 只留 `===JSON_START===/===JSON_END===` 状态摘要。
- 为什么落文件：Ghidra 的 INFO 日志混 stdout；Windows 控制台编码毁非 ASCII；大输出被管道截断。文件 + Read 工具最稳。
- driver 每次 exec 的完整 stdout/stderr 落在 `<junction>/projects/<项目名>.exec.log`；分析日志在 `<ws>/logs/`。

## 4. Windows / PyGhidra 坑（实测）

1. **APPDATA 重定向**：driver 把 `APPDATA/LOCALAPPDATA/USERPROFILE` 指到 `<ws>/settings`（配合文件沙箱）。副作用：Ghidra 去重定向后的目录找扩展——Jython 扩展在那里"消失"。用 PyGhidra 无此问题；想救 Jython 就在重定向目录里建 junction 指回真实扩展。
2. **`.py` 不能交给 analyzeHeadless**：见文件头警告，两个原因（无 PyGhidra 启动器 + APPDATA 重定向藏扩展）互相独立。
3. **`.java` 脚本反过来**：PyGhidra 跑不了注册目录外的 `.java`（`JavaScriptProvider: Failed to find source bundle`），driver 自动改走 `analyzeHeadless -scriptPath -postScript`。
4. **analyzeHeadless 参数走 Java property parser**：路径必须**正斜杠**，反斜杠被当转义 → `Bad argument: C:\Users\...`。
5. **工作区路径不能含 `.` 开头元素**：`ProjectLocator` 直接 abort。所以走 junction `~/dsh-ghidra-workspace`（driver 自动建/复用）。
6. **JPype 需要 JDK**：`JAVA_HOME` 指向 JDK（本机 `C:\Java`，Java 25 可用）；JRE 起不了 JVM 编译桥。
7. **内存**：JVM 堆由 `MAXMEM` 环境变量控制（默认 ~4G）。大二进制 OOM 时 `export MAXMEM=8G`。`GHIDRA_HEADLESS_MAXMEM` 是某插件的自定义变量，Ghidra 原生不读。
8. **analyzeHeadless abort 时退出码仍为 0**：不要信退出码，以输出文件/`.rep` 目录是否存在判定成败（driver 内部已按此判断）。
9. **超时**：冷启动 10~60s 是常态。调用方（agent Bash 工具）给超时：小样本 300s，大样本 600s+。

## 5. analyzeHeadless flag 速查（仅 export / .java 路径用得到）

| flag | 作用 |
|---|---|
| `-import <file>` | 导入并分析新二进制 |
| `-process <name>` | 处理项目里已有程序（配合 -noanalysis） |
| `-noanalysis` | 跳过自动分析 |
| `-readOnly` | 只读打开；省略则退出时保存修改 |
| `-overwrite` | 导入时覆盖已存在的同名程序 |
| `-scriptPath <dir>` | 脚本搜索目录（Windows 下多目录用 `;` 分隔） |
| `-preScript` / `-postScript` | 分析前/后跑的脚本（**参数必须紧跟脚本名**） |
| `-analysisTimeoutPerFile <秒>` | 单文件分析超时 |
| `-max-cpu <N>` | 分析并行度 |
| `-log <file>` | 日志文件 |
| `-loader <名>` / `-baseAddress` | raw 二进制/固件加载控制 |

## 6. raw 固件 / dump 内存段导入

`driver.py export` 不暴露 loader 参数——raw 固件直接手写一次 analyzeHeadless（正斜杠路径！）：

```bash
"$GHIDRA_HOME/support/analyzeHeadless.bat" "$HOME/dsh-ghidra-workspace/projects" dsh_fw \
  -import "C:/abs/path/dump.bin" -loader BinaryLoader -baseAddress 0x08000000 \
  -processor "ARM:LE:32:Cortex" -analysisTimeoutPerFile 600
```

建好后照常 `driver.py exec dump.bin <script>`。脱壳 dump 的内存段同理：`-baseAddress` 给 dump 时基址，导入后在入口点 Create Function + 重分析。

## 7. 排障顺序

1. `<junction>/projects/<项目名>.exec.log` 末尾 + `<ws>/logs/` 对应日志的 `ERROR` 行
2. `script not found` → 脚本名/路径；`project not found` → 先跑 `driver.py export`
3. `ModuleNotFoundError: No module named 'ghidra'` → 有代码在 `pyghidra.start()` 之前 import 了 ghidra.*
4. `ReadOnlyException` / 改了没保存 → 写操作用了 `exec` 而不是 `exec-w`
5. `Bad argument: C:\...` → analyzeHeadless 路径含反斜杠，换正斜杠
6. `JythonStubScriptProvider` / `Ghidra was not started with PyGhidra` → 拿错启动器了，见 §4.1/§4.2

## 8. 二进制比对（ghidriff）

本 skill 不做 Version Tracking，用现成工具（它自己就是 Ghidra headless 封装）：

```bash
pip install ghidriff
export GHIDRA_INSTALL_DIR="C:/t001s/ghidra_12.1.3_PUBLIC_20260817/ghidra_12.1.3_PUBLIC"  # 不装就用它自动下载的 Ghidra
ghidriff old.exe new.exe -o ./diff_out/ --json-format        # JSON 喂 agent / Markdown 给人看
ghidriff old.exe new.exe -o ./diff_out/ --engine VersionTrackingDiff --threaded \
  --max-section-funcs-analyze 8000 --max-section-funcs-full 800   # 大文件防 OOM
ghidriff --list-engines                                       # VersionTrackingDiff(默认)/SimpleDiff/StructualGraphDiff
```

产物三件套：Markdown 报告 / JSON / Ghidra 项目（可用 GUI 或本 skill 的 exec 继续分析）。

## 9. Function ID / FIDB

- Function ID 是分析器：`driver.py import --analysis default` 开启（`minimal` 档为速度会关掉它）。
- FIDB 签名库的制作/管理（File → Batch Import 到 FIDB、Debug Function ID）是低频 GUI 操作，不在本 skill 范围；需要时对一批样本跑 GUI 的 Function ID 插件即可。
