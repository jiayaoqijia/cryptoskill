---
name: android-re
description: 分析 APK/DEX、Manifest、Java/smali、Android 加载环境和运行交互。APK 内原生 .so 主体由二进制分析协助，Android 侧继续负责 JNI 和设备条件。
---

# android-re

## 输入与输出

输入为 APK/目录、设备与用户问题；输出为包/签名/组件、DEX/JNI 定位、静态或运行证据、产物与限制。

检查 Manifest、多 DEX 和 native 库，按自有类/入口定位而非只看最大 classes.dex。jadx、apkanalyzer、androguard 等按需发现，反编译失败可对照 smali/字节码。条件跳转与结构体偏移影响结论时核对指令；自写 parser 用已知 fixture 或成熟实现检验。

运行时确认 adb 设备、ABI、权限、应用状态和输入回读；Frida host/server 兼容性需实测。Windows SDK/模拟器属于独立后端，WSL 不默认可用。截图、Toast 或回显说明对应输入和状态，正负对照可检验接受判据，未知正例不伪造。

原生 .so 按设备 ABI、JNI_OnLoad/RegisterNatives 与加载条件交 static/dynamic，Android 侧不退出整个任务。改写/重签输出副本，记录签名与原包差异，不用修改后的接受证明原包行为。设备/图形工具不足时可以交付静态部分。

## 会话与交接

按当前问题选方法，可静态先行、动态先行或直接建模。连续实验没有新增证据时盘点前提和可区分解释的实验；时间盒用于复查，可说明价值后继续原路线。

简单单点查询记录最小证据即可；多阶段、恢复或协作任务按需使用 analysis-session，记录关键结论、目标代次、实验干预和未决问题。普通工具事件由运行层记录。候选与外部接受分别说明，可交付限定范围的未完成报告。共享项目写操作协调所有权；未获变更权时先只读。


## 按需资料

| 文件 | 何时读 |
|---|---|
| `references/apk-triage.md` | zip 结构与关键条目、AXML/Manifest 要点、签名版本判定、多 dex 自有类统计法、flag 形态 regex 集 |
| `references/dalvik-notes.md` | smali 速查：常见 opcode 形态、const-string/invoke 模式、equals 比较点、R 类与命名误导识别 |

## 补充专题入口

- [tools](references/tools.md)：当前问题涉及文件名对应专题时按需读取。
