> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# 反编译伪码陷阱与机械化核查流程

把"读伪码"从靠手感变成可机械把关的工程流程。适用范围：一切打算**引用伪码内容下结论**的场景；纯导航不受本文约束。实测基线（判例H 样本，468 函数 / 2.0 MB 伪码，尾调用已剔除）：**2.8%（13/468）的函数伪码不可直接引用、255 处常量渲染可疑**——撞上陷阱不是运气差，是系统性问题，必须系统化处理。（旧口径 6%（28/468）把 Ghidra 对**尾调用**的 `Could not recover jumptable` 误报也算在内：`JMP reg` 紧邻尾声序列 `ADD RSP,imm`/`POP`×N/`LEAVE` 时是良性尾调用而非跳转表，`decomp_lint.py --binary` 现已自动甄别剔除，本样本剔除 15 个函数。）

## 1. 四层信任模型（L0–L3）

| 层 | 来源 | 用途 | 可承载结论 |
|---|---|---|---|
| **L0** | 原始字节（`read_views.py`） | 常量 / 长度 / 密文 / 密钥的**唯一权威** | ✅ |
| **L1** | 反汇编（`disassemble`） | 跳转表 / 位运算 / 字段序 / 栈槽归属定案 | ✅ |
| **L2** | P-code（`pcode [--high]`） | 语义中间层：无类型推断、无控制流美化 | ✅ |
| **L3** | 伪码（`decompile`） | **只用于导航 + 生成假设** | ❌ 禁止承载结论 |

**硬规则**：写进交付的每条结论必须能追到 L0/L1/L2 证据（地址 + 复现命令）。顺序建议：**伪码导航 → P-code 定位语义 → 汇编定案**；伪码看不懂不要直接跳汇编，先看 P-code 通常更快。

**状态污染警告**：Ghidra 项目是**有状态的**——任何"只读"分析工具只要触发反汇编/建函数（含 `disassemble --force`、`jt_resolve` 的 target 恢复），就会改写项目并改变后续所有测量的基线。**做行为对照实验时，先确认分析动作没有改写项目状态**（对照地址必须是未被任何工具处理过的；必要时用 `list-project-programs` 核对或重建项目做干净对照）。实例：一次"disassemble 已修"的结论就是假象——`jt_resolve` 先前已把该地址强制反汇编并持久化，换干净地址立刻复现旧症状。

## 2. 失败模式表（伪码表现 → 判定 → 核查配方）

