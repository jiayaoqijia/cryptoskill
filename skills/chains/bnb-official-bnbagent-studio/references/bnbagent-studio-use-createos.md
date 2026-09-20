---
name: bnbagent-studio-use-createos
description: Deploy and operate Studio agents on CreateOS through the nodeops provider and published deploy 0.6.6 SDK. Covers account credentials, ZIP/container packaging, runtime secrets, health recovery, project lifecycle and wallet payment restrictions.
---

# Deploy and operate on CreateOS

Use Studio's `nodeops` provider for NodeOps-hosted infrastructure. AWS and Azure providers remain separate choices for infrastructure in the user's own cloud account. Studio pins `@bnbagent/deploy-cli@0.6.6` and resolves the published `@bnbagent/deploy-provider-nodeops/sdk` through that dependency. No local deploy checkout, source override or Bun process is required for NodeOps.

## Check the installed CLI

Run `bag --version` and `bag deploy --help`. Confirm that `nodeops` is advertised before following this reference; older Studio releases lack the adapter. If absent, use the main skill's approved upgrade workflow. Do not bypass Studio with a raw provider deployment, because it omits Studio packaging, secrets and resource records.

The generic router's minimum version does not establish NodeOps compatibility. Use the release's documented CLI version with deploy 0.6.6; an alpha may be required while npm `latest` lacks this integration. Do not repeatedly install `latest` without checking its capabilities. Reuse existing installation authorization and verify the selected CLI's version and provider after installation.

## Complete a build-and-deploy request

For requests such as "build a simple agent and deploy it to NodeOps", carry the task through implementation, local testing, deployment and a real business request to the deployed endpoint. Use the scaffolding reference for project mechanics; this section takes precedence over its generic intake form and AWS/platform defaults for a NodeOps task.

- Infer routine technical choices from the request and existing project. Ask only for missing information that affects the outcome: what the agent should do, access/pricing intent when material, unavailable credentials/funding, or an unapproved spending limit. If a useful simple behavior was delegated to you, choose it and state the assumption. Do not require the user to choose a protocol, signer, build transport or cloud architecture. Keep prior authorization; do not repeatedly ask for the same budget approval.
- Preserve an existing deployment's recorded identity and configuration. For a new project, honor an explicit mode; a request to pay NodeOps with x402 or MPP selects wallet mode. Otherwise reuse a configured account/API Key when available, or use wallet mode. Do not require a CreateOS account merely because the workload is an agent. Account is the suitable existing option when in-place updates or logs are required; do not silently change a wallet choice to obtain those features.
- For a new wallet-mode project without an explicit payment selection, prefer `evm-local`, BSC USDC and MPP. Preserve an existing compatible wallet and configured chain/protocol. The MPP preference is based on the standalone live probe, not a claim that Studio's full live E2E is already certified. An explicitly requested x402 payment sets `[deploy.nodeops.payment].protocol = "x402"`; never fall back to MPP silently. Check the Gateway's advertised chains and the actual deployment challenge. A missing matching offer is a blocker, not permission to change the payment terms.
- Use `--destination self --no-onboard` for NodeOps, with ZIP for a compatible Node workload; select Dockerfile source when required by its dependencies. The generated runtime template name does not mean deployment to AWS. NodeOps runs through the Node.js SDK and does not require Bun, AWS credentials or AgentCore provisioning. Keep the agent's business network separate from the hosting-payment chain; BSC USDC hosting payment does not authorize changing the agent's business network or enabling its seller-payment rail.
- Implement the requested behavior and verify a representative local input/output before paying for deployment. Use the explicit business configuration below instead of the scaffold's paid defaults. A generated stub is not a completed application. Reuse available model/storage configuration and collect missing secrets only through the local secret workflow. Configure an appropriate persistent store if the requested behavior produces durable deliverables; do not claim local filesystem storage is durable cloud storage. Complete the public buyer URL preflight below before submitting any deployment POST.
- Check the wallet and prepare the artifact with the commands below. Show the estimated/actual hosting cost and enforce the approved caps; example caps are not authorization. Funding and credential entry may require the user's wallet or terminal. Once authorized, complete the deployment and verification without handing ordinary CLI steps back to the user. An unavailable prerequisite should leave a working local implementation and a precise explanation of what remains.

