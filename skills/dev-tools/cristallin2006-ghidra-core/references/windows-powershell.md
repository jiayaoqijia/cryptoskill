# Windows / PowerShell 5.1 环境坑（每条都真实消耗过轮次）

在 Windows 宿主导.shell 里跑工具前必读。Git Bash 用户注意：dsh 宿主侧命令可能落在 PowerShell 5.1，本文所有"PowerShell"特指 5.1（`\"` 行为与 7+ 不同）。

## 1. 引号与参数传递（最痛）

- **`\"` 在 PowerShell 5.1 双引号字符串里不是转义**（反引号 `` ` `` 才是）——写了 `\"` 会**提前结束字符串**，后续参数全部错位，报错却指向无关的"缺少参数"（ledger.py 两次失败调用即此坑）。
  → 长文本一律 here-string `@'...'@`，且文本内避免双引号；**更稳的做法：长文本走文件**（ledger.py 已支持 `--conclusion-file/--evidence-file/--quote-file`）。
- 向 native exe 传**含内嵌 `"` 的字符串参数**会损坏参数边界（PS 5.1 已知缺陷）→ 走文件传递。
- `python -c "..."` 内联带引号/括号必然碎 → **一律写成 `.py` 文件再执行**。

## 2. 重定向与编码

- **PowerShell 的 `<` 输入重定向不存在** → 用 `cmd /c "... < input.txt > out.txt 2> err.txt"`。
- **`>` 重定向会破坏二进制**（PS 按文本重编码）：`adb exec-out screencap -p > x.png` 产出的 PNG 无法解析 → 设备端落盘再 pull：`adb shell screencap -p /sdcard/a.png && adb pull /sdcard/a.png`。
- **外部程序输出被 PS 重定向后可能是 UTF-16LE（带 `ff fe` BOM）** → 用 `[System.Text.Encoding]::Unicode` 读，或让程序直接写 UTF-8 文件。
- 控制台默认 **GBK/cp936**：Python 打印非 GBK 字符（如 `\uf900`）抛 `UnicodeEncodeError` → 脚本首行 `sys.stdout.reconfigure(encoding='utf-8', errors='replace')`，**stderr 同样要 reconfigure**（`[GATE]` 等报错行在 stderr，漏了照样乱码）。本家族全部宿主脚本已强制此约定。

## 3. 进程与路径

- `cd` **不改变** `[Environment]::CurrentDirectory`——.NET API 的相对路径会走偏 → 统一绝对路径。
- `Get-WindowsOptionalFeature` 需要提权 → 判定虚拟化可用性改用 `emulator-check accel`（实测 WHPX 可用）。
- Windows 上**被强杀的进程以裸 `exit code: 1` 收尾、不带 signal 标记** → 应判为"被打断"而非"命令失败"。
- 只取 `python` 输出的前几行来 grep JSON 容易截断漏项 → 结构化解析（`ConvertFrom-Json` / python 读全量），别 grep 文本片段。

## 4. 长耗时操作

下载 ~1GB 系统镜像、无头模拟器启动、`sdkmanager --list` 都可能超过默认超时 → **一律后台任务 + 输出落盘**，靠"只读可重试"判断是否安全重试，避免"中断后状态未知"。

## 5. 跨 shell 调用（Git Bash / WSL）

- **Git Bash 会把 `/root/...` 这类参数转成 Windows 路径** → `wsl` 命令前必须 `export MSYS_NO_PATHCONV=1`。
- Git Bash 的 `/tmp` 对 Windows 原生 python 不可见（它是 Bash 的虚拟挂载）→ 跨 shell 传文件用 `~/` 下的真实路径。
- **`wsl -e bash -lc '...'` 内联时，载荷里的一层反斜杠会被吞掉**（实测隔离复现，与 printf 无关，是参数传递层）：

  | 写法 | 实测 `od -c` | 结果 |
  |---|---|---|
  | `wsl -e bash -lc 'printf "A\nB" \| od -c'` | `A n B`（`41 6E 42`） | `\n` 变成字面量 `n` |
  | `wsl -e bash -lc 'printf "A\\nB" \| od -c'` | `A \n B`（`41 0A 42`） | 加倍可得到真换行 |
  | `wsl -e bash -lc 'printf "a\tb" \| od -c'` | `a t b` | `\t` 同样被吞 |

  → **纪律同 §1 的 `python -c`：一律把载荷写成 `.sh` 文件再 `bash file.sh`**（实测同一 payload 从文件走就是真换行）。
  本会话（本文档落地之后）正是被这条坑到：`printf 'DDDJJJBBBRRREEE\n'` 实际喂进去的是 `DDDJJJBBBRRREEn`，
  程序正确地回了 `NO!NO!NO!`，**一度看起来像"flag 结论被推翻"**。是"正 + 负对照成对"的 oracle 把假警报拆掉的 ——
  单看那一次输出会误判。
- **从 Windows 侧写入的 `.sh` / `.txt` 是 CRLF**，bash 会报 `$'\r': command not found` 或用错值 →
  执行前先 `sed -i 's/\r$//' <file>`。本会话每个脚本都跑过这一句，属固定动作而非偶发。
- **WSL 默认只有 x86_64 运行库**：跑 32 位 ELF 前先 `dpkg --add-architecture i386 && apt-get update && apt-get install -y libc6:i386 libstdc++6:i386`，
  否则 `/lib/ld-linux.so.2: No such file or directory`（`ldd` 还会误报 "not a dynamic executable"）。
