> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# 固件 / 嵌入式逆向（判型 → 提取 → 导入 Ghidra → 仿真选型）

> **分工边界**：本篇管固件镜像的判型、文件系统提取、架构识别、嵌入式反编译注意事项与仿真选型。
> 不管：raw 固件导入 Ghidra 的命令细节（ghidra-core references/headless.md §6）、CTF 通用 flag 狩猎与求逆纪律（ghidra-static ctf-patterns.md）、反分析（anti-analysis.md）、动态调试细节（re-dynamic）、APK/安卓固件（android-re）。

## 1. 环境事实（本机实测；doctor.py 工具注册表为实时真相源）

| 工具 | 状态 | 备注 |
|---|---|---|
| `file` / `strings` / `readelf` / `xxd` | ✅ WSL | binutils 系只在 WSL，Git Bash 一律加 `wsl -d Ubuntu -u root --` 前缀（triage.md §4 注） |
| `unsquashfs` | ✅ WSL | SquashFS 直接解 |
| `qemu-system-x86_64` | ✅ WSL | 注册表 `qemu(wsl)`；**无 ARM/MIPS 整机版**（qemu-system-arm/mips 未装） |
| `binwalk` | ❌ 未装 | WSL `apt install binwalk`；本篇按未装写保底路径（§2），勿指望它一把梭 |
| jefferson / ubi_reader / sasquatch / cpio | ❌ 未装 | 安装提示见 §3 各行 |
| qemu-user（`qemu-arm-static` 等） | ❌ 未装 | WSL `apt install qemu-user-static` |
| firmadyne | ❌ 未装 | 仅提思路，见 §6 |

## 2. 判型（无 binwalk 的保底路径）

1. `file firmware.bin`（WSL）——认得出 uImage/TRX/cpio/gzip 就直接定性。
2. `xxd firmware.bin | head -32` 看 vendor 头：TRX=`HDR0`（Asus/Linksys 旧款）、uImage=`27 05 19 56`、CHK=`2a 23 24 5e`（TP-Link）、DLOB（D-Link 加密包装）。
3. 扫已知 magic 偏移（binwalk 签名扫描的手工等价物）：

```bash
wsl -d Ubuntu -u root -- python3 - <<'EOF'
data = open("/mnt/c/path/firmware.bin","rb").read()
MAGIC = {b"hsqs":"squashfs-le", b"sqsh":"squashfs-be", b"\x85\x19":"jffs2", b"UBI#":"ubi",
         b"070701":"cpio-newc", b"\x1f\x8b":"gzip", b"\xfd7zXZ":"xz",
         b"\x28\xb5\x2f\xfd":"zstd", b"\x27\x05\x19\x56":"uImage"}
for m, name in MAGIC.items():
    off = 0
    while (i := data.find(m, off)) != -1:
        print(f"{name:12s} @ 0x{i:x}"); off = i + 1
EOF
```

4. **熵分析**（binwalk `-E` 等价物，逐 4KB 块）：

```bash
wsl -d Ubuntu -u root -- python3 -c "
import math, collections; d = open('/mnt/c/path/firmware.bin','rb').read()
[print(f'{o:08x} {-sum(v/n*math.log2(v/n) for v in collections.Counter(b).values())/8:.3f}') for o in range(0,len(d),4096) if (b:=d[o:o+4096]) and (n:=len(b))]"
```

   判读：>0.95 ≈ 加密或高熵压缩（**高熵≠加密**——先试解压，全部失败才谈加密）；0.7–0.95 压缩段；0.3–0.7 代码/字符串；<0.3 填充区。熵分布与预期不符（如题目暗示可解却全段 0.99）→ `ledger.py anomaly` 落账（铁律 12），不许当噪声放过。装了 binwalk 之后：`binwalk firmware.bin` 签名扫描、`binwalk -Me firmware.bin` 递归提取。

## 3. 提取对照表（按 §2 认出的格式选行）

| 格式 | 工具 | 命令（均在 WSL） | 未装备注 |
|---|---|---|---|
| SquashFS | `unsquashfs` ✅ | `unsquashfs -d rootfs/ part.sqfs`；非零偏移先 `dd if=fw.bin of=part.sqfs bs=1 skip=$((0xOFFSET))` | 非标 LZMA 变种（老 Realtek SDK）解不开 → sasquatch（未装：apt 无此包，需源码构建 devicarty/sasquatch） |
| JFFS2 | jefferson | `jefferson -d rootfs/ part.jffs2`（大端加 `-b`） | 未装：`pip install jefferson` |
| UBI/UBIFS | ubi_reader | `ubireader_extract_files part.ubi -o rootfs/` | 未装：`pip install ubi-reader` |
| cpio initramfs | `cpio` | `mkdir rootfs && cd rootfs && cpio -idm < ../initrd.cpio`（gzip 包壳先 `zcat`） | 未装：`apt install cpio` |
| gzip/xz/zstd 裸压缩段 | 系统自带 | `dd` 切出后 `zcat` / `xz -d` / `zstd -d` | — |
| 多分区（A/B） | `dd` | `dd if=fw.bin of=part_a.bin bs=1 skip=$((0x100000)) count=$((0x700000))` | — |

- **产物锁定**：每切出一个新文件，当刻 `ledger.py observe <样本> --tool dd --note "part_a.sqfs sha256=$(sha256sum part_a.sqfs)"`（evidence-ledger.md 六条规则之 6）。
- rootfs 第一扫（硬编码凭据快赢）：

