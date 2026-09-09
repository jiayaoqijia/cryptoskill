---
name: base
description: Base chain ecosystem — Basenames (name.base.eth ENS-style naming) resolution + registration, and Base App / Farcaster Mini App scaffolding (manifest, embed meta tags, validation). Custody-free. Triggers: base name, basename, .base.eth, resolve base name, register basename, base app, mini app, miniapp, farcaster frame, fc:miniapp, MiniKit, OnchainKit, base super app, farcaster.json manifest.
---

# Base Ecosystem skill

Tools for building on Coinbase's Base L2: human-readable names and Mini Apps.

## Basenames (`name.base.eth`)

ENS-style naming on Base. Resolution verified live against Base mainnet.

| Tool | Purpose |
|---|---|
| `chaingpt_base_resolve_name` | Forward (name → address) or reverse (address → primary name). Auto-detects from input. Read-only. |
| `chaingpt_base_name_availability` | Is a label available + the price for N years. Read-only. |
| `chaingpt_base_register_name_tx` | Build the UNSIGNED registration tx (payable; sets the addr record + optional reverse record). Mainnet needs `acknowledgeMainnet:true`. |

`chaingpt_base_resolve_name query=jesse.base.eth` → address. `query=0x…` → name.

## Base App / Farcaster Mini Apps

A Mini App is a web app that runs inside the Base App **and** Farcaster from a
feed post (Farcaster Mini Apps spec; MiniKit wraps OnchainKit on the Base side).
These tools are pure generation/validation — no network, no keys.

| Tool | Purpose |
|---|---|
| `chaingpt_miniapp_manifest` | Generate `/.well-known/farcaster.json` (the `miniapp` object + `frame` alias). |
| `chaingpt_miniapp_embed` | Generate the `fc:miniapp` (+ legacy `fc:frame`) HTML meta tag for shareable embeds. |
| `chaingpt_miniapp_validate` | Validate a manifest against the spec (required fields, lengths, https, category). |

> The manifest's `accountAssociation` (domain-ownership proof) must be signed
> with your Farcaster custody key — generate it with `npx create-onchain --manifest`.
> The tool emits a placeholder and explains the step.

## Reliability

EVM reads use a public-RPC fallback chain. For heavy use set `BASE_RPC_URL` to a
dedicated endpoint. 0 ChainGPT credits.
