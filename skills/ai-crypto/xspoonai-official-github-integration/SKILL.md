---
name: github-integration
description: GitHub 集成 Skill，支持创建/查询 Issue、PR，获取仓库信息。用于 Agent 与 GitHub 协作。
version: 1.0.0
author: varown
tags:
  - github
  - api-integration
  - issue
  - pull-request
  - repository
triggers:
  - type: keyword
    keywords:
      - github
      - issue
      - pr
      - pull request
      - repository
      - 创建issue
      - 查询pr
    priority: 85
parameters:
  - name: action
    type: string
    required: false
    description: 操作类型 (create_issue, list_issues, get_issue, list_prs, get_pr, repo_info)
  - name: repo
    type: string
    required: false
    description: 仓库名，格式 owner/repo
  - name: title
    type: string
    required: false
    description: Issue/PR 标题
  - name: body
    type: string
    required: false
    description: Issue/PR 正文
prerequisites:
  env_vars:
    - GITHUB_TOKEN
scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: github_issue
      description: 创建、列出或查询 GitHub Issue
      type: python
      file: github_issue.py
      timeout: 30
    - name: github_pr
      description: 列出或查询 GitHub Pull Request
      type: python
      file: github_pr.py
      timeout: 30
---

# GitHub Integration Skill

你正在使用 **GitHub 集成模式**。你是一个 GitHub 协作专家，能够帮助用户管理 Issue、PR 和仓库信息。

## 支持的操作

| 操作 | 描述 | 脚本 |
|------|------|------|
| create_issue | 创建新 Issue | github_issue |
| list_issues | 列出仓库 Issue | github_issue |
| get_issue | 获取单个 Issue 详情 | github_issue |
| list_prs | 列出仓库 PR | github_pr |
| get_pr | 获取单个 PR 详情 | github_pr |

## 环境变量

| 变量 | 必填 | 描述 |
|------|------|------|
| GITHUB_TOKEN | 是 | GitHub Personal Access Token，需 repo 权限 |

## 使用示例

### 创建 Issue

```json
{
  "action": "create_issue",
  "repo": "owner/repo",
  "title": "Bug: 登录失败",
  "body": "描述问题..."
}
```

### 列出 Issues

```json
{
  "action": "list_issues",
  "repo": "owner/repo",
  "state": "open",
  "limit": 10
}
```

### 获取 PR 详情

```json
{
  "action": "get_pr",
  "repo": "owner/repo",
  "pr_number": 42
}
```

## 最佳实践

1. **Token 安全**：永远不要硬编码 GITHUB_TOKEN，使用环境变量
2. **权限最小化**：Token 只需 `repo` 权限即可
3. **速率限制**：GitHub API 有速率限制，大批量操作注意节流
4. **仓库格式**：repo 参数使用 `owner/repo` 格式，如 `XSpoonAi/spoon-awesome-skill`
