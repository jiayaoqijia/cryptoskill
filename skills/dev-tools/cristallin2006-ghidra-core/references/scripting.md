> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# Ghidra 脚本编写（PyGhidra · Ghidra 12.x）

写自定义脚本放 `scripts/` 下即可被 driver.py 发现。**一次性逻辑优先用 `exec_code.py`**（预置 helper 的任意代码执行），只有可复用的能力才沉淀为独立脚本。

## 0. 运行时：PyGhidra（Python 3）

本 skill 已全部从 Jython 迁移到 PyGhidra（原因见 SKILL.md §0）。对脚本作者的影响：

| 方面 | Jython（旧） | PyGhidra（现在） |
|---|---|---|
| Python 版本 | 2.7 | 3.x（f-string、类型注解随便用） |
| Java 数组 | `from jarray import array` | `jpype.JArray(jpype.JByte)([...])` |
| `long("41",16)` | 可用 | 改 `int("41",16)` |
| Java String → Python | 需手动转 | 自动是真 `str`，`json.dumps` 直接吃 |
| `currentProgram`/`getScriptArgs()` | GhidraScript 全局 | 仍可用（`__missing__` 懒取 GhidraScript 属性），无需改 |
| 有符号 byte | `b & 0xff` 同 | `memory.setByte` 仍收**有符号** byte，`>127` 的 int 会 `OverflowError` |

Ghidra Java API 完全一致，下面所有模板照常适用。PyGhidra 启动层面的坑（`pyghidra.start()` 必须先于 `ghidra.*` import 等）由 driver.py 处理，脚本作者不用管。

## 0.5 exec_code.py：一次性逻辑的首选

```bash
# 写个 payload 文件（只需业务逻辑，helper 全预置好）
cat > /tmp/pay.py <<'EOF'
for f in list(fm.getFunctions(True))[:5]:
    print(f.getName(), f.getEntryPoint())
output_json({"status": "success", "count": fm.getFunctionCount()})
EOF
"$PY" "$SK/driver.py" exec <binary> exec_code.py "@/tmp/out.json" /tmp/pay.py
```

预置名字：`program`/`currentProgram`、`fm`、`listing`、`memory`、`toAddr`、`monitor`、`find_function(name_or_addr)`（三级查找）、`output_json(data)`。⚠ 无沙箱任意代码执行。

## 1. 标准骨架（独立脚本照抄）

```python
# @category DSH.Reverse
# @runtime PyGhidra
import json

def output_json(data, out_path=None):
    if out_path:
        f = open(out_path, 'w')                      # ensure_ascii → 纯 ASCII，无编码坑
        f.write(json.dumps(data))
        f.close()
        data = {"status": data.get("status", "success"), "out": out_path}
    print("===JSON_START===")
    print(json.dumps(data))
    print("===JSON_END===")

def run():
    program = currentProgram
    if program is None:
        output_json({"status": "error", "error": "No program loaded"})
        return
    args = getScriptArgs()
    out_path = None
    if args and args[0].startswith('@'):
        out_path = args[0][1:]
        args = args[1:]
    try:
        # ... 干活 ...
        output_json({"status": "success", ...}, out_path)
    except Exception as e:
        import traceback
        output_json({"status": "error", "error": str(e), "traceback": traceback.format_exc()})

run()
```

可用全局：`currentProgram` / `currentAddress` / `currentLocation` / `currentSelection` / `monitor` / `state`。

## 2. 函数三级查找（万能 helper）

```python
def find_function(program, name_or_addr):
    fm = program.getFunctionManager()
    if name_or_addr.startswith('0x'):
        addr = toAddr(name_or_addr)                  # GhidraScript 内置；None 需判空
        if addr:
            f = fm.getFunctionAt(addr) or fm.getFunctionContaining(addr)
            if f: return f
        return None
    for f in fm.getFunctions(True):                  # True = 地址正向
        if f.getName() == name_or_addr: return f
    low = name_or_addr.lower()
    for f in fm.getFunctions(True):
        if low in f.getName().lower(): return f
    return None
```

## 3. 反编译（DecompInterface 生命周期）

```python
from ghidra.app.decompiler import DecompInterface, DecompileOptions
from ghidra.util.task import ConsoleTaskMonitor

decomp = DecompInterface()
decomp.setOptions(DecompileOptions())
decomp.openProgram(program)
try:
    results = decomp.decompileFunction(func, 60, ConsoleTaskMonitor())   # 超时秒
    if results.decompileCompleted():
        c_code = results.getDecompiledFunction().getC()
    # 局部变量：results.getHighFunction().getLocalSymbolMap().getSymbols()
finally:
    decomp.dispose()                                 # 必须 dispose，否则句柄泄漏
```

## 4. 遍历惯用法

```python
fm = program.getFunctionManager()
for func in fm.getFunctions(True): ...               # 全函数
listing = program.getListing()
for data in listing.getDefinedData(True):            # 已定义数据
    if data.hasStringValue(): s = data.getValue()
for inst in listing.getInstructions(func.getBody(), True): ...   # 函数内指令
for blk in program.getMemory().getBlocks(): ...      # 内存块
```

