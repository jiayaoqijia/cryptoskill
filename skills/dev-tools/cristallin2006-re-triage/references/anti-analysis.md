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

## 1.5 「疑似反调试」必须先证伪（误判 = 路线自杀）

看到像陷阱的字面量/分支（`"Don't hook!!!"` 这类字符串、可疑的恒假比较）就宣布
"anti-tamper 设计"并放弃插桩，等于把唯一能看穿内部的工具亲手扔掉（858e13b3：
`_p3` 的固定实参与 `_tips` 的初值本来就长那样——是设计常量，不是反调试）。

证伪纪律：判某字面量/分支是陷阱之前，必须做**无插桩基线对照**——不挂任何 hook 跑一遍，
该值/该分支仍在 ⇒ 程序固有逻辑，不是冲你来的。「挂上 hook 后行为变了」不构成陷阱证据
（hook 本身就改变行为）。基线对照做不了 ⇒ 不许下"有反调试"结论（铁律 10④ 否定性结论门槛）。

## 2. Check → Bypass 对照表

| 检测手段 | 识别特征 | 绕过 |
|---|---|---|
| `ptrace(PTRACE_TRACEME)` | 导入 ptrace | `LD_PRELOAD` hook 返回 0；或 patch 调用 |
| `/proc/self/status` TracerPid | 字符串 `/proc/self` | hook `open`/`read` 改返回值 |
| PEB.BeingDebugged | 偏移 0x2 读取 | ScyllaHide；或 patch 判断跳转 |
| PEB.NtGlobalFlag | 64 位偏移 0xBC，掩码 0x70 | ScyllaHide |
| Heap Flags/ForceFlags | 偏移 0x70 应为 0x2；0x74 应为 0 | ScyllaHide |
| `NtQueryInformationProcess` | class 0x7(DebugPort)/0x1E(DebugObject)/0x1F(DebugFlags)，返回 0 = 被调试 | hook 改返回值 |
| ThreadHideFromDebugger | `NtSetInformationThread` class 0x11 | hook 掉 |
| `rdtsc` + sub/cmp 时间差 | rdtsc 指令 | bp rdtsc；patch 比较；hook 时间源 |
| `cpuid` 后 jz/jnz | CPUID 指令 + 条件跳 | 改标志位或 patch（Ghidra 批量标记脚本见 scripting.md §8） |
| `int3` 扫 / DR0-DR7 检测 | 0xCC 扫描、调试寄存器读 | patch int3；ScyllaHide 藏硬件 BP |
| TLS 回调 | PE TLS Directory AddressOfCallBacks（先于 main） | TLS 断点或 patch 回调 |
| VEH + 故意异常 | AddVectoredExceptionHandler + 触发异常 | bp VEH 注册函数；跟 handler |
| 时间锁 | 与大整数常量比较（2012≈1.35B, 2017≈1.5B） | faketime / patch 比较 |
| 代码自校验 | CRC32 over .text | 硬件断点；patch 比较点；hook hash 函数；**用 Unicorn/Qiling 仿真天然免疫** |

## 3. 反反汇编（Ghidra 侧处理）

| 手法 | 特征 | 处理 |
|---|---|---|
| 跳转进指令中间 | `eb 01 e8` 类 junk bytes | undefine 后从正确偏移重新 disassemble |
| 不透明谓词 | 恒真/恒假分支 | Z3 证明后 patch；GOOMBA |
| 函数切块 | 一个函数拆成多个块 | 每块 Create Function；或分析后手工拼 |
| `leave; ret` 无 call 链 | 许多小块以 `leave; ret` 结尾却无对应 call；"stack frame is too big" 报错 | 识别为链式调用，按块逐个反编译 |
| switch 恢复失败 | 跳转表识别错 | 手动指定跳转表；看汇编兜底 |

## 4. OLLVM 反混淆（分层顺序有讲究）

**顺序：先 bcf（虚假控制流/不透明谓词）→ 再 fla（控制流平坦化）→ 最后 sub/MBA（指令替换/混合布尔算术）**。嵌套 fla 需迭代处理。

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

**断点四级火箭（顺序 MUST）**：
1. TLS 回调断点 → 2. EP 断点 → 3. 敏感 API 断点 → 4. 保底 `ExitProcess` 断点。

因反调试退出时**不急着重启**——立即 dump memory 写证据。

- 沙箱无行为/秒退 → 查反调试/反 VM；**禁止把"无行为 + 疑似 anti-VM"写成"样本无害"**。
- 仿真器优先于调试器：Qiling/Unicorn 无调试器痕迹，默认绕过一切反调试；Qiling 还能 `ql.os.set_syscall("ptrace", hook)` 定点骗。
- API 哈希解析：不浪费时间逆哈希函数本身——`LD_PRELOAD` hook OpenSSL/系统 API 抓解析结果；`bp GetProcAddress` 反查回注。

## 6. 动态/静态不一致时

Ghidra 分析与调试器行为对不上 → 查 PEB anti-debug 是否**改变了比较目标值**（反调试分支会走不同常量）。

## 7. 反 VM / 反沙箱（样本"秒退/无行为"时的排查清单）

样本在沙箱里无行为，第一反应是查这些检测点（命中即证实"有条件执行"，不是"无害"）：

| 检测点 | 具体特征 |
|---|---|
| VM 进程/服务 | 字符串/进程名枚举：`vmtoolsd.exe`、`VBoxService.exe`、`prl_cc.exe` |
| MAC 前缀 | 00:0C:29 / 00:50:56（VMware）、08:00:27（VirtualBox）、00:1C:42（Parallels） |
| 注册表 artifact | `HKLM\SOFTWARE\VMware, Inc.`、`HKLM\HARDWARE\ACPI\DSDT\VBOX__` |
| 用户交互检测 | `GetCursorPos`（坐标长期不变 = 沙箱）、`GetAsyncKeyState` |
| 环境指纹 | 磁盘 < 60GB、CPU ≤ 2 核、RAM < 4GB（WMI/Win32 API 查询） |
| sleep 膨胀 | `Sleep(600000)` 配合沙箱时间加速检测：`GetTickCount` 差值 ÷ 请求值异常 = 被加速 |

绕过：Qiling/Unicorn 仿真天然无 VM artifact（仿真器优先原则，见 §5）；静态侧定位检测函数后 patch 返回值，或 xor 分支条件。
