[中文](AI_E2E_SCENARIOS.zh-CN.md) | English

# AI End-to-End Execution Scenarios

This document provides executable AI storylines from routing to execution.

## Scenario 1: Query aelf block height

Goal: user asks “check current chain block height”.

Execution flow:
1. Read `skills-catalog.json` and locate chain-read skills.
2. Use routing matrix and choose `aelf-node-skill` (instead of `aelfscan`).
3. Run quick bootstrap:
```bash
./bootstrap.sh --only aelf-node-skill --skip-install
```
4. Follow that skill repo's setup path (MCP/OpenClaw/CLI).
5. Call the related read tool (for example get-chain-status / get-block-height).

Success criteria:
1. Returns latest block height.
2. Output includes selected skill and invocation mode for traceability.

## Scenario 2: Transfer routing before execution (EOA/CA)

Goal: user asks “transfer 1 ELF” without identity mode.

Execution flow:
1. Perform identity routing first:
- default `portkey-eoa-agent-skills` when no CA signals exist.
- switch to `portkey-ca-agent-skills` on guardian/CA hash/register/recover signals.
2. Ensure active wallet context is set (`portkey_set_active_wallet` or create/unlock flow auto-write).
3. Run read checks first (balance, address validity, network config).
4. Execute write operation (transfer) with `signerMode=auto`.
5. If context points to encrypted wallet, provide `password` input or password env.
6. If user requests safety first, prefer simulate/dry-run when available.

Success criteria:
1. Routing decision is explainable (why EOA vs CA).
2. Required pre-write checks are done before sending tx.
3. Output includes recovery hints (insufficient balance, network issues, missing context/password).

## Scenario 3: Awaken swap composition (Wallet + DEX)

Goal: user asks “swap ELF to USDT on Awaken”.

Execution flow:
1. Use routing matrix to determine wallet identity mode first:
- no CA signal: `portkey-eoa-agent-skills`
- with CA/guardian signals: `portkey-ca-agent-skills`
2. Use wallet skill for pre-checks (balance, address, network) and confirm active context.
3. Use `awaken-agent-skills` to fetch quote.
4. Perform allowance/approve and swap with `signerMode=auto` (shared context first).
5. If context signer requires password, pass tool input password or password env.
6. Return tx outcome with explicit composition-routing explanation.

Success criteria:
1. Clearly states the composition of wallet skill + awaken skill.
2. Required pre-checks and permission checks are completed before swap.
3. Output includes recovery hints (insufficient balance, approve failure, network errors).

## Scenario 4: AI contributor onboarding a new skill

Goal: AI receives a request to integrate a new skill into this aggregation repository.

Execution flow:
1. Read `CONTRIBUTING.md` and `docs/AI_SKILL_CONTRACT.md`.
2. Validate required schemas:
- `docs/schemas/workspace.schema.json`
- `docs/schemas/skill-frontmatter.schema.json`
- `docs/schemas/openclaw.schema.json`
- `docs/schemas/skills-catalog.schema.json`
3. If the skill supports MCP + setup, ensure catalog metadata exposes `setupCommands.ironclaw`, `clientSupport.ironclaw`, `distributionSources`, and `clientInstall`.
4. Add new path to `workspace.json` with `${SKILLS_BASE}` placeholder.
5. If dependency exists, add direct `dependsOn` entries.
6. Run gates in order:
```bash
bun run catalog:generate
bun run health:check
bun run readme:check
bun run security:audit
./bootstrap.sh --only <skill-id> --skip-install
```
7. Prepare PR body with the 6 fixed sections from AI contract.

Success criteria:
1. Catalog generation passes with schema `1.3.0`.
2. No gate failure (`health/readme/security/bootstrap`).
3. PR description contains Goal/Non-goal, key files, contract mapping, validation outputs, risk, rollback.

Additional install-routing rule:
1. GitHub repo URLs are discovery-only.
2. For OpenClaw/IronClaw execution, prefer `clientInstall.*.installCommand` when present.

## Common Recovery Template

1. Dependency download failed
- Action: `./bootstrap.sh --source github --only <skill-id>`

2. skill-id not found
- Action: `bun run catalog:generate`, then retry `--only`

3. health check failed
- Action: follow `health:check` output and add missing artifacts (setup/mcp/openclaw)
