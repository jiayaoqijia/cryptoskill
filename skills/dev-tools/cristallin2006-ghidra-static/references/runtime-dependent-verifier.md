> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# 运行时依赖型校验（runtime-dependent verifier）

校验所期望的输入依赖**进程运行时状态**（PID、/proc/self/*、ASLR 基址、rdtsc、
clock_gettime、environ/argv、栈地址）时的分解配方。核心一句话：

> **runtime 依赖 ≠ 无解。把计算分解为「运行时前缀」×「确定性变换」：
> 前缀找塌缩点枚举掉，变换离线逆，运行时值从活进程内存现读。**

## 识别信号

静态期看到以下组合，立刻怀疑本模式（落 ledger observe）：

- imports/xrefs 含 `getpid|getppid|gettimeofday|clock_gettime|rdtsc|sysinfo|uname`
- 字符串/常量含 `/proc/self/stat`、`/proc/self/maps`、`/proc/self/exe`、`[stack]`
- 校验输入疑似依赖内存布局：栈地址、映射基址（`>>12` 页号化是典型指纹）
- 同一候选输入**跨 run 结果不同**（动态期确认信号——但先排 harness 噪声，
  见 re-dynamic §4②；同 run 内复跑一致 + 跨 run 不一致 = 运行时依赖实锤）

## 分解步骤

### ① 沿熵源数据流找「塌缩点」

运行时值从被读入到参与比较，中间一定被加工。沿数据流追，找**空间骤减点**：

- `& mask`（如 `& 31` → 32 种）、`% N`、取字节/取位域
- 作为表索引/选择子（selector）——表有多大，可能性就只剩多少
- 进 hash 后再取小字段（hash 本身不塌缩，取低 5 bit 才塌缩）

塌缩点识别动作（逐个问，不许跳过）：

- 把每个 runtime 依赖的字节/槽位列出来，逐问「它有几个可能取值？」
- 传给 hash 的**单字节参数**（栈上 `[rsp+0xNN]` 的 1B 槽位进 hash 调用）
  几乎必是 selector——`hash(...||byte(s))` 里 s 的取值数 = 枚举空间
- `% 小常数`、`& (2^k-1)`、交织表/分片表的列号 = 同上
- 「runtime 值进 hash 后取字节当索引 ⇒ mask/key 只是 selector 的函数」
  是本模式最高频形态：`answer = offline[selector] ⊕ live_mask`（见 ④）

**塌缩点未找到前，③④不许开工**（读了消耗点的值也不知道该读哪个分支）。

**塌缩后空间 ≤ 2^16 ⇒ 枚举离线化**：对每个候选 selector 各算一份答案，
运行时确定 selector 后直接查表。找不到塌缩点、空间确实大（全 64 bit 参与）
→ 进 ②，但先落 `ledger.py stuck` 声明「塌缩点未找到」再走下一步。

### ② 确定性变换离线逆

#### 前置决策：比较目标随 run 变 ⇒ 离线求解全灭，只许同进程

两次**不修改二进制的裸跑**，若比较点期望值（memcmp 另一侧/等价目标）不同
⇒ 目标本身是运行期派生（PID/starttime/栈地址进链）。此刻立即成立：

- 离线求出的任何静态输入都必然失败——它对的是旧 run 的目标。
  **SMT/angr/手逆固定目标整个路线类全灭，不许再写进 stuck --escalate**
  （活跃 negative conclude 在场时 ledger stuck 会机械拦，判例 a0f3be66：
  「目标随 run 变」落账后 136 秒仍升级离线 angr 求解，35 分钟空转）。
- 唯一活路是**同进程求解**：断在「目标已算好」之后、比较之前，读本 run 的
  目标/轮数据/派生料，在进程内（或对着刚读出的活值）反序跑轮/反向代入
  求 X；拿到 X 后两选一——(a) 同进程投喂（写输入缓冲/gdb call/rewind），
  (b) 若 key 链已完全映射，**直接自己算 flag，不需要让闸门通过**。
- 输入消费点早于目标计算点也没关系：用任意输入跑到目标点抄料，逆出 X
  后直接走路线 (b) 算 flag——flag 由静态密文 + 活值派生，不必重跑。

塌缩点之后的计算（混淆再重也是）只依赖 input + selector，与进程无关：

- ARX / Feistel / 查表置换：检查各步是否满足可逆条件；查表非双射、截断、偶数模乘等可丢信息，按实际结构选择反推或 SMT
- 真不可手逆 → SMT，但先过剥离闸（gate_smt：peel_inverse.py → cone_invert.py）
- 「40KB 混淆 blob 不可建模」通常是误判——blob 里 runtime 前缀往往只有几行，
  其余全是确定性部分。**先把前缀从 blob 里切出来，再谈可不可建模**

#### 可逆性先判结构，再看原语（见到 hash / 雪崩不许直接判死刑）

「链里有 N 次 SHA-256 调用」「单字节翻转全雪崩」都**不是**单向证据：

- **非线性 ≠ 不可逆**。Feistel / SPN 全非线性且整体可逆；仿射性检验
  （`f(a)^f(b)^f(0) == f(a^b)`）被证伪只排除线性，不排除可逆。
- **Feistel 的轮函数单向也整体可逆**：逆 = 反序跑轮，永远不需要逆轮函数。
  识别指纹：状态分半 + 每轮交换 + 直线 blob 里的短回跳簇（轮循环）+
  轮密钥来自可读取的内存。
- **区域里有 hash 调用 ≠ hash 在待逆数据流上**：先画调用图确认 hash 在
  input→answer 的必经路上，还是在建平行的 context/nonce/tag。
- **真单向只有一类**：输出被压缩/截断（digest 直接当答案、mod 小空间、
  丢位）。没见到截断点之前，「不可逆」结论不予成立。

三个廉价结构侦察动作（合计 <10 min，做完才允许谈工作量）：

1. 数链上 `call` 目标清单 → 识别原语（SHA / ChaCha / AEAD / 自写 mixer）
2. 数短回跳簇 → 轮结构计数（轮数 × 单轮成本 = 求逆总成本）
3. 画数据流二分：哪些 buffer 依赖 input，哪些只依赖 runtime/常量

「链太大 / 要数小时」是工作量估算，不是否定结论——结构侦察未做完，
不许用估算当放弃理由；真要下否定结论走 `conclude --kind negative --proof`
（交付物 write/present 里出现「不可求逆/不可建模/unsolvable」类判词而台账
无 negative 落账 → **gate_deliver 机械拦**；判例 c3964a8b：读完本节 8 分钟后
仍以「链上有 SHA-256 → 非线性 → 不可求逆」交卷，故升格为机械门）。

### ③ 运行时值现场读（不要自己复现熵源）

程序自己会把 mask/selector/key 算好放在内存里。**断在消耗点，直接读**：

- 消耗点：memcmp/逐字节比较前、AEAD/crypto setkey 前、write 输出前
- `gdb -batch` + 断点 + `x/16xb <addr>`（模板：re-dynamic `scripts/gdbkit.py`）
- **要的是本 run 自洽，不是跨 run 可复现**——别去禁 ASLR / 冻结时间 /
  固定 PID，那是把简单问题做难。`setarch -R` 失败不等于此路不通

### ④ 组装与投喂

```
answer = offline_candidate[selector] ⊕ live_mask     # 典型形态，按实际组合
```

投喂时机必须在本进程内（selector/mask 是进程实例的函数）：
断点抄值 → 算 answer → 喂给**同一进程**（gdb `call`/写输入缓冲区/下一轮交互输入）。

## 反模式（全部有实盘判例）

1. **题名/题面暗示 glitch/不稳定/故障 ⇒ 把跨 run 不一致判为「故障注入污染、
   不可解」**：题名是叙事不是机制。跨 run 不一致的第一解释永远是「runtime
   依赖」并走 ①；判「污染/不可解」是否定结论，走 `conclude --kind negative
   --proof` 硬门（多数证不出来）。
2. **就地哈希误判为「数据被写坏」**：buffer 先存 hash 输入描述符（domain
   指针 + 数据指针 + 长度），随后被 digest **就地覆盖**——这是 in-place
   hash 的正常写法，不是 glitch 把表写坏了。看到「指针数组被 hash 输出覆盖」
   先重读数据流，别下污染结论。

3. **force compare / patch 中间值当主路**：比较点改过去，下游用不一致状态
   重驱动，以内部一致性检查 abort（如 `_exit(自定义码)`）。patch 态只能
   用于探索控制流，不能产出验证数据（re-dynamic §4①）。
4. **「需要可复现 run」谬误**：禁 ASLR/冻时间失败 → 宣布不可解。
   正确问题：「程序算好的那个值，我能不能在消耗点直接读出来？」
5. **runtime 前缀当黑盒整体放弃**：不找塌缩点就下「不可建模」结论——
   这是否定结论，走 `conclude --kind negative --proof` 硬门，多数情况证不出来。
6. **对熵源本身建模**：去模拟 /proc 格式、预测 PID 分配——程序自己会读，
   你只需要读它读完的结果。
7. **雪崩 + 区域内有 hash 调用 = 判单向**：非线性 ≠ 不可逆（Feistel/SPN
   皆非线性可逆，仿射检验证伪不算数）；hash 调用可能在平行的
   context/nonce 上而不在待逆数据流上；真单向只在输出截断时成立——
   见 ② 的可逆性结构判定。
8. **已落账「目标随 run 变」仍升级离线求解**（判例 a0f3be66）：negative
   落账 ≠ 路线类自动关闭。escalate 前必须先过 ② 的前置决策；ledger stuck
   在活跃 negative 在场时机械拦，用 --ack-negatives 逐条说明升级路径为何
   不被覆盖——说不清就是不该走。

## 时间盒

- 塌缩点搜索 15 min 无果 → `ledger.py stuck`（gate_stuck 下游换路校验会查）
- 枚举空间 > 2^16 且无塌缩点 → 升级：全文反编译变换链 / 问人
