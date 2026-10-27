# Linux v0.2 参数契约

所有记忆/协作工具：顶层 action、task、options。task 必须是本会话绑定并拥有的现有 analysis_session 任务。不能通过 options 传 actor/project/SQL/命令。

## 基本示例

登记任务级静态资料：

~~~json
{"action":"source","task":"TASK","options":{"path":"evidence.txt","target_id":null,"expected_generation":0}}
~~~

读取返回的 SOURCE_ID 后提出候选：

~~~json
{
  "action":"propose",
  "task":"TASK",
  "options":{"candidate":{
    "schema_version":"0.2",
    "operation_id":"unique-per-attempt",
    "target_id":null,
    "expected_generation":0,
    "kind":"claim",
    "title":"当前命题",
    "body":"结论、条件及限制",
    "origin":"inferred",
    "verification":"untested",
    "evidence_refs":[{"source_id":"SOURCE_ID","locator":"lines 1-3"}],
    "accept_scope":null,
    "unresolved":["尚未动态验证"],
    "details":{
      "proposition":"可验证的具体命题",
      "conditions":{"description":"当前资料与条件","environment_ref":null,"analysis_revision_ref":null}
    }
  }}
}
~~~

evidence_refs 的 locator 描述真实位置；可额外给 content_sha256 核对内容。宿主只能检查来源存在、哈希和权限，不能证明自然语言解释正确。

候选校验失败会指出具体字段路径与原因，例如 `$.details.conditions: missing required field`。按当前 schema 补全真实资料或显式允许的 null 后重试；不要猜填证据、自动重开已结束任务或绕过权限。错误不会持久化候选，也不回显字段值；schema 仍为 0.2。

review_publish：options 为 id、expected_revision、decision=publish|reject、reason；publish 前用 read_source 回查全部支持来源。返回 revision 增加，引用/后续修改使用新值。revise 输入 candidate、id、expected_revision，candidate 使用新的 operation_id。

## 各类 details

公共 conditions：description、environment_ref、analysis_revision_ref。引用字段可为 null，不能虚构已登记对象。

| kind | details 必需字段 |
|---|---|
| observation | conditions、observation_level=source_output 或 target_measurement |
| claim | proposition、conditions |
| hypothesis | status=proposed/testing/supported/refuted/deferred、proposition、test_plan、discriminating_outcomes 字符串数组；可选 work_refs |
| experiment | execution_status、outcome、conditions、input_refs、tools、interventions、observations、tested_propositions、excludes、does_not_exclude |
| constraint | conditions、constraint_type=environment/task_requirement/resource/data_handling |
| method_candidate | preconditions、failure_boundaries、case_refs、redaction_status=not_reviewed/reviewed |

experiment.execution_status：completed/failed/blocked/interrupted/unknown。outcome：supports/contradicts/inconclusive/no_effect。input_refs 与 evidence_refs 形状相同，其余复数字段为字符串数组。hypothesis supported/refuted 需要证据，但字段合法不证明判断成立。

公共可选字段：dependency_refs=[{record_id,revision}]、observed_at、valid_from、valid_to、recheck_after；时间为带时区的 ISO 时间或 null。recheck_after 到期表示需复核，不证明事实为假。dependency 只能指向同任务当前有效记录；变更后派生结论需复核。

## 关系与检索

link：left、right、left_revision、right_revision、kind、reason。kind 为 supports/contradicts/derived_from/depends_on/tests/supersedes；left supersedes right。v0.2 限同目标/代次，避免跨目标误复用。

invalidate：id、expected_revision、reason、state=revoked|superseded|needs_recheck。archive 等同 superseded。

query：query、limit=1..50、offset、include_history、target_id（可选）。默认隐藏失效/撤销条目，disputed 成组提示。扫描上限 500，返回 scan_truncated；不能把部分扫描当完整覆盖。

context：query、target_id、budget_bytes=512..16384（默认 8192）；仅打包已复核成果。冲突组不拆开成单侧结论；放不下保留引用提示。导出和查询不授予任意文件写入。

## 协作

analysis_collaboration：

- add：question、sources=[SOURCE_ID]、depends_on=[WORK_ID]。
- dispatch：work=[WORK_ID]，最多两个；等待有限批次完成。
- result：work=WORK_ID；status 不需 options。
- review：work、decision=adopted|rejected|needs_more_evidence、reason。
- retire：work、reason；recover 不需 options。

子 agent 使用 dsh_evidence 的 work 与 source_id，返回 JSON 对象 conclusion、evidence（source ID 数组）、unresolved（字符串数组）。子结果始终 inferred/untested，无法借返回字段升级验证。主代理通过 propose 将有价值的结果整理成候选，不直接把全部流水存入记忆。

open 无 options 或 resume_token；handoff 生成新交接 token。token 不属于分析资料，避免放入候选、工具 source 文件或交付报告。