```bash
wsl -d Ubuntu -u root -- bash -c 'cd /mnt/c/path/rootfs && \
  cat etc/shadow 2>/dev/null; \
  grep -rniE "password|secret|api[-_]?key" etc/ 2>/dev/null | head -40; \
  find . \( -name "*.pem" -o -name "id_rsa*" -o -name "*.key" \) | head; \
  grep -rniE "flag\{" . 2>/dev/null | head'        # flag regex 权威表见 triage.md §4
```

  `/etc/shadow` 弱 hash → hashcat（注册表 `hashcat(wsl)`；按 `$1$/$5$/$6$` 前缀选 `-m 500/1800/7400`）。

## 4. 架构识别 → Ghidra 导入

1. `file rootfs/bin/busybox`：`LSB`=小端、`MSB`=大端。常见组合：MIPSel（MTK/雷凌）、MIPSbe（Broadcom 旧款）、ARM LE（现代设备绝大多数）、AArch64。
2. processor 串与基址：

| 架构 | Ghidra processor | 基址 |
|---|---|---|
| ARM LE（Linux 用户态 ELF） | `ARM:LE:32:v7` | ELF 自带，不用猜 |
| ARM Cortex-M 裸核 | `ARM:LE:32:Cortex` | `0x08000000`（STM32 flash）/ `0x00000000`（向量表在 0 时） |
| MIPS 小端 | `MIPS:LE:32:default` | `0x80000000` 起步试 |
| MIPS 大端 | `MIPS:BE:32:default` | 同上 |

3. **基址反推法**（ELF 头被剥/纯 raw dump）：先按 `0x80000000` 导入 → 看字符串 xref 目标地址与字符串实际偏移的差值，差值即真实基址；Cortex-M 看文件开头中断向量表——offset 0 = 初始 SP（指向 RAM，如 `0x2000xxxx`），offset 4 = Reset_Handler 入口，入口值即 flash 真实基址。
4. 导入命令照 headless.md §6（`-loader BinaryLoader -baseAddress <基址> -processor <串>`，路径正斜杠）；建好后照常 `driver.py exec`。

## 5. 嵌入式反编译注意

- **MMIO 不是内存**：对外设寄存器段（STM32 `0x4000xxxx` 起、ESP32 `0x3FF4xxxx`）的读写是硬件副作用，反编译器渲染成普通全局变量访问。识别后给地址段建 label+注释，禁止按"无意义读写"忽略——硬件加密引擎/密钥寄存器常藏这里（对照 triage.md §7 硬件 AES 行）。
- **无 ELF 头时函数边界靠序言模式**：ARM Thumb `push {..., lr}`（`2d e9` / `b5 xx`）、ARM `e92d`（stmfd sp!）、MIPS `addiu sp, sp, -N`（`27 bd ff`）。headless 脚本按字节模式扫候选入口 → Create Function → 重分析。
- 裸核无 imports 锚点：triage.md §1 硬门不适用，改用**字符串 xref 反推功能函数** + 中断向量表枚举入口。
- 结论照常入账：`ledger.py conclude --source read_views --independent ... --quote ...`（铁律 8/10——关键常量跨工具对照后再锁）。

## 6. 仿真（能跑单个 ELF 就别起整机）

- **首选 qemu-user 跑单个服务**（httpd/cgibin），比整机仿真便宜一个数量级：

```bash
wsl -d Ubuntu -u root -- bash -c 'apt install -y qemu-user-static   # 未装，先装
qemu-arm-static -L /mnt/c/path/rootfs /mnt/c/path/rootfs/usr/sbin/httpd'
# 调试：加 -g 1234 起 gdbserver；另端 gdb(wsl) 里 target remote :1234
```

  坑：`/proc` 缺失 → 先 `mount -t proc proc rootfs/proc`；`nvram_get` 拿不到值导致 httpd 崩 → LD_PRELOAD 假 nvram 库，或上整机仿真。
- **整机仿真**：本机只有 `qemu-system-x86_64`，**ARM/MIPS 整机起不来**。x86 固件 / MBR 题可用（命令见 triage.md §7 MBR 行）。
- **firmadyne 思路**（未装，知道即可，别自己重造）：extractor 提 rootfs → getArch 判架构 → makeImage 装配内核+rootfs → inferNetwork 推网络配置 → run.sh 起 qemu-system，`libnvram.so` hook 所有 nvram 调用返回默认值。需要真整机时 `git clone firmadyne/firmadyne`。
- 仿真行为与静态分析对不上 → `ledger.py anomaly` 落账（铁律 12）。

## 7. CTF 固件题常见形态

| 形态 | 落点 |
|---|---|
| 路由/摄像头固件藏 flag | rootfs 先 `grep -rniE "flag\{"`；扫不到查 www/ 目录（js/cgi 注释）、`/etc_ro` 出厂配置 |
| UART/boot 日志文本 | 日志里挖地址泄露（基址/栈地址）配合 §4 基址反推；尾部常直接打印 flag 或调试菜单口令 |
| 配置分区 / NVRAM dump | 无文件系统 magic 的裸分区：`strings -n 6` + §2 熵分段；`key=value` 形态里翻 `flag=`/`key=` |
| 加密分区 | 熵 ~0.99 但旁边有明文 bootloader → 逆 bootloader 找解密函数/key；同芯片公开解密方案先搜 |
| 固件内嵌 ELF 服务 | §6 qemu-user 跑起来当 oracle，配合 ctf-patterns.md §5 侧信道表 |

溯源意识：真实固件与 CTF 同一纪律——每条"flag/凭据在 X 偏移"必须 `conclude` 带 `--quote` 原文（铁律 10），禁止凭记忆交付。

署名：本文借鉴 zhaoxuya520/reverse-skill（MIT License）之 `skills/firmware-pentest/references/extraction-methodology.md`（vendor 头 magic、文件系统提取对照、熵判读区间）与 `skills/firmware-pentest/references/emulation-and-fuzz.md`（qemu-user / firmadyne 仿真分档），已按本机环境实测结果重写与裁剪。