Hosting-payment x402 and selling the agent's service through x402 are separate choices. A request to "pay NodeOps using x402" changes only the hosting-payment configuration. Do not add merchant onboarding or enable a paid seller face on that basis. For an ambiguous "use x402" request, resolve it from context; ask one short clarification only when both interpretations remain plausible. If paid agent service is also requested, read the seller reference and verify its provider prerequisites separately.

### Choose an explicit business interface before initialization

Bare `bag init` defaults to A2A plus a paid B402 face and both commerce rails. Do not inherit those defaults for a request that only authorizes NodeOps hosting payment. Keep an existing project's chosen business interface and prices. For a new project, resolve the intended service access and price from the user's request; if unclear, ask about free versus paid access in product terms, not about protocol internals.

For an A2A seller using ERC-8183 jobs, explicitly pass `--protocols A2A --rails 8183`. For a user-approved zero-price job service, the initialization shape is:

```bash
bag init <name> --destination self --wallet-kind evm-local --no-onboard \
  --protocols A2A --rails 8183 --erc8183-price 0 \
  --network <business-network> --llm-provider <configured-provider> \
  --storage-provider <configured-store>
```

Replace the placeholders with the selected business settings. Zero ERC-8183 price removes token escrow, but job creation/funding-state transitions, on-chain gas and deliverable submission still apply; it is not anonymous free HTTP access. For a paid ERC-8183 service, replace `0` with the agreed price in token base units. Do not add `--payment-protocol x402` to select NodeOps hosting payment: that init flag configures the agent's seller face. Set hosting payment only in `[deploy.nodeops.payment]`.

The current NodeOps readiness path rejects an X402/MPP-only B402 business service with `x402_forced_dormant_runtime`, including zero-price mode. Do not recommend `--protocols X402 --rails b402 --b402-price 0` as a working NodeOps shortcut, bypass readiness, or add an unused ERC-8183 rail just to turn a blocker into a warning. If the user requires ordinary anonymous HTTP or a paid B402-only service, complete the local business implementation and identify the missing supported deployment/serving path before incurring hosting costs. NodeOps hosting-payment x402 remains a separate supported adapter path.

### Finish with an operational agent

After `deploy`, use the saved project/deployment IDs to poll status and run `bag deploy verify --provider nodeops --skip-register`. Complete and verify any prearranged domain routing, fetch the Agent Card and check its advertised `url`, then send a representative request through that public business address and check the returned result against the local expectation. Health HTTP 200 and an Agent Card alone do not prove the agent works. For ERC-8183, a successful `negotiate` or `notify_funded` acknowledgement is insufficient: exercise the authorized buyer/job flow through the deliverable result, including gas even for zero token escrow. For paid business requests, use the configured buyer/payment flow within its separately authorized budget; never add a public bypass or disable billing to make verification pass. Register the agent only if requested or already authorized, after verifying its advertised public URL.

Deliver the working URL, a usable request example, the observed business result, deployment identifiers and available payment receipt/cost evidence. If existing credits paid for deployment, say so rather than claiming x402/MPP settlement was exercised. Clearly report any remaining business or payment verification gap. On an uncertain payment or acknowledged deployment failure, follow the recovery rules below; do not start a new paid deployment as a retry. Do not delete a successfully delivered resource as test cleanup unless requested.

## Account mode for seller agents

Add to `app/agent/studio.toml`:

```toml
[deploy.nodeops]
mode = "account"
port = 8080
packaging = "zip"
# health_path = "/ping"
# account_id = "your-createos-account-id"
# environment = "production" # must already exist
```

Inject `CREATEOS_API_KEY` through the process environment. Use the existing Studio secret workflow for model, wallet and storage credentials; never copy secrets into source or the archive. Studio sends runtime secrets separately from the artifact and excludes the control-plane API Key. The account needs sufficient CreateOS credits; account deployment does not buy credits automatically.

