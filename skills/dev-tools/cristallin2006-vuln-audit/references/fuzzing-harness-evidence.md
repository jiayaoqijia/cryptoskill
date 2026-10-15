# Fuzzing：入口、有效覆盖与可复现缺陷

适用于需要扩大输入探索的本地目标或授权测试副本。优先选能保持真实解析语义的最小入口；简单的一个触发输入无需先建完整 fuzzing 系统。

## 选择后端和入口

| 已有条件 | 选择要点 |
|---|---|
| 有源码、可重编译 | 按工具和编译器条件选择插桩；保留编译参数、sanitizer、库与产物 hash |
| 只有二进制 | 根据架构、系统调用和依赖选择 QEMU/Frida/Unicorn 等后端；支持情况以实际版本为准 |
| 文件/标准输入解析器 | 确认测试字节真正到达解析器；避免只覆盖参数检查或文件不存在分支 |
| 有状态协议、GUI、设备依赖 | 可提取核心解析入口或构造状态回放；记录被替代的运输与环境，保留与真实目标对照 |

## 先证明 harness 在测目标问题

- 准备至少一个已知可进入目标逻辑的输入和一个可解释的不同路径输入。观察覆盖或明确到达点，不单看进程启动和 exec/s。
- 确认 persistent 循环重置了目标所依赖的状态。相同输入在不同先前输入后行为改变时，先处理状态污染；有意测试状态序列时完整保留该序列。
- 保存覆盖口径与后端。插桩失效、依赖库未覆盖、初始化重复失败都会使“跑了很久”失去意义。
- crash/timeout 先当候选。固定原始输入、环境与日志；确认是目标问题，而非错误 ABI、桩、forkserver、OOM 或 harness 自己的断言。

## 发现后的交付

输入缩减时持续检查同一故障签名/根因，不能只维持任意非零退出。保留原始样本和缩减样本；在相应原程序/构建上重放，并分别说明 sanitizer 报告、真实越界、可控性和可利用性。

有稳定复现后再考虑利用原语；vuln-audit 不要求自动构造 exploit。有限时间无发现只能表述已测的输入域、覆盖与环境，不能宣布目标无漏洞。

资源上限、jobs 的归属和运行结果沿用 DSH 现有运行层。本卡不设置跨任务固定并发、不擅自停旧进程，也不把本地 corpus 方法直接套用到远程服务；远程请求仍受任务授权与预算限制。

来源核验 2026-10-14：[AFL++ 流程](https://github.com/AFLplusplus/AFLplusplus/blob/dbaf11913c1b2702dee5b4d3dcfffd52f1defe50/docs/fuzzing_in_depth.md)、[二进制目标](https://github.com/AFLplusplus/AFLplusplus/blob/dbaf11913c1b2702dee5b4d3dcfffd52f1defe50/docs/fuzzing_binary-only_targets.md)、[实践与状态问题](https://github.com/AFLplusplus/AFLplusplus/blob/dbaf11913c1b2702dee5b4d3dcfffd52f1defe50/docs/best_practices.md)。以上为自主归纳及适配，未复制 AFL++ 可执行代码或安装后端。实际运行仍需验证版本、插桩和 harness。