| 伪码表现 | 判定 | 核查配方 |
|---|---|---|
| `Could not recover jumptable` + 间接 `JMP` 渲染成间接 `CALL` | ❌ 真失败（语义错误） | `jt_resolve.py` 一键解 + 人工抽查（§3④） |
| `Could not recover jumptable`，但 `JMP reg` 紧邻尾声（`ADD RSP,imm`/`POP`×N/`LEAVE`，可夹 `MOV` 传参） | ⚠️ **误报**：良性尾调用，不是跳转表 | `decomp_lint.py --binary` 自动甄别剔除；判例H 实测 66 处 jumptable 警告中 15 处属此类 |
| **只暴露多张跳转表里的一张** | ❌ 真失败（更隐蔽） | 反汇编搜 `LEA RAX,[0x44....]` + `JMP RAX` 找全部表基址；两张表共用同一索引时**只解一张 = 解错一半** |
| 重叠栈槽同名：`local_3e8` 既是 256 字节缓冲区又是 `{len,ptr,cap}` 结构 | ❌ 真失败 | 按 `[RSP+off]` 手工重建栈帧，变量名永远不可信 |
| 常量渲染漂移：`&DAT_0000xxxx`（小整数/长度渲染成地址）、`case 100:`（实为 `0x64`）、偏移错几字节 | ❌ 真失败 | `read_views.py --expect-hex "<渲染文本>"`，不符则渲染文本**整体作废** |
| 向量化字节比较 `auVar127[i] = -(pcVar1[i]=='D')` | ⚠️ 语义是 `memcmp`，**不能按字面读** | 折叠成 `memcmp(p, "...", n) == 0` |
| 位域/向量拆分 `CONCAT\d\d` / `SUB16x` / `auVar` | ⚠️ 字面值不可信 | 折叠成 `(u16)(...)` / 字段提取 |
| **CALL 之后代码消失 / 函数无调用者 / 大片染灰**：UD2/INT3 落函数体中间切断 fall-through，或 callee 被标 NoReturn 传染所有调用者 | ⚠️ **判定不可信**（铁律 10⑦：自定义信号 handler 可改写保存的 RIP/ucontext，让「非法指令」正常返回） | `noreturn_fix.py <bin>` 体检（terminal 含 UD2/INT3 的才可疑，exit/abort 合法）→ `--fix <func>` 清 NoReturn / `--flow <addr>` 补 fall-through override → 重反编译调用者验证（判例 4307cc95：误判 flag 路径不可达丢 86 min） |
| **同值二选一条件赋值**：`if (cond == 0) p = ptrA; else p = ptrB;`（两分支赋同类型量，cond 来源不明） | ⚠️ **先假设它有语义**（奇偶分支/轮次分支/模式切换），不许当生成器噪音跳过 | 在数据上验证一次（钉 cond 看行为差异）再决定忽略；chal 复盘 E2：这就是"偶数轮交换中间两字"的 MA 回写，当噪音跳过后多烧 ~10 min |
| **生成产物临时槽复用**：Cython/自动生成的 C 里 `plVar8`/`local_198` 在不同语句被复用成不同语义 | ⚠️ **变量名无权威性**——角色用元数据（ctf-patterns §12.1 `co_varnames`）或扰动实验（铁律 14）钉，不用名字猜 | **作用域**：仅限自动生成/优化/混淆产物（Cython 包装、Go、Rust、strip 重命名、VM 混淆）；有 DWARF/PDB/未 strip 符号时变量名基本可信，照常使用 |

注意对称教训：伪码里看着诡异的**也可能是忠实的**（"5 次递归子调用"复核后是真 `CALL` 指令）——归因于工具之前先复核（见 §4 第 6 条）。

## 3. 五阶段流水线

**① 体检**（先做，别跳）：`decompile-all` → `decomp_lint.py all.c --binary <bin>` → 拿 fatal 函数清单 + 危险渲染计数（`--binary` 启用尾调用甄别：尾声后的 `JMP reg` 是良性尾调用，单列不计入 fatal）。**fatal 清单内的函数禁止读伪码**，直接走 L1/L2。

**② 修视图**（读之前先修）：`set-signature` / `set-calling-convention` / `create-struct` / `retype-variable` / `rename-function`。**迭代**：标对一层类型，噪声成片消失（`undefined` 类型是主要靶子），每修一处重新反编译看一次。总原则：不要"读"烂伪码，要"造"好伪码——类型信息能改善；控制流恢复基本不能（只能识别并回退汇编），**例外是分析器误判型截断**：UD2/INT3 切断 fall-through、NoReturn 标志误传染，这类用 `noreturn_fix.py` 直接修视图（清标志 / 补 override），修完重反编译即可恢复。

**③ 骨架化去噪**：向量化比较 → `memcmp`；std 样板（`find` 两路搜索、Vec 增长、`expect` panic 桩、bounds check）→ `skip`。**判据**："每个字符都读懂了但不知道在干嘛" = 这一层——识别形状，不要读实现。

**④ 定点核验**（fatal 处与常量处）：
- 跳转表：`jt_resolve.py <bin> <分发点>` 一键解【所有】表基址 + 人工抽查。**CFG 交叉验证有前置条件**：Ghidra 没恢复跳转表时 case 体往往尚未反汇编，target 全落「未反汇编间隙」，CFG 校验无从谈起——先对 target 强制反汇编（`disassemble <addr> --force`），能恢复才做 basic-block 交叉验证；恢复不了就用「索引范围 + 目标区间连续性」作为替代判据。只解一张 = 解错一半
- 常量/长度：一律走 `read_views.py --expect-hex/--expect-len` + `const_audit.py` 扫渲染嫌疑，过不了的过 `crypto_sanity.py check`（长度不合法 exit 2 = 第一嫌疑人是读数）
- 栈槽归属：`frame_map.py <bin> <func>` 出槽位归属表（同槽多宽度自动标可疑）；手工对照时从入口 `SUB RSP,0xNNN` 起算全部 `[RSP+off]`

