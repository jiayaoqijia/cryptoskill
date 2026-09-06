[中文](CATALOG_SCHEMA.zh-CN.md) | English

# Catalog Schema Semantics (v1.3.0)

This document defines field semantics of `skills-catalog.json` for both AI and humans.

## 1. Top-level structure

```json
{
  "schemaVersion": "1.3.0",
  "generatedAt": "ISO-8601",
  "source": "workspace.json",
  "skills": [],
  "warnings": []
}
```

Field meanings:
1. `schemaVersion`: schema version, currently `1.3.0`.
2. `generatedAt`: generation timestamp (UTC ISO string).
3. `source`: source file name used to build the catalog.
4. `skills`: skill entries.
5. `warnings`: non-blocking warnings (for example path exists but is not a skill repo). Public mode sanitizes local absolute paths.

## 2. Skill field semantics

Each `skills[]` item includes:
1. `id`: stable routing ID used by `--only <skill-id>`.
2. `displayName`: human-readable name.
3. `npm.name` / `npm.version`: default package coordinate and version.
4. `repository.https`: github fallback when npm flow fails.
5. `distributionSources`: machine-readable discovery sources (`githubRepo`, `npmPackage`, optional `clawhubId`).
6. `description`: high-level summary for routing.
7. `description_zh`: optional Chinese description, preferred by Chinese rendering and fallback to `description` when missing.
8. `capabilities`: short capability sentences for intent matching.
9. `artifacts`: boolean availability flags of required artifacts.
10. `setupCommands`: compatibility display commands for humans/local repos.
11. `clientSupport`: support level matrix by client type, including `ironclaw`.
12. `clientInstall`: machine-executable activation contract for `openclaw` and `ironclaw`.
13. `openclawToolCount`: number of OpenClaw tools.
14. `dependsOn`: optional direct dependency skill id list for composition/order-aware execution.
15. `sourcePath`: local-only optional field, omitted in public catalog by default.

## 3. `artifacts` semantics

1. `skillMd: true`
- Means target repo has `SKILL.md` and AI can extract capabilities/limits/safety rules.

2. `mcpServer: true`
- Means MCP entry is present via `src/mcp/server.ts` or equivalent `scripts.mcp`.

3. `openclaw: true`
- Means `openclaw.json` is present for OpenClaw tool descriptions.

## 4. `distributionSources` and `clientInstall`

1. `distributionSources`
- Describes where a host can discover a skill.
- `githubRepo` is for source lookup only, not final IronClaw activation.
- `npmPackage` is the default executable distribution coordinate.
- `clawhubId` is optional and only present when OpenClaw managed install is available.

2. `clientInstall.openclaw`
- `managed-install`: host should use ClawHub / managed install, no local command required.
- `package-setup`: host should execute `installCommand`, typically `bunx -p <pkg> <setup-bin> openclaw`.

3. `clientInstall.ironclaw`
- `trusted-local-install`: host should execute `installCommand`, typically `bunx -p <pkg> <setup-bin> ironclaw`.
- `requiresTrustPromotion: true` means the host must surface a trust prompt because trusted local files and MCP config will be written.

## 5. `clientSupport` enum semantics

1. `native`
- Usable out-of-box, usually with official artifacts and setup commands.

2. `native-setup`
- Natively supported but requires setup command execution first.

3. `manual-mcp`
- MCP-compatible but requires manual configuration.

4. `manual-cli-or-mcp`
- Can be connected manually via CLI or MCP.

5. `manual`
- Usable manually, no standard one-click setup path.

6. `unsupported`
- Not supported for that client at the moment.

## 6. `capabilities` writing guidelines

Recommended style:
1. Start with action verbs (for example `Query block status`, `Create wallet`).
2. One capability sentence should describe one action.
3. Avoid vague wording such as `handle everything`.
4. Include boundary hints such as `read-only` and `simulate/send`.

## 7. Modes and compatibility

1. Public mode (default)
- Command: `bun run catalog:generate`
- Output: `skills-catalog.json`
- Characteristic: no `sourcePath`, warnings are path-sanitized, suitable for external AI consumption.

2. Local mode (path debugging)
- Command: `bun run catalog:generate:local`
- Output: `skills-catalog.local.json`
- Characteristic: includes `sourcePath`, intended for local machine only.

3. Additive note (1.3.0)
- Added `setupCommands.ironclaw` for trusted-skill setup guidance.
- Added `clientSupport.ironclaw` to the client support matrix.
- Added `distributionSources` and `clientInstall` to distinguish discovery from activation.
- Existing consumers should ignore unknown fields if not needed.
