---
name: bnbagent-studio-use-aws-agentcore
description: When the user wants to deploy or operate a bnbagent-studio project on AWS Bedrock AgentCore - deploy with `bag deploy --provider aws` (all cloud lifecycle mutations are delegated to pinned `@bnbagent/deploy-cli@0.6.6`), inspect with `bag deploy status` / `logs --provider aws` / `verify --provider aws`, and tear down with `bag deploy destroy --provider aws --execute [--purge]`. Also covers AWS credential prerequisites, the optional read-only quota probe, and the runtime-secret channel.
---

> **Reference file** of the `bnbagent-studio` router skill - installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# bnbagent-studio-use-aws-agentcore

Procedure for deploying and operating the seller Agent on **AWS Bedrock AgentCore** via the **delegated deploy**: `bag deploy --provider aws` hands a generated deploy spec to the pinned **`@bnbagent/deploy-cli`** (run via `bunx --bun`; override the command with `BNBAGENT_DEPLOY_COMMAND`), which executes every cloud lifecycle mutation through the AWS SDK under the user's credentials. There is **no `aws` CLI, no CDK deploy, and no `agentcore deploy`** in the mutation path - the npm `@aws/agentcore` CLI is used ONLY by `bag dev --container` (image-parity local runs). If the AWS CLI is installed, `bag deploy prepare` may use it only for a fail-open, read-only AgentCore quota-headroom probe.

The deployed product is **one** valuable Agent that serves its selected public faces (A2A → `0.0.0.0:9000`, MCP-only → `0.0.0.0:8000/mcp`, or A2A+MCP → A2A-native `dualMain.ts` on `:9000` with `/mcp` tunneled by the platform, per `app/agent/studio.toml [stack].protocols`): it holds the key, signs in-process, and is its own public endpoint behind an OAuth2 authorizer. There is no separate service to deploy - the agent IS the public surface, so this one procedure is the whole runtime deploy.

```
<workspace>/
├── agentcore/
│   ├── agentcore.json     # deploy descriptor: name (resource naming), protocol, authorizer, envVars
│   └── aws-targets.json   # AWS account + region the deploy targets
└── app/agent/             # the deployed code (entrypoint lives here)
```

> **`bag deploy --provider aws` runs the whole deploy.** It gates on readiness, builds the agent (`pnpm build`), collects the runtime secrets, and delegates to bnbagent-deploy. The old `bag deploy agent` spelling is a deprecated compatibility alias.

## Prerequisites

1. **Bun 1.3+ (`bunx`) on PATH** - the pinned `@bnbagent/deploy-cli` runs through it (`bag deploy prepare` fails a CRITICAL check when `bunx` is missing). Install from https://bun.sh, or point `BNBAGENT_DEPLOY_COMMAND` at another launcher.
2. **AWS credentials** for the deploy identity - use `bnbagent-deploy login --provider aws` or the standard env/profile files. Studio does not inspect credentials itself; the delegated deploy-cli validates identity and permissions before mutation. Credentials may come from `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_REGION` or the standard `~/.aws/credentials` file. Verify you're in the RIGHT account: it must match `agentcore/aws-targets.json` (the AWS Console's account menu shows the active account id). Least-privilege policy JSON: `docs/guides/agentcore-deploy-iam.md`.
3. **Docker running - container packaging only** (`wallet.kind = "twak"` or a scaffold with `[deploy].platform_artifact = "container"`): bnbagent-deploy builds the scaffolded Dockerfile locally for linux/arm64 and pushes it to ECR. A default evm-local AWS scaffold deploys as a Node zip and needs no Docker; an evm-local platform-container scaffold remains a container when AWS is selected later.
4. **`@aws/agentcore` CLI - ONLY for `bag dev --container`** (use the repository baseline, Node >=22: `npm install -g @aws/agentcore`). Not needed to deploy. ⚠️ Some environments carry `bedrock-agentcore-starter-toolkit`, a **same-named but incompatible** `agentcore` shim that can shadow the npm CLI on PATH. Check with `which -a agentcore` and remove the shim (or put the npm `@aws/agentcore` first on PATH) if `bag dev --container` misbehaves.
5. **AWS CLI - optional for readiness only.** When available, `bag deploy prepare` reads quota `L-F4575653` and lists existing AgentCore runtimes so it can stop before a full-quota deploy creates orphaned intermediate resources. The probe stays silent if the CLI, credentials, `servicequotas:GetServiceQuota`, `bedrock-agentcore:ListAgentRuntimes`, or usable JSON output is unavailable. The delegated deployment itself does not require the AWS CLI.

## The runtime-secret channel (read this first)

