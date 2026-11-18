---
name: radar-pwa-install
description: >-
  Install DUP Market Radar dashboard as a phone/desktop PWA panel over HTTPS
  or localhost. Use when the user asks for Android install, home-screen
  shortcut, or phone control of radar — not running the server on the phone.
license: MIT
compatibility: Requires running radar HTTP dashboard with /manifest.webmanifest and /sw.js.
metadata:
  author: dup-labs
  version: "0.1.10"
  product: dup-market-radar
---

# Radar PWA install (phone panel)

## When to Use

- «поставь на телефон / PWA / home screen / Android panel»

## Reality check

- Phone = **remote panel** to a PC/VPS radar.
- Server stays on host with KuCoin keys; phone never holds live secrets as the node.

## Steps

1. Radar running (`run_radar.ps1` or Docker).
2. Open dashboard URL that serves `manifest.webmanifest` + `sw.js`.
3. Prefer HTTPS (or localhost) for install prompts.
4. Browser → Install app / Add to Home Screen.
5. Set API key in panel if `RADAR_REQUIRE_API_KEY=1`.
6. Confirm health/snapshot before Auto toggles.

## LAN tip

Use host LAN IP or tunnel; ensure TrustedHost / CORS allow the origin used.

## Refuse

- “Move radar server onto Android” as the supported path.
- Storing exchange secrets in the PWA.
