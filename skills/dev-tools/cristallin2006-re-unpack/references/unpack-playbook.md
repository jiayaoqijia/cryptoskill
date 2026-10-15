# Unpack Playbook（re-unpack 细节手册）

工具：`$UNP/unpacker.exe`（Unpacker venv）与 `$UPX`（原生 UPX）。配置 `~/.kimi-work/unpacker-src/config/config.yaml`：`upx_prefer_native: true`、IAT 重建默认开、多层 max 5。

## 检测层（detect 怎么判断的）

多方法融合，输出 packer id + confidence：
1. **签名**：文件内容特征字节
2. **节名**：UPX0/UPX1、`.aspack`、`.themida`、`.vmp0/1/2`、`.MPRESS1/2`（注意：检测用 UPX0/UPX1 节名而非 `UPX!` 魔数——后者在已脱壳文件数据里会误报）
3. **熵**：节级 Shannon 熵（packed 节通常 >7）
4. **启发式**：入口点在最后一个节、可写可执行节、IAT 极小等

**已知坑**：检测层可能报 `not packed` 但编排层仍按启发式尝试 UPX 并成功（实测 UPX+`--force` 打的包即如此）——看 layer 结果比看 Detected 行更可靠。

## 各壳对策

### UPX（Tier A，直接解压，不执行样本）

- 原生 `upx -d -o <out> <sample>`（Unpacker 自动调；PATH 须有 upx）
- **GUARD_CF 的 PE 要先 `upx --force` 打包**才能被 upx 自己解（实测 whoami.exe 如此）；拿到别人用 --force 打的包时 `upx -d` 可能也报不支持，同样加 `--force`
- **元数据被篡改**（`upx -d` 报 not packed / header corrupted）→ 修头：
  1. 找 `UPX!` 魔数（l_info 起始），被清零/改写就恢复 `55 50 58 21`
  2. 检查 p_info（`UPX!` 后 12 字节：p_filesize/p_blocksize）是否被抹
  3. PackHeader 魔数 `0x21585055`（"UPX!"LE）完好但版本/方法字段被改 → 按 UPX 源码 `PackHeader::fill` 的合法域修
  4. 修完 `upx -d`；仍失败进失败阶梯 ③
- 验证锚点：unpacked 大小 ≈ 原始、熵 5~6、字符串数翻倍级增长

### ASPack / Themida / MPRESS（Tier B，Unipacker 仿真 dump，**PE32 only**）

- Unicorn 仿真入口 stub → 检测"脱壳完成"（节跳转 / write+execute / ASPack 内建逻辑）→ dump 内存镜像 + 修 IAT
- Unipacker 有本仓库补丁：逐页安全读内存（未映射页补零）+ dump 容错（IAT 修不了就清零 import 目录也写出）
- **PE32+（64 位）直接报 "Not a valid PE file"**——别在 64 位上浪费时间

### VMProtect（Tier B）

- 32 位：同 Unipacker unknown 模式（仿真到启发式停，dump）；可能需多轮（每层剥一次）
- 64 位：Qiling + Windows rootfs，带超时跑，从内存按 image base + SizeOfImage dump；**无"脱壳完成"启发式，dump 可能是部分的，IAT 不修**——交付时必须标注置信度

### 未知/自定义壳（generic）

- 检测能报 packer id 但无对应 unpacker → 明确报"未实现"，进失败阶梯 ③④
- 自定义壳常见只有几 KB stub + 一大块加密数据：XOR/RC4 居多，仿真（emulate-function）通常比完整逆向快

## 多层壳

编排层自动：unpack → 对产物再 detect → 再 unpack，直到 `max_layers`（默认 5）或测不出壳。每层输出独立文件（`sample.unpacked.<packer>.exe`），Final output 是最内层。
**注意**：`--max-layers` 别调大——死循环壳（自指）会烧时间；到 5 层还没完说明检测在误报，停手换阶梯。

## IAT 重建

- Unpacker 编排层默认 `rebuild_iat: true`（PE rebuilder 修 import 目录）
- IAT 重建失败的产物仍可读代码，但 imports 表不准——triage 回链时若 clean_iat_warning 误报，回头查 IAT
- 验证 IAT 修没修好的快捷方式：脱壳产物 `triage` 后 imports 里应出现真实 API 名而非只有 LoadLibrary/GetProcAddress

## 验证清单（复制即用）

```python
# python - 熵对比（packed 应 >7，unpacked 应 5~6）
import math
from collections import Counter
def entropy(p):
    d = open(p, "rb").read(); c = Counter(d); n = len(d)
    return -sum((v/n)*math.log2(v/n) for v in c.values())
```

1. 熵：packed vs unpacked（记录数字）
2. 大小：unpacked > packed
3. 字符串：`re.findall(rb"[ -~]{5,}", data)` 计数对比 + DLL 名出现
4. 回链：`rpc_driver.py ensure` + `triage` 正常出结果（imports 有真实 API）

## 安全注意

UPX 是纯解压不执行样本，安全；Unipacker/Qiling 会**在仿真器里跑样本代码**（API 走 stub，不碰真机），但 Qiling 可映射宿主路径——用自包含 rootfs，别映射敏感目录；所有样本按敌意对待，分析机与生产机隔离。
