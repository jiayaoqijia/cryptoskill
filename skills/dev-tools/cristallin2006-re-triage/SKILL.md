---
name: re-triage
description: 识别未知文件、语言、架构、壳与运行条件，给出后续取证选择。用于未知样本和初步风险分诊；不规定整个任务的分析顺序。
---

# re-triage

## 输入与输出

输入为真实样本/目录与用户问题；输出为文件哈希、格式/架构、语言/壳线索、风险与最小后续问题。

## 最短可用流程与判据

先按需使用 file、文件头、节/段和元数据识别，必要时调用 ghidra-core 的 triage。已知文件类型且只问一个局部问题时无需全量导入。壳判断交叉看节名、magic 与结构：高熵、UPX 字符串或干净导入表都不单独证明加壳；verdict=none 也不排除壳。

少量导入可能来自动态加载；未发现 API 不支持全局“无能力”结论。`selfmod_signal` 是线索：确认信号 handler、保存 PC 及控制流影响再解释可达性。CPython/Cython 扩展可结合元数据、常量和栈帧确定角色。

## 交接选择

要回答程序语义 → ghidra-static；运行时行为/实验 → re-dynamic；已确认需解包 → re-unpack；缺陷与可控性 → vuln-audit。pcap → traffic-analysis；APK 的 Manifest/DEX/加载环境 → android-re，其中 native 主体可并行交给静态/动态分析。 .NET 通常用 IL 工具，NativeAOT/IL2CPP 用 native 方法。运行条件选择以执行环境实测为准。准备从局部静态观察推断“没有其他路径/数据无作用”时，按 re-dynamic 的 references/coverage-review.md 评估证据覆盖，选择适用实验或证明。

Unity 的输入校验与场景探索按用户目标及实际入口分流；NES 状态注入与原始通关分别记录。具体条件见对应 reference。输出交接保留已确认事实，避免重复分诊。

## 会话与交接

按当前问题选方法，可静态先行、动态先行或直接建模。连续实验没有新增证据时盘点前提和可区分解释的实验；时间盒用于复查，可说明价值后继续原路线。

简单单点查询记录最小证据即可；多阶段、恢复或协作任务按需使用 analysis-session，记录关键结论、目标代次、实验干预和未决问题。普通工具事件由运行层记录。候选与外部接受分别说明，可交付限定范围的未完成报告。共享项目写操作协调所有权；未获变更权时先只读。


## 按需资料

| 文件 | 何时读 |
|---|---|
| [能力识别证据](references/capability-evidence.md) | 能力规则命中、组合特征、作用域和未命中的解释 |
| `references/triage.md` | 分诊细节：语言识别特征、壳检测、高危 API 组合、平台速查、flag 形态 regex 集（全家权威源） |
| `references/anti-analysis.md` | 命中反调试/反混淆/自校验时的识别与绕过对照表 |
| `references/dotnet-il.md` | 判出 .NET 后：de4dot 脱混淆、dnSpyEx 反编译/IL patch、混淆器对抗决策 |
| `references/unity-runtime-fields.md` | 仅 Unity/Mono：程序集清单、实例字段和原游戏正反例 |
| `references/unity-scene-exploration.md` | 仅 Unity/Mono 场景探索：场景线索、运行时视点、视觉碎片与负面结论边界 |
| `references/nes-state-analysis.md` | 仅 iNES：状态写点、单地址注入、帧步进与画面验证 |
| `references/pyc-bytecode.md` | pyc/PyInstaller 样本：magic→版本判定、反编译器选择矩阵、PyArmor 识别 |
| `references/firmware.md` | 固件镜像：binwalk/熵判型、文件系统提取、ARM/MIPS 基址反推导入 Ghidra |
| `references/ollvm-deobf.md` | OLLVM 混淆的工具级执行：选型决策表、手工 deflat、claripy 化简 |