## 5. Xref / 调用图

```python
for ref in getReferencesTo(addr): ...                # FlatProgramAPI 内置
    ref.getReferenceType().isCall() / .isJump() / .isData()
for ref in getReferencesFrom(addr): ...
# 函数级（比手工遍历 ref 高效）：
callers = func.getCallingFunctions(monitor)
callees = func.getCalledFunctions(monitor)
# 基本块 CFG：
from ghidra.program.model.block import BasicBlockModel
model = BasicBlockModel(program)
blocks = model.getCodeBlocksContaining(func.getBody(), monitor)
```

## 6. 写操作 = 事务（铁律）

```python
tid = program.startTransaction("Rename func")
success = False
try:
    func.setName("check_flag", ghidra.program.model.symbol.SourceType.USER_DEFINED)
    success = True
finally:
    program.endTransaction(tid, success)
```

- headless 保存机制（PyGhidra 流程）：写操作脚本用 `driver.py exec-w` 运行，driver 在脚本结束后显式 `program.save()`；`exec` 不会落盘。`-readOnly` 旧语义仅存在于 `.java` 脚本走的 analyzeHeadless 分支。
- 注释：`from ghidra.program.model.listing import CommentType` → `codeUnit.setComment(CommentType.PLATE, text)`（12.x 枚举；旧的 `CodeUnit.PLATE_COMMENT` int 常量仍可用但已 deprecated，新代码别用）。
- 改签名：`FunctionSignatureParser(dtm, None).parse(func.getSignature(), sig_str)` + `ApplyFunctionSignatureCmd(entry, new_sig, SourceType.USER_DEFINED).applyTo(program)`。

## 7. Java 互操作坑（PyGhidra / JPype）

- `memory.getByte(addr)` 返回**有符号** Java byte → 必须 `b & 0xff`；`setByte` 同理收有符号值（`>127` 的 Python int 会 `OverflowError`）。
- Java byte 数组：`jpype.JArray(jpype.JByte)([b if b < 128 else b - 256 for b in bs])`（Jython 的 `from jarray import array` 在 PyGhidra 下不存在）。
- Python 3 随便用 f-string；`long()` 不存在，用 `int()`。
- 手工拼多字节值时注意端序：`sum((b & 0xff) << (8*i) for i,b in enumerate(raw))` 是**小端**假设；大端目标要反转（`program.getLanguage().isBigEndian()`）。

## 8. 实用模板

### 批量找含特征指令的函数（如 CPUID 反虚拟机）

```python
for func in fm.getFunctions(True):
    if not func.getName().startswith('FUN_'): continue
    for inst in listing.getInstructions(func.getBody(), True):
        if inst.getMnemonicString() == 'CPUID':
            func.setName('anti_vm_check_' + func.getEntryPoint().toString(),
                         SourceType.USER_DEFINED)    # 记得包事务
            break
```

### 提取函数内所有 XOR 立即数（找解密 key）

```python
for inst in listing.getInstructions(func.getBody(), True):
    if inst.getMnemonicString() == 'XOR':
        for i in range(inst.getNumOperands()):
            for obj in inst.getOpObjects(i):
                if hasattr(obj, 'getValue'):
                    print("0x%x" % obj.getValue())
```

### 决策树批量提取（f1..fN 调度器 + CMP 常量）

```python
import re
for func in fm.getFunctions(True):
    if not re.match(r'f\d+$', func.getName()): continue
    for inst in listing.getInstructions(func.getBody(), True):
        if inst.getMnemonicString() == 'CMP':
            ops = inst.getOpObjects(1)
            if ops and hasattr(ops[0], 'getValue'):
                print(func.getName(), "0x%x" % ops[0].getValue())
```

### EmulatorHelper 仿真（不脱壳解密 stub / 跑单个函数）

```python
from ghidra.app.emulator import EmulatorHelper
emu = EmulatorHelper(program)
emu.writeRegister("RSP", 0x2fff0000)
emu.writeMemoryValue(data_addr, len(encrypted), encrypted_val)   # 或逐字节 writeMemory
emu.writeRegister("RDI", arg1)
emu.setBreakpoint(return_addr)
emu.writeRegister(emu.getPCRegister(), func.getEntryPoint().getOffset())
emu.run(monitor)                    # 或循环 emu.step(monitor) 观察
result = emu.readMemory(out_addr, out_len)   # 读出解密结果
emu.dispose()
```

用途：自定义壳的解密函数、密钥派生、单函数行为验证。边界：`func.getBody().contains(pc)` 判断返回；call 出外部函数会失控，必要时给外部 call 设断点跳过。

## 9. Best Practices 五条（来自 ai-ghidra-tools，实测有效）

1. **Check for null**：`currentProgram`、`toAddr()`、`find_function` 返回值全部判空
2. **Use monitors**：长操作传 `monitor` 支持取消
3. **Handle errors**：try/except 包住，错误进 JSON 的 `traceback` 字段
4. **Clean up resources**：decompiler `dispose()`，文件 `close()`
5. **Use transactions**：一切修改包 `startTransaction/endTransaction`
