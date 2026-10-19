# 复合变换：语义、有限搜索与验证

适用于布局已明确、有少量有来源的操作/参数假设的本地数据。已知算法可直接求逆或调用库；真正加密、哈希、任意 VM 和状态机不属于下面字节搜索器的完备覆盖范围。

## 建模与减少重复

注明输入输出、阶段顺序、位宽、端序、截断、索引、周期、状态与参数来源。若声明的是正向编码链，解码要将阶段逆序并各自求逆；从数据到候选的假设链则直接应用。不要混淆这两种方向。

| 操作 | 可逆条件与常见误判 |
|---|---|
| XOR 常量/周期密钥 | 同密钥、相位与索引才自逆；未知四字节密钥不是四个候选 |
| 模加减、`a*x+b mod 2^w` | 加减互逆；a 为奇数才有唯一仿射逆；w、截断位置和有符号提升须确认 |
| ROL/ROR | 同位宽互逆；位旋转不同于字节序交换，机器对旋转计数的处理需核对 |
| 逆序、字内反转、位反转、半字节交换 | 明确作用于整体、定宽组还是单字节；分组须符合边界 |
| 索引混合、累加或状态更新 | 起始索引/状态是语义一部分，不可按无状态常量运算随意合并 |

同族连续可以有效，例如 XOR 后 ADD。相同字节域的连续 XOR、旋转或仿射可按代数合并；跨索引、状态或布局操作不能凭族名去重。中间结果可能是二进制，不因不可打印而剪枝。

原始路径数为各阶段选择数之积，再对管道、切片与参数来源求和；每条路径还需计算和判断。成本估算不等于耗时保证。先约束方向、位置、长度、周期和候选密钥；扩展空间应有新的结构依据。一次实验的预算不替代用户目标或全局任务时限。

## 本地搜索器

`ghidra-core/scripts/transform_search.py` 使用 Python 3.10+ 标准库，不执行目标、联网或提交。当前仅支持 **8 位字节域**：xor（含零字节密钥与显式相位）、add/sub、affine、rol/ror、reverse、word_reverse（2/4/8 字节组）、nibble_swap、bit_reverse、index_xor/index_add。32 位算术、状态机、编码与压缩等需使用已有工具或另建模型，不悄悄降为字节域。

先运行 `python3 transform_search.py self-test`。下面是纯合成的 JSON：外层 pipelines 是管道备选；每个管道按顺序列阶段；每个阶段列显式操作候选。没有隐含全族枚举或固定族排列。

```json
{
  "version": 1,
  "source": {"hex": "00010203", "basis": "synthetic local bytes"},
  "width": 8,
  "direction": "forward",
  "pipelines": [[
    [{"op":"xor", "key_hex":"00", "basis":"identity control"},
     {"op":"xor", "key_hex":"5a", "basis":"synthetic candidate"}],
    [{"op":"add", "value":0}, {"op":"add", "value":19}]
  ]],
  "criteria": {"prefix_hex":"5a5b"},
  "budget": {"max_input_bytes":4096, "max_paths":4, "max_byte_ops":10000},
  "top":4
}
```

```bash
python3 transform_search.py search spec.json --estimate
python3 transform_search.py search spec.json --report recovery-report.json
python3 transform_search.py replay recovery-report.json --rank 1 --output candidate.bin
```

source 选择 `hex` 或 `path` 之一；path 相对 spec 文件。可提供 sha256 校验整个输入，offset/length 选择区域；报告保存原输入哈希，重放会重新核对。max_input_bytes 限制整个输入读取量，较大的样本先提取有依据的区域。仅声明内存地址不会自动读取进程。

direction=forward 按所列阶段应用；inverse 将阶段倒序并求各候选逆。偶数仿射乘子在 forward 可分析，inverse 返回 unsupported。`xor` 的 phase 默认为 0；`index_*` 使用所选区域从 0 开始的 i，`a*i+b mod 256` 为混入值，其他起点须在 b 中明确建模。word_reverse 仅允许对齐分组。空管道 `[]` 是明确的恒等对照。

判据可用 prefix_hex、suffix_hex、length、sha256，多个条件须全部满足；ASCII 前后缀可显式设置 ascii_case_insensitive=true。没有判据时 matches_declared_criteria 为 null。可打印率、UTF-8 与 magic 仅作分项排名；命中这些条件不代表目标接受，也不代替完整格式解析或目标验证。

max_paths 限制实际考虑的原始路径；max_byte_ops 是显式工作量预算（含 256 值规范化及数据变换，不是 CPU 指令或秒数）。预算耗尽返回 incomplete 与未覆盖数量；complete 只表示声明空间全部考虑，不表示有解或全局无解。没有任何硬判据命中时仍保留排名候选；不因此自动扩展范围。

相邻、与位置无关的字节操作用完整 256 值映射证明等价后合并；周期密钥、索引及布局操作是边界。缓存仅减少等价路径的重复执行；有限缓存淘汰会重算，不丢弃搜索分支。top 只限制最终候选列表，不按分数裁掉中间路径；报告给出考虑/执行/等价跳过/缓存淘汰数及原始空间。

完整链、参数和来源可能包含秘密，仅在显式 --report 指定的新文件内保存（Linux 权限 0600）；stdout 不输出解码字节或完整密钥链。replay 验证源与结果哈希后写入指定的新文件，不覆盖已有文件。JSON 输入与可重放报告支持至多 1 MiB、管道最多 64 阶段、top 最多 1000；超出返回错误/unsupported，不静默截断。结果版本是 1.0.0。

搜索器自检、合成已知答案、原目标确认分别记录。未知有效输入时不伪称已完成正负例验证。连续未中时复查数据、方向、参数来源和覆盖缺口，再决定改假设、补材料或合理暂缓，不按固定失败次数强制换工具。

方法参考：[CyberChef Magic](https://github.com/gchq/CyberChef/wiki/Automatic-detection-of-encoded-data-using-CyberChef-Magic) 的结构识别和候选排名、[Binary Refinery](https://github.com/binref/refinery) 的可组合字节变换；工具独立实现，未移植源码。CyberChef CLI 的 Magic 可用性须单独探测，不能把本机 CLI 当现成搜索后端。
