# GitHub Integration Skill

让 AI Agent 与 GitHub 协作的集成 Skill，支持 Issue 和 Pull Request 的创建、查询操作。

## 功能概览

| 功能 | 脚本 | 描述 |
|------|------|------|
| 创建 Issue | `github_issue.py` | 在指定仓库创建新 Issue |
| 列出 Issues | `github_issue.py` | 按状态筛选列出 Issue |
| 获取 Issue | `github_issue.py` | 获取单个 Issue 详情 |
| 列出 PRs | `github_pr.py` | 按状态筛选列出 Pull Request |
| 获取 PR | `github_pr.py` | 获取单个 PR 详情（含 diff 链接） |

## 环境配置

### 1. 创建 GitHub Token

1. 访问 [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. 选择 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制 Token

### 2. 配置环境变量

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

或创建 `.env` 文件：

```
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

## API 文档

### github_issue

**输入 (JSON via stdin):**

```json
{
  "action": "create_issue",
  "repo": "owner/repo",
  "title": "Issue 标题",
  "body": "Issue 正文（可选）"
}
```

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| action | string | 是 | create_issue / list_issues / get_issue |
| repo | string | 是 | 仓库名，格式 owner/repo |
| title | string | create 时必填 | Issue 标题 |
| body | string | 否 | Issue 正文 |
| state | string | 否 | list 时：open/closed/all，默认 open |
| limit | int | 否 | list 时返回数量，默认 10 |
| issue_number | int | get 时必填 | Issue 编号 |

**输出:** JSON 格式，成功时含 `success: true` 及相应数据

### github_pr

**输入 (JSON via stdin):**

```json
{
  "action": "list_prs",
  "repo": "owner/repo",
  "state": "open",
  "limit": 10
}
```

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| action | string | 是 | list_prs / get_pr |
| repo | string | 是 | 仓库名 |
| state | string | 否 | open/closed/all |
| limit | int | 否 | list 时返回数量 |
| pr_number | int | get 时必填 | PR 编号 |

## 错误处理

常见错误及处理：

| 错误 | 原因 | 解决 |
|------|------|------|
| 401 Unauthorized | Token 无效或过期 | 检查 GITHUB_TOKEN |
| 403 Forbidden | 权限不足 | Token 需 repo 权限 |
| 404 Not Found | 仓库不存在或无权限 | 检查 repo 拼写和权限 |
| 422 Validation Failed | 参数错误 | 检查 title、body 等必填项 |

## 示例

### 命令行测试

```bash
# 创建 Issue
echo '{"action":"create_issue","repo":"varown/spoon-awesome-skill","title":"Test","body":"From skill"}' | python scripts/github_issue.py

# 列出 Issues
echo '{"action":"list_issues","repo":"XSpoonAi/spoon-awesome-skill","state":"open","limit":5}' | python scripts/github_issue.py

# 获取 PR
echo '{"action":"get_pr","repo":"XSpoonAi/spoon-awesome-skill","pr_number":1}' | python scripts/github_pr.py
```

### 与 SpoonReactSkill 集成

```python
from spoon_ai.agents import SpoonReactSkill
from spoon_ai.chat import ChatBot

agent = SpoonReactSkill(
    name="github_agent",
    skill_paths=["ai-productivity/api-integration/github-integration"],
    scripts_enabled=True
)
await agent.activate_skill("github-integration")
result = await agent.run("在 varown/spoon-awesome-skill 创建一个标题为 Test 的 Issue")
```

## 安全说明

- **切勿**将 GITHUB_TOKEN 提交到代码仓库
- 使用 `.gitignore` 排除 `.env` 文件
- 生产环境建议使用短期 Token 或 OAuth
