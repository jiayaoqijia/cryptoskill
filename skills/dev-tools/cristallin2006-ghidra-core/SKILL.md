---
name: ghidra-core
description: 运行 Ghidra RPC、导入与项目管理、事务、标注、导出、daemon 起停与执行排障时使用。分析方法见 ghidra-static/re-dynamic；通用任务状态见 analysis-session。
---

# ghidra-core

## 输入与输出

输入是样本路径、项目、函数/地址及操作；输出为 RPC JSON、导出文件与执行诊断。结果含地址时记录 image base、处理器和分析配置。脚本入口保留兼容路径。

## 最短可用流程

```bash
SK="${DSH_HOME:-$HOME/.dsh}/skills/ghidra-core/scripts"
python3 "$SK/rpc_driver.py" ensure /path/to/sample
python3 "$SK/rpc_driver.py" decompile /path/to/sample main
python3 "$SK/rpc_driver.py" "@/path/to/out.json" triage /path/to/sample
```

`ensure` 可启动对应 daemon、导入样本并分析。`@out` 为首参数。批量查询可选 decompile-all/search-decompiled，写操作使用 Ghidra 事务并自动存盘。项目写锁与 daemon 内 handler 串行锁都需尊重；同一 daemon 多代理排队不会自然提速。共享变更由 analysis-session 的 lease/guard 协调，锁只覆盖经该入口发起的操作。

## 执行与故障

按需用 `doctor.py --quick` 查 Ghidra 核心；跨工具环境用 analysis-session 的 discover，使用前只测当前需要的工具。路径/版本由探针获得，本机候选放在 runtime/environment.json。Ghidra 工作区路径仍遵守实际引擎的路径限制；勿改变在用项目的属主或目录。导入复用需同时核对样本哈希、处理器和分析配置。

daemon 故障先查对应实例与日志，必要时停止并重启该实例；不宽泛 pkill。命令用法 `rpc_driver.py --help` 或 [rpc-commands.md](references/rpc-commands.md)，GUI/legacy/移植问题按下面索引读取。非 Ghidra 方法与运行能力已有独立入口，旧 scripts 路径为兼容包装。

## 会话与交接

按当前问题选方法，可静态先行、动态先行或直接建模。连续实验没有新增证据时盘点前提和可区分解释的实验；时间盒用于复查，可说明价值后继续原路线。

简单单点查询记录最小证据即可；多阶段、恢复或协作任务按需使用 analysis-session，记录关键结论、目标代次、实验干预和未决问题。普通工具事件由运行层记录。候选与外部接受分别说明，可交付限定范围的未完成报告。共享项目写操作协调所有权；未获变更权时先只读。

## 补充专题入口

- [crypto-ident](references/crypto-ident.md)：当前问题涉及文件名对应专题时按需读取。
- [evidence-ledger](references/evidence-ledger.md)：当前问题涉及文件名对应专题时按需读取。
- [headless](references/headless.md)：当前问题涉及文件名对应专题时按需读取。
- [pyghidra-migration](references/pyghidra-migration.md)：当前问题涉及文件名对应专题时按需读取。
- [scripting](references/scripting.md)：当前问题涉及文件名对应专题时按需读取。
- [unicorn-harness](references/unicorn-harness.md)：当前问题涉及文件名对应专题时按需读取。
- [windows-powershell](references/windows-powershell.md)：当前问题涉及文件名对应专题时按需读取。
