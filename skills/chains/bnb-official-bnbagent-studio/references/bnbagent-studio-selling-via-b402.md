---
name: bnbagent-studio-selling-via-b402
description: When the user wants a bnbagent-studio agent to sell paid or FREE HTTP requests through the B402-backed x402 rail. Owns the explicit pricing choice and, for PAID mode, per-agent merchant onboarding, RSA key preparation, egress-IP allowlisting, sandbox/production separation, B402 environment setup, seller status checks, and activation by redeploy (managed platform, self-hosted AgentCore, or self-hosted Azure Foundry).
---

> **Reference file** of the `bnbagent-studio` router skill, installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# Sell via B402

Use this playbook to activate the x402 seller rail for one agent. First choose PAID or FREE explicitly. B402 merchant credentials are per agent and per environment and are needed only for PAID. Never reuse a merchant record across agent wallets, or mix sandbox and production values.

## Preconditions

- The agent wallet already exists. In PAID mode its address receives the actual selected active token: Mainnet U/USD1/USDC/USDT or Testnet U/USDC/USDT. Testnet does not support USD1.
- The project targets the managed platform or a self-hosted AgentCore/Azure Foundry runtime. PAID self-hosted targets still require the documented envelope-v1 ingress and fixed-egress B402 path; platform/backend capability and deployment readiness must pass before activation.
- PAID managed platform only: an interactive GitHub-login session from `bag platform login` is available for reading the platform Relay egress IPs. A `bnbk_…` CI token does not satisfy this endpoint's GitHub-user check.
- `[payments.b402_seller]` exists. If not, run `bag x402 sell init`.

The PAID application uses the **agent wallet address**, not a developer treasury, buyer wallet, or platform wallet.

## Choose PAID or FREE

Use one of these explicit boundaries:

```bash
bag init <name> --rails b402 --seller-price-usd 0
bag x402 sell init --price-usd 0
bag config set payments.seller.price_usd 0
```

`"0"` means anonymous FREE passthrough. The runtime returns work directly and does not issue a 402 challenge, call B402 `/supported`/verify/settle, transfer a token, or write an `x402_sell` settlement audit. B402 credentials are ignored and not synchronized. Run `bag x402 sell status`, `bag doctor`, and `bag deploy prepare`; all must label the route FREE.

This is unrestricted public access. Confirm that intent before continuing. Managed platform still publishes the route through its gateway; self-hosted AgentCore and Azure Foundry deploys still need an envelope-v1 front. If FREE is the selected product, skip the merchant/RSA/IP sections below.

## Generate the agent's RSA material

