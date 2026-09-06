[中文](SKILL_TEMPLATE.zh-CN.md) | English

# SKILL.md Template

Use this template as the minimum structure required by `docs/AI_SKILL_CONTRACT.md`.

```md
---
name: "<skill-id>"
version: "<package-version, optional but recommended for IronClaw>"
description: "<one-line English description>"
description_zh: "<one-line Chinese description, optional but recommended>"
activation:
  keywords:
    - "<keyword-1>"
  exclude_keywords:
    - "<exclude-keyword-1>"
  tags:
    - "<tag-1>"
  max_context_tokens: 1600
---

# <Display Name>

## When to use
- Describe the primary intent and audience.

## Capabilities
- Capability 1
- Capability 2

## Safe usage rules
- Sensitive data handling.
- Confirmation requirements for write actions.

## Distribution / Activation
- GitHub repo/tree URLs are discovery-only for AI hosts.
- Preferred IronClaw activation command from npm: `bunx -p <package-name> <setup-bin> ironclaw`
- Preferred OpenClaw activation command from npm when managed install is unavailable: `bunx -p <package-name> <setup-bin> openclaw`

## Limits / Non-goals
- What this skill does not do.
- Known constraints and risk boundaries.
```

Minimum checks:
1. Front matter has `name` and `description`.
2. If IronClaw routing is supported, include `version` and `activation.*`.
3. `## Capabilities` section exists and uses bullet items.
4. `## Distribution / Activation` states discovery vs activation.
5. `## Limits / Non-goals` section exists.
