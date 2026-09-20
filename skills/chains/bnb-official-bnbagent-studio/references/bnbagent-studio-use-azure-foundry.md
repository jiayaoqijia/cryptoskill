---
name: bnbagent-studio-use-azure-foundry
description: When the user wants to deploy or operate a bnbagent-studio project on Azure AI Foundry Hosted Agents - scaffold with `bag init --runtime azure-foundry`, deploy either to the managed platform with `bag deploy --provider bnb --backend azure` or directly with `bag deploy --provider azure`; all cloud lifecycle execution is delegated to pinned `@bnbagent/deploy-cli@0.6.6`. Native MCP is not supported on Azure; use AgentCore for MCP.
---

> **Reference file** of the `bnbagent-studio` router skill - installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# bnbagent-studio-use-azure-foundry

Azure Foundry is listed in `bag init --help` and the deploy provider menu. The
Foundry data plane, Entra scope, unified entrypoint, deployment flow, and x402
envelope tunnel were verified end to end in 2026-08.

Procedure for deploying and operating the seller Agent on **Azure AI Foundry Hosted Agents** (`[stack].runtime = "azure-foundry"`). ALL cloud execution is **delegated to the pinned `@bnbagent/deploy-cli`** (run via `bunx --bun`; override with `BNBAGENT_DEPLOY_COMMAND`), whose Azure provider is **SDK/REST-only**. Studio never shells out to (or requires) the `az` / `azd` CLIs. Direct user-owned deployment uses browser/local credentials and may self-heal RBAC; the managed platform uses environment credentials in `ambient-only` mode and only probes RBAC.

```
<workspace>/
├── app/agent/             # the deployed code (src/unifiedMain.ts host + Dockerfile here)
│   ├── studio.toml        # [azure] resources plus named HTTP/A2A/Invocations endpoint records
│   └── Dockerfile         # the container image bnbagent-deploy builds + pushes
└── .studio/               # secrets + wallets (workspace root - never in the image)
```

> **Deploy model: CONTAINER-ONLY.** The deploy-cli Azure provider rejects Node zip artifacts, so every azure-foundry deploy builds the scaffolded `app/agent/Dockerfile` **locally with Docker** (linux/amd64) and pushes it to the auto-provisioned Azure Container Registry; Foundry Agent Service pulls and runs the image. A running Docker daemon is required.

> **Protocol:** A2A, X402-only, and A2A+X402 projects are supported. The deployed Node host speaks both Foundry container contracts on `:8088`: `GET /readiness`, pass-through `POST /invocations`, and OpenAI-compatible `POST /responses`; new direct A2A deploys also enable native incoming A2A. None of these endpoints is native MCP streamable HTTP, so `bag init` and provider selection reject azure-foundry + MCP.

> **Auth is explicit.** User-owned Azure needs a saved delegated browser sign-in, or an ambient Azure credential chain in CI. Deployment itself never shells out to `az` or `azd`, and a non-interactive deploy cannot open a browser.

## Prerequisites

1. **Bun 1.3+ (`bunx`) on PATH** - the pinned `@bnbagent/deploy-cli` runs through it.
2. **Docker running** - the image is built locally (linux/amd64) before push.
3. **An Azure subscription** the operator may provision in (Foundry account/project, container registry, hosted agent). Before a local self-deploy, run `bunx --bun @bnbagent/deploy-cli@0.6.6 login --provider azure`; use OIDC/service-principal credentials in CI.

## ⚠️ Foundry gotchas (read before deploying)

`bag deploy prepare --runtime azure-foundry` encodes these as checks, but know them:

- **Region must support Hosted Agents.** Default `eastus2`. `eastus` does NOT. Prepare refuses an unsupported `[azure].location` (else deploy fails with `Unsupported region for Foundry Hosted Agents`).
- **Account name MUST equal the custom subdomain.** The runtime derives `https://{account_name}.services.ai.azure.com`; a mismatch resolves to NXDOMAIN and the agent returns HTTP 500. `bag init` sets them equal - keep them equal in `[azure]`.
- **Empty `APPLICATIONINSIGHTS_CONNECTION_STRING` crashes the exporter.** The emitted entrypoint drops it when blank - don't remove that guard.
- **The hosted container contract is fixed.** Keep `AGENT_PORT=8088`, `GET /readiness` returning HTTP 200, and both `POST /invocations` and `POST /responses`. Local A2A still runs on `:9000`; do not copy that local port into the Foundry Dockerfile.
- **Prepare checks are local-only.** They validate the scaffold (region, subdomain, entrypoint + Dockerfile, an OpenAI-compatible `[llm]` provider, twak readiness) without any cloud call; Azure auth happens at deploy time.