```bash
bag deploy prepare --provider nodeops
bag deploy --provider nodeops --yes
bag deploy list --provider nodeops --json
bag deploy status --provider nodeops --json
bag deploy verify --provider nodeops --skip-register
bag deploy logs --provider nodeops
```

Readiness builds and validates a temporary artifact without cloud mutation. ZIP packaging needs an HTTP entrypoint compatible with Studio's generated A2A/MCP recipes. For container packaging, set `packaging = "container"` and `image_repository = "ghcr.io/owner/agent"`, supply a Dockerfile and safe `.dockerignore`, and authenticate Docker to the registry. The resulting image must be publicly pullable. TWAK requires a container with its CLI installed.

Redeploying in account mode updates the matching project. If another provider remains active, automation needs `--allow-multiple`. Preserve the account pin when managing an existing project. Studio rejects ambiguous identities rather than selecting one silently.

## Public buyer URL preflight — before any deploy POST

For the generated A2A card or a business payment challenge, resolve the public base URL before deployment. Set `BNBAGENT_PUBLIC_URL` in workspace `.studio/.env.local` with `bag env set BNBAGENT_PUBLIC_URL <public-base-url>` (no `/x402` or `/mpp` suffix). Studio also supplies it as `AGENTCORE_RUNTIME_URL`. Without it, these generated URLs fall back to localhost; `verify --skip-register` checks HTTP reachability and does not validate the Card's advertised URL. This is a skill preflight requirement, not a check already enforced by the CLI.

- **Account:** reuse a known stable environment URL or an already configured domain where available. If initial provisioning is needed to obtain the address, account mode supports a subsequent configuration/code deployment to the same project. Include that second deployment in the authorized plan and verify the current endpoint afterward; do not call the initial health-only result complete.
- **Wallet:** the initial deployment's generated URL is not known in advance, and this adapter cannot update runtime variables or redeploy the same project afterward. Use a known user-controlled public hostname only with a concrete, authorized routing plan, such as an existing reverse proxy that can be pointed at the returned service URL after deployment. Configure the hostname in runtime variables before the first upload, then execute and verify that routing after deployment. Do not invent a NodeOps custom-domain API or assume the wallet SDK provisions the hostname.

If wallet mode has neither a usable stable address/routing plan nor an already implemented and tested way for the application to advertise its correct public origin, stop before the deploy POST and explain the missing prerequisite. Keep the local implementation ready. Do not pay first and propose editing local `.env` afterward, redeploy to learn another URL, or silently switch to account mode. A plain health probe may be deployed without discovery for an explicitly scoped infrastructure test, but it is not delivery of the requested operational agent.

After deployment, inspect the A2A Card's `url` and any applicable business payment resource URL: they must use the intended public origin, never localhost, a bind address or an unrelated deployment. Exercise that advertised address, not just the provider's generated health URL. Preserve records and report a remaining verification gap if this fails; do not pay for a replacement as recovery.

## Health, records and recovery

Studio checks `/ping` (or `health_path`) and the A2A agent card when enabled. Deploy exits nonzero on health failure, but the cloud resource and `.studio/deployments/nodeops.json` record remain. `status --json` includes `last_health`, a saved observation rather than a new application probe. Retry `verify --skip-register` to refresh it without redeploying or paying. Omitting `--skip-register` may register/update the ERC-8004 endpoint through Studio's normal workflow.

Remote `list` can find projects absent from local records. Status/logs/verify/destroy use locally recorded mode, origin, subject and environment even if configuration later changes. Do not fabricate local records from a similarly named project.

```bash
bag deploy destroy --provider nodeops                 # preview
bag deploy destroy --provider nodeops --execute --yes # delete entire project
```

Deletion removes project environments too; registry images and payment history remain. `--purge` and `--purge-images` are unsupported for NodeOps.

## Wallet deployment through conversation

