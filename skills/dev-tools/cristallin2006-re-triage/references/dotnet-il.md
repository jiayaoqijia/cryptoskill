> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# .NET 样本 IL 分析（de4dot 脱混淆 / dnSpyEx 反编译 / 元数据坑）

> 本篇管：托管 .NET（CLR/IL）样本判型完成后的深挖——脱混淆、CLI 批量反编译、IL 阅读、动态调试入口。
> 不管：NativeAOT/IL2CPP（是 native，回 ghidra-static）；外层还有壳（先 re-unpack）；Android DEX（android-re `references/dalvik-notes.md`）。判型特征与路线决策见 `references/triage.md` §3。
> 工具可用性以 `python "$SK/doctor.py"` toolchain 节为准（dnSpyEx/de4dot/DIE 均为 Tier C 已装）。

## 1. 判型复核（进本篇前的硬门）

1. triage 报 `mscoree.dll` / `_CorExeMain` → 本篇；有 CLR 头但字符串含 `System.Private.CoreLib` AOT 特征或出现 `global-metadata.dat`+libil2cpp → **回 ghidra-static**（native，别用本篇工具）。
2. DIE 复核混淆器：`"$HOME/Desktop/src/tools/die/die/diec.exe" sample.exe`（对 .NET 报 compiler/runtime + 混淆器名）。
3. **铁律 4 等价物**：.NET 的 IAT 只有 `_CorExeMain` 是**正常**的，不是动态加载嫌疑、不许据此报"干净导入表"；威胁面改走元数据——dnSpyEx 里看 AssemblyRef/TypeRef 引用表等价于 imports 锚点，不许空过硬门。
4. 开工即 `ledger.py observe` 落账；先对原始样本记 SHA256，脱混淆产物是新样本、单独落账。

## 2. 标准流程（先脱混淆，再反编译）

```bash
DE4="$HOME/Desktop/src/tools/de4dot/de4dot.exe"
DSC="$HOME/Desktop/src/tools/dnSpyEx/dnSpy.Console.exe"

"$DE4" -d sample.exe                          # 只检测混淆器并退出
"$DE4" -f sample.exe -o sample.cleaned.exe    # 自动识别并脱混淆（改名+控制流+字符串解密）
"$DE4" -p cf -f sample.exe -o out.exe         # 识别错时强制类型（cf=ConfuserEx，un=Unknown）
"$DSC" -o out_dir sample.cleaned.exe          # 导出整个 C# 工程到目录（默认 C#）
"$DSC" -t "Namespace.ClassName" sample.cleaned.exe   # 单个类型打到 stdout
"$DSC" -l IL -t "ClassName" sample.cleaned.exe       # 要 IL 而不是 C#（看混淆残留/校验语义时用）
"$DSC" --md 0x0600001A sample.cleaned.exe     # 按元数据 token 反编译单个成员
```

- **顺序 MUST：de4dot 先行**。直接在 dnSpyEx 里读混淆样本会淹没在 `<PrivateImplementationDetails>` 和乱码名里。
- de4dot 原地改文件名，务必在副本上跑；`--preserve-tokens` 保留 token/#US/#Blob（后续要按 token 对照 IL 时加）。
- 字符串解密失败（残留 `Class0.smethod_0(12345)` 调用）→ 用 `--default-strtok <token>` 指定解密方法强制解密。

## 3. IL 速查（读 `-l IL` 输出 / dnSpyEx IL 视图）

