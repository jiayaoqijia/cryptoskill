> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# 信号/异常即控制流（exception-as-control-flow）

样本把 SIGILL/SIGSEGV/SIGTRAP 的 **handler 当成计算的一部分**：fault 不是崩溃，
是指令流本身。识别晚了会把「非法指令」误判为死代码/程序结束，或把 handler
合成语义误判为反调试。

## 识别信号

- imports 同时出现 `sigaction` + `sigaltstack`(+`mprotect`/`munmap`/`mincore` 更典型）
- 代码流里裸 `0f 0b`(UD2)/`0xcc`(INT3)，且**后面跟着不像代码的字节**
  （UD2 tape：fault 后的字节是数据，handler 负责解码）
- 对 PROT_NONE/unmapped 页的 `movzx`/`mov` 读——读是故意 fault,handler 合成「虚拟字节」
- triage `selfmod_signal` 命中（gdb 看不见的自修改之外，也覆盖 fault 驱动）

## 静态视图修复（先做，否则后面全歪）

1. **handler 改写保存的 RIP → UD2 后的代码是可达的**。Ghidra/IDA 把 UD2 判
   non-returning 会截断调用图、把其后代码显示为死代码——用 ghidra-core
   `scripts/noreturn_fix.py`（体检 → `--fix <func>` / `--flow <addr>`）修视图，
   别接受截断后的伪码（铁律 10⑦）。
2. **handler 函数常不在函数列表里**（经 sigaction 注册，无 call xref，分析器
   不自动建函数）→ `create-function <bin> <handler地址>` 或 import-raw 时
   `--entry` 显式给。handler 地址从 sigaction 调用的第 2 参数读
   （`sa_handler`/`sa_sigaction` 字段）。
3. 可达性/死代码类否定结论走 `conclude --kind negative --proof` 硬门。

## handler 解剖（x86-64 Linux）

`sigaction(signum, &act, &old)`，`act` 布局：`{sa_handler(8), sa_mask(128), sa_flags(8) ...}`

- `sa_flags & 0x4`(SA_SIGINFO)→ handler 原型 `h(int sig, siginfo_t *si, void *uc)`，
  **第 3 参数 ucontext 是计算通道**
- `sa_flags & 0x08000000`(SA_ONSTACK)→ 配合 sigaltstack，说明 fault 时栈可能已坏
- si 里 `si_addr`(fault 地址）在 siginfo +0x10

**ucontext_t 寄存器偏移**（uc 指针 + 下表；gregs 从 +0x28 起，顺序 R8..R15,RDI,RSI,RBP,RBX,RDX,RAX,RCX,RSP,RIP,EFL):

| 寄存器 | 偏移 | 寄存器 | 偏移 |
|---|---|---|---|
| RDI | +0x68 | RBX | +0x80 |
| RSI | +0x70 | RDX | +0x88 |
| RBP | +0x78 | RAX | +0x90 |
| RCX | +0x98 | RSP | +0xa0 |
| **RIP** | **+0xa8** | EFL | +0xb0 |

handler 干的三件事对应三问：**改了哪个寄存器**（合成值，常写 RAX)、
**RIP 推进多少**（跳过 fault 指令/tape 记录宽度）、**校验了什么**
(fault 地址/序号不符 = 反 patch 或状态机）。

## gdb 配方

```bash
# 让 handler 干活，别让 gdb 抢在 handler 前面停：
handle SIGILL nostop noprint pass
handle SIGSEGV nostop noprint pass
# 观察 handler：断在 handler 入口，看 ucontext
break *0x<handler>
p/x *(unsigned long*)($rdx+0x90)   # ucontext.RAX（SA_SIGINFO 时 rdx=uc）
p/x *(unsigned long*)($rdx+0xa8)   # ucontext.RIP
# 不确定 handler 地址：catch 安装动作本身
catch syscall rt_sigaction
```

模板库：re-dynamic `scripts/gdbkit.py`(`uct()`/`sig_pass()` 已封装上表与 handle 行）。

## 反模式

1. **把 SIGSEGV 当 crash 处理**(gdb 默认 stop)→ 停在 fault 点就以为程序死了；
   先 `handle ... pass` 再看程序是否自己走下去。
2. **「修掉」fault 源**：把 PROT_NONE 页全置可读 / 把 UD2 patch 成 NOP——
   fault 是计算输入，改掉它 = 改掉计算结果（改环境=改计算）。只能探索控制流，
   不能产出验证数据（re-dynamic §4①）。
3. **mincore/常驻性检查当反调试**：页常驻模式本身可能是计算的输入数据，
   中和它之前先确认它是不是校验材料。
4. **假设 UD2 = 程序结束**：先查有没有 handler 推进 RIP，再下结论（硬门见上）。