## Runtime secrets - the delegated hand-off

`bag deploy --provider azure` bundles the runtime secrets (provider/storage keys, `WALLET_PASSWORD`, the encrypted keystore as `WALLET_KEYSTORE_JSON` - plus the `BNBAGENT_LLM_*` wiring the Foundry host reads) and hands them to bnbagent-deploy as a private (mode 0600) tempdir envFile; the deploy CLI provisions them for the hosted agent as **Foundry CustomKeys**. No vault setup, no role assignments, and no cloud CLI on your side.

> The encrypted keystore (`.studio/wallets/`) stays at the workspace root and rides only that secret channel - never baked into the image.

Provider-native overrides go in the optional `studio.toml [deploy.foundry]` table (verbatim deploy-spec keys; deploy-cli 0.5.14 consumes `account`, `cpu`, `incomingA2a`, `agentCard`, `location`, `memory`, `project`, `projectEndpoint`, `protocol`, `rawInvocations`, `registry`, and `subscriptionId`, and warns about anything else). The `[azure]` block's `subscription_id` / `account_name` / `project_name` / `project_endpoint` / `location` win over conflicting `[deploy.foundry]` keys.

## Typical workflow

### A. Scaffold

```bash
bag init myagent --runtime azure-foundry
```

`bag init` makes no Azure calls; all cloud onboarding happens at deploy time.

### B. Deploy

> **Preview, live E2E verified 2026-07-20.** The A2A azure-foundry path was verified through container build/push, CustomKeys wallet injection, hosted agent create/update, cold-start smoke, status, invoke, logs, a signed `negotiate`, and destroy. Foundry itself remains a preview service.

> ⚠️ **First deploy: relay the Azure-resource notice to the user.** `bag deploy --provider azure` prints a notice that the delegated deploy CREATES billable Azure resources (Foundry account/project, container registry, hosted agent container) under the signed-in subscription. Show it, get consent, then deploy.

```bash
bag deploy prepare --runtime azure-foundry   # local readiness gate (region/subdomain/Dockerfile)
bag deploy --provider azure                  # delegated: onboard → build+push → CustomKeys → deploy [--smoke]
```

`bag deploy --provider azure` runs an HTTP contract smoke by default (pass `--skip-smoke` to omit it), enables incoming A2A, and captures `[azure].http_endpoint`, `a2a_endpoint`, and `agent_card_endpoint`. When X402 is selected it also declares and records `[azure].invocations_endpoint` for the operator's authenticated envelope tunnel. `[azure].agent_endpoint` remains the compatibility primary and points to A2A for new deployments. If Foundry creates the resource but a post-create check fails, Studio still records discovered endpoints so `status`, `logs`, and `destroy` can manage it; the deploy command continues to return non-zero.

For a first deploy in non-interactive automation, pass `--yes`. Studio treats
that as confirmation of the full deployment plan and delegates explicit
Foundry project onboarding. Configure `[azure].subscription_id` and
`account_name` when several candidates are accessible so no prompt or guess is
required.

For a first deploy in non-interactive automation, pass `--yes`. Studio treats
that as confirmation of the full deployment plan and delegates explicit
Foundry project onboarding. Configure `[azure].subscription_id` and
`account_name` when several candidates are accessible so no prompt or guess is
required.

### C. Validate / operate

```bash
bag deploy status                            # all recorded providers + live state
bag deploy info --provider azure --with-curl # endpoint + Entra token shortcut + request body
bag deploy logs --provider azure --limit 50 # delegated Hosted Agent logs
```

`bag deploy info` reads the recorded named Azure endpoints without recreating the temporary deploy spec. `--with-curl` adds an optional `az account get-access-token --resource https://ai.azure.com` shortcut and complete Responses HTTP, Agent Card, and A2A requests. This does not make the Azure CLI a deploy prerequisite;
application clients may mint the same `https://ai.azure.com/.default` scope
with `DefaultAzureCredential` or `ClientSecretCredential`.

