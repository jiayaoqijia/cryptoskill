---
name: bnbagent-studio-use-bnb-trial
description: Use when deploying or operating a bnbagent-studio seller on the BNB Chain managed 48h testnet trial, including GitHub device login, trial eligibility/expiry, staging verification, status, logs, verify, and destroy.
---

> **Reference file** of the `bnbagent-studio` router skill. Load it only for provider `bnb` deployment work.

# Use the BNB Chain 48h trial

Treat this provider as a temporary testnet sandbox. Require a throwaway wallet, keep `bsc-testnet`, and explain that the runtime signing material is transmitted to the operator's managed secret store for the trial. Never use a mainnet key. Exception: `wallet.kind='altana'` ships only the bounded, budget-limited, revocable session - the throwaway-wallet advice does not apply; tighten the session instead (`bag wallet session grant --force --budget-u <small> --expiry-days <short>`) and never run `bag wallet new` on an altana project (it breaks the session's `[wallet].address` anchor).

All auth and cloud lifecycle work must cross the pinned `@bnbagent/deploy-cli@0.6.6` boundary. Do not call a cloud CLI or platform REST routes directly. The managed backend is recipe-derived: `agentcore` uses AWS; `azure-foundry` uses Azure. For headless managed Azure, confirm with `bag deploy --provider bnb --backend azure --yes`; never treat `--backend` as a cross-cloud recipe converter.

## Select and authenticate

Run:

```bash
bag platform login
bag platform credit
bag deploy prepare --provider bnb --backend aws
bag deploy --provider bnb
```

For an `azure-foundry` recipe, use
`bag deploy prepare --provider bnb --backend azure` followed by
`bag deploy --provider bnb --backend azure --yes`. The explicit Platform
prepare target must accept `[storage].kind='local'`: the API supplies managed
S3/Blob storage and Studio must not require or forward BYOS credentials.

`bag platform login` must print the GitHub verification URL and device code. It must not open a browser. Give both values to the user and wait for them to complete verification.

Before offering BNB, inspect the trial result:

- `available`: selectable; explain that the 48h clock starts on first success.
- `active`: selectable; show remaining time and expiry immediately.
- `expired`: show the row and expiry, but mark it unavailable and do not select it. AWS remains independently available when compatible with the project scaffold.
- unknown/auth required: explain that eligibility cannot be confirmed until login; the delegated deploy rechecks before building.

Every deploy/redeploy uses scheme C. Never silently reuse `[deploy].destination` or the last provider. A sole active BNB record may produce an explicit “update BNB” action. Switching to another compatible provider creates a coexisting deployment; it does not destroy BNB automatically.

Automation requires `--provider bnb --yes`. When another provider remains active, also require `--allow-multiple`.

## Operate

```bash
bag deploy status
bag deploy logs --provider bnb
bag deploy verify --provider bnb
bag deploy destroy --provider bnb           # dry-run
bag deploy destroy --provider bnb --execute # destructive confirmation
```

`status` lists every recorded provider and includes the live trial countdown. Use `--no-probe` only when local records are desired. With multiple deployments, logs/verify/destroy must select a provider interactively or pass `--provider`.

Destroy clears the BNB lifecycle record after the delegated delete succeeds. The Agent's managed deliverables share that lifecycle: deletion removes them and their `bnbagent-api` URLs eventually return 404. It does not delete the local keystore or the on-chain ERC-8004 identity. Destroyed BNB slugs are retired; choose a fresh slug before redeploy.

## Manual staging verification

Use the staging endpoint only for the current shell:

```bash
export BNBAGENT_API_URL=https://bnbagent-api-staging.bnbchain.world
bag platform login
bag platform credit
bag deploy --provider bnb
bag deploy status --provider bnb
bag deploy logs --provider bnb
bag deploy verify --provider bnb --skip-register
bag deploy destroy --provider bnb
```

Do not execute the final destructive step until the user explicitly approves `bag deploy destroy --provider bnb --execute`. For headless verification, use `BNBAGENT_API_TOKEN`, `BNBAGENT_API_URL`, `--provider bnb`, and `--yes`.

Treat both artifact channels as required release coverage. The 2026-07-20 staging baseline passed ZIP and linux/arm64 container through deploy, status, OAuth-authenticated signed A2A negotiation, logs, and destroy. Do not infer funded delivery or durable-storage coverage from that smoke; those require the separate commerce flow in `docs/guides/verification.md`.