| IL | 含义 | 逆向看点 |
|---|---|---|
| `ldstr "..."` | 压入 #US 堆字符串 | operand 是 token `0x70xxxxxx`；加密字符串常表现为 `ldstr`+紧跟解密 `call` |
| `ldc.i4.N` / `ldc.i4 <n>` | 压入 int 常量 | 密钥/魔数/长度；`ldc.i4.s` 是 1 字节短型 |
| `call` / `callvirt` / `newobj` | 静态/虚方法/构造 | `callvirt` 目标看对象类型；P/Invoke 看 `pinvokeimpl` |
| `ldloc.N` / `stloc.N` / `ldarg.N` | 局部变量/参数 | IL 是栈机，局部变量槽位即 C# 变量 |
| `brtrue/brfalse/br/switch` | 分支 | `brtrue` = 非零则跳；混淆后常见 `br` 链（一层跳一层） |
| `box` / `unbox` / `castclass` | 装箱/拆箱/转型 | `castclass` 失败抛异常 = 类型判断点 |
| `ldtoken` / `typeof` | 元数据 token | 反射操作 token 时警惕动态解密 |
| `ret` / `throw` / `leave` | 返回/异常 | 混淆器爱把逻辑塞进 `catch/finally`，C# 视图可能丢细节 → 切 IL 看 |

## 4. 元数据坑（静默错误高发区）

- **token 结构**：高字节是表号——`0x06`=MethodDef、`0x0A`=MemberRef、`0x70`=#US 堆、`0x02`=TypeDef。`--md` 只接 `0x06/0x02` 类定义 token，`0x70` 是字符串堆偏移不是表行号。
- **#US（User Strings）堆**：`ldstr` 的 operand 是**堆内偏移**，首字节是压缩长度、尾部有终结标志字节——手写解析必须处理压缩整数，且按铁律 11 与 dnSpy.Console `-l IL` 输出逐条对照后才许下结论。
- 混淆器把真字符串搬进资源/加密 blob 时，`ldstr` 全变成索引调用 → 回 §2 的 `--default-strtok`。
- 入口点不一定在 `Main`：查 `<Module>::.cctor`（模块静态构造，先于 Main 执行，反调试/解混淆常藏这里，等价 native 的 TLS 回调）。

## 5. 混淆对抗阶梯（de4dot 不够用时）

| 症状 | 处置 |
|---|---|
| de4dot 报 unknown obfuscator | `-p un --un-name <regex>` 按命名模式跑通用清理；只改名就用 `--dont-rename` 关掉再看 |
| 控制流仍平坦（br 链 + switch 状态机） | `--only-cflow-deob` 单独重跑；仍乱 → dnSpyEx IL 视图手工读 |
| 方法体加密（运行时才解密，静态是空壳） | 转动态：dnSpyEx 调试器断在方法入口看解密后 IL；或 dump 内存程序集回本篇重新分诊 |
| 反调试（`Debugger.IsAttached` 检查） | dnSpyEx 里 Edit Method 改掉检查，或用其"调试器隐藏"选项；改动后样本只用于探索（铁律 10） |
| 虚拟机化混淆（VMProtect.NET/.NET Reactor VM） | 不硬逆 VM：trace 输入输出抓校验点，按 re-dynamic 流程走 |

## 6. 动态与验证纪律

- **dnSpyEx GUI = 唯一动态入口**：断点下在托管方法上直接看 IL/局部变量；Edit Method（C# 级）/Edit IL 改完 Continue 即生效——**改过的运行态只能探路，不能当数据模型证据**（铁律 10）。
- 拿到 flag/密钥类结论：正向跑一遍程序确认（铁律 8 求逆前先正向验证），`ledger.py conclude --source --independent` 标注；Edit Method 后测得的结论必须 `--independent no`。
- 混合体（managed 外壳 + native dll）：native 部分回 ghidra-static，P/Invoke 声明（`[DllImport]`）就是两世界的接口清单。
- 时间盒不变：15 分钟静态无关键路径 → 转 dnSpyEx 动态（铁律 6）。

---
工具上游：dnSpyEx（github.com/dnSpyEx/dnSpy，GPLv3）、de4dot（github.com/ViRb3/de4dot-cex，GPLv3）；IL 语义以 ECMA-335 规范为准。本篇仅参考其用法，未复制正文。