The generated curl stores the response headers, extracts
`x-agent-session-id`, and prints the exact
`bag deploy logs --provider azure --session <id>` command. Without an explicit
session, logs lists the recent sessions visible to the current Azure identity.
Foundry scopes that list by identity/isolation key, so an external buyer or
gateway must still preserve the session header from its own response.

The built-in smoke proves the container contract, not the seller signature. For a release E2E, POST A2A JSON-RPC `message/send` to the recorded A2A endpoint with `A2A-Version: 0.3`, `params.message.kind = "message"`, and the JSON skill envelope in a `text` part; or use the Responses/Invocations contract selected for the deployment. Require `response.accepted=true`, a non-empty `negotiation_hash`, and `provider_sig`.

### X402 external gateway

Foundry does not expose a raw anonymous `/x402` URL. An operator-run HTTPS
gateway authenticates to the recorded Invocations endpoint with an Entra token
for `https://ai.azure.com/.default`, wraps the incoming HTTP request as
`http-envelope-v1`, and unwraps the returned inner status, headers, and base64
body:

```json
{
  "v": 1,
  "method": "POST",
  "path": "/x402",
  "query": {},
  "headers": { "content-type": "application/json" },
  "body": "<base64-encoded request body>"
}
```

`bag deploy info --provider azure --json` reports the deployed face snapshot,
seller state, carrier contract, and a request example. In FREE mode that
example executes seller work without a payment; in PAID mode it returns the
inner 402 before work until a valid payment is supplied. A PAID seller also
needs fixed facilitator egress; use an Azure Container Apps workload-profiles
environment with VNet integration and a NAT Gateway static IP, then allowlist
that IP with B402. Studio does not deploy or manage the gateway or network.

### X402 external gateway

Foundry does not expose a raw anonymous `/x402` URL. An operator-run HTTPS
gateway authenticates to the recorded Invocations endpoint with an Entra token
for `https://ai.azure.com/.default`, wraps the incoming HTTP request as
`http-envelope-v1`, and unwraps the returned inner status, headers, and base64
body:

```json
{
  "v": 1,
  "method": "POST",
  "path": "/x402",
  "query": {},
  "headers": { "content-type": "application/json" },
  "body": "<base64-encoded request body>"
}
```

`bag deploy info --provider azure --json` reports the deployed face snapshot,
seller state, carrier contract, and a request example. In FREE mode that
example executes seller work without a payment; in PAID mode it returns the
inner 402 before work until a valid payment is supplied. A PAID seller also
needs fixed facilitator egress; use an Azure Container Apps workload-profiles
environment with VNet integration and a NAT Gateway static IP, then allowlist
that IP with B402. Studio does not deploy or manage the gateway or network.

### D. Tear down

```bash
bag deploy destroy --provider azure                 # dry-run plan
bag deploy destroy --provider azure --purge-images  # read-only ACR repository inventory
bag deploy destroy --provider azure --execute       # delegates `destroy --yes`
bag deploy destroy --provider azure --execute --purge-images # delete this agent's owned ACR repository
bag deploy destroy --provider azure --execute --purge # retained resources too
```

Default destroy keeps pushed images and reports that they continue to bill for
storage. `--purge-images` inventories manifest/tag count and estimated image
size, then deletes only the deterministic `bnbagent/<agent-name>` repository in
a registry proven to be owned by bnbagent-deploy. External registry overrides,
untagged registries, and registries shared by another Foundry project are kept.
`--purge` also removes the retained resources the deploy record tracks -
including the soft-deleted Cognitive Services account, freeing the custom
subdomain immediately (otherwise held ~48h). A successful teardown clears all
recorded `[azure]` endpoints.

## Scope note

Azure Foundry is an alternate runtime for the whole seller agent. There is no separate keyless Layer B service to keep in sync; ERC-8183 seller delivery still runs through the single signer runtime selected in `studio.toml [stack].runtime`.

## Reference

- `bag deploy --help` / `bag deploy <command> --help` (authoritative for commands + flags)
- `app/agent/studio.toml [azure]` - resource configuration plus `http_endpoint` / `invocations_endpoint` / `a2a_endpoint` / `agent_card_endpoint`
- `app/agent/studio.toml [deploy.foundry]` - provider-native deploy-spec passthrough
- `BNBAGENT_DEPLOY_COMMAND` - override the pinned `bunx --bun @bnbagent/deploy-cli@<pin>` invocation (E2E/dev)