**⑤ 执行验证**（终极）：**能观测就别推断**。叶子函数 → `emulate-function`；整程序带 I/O → ghidra-core `references/unicorn-harness.md`；最终交付验证 → Wine/真机。

## 4. 质量门 6 条（任一不过，禁止引用该伪码）

| # | 门 | 检查方式 |
|---|---|---|
| 1 | 函数无 fatal 告警 | `decomp_lint.py` |
| 2 | 引用的每个常量都过了 L0 权威读数 | `read_views.py --expect-*` |
| 3 | 每个跳转表的**所有**基址已解并交叉验证 | §3④ a/b/c |
| 4 | 同一区域二次回访带 `--delta` | `ledger.py observe` |
| 5 | 承重结论有执行验证或字节验证 | §3⑤ |
| 6 | **归因 / 更正 / 撤回也有证据** | 配一条能证伪它的命令 |

第 6 条是活教材：一处复盘里两处"反编译器的错"复核后只有一处成立，另一处是自己噪声拟合。**「我觉得应该更正/撤回一下」比「这是工具的错」更容易被放过**——它披着自我批评的外衣（同一失效模式在 判例H 连撞 4 次：递归调用归因、跳转表项数、漂移归因、更正后的地址也错）。归因、更正、撤回本身都是结论，都要验证。

## 5. 决策树（什么时候根本不该读伪码）

```
任务需要"它做了什么"（可观测）     → 直接执行（§3⑤），伪码只用来定位入口
任务需要"它怎么写的"（要改/复现）  → 走完整五阶段
候选空间可枚举（N 调用点 × 独立槽）→ 探槽独立性（call_histogram.py 数直方图 + 逐位翻转），独立就逐槽枚举，绕开语义阅读
函数在 fatal 清单里               → 禁止读，直接 L1/L2
同一段读第二遍仍不确定             → 停，落 ledger，换层
```

## 6. 配套脚本（ghidra-core/scripts/）

| 脚本 | 用途 |
|---|---|
| `decomp_lint.py` | 阶段①：fatal 清单 + 危险渲染计数 |
| `call_histogram.py` | 决策树：CALL 目标直方图定位重复调用点 |
| `read_views.py` | L0 权威读数 + `--expect-hex/--expect-len` 对照 |
| `jt_resolve.py` | 阶段④：跳转表全基址一键解析（替代手工解 rel32） |
| `frame_map.py` | 阶段④：栈帧槽位归属表，同槽多宽度自动标可疑 |
| `const_audit.py` | 阶段④ + 质量门 #2：伪码常量渲染嫌疑扫描 |
| `noreturn_fix.py` | non-returning/UD2 截断修复：体检 NoReturn 函数 + 流切断点，`--fix` 清标志、`--flow` 补 fall-through（铁律 10⑦ 的修复侧） |

## 7. 一页速查

```
① 体检   decompile-all → decomp_lint.py --binary → 拿 fatal 清单（尾调用已剔除），先排除那 2.8%
② 修视图 set-signature / create-struct / 重命名 → 重新反编译（迭代，标对一层噪声成片消失）；
         UD2/NoReturn 截断 → noreturn_fix.py 体检 + --fix/--flow 修视图
③ 骨架化 向量化→memcmp、std 样板→skip、panic 桩→skip（识别形状，不读实现）
④ 定点核 跳转表 jt_resolve 一键解【所有】基址（target 落间隙先 disassemble --force 再 CFG 验证）；
         常量 read_views --expect-* + const_audit；栈槽 frame_map
⑤ 跑它   能观测就别推断：叶子 emulate-function / 整程序 emulate_program.py / 最终 Wine
门禁     无 fatal / 常量过 L0 / 表全解 / 回访带 delta / 承重结论有执行证据 / 归因·更正·撤回也有证据
```

---

*素材来源：`Desktop/fupan/历史复盘` §9（四层信任模型 / 失败模式 / 五阶段流水线 / 质量门 / 决策树，数字为该样本实测基线）。*
