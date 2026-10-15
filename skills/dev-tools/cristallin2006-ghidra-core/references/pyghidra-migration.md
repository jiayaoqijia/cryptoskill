# PyGhidra 移植须知（踩过的坑，2026-09 实测）

> 从 ghidra-core/SKILL.md §7 抽取。适用场景：写新 Ghidra 脚本、移植旧 Jython 脚本、排障启动/API 形状问题。

移植把 21 个脚本从 `@runtime Jython` 改成 `@runtime PyGhidra`。语法层面几乎零成本（实测无 `xrange`/`iteritems`/`has_key`/`except X, e`，仅 `search_bytes.py` 用了 Jython 独有模块）。真正的坑都在**启动方式**和**API 形状**上：

1. **`.py` 不能交给 `analyzeHeadless`**（在 PyGhidra 流程下）：那会起普通 JVM，报 Jython 缺失。注意这条与 SKILL.md §0 的 APPDATA 重定向是**两个独立原因**——即使装上 Jython 扩展，PyGhidra 启动器也不认 `analyzeHeadless`。
2. **`pyghidra.start()` 必须在任何 `ghidra.*` import 之前**：否则 `ModuleNotFoundError: No module named 'ghidra'`。`driver.py` 的 `main()` 里处理。
3. **（旧版认知，已过期）`pyghidra` CLI 参数透传**：早期记录称 CLI 只接受一个脚本位置参数；实测 pyghidra 3.1.0 已把脚本后的参数全部传入 `script_args`，裸 CLI 可用。driver.py 仍走 `pyghidra.ghidra_script(..., script_args=[...])` 这个稳定 API，多一层脚本名解析和 exec-w 存盘。
4. **`program_loader().load()` 返回的是 `LoadResults` 而不是 `Program`**：要 `results.getPrimaryDomainObject()`，并且 `LoadResults` 是 `AutoCloseable`，用 `close()` 释放。
5. **`walk_programs(project, callback, ...)` 是回调式**，不是可迭代对象。它会在**自己的 program 上下文里**打开每个程序，所以不要在回调里长期持有 `program`。
6. **`open_project(path, name, create)`**：path 是**父目录**，不是 `.gpr` 文件；`ProjectLocator` 拒绝含 `.` 的路径元素（所以走 junction）。
7. **`currentProgram` / `getScriptArgs()` 仍然可用**：PyGhidra 的脚本 globals 用 `__missing__` 从 `GhidraScript` 实例懒取属性，所以老脚本不用改成显式 `getCurrentProgram()`。
8. **字符串类型更友好**：Java String 到 Python 是真正的 `str`（实测 `type(...).__name__ == 'str'`），`json.dumps` 不需要手动转换。构 Java `byte[]` 用 `jpype.JArray(jpype.JByte)`（Jython 的 `from jarray import array` 不存在）。
9. **Jython 的 `-preScript` 没有对应物**，但功效可以等价实现：分析选项必须在程序**已加载、`analyze()` 尚未运行**之间设置。这是 `analysis_config.py` 的职责，`driver.py import` 已内置；旧的 `set_analysis_options.py` 因此降级为参考实现（它作为独立脚本在 PyGhidra 流程里没有钩子可挂）。

### 三个「遗留问题」已修复（2026-09 实测）

都是**脚本自身的 bug**，不是 Ghidra/PyGhidra 的限制：

- **`patch_bytes.py` 现在能打补丁**。原来的 `if not block.isWrite(): return` 拒绝一切代码段写入——但那个 flag 是**权限位不是保护**（`.text` 的字节本来就是可写的）。现在流程是：`block.setWrite(True)` → `clearCodeUnits()` 清掉与补丁区重叠的反汇编 → `setByte()`（**必须传有符号 byte**，`>127` 的 Python int 会 `OverflowError`）→ `finally` 里恢复 `setWrite(False)`。实测把 `.init` 的 `74 02`(JZ) 改成 `75 02`(JNZ)，**新进程读回仍是 `75 02`**，且 `write:false` 已复位。
  ⚠️ 代价：被覆盖的指令会变成 `undefined`，**需要重新分析**才恢复反汇编视图（脚本结果里用 `instructions_cleared` 报告）。
