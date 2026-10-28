# 本 skill 工具入口

按当前问题选择工具，用 --help 查参数；工具是否可用以发现/功能探针为准。

| 脚本 | 用途线索 |
|---|---|
| `scripts/_android_tools.py` | _android_tools.py - android-re scripts 共享的 Android SDK 工具探测与调用层. |
| `scripts/apk_oracle.py` | apk_oracle.py - 一键真机 oracle：模拟器内逐候选验证 flag，正负对照成对出报告. |
| `scripts/apk_triage.py` | apk_triage.py - APK 一条命令分诊（签名 / Manifest / 逐 dex 自有类统计 / 可疑 API / flag 全扫）. |
| `scripts/axml_decompile.py` | axml_decompile.py - 二进制 AndroidManifest.xml（AXML）→ 文本 XML. |
| `scripts/dex_disasm.py` | dex_disasm.py - Dalvik 反汇编（包官方 apkanalyzer，内置自检）. |
| `scripts/dex_index.py` | 被动发现、可重建 DEX 方法/使用点索引、精确分页、显式 JADX 类导出；见 dex-static-index.md。 |
| `scripts/dex_triage.py` | dex_triage.py - 多 dex 枚举与扫描（类/方法/字符串 + 包前缀过滤 + 关键词扫描）. |
