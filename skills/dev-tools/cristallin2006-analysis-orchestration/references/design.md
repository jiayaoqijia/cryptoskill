# 持续型解题编排 0.4.0

0.4.0 增加持久化的空闲处置、状态签名与完成检查；0.3.1 的取消监听清理和数据库关闭顺序修复继续保留。完成检查与证据边界见 [resolution.md](resolution.md)。以下持续型生命周期设计沿用 0.3.0。

复用 DSH 原生 startContinuable / sendMessage / drainContinuableChildren，模型路由、沙箱、工具过滤及会话持久化由原生维护。空闲执行实例可能释放，后续从同一子会话恢复；不是后台无限推理或永久常驻进程。

task_ms / timeout_ms / max_steps / max_wakeups 默认 null，不按时长、累计步骤或提醒次数自动停止。明确提供有限预算时才执行。移除插件 maxTokens=4096：首次创建沿用父模型设置；原生冷恢复按描述恢复模型与推理路由，生成预算采用原生路由默认，不保证继承父代理后来改过的每项参数。

默认任务并发 2，宿主最多 3；每代次最多 64 项；状态库结果保留前 32768 字符并标记截断，原文在原生子会话。交接、状态摘要和近期指导有界；报告超过 200 次不会因此失去反馈能力。指导窗口优先移出已回执项，未处理项过多要求核对投递。

返回为 returned，须复核。followup/steer 可恢复同一 child，新的 result_revision 撤销旧采纳；已有依赖使用该工作时拒绝原地续做。空闲释放执行槽位。取消、暂停、父会话退出、插件卸载和结束均确认原生收尾，不能根据元数据假定外部进程已退出。

原生血缘与状态库双重绑定子代理。技能不会自动赋予工具、递归派发或权限。结束/暂停/宿主重载后，即使原生子会话仍可寻址，未由当前编排授权的冷恢复也在步骤与工具入口拒绝。recover 不自动重放。

网络覆盖维持现状：严格 HTTP 控制尚不支持执行型 Solver，因此拒绝启用；普通 shell/MCP 没有因此获得逐发送计量或全局出口隔离。此版本不是 VPN 事件流量控制修复。单次工具超时、用户取消和资源租约继续适用。

## 架构来源

下列为先前版本延续的独立架构借鉴，未复制代码或提示词；本次持续会话直接使用本机 DSH 原生 API：

- [BreachWeave](https://github.com/m-sec-org/BreachWeave/tree/bc2d9502a2625c5ef354adc30243bd091341cc51)：Planner / Solver / Observer 职责分离及保守纠偏。
- [所检查 ARTEX 版本](https://github.com/jiwoochris/artex-global/blob/fdfb7a17b7da5e2de716c0e98475ec77a41c64c6/server/engine.go)：事件唤醒、心跳与工作生命周期。
- [Microsoft Magentic](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/magentic)：独立协调与进度复查，未声称实现其完整算法。

合成验收验证机制，不证明真实解题收益或多代理相对单代理的优势。