This playbook is the canonical key-generation procedure; neither the CLI nor the B402 SDK generates keys. The pair authenticates every facilitator API call under the [B402 request-signing scheme](https://developers.binance.com/en/docs/products/onchainpay-x402/basics/3.request-signing); the runtime signs each request automatically once the credentials are stored.

Work from the workspace root. Keep private material under `.studio/`, which is excluded from source and deploy artifacts. Generate a separate key pair for each environment:

```bash
umask 077
b402_env=sandbox
mkdir -p ".studio/b402/$b402_env"
openssl genpkey -algorithm RSA \
  -out ".studio/b402/$b402_env/private.pem" \
  -pkeyopt rsa_keygen_bits:1024
openssl pkey -in ".studio/b402/$b402_env/private.pem" -pubout \
  -out ".studio/b402/$b402_env/public.pem"
openssl pkey -in ".studio/b402/$b402_env/private.pem" -pubout -outform DER |
  openssl base64 -A > ".studio/b402/$b402_env/public.der.b64"
openssl pkcs8 -topk8 -nocrypt \
  -in ".studio/b402/$b402_env/private.pem" -outform DER |
  openssl base64 -A > ".studio/b402/$b402_env/private.der.b64"
chmod 600 ".studio/b402/$b402_env/private.pem" \
  ".studio/b402/$b402_env/private.der.b64"
```

Do not print the private key or its base64 form. Submit only the public key material to B402.

The current B402 request-signing contract explicitly requires a 1024-bit RSA key and RSA-SHA256. Follow that protocol requirement even if a larger RSA key would normally be preferred elsewhere. Repeat with `b402_env=production` instead of reusing the sandbox pair.

## Collect the IP allowlist

B402 allowlists the merchant's **outbound** (egress) IPs, the addresses the agent's facilitator calls come FROM. Submit every part that applies to your deployment target:

1. **Platform Relay egress IPs (managed-platform deploys)**: the addresses that the platform B402 Relay uses to reach the facilitator. The managed deployment worker points the runtime copy of `B402_BASE_URL` at this Relay on both managed backends (AgentCore and Azure Foundry). Refresh and read the interactive session without printing its bearer:

   ```bash
   bag platform whoami >/dev/null
   platform_session="$HOME/.bnbagent-deploy/bnb/session.json"
   platform_access_token="$(jq -er '.access_token' "$platform_session")"
   platform_api_url="$(jq -er '.apiUrl' "$platform_session")"
   curl -H "Authorization: Bearer $platform_access_token" \
     "$platform_api_url/v1/b402/whitelist-ips"
   unset platform_access_token
   # → {"whitelist_ips": ["13.115.15.190", …], "cache_ttl_seconds": 300}
   ```

   Submit every address in `whitelist_ips`. The list is served with a short cache TTL and can rotate, so re-read it right before submitting the form. The login session is stored mode `0600`. Do not echo, log, or paste its access or refresh token. `bnbk_` tokens from `bag platform token` are deliberately rejected by this GitHub-login-only endpoint.

2. **Your local public IP**: required so a local `bag dev` run can reach B402:

   ```bash
   curl ipinfo.io/ip
   ```

3. **Self-hosted AgentCore egress (self-deploys)**: operate a restricted B402 Relay on a host with a fixed public egress IP, such as a user-managed VPS, and submit that IP. Set the runtime `B402_BASE_URL` to the Relay base URL. The Relay exposes only `supported`, `verify`, and `settle`, fixes the upstream facilitator, and forwards the signed body and Tesla header allowlist without holding the merchant private key or automatically retrying a settlement transport failure. Review the public [BNB Agent Studio deployment guide](https://docs.bnbchain.org/developer-kit/bnbchain-studio/deployment/) for provider constraints and supported front-door patterns.

   As an alternative, use AWS-supported AgentCore VPC mode with a private subnet, NAT Gateway, and Elastic IP. Submit the Elastic IP and keep `B402_BASE_URL` pointed at the facilitator. Studio does not deploy or manage that AWS network.

4. **Self-hosted Azure Foundry egress (self-deploys)**: Foundry hosted-agent containers have floating egress just like AgentCore, so the agent must NOT call the facilitator directly. Run the envelope gateway on a Container Apps workload-profiles environment whose subnet has a NAT Gateway with a Standard static public IP, co-host a restricted B402 forwarder there (the AWS guide's Relay example works verbatim — the NAT Gateway replaces its fixed-IP host requirement), point the runtime `B402_BASE_URL` at that forwarder, and submit the NAT Gateway IP. The environment type and VNet cannot be changed after creation. Review the public [BNB Agent Studio deployment guide](https://docs.bnbchain.org/developer-kit/bnbchain-studio/deployment/) for provider constraints and supported front-door patterns. Studio does not deploy or manage that Azure network.

Do not add the public inbound gateway IP, a transient build-runner IP, or guessed addresses. If the whitelist endpoint is unreachable, stop onboarding and confirm the platform environment with the operator.

## Submit the B402 merchant application

Apply through the [B402 developer account application](https://developers.binance.com/en/docs/products/onchainpay-x402/basics/6.apply-developer-account). Complete one application for sandbox and a separate application for production. Fill the form as follows:

| Field | Value |
| --- | --- |
| Business Name | Your agent or business display name |
| Email | Primary contact email address |
| Wallet address | The agent wallet for that environment |
| Public key | The contents of `.studio/b402/<environment>/public.der.b64` |
| IP allowlist | For managed deploys (both backends), every platform Relay IP from `/v1/b402/whitelist-ips`; for self-hosted AgentCore, the user's Relay or VPC NAT Elastic IP; for self-hosted Azure Foundry, the ACA NAT Gateway static IP; add the local public IP when `bag dev` must reach B402 directly |
| Webhook callback URL | Supply only when the integration uses callbacks |

Keep the two environments isolated:

| Environment | Chain       | Credentials     | Wallet/IP registration |
| ----------- | ----------- | --------------- | ---------------------- |
| Sandbox     | BSC testnet | sandbox-only    | apply separately       |
| Production  | BSC mainnet | production-only | apply separately       |

## Store the issued credentials

Open the workspace `.studio/.env.local` in an editor and fill exactly four values:

```dotenv
B402_BASE_URL=
B402_CLIENT_ID=
B402_ACCESS_TOKEN=
B402_PRIVATE_KEY_B64=
```

Copy the single-line DER value from `.studio/b402/<environment>/private.der.b64` into `B402_PRIVATE_KEY_B64`. `B402_BASE_URL`, `B402_CLIENT_ID`, and `B402_ACCESS_TOKEN` are the values issued together for that environment. Do not include any value in shell history, terminal output, source files, TOML, screenshots, or support tickets.

`B402_PRIVATE_KEY` accepts the PEM representation as an alternative. Keep exactly one private-key form; do not set both.

For the current managed BSC Testnet path, the platform-supported upstream is `https://qacb.sdtaop.com`; the worker projects only the AgentCore runtime copy to its Relay. For a generic self-hosted environment, use the authenticated base URL issued during onboarding. With your own Relay, set the runtime `B402_BASE_URL` to that Relay base URL and configure the Relay's fixed upstream to the issued URL.

## Verify and activate

For PAID mode, check names and presence without exposing values:

```bash
bag x402 sell status --no-probe
```

When the credentials, IP allowlist, and facilitator environment are ready, run the authenticated read-only capability check:

```bash
bag x402 sell status
```

For a sandbox/trial agent, the capability snapshot must use exact `eip155:97`; B402 `TEST_U` is `0x330949Aed7d00FCe0558C64ED6FeC9792616cC39` with 6 decimals and EIP-3009-only, while `TEST_USDC`/`TEST_USDT` may activate Permit2 Exact. For production it must find exact `eip155:56`. A network mismatch is not safe to ignore. A failed probe produces a timestamped dormant snapshot rather than reusing guessed methods.

`ACTIVE` on this snapshot means the facilitator will settle that asset × method for the route you publish. It is a statement about your **seller** face, not about which buyer can pay it — the buyers of your routes are third-party x402 clients. Studio's own buyer covers these routes unevenly: `evm-local` and `turnkey` sign EIP-3009 only, `twak` is fail-closed for paid x402, and `altana` is the one wallet kind that pays `permit2-exact`, once `bag wallet session x402-setup` has armed that asset's Permit2 allowance. So a testnet USDC/USDT route is correctly `ACTIVE` even while `bag x402 buy --asset USDC` from a local wallet against your own agent is refused: that is the buyer wallet's signing boundary, not a dead route.

Run the deployment gate, then redeploy to activate the selected mode:

```bash
bag deploy prepare
bag deploy --provider bnb                   # managed platform, recipe backend
bag deploy --provider bnb --backend azure   # managed Azure, explicit non-TTY confirmation
bag deploy --provider aws                   # self-hosted AgentCore
bag deploy --provider azure                 # self-hosted Azure Foundry
```

When readiness succeeds, a managed-platform deploy summary reports `x402 rail is ACTIVE` (or `ACTIVE in FREE mode`) and prints the anonymous `/x402` URL. A self-hosted AgentCore or Azure Foundry summary uses the corresponding self-hosted label: the rail runs in-process, but there is no anonymous URL. Operate the documented envelope-v1 front for that runtime. The default Bag self-deploy uses Cognito OAuth over raw HTTPS; AWS SDK/SigV4 is only for a runtime deliberately configured with IAM authorization; PAID also needs a fixed-egress B402 Relay or equivalent network path. Review the public [BNB Agent Studio deployment guide](https://docs.bnbchain.org/developer-kit/bnbchain-studio/deployment/) for supported provider and front-door patterns. A dormant or forced-dormant summary means the rail was not activated; fix the named credential, runtime, network, or tunnel condition and redeploy. These are implemented status/readiness semantics, not a claim that a live deployment or payment has been verified.

## Hard rules

- Never log or print any B402 value or private key.
- Never put a B402 value in `studio.toml` or a deploy descriptor.
- Never replay a paid HTTP request whose outcome is unknown. Follow `docs/guides/x402-selling.md` and reconcile `(nonce, network, payer)` first.
- Binance `/settle` is asynchronous. A parseable `success: false` response with a transaction is pending and requires an idempotent poll with the same settlement payload. Studio with `@bnb-chain/b402@0.2.1` does not yet perform that poll; it classifies pending as unknown. Version 0.2.1 separately guards credential replays through an atomic store. Do not claim current mainnet readiness until polling is implemented.
- Settlement happens before work. A later work failure retains the payment and does not trigger an automatic refund.
- AgentCore and Azure Foundry targets are supported in managed-platform and self-hosted modes when their capability/readiness checks pass. Self-hosted targets have no anonymous URL and need an operator-run envelope-v1 front. This support statement does not claim that a particular live deployment or payment succeeded.
- Every supported `wallet.kind` can be the PAID B402 payout wallet: `evm-local`, `twak`, `turnkey`, and `altana`. The payout lands at the configured `pay_to` or, by default, `[wallet].address`; for altana that address is the admin EOA (EIP-7702 — the smart account address equals the admin address), so the locally-held admin keystore can always move the revenue. Register the B402 merchant credentials for that exact address. FREE x402 bypasses B402 and has no payout.
- Buyer compatibility is per network/asset/method: Mainnet USD1 is `0x8d0D000Ee44948FC98c9B98A4FA4921476f08B0d`, 18 decimals, EIP-3009-only with domain `World Liberty Financial USD / 1`; it has no Permit2 route and its Commerce/facilitator live verification remains a release gate. Mainnet U may use EIP-3009 and Permit2 Exact; Testnet `TEST_U` uses `0x330949Aed7d00FCe0558C64ED6FeC9792616cC39`, 6 decimals, and EIP-3009 only; USDC/USDT use Permit2 Exact. Testnet does not support USD1. `permit2-upto` is never active. Altana Permit2 payment requires the atomic `requestExact` boundary and bounded canonical-Permit2 allowance; local/Turnkey Permit2 and TWAK paid x402 remain deferred. Status reports snapshot facts only and does not prove a live chain payment.
- Never describe FREE as a zero-value B402 settlement. It bypasses B402.
