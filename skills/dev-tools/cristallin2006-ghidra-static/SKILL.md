---
name: ghidra-static
description: 恢复二进制函数语义、控制流/数据流、常量与算法，解释反编译结果的局限。用于函数分析、静态建模与语义标注；Ghidra 命令由 ghidra-core 提供。
---

# ghidra-static

## 输入与输出

输入为样本、已知类型/处理器、当前函数或问题；输出为带地址与来源的语义模型、常量、路径条件、未决假设及适用范围。

## 最短可用流程

本技能的输入、分析状态与验证约定见 [核心证据卡](references/core-evidence.md)。编排 Solver 由宿主完整交付此卡；普通模式从该入口读取。下列专题按当前问题选择，不递归加载全部参考资料。

从字符串/API/比较点或已知函数定位相关代码，追输入到判定点的数据流。按问题选择 decompile、disassemble、xref、CFG 或 P-code；批量检索可用 search-decompiled。类型、字段序、栈槽归属与反编译渲染有疑点时对照原始字节和指令，不把局部视图当唯一真相。

注释/重命名记录依据；修改字节与分析原始行为分开，导出记录原文件与产物哈希。疑似死代码先查反编译器截断、异常/信号边和间接跳转。PE SEH/VEH 仅在有线索时读对应配方。

## 建模与验证选择

先明确输入长度、编码、padding、字节序、位宽和溢出语义。SSA/常量/依赖图可辅助判断：可剥离递推用 scripts/peel_inverse.py；局部单未知量反推用 scripts/cone_invert.py；结构适合约束求解时可直接用 SMT。不存在跨问题的固定优先级。Ghidra API 依赖的 ssa_reconstruct.py、read_views.py、frame_map.py 等留在 core。

独立前向实现验证候选有价值；同源实现一致只证明局部自洽。已知输入往返测试不等于完整模型闭合，还要按需要与实际目标行为对照。不可打印候选结合输入契约判断。动态实验用于区分假设，数学结构明确后可交给 ctf-crypto；看到 XOR/AES/Z3 不自动转交。

交付包含模型范围、地址/字节与复现证据、候选的验证层次、产物和未决问题。缺少运行后端时可以交付限定的静态结论。

关联动态地址时先区分原始 ELF VA、Ghidra rebase 和运行时 load bias；段起点不等于任意函数地址。离线坐标核对见 `re-dynamic/references/re-workbench.md`，其结果为声明条件下的算术关联，不自动授权改名、改类型或回写项目。

需要导出当前程序的只读文件映射和查询字节时，使用 `scripts/ReEvidenceSnapshot.java`；操作与证据边界见 `re-dynamic/references/static-correlation.md`。该导出不修改程序，也不替代原始指令核对。

## 会话与交接

按当前问题选方法，可静态先行、动态先行或直接建模。连续实验没有新增证据时盘点前提和可区分解释的实验；时间盒用于复查，可说明价值后继续原路线。

简单单点查询记录最小证据即可；多阶段、恢复或协作任务按需使用 analysis-session，记录关键结论、目标代次、实验干预和未决问题。普通工具事件由运行层记录。候选与外部接受分别说明，可交付限定范围的未完成报告。共享项目写操作协调所有权；未获变更权时先只读。


## 按需资料

| 文件 | 何时读 |
|---|---|
| [nginx 模块分析](references/nginx-module-analysis.md) | 模块/配置回调、真实请求 handler 或 master/worker/request 对象关联不清 |
| [VM 状态与求逆](references/vm-state-inversion.md) | 指令位宽、副作用、就地读写版本、容器选择或可逆条件影响当前结论 |
| [数据驱动恢复](references/data-driven-recovery.md) | 固定输出、未知数据表或代码/数据关系不清；需要区分布局、恢复假设和验证 |
| [复合变换与搜索](references/transform-pipelines.md) | 数据布局已明确且有有限变换假设；需要求逆、约束搜索、等价去重或解释无命中 |
| [P-code 位宽语义](references/pcode-width-contracts.md) | 伪码出现截断/溢出/符号扩展等疑点时核对 P-code 语义 |
| `references/ctf-patterns.md` | CTF 模式库与 flag 狩猎启发式（XOR/期望值/oracle/自定义 VM/魔数/S-box 指纹/随机源分类/侧信道/动态工具选型/Cython 扩展元数据） |
| `references/go-binary.md` | triage 报 `lang_hints.go=true` 或发现 Go 指纹（pclntab/buildinfo/garble）时 |
| `references/rust-binary.md` | triage 报 `lang_hints.rust=true` 或发现 Rust 特征串时 |
| `references/cpp-binary.md` | C++ 样本：vtable/RTTI 恢复、this 指针类型化、STL 噪声过滤、MFC 消息映射 |
| `references/classic-crypto.md` | 认出算法后的求逆执行：换表 base64/RC4/TEA 手撕、流水线求逆纪律（识别归 ghidra-core crypto-ident.md） |
| `references/decompiler-pitfalls.md` | 结论依赖有疑点的伪码时，对照常量、类型、向量初始化、调用参数及控制流；按问题选视图，不固定全量体检 |
| （已迁移） | 漏洞定位完成、要写 exp 时 → 转 **`pwn-exploit`** 场景 skill（`pwn-exploit/references/basic-chain.md`：checksec 打法树/ROP/libc 泄露/pwntools 骨架，WSL 工具链） |

## 补充专题入口

- [crypto-ident](references/crypto-ident.md)：当前问题涉及文件名对应专题时按需读取。
- [ctf2-failure-routing](references/ctf2-failure-routing.md)：当前问题涉及文件名对应专题时按需读取。
- [exception-control-flow](references/exception-control-flow.md)：当前问题涉及文件名对应专题时按需读取。
- [runtime-dependent-verifier](references/runtime-dependent-verifier.md)：当前问题涉及文件名对应专题时按需读取。
- [tools](references/tools.md)：当前问题涉及文件名对应专题时按需读取。
- [windows-exception-flow](references/windows-exception-flow.md)：当前问题涉及文件名对应专题时按需读取。
- [x86-edge-semantics](references/x86-edge-semantics.md)：当前问题涉及文件名对应专题时按需读取。