The deployed runtime does NOT read `.env.local` - nothing ships it. Instead, `bag deploy --provider aws` collects the runtime secrets (provider/storage keys, `WALLET_PASSWORD`, the encrypted keystore as `WALLET_KEYSTORE_JSON` - or the twak bundle; for `wallet.kind='altana'` ONLY the bounded session as `ALTANA_SESSION` - no keystore, no `WALLET_PASSWORD`) and hands them to bnbagent-deploy as a private (mode 0600) tempdir envFile. The deploy CLI provisions them as ONE Secrets Manager secret (`bnbagent/<project>/runtime`), injects the `BNBAGENT_RUNTIME_SECRET_ID` pointer into the runtime env, and grants the runtime execution role read access. The entrypoint loads the bundle at cold start.

> **The KEYSTORE is never bundled.** The encrypted wallet keystore lives at the WORKSPACE root (`.studio/wallets/`, outside `app/agent/`, so no packaging path can include it) and reaches the runtime ONLY via that Secrets Manager channel. Only put non-secret runtime config in `agentcore.json` `envVars[]`.

> **`--secrets-mode envvars` is testnet-only.** It inlines the secrets as PLAINTEXT runtime env vars in the deploy spec - use it only when you cannot grant `secretsmanager:CreateSecret`; it is refused on mainnet.

Provider-native overrides: the optional `studio.toml [deploy.agentcore]` table passes verbatim deploy-spec keys through to CreateAgentRuntime / UpdateAgentRuntime. Two keys are reserved and refused: `secretName` (studio-managed) and `environmentVariables` (would replace the merged runtime env, secret pointer included).

## Command reference

Everything runs through `bag deploy` (run `bag deploy <cmd> --help` for flags); cloud execution is the pinned bnbagent-deploy's job.

| Command | What it does |
| --- | --- |
| `bag deploy prepare` | The deploy-readiness sweep, including `bunx` and the optional fail-open AgentCore quota probe. Run before deploying. |
| `bag deploy --provider aws [--yes]` | The whole deploy: prepare gate → AWS-permissions notice → secret hand-off → `pnpm build` → delegated deploy (artifact, runtime create/update, secret provision + role grant, Cognito inbound OAuth) → ARN capture + state stamp. Automation requires `--yes`; add `--allow-multiple` when another provider stays active. |
| `bag deploy verify [--provider aws]` | Ask bnbagent-deploy for live provider status, then reconcile ERC-8004. Provider is required only when multiple deployments are recorded. |
| `bag deploy status [--provider aws]` | List every recorded deployment and delegated live state (read-only); `--no-probe` is local-only. |
| `bag deploy logs [--provider aws] [--follow] [--since 10m]` | Delegate runtime logs to bnbagent-deploy. |
| `bag deploy destroy [--provider aws]` | Dry-run teardown plan; `--execute` delegates `destroy --yes`; `--purge` also deletes retained ECR/log resources. |
| `bag deploy provision-cognito [--wire]` | **Deprecated** (hidden from `--help`). Emits a Cognito CDK app whose pool a deploy never uses. |

## Typical workflows

### A. Run locally

Prefer `bag dev` (auto-loads `.env.local`, runs the agent in-process, no Docker). `bag dev --container` opts into the native `agentcore dev` container for full image parity - the ONE flow that needs the npm `@aws/agentcore` CLI plus a container engine.

### B. Deploy to AWS (delegated)

> ⚠️ **First deploy: relay the AWS-permissions notice to the user.** Deploying provisions resources in the user's AWS account. `bag deploy --provider aws` prints a pre-deploy notice (required-permission guides, AWS best-practice links, and a disclaimer) and gates the project's FIRST deploy on an explicit acceptance - in a non-interactive run it exits with an error instead of prompting. When that happens: show the printed notice to the user **verbatim**, get their explicit consent, then re-run with `--accept-risk`. NEVER add `--accept-risk` without asking the user first.

> 🔒 **Inbound auth is auto-provisioned.** An AgentCore seller endpoint is **never anonymous**. The delegated deploy provisions a Cognito inbound OAuth (account pool + per-agent M2M client) so the runtime is token-gated, then writes the live token URL, scope, client id, and discovery URL back into `studio.toml`, `agentcore.json`, and the printed buyer block. Hand those to each buyer; the client secret is retrieved read-only in the AWS Console (Cognito → User pools → App clients → "Show client secret") - never persisted by studio.
>
> `bag deploy provision-cognito` (the CDK path) is **deprecated**: a deploy provisions and uses its own pool regardless, so the CDK stack is a billable orphan and anything wired from it gets overwritten.
>
> Buyers reach the agent over plain HTTPS + an OAuth2 Bearer (the client-credentials grant) - **no AWS SigV4 / IAM credentials**. Locally, `bag dev` runs without Cognito env, so the card omits the scheme.

