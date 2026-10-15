# CTF2 实战失败信号 → 下一步

| 信号 | 立即动作 |
|---|---|
| `decompile` 空、重叠指令、伪码栈槽/参数不可信 | `disassemble` 对真实指令与函数入口；栈变量按 disp 区间重建。先用奇偶、范围、长度快速证伪伪码。 |
| `search-decompiled` 超时或 parse fail | 查字符串文件偏移；用 PE/ELF 格式库映射 VA 后 `xrefs-to`，必要时再向上追一层调用者。不要手写 `objdump -h` 列宽解析。 |
| pyc 反编译报错/截断，求逆自洽却乱码 | 看 magic 和文件头；`pydisasm`/xdis 读真实 `LOAD_CONST` 与常量池。若头后是 ASCII，检查伪 pyc；不要把反编译渲染当权威值。 |
| Ghidra PIE 地址设 gdb 断点失败 | 用运行时 mappings 算 load bias：`runtime = mapping_base + (ghidra_va - ghidra_image_base)`；先确认目标映射已加载。 |
| 静态显示常量比较，原样输入却被拒 | 跟到比较调用内部，核对变换、运行期指针与 varargs；直接喂字面量做负对照。 |
| 方程求出多个程序接受输入 | `model_structure.py length` 核对被检查下标，或 `matrix` 判模矩阵可逆性；记录自由位/多解，寻找题面、附件或平台独立定值。 |

复合变换求逆前写明正向流水线 `A → B → C`，逆向按 `C⁻¹ → B⁻¹ → A⁻¹`。双向往返只查实现接线；模型与程序一致还要用已知输入或运行时中间态逐字节对拍。模矩阵 `gcd(det, modulus) != 1` 只证明映射不可逆，目标是否有解仍须另证。
