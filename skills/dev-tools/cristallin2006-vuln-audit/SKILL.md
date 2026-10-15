---
name: vuln-audit
description: 识别二进制缺陷、输入可控性、触发条件与影响范围，适用于漏洞预筛和根因分析。程序语义问题交 ghidra-static，可靠利用构造交 pwn-exploit。
---

# vuln-audit

## 输入与输出

输入是目标样本/源码片段、范围和已知入口；输出是缺陷位置、可控输入、路径条件、影响、证据与待验证项。

从输入源到危险操作追数据流，按实际线索查 references/vuln-patterns.md：内存边界、格式化字符串、释放后使用、整数运算、命令构造、随机数和密钥。危险 API 命中是候选；xrefs 不完整不证明不可达。区分崩溃、越界、可控性与稳定利用能力。

有新旧版本时按 references/patch-diff.md 找候选根因，并用具体输入对照行为。优先最小复现实验；环境或授权不足时明确未验证范围。审计交付缺陷及触发条件，不强制构造完整 exploit。执行 Ghidra 操作时加载 ghidra-core，动态实验加载 re-dynamic。

## 会话与交接

按当前问题选方法，可静态先行、动态先行或直接建模。连续实验没有新增证据时盘点前提和可区分解释的实验；时间盒用于复查，可说明价值后继续原路线。

简单单点查询记录最小证据即可；多阶段、恢复或协作任务按需使用 analysis-session，记录关键结论、目标代次、实验干预和未决问题。普通工具事件由运行层记录。候选与外部接受分别说明，可交付限定范围的未完成报告。共享项目写操作协调所有权；未获变更权时先只读。


## 按需资料

| 文件 | 何时读 |
|---|---|
| [Fuzzing 与复现](references/fuzzing-harness-evidence.md) | 需要扩大输入探索时：harness、有效覆盖、崩溃归因与缩减 |
| `references/vuln-patterns.md` | 漏洞模式检查项清单（识别信号/命令/判定标准/误报）——审计主文档 |
| `references/patch-diff.md` | 有补丁前后两版二进制时：ghidriff/version-track 差分 → 根因反推 → PoC 思路（N-day） |
