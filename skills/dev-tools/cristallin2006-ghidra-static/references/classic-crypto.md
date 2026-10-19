> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# 经典密码/编码手撕（认出算法之后的求逆执行）

**分工**：认出算法（常量指纹）看 ghidra-core `references/crypto-ident.md`；流水线总纪律与速查表看 `ctf-patterns.md` §3/§8。本篇管**认出之后怎么落地求逆**——换表 base64 / RC4 / TEA 家族 / 自定义置换的具体执行细节与事故点。

已确认的经典算法按本篇处理；未知数据与复合搜索见 [数据驱动恢复](data-driven-recovery.md) 和 [复合变换](transform-pipelines.md)。crypto_sanity.py 仅提供支持格式的局部诊断，原始字节和目标语义优先；关键结论按当前 analysis-session/analysis-memory 接口记录。

## 1. 换表 Base64（最高频自定义编码）

**辨识**：
- 函数体是标准 base64 骨架（`>>2`、`&0x3F`、按 3 字节组处理、`=` 补齐），但**标准 alphabet `A-Za-z0-9+/` 在二进制里搜不到** → 换表。
- `.rodata`/`.data` 里一段 64 字节无重复的可打印字符串（可含乱序），即置换表。`search-strings` 或 xref 编码循环的查表地址定位。

**求逆（两行逻辑，不要逆算法）**：
```python
import base64
TABLE = "<从二进制 dump 的 64 字符置换表>"
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
dec = base64.b64decode(ct.translate(str.maketrans(TABLE, STD)))
```

**事故点**：
1. **padding 不按标准**：有的实现补 `=` 以外的字符，或干脆不补。长度 % 4 != 0 先手工补 `=` 再喂 b64decode；补了还报错就回 Ghidra 核对补齐逻辑。
2. **表在 .data 而非 .rodata**：说明表可能运行时先被变换（XOR/打乱）再用——静态 dump 的是**初始态**，用 oracle.py 在编码函数入口处 dump 运行时表对照，不一致就取运行时那份。
3. **编码≠加密**：换表 base64 只是 obfuscation，解出来还是中间态，继续往流水线下一级走（见 §4）。

## 2. RC4

**辨识**（crypto-ident.md §1 已列指纹，此处是反编译形态确认）：
- KSA：一个 256 循环做 `S[i]=i`，紧接第二个 256 循环 `j=(j+S[i]+key[i%klen])&0xFF; swap`。
- PRGA：循环里 `i=(i+1)&0xFF; j=(j+S[i])&0xFF; swap; out ^= S[(S[i]+S[j])&0xFF]`。
- 特征噪声：大量 `& 0xFF`、双层 swap。

**求逆纪律：直接 Python 重写，不逆算法本体**——30 行重实现 + 已知密文/key 反解，比逐行核对反编译便宜一个数量级。C 的 `char` 符号性是唯一坑：反编译里 `S[i]` 参与运算若按 signed char 提升，索引会变负——**Python 侧全部 `& 0xFF` 兜底**，然后正向验证（§4 第 1 步）会立刻暴露差异。
- key 来源：硬编码缓冲区 xref 直接读（`read_views.py --expect-hex` 对照渲染文本）；`key[i%klen]` 的 klen 从 KSA 循环的取模立即数确认。
- RC4 自逆：解密 = 同函数再跑一遍，求逆题甚至不用写 decode。

## 3. TEA / XTEA / XXTEA

`0x9E3779B9`（及其累加形态 `sum += 0x9E3779B9`）一出即定性（crypto-ident.md §1）。认出后**三个变种参数必须逐一钉死再动手**：

| 检查项 | 怎么定 | 事故点 |
|---|---|---|
| 端序 | 看密文/key 拷贝进 v0/v1 处是 `memcpy`（小端直读）还是逐字节 `<<24\|<<16\|<<8`（大端拼） | 端序错 = 解出来每 4 字节组内字节全反 |
| 轮数 | 循环计数常量 / `sum` 终值：32 轮标准 TEA 终值 `0xC6EF3720` | 64 轮变种常见；数不准就抄终值反推 |
| 变种 | TEA：`sum+=delta` 在表达式内；XTEA：key 索引含 `sum`/`sum>>11`；XXTEA：按块长 n 循环、`MX` 宏 | 三者结构神似，认错变种正向验证必挂 |

求逆写法：加密循环逆序、减 delta、交换 v0/v1 角色即可——TEA 家族求逆是机械变换，**但只在端序/轮数/变种三参数钉死之后**。key 是 4×u32 = 16 字节，`read_views.py` 取数时防渲染吞前导 0。

## 4. 流水线求逆纪律（encode 题复盘核心教训）

`flag → 变换A → 变换B → … → 比较目标` 类题目，标准死法是一次性写完整个逆算法再调试——错了不知道错在第几级。纪律（与 ctf-patterns.md §8 互补，本篇是执行细则）：

1. **建立可核对的模型**：已有输入输出时可复现正向阶段；可逆关系明确时也可先求逆再全长重放。自造向量只检验实现，不能代替实际目标证据。
2. **用中间态定位差异**：按问题使用 oracle.py --break/--dump、实际进程或静态证明；oracle.py 是仿真后端。出现差异先核对布局、位宽、ABI、初始化和环境，不无条件要求 GDB。
3. **逆变换按正序的倒序拼**：各阶段须可逆且语义明确；往返自检可能共享错误，必要时增加独立实现、固定向量或目标对照。非单射阶段可能有多个原像。
4. **诊断不替代语义**：读取长度异常时复查对象边界与原字节；非标准 padding、编码或二进制结果不能仅凭通用检查器判错。缺少正例时明确保留模型不确定性。
5. 完整候选与全链路重放结果一起交接；可打印性或前两字节相符不足以确认。候选、模型自洽、原目标测试与外部接受分开记录，不自动提交。

**改表加密题教训**：流水线里只要有一级是"看起来像标准算法但实际改过"（换表、改轮数、改 delta），整链求逆会在最后一级才爆炸——逐段验证把爆炸半径锁在单级内。

## 5. 自定义置换 / S 盒定位

认出结构是查表变换但表未知时：

1. **零引用数据块扫描**：ghidra-core `scripts/unreferenced_data.py`——置换表/S 盒常被编译器算作"未被代码直接寻址"（实际被指针运算访问），落在零引用清单里。
2. 从编码/加密循环反查：找循环体内的查表基址（`MOVZX reg, byte [base + reg]` 形态），xref base 即表。
3. 表长 64 → 换表 base64（§1）；表长 256 且是 0–255 排列 → 置换盒或 RC4 S（§2）；表长 256 非排列 → AES 类 S 盒回 crypto-ident.md 对指纹。
4. 表在 .data → 先确认无运行时初始化改写（xref 写访问），有则取运行时 dump。

## 6. 工具路径速查（双平台）

| 用途 | Windows | WSL/Linux |
|---|---|---|
| 门控/取数/台账 | `python ghidra-core/scripts/{crypto_sanity,read_views,ledger}.py` | 同（路径换成 Linux 部署根） |
| 运行时抓中间态 | `python re-dynamic/scripts/oracle.py --break ... --dump ...` | 同 |
| Python 重实现 | re-tools-venv `Scripts/python.exe`（base64/struct 标准库够用） | `~/re-pwn-venv/bin/python` |
| 端序/ELF 辅助 | — | `readelf -x .data bin`（registry: readelf） |
| 批量搜常量 | rpc `find-bytes`（ghidra-core §5） | 同 |

---

借鉴声明：本篇纯自撰（素材来自家族 encode 题复盘与复合载体题复盘），未复制任何外部许可源内容。
