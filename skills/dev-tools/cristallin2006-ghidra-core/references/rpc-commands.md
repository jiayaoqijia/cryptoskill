# Ghidra 执行接口

按当前命令查参数；下列宿主脚本路径保留兼容包装，通用状态见 analysis-session。方法选择由模型决定。

## 5. 能力清单（三层）

通用约定：`rpc_driver.py` 的 `[@out文件]` 恒为第一个参数；函数定位支持 `0x地址` / 精确名 / 模糊子串；写操作即刻生效并自动存盘。

### 第 1 层：rpc 命令（主力，`python rpc_driver.py <命令> <binary> [参数]`）

| 命令 | 用途 |
|---|---|
| `ensure` / `status` / `stop` | daemon 与二进制生命周期（ensure 幂等） |
| `triage` ◆ | 一键分诊报告（本 skill 入口） |
| `metadata` / `imports` / `exports` / `memory-map` / `relocations` | 程序元数据 |
| `functions` / `decompile`（`--format text` 顶层直接给 `text` 键，失败 `error` 带原始异常原文）/ `decompile-all` / `search-decompiled` | 函数与伪码 |
| `disassemble`（`--force` 在请求地址强制解码——跳转表 target 未反汇编时用，否则只会前跳到下一条已有指令 + warning）/ `assemble` ✎ / `basic-blocks` / `pcode` | 汇编/CFG/P-code |
| `strings` / `symbols` / `find-bytes` | 搜索 |
| `xrefs-to`（`--follow-fatptr` 自动追 Rust/Go {ptr,len} 描述符第二跳，hop=2 + via=描述符地址）/ `xrefs-from` | 交叉引用 |
| `read-bytes` / `read-pointers` / `write-bytes` ✎ | 内存读写（write-bytes 已对齐 patch_bytes 语义） |
| `rename-function` ✎ / `rename-symbol` ✎ / `batch-rename` ✎ / `set-comment` ✎ / `batch-set-comment` ✎ / `set-signature` ✎ | 标注 |
| `create-struct` ✎ / `create-enum` ✎ / `modify-struct` ✎ / `set-data-type` ✎ / `apply-data-type-range` ✎ / `set-equate` ✎ | 数据类型 |
| `retype-variable` ✎ / `rename-variable` ✎ / `batch-edit-variables` ✎ / `set-calling-convention` ✎ / `set-thunk` ✎ / `create-function` ✎ / `create-label` ✎ | 深度修改 |
| `version-track` / `function-diff` / `match-function` | 二进制比对（Auto VT + BSim） |
| `list-vtable` / `get-processor-context` / `set-processor-context` ✎ | C++/ISA 上下文 |
| `tag-function` ✎ / `list-tags` / `functions-by-tag` / `set-bookmark` ✎ / `list-bookmarks` | 进度标记 |
| `exec-code` ◆⚠ | 逃生舱：daemon 内 exec Python 文件（预置 program/find_function/output_json；无沙箱） |
| `export-binary` ◆ | Original File 导出 + md5 对比 |
| `emulate-function` ◆ | EmulatorHelper P-code 仿真（寄存器/内存预置，call-depth 追踪） |
| `exec-code` + `scripts/unreferenced_funcs.py` ◆ | 零调用方函数清单（藏 flag 的第二函数）：`python rpc_driver.py [@out] exec-code <binary> "$SK/unreferenced_funcs.py"`；`--reachable-from <root>` 做可达性过滤——daemon 下脚本参数走 `DSH_UNREF_ARGS` 环境变量（须在 ensure/启动 daemon 前导出）；排除 thunk/external/entry-export 根 |
| `exec-code` + `scripts/unreferenced_data.py` ◆ | 零引用数据块清单 + 置换/密钥材料分类 + 相邻块跨度合并（藏置换表/S-box）：`python rpc_driver.py exec-code <binary> "$SK/unreferenced_data.py"`；daemon 下脚本参数走 `DSH_UNREF_DATA_ARGS` 环境变量（须在 ensure/启动 daemon 前导出）；`--min-size <n>` 调阈值，`--include-referenced` 全量 |

◆ = dsh 自定义工具（`engine/ghidra-rpc/ghidra_rpc/server/tools/dsh_tools.py`）。✎ = 写操作。⚠ = 无沙箱。
完整命令与参数：`~/Desktop/src/ghidra-bridge/ghidra-rpc-venv/Scripts/ghidra-rpc.exe --help`，或 `engine/ghidra-rpc/docs/` + `engine/ghidra-rpc/README.md`。

### 第 2 层：宿主工具脚本（◈ 直接 python 运行，不经 daemon/driver）

