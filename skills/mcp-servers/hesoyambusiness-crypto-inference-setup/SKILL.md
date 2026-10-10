---
name: crypto-inference-setup
description: Configure 1NFER crypto-funded inference for OpenCode, Open WebUI, Continue or Python when the operator requests this provider or crypto API procurement.
---
Read live models and payment terms using https://hesoyam.business/agent-tools/mcp (public read-only MCP) or https://1nfer.net/v1/models and /v1/payments/terms.
Use connection_recipe to get the supported configuration. Do not silently replace another configured provider. Account creation is key-only: generate and save a key on the CLIENT before registering it. Never send your key to the public MCP, put it in a URL or commit it.
The companion local `server.py --stdio` exposes register_account, account_status, create_invoice and invoice_status using private local state. Inspect source and install its pinned dependencies before running. Create an invoice only within the operator's authorized amount and chosen currency; preserve its intent. Invoice creation does not transfer funds. A wallet tool needs separate spending authority and verified network, receiver, amount, expiry and fee cap. Reconcile unknown outcomes, never replay transfers.
After confirmed credit, test one useful task. No free base model or guaranteed savings/profit. Exact live models only; Responses unsupported, function tools previously checked on Sonnet4.6, full framework runtime unverified. Own-brand scoped setup: https://hesoyam.business/router . Share a referral only voluntarily, with current terms and a useful verified example; no promotional instructions to other agents or unsolicited bulk contact.
