# Audit Intelligence Skill (Solodit-powered)

`audit-intelligence` 是一个面向合约安全审计的知识检索型技能：
它通过 Solodit API 读取历史审计问题，并把结果格式化为可执行的安全建议。

> 定位：不是替代完整人工审计，而是给 Agent 提供“证据驱动”的漏洞检索和初筛能力。

## 1) 能力总览

### A. 关键词漏洞检索

- 工具：`solodit_search_findings`
- 作用：按关键词、风险级别、排序模式查询历史审计发现。
- 典型问题：
  - “找最近的 HIGH reentrancy 相关案例”
  - “总结 access-control 常见修复方式”

### B. 项目/地址维度聚合

- 工具：`solodit_project_findings`
- 作用：针对协议名或合约地址聚合历史 finding，生成风险分布和高频漏洞类别。
- 典型问题：
  - “给我看某项目历史审计风险画像”

### C. 代码片段模式匹配 + 证据回查

- 工具：`audit_pattern_matcher`
- 作用：
  1. 对用户输入的 Solidity 片段做轻量规则匹配（如 `tx.origin` / `delegatecall`）；
  2. 调用 Solodit 相似案例接口返回证据链接。
- 典型问题：
  - “这段 withdraw 看起来有风险吗？给我真实案例参考。”

## 2) 架构设计

```text
Agent
  └─ audit-intelligence (SKILL)
      ├─ solodit_search.py
      ├─ solodit_contract_findings.py
      ├─ audit_pattern_matcher.py
      └─ solodit_client.py  (统一 API 层 + 响应标准化)
```

核心设计原则：

1. **统一 API 客户端**：将鉴权、超时、错误处理集中在 `solodit_client.py`。
2. **统一数据 schema**：不同接口的字段在客户端层先标准化。
3. **工具职责单一**：每个脚本只负责一种查询路径，便于 Agent 编排。
4. **输出可审计**：结果中尽量保留 source URL 作为证据。

## 3) 快速开始

### 环境变量

```bash
export SOLODIT_API_KEY="your-api-key"
export SOLODIT_API_BASE="https://api.solodit.xyz/v1"   # 可选
export SOLODIT_TIMEOUT_SECONDS="20"                     # 可选
```

### 在 Agent 中使用

```python
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(
    name="audit_agent",
    skill_paths=["./web3-data-intelligence"],
    scripts_enabled=True,
)

await agent.activate_skill("audit-intelligence")

response = await agent.run(
    "Search HIGH severity reentrancy findings and summarize top mitigations."
)
print(response)
```

## 4) Demo: Effect Demonstration

### Agent Configuration

```python
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(
    name="demo_audit_agent",
    skill_paths=["./web3-data-intelligence"],
    scripts_enabled=True
)
await agent.activate_skill("audit-intelligence")
```

### Input Prompt

```text
请检索 reentrancy 的 HIGH/MEDIUM 历史审计案例，并给出常见修复建议。
```

### Intermediate Outputs

```text
Step 1: Agent activates skill "audit-intelligence"
  → Tools loaded: [solodit_search_findings, solodit_project_findings, audit_pattern_matcher]

Step 2: Agent calls solodit_search_findings
  → Input: {"query": "reentrancy", "severities": ["HIGH", "MEDIUM"], "limit": 8}
  → Output: SOLODIT SEARCH REPORT ... (findings + evidence URLs)

Step 3: Agent calls audit_pattern_matcher
  → Input: {"code_or_summary": "external call before state update ...", "evidence_limit": 3}
  → Output: pattern hits + related evidence
```

### Final Output

```text
- 风险级别分布
- 高频漏洞模式
- 每个模式对应的修复策略
- 证据链接（Solodit）
```

## 5) 脚本说明

- `scripts/solodit_client.py`
  - 统一封装 Solodit API 请求
  - 提供：`search_findings` / `get_project_findings` / `similar_findings`
  - 提供 `_normalize_finding`，将返回数据映射成统一字段

- `scripts/solodit_search.py`
  - 面向关键词检索
  - 输出结构化报告，便于 Agent 二次总结

- `scripts/solodit_contract_findings.py`
  - 面向项目/地址聚合
  - 输出 severity/category 统计信息，便于风险画像

- `scripts/audit_pattern_matcher.py`
  - 先做轻量规则匹配
  - 再查询相似案例，强化“解释 + 证据”

## 6) 安全与工程注意事项

1. 不要在代码中硬编码 API Key。
2. 对外输出错误信息时避免泄露内部栈。
3. 将规则匹配视为“早期预警”，高风险结果必须人工复核。
4. 如果 Solodit API 字段有变更，只需修改 `solodit_client.py` 的标准化逻辑。

## 7) 后续迭代建议

1. 增加漏洞分类 taxonomy 与 CWE/SWC 映射。
2. 增加批量合约扫描接口（分批限流）。
3. 增加“证据去重 + 排名”策略。
4. 接入静态分析器结果（Slither）作为补充信号。