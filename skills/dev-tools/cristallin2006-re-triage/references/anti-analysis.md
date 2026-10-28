> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# 反分析识别与绕过（反调试 / 反混淆 / 自校验）

## 1. 静态识别清单（headless 可自动扫）

搜 imports 和字符串命中即警觉：

```
ptrace  IsDebuggerPresent  CheckRemoteDebuggerPresent  NtQueryInformationProcess
NtSetInformationThread  rdtsc  cpuid  GetTickCount  QueryPerformanceCounter
/proc/self  SIGTRAP  alarm  OutputDebugString  FindWindow(调试器窗口名)
```

`triage` 命令（ghidra-core §5）的 `suspicious_imports.anti_debug` 已覆盖 Windows 侧主项。

## 1.5 区分程序逻辑、检测条件与插桩副作用

可疑字符串、恒定参数或单次崩溃只提供线索。按当前命题选择静态条件追踪、未插桩对照或其他可区分实验；已有明确源码/指令证据时可先保留静态解释，不要求每次重新跑完整基线。

基线中也出现该分支，仅说明它不是此次插桩独有的现象，不能排除其中确有反调试检查。插桩后行为改变可能来自检测、时序、ABI/参数错误、异常或探针副作用，需要比较实际条件。无法运行时标明未动态确认，仍可交付静态证据与未决项。

## 2. 检测线索与候选干预

表中偏移和实现仅作特定构建下的线索，需核对当前位宽、版本、参数与输出含义；命中不自动证明可达或可绕过。

| 检测手段 | 识别特征 | 绕过 |
|---|---|---|
| `ptrace(PTRACE_TRACEME)` | 导入 ptrace | `LD_PRELOAD` hook 返回 0；或 patch 调用 |
| `/proc/self/status` TracerPid | 字符串 `/proc/self` | hook `open`/`read` 改返回值 |
| PEB.BeingDebugged | 偏移 0x2 读取 | ScyllaHide；或 patch 判断跳转 |
| PEB.NtGlobalFlag | 64 位偏移 0xBC，掩码 0x70 | ScyllaHide |
| Heap Flags/ForceFlags | 偏移 0x70 应为 0x2；0x74 应为 0 | ScyllaHide |
| `NtQueryInformationProcess` | 区分 NTSTATUS 与 class 0x7(DebugPort)/0x1E(DebugObject)/0x1F(DebugFlags) 的输出，各字段的零值语义分别核对 | 结合实际检查字段设计受控干预 |
| ThreadHideFromDebugger | `NtSetInformationThread` class 0x11 | hook 掉 |
| `rdtsc` + sub/cmp 时间差 | rdtsc 指令 | bp rdtsc；patch 比较；hook 时间源 |
| `cpuid` 后 jz/jnz | CPUID 指令 + 条件跳 | 改标志位或 patch（Ghidra 批量标记脚本见 scripting.md §8） |
| `int3` 扫 / DR0-DR7 检测 | 0xCC 扫描、调试寄存器读 | patch int3；ScyllaHide 藏硬件 BP |
| TLS 回调 | PE TLS Directory AddressOfCallBacks（先于 main） | TLS 断点或 patch 回调 |
| VEH + 故意异常 | AddVectoredExceptionHandler + 触发异常 | bp VEH 注册函数；跟 handler |
| 时间锁 | 与大整数常量比较（2012≈1.35B, 2017≈1.5B） | faketime / patch 比较 |
| 代码自校验 | CRC32 over .text | 硬件断点；patch 比较点；hook hash 函数；可按条件选择仿真，并核对自校验读取的真实字节、映射和系统语义；不保证免疫 |

## 3. 反反汇编（Ghidra 侧处理）

| 手法 | 特征 | 处理 |
|---|---|---|
| 跳转进指令中间 | `eb 01 e8` 类 junk bytes | undefine 后从正确偏移重新 disassemble |
| 不透明谓词 | 恒真/恒假分支 | Z3 证明后 patch；GOOMBA |
| 函数切块 | 一个函数拆成多个块 | 每块 Create Function；或分析后手工拼 |
| `leave; ret` 无 call 链 | 许多小块以 `leave; ret` 结尾却无对应 call；"stack frame is too big" 报错 | 识别为链式调用，按块逐个反编译 |
| switch 恢复失败 | 跳转表识别错 | 手动指定跳转表；看汇编兜底 |