Read this section before choosing a wallet for NodeOps. Use `evm-local` for the currently tested Studio signing path. Turnkey implements the required public signing interfaces but still needs provider-specific live acceptance testing. TWAK lacks generic EIP-712 signing; Altana's session `x402.pay` is not wired into Gateway authentication/payment. Do not silently replace an existing wallet to work around these limits.

Studio pins published deploy 0.6.6, which supports runtime credentials through `settings.runEnvs`, independently of the uploaded archive. The 2026-09-10 standalone live probe confirmed Dockerfile deployment, BSC MPP settlement and runtime variable injection; the installed-package integration suite covers the Studio path with injected HTTP responses. These do not establish secret-vault encryption, redaction or variable rotation. If readiness reports an older SDK without runtime variable support, follow the approved CLI upgrade workflow; do not use a source override or embed credentials in the artifact.

For evm-local workloads, runtime variables include the encrypted `WALLET_KEYSTORE_JSON` and its `WALLET_PASSWORD`. NodeOps therefore receives the material needed by the deployed agent to unlock and use that wallet. The claim "no private-key export" applies to the hosting-payment signer, not to runtime custody. Explain this boundary when choosing the deployment wallet, honor existing custody authorization and prefer a dedicated wallet for new third-party-hosted agents. Do not display or log the secret payload or imply that keystore encryption keeps it inaccessible to a runtime that also receives the password.

For a new project, use the explicit business-interface initialization above, install dependencies, and run `(cd app/agent && bag wallet new --generate-password)`. To import a raw key with a new generated password, use `bag wallet new --private-key - --generate-password` with the key supplied by the user through stdin. If the user requires their own password, they privately read/export `WALLET_PASSWORD` in their terminal and run `bag wallet new --private-key - --save-password`; the flag persists it in `.studio/.env.local` (0600) and refuses existing wallets or a different saved password. Never put passwords or private keys in argv. Reuse an initialized wallet within its authorized custody scope instead of generating another. Configure model/storage credentials using the existing local secret workflow; never collect private keys, passwords or API keys in chat. A wallet used to pay NodeOps is not automatically compatible with every runtime wallet backend.

Merge the following into `app/agent/studio.toml`. These amounts are example spending caps, **not a NodeOps quote**; use the user's approved limits. Keep existing signing-policy entries.

```toml
[deploy.nodeops]
mode = "wallet"
packaging = "zip"
port = 8080

[deploy.nodeops.payment]
protocol = "mpp"
chain = "bsc"
asset = "USDC"
months = 1
max_per_payment_usd = "5.00"
max_per_day_usd = "5.00"
max_per_month_usd = "20.00"
max_approval_gas_wei = "1000000000000000"
auto_pay = false
use_existing_credits = false

[wallet.signing]
extra_domains = [[56, "0x000000000022D473030F116dDEE9F6B43aC78BA3"]]
extra_primary_types = ["PermitWitnessTransferFrom"]
```

For a wallet workload that needs a Dockerfile, merge the following into the same `[deploy.nodeops]` table, preserving the payment and signing tables:

```toml
[deploy.nodeops]
mode = "wallet"
packaging = "container"
build = "remote"
port = 8080
```

Provide `app/agent/Dockerfile`, a safe `.dockerignore`, and a process that listens on the configured port. This uploads source for NodeOps to build; do not add account-only `image_repository`, Docker registry credentials, an existing image reference or platform selection. `build="remote"` is required by the wallet SDK and is not inferred from `packaging="container"`. Runtime secrets still travel separately through `settings.runEnvs`, never in the Dockerfile or build context.

For an explicit BSC x402 hosting-payment request, change only `protocol = "mpp"` to `protocol = "x402"` in this example. The BSC USDC token, Permit2 signing policy, bounded approval and spending caps still apply. Deploy handles the `PAYMENT-REQUIRED` challenge and `PAYMENT-SIGNATURE` response; do not route this deployment through the general `bag x402 buy` command. Gateway advertisement and injected-response integration tests cover this option; a real Studio x402 deployment and business invocation still need live acceptance testing.

