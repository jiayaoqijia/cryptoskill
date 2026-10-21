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
完整命令与参数以当前发现的 `rpc_driver.py --help` 或 `engine/ghidra-rpc/` 文档为准；不要求存在原机器的 Desktop/venv 目录。

### 第 2 层：宿主工具脚本（◈ 直接 python 运行，不经 daemon/driver）

| 脚本 | 用途 |
|---|---|
| `rpc_driver.py` | 统一入口：项目映射/key 替换/@out/环境自给 |
| `ledger.py` ◈ | 旧二进制台账兼容入口；实现已移至 runtime/analysis-v1，格式与新字段见 analysis-session 的 legacy-ledger.md |
| `read_views.py` | 三视图读字节（hexdump/hex/cstr）及显式 --expect-len/--expect-hex 对照，失败 exit 2；按具体读数疑点选用。 |
| `crypto_sanity.py` | 局部格式/输入契约诊断：Base64 字母表与 padding 可显式指定；check-result 仅检查已声明格式，不证明目标接受。0 检查通过 / 1 输入用法错误 / 2 不满足已检查条件 / 3 契约未确定。 |
| `launch_gui.py` | detached 拉起 Ghidra GUI，可直接打开项目 |
| `doctor.py` | 环境自检（8 项：安装/JDK/双 venv/工作区/项目/rpc 包/daemon 起停），全绿 exit 0 |
| `venv_health.py` | 在对应解释器真实 import，并提供依赖诊断。需要相关后端且可用性未知时按需探测；某个 venv 未命中不证明系统不存在等价能力，不自动安装或升级。 |
| `guarded_run.py` | 可选的长计算保护器：输出落盘、心跳和受管理的结束；--timeout N --log F -- cmd，超时退出码 124。适用于需要此机制的本地计算，不因超过固定秒数强制使用，也不改变 Solver 默认无时限。 |
| `pe_info.py` ◈ | PE 分诊：头/节表/熵/导入表/资源；PE32 与 PE32+ 双路径（ImageBase 与导入 thunk 宽度都按位数分派）。`python pe_info.py <exe>` |
| `decomp_lint.py` | 已有伪码的告警与渲染疑点清单，有 fatal 标签时 exit 2；--binary 可提供尾调用模式线索。标签不禁止导航，不证明目标有错；按相关结论核对原始字节、指令或行为。 |
| `call_histogram.py` | CALL/JMP 目标分布，用于定位重复调用/分发模式；次数阈值是线索，不要求所有 Rust/内联 main 先运行。 |
| `emulate_blob.py` | 裸 blob Unicorn 仿真骨架：`--base/--entry/--rsp/--max-insns/--reg/--map-file/--dump-dir`（`--entry` 是相对 `--base` 的偏移），停止原因分类 + dirty 页 dump；exit 0 跑完 / 2 用法错 / 3 unicorn 缺失（提示进 re-tools-venv）/ **4 harness 配置错**（blob 不可读或为空、未知 `--reg`、映射失败、**入口未映射**——不误报 RET 飞出）（多层载荷题用，ctf-patterns §10） |
| `const_scan.py` | Cython/C 常量重建：扫反编译 C（或 decompile-all @out JSON）的 `PyList_New(n)`/`PyTuple_New(n)` + 随后常量写入，重建 Python 字面量；小整数聚集自动告警"疑似字节级常量表"；`--binary <样本>`（须先 ensure）把 `<DAT_…>` 缓存 PyLong 引用还原成 Python 值，CPython 布局自动投票（`--py 311/312` 强制）（chal 复盘 T3：L 表 48 项实测定位+还原） |
| `xor_scan.py` | blob 变换搜索：单字节 XOR 全扫 + 可选滚动密钥/ADD/SUB，按可打印率+magic（MZ/ELF/PK/UPX!）+flag 正则综合评分排 Top N；`--dump <key>` 落地解密产物（判例F·缺口4，不要再现场手写第 5 版） |
| `emulate_program.py` | **整程序仿真**（emulate_blob 的上层）：PE 装载 + IAT 桩（88 个内建 Win32 stub，ABI 陷阱已正确实现）+ 喂 stdin + 成功/失败断点；`--trace-api` 排障、`--dump-state` 取状态。console 型校验程序专用（边界见 docstring）；判例H 实测 0.047s 跑到成功分支（unicorn-harness.md 的可执行形态） |
| `jt_resolve.py` | 跳转表一键解析：LEA+JMP 线索 ∪ decompile 警告 ∪ 伪码残留三路并集找**所有**表基址，rel32/abs32 双模式解 target，basic-blocks CFG 交叉验证；只解一张 = 解错一半（判例H 实测双表全解） |
| `frame_map.py` | 栈帧槽位归属表：`SUB RSP` 定帧 → 扫 `[RSP+off]` 首写/宽度/读写次数；同槽多宽度标可疑（伪码 `local_XXXX` 重叠命名的真身） |
| `const_audit.py` | 伪码常量对照审计：`&DAT_0000xxxx` 小整数嫌疑（判例H 实测抓到 `&DAT_00000007` = 长度 7）、`DAT_` 引用实际字节对照、指针化字面值漂移判定（注意：指向字符串中部的真实 `LEA` 立即数**不是**漂移，工具已加反汇编引用抑制） |
| `model_diff.py` | 模型实现与本地 oracle 的输入分布对拍：--input-gen、--seed、首个分歧与指纹统计。指纹帮助选核查方向，接口/位宽与算法错误均保留可能；0 一致 / 2 有分歧 / 3 命令错误。 |
| `oracle_family.py` ◈ | **打桩 oracle 家族（单因子隔离）**：binary + `--stub 0xaddr=0xval`（可重复）批量产 patched 副本（x86-64 函数头写 `mov eax,imm32;ret`，`--rax` 用 imm64 形式）逐个运行出差分表：输出变 ⇒ 该因子参与计算；已测常量/输入/路径下不变 ⇒ 未观察到影响，不能证明全局无关。`--addr-is va`（默认，ELF 按 program header、PE 按节表+ImageBase 换算，可用 `--dry-run` 只验换算不 patch）/offset；非 x86-64 exit 3；exit 0 全部跑完 / 2 有副本运行失败 / 3 用法/架构错误 |
| `ssa_trace.py` ◈ | **Cython/CPython 扩展 SSA 数据流追踪器**（ctf-patterns §12.2 工具形态）：int 子类包裹（`+ - * ^ & | << >> % //` 自动落账成事件流）+ import 前 builtins 记录包装（`--observe-builtins`）+ `random.*`/`os.urandom` 钩子（`--pin-urandom`/`--seed` 做 §9 角色判别）；`--class CLS --ctor-input 'A*48' --wrap m1,m2 --out trace.json`。exit 0 正常 / 2 用法错 / 3 加载失败。stdlib only，不经 daemon（Reverse-chal 复盘分水岭：8 min 拿 ARX 递推结构，替代手读生成 C） |
| `ssa_reconstruct.py` ◈ | **SSA 事件流→直线程序重建 + 裸字面量解析**（§12.2 后半链，吃 ssa_trace 的 trace.json）：产出可读直线程序（行格式与 peel_inverse 输入约定一致），高频裸字面量用 identity/sw/sw<<16/位移/*16 + `sw(a)<<16|sw(b)` 打包四式逐一试解，解不出标 ?? 交人工不猜——Cython 值 C 化断链处"神奇常数"的归位器。exit 0 正常 / 2 输入错。stdlib only，不经 daemon |
| `peel_inverse.py` | 识别所支持直线程序的递推依赖并可 --emit-solver 生成剥离骨架；填写已知值、查表实现与种子后独立验证。是否适合剥离、局部反推或 SMT 由问题结构决定，不存在运行骨架才能放行其他方法的门。0 判定完成 / 2 输入或材料不足。 |
| `cone_invert.py` | 对支持的直线程序从 --known 锚点反推；有损操作与缺失 CALL_TABLES/枚举域会形成缺口。矛盾可来自方程、常量、符号化或路径条件，诊断不是唯一根因。--diff-symbolize 可比较两份输入相关重建结果；0 收敛 / 1 矛盾 / 2 输入错误。 |
| `layer_dump.py` ◈ | **分层运行时解密样本的 dump 一条龙**（gdb 模板；c50c8812 同一模式手写 heredoc ×4 的沉淀）：`--break 0x加载器返回点 --dump VA:LEN:OUT`（可重复）→ 断点首次命中即 dump 全层并退出 + sha256/尺寸校验；`--pass-signals`（SIGILL/SIGSEGV/SIGBUS 穿透，自修改样本用；**SIGTRAP 禁止 pass**——gdb 断点/单步内部复用它，pass 即程序死，实测）、`--input` 喂 stdin、`--disasm`（objdump 线性反汇编按 VA 对齐成 OUT.dis，读时以地址为锚别信 CFG）、`--strings`。取层后要 xref/反编译走重载管线 `rpc_driver.py import-raw <原样本> OUT --base 0xVA [--entry 0x…]`（dump 按原 VA 导入为新程序，共享原样本 language）。exit 0 成功 / 2 用法 / 3 gdb、objdump 缺失 / 4 断点未命中零产出。stdlib only，不经 daemon |
| `noreturn_fix.py` | NoReturn 与 UD2/INT3 路径疑点诊断；--fix 清标志，--flow/--flow-clear 管理分析覆盖。仅在有依据且获准的所属项目中修改，随后核对调用方；真实 exit/abort 可能正确终止。0 成功 / 1 用法 / 2 目标未找到 / 3 daemon 不可达。 |

### 第 3 层：legacy（冻结备查，被 rpc 取代）

`scripts/` 下 25 个 PyGhidra 脚本 + `driver.py` + `analysis_config.py`：**冻结，仅备查**。`driver.py` 仍是两条后路——(a) daemon 整体挂掉时的直接执行通道（`driver.py export/exec/exec-w`，用 pyghidra-venv）；(b) 调试脚本行为差异时的对照组。不要在新工作流里再用它们；行为差异以 rpc 为准。

✎ 注意：legacy 时代"写操作必须 exec-w 才存盘"的纪律**已由 daemon 的自动存盘取代**——rpc 写命令每次写完即 `project.save()`，`stop` 时再全量保存。

### 执行模型（engine 内部，排障时读）
- daemon 进程 = rpc-venv 的 python + 进程内 JVM（pyghidra）；transport = 127.0.0.1 TCP + token（endpoint 文件在 `<ws>/rpc-localappdata/ghidra-rpc/`）
- session/registry 在 `<ws>/rpc-state/`（`GHIDRA_RPC_STATE_DIR`）；daemon 日志在 `<ws>/rpc-localappdata/ghidra-rpc/*.log`
- 所有 handler 由全局锁串行化——**并发客户端不会并行执行**，长命令会挡住其他命令
- daemon 崩溃后下一条命令自动按 session 重启（auto-restart）；`stop` 不干净时删 endpoint 文件再起
- 修改长驻 engine 后，需要让对应实例重新加载代码。先核对样本/项目归属、PID/启动身份、共享使用和保存状态，再通过所属 daemon 的 stop/管理接口停止并确认收尾；不要宽范围 pkill。文档/宿主脚本更新通常无需重启 daemon。
