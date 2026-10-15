> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# Python 字节码 / pyc 逆向（magic 判版本 / 反编译器选调 / PyInstaller 链路 / dis 兜底 / PyArmor 识别）

> 本篇管：pyc 字节码版本判定、反编译器选择、PyInstaller 样本 exe→.py 完整链路、dis/marshal 手工直读兜底、PyArmor 初步识别。
> 不管：PyInstaller 解包自动化的实现细节（看 `re-unpack/scripts/pyinstaller_extract.py` 头部注释）；动态调试与运行时 dump（re-dynamic）；.NET IL（`references/dotnet-il.md`）。判型与路线决策见 `references/triage.md` §3。
> 工具可用性以 `python "$SK/doctor.py"` 为准（uncompyle6/decompyle3/pyinstxtractor 为 Tier A，pycdc 为 Tier B）。

## 1. magic number → Python 版本判定

pyc 前 4 字节 = 2 字节小端 magic + 恒定的 `0d 0a`；magic 不在表里按"就近归入同一大版本"处理（小版本会递增 magic）。

| 前 4 字节（hex） | magic 值 | Python |
|---|---|---|
| `03 f3 0d 0a` | 62211 | 2.7 |
| `42 0d 0d 0a` | 3394 | 3.7 |
| `55 0d 0d 0a` | 3413 | 3.8 |
| `61 0d 0d 0a` | 3425 | 3.9 |
| `6f 0d 0d 0a` | 3439 | 3.10 |
| `a7 0d 0d 0a` | 3495 | 3.11 |
| `cb 0d 0d 0a` | 3531 | 3.12 |

```bash
xxd -l 16 entry.pyc        # 看头；第 3-4 字节必须是 0d 0a，否则头被剥/已损坏
```

头总长：2.7 = 8 字节；3.3–3.6 = 12 字节；**3.7+ = 16 字节**（magic 4 + bit field 4 + mtime 4 + size 4）。补头时按版本给足长度。

## 2. 反编译器选择矩阵

```bash
VENVS="$HOME/Desktop/src/re-tools-venv/Scripts"          # WSL: ~/re-tools-venv/bin
"$VENVS/uncompyle6.exe" -o out_dir entry.pyc             # ≤3.6 / 2.x
"$VENVS/decompyle3.exe"  -o out_dir entry.pyc            # 3.7 / 3.8（语法还原更准）
wsl -d Ubuntu -u root -- pycdc /mnt/c/Users/Lenovo/work/entry.pyc   # ≥3.9 唯一选项
```

| bytecode 版本 | 选 | 用错工具的典型失败形态 |
|---|---|---|
| 2.x – 3.6 | uncompyle6 | decompyle3 不覆盖 3.7 以下 |
| 3.7 – 3.8 | decompyle3 | uncompyle6 对 3.7/3.8 控制流易报错 |
| ≥ 3.9 | pycdc | uncompyle6/decompyle3 报 `Unknown opcode ...` 或 unsupported version —— **这是版本不匹配，不是样本坏了**，别再修文件 |

- 这两个包没有 `__main__`，**不能 `python -m`**，必须走 venv 的 console script（上表路径）。
- `-o` 语义坑：decompyle3 要求 `-o` 目标目录**已存在**，先 `mkdir -p out_dir`。
- pycdc 输出到 stdout，自行重定向存盘；未装时在线 https://pylingual.io 可临时兜底（注意样本敏感性，涉毒不上传）。
- pycdc 对 3.11/3.12 新语法可能**静默丢语句**（控制流缺一块而无报错）——拿到结果先扫是否逻辑完整，残缺即按铁律 11 用 dis 直读对照（§4）。

## 3. PyInstaller 样本完整链路

一条龙（推荐，自动分诊→解包→按版本选调）：

```bash
python "C:/Users/Lenovo/.dsh/skills/re-unpack/scripts/pyinstaller_extract.py" sample.exe --check   # 只分诊
python "C:/Users/Lenovo/.dsh/skills/re-unpack/scripts/pyinstaller_extract.py" sample.exe           # 解包+反编译入口
python "C:/Users/Lenovo/.dsh/skills/re-unpack/scripts/pyinstaller_extract.py" sample.exe --all     # 反编译全部 pyc
```