Studio uses public wallet signing operations, never private-key export. SDK `0.6.0` supports the nested EIP-712 types. BSC payment uses USDC at `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d`, not the U token used for Pieverse/jobs. The wallet needs USDC and, when allowance is insufficient, BNB for gas. `max_approval_gas_wei` explicitly caps a bounded USDC-to-Permit2 approval. Studio signs only chain 56 legacy `approve` transactions to this token and spender, within the approved amount/gas caps; it rejects arbitrary transactions. The approval is available only during an authorized payment (`--pay`, or configured `auto_pay`), not readiness/status. Without that gas option, allowance must already be sufficient.

Run the following from `app/agent`:

```bash
bag deploy wallet --json
bag deploy prepare --provider nodeops
# After the user has authorized deployment and payment within the configured caps:
bag deploy --provider nodeops --yes --pay
bag deploy status --provider nodeops --json
bag deploy verify --provider nodeops --skip-register
```

`--skip-prepare` skips readiness checks only; the fatal storage guard and deploy SDK validation still run. `--force` does not override fatal storage or wallet signing checks. The explicit `--force-deploy-broken-storage` override permits knowingly deploying broken/local storage with a warning; do not add it merely to get a deployment through. `prepare --provider nodeops` selects the cloud provider, not a local runtime named nodeops.

`deploy wallet` is read-only and reports on-chain USDC. `createosCredits: null` means unknown hosting credits, not zero. Funding and hidden credential entry may require the user's terminal/wallet. Base/Arbitrum require their exact USDC domain instead of the BSC Permit2 configuration. With deploy 0.6.6 and SDK 0.6.0, their MPP/x402 credential windows are rejected by the default 600-second wallet policy; treat this as a compatibility blocker and do not relax that policy or switch chains without authorization. `RPC_URL_BSC` overrides the default `https://bsc-dataseed.bnbchain.org`; RPC requests have bounded timeouts and do not retry broadcasts automatically.

`--yes` confirms deployment; `--pay` additionally authorizes payment within the caps. An initial deploy POST may consume existing credits and create a project even without a payment challenge. `use_existing_credits` is the separate choice for credits shared by active projects. `auto_pay=true` additionally requires the approved `pay_to` recipient pin. It automates payment when deployment is invoked; it does not schedule renewal.

Wallet deployments are create-only. Use `status` and `verify` after an acknowledged build failure, timeout or uncertain response; retain `.studio/deployments/nodeops.json` and deploy's durable journal under `~/.bnbagent-deploy/nodeops/payments/`. With deploy 0.6.6, a verified pre-broadcast failure releases the reservation and a retry can resume the same deployment. An ambiguous approval broadcast, a submitted payment, or an old reservation without preparation evidence must remain blocked for reconciliation; missing resource IDs are not proof that payment failed. All callers of a wallet must share one journal for budget aggregation and locking. Do not change names, clear the journal or submit another payment to recover an unknown outcome. Logs, existing-image deployment, named-environment management and in-place updates are not exposed by the current wallet adapter.

## When the user asks to renew

Distinguish hosting renewal from Pieverse LLM-credit replenishment and Altana session expiry. The latter have their own references; neither renews a NodeOps project.

An agent can implement a hosting renewal policy and scheduler. However, this integration has not verified the existing-wallet/project recharge operation or how its result extends the active resource. Public Gateway `/agent/deploy` couples credit purchase with creating a deployment; `months` is a credit price multiplier. Do not invent `bag deploy renew`, treat USDC balance as hosting credits, transfer USDC directly to a quoted recipient, or schedule repeated deployment POSTs as renewal.

For now, inspect recorded status/inventory and report that NodeOps hosting renewal is not executable through Studio. Do not claim auto-renew is enabled. To implement it, first verify a recharge path tied to the existing billing identity, then add budget checks, serialized execution, receipt reconciliation and a scheduler that can still run if the hosted agent stops. This is an integration gap, not evidence that the NodeOps backend cannot renew resources.
