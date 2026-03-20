---
name: dagny-nostr-nak
description: Manage Nostr posting and engagement via the nak CLI. Use for creating notes, replying in threads, tagging npubs, checking replies/mentions, monitoring a relay (default wss://relay.primal.net), and publishing events with correct root/reply tags. Requires access to NOSTR_SECRET_KEY (nsec) for signing/publishing.
---

# Nostr (nak)

## Overview
Use `nak` for all Nostr actions: publish notes, reply in threads, and query relays for replies/mentions. Default relay: `wss://relay.primal.net` unless the user specifies another.

## Install / Update nak
- **Repo**: https://github.com/fiatjaf/nak
- **Install** (script): `curl -sSL https://raw.githubusercontent.com/fiatjaf/nak/master/install.sh | sh`
- **Update**: re-run the install script above (it installs latest)
- **Tip**: review the script before running if you want to audit what it does.

## Onboarding (keys)
- **Generate a new key**: `nak key generate` (prints nsec + npub)
- **Save the secret**: store `NOSTR_SECRET_KEY` in a shell profile or a local `.env` with restricted permissions.
  - Example: `export NOSTR_SECRET_KEY="nsec1..."`
  - Optional: `chmod 600 .env` if you store it locally.
  - Prefer env vars over inline `--sec` in commands.

## Quick Start (common tasks)
- **Post a note**: `nak event -k 1 --sec $NOSTR_SECRET_KEY -c "..." <relay>`
- **Reply to a note**: include `root` and `reply` tags (see below)
- **Check replies**: `nak req -k 1 -e <event_id> -l <N> <relay>`
- **Check mentions**: `nak req -k 1 -p <your_pubkey_hex> -l <N> <relay>`

## Workflow: Posting & Replies

### 1) Create a new note
- Build content.
- Publish:
  ```bash
  nak event -k 1 --sec $NOSTR_SECRET_KEY -c "<content>" wss://relay.primal.net
  ```

### 2) Reply to a reply (correct threading)
Always include both `root` and `reply` tags so clients display it as a reply:

- `root` = original top‑level note id
- `reply` = the specific note you’re replying to

Use `-t e="<id>;<relay>;root"` and `-t e="<id>;<relay>;reply"`.

Example:
```bash
nak event -k 1 --sec $NOSTR_SECRET_KEY \
  -t e="<root_id>;wss://relay.primal.net;root" \
  -t e="<reply_id>;wss://relay.primal.net;reply" \
  -p <other_pubkey_hex> \
  -c "<reply content>" \
  wss://relay.primal.net
```

### 3) Check for replies to a note
```bash
nak req -k 1 -e <root_id> -l 20 wss://relay.primal.net
```

### 4) Check mentions of your pubkey
```bash
nak req -k 1 -p <your_pubkey_hex> -l 20 wss://relay.primal.net
```

## Conventions
- Default relay: `wss://relay.primal.net`
- Prefer `NOSTR_SECRET_KEY` env var instead of inline `--sec`.
- When tagging users, include `-p <npub/hex>`.
- For human-facing links, encode with `nak encode nevent ...` and format as `https://primal.net/e/<nevent>`.

## References
- Use `nak event --help` and `nak req --help` for flag details.
