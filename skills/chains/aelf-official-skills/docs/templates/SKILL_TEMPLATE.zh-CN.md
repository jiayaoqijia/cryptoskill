中文 | [English](SKILL_TEMPLATE.md)

# SKILL.md 模板

以下模板满足 `docs/AI_SKILL_CONTRACT.zh-CN.md` 的最低结构要求。

```md
---
name: "<skill-id>"
version: "<包版本，可选但推荐用于 IronClaw>"
description: "<英文一句话描述>"
description_zh: "<中文一句话描述，可选但推荐>"
activation:
  keywords:
    - "<keyword-1>"
  exclude_keywords:
    - "<exclude-keyword-1>"
  tags:
    - "<tag-1>"
  max_context_tokens: 1600
---

# <展示名称>

## When to use
- 描述该 skill 适用的核心场景和用户意图。

## Capabilities
- 能力 1
- 能力 2

## Safe usage rules
- 敏感信息处理规则。
- 写操作前的确认要求。

## Distribution / Activation
- GitHub repo/tree URL 仅用于 discovery。
- IronClaw 推荐 npm 激活命令：`bunx -p <package-name> <setup-bin> ironclaw`
- OpenClaw 在没有 managed install 时，推荐 npm 激活命令：`bunx -p <package-name> <setup-bin> openclaw`

## Limits / Non-goals
- 明确该 skill 不做什么。
- 已知限制和风险边界。
```

最低检查项：
1. front matter 包含 `name` 和 `description`。
2. 若支持 IronClaw 路由，补充 `version` 与 `activation.*`。
3. 存在 `## Capabilities` 且为列表。
4. `## Distribution / Activation` 需要明确 discovery 与 activation 的区别。
5. 存在 `## Limits / Non-goals`。
