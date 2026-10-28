# DEX 静态索引与方法身份

需要按完整签名找方法、字节码、字符串/字段使用点，或核对多 DEX 引用时读。普通 APK 分诊和前台查询仍可直接使用现有工具，不要求先建立索引、跑双工具或建立完整地图。

## 工具发现与执行

从本 skill 目录运行（或使用安装后的绝对路径）：

```bash
python3 scripts/dex_index.py doctor
python3 scripts/dex_index.py build --input app.apk --output case-index.sqlite3
# 显式指定已有解释器；不修改全局 Python 或自动安装包
python3 scripts/dex_index.py build --input first.dex --input second.dex \
  --python /your/venv/bin/python --output another-index.sqlite3
```

doctor 只发现路径/软件元数据，不启动 ADB、工具或包 import。版本入口可运行、样本能解析、设备能力可用是不同事实。SDK 默认路径使用当前宿主的工具名；Windows SDK 不自动变成 WSL 原生后端。可用 ANDROID_SDK_ROOT、APKANALYZER、D8、DEXDUMP、JADX、AGPY 指定实际位置。

build 才显式运行 Androguard。当前验收基线为 4.1.4；不强制永久锁定，其他版本需对所用接口与样本重新验收。新脚本复用同一分发包 re-dynamic/scripts 的证据辅助器；原有 APK 脚本入口保留。缺少该后端时可用已有 JADX、SDK 或其他已验证方法继续当前问题。

索引支持裸 DEX 与 ZIP/APK 内所有名字以 .dex 结束的条目，包含非标准 assets 路径。保留重复 ZIP 条目的 ordinal/header offset 与内容哈希，不以同名条目覆盖。不会递归解包嵌套归档或把 opaque payload 自动判为已分析 DEX；coverage 只描述所选条目。

默认每输入 512 MiB、每 DEX 条目 128 MiB，可通过 --max-input-bytes / --max-dex-bytes 调整。这是本次读取预算，不是累计任务/方法数量限制。超出会拒绝该条目并标记 partial；解析失败与“不存在方法”不同。未完成的索引不能作为全范围无引用证明。

## 精确查询与完整原件

```bash
python3 scripts/dex_index.py query --index case-index.sqlite3 --table sources
python3 scripts/dex_index.py query --index case-index.sqlite3 \
  --signature 'Lexample/Check;->verify(Ljava/lang/String;I)Z'
python3 scripts/dex_index.py query --index case-index.sqlite3 --table instructions --method METHOD_ID
python3 scripts/dex_index.py query --index case-index.sqlite3 --table refs \
  --kind call --target 'Lexample/Check;->verify(Ljava/lang/String;I)Z'
python3 scripts/dex_index.py definitions --index case-index.sqlite3 \
  --signature 'Lexample/Check;->verify(Ljava/lang/String;I)Z'
```

方法 ID 绑定容器、具体 DEX 条目、原始类 descriptor、方法名与完整原型。JADX 别名、Java 行号、短方法名不是主键。native/abstract 声明可存在但没有本 DEX 方法体，不能推断 JNI 实现地址。

指令同时记录 offset_bytes、offset_code_units 与验证过的文件偏移；不能把 DEX 偏移加到 native load bias。code_item 的文件坐标只有在解码器完整指令字节与原输入相同时才导出。字符串/字段/类型是实际指令操作数使用点；call 指向编码的声明签名，不证明运行时分派。其他操作数保留为 uninterpreted_operand，不伪造已解析调用。

查询 tables：inputs、sources、methods、instructions、refs。methods 可按 --signature / --source 过滤；instructions/refs 可按 --method；refs 还支持 --kind / --target。过滤均为精确匹配。definitions 分页列出选定输入内的同签名定义，多个候选不擅自选一个。

结果有 snapshot、next，下一页携带 --snapshot 与 --after；--limit 为单页条目数，--max-bytes 为单页输出预算。大字段返回 large_fields_omitted 和精确原件入口：

```bash
python3 scripts/dex_index.py read-document --index case-index.sqlite3 \
  --table methods --row ROW --snapshot INDEX_SHA256 --offset 0 --max-bytes 8192
```

原件是精确 JSON 行的 UTF-8 字节，以 base64 分页；先连接全部字节再解码，直到 next=null。单页不等于全文。索引变化会拒绝旧 snapshot，不把摘要、预览或空列表当完整证据。索引输出不覆盖旧文件，可随时从原始输入重建。

## 按需 Java 视图

```bash
python3 scripts/dex_index.py decompile --input app.apk --class 'Lexample/Check;' \
  --output new-class-export
```

明确调用已配置 JADX，保存输入副本、Java 输出、完整 stdout/stderr 与文件哈希；--jadx 可覆盖路径。--timeout 是该工具一次等待预算，不是解题期限。退出成功不证明语义正确；检查 receipt 和诊断，分支/位宽/异常路径存在疑点时核对相关原始字节码。宿主工具失败不说明 APK 无实现。

需要关联已保存观察与真实 Ghidra 文件映射时，读 `re-dynamic/references/static-correlation.md`。将索引/关联作为 derived 产物通过现有 analysis_session artifact 或记忆证据流程登记；保存原件引用、覆盖范围与未知项，不自动将全索引加入上下文或发布跨任务经验。
