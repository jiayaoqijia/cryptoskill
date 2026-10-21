> 使用范围：本文保留专业配方。历史“铁律”、固定时间盒、工具顺序与每步台账要求已改为方法建议；当前会话/资源接口见 analysis-session，实际脚本以 --help 为准。证据结论限定输入、路径、环境与干预，允许未完成报告。

# C++ 二进制逆向（vtable / RTTI / STL 噪声 / MFC 消息映射）

**分工边界**：本篇只管 C++ 特有结构——vtable 恢复、this 指针类型化、RTTI 链、STL 内联噪声过滤、MFC 消息映射定位 handler。通用 flag 狩猎/XOR/VM → `ctf-patterns.md`；Go/Rust 各自的运行时结构 → `go-binary.md`/`rust-binary.md`；命令参数细节一律回 ghidra-core §5；动态侧（Frida/gdb/x64dbg）→ re-dynamic。观察/结论一律 `ledger.py observe`/`conclude` 落账。

```bash
SK="$HOME/.dsh/skills/ghidra-core/scripts"
RD="$SK/rpc_driver.py"        # 所有 rpc 命令：python "$RD" <命令> <binary> [参数]
```

## 1. 识别（5 分钟判定）

| 信号 | 判定 |
|---|---|
| 符号以 `_Z` 开头（`_ZN6Player6attackEi`） | Itanium ABI（GCC/Clang，ELF/MinGW）；Ghidra 的 GNU Demangler 分析器通常已自动解 |
| 符号以 `?` 开头（`?attack@Player@@QEAAXH@Z`） | MSVC mangling；含 `??$` 的是模板实例 |
| 字符串 `.?AV...@@` | MSVC RTTI TypeDescriptor 名 = 类名裸奔 |
| 导入/字符串 `__cxa_throw` `__cxa_begin_catch` `_Unwind` `.eh_frame` | Itanium 异常框架 |
| 导入 `__CxxFrameHandler3/4`、`.pdata` 丰富 | MSVC x64 异常框架 |
| 字符串 `vector`/`basic_string`/`bad alloc`/`length_error` | STL 内联展开，预备 §4 纪律 |
| `.data.rel.ro`（ELF）/`.rdata`（PE）里成串指向 .text 的指针 | vtable 候选 |

```bash
python "$RD" strings <bin> "typeinfo|vftable|cxa_throw|bad_cast|.\?AV"
python "$RD" symbols <bin> "_Z"          # Itanium mangled 符号兜底
```

WSL 里批量 demangle：`c++filt`（随 binutils，与 strings(wsl)/readelf(wsl) 同源）：`echo '_ZN6Player6attackEi' | c++filt`。

## 2. vtable 恢复（核心流水线）

认 vtable 的结构特征：

- **Itanium**：vtable 槽 -2 = typeinfo 指针，槽 -1 = offset-to-top（通常 0），槽 0 起是虚函数。
- **MSVC**：vftable 地址**上一格**（x64 即 `vftable-8`）是指向 RTTICompleteObjectLocator（COL）的指针，槽 0 起是虚函数。
- 构造函数里 `mov [reg], offset <vftable>`（store 立即数地址进对象头）= 最直接锚点：`find-bytes` 搜 vftable 地址的立即数，或对 vftable `xrefs-to` 反查构造函数。

列槽并解析目标：

```bash
python "$RD" list-vtable <bin> 0xADDR            # 或传符号名
python "$RD" list-vtable <bin> 0xADDR -c 16      # 强制槽数（边界符号缺失时）
```

输出每槽 `target_address/target_name`，`stopped_reason` 语义：`next_vtable_symbol`（权威边界）> `non_function_pointer`（首个非函数指针，MSVC 无 vftable 符号时主要靠它）> `cap`（硬顶 4096，需人工确认）。槽目标逐个 `rename-function` 为 `Class_method`（铁律 5）。

虚函数调用的反编译形态（认出即不被劝退）：

```c
(**(code **)(*this + 0x18))(this);          // 调用 vtable 槽 3（0x18/8）
(*(this->vftable->attack))(this, dmg);      // §3 类型化之后的形态
```

## 3. this 指针类型化（反编译质量质变的单点操作）

顺序 MUST（每步 daemon 内即刻生效）：

1. 先建 vtable 结构体，再建类结构体（field 0 恒为 vftable 指针）：

```bash
python "$RD" create-struct <bin> Player_vtbl "void * dtor" "void * attack" --if-not-exists
python "$RD" create-struct <bin> Player "Player_vtbl * vftable" "int hp" --if-not-exists
```

2. 给成员函数上 this 签名（Ghidra 认 `__thiscall`）：

```bash
python "$RD" set-signature <bin> FUN_00401230 "void __thiscall attack(Player * this, int dmg)"
```