## 4. OLLVM 反混淆（分层顺序有讲究）

可按依赖尝试 bcf（虚假控制流/不透明谓词）、fla（控制流平坦化）与 sub/MBA（指令替换/混合布尔算术）。先处理会妨碍后续分析的层；嵌套结构按实际证据迭代，不规定通用固定顺序。

- 平坦化识别：while+switch 星形 CFG，状态变量驱动 → GDB 脚本断 `je` 记录状态变量序列，重建真实 CFG；Ghidra 侧用 `get_basic_blocks.py` 导出 CFG 后离线分析。
- MBA 化简表（常见等价式）：

```
(x ^ y) + 2*(x & y)      == x + y
(x | y) - (x & y)        == x ^ y
2*(x | y) - (x ^ y)      == x + y
(x ^ y) + (x & y)        == x | y
```

- 工具：GOOMBA（Ghidra 插件，P-Code 级 MBA 化简：jar 拷进 Ghidra extensions → CodeBrowser Analysis → GOOMBA；⚠ 注意与 Hex-Rays IDA 的 goomba 区分）；SiMBA 的 PyPI 包 `simba-simplifier` 是占位包（0.0.1 无功能），**不要装**，真要用需从源码构建（当前未装）；符号执行兜底（angr/Miasm）。
- Goron/Arkari 间接跳转变种：先试把数据段设只读再分析。

## 5. 动态交接原则（静态被反分析卡死时）

依据初始化时序和待区分问题选择 TLS 回调、入口点、敏感 API 或退出位置；这些是候选观察点，不要求依次打满。

目标即将退出且相关状态可能消失时，可在已有授权与可用工具下保存必要内存或日志；不能采集时记录缺口，不强制 dump 全进程。

- 沙箱无行为/秒退 → 查反调试/反 VM；**禁止把"无行为 + 疑似 anti-VM"写成"样本无害"**。
- 按问题选择真实进程、调试器或 Qiling/Unicorn。仿真可能改变某些检测条件，也可能因系统调用、时间或环境模型不足产生差异；`ptrace` 等 stub 属于明确干预，不能代表未干预目标行为。
- API 哈希解析可结合静态算法恢复与动态解析结果；`LD_PRELOAD`、符号断点或 `GetProcAddress` 观察需符合目标加载条件，并核对实际命中与返回地址。

## 6. 动态/静态不一致时

Ghidra 分析与调试器行为对不上 → 查 PEB anti-debug 是否**改变了比较目标值**（反调试分支会走不同常量）。

## 7. 反 VM / 反沙箱（样本"秒退/无行为"时的排查清单）

样本静默或提前退出时，可结合启动条件、权限、输入和以下检测线索区分解释；字符串命中不等于检测已执行，未观察到行为也不足以判定无害：

| 检测点 | 具体特征 |
|---|---|
| VM 进程/服务 | 字符串/进程名枚举：`vmtoolsd.exe`、`VBoxService.exe`、`prl_cc.exe` |
| MAC 前缀 | 00:0C:29 / 00:50:56（VMware）、08:00:27（VirtualBox）、00:1C:42（Parallels） |
| 注册表 artifact | `HKLM\SOFTWARE\VMware, Inc.`、`HKLM\HARDWARE\ACPI\DSDT\VBOX__` |
| 用户交互检测 | `GetCursorPos`（坐标长期不变 = 沙箱）、`GetAsyncKeyState` |
| 环境指纹 | 磁盘 < 60GB、CPU ≤ 2 核、RAM < 4GB（WMI/Win32 API 查询） |
| sleep 膨胀 | `Sleep(600000)` 配合沙箱时间加速检测：`GetTickCount` 差值 ÷ 请求值异常 = 被加速 |

仿真、调试和实际设备各有环境指纹与覆盖限制。定位检测条件后可设计范围明确的干预副本，再与原始条件区分；patch 后的行为不替代原件验证。
