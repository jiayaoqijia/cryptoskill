中文 | [English](EXAMPLE_NEW_SKILL_DIFF.md)

# 黄金路径示例：新增 Skill 的完整 Diff

该示例展示新增一个 skill 的最小完整变更集。

## 1) `workspace.json`

```diff
 {
   "projects": [
+    {
+      "path": "${SKILLS_BASE}/AElf/example-skill",
+      "dependsOn": ["aelf-node-skill"]
+    }
   ]
 }
```

## 2) `skills-catalog.json` 产物片段

```json
{
  "id": "example-skill",
  "displayName": "Example Skill",
  "dependsOn": ["aelf-node-skill"],
  "npm": { "name": "@example/skill", "version": "0.1.0" }
}
```

## 3) 门禁命令输出（节选）

```text
$ bun run catalog:generate
[DONE] Generated catalog: .../skills-catalog.json
[INFO] Schema: 1.3.0

$ bun run health:check
[Health Check] Summary: total=8, pass=8, warn=0, fail=0

$ bun run security:audit
[OK] Security audit passed for 8 skill(s).

$ ./bootstrap.sh --only example-skill --skip-install
[INFO] Skills selected (with dependencies): 2
```

## 4) PR 必备结构

1. Goal / Non-goal
2. Files to change
3. Contract mapping
4. Validation commands
5. Risk & rollback
6. Acceptance evidence

PR 描述示例片段：

```md
## Goal / Non-goal
- Goal: 接入 `example-skill`，并声明依赖 `aelf-node-skill`。
- Non-goal: 不修改上游 skill 仓业务逻辑。

## Validation commands
- `bun run catalog:generate`
- `bun run health:check`
- `bun run readme:check`
- `bun run security:audit`
- `./bootstrap.sh --only example-skill --skip-install`
```
