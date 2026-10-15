# Rust 二进制逆向（triage `lang_hints.rust=true` 时读本文件）

## 1. 识别特征串

```
panicked at          core::panicking          called `Option::unwrap()` on a `None`
std::rt::lang_start  .cargo/registry          rustc 1.xx.y
```

## 2. 最有价值的一招：panic 路径 = 源码地图

`panicked at '...', src/main.rs:42:17` 这种字符串直接泄露**源文件名 + 行号**。
`strings <bin> | grep panicked` 先把所有 panic 点挖出来——按文件/行号就能拼出程序的大致模块结构，比看反编译快得多。

## 3. 依赖还原（推断能力面）

panic 路径里的 `.cargo/registry/src/.../cratename-x.y.z` 用正则批量提取：

```bash
strings <bin> | grep -oP '\.cargo/registry/src/[^/]+/[\w-]+-\d+\.\d+\.\d+' | sort -u
```

crate 名 + 版本 → 直接查该 crate 源码，等于拿到部分"源码级"参考。

## 4. 三个结构性坑

- **单态化（monomorphization）**：同一泛型函数按类型复制多份，逻辑雷同——**不要逐个函数读**，从字符串 xref 入手定位"干实事"的那份。
- **unwrap/expect 链**：大量 `Result/Option` 解包噪音淹没真实逻辑；反编译里看到对 `core::panicking::panic*` 的调用直接跳过。
- **字符串是 fat pointer `{ptr, len}`**（同 Go）：非 NUL 结尾，Ghidra 字符串分析会漏，靠 xref 补。

## 5. 符号

- mangled 名 `_RN...` / `_ZN...`：`rustfilt` 批量 demangle（`strings <bin> | grep '^_R' | rustfilt`）
- stripped 时 panic 字符串里的路径/行号就是唯一的符号源，优先榨干它
