[中文](EXAMPLE_NEW_SKILL_DIFF.zh-CN.md) | English

# Golden Path Example: New Skill Integration Diff

This example shows the minimum complete change set for adding one skill.

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

## 2) Generated `skills-catalog.json` entry

```json
{
  "id": "example-skill",
  "displayName": "Example Skill",
  "dependsOn": ["aelf-node-skill"],
  "npm": { "name": "@example/skill", "version": "0.1.0" }
}
```

## 3) Gate outputs (trimmed)

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

## 4) PR payload

1. Goal / Non-goal
2. Files to change
3. Contract mapping
4. Validation commands
5. Risk & rollback
6. Acceptance evidence

Example PR body snippet:

```md
## Goal / Non-goal
- Goal: onboard `example-skill` with dependency on `aelf-node-skill`.
- Non-goal: no business logic changes in upstream skill repositories.

## Validation commands
- `bun run catalog:generate`
- `bun run health:check`
- `bun run readme:check`
- `bun run security:audit`
- `./bootstrap.sh --only example-skill --skip-install`
```
