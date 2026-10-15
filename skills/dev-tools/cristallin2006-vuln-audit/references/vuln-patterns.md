# 漏洞模式检查项清单（vuln-audit 主文档）

每项：**模式／识别信号／怎么查／判定标准／常见误报**。命令均以 `python "$SK/rpc_driver.py"` 为前缀（`SK="$HOME/.dsh/skills/ghidra-core/scripts"`），参数细节见 ghidra-core §5。

快速粗筛入口：`triage` 的 suspicious_imports 六组 + `imports` 全表 → 决定本清单哪些项需要深查。

## 1. 栈溢出（无边界拷贝）

**识别信号**：imports 含 `gets`/`strcpy`/`strcat`/`sprintf`/`scanf("%s")`/`vsprintf`；或伪码中向固定大小栈数组（`local_XX[32]` 类）拷贝的循环无长度判断。

**怎么查**：
```
imports <bin>                       # 先确认危险函数存在
xrefs-to <bin> strcpy               # 找调用点
decompile <bin> <调用者>            # 看源缓冲是否用户可控、有无长度检查
```

**判定标准**：目标缓冲在栈上（`local_*`）+ 源为用户输入 + 无 `strlen`/边界比较 → 命中。存在 `strncpy`/`snprintf`/`fgets` 且 n 来自 sizeof → 安全，不记。

**常见误报**：源是程序内部常量字符串；目标缓冲远大于任何可能输入；n 被正确计算。Canary（`__stack_chk_guard`/`_GS`）不消除漏洞，只降利用成功率——照记，备注保护情况。

## 2. 格式化字符串

**识别信号**：`printf`/`fprintf`/`snprintf`/`syslog` 的第一参数不是字符串字面量而是变量（伪码里 `printf(local_xx)` 或 `printf(param_1)`）。

**怎么查**：
```
xrefs-to <bin> printf
decompile <bin> <调用者>            # 确认 format 参数来源
search-decompiled <bin> "printf\([a-z]"   # 粗筛非字面量 format
```

**判定标准**：format 串含用户输入（read/recv/argv/环境变量）→ 命中。`printf(buf)` 中 buf 为纯内部日志模板 → 误报。Windows 上 `printf(user)` 可致崩溃泄信息，Linux 上 `%n` 可写内存。

**常见误报**：format 来自配置文件但配置不可控；`printf("%s", user)` 是安全写法（有格式符），别记。

## 3. 堆问题（UAF / double-free）

**识别信号**：伪码中 `free(p)` 之后同函数内继续使用 `p`（读写字段或再 free）；`free` 后指针未置 NULL 且该指针存在于长期存活结构体中。

**怎么查**：
```
xrefs-to <bin> free
decompile <bin> <调用者>            # 顺着 free 后的基本块看 p 的使用
basic-blocks <bin> <函数>           # free 后是否有路径重新引用 p
```

**判定标准**：free 后可达路径上存在解引用或二次 free（且无重新 malloc/置 NULL）→ 命中。free 后立即 `p = NULL` 或函数随即返回 → 安全。

**常见误报**：free 的是局部临时对象且作用域结束；自定义 allocator 的 "free" 语义不同（Go/Rust 二进制不适用本条）。

## 4. 整数溢出（分配前算术）

**识别信号**：`malloc(n)`/`calloc`/operator new 的 size 参数是用户可控值的乘/加运算（`malloc(count * 16)`），且 count 无上限检查；或比较用有符号、索引用无符号导致的回绕。

**怎么查**：
```
xrefs-to <bin> malloc
decompile <bin> <调用者>            # 看 size 表达式与上限检查
search-decompiled <bin> "malloc\(.*\*"    # 粗筛乘法分配
```

**判定标准**：size = f（用户输入） 且 f 可回绕（乘法溢出/加法回绕/负值转巨大无符号） → 分配小块拷贝大量 → 命中。

**常见误报**：count 来自本程序先前校验过的内部状态；表达式在 64 位下不会回绕且输入域已限幅。

## 5. 命令注入

