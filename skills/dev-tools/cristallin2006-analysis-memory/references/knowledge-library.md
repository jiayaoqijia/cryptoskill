# 可选知识召回与项目方法记忆（v1）

需要找深入资料、复用同项目方法或复盘知识缺口时，可用主会话工具 `dsh_knowledge`。先绑定任务并 `dsh_memory_write open`，task 始终在顶层；`schema` 不要求任务。无需每题查库，不命中也可继续自主探索。没有新增执行、收尾或派发门槛。

## 找资料

`search options={query:"位宽 符号扩展",kind:"all"}`；kind 可为 all/reference/method。query 省略可浏览。使用英文标识符、中文现象或同义表达；目录维护中英文别名。词法分数仅用于排序，返回匹配字段，反例中的词也可能匹配，不代表方法适用或命题成立。目录是维护的导航，不是自动理解全部正文的语义引擎。首批 12 个专题覆盖 Web、静态逆向、密码、Pwn 和负结果复用，未收录的 skill/reference 仍可照常发现和调用。

结果含 total、snapshot、next_offset。用 offset、snapshot 续页；limit=1..50，max_bytes=2048..12000 默认 8192。只限制单页，库内累计方法数量无固定上限；不会只查最近 N 条。无命中不证明没知识或没做过实验。

参考卡只在当前原生 skill 注册表允许模型调用时出现。`read_reference options={id:"reverse-width",offset:0}` 从该 skill 当前本地 provider 读取目录中的完整参考文件，不接受路径或 URL。返回 text、sha256、snapshot、next_offset；offset 为 Unicode 码点。继续携带 snapshot，必要时用 expected_hash 固定全文。原文件变更后需重新开始，不能混拼。每份参考文件目前支持至 1 MiB；更大的原始材料继续使用既有授权文件工具，不能通过静默裁剪迁就本接口。

返回条件和反例用于判断相关性；详细方法仍以原文为准。选择必要方法时，将来源 skill 和适用 reference 放入已有 `skill_plan`，宿主维持完整交付；摘要、目录命中和已读回执都不证明正确应用。不得把目录变成每项必查清单。

## 提炼方法

任务内先用现有 propose/review_publish 形成已复核的 `method_candidate`。只保存值得复用的解释和失败边界，不要求每次操作形成记录。

`draft_method options={record_id,record_revision,card,redaction_note}`，card 必填：

```json
{
  "title":"核对文本解码差异的字节条件",
  "signals":["显示相同但字节结果不同"],
  "aliases":["encoding newline byte mismatch"],
  "preconditions":["能够读取准确原始字节"],
  "procedure":["比较原始长度、编码和末尾字节；按差异选择进一步实验"],
  "verification":["使用不自动去空白的工具重放并核对完整输出"],
  "failure_boundaries":["缺少原始输入时不能断言差异来源"],
  "counterexamples":["文本显示可能折叠不同换行"],
  "uncertainties":["具体输入差异仍需在当前任务验证"],
  "tags":["encoding","evidence"]
}
```

title、signals、preconditions、procedure、verification、failure_boundaries 需有内容；其余数组允许为空。不强迫编造反例或确定性。单卡至 48 KiB，超限明确拒绝，不截断。大原件留在原授权范围。源候选、卡和脱敏说明相同的重试返回原 ID。

提炼时移除原任务路径、地址、真实用户名、凭据、实例状态、访问 token 和授权说明；不要直接复制源 body 或工具流水。源 provenance 和审核备注在本机库内保留，用于撤回和复核，不随共享卡导出；工具投影也不附带源 task/record/source ID、工作区路径或原证据。内置敏感模式只是辅助，不是完备 DLP，显式脱敏审核仍需回查真实内容。

## 发布与复用

`review_method options={id,expected_revision:1,decision:"publish",reason:"已核对来源、前提、失败边界并移除实例信息"}`。发布前源候选必须仍为同修订、reviewed/current、details.redaction_status=reviewed；原始证据读取和有效性重新核对。草稿只对原任务可见，发布后同一 canonical 工作区的后续已打开记忆的 owner 可检索。目录/方法不是命令，不携带原任务访问权限或当前实例事实。

同工作区是显式的共享边界；不要把互不信任或隔离项目放在同一目录。工具没有任意项目/工作区切换参数，不是全局跨项目记忆。源候选或证据变更后方法标记 needs_recheck，默认搜索省略；`include_history:true` 可查看同项目失效/退役方法和本任务草稿，不能查看其他任务未发布草稿。过往正确不表示当前适用，发布不升级 tested/accepted。

`read_method options={id,expected_revision:2}` 逐页返回完整卡、前提、验证方式、反例、不确定性和当前状态。后续页携带 snapshot；完整 JSON 由 text 拼接解析。不要只传标题或把 procedure 摘成无条件打法。Solver 如需参考，可由主代理交接脱敏卡与其条件，专业原文仍按 skill_plan/skill 读取；不授全局方法工具，不广播库或真实案例。独立盲审分支不得注入第一位 Solver 的解释或方法结论。

reject 只处理原任务草稿；retire 可由同项目当前 owner 显式撤回已发布方法并说明原因。状态变更使用当前 expected_revision，保留旧修订。修改正文需提炼新的当前候选和新卡，旧卡按需 retire；不后台覆盖，不自动写回专业 skill。来源失效不自动撤销已经执行的外部操作，也不会自动唤醒 Solver。

## 知识缺口的判断

复盘里的 card JSON 只是素材，不能省略已复核 method_candidate、record_id/record_revision、redaction_note 和当前 expected_revision 后直接发布。可将“分层分帧/状态消费”与“调用实参/实例证据”拆开，不把某题的偏移、密钥表、固定堆路线或两次相同 flag 变成通用步骤；不因整理复盘自动创建或发布方法。

没有现成方法、导航没找到、条件不符、错误应用、原环境已变是不同问题。一次失败先按证据区分，再决定补别名、补参考卡、补反例或保留未决；不自动生成通用规则，不强制做固定次数的查询或实验。此次不引入向量服务、后台整理 agent 或第二套缺口台账。

隔离测试只验证检索、版本、持久化、分页和权限，不证明模型理解、解题收益或新跑分。关闭/故障时继续使用原 skill、证据和任务工具。
