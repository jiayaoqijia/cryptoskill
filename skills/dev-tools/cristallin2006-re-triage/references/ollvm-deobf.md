> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# OLLVM 反混淆专项（工具选型与执行）

> **分工边界**：本篇管 OLLVM（bcf/fla/sub-MBA）的**工具级执行**——选型决策、手工 deflat、MBA 化简脚本。
> 识别特征、分层顺序（bcf→fla→sub）、通用原则（GOOMBA、Goron/Arkari 数据段只读）看 anti-analysis.md §4，本篇不重复；
> 反调试/自校验看 anti-analysis.md §2/§5；动态仿真接管（Qiling/Unicorn 全家桶）看 re-dynamic。
> 全程观察/结论走 ghidra-core `scripts/ledger.py observe` / `conclude` 落账。

> **路径约定**：`$RP` = re-tools-venv 的 python（Windows `~/Desktop/src/re-tools-venv/Scripts/python.exe`；Linux `~/re-tools-venv/bin/python`）。gdb 走 WSL。

## 1. 三类混淆识别复核（先确认再选工具）

| 混淆 | 快速确认信号（一条即实锤） |
|---|---|
| bcf（虚假控制流） | 块数膨胀 3 倍以上，且大量分支条件是 `x*(x+1) & 1` 这类**与输入无关的奇偶式**（不透明谓词），else 侧是永不执行的垃圾块 |
| fla（控制流平坦化） | CFG 呈**星形**：一个 dispatcher 块（大 switch 或 if-chain）被几乎所有块回边指向；反编译出 `while(1){ switch(state){...} }`，`state` 即状态变量 |
| sub/MBA（算术膨胀） | 单行伪代码含 ≥4 层嵌套的 `^ & \| ~` 混合运算，且常量项成对出现（`(x^y)+2*(x&y)` 形态），查等价式表（anti-analysis.md §4）能对上 |

## 2. 工具选型决策表（按架构 × 有无 IDA 分流）

| 你的情况 | 首选 | 备选 | 本机现实 |
|---|---|---|---|
| 有 IDA 7.5+ 联网、不敏感样本 | obpo-plugin（microcode 级，效果最强；**云插件会上传函数二进制**） | d810-ng | ✗ 本机无 IDA |
| 有 IDA、样本敏感需本地 | d810-ng（Z3 集成，OLLVM/Tigress/Hodur/Approov 多变种） | GOOMBA | ✗ 本机无 IDA |
| 有 Binary Ninja | ollvm-breaker（ARM .so 实战向） | — | ✗ 本机无 BN |
| 无 IDA/BN，x86/x64，纯脚本 | **angr 符号执行 + 手工 patch（本机主力路径，§3/§4）** | Miasm ollvm-unflattener（未装，勿现配环境） | ✓ `$RP`（angr 在 re-tools-venv，Tier B） |
| ARM64 .so，无 IDA | gdb(wsl) 手工 deflat（§3）→ Unicorn 仿真验证 | qiling(wsl) 整体仿真 | ✓ gdb/unicorn/qiling 均在注册表 |

> 变种警示：Pluto/Polaris 带 Trap Angr pass（符号执行路径爆炸）——angr 跑了 10 分钟无收敛先怀疑中招，转动态；Goron/Arkari 间接跳转先设数据段只读（anti-analysis.md §4）。

## 3. fla 手工打法（gdb 断点采状态序列 → 重建 CFG）

通用原则与分层顺序见 anti-analysis.md §4；这里给可直接跑的操作序列。

1. 定位：Ghidra 里找 dispatcher 块与状态变量（通常是局部变量，在 switch 前被反复赋值），记下**状态变量比较点**地址 `CMP_ADDR`。
2. 采集（WSL）：

```gdb
wsl gdb -q ./target
(gdb) b *CMP_ADDR
(gdb) commands
> silent
> printf "state=0x%x\n", $eax    # 换成状态变量实际所在寄存器/栈槽
> c
> end
(gdb) run < input.txt > state_trace.log
```

3. 重建：把 `state_trace.log` 按序排成 `块地址 → 后继块地址` 映射（每个真实块末尾对状态变量的赋值 = 它的真实后继）。
4. 落地二选一：
   - **patch 法**：把每个真实块末尾改成直接 `jmp 真实后继`，nop 掉回 dispatcher 的跳转；dispatcher 整块留作死代码。
   - **分析辅助法**：不 patch，拿映射表在 Ghidra 里人工连边读伪代码（样本有自校验时用这个，见 anti-analysis.md §2 自校验行）。
5. 嵌套 fla：内层状态机与外层的 dispatcher 不同地址，回到第 1 步对新 dispatcher 迭代（anti-analysis.md §4 已述）。

## 4. MBA 化简（angr/claripy 实操）

等价式表在 anti-analysis.md §4，查表能命中就直接替换伪代码；查表不命中时用 claripy **验证**候选等价式，不要盲换：

```bash
"$RP" - <<'EOF'
import claripy
x, y = claripy.BVS('x', 32), claripy.BVS('y', 32)
orig = (x ^ y) + 2 * (x & y)          # 从伪代码抄下来的膨胀式
cand = x + y                           # 候选化简结果
s = claripy.Solver()
s.add(orig != cand)
print('EQUIVALENT' if not s.satisfiable() else 'NOT equivalent')
# 快速看一眼化简形态（化简能力有限，不等价于证明）：
print(claripy.simplify(orig))
EOF
```

- 位宽必须与汇编一致（32/64 位搞错会误判等价）。
- 输出 `NOT equivalent` → 候选错了，回等价式表换一条再验；**未验证的替换禁止写进结论**。

## 5. 时间盒与升级（挂铁律 6）

- 单函数手工化简**超过 2 轮（采集→重建为一轮）仍无进展** → 停手，转动态 oracle：用 Unicorn/qiling 直接仿真该函数，喂输入抓输出当 ground truth（re-dynamic 篇），不再纠缠 CFG 还原。
- angr 路径爆炸/10 分钟不收敛 → 怀疑 Trap Angr（§2 警示），同样转动态。
- 每次切换路线前 `ledger.py conclude` 记"静态已卡死 + 卡点证据"，避免下一个人重走。

---

署名：§2 决策表结构参考 github.com/zhaoxuya520/reverse-skill（MIT License）`skills/reverse-engineering/references/ollvm-deobfuscation.md`，内容按本机工具链（无 IDA/BN，angr+手工为主）重写。
