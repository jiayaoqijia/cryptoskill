# cyberchef CLI 速查(ctf-misc 本地增补,非上游文件)

确定性变换工具:505 个 op(编码/压缩/哈希/ XOR/ROT/字符码…),替代手工逐层解码和现场写一次性脚本。
**用法优先于自己写 python**:编码链题先用本工具;只有 op 覆盖不到(自研算法、需循环爆破)才写脚本。

## 用法

```bash
cyberchef '<recipeJSON>' [inputFile]     # 输入缺省读 stdin,结果写 stdout(无尾换行)
cyberchef --list [子串]                   # 列出/过滤全部 op 名,505 个
```

recipeJSON = op 数组;字符串 = 无参数 op,对象 = `{"op": 名字, "args": {...}}`:

```bash
echo -n "aGVsbG8=" | cyberchef '["From Base64"]'                      # → hello
echo -n "hello" | cyberchef '["Gzip","To Base64"]'                    # 压缩再编码(链式)
cyberchef '["URL Decode","From HTML Entity"]' input.txt               # 读文件
```

## 高频 recipe(已实测可用)

| 场景 | recipe |
|---|---|
| Base 家族 | `["From Base64"]` / `["From Base58"]` / `["From Base85"]` / `["From Base32"]` |
| Hex 互转 | `["From Hex"]` / `["To Hex"]`(注意大小写选项在 args) |
| URL/HTML | `["URL Decode"]` / `["From HTML Entity"]` |
| 字符码 | `[{"op":"From Charcode","args":{"base":10,"delimiter":"Space"}}]` |
| ROT | `[{"op":"ROT13","args":{"amount":13}}]` |
| 压缩 | `["Gunzip"]` / `["Bzip2 Decompress"]` / `["Zlib Inflate"]` |
| 哈希 | `["MD5"]` / `["SHA256"]`(输出 hex 字符串) |
| JWT | `["JWT Decode"]`(仅解码;伪造攻击用 `jwt_tool`) |
| 摩斯 | `["From Morse Code"]` |

## XOR 的正确写法(toggleString 坑)

XOR 的 Key 参数是 toggleString,必须写成对象,`option` 是 key 的编码:

```bash
echo -n "1e0d1b1d4b" | cyberchef '["From Hex",{"op":"XOR","args":{"Key":{"string":"42","option":"Hex"}}}]'
```

- `option` 可选:Hex / UTF8 / Latin1 / Base64 / Decimal / Regex
- 写 `"Key":"42"` 会报 `Scheme must be one of...`——那是参数错位到 Scheme 槽位了
- **XOR 爆破单字节 key 不归这里**——用 `xortool`(自动定 key 长 + 爆破)

## 限制

- **Magic op 不可用**(flow control 类 op 被 Node API 禁用)——自动识别编码请走 `encodings.md` 的判型流程 + `--list` 猜 op
- 输出二进制时被 wrapper 按 UTF-8 解码,含不可见字节请接 `| xxd`
- op 确切参数名拿不准:读 `/opt/node24/lib/node_modules/cyberchef/src/core/operations/<Op名>.mjs` 的 `this.args` 定义