3. 对游离的 this 用法做局部改型：`retype-variable <bin> <func> param_1 "Player *"`。
4. 全局/堆上对象实例：`set-data-type <bin> 0xADDR Player`；成片数组用 `apply-data-type-range <bin> <start> <end> Player --clear`。

类型化后虚调用直接渲染成 `this->vftable->attack(...)`，再 `decompile` 复验。**坑**：`apply_c_types.py`/`apply_data_type.py` 是 legacy 第 3 层脚本，写的是 `projects/` 老项目（需先 `driver.py export`），daemon 的 `projects-rpc/` 项目**看不到**这些类型——daemon 工作流只用上面的 rpc 命令，只有走 `driver.py exec-w` 后路时才用那两个脚本批量吃 `.h`。

## 4. STL 噪声过滤纪律

- `??$`/`_ZSt` 前缀函数、allocator/dealloc、`vector` 扩容循环（容量 ×2 + 搬迁）= **认出语义即跳过，不逐行逆**；逆 allocator 没有任何业务收益。
- `std::string` SSO 形态（x64）：
  - MSVC：32 字节 `{ union { char buf[16]; char *ptr; }; size_t len; size_t cap; }`，cap<16 → 字符就在 buf 里（反编译里是一坨栈上字节操作，别当加密）。
  - libstdc++：`{ char *ptr; size_t len; union { char buf[16]; size_t cap; }; }`，ptr 指向对象自身 → SSO；ptr 指向堆 → 长字符串，**读 flag 类内容跟 ptr 不跟 buf**。
- 业务层定位永远先走字符串/xref（flag 提示语、格式化串、文件路径），模板展开层只当通路；跨函数搜语义词用 `search-decompiled <bin> <regex>`。

## 5. RTTI 恢复（类名/继承层次）

**MSVC 链**（x64，偏移全从 vftable 起算）：

```bash
python "$RD" read-pointers <bin> <vftable-8> 1      # COL 指针（count 是位置参数）
```

COL（RVA 结构）`+0x10` = TypeDescriptor → 其 `+0x10` 起是名字 `.?AVPlayer@@`（`read-bytes` 读 cstr）；COL `+0x14` = ClassHierarchyDescriptor → BaseClassArray 还原继承树。类名到手立即 `rename-function` + plate comment（铁律 5）并 `conclude` 锁类归属。

**Itanium 链**：vtable 槽 -2 指向 typeinfo 对象，其 vtable 是 `__class_type_info`（单继承无信息）/`__si_class_type_info`（+8 = 基类 typeinfo）/`__vmi_class_type_info`（多继承+偏移表）；typeinfo `+8` 是 `_ZTS6Player` 名，c++filt 即类名。

## 6. MFC 消息映射（Windows GUI 题）

识别：导入 `MFC140u.dll`/`MFC42.dll`、字符串 `AfxWnd`。定位按钮 handler：

1. 资源或代码里拿控件 ID（`python "$SK/pe_info.py" <bin>` 看资源节；`strings <bin>` 找按钮文本）。
2. 类的消息映射表 = `.rdata` 里 `AFX_MSGMAP_ENTRY` 定长数组（每项末尾 `pfn` 是指向 .text 的 handler 指针；由类 vtable 的 `GetMessageMap` 槽挂出）；`ON_COMMAND(ID, handler)` 项的 nID 字段 = 控件 ID。
3. 逐项 `read-pointers` 扫表，nID 命中的项取 pfn → `rename-function <bin> <pfn> OnBtnCheck` → `decompile`。
4. 动态对照：re-dynamic `scripts/win_gui_drive.py`（Windows-only）PostMessage 点按钮 + x64dbg 断 handler 入口确认；GUI crackme 通用断点见 ctf-patterns.md §6。

## 7. 时间盒纪律与退路

- **模板/STL 展开函数禁止逐个深读**（本篇 §4）；vtable/RTTI 重建 ~15 分钟无业务层进展 → 铁律 6 转动态：Frida `Interceptor.attach` 直接 hook vtable 槽目标函数（槽地址 §2 已解析），或 gdb `info vtbl this`（pwndbg 增强）。
- 同一区域第二次 `ledger.py observe` 必须答 `--delta`（铁律 7）；类归属/槽目标这类权威结论 `conclude` 写入即锁定。
- RTTI/vtable 里读出的字符串与指针常量走 `read_views.py` 三视图取数（保留地址与版本）；涉及字节/编码条件核对时可用 `crypto_sanity.py check`（仅验证所声明的局部格式）。

---

借鉴来源：无外部许可源内容复制；vtable 遍历终止语义依据本家族 `engine/ghidra-rpc/ghidra_rpc/server/tools/cpp.py`。