| 脚本 | 用途 |
|---|---|
| `rpc_driver.py` | 统一入口：项目映射/key 替换/@out/环境自给 |
| `ledger.py` ◈ | 旧二进制台账兼容入口；实现已移至 runtime/analysis-v1，格式与新字段见 analysis-session 的 legacy-ledger.md |
| `read_views.py` | **铁律 8 权威读数**：三视图读字节（hexdump/fromhex-ready hex/cstr）+ `--expect-len`/`--expect-hex` 一致性检查（失败 exit 2） |
| `crypto_sanity.py` | **铁律 9 求逆闸门**：`check`（常量长度/格式合法性：hex 偶数、base64 %4、流密码等长）+ `check-result`（反推结果可打印性/格式），违规 exit 2 禁止求逆 |
| `launch_gui.py` | detached 拉起 Ghidra GUI，可直接打开项目 |
| `doctor.py` | 环境自检（8 项：安装/JDK/双 venv/工作区/项目/rpc 包/daemon 起停），全绿 exit 0 |
| `venv_health.py` | **venv 健康（装了≠能 import）**：各工具 venv 关键包真实 import 探针 + angr≥10 内置 claripy 自洽检查，附可照抄修复命令；要用 angr/z3 的局开工先跑 `--quick`，exit≠0 先修（判例 a0f3be66） |
| `guarded_run.py` | **长任务保护执行器（timeout ≥300s 的计算任务必须走它）**：逐行 tee 落盘（杀掉也有部分结果）+ 静默心跳 + terminate→kill 两段终止；`--timeout N --log F -- cmd`；超时退出码 124。替代裸 `timeout N python3 x.py > log`（块缓冲+SIGTERM 丢光输出，chal 复盘） |
| `pe_info.py` ◈ | PE 分诊：头/节表/熵/导入表/资源；PE32 与 PE32+ 双路径（ImageBase 与导入 thunk 宽度都按位数分派）。`python pe_info.py <exe>` |
| `decomp_lint.py` | **伪码体检（读伪码之前先跑）**：输入 decompile-all 的 @out JSON，输出 fatal 函数清单（跳转表未恢复等，这些函数禁止读伪码）+ 危险渲染计数；有 fatal exit 2。加 `--binary <bin>` 启用**尾调用甄别**（审计 A5：尾声 `ADD RSP,imm`/`POP`×N/`LEAVE` 后的 `JMP reg` 是良性尾调用，Ghidra 误报 jumptable，单列不计入 fatal；判例H 实测基线由 28/468=6.0% 修正为 13/468=2.8%，剔除 15 个尾调用函数） |
| `call_histogram.py` | CALL/JMP 目标直方图：从反汇编里数出"重复调用点"（≥3 次高亮 = 疑似分发器/校验体骨架），Rust/内联 main 场景的开工第一个动作（ctf-patterns §4） |
| `emulate_blob.py` | 裸 blob Unicorn 仿真骨架：`--base/--entry/--rsp/--max-insns/--reg/--map-file/--dump-dir`（`--entry` 是相对 `--base` 的偏移），停止原因分类 + dirty 页 dump；exit 0 跑完 / 2 用法错 / 3 unicorn 缺失（提示进 re-tools-venv）/ **4 harness 配置错**（blob 不可读或为空、未知 `--reg`、映射失败、**入口未映射**——不误报 RET 飞出）（多层载荷题用，ctf-patterns §10） |
| `const_scan.py` | Cython/C 常量重建：扫反编译 C（或 decompile-all @out JSON）的 `PyList_New(n)`/`PyTuple_New(n)` + 随后常量写入，重建 Python 字面量；小整数聚集自动告警"疑似字节级常量表"；`--binary <样本>`（须先 ensure）把 `<DAT_…>` 缓存 PyLong 引用还原成 Python 值，CPython 布局自动投票（`--py 311/312` 强制）（chal 复盘 T3：L 表 48 项实测定位+还原） |
| `xor_scan.py` | blob 变换搜索：单字节 XOR 全扫 + 可选滚动密钥/ADD/SUB，按可打印率+magic（MZ/ELF/PK/UPX!）+flag 正则综合评分排 Top N；`--dump <key>` 落地解密产物（判例F·缺口4，不要再现场手写第 5 版） |
| `emulate_program.py` | **整程序仿真**（emulate_blob 的上层）：PE 装载 + IAT 桩（88 个内建 Win32 stub，ABI 陷阱已正确实现）+ 喂 stdin + 成功/失败断点；`--trace-api` 排障、`--dump-state` 取状态。console 型校验程序专用（边界见 docstring）；判例H 实测 0.047s 跑到成功分支（unicorn-harness.md 的可执行形态） |
| `jt_resolve.py` | 跳转表一键解析：LEA+JMP 线索 ∪ decompile 警告 ∪ 伪码残留三路并集找**所有**表基址，rel32/abs32 双模式解 target，basic-blocks CFG 交叉验证；只解一张 = 解错一半（判例H 实测双表全解） |
| `frame_map.py` | 栈帧槽位归属表：`SUB RSP` 定帧 → 扫 `[RSP+off]` 首写/宽度/读写次数；同槽多宽度标可疑（伪码 `local_XXXX` 重叠命名的真身） |
| `const_audit.py` | 伪码常量对照审计：`&DAT_0000xxxx` 小整数嫌疑（判例H 实测抓到 `&DAT_00000007` = 长度 7）、`DAT_` 引用实际字节对照、指针化字面值漂移判定（注意：指向字符串中部的真实 `LEA` 立即数**不是**漂移，工具已加反汇编引用抑制） |
| `model_diff.py` ◈ | **铁律 10② 分歧指纹产出**：模型实现 vs 真实 oracle 命令随机对拍 N 组（`--input-gen hex:N/dec/ascii:N`，确定性 `--seed`），首个分歧给 hex 对照 + 指纹分类 + mismatch 率汇总。判词优先级**宽度级 > 字节级 > 无规律**：宽度级（按 2/4 字节块）高低半块交换 / 低半块全对+高半块 XOR·加法恒定（chal 形状）/ 单侧半块恒为常量；字节级低 nibble 全对 / nibble 交换 / 单常量差 / 全体偏移固定值 —— 以上全部判疑似接口/搬运错，宽度级命中**绝不**落"疑似算法错"；仅"完全无关"判疑似算法错。exit 0 全一致 / 2 有分歧 / 3 命令错误。纯本地子进程工具，不经 daemon |
| `oracle_family.py` ◈ | **铁律 14 打桩 oracle 家族（单因子隔离）**：binary + `--stub 0xaddr=0xval`（可重复）批量产 patched 副本（x86-64 函数头写 `mov eax,imm32;ret`，`--rax` 用 imm64 形式）逐个运行出差分表：输出变 ⇒ 该因子参与计算；已测常量/输入/路径下不变 ⇒ 未观察到影响，不能证明全局无关。`--addr-is va`（默认，ELF 按 program header、PE 按节表+ImageBase 换算，可用 `--dry-run` 只验换算不 patch）/offset；非 x86-64 exit 3；exit 0 全部跑完 / 2 有副本运行失败 / 3 用法/架构错误 |
| `ssa_trace.py` ◈ | **Cython/CPython 扩展 SSA 数据流追踪器**（ctf-patterns §12.2 工具形态）：int 子类包裹（`+ - * ^ & | << >> % //` 自动落账成事件流）+ import 前 builtins 记录包装（`--observe-builtins`）+ `random.*`/`os.urandom` 钩子（`--pin-urandom`/`--seed` 做 §9 角色判别）；`--class CLS --ctor-input 'A*48' --wrap m1,m2 --out trace.json`。exit 0 正常 / 2 用法错 / 3 加载失败。stdlib only，不经 daemon（Reverse-chal 复盘分水岭：8 min 拿 ARX 递推结构，替代手读生成 C） |
| `ssa_reconstruct.py` ◈ | **SSA 事件流→直线程序重建 + 裸字面量解析**（§12.2 后半链，吃 ssa_trace 的 trace.json）：产出可读直线程序（行格式与 peel_inverse 输入约定一致），高频裸字面量用 identity/sw/sw<<16/位移/*16 + `sw(a)<<16|sw(b)` 打包四式逐一试解，解不出标 ?? 交人工不猜——Cython 值 C 化断链处"神奇常数"的归位器。exit 0 正常 / 2 输入错。stdlib only，不经 daemon |
| `peel_inverse.py` ◈ | **铁律 6 工具形态：求逆前先查依赖图**（吃 ssa_reconstruct 的直线程序）：找 `& 0xffffffff` 掩码变量的依赖结构，检出"滞后-2 递推段"（mask_i 只依赖前两个）→ `--emit-solver peel_solve.py` 生成可运行剥离骨架（f0/f1 探针自动判加法/异或反解，前向重放自验），填 KNOWN（段末两掩码目标值）/CALL_TABLES（查表函数）/SEEDS（种子实测值）后运行即逐层反解；**骨架 0 次填写/运行 = 未过闸（4ccec36c）**；无干净结构转 cone_invert.py，仍不通才放行 SMT。exit 0 判定完成 / 2 输入错或骨架缺料（指名缺哪个变量）。stdlib only，不经 daemon |
| `cone_invert.py` ◈ | **阶梯 ①' 通用锥形反推**（peel 无递推段/段非目标时的下一档，4ccec36c 复盘产物）：吃同一份直线程序，`--known 名=值` 锚点起步逐语句反向传播——`d=a OP b` 已知 d+单操作数精确反解另一个（+/-/^/全 1 掩码 & 精确；<</>>/|/%/非全 1 & 有损指名交人工），`d=fn(args)` 缺一个参数用 `--calls` 的 CALL_TABLES 前向实现爆破（默认域 2^16，`--brute fn=N` 可调）；模派生值自动带 mod 传播防误杀；**矛盾检出 exit 1 分两类判词**：① 矛盾锥含未知量 = 方程/常量错了（铁律 9 禁止续命）；② 矛盾锥全被字面量决定、无未知量 = **输入符号化不完整**（29bf99c0 判例），指引走 `--diff-symbolize reconB --out asym.txt`（同长度不同输入两份 recon 按值集合 diff——A 有 B 没有的字面量即随输入变化，自动符号化为 IN0..INK；不按行号，控制流差异导致行数错位也能用；`--min-lit` 默认 256 防误符号化结构小常量）补全后重跑；断链点（缺 CALL_TABLES/爆破域小）无论变量是否已从他路解出都单列缺料警告。exit 0 收敛 / 1 矛盾 / 2 输入错。stdlib only，不经 daemon |
| `layer_dump.py` ◈ | **分层运行时解密样本的 dump 一条龙**（gdb 模板；c50c8812 同一模式手写 heredoc ×4 的沉淀）：`--break 0x加载器返回点 --dump VA:LEN:OUT`（可重复）→ 断点首次命中即 dump 全层并退出 + sha256/尺寸校验；`--pass-signals`（SIGILL/SIGSEGV/SIGBUS 穿透，自修改样本用；**SIGTRAP 禁止 pass**——gdb 断点/单步内部复用它，pass 即程序死，实测）、`--input` 喂 stdin、`--disasm`（objdump 线性反汇编按 VA 对齐成 OUT.dis，读时以地址为锚别信 CFG）、`--strings`。取层后要 xref/反编译走重载管线 `rpc_driver.py import-raw <原样本> OUT --base 0xVA [--entry 0x…]`（dump 按原 VA 导入为新程序，共享原样本 language）。exit 0 成功 / 2 用法 / 3 gdb、objdump 缺失 / 4 断点未命中零产出。stdlib only，不经 daemon |
| `noreturn_fix.py` ◈ | **铁律 10⑦ 的修复侧**（4307cc95：UD2 被误判 non-returning → 调用图截断 → 误判 flag 路径不可达丢 86 min；铁律只教「判定不可信」，本脚本补「怎么修」）：无参体检 = 列 NoReturn 函数 + 函数体内 UD2/INT3 流切断点（terminal 含 UD2/INT3 才可疑，exit/abort 合法 no-return 不用修）；`--fix <func>` 清 NoReturn 标志（调用者 CALL 之后代码恢复）；`--flow <addr>` 在 UD2/INT3 处补 fall-through override 到下一条（`--flow-clear` 撤销）；修后重反编译调用者验证，下游仍 undefined 用 rpc `disassemble --force` 补。经 exec-code 通道，exit 0 成功 / 1 用法 / 2 目标未找到 / 3 daemon 不可达 |

### 第 3 层：legacy（冻结备查，被 rpc 取代）

`scripts/` 下 25 个 PyGhidra 脚本 + `driver.py` + `analysis_config.py`：**冻结，仅备查**。`driver.py` 仍是两条后路——(a) daemon 整体挂掉时的直接执行通道（`driver.py export/exec/exec-w`，用 pyghidra-venv）；(b) 调试脚本行为差异时的对照组。不要在新工作流里再用它们；行为差异以 rpc 为准。

✎ 注意：legacy 时代"写操作必须 exec-w 才存盘"的纪律**已由 daemon 的自动存盘取代**——rpc 写命令每次写完即 `project.save()`，`stop` 时再全量保存。

### 执行模型（engine 内部，排障时读）
- daemon 进程 = rpc-venv 的 python + 进程内 JVM（pyghidra）；transport = 127.0.0.1 TCP + token（endpoint 文件在 `<ws>/rpc-localappdata/ghidra-rpc/`）
- session/registry 在 `<ws>/rpc-state/`（`GHIDRA_RPC_STATE_DIR`）；daemon 日志在 `<ws>/rpc-localappdata/ghidra-rpc/*.log`
- 所有 handler 由全局锁串行化——**并发客户端不会并行执行**，长命令会挡住其他命令
- daemon 崩溃后下一条命令自动按 session 重启（auto-restart）；`stop` 不干净时删 endpoint 文件再起
- **改了 `engine/` 下任何代码必须重启 daemon 才生效**（daemon 是长驻进程，启动时一次性加载 engine 代码；scripts/ 与文档改动不用）：`pkill -f 'ghidra_rpc[.]daemon'` 后下一条 rpc 命令自动拉起新 daemon。否则会出现"改了引擎、测了还是旧行为"的假缺陷——排障前先核对 daemon 启动时间晚于引擎改动时间