- **`rename_symbol.py` 现在接受裸地址**。原来只认 `0x` 前缀，传 Ghidra 自己打印的 `00102ae0` 会掉进「按符号名查找」分支必然失败。现在裸十六进制也走地址路径，并且地址落在函数体内时会取**包含它的函数**。实测 `00102ae0` 与 `0x1029f0` 都成功，名字在**新进程里仍然存在**。
- **分析配置可用**：`driver.py import --analysis minimal|default`。`minimal` 关闭重型分析器（实测关掉 Decompiler Switch Analysis / DWARF / Demangler GNU / Function ID / Stack / Create Address Tables），`default` 重新打开（实测打开 Aggressive Instruction Finder / Decompiler Parameter ID）。
  注：`setBoolean` 必须在事务内调用，否则 `db.NoTransactionException`。

### 实测覆盖（对某 CTF stripped ELF，96 函数）

**上游 21 个脚本 + `analysis_config` 均可用**：`triage_scan` `analyze_binary` `get_memory_map` `get_symbols` `list_functions` `decompile_function` `decompile_all` `get_disassembly` `get_xrefs` `get_call_graph` `get_basic_blocks` `search_strings` `search_bytes` `get_data_at_address` `list_classes` `emulate_function` `add_comment` `set_function_signature` `rename_symbol`（地址或名字）`patch_bytes`（含写权限授予）`set_analysis_options`（已被 `analysis_config.py` 取代，保留仅作参考）

**本 skill 新增 4 个，同样实测通过**（同一 stripped ELF）：`exec_code` `export_binary` `apply_c_types` `apply_data_type`
- `exec_code.py` —— 文档承诺的名字空间逐个验证存在：`program`/`listing`/`memory`/`fm`/`toAddr`/`find_function`/`output_json` 全部可用（`fm.getFunctionCount() == 96`）
- `export_binary.py` —— 导出 18576 字节，与原文件 **SHA256 完全一致**；同时返回 `md5`/`original_md5` 便于确认补丁是否生效
- `apply_c_types.py` —— 解析出 14 个类型（`/svc_hdr`、`/svc_op` + 12 个 stdint typedef）
- `apply_data_type.py` —— 需前一步**已落盘**，见 SKILL.md §5 类型库两步走

**脚本目录（迁移当时的构成）= 25 个任务 `.py` + `driver.py` + `analysis_config.py`（共 27 个），无 shell 脚本**——此后目录持续增长（现行 47 个 `.py`，三层结构见 SKILL.md §5）；`run-headless.sh` 曾在目录里，现已删除；`analyzeHeadless` 只由 `driver.py` 的 `.java` 分支调用，不要直接用它跑 `.py`。`__pycache__` 不必提交。

### PyGhidra 持久化限制：存不下自己加载的程序（已用 `export` 绕过）

`driver.py import` **不能把项目落盘**：`program_loader().load()` 返回的程序在一个报告只读的 `DomainFileProxy` 后面，而
`DomainFile.setReadOnly()` 在 proxy 上抛 `UnsupportedOperationException`、`ProgramDB` 又没有 `setChanged`，
所以 `program.save()` 必然 `ghidra.util.ReadOnlyException`。该进程结束后项目里就没有程序了。

**绕法（已实测）**：需要可复用项目时先跑一次 `driver.py export`，它把导入交给 Ghidra 自带的
`analyzeHeadless -import`（参数表里没有脚本，因此不触发 Jython/PyGhidra 的任何 provider 问题），
产出的扁平项目结构正是 `exec`/`exec-w` 能打开的。

```bash
driver.py export ./svc               # 建项目（一次性）
driver.py list   ./svc               # -> /svc (x86:LE:64:default)
driver.py exec   ./svc get_xrefs.py "@out/xrefs.json" 0x102ae0 both
```

实测三段全通，`get_xrefs` 返回 3 条。分工是：**export 负责持久化，import 负责一次性的进程内分析+分诊**。