- 闸门：无 `MEI\x0c\x0b\x0a\x0b\x0e` cookie 的非 PyInstaller 样本 exit 2 拒绝跑——先确认是不是 upx/nuitka（`references/triage.md` §3、§6）。
- 默认输出 `<binary名>_pyinst/<binary名>_extracted/`，反编译产物在 `decompiled/`。

手工链路（自动化失败时分步排查）：

```bash
mkdir work && cd work
python "$HOME/Desktop/src/tools/pyinstxtractor/pyinstxtractor.py" ../sample.exe   # 产物建在当前 cwd，必须先 cd
```

1. 入口 pyc 在 `<name>_extracted/` 根目录；pyinstxtractor 新版会自动补头。
2. **头是裸 marshal 数据（缺 16 字节头）时**：从同归档里拿一个完好的 stdlib pyc（如 `struct.pyc`/`pyimod01_os_path.pyc`），取其前 16 字节拼到目标文件前：

```bash
head -c 16 struct.pyc > fixed.pyc && cat entry >> fixed.pyc
```

3. 修好后回 §1 验 magic、§2 选调反编译。

## 4. 字节码直读兜底（反编译器全挂时）

```python
# dump_pyc.py —— 解释器版本必须与样本同大版本（≥样本版本），3.11+ code object 结构变了，
# 旧解释器 marshal.loads 直接报 bad marshal data (unknown type code)
import dis, marshal, sys
data = open(sys.argv[1], "rb").read()
code = marshal.loads(data[16:])          # 3.7+ 头 16 字节；2.7 是 8 字节
dis.dis(code, adaptive=False)            # 3.11+ 关键参数
```

- **3.11 自适应解释器坑**：pyc 里静态存的是非特化指令，但运行时被写回的 pyc 可能含 specializing 后的 quickened 指令和 `CACHE` 槽；`dis` 不加 `adaptive=False` 会把两者混着显示。看到 `BINARY_OP_ADAPTIVE` / `_QUICK` 后缀即知是特化形态，语义按基指令读。
- marshal 读不出 = 版本不匹配或文件是加密/截断的，先回 §1 验头。
- code object 里常量化秘密在 `co_consts`，字符串/密钥先扫这层：`code.co_consts` 递归打印。

## 5. PyArmor 初步识别与升级路径

静态特征（命中即改路线，不要硬啃）：

- 字符串含 `pytransform`、`__pyarmor__`、`__armor_enter__`/`__armor_exit__`、`pyarmor_runtime_000000`（PyInstaller 解包目录里出现同名 .pyd/文件夹 = 实锤）
- 入口 pyc 极薄：只有一个 `from pytransform import pyarmor_runtime; pyarmor_runtime(...)` 加一次 `__pyarmor__(...)` 调用
- 目标 code object 的 `co_code` 前几字节是加密块（marshal 可读但 dis 出来是垃圾）

处置：本篇只做识别与记录；解密在运行时发生，**转 re-dynamic**（hook marshal 加载点 / 运行后 dump 解密后的 code object，拿回本篇按 §4 直读）。静态 15 分钟无关键路径即转（铁律 6）。

## 6. 事故意识与落账纪律

- **pyc 头修复是静默错误高发区**：magic 错一个字节，反编译器报的不是"bad magic"而是莫名其妙的 parse error/opcode 表错乱，极易误判为"样本损坏"或"版本不支持"。每次修头后**先 `xxd -l 4` 肉眼对 §1 表**，再上反编译器。
- 修复产物按铁律 11 双源验证：反编译结果与 §4 dis 直读逐函数对照后才许下结论；`ledger.py conclude --source --independent` 标注。
- 开工即 `ledger.py observe` 落账：原始样本记 SHA256；解包出的 pyc、修头后的 fixed.pyc、反编译 .py 都是派生样本，分别落账、标注来源链。

---
工具上游：pyinstxtractor（github.com/extremecoders-re/pyinstxtractor，GPLv3）、uncompyle6/decompyle3（github.com/rocky，GPLv3）、pycdc（github.com/zrax/pycdc，GPLv3）；pyc magic 数值取自 CPython `Lib/importlib/_bootstrap_external.py`（PSF License）。本篇仅参考其用法与数据表，未复制正文。
