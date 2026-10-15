# 运行接口

实现 runtime/analysis-v1，版本由 session.py --version 返回。SQLite 事务统一串行状态写入；WAL/同步提交用于并发与崩溃恢复。旧 JSONL 台账保留追加，CLI 全操作加 flock，渲染为派生视图。数据库放 Linux 文件系统，不放 /mnt/c；不要手动修改运行中的数据库。

`discover --tools TOOL...` 轻量发现 PATH 和候选解释器，不改代理/包。`discover --python PATH --module NAME` 只对指定解释器做一次 import 冒烟；结果及失效条件需要在任务中引用。是否可运行某个目标仍需具体功能测试。

实测 host 重载可停止关联后台进程；维护前记录准确的进程身份、项目/加载程序和启动环境。恢复已有 Ghidra 项目使用匹配原样本的 load --no-analyze，确认命名和 hash 均匹配以避免重新导入。运行资源的活跃 PID 失效后标 inactive，结果待核对；不把消失的进程算作任务完成。

任务状态与方法自由分开。resources 登记不自动停止进程。leases 是受控入口的协作契约，guard 阻止错误/过期 token 和失效目标代次；无法约束绕过入口的任意 shell 变更。运行库不替代容器平台权限或 Ghidra 原生事务。

使用 `events TASK_ID` 查询元数据。hooks 桥接只有文本 tool_response，未能可靠取得的退出码保留 null。完整工具输出继续留在原生 DSH 会话存储；元数据哈希用于关联，不作为证明。已加载 skill 的版本可在交接中手工记录，hooks 能识别的只记录请求文件 hash，不声称父子代理共享上下文。

备份/回滚以 migration 报告中的绝对目录为准。旧台账和 Ghidra 项目不会自动转成新任务，按需在恢复时显式关联。


## 原生沙箱下的状态能力

用户 profile 的 hooks-claude-code 行由本地 analysis-hooks-sandbox 薄适配器加载官方桥接。只把固定的 analysis_hook.py 命令显式限定为 workspace-write @ /root/.dsh/analysis-state。原生 analysis_session 也使用同一受限 ctx.shell 路径，只接受列明的纯状态操作。未修改官方包、默认 sandbox-policy、会话权限或审批策略。

全局 sandbox-policy.workspaceRoot 是无会话调用的部署回退值；普通工具仍可按 session.cwd 解析自身策略。修复不把这个回退根改为任意会话根，也不赋予所有 shell 对 DSH_HOME 的写权限。

health/host-PID.json 是宿主写入的钩子健康记录，包含生命周期点、错误计数与实际沙箱事实，不复制 prompt/参数/响应正文。SQLite 失败时，hook 仍输出独立上下文并返回 1；适配器补交官方桥接在非零退出时忽略的上下文，不伪造 0 退出码。

不把失败后的事件补造为成功，也不自动改用 /tmp 或 Windows 盘上的另一个数据库。新版本开始成功记录的事件与历史缺失段分别说明。
