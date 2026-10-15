# Go 二进制逆向（triage `lang_hints.go=true` 时读本文件）

## 1. 识别（含 stripped 二进制）

stripped 也抹不掉的指纹：

| 指纹 | 位置 | 含义 |
|---|---|---|
| `\xff Go buildinf:` | 文件内字节序列 | buildinfo magic，**Go 版本字符串在其后 256 字节内** |
| pclntab magic `fb ff ff ff 00 00` | section 头部 | Go 1.2–1.15 |
| pclntab magic `fa ff ff ff 00 00` | 同上 | Go 1.16–1.17 |
| pclntab magic `f1 ff ff ff 00 00` | 同上 | Go 1.18–1.19 |
| pclntab magic `f0 ff ff ff 00 00` | 同上 | Go 1.20+ |
| 字符串 `go.buildid` / `runtime.gopanic` | 字符串表 | triage 字符串扫描已覆盖 |

`buildinfo` 后还能挖出模块路径（`github.com/...`）→ 直接推断程序用了哪些库、大概是什么工具。

## 2. 三个必踩的坑

- **Go string 是 `{ptr, len}` 不是 NUL 结尾**——Ghidra 默认字符串分析会漏大量字符串，strings 命令输出也碎。对策：GoReSym 恢复、或靠 xref 从代码反查字符串地址对。
- **stripped ≠ 没符号**：pclntab 里仍保留完整函数名和文件路径，GoReSym 能全部恢复。
- **函数数量爆炸**（runtime + 依赖全静态链进来）：**只看 `main.*` 包的函数**，其余全是噪音。

## 3. 标准流程

```bash
GoReSym -d <bin>          # 恢复函数名/类型/源文件行号（stripped 也行）
# 或 Ghidra 内：装 golang-loader 插件辅助字符串/类型恢复
```

然后在 Ghidra 里 `functions <bin> | grep main.` 锁定业务逻辑。

## 4. garble 混淆（CTF 出题人爱用）

特征：函数名变成乱码哈希、字符串全部加密、但 pclntab 结构还在。

- **GoResolver**（CFG 相似度匹配已知库函数）恢复库函数名，剩下的小集合就是业务代码
- garble 的字符串解密是运行时统一 stub 做的——找到解密 stub，`emulate-function` 或 oracle.py 批量跑一遍拿明文，不要逐个手逆

## 5. PyGhidra 定位 pclntab（脚本骨架）

```python
# 在 exec_code.py 里跑（PyGhidra 语境；exec_code 已注入 memory/monitor）
# 注意：Memory.findBytes 只有 byte[] 重载，传 bytes 别传 str
magics = {
    "fb ff ff ff 00 00": "go1.2-1.15",
    "fa ff ff ff 00 00": "go1.16-1.17",
    "f1 ff ff ff 00 00": "go1.18-1.19",
    "f0 ff ff ff 00 00": "go1.20+",
}
pat = bytes.fromhex("ff 20 47 6f 20 62 75 69 6c 64 69 6e 66 3a")  # "\xff Go buildinf:"（ff 后有空格 0x20）
for block in memory.getBlocks():
    addr = block.getStart()
    while addr is not None:
        addr = memory.findBytes(addr, block.getEnd(), pat, None, True, monitor)
        if addr is not None:
            print("buildinfo @", addr)
            # 其后 256 字节内是 Go 版本字符串；可 createLabel + plate comment 锁定
            addr = addr.add(1)
```

（pclntab 同理，逐 magic 扫；版本确定后写 plate comment 锁定。实测：stripped Go 1.26 PE 里 buildinfo 命中、版本串 `go1.26.5` 紧随其后；pclntab `f0 ff ff ff` 前缀命中但后两字节不一定是 `00 00`，按 4 字节前缀匹配更稳。）