**识别信号**：imports 含 `system`/`popen`/`ShellExecuteA/W`/`WinExec`/`CreateProcessA/W`/`execve` 系；伪码中命令行由 `sprintf`/`strcat`/字符串插值拼出且含用户输入。

**怎么查**：
```
xrefs-to <bin> system
decompile <bin> <调用者>            # 命令行来源是否拼接用户输入
search-decompiled <bin> "system\(|popen\(|ShellExecute"
```

**判定标准**：命令串任意片段来自用户输入且无白名单/转义 → 命中。命令串全为字面量、参数来自固定枚举 → 安全。

**常见误报**：拼接的是程序自身路径/安装目录（仍可能 PATH 劫持，降级为备注）；`CreateProcess` 用独立 argv 而非 shell 串（注入面小很多，降级）。

## 6. 危险 API 组合（triage 六组升级版）

**识别信号**：triage `suspicious_imports` 的组合命中，而非单组单命中。

**怎么查**：`triage <bin>` 看六组；命中组合后 `xrefs-to` 到具体调用点确认语义。

**判定标准（攻击面信号）**：
- injection ≥2（如 OpenProcess+VirtualAllocEx+WriteProcessMemory+CreateRemoteThread 齐三个以上）→ 进程注入链
- dynamic_loading（LoadLibrary+GetProcAddress）+ network 任一项 → 下载/加载二段载荷嫌疑
- persistence 组任一项 + anti_debug 组任一项 → 驻留+反分析，恶意样本权重上调
- crypto 组 + network 组 → 加密信道/勒索行为候选

**常见误报**：安装程序/更新器天然命中 injection+persistence；调试器/性能工具命中 anti_debug（QueryPerformanceCounter 是计时不是反调试，单独命中降级）。

## 7. 不安全的随机数

**识别信号**：`srand(time(0))` 后 `rand()` 的输出用于密钥/token/验证码/挑战值；或 `GetTickCount` 直接当随机源。

**怎么查**：
```
xrefs-to <bin> srand
xrefs-to <bin> rand
decompile <bin> <调用者>            # rand 输出流向：安全用途 or 游戏逻辑
```

**判定标准**：rand 输出进入密钥派生/口令/token/会话 id → 可预测，命中。仅用于延迟抖动/游戏行为 → 不记。

**常见误报**：`CryptGenRandom`/`BCryptGenRandom`/`getrandom`/`/dev/urandom` 是安全源——看到它们说明作者知道怎么做，反而要重点查有没有**混用** rand 兜底的分支。

## 8. 硬编码密钥/口令

**识别信号**：`.rodata` 中紧邻 crypto 调用（AES/DES/RC4/XOR 循环）的 8/16/24/32 字节常量数组；字符串含 `key`/`pass`/`secret`/`-----BEGIN`/`AKIA` 前缀；XOR 循环里引用的单字节/多字节常量。

**怎么查**：
```
strings <bin> "key|pass|secret|BEGIN"
search-decompiled <bin> "\^ 0x|\^0x"     # XOR 解密例程
decompile <bin> <crypto调用者>            # key 参数来源地址
read-bytes <bin> <地址> <长度>            # 直接提取密钥字节
```

**判定标准**：密钥/口令以明文或可单步还原的编码（单字节 XOR、Base64）存在且用于保护实际数据 → 命中，直接提取为证据。

**常见误报**：字符串里的 "keyboard"/"passport" 等自然语言词；公钥/盐（设计就是公开的，不记）；CTF 题的假 flag 诱饵（多个候选时以最终比较点 xref 为准）。

---

## 通用判定纪律

1. **模式命中 ≠ 漏洞**：每项必须过"用户输入可达性"这关——用 `xrefs-to` 反查调用链，追到 main/recv/read/argv/环境变量才算实。
2. **保护机制记录但不豁免**：Canary/NX/DEP/ASLR/CFG 影响利用难度不影响漏洞存在性，逐项备注。
3. **证据格式**：每个命中 = 地址 + 伪码/汇编摘录 + 输入来源链 + 复现命令。
4. **静态存疑 → 动态验证**：给出建议入口（fuzz harness、Frida hook 点、angr 目标地址），别在静态层硬撑结论。