The 2026-07-20 live baseline passed both ZIP and linux/arm64 container through deploy, status, OAuth-authenticated signed A2A negotiation, logs, destroy, and purge. A SigV4 invoke against this custom-JWT endpoint is expected to fail; use the buyer OAuth bearer when verifying the data plane. That baseline bypassed local storage readiness and therefore does not prove funded delivery or durable storage.

```bash
# 1. Set the real AWS account + region in agentcore/aws-targets.json and
#    export the deploy credentials (env vars or ~/.aws/credentials).
# 2. Check readiness, then deploy - the pinned bnbagent-deploy does the cloud work:
bag deploy prepare
bag deploy --provider aws
```

> After deploy, ERC-8004 registration records the **AgentCore endpoint**: A2A uses the normalized agent-card URL (`AgentEndpoint.a2a`), while MCP records the `/mcp` endpoint plus access metadata. `bag deploy verify` handles this. The on-chain identity points buyers straight at the agent; there is no proxy or relay in front of it.

### B1. Troubleshooting the delegated deploy

- **`could not start bnbagent-deploy (bunx not found)`** - install Bun 1.3+ (https://bun.sh) or set `BNBAGENT_DEPLOY_COMMAND` to a command that can run the pinned `@bnbagent/deploy-cli`.
- **Permission denials (AccessDenied)** - the deploy identity is missing one of the least-privilege statements; apply the policy JSON from `docs/guides/agentcore-deploy-iam.md`. The deploy CLI preflight-simulates its permissions when it can and names the denied actions.
- **Wrong account** - the credentials in the environment resolve to an account that does not match `agentcore/aws-targets.json`; fix the env vars / `~/.aws/credentials` profile, not the descriptor.
- **Container build fails / hangs** (twak) - the image is built LOCALLY for linux/arm64 and pushed to ECR; Docker must be running (x86 machines need buildx/containerd cross-build support).
- **`agentcore_quota_headroom` CRITICAL (quota 0 or full)** - the `L-F4575653` ("Total Agents per Account") quota has no free slot; new accounts can start at an applied quota of ZERO even though the console shows a higher default. Raising it is a manual AWS step (`bag` and the AWS CLI cannot request it): open the Service Quotas console for "Amazon Bedrock AgentCore" in the target region and request an increase — low first requests are sometimes rejected and need an AWS support case. Check where an earlier request stands with `aws service-quotas list-requested-service-quota-change-history --service-code bedrock-agentcore --region <region>` (a `CASE_CLOSED` entry without a quota change means it was rejected — escalate via support). While the increase is pending, deploy to the managed platform instead: `bag deploy --provider bnb`. If the quota is full but nonzero, `bag deploy destroy` in an old workspace frees a slot.

### C. Inspect / operate

```bash
bag deploy status                         # every recorded provider + delegated live state
bag deploy logs --provider aws --since 1h # delegated CloudWatch tail
bag deploy verify --provider aws          # delegated status + ERC-8004 reconcile
bag deploy destroy --provider aws         # dry-run teardown plan
bag deploy destroy --provider aws --execute # delegated teardown (add --purge)
```

If verification reports a partial ERC-8004 registration because `setAgentURI` did not complete, the deployment check remains a warning and records pending identity state. Retry with `bag erc8004 update-endpoint --endpoint <url>`, or run `bag erc8004 clear-pending` first when the relay transaction was never observed on-chain.

## Reference

- b402/x402 selling on self-hosted AgentCore: the rail activates in-process with complete B402 credentials for PAID, or without them when explicit zero selects FREE. There is no anonymous URL - operate your own HTTP front that relays envelope-v1 through the runtime's configured authorizer. The default Bag deploy uses Cognito OAuth over HTTPS, not SDK/SigV4. PAID also needs a fixed-egress B402 Relay or VPC/NAT/Elastic-IP path. See `bnbagent-studio-selling-via-b402` and the public [BNB Agent Studio deployment guide](https://docs.bnbchain.org/developer-kit/bnbchain-studio/deployment/).
- `bag deploy --help` / `bag deploy <command> --help` (authoritative for commands + flags)
- `agentcore/agentcore.json` - name (resource naming continuity), protocol, authorizer, envVars
- `agentcore/aws-targets.json` - AWS account + region
- `app/agent/studio.toml [deploy.agentcore]` - provider-native deploy-spec passthrough
- `docs/guides/agentcore-deploy-iam.md` - least-privilege IAM for the delegated deploy
- `BNBAGENT_DEPLOY_COMMAND` - override the pinned `bunx --bun @bnbagent/deploy-cli@<pin>` invocation (E2E/dev)
