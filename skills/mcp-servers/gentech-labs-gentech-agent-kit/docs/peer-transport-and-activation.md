# Agent Activation & Peer Transport — GenTech Agent Kit

The vault handoff is the **durable record**; `hermes peer dm` is the **live wake-up**
that spawns a real, synchronous turn in the target agent and returns its reply.
This is the active-memory layer: an agent only runs when there's something to do,
on a fresh session, and the reply proves it acted.

## Fleet wiring (Sep 9, 2026)

```
hermes -p <profile> peer add <target> --url http://127.0.0.1:<port> --key <API_SERVER_KEY>
hermes -p gentech peer dm gizmo "Pick up the open handoff at <path> — <task>"
```

**Per-profile distinct ports** (all gateways share one host and collide on the
default 8642):
- gentech = 8642
- gentech-treasury = 8643
- gizmo = 8644
- pixel = 8645

**Per profile** you need, in `.env` + `config.yaml`:
- `API_SERVER_KEY` (min 16 chars; the platform refuses to start without a usable key)
- `gateway.api_server.key` and `gateway.api_server.port` in config.yaml

Peer auth keys land in `~/.hermes/.env` as `HERMES_PEER_<NAME>_KEY`.

**To bring up the api_server platform:** set the key (+ port), then RESTART that
gateway from a separate shell OUTSIDE the gateway process (the gateway SIGTERMs
its children). A prepped script lives at `/root/scripts/fleet-gateway-restart.sh`.

## Bot Chat bloat — why a peer DM can fail

A peer DM targets the target's canonical **"Bot Chat"** session. That session
does NOT auto-reset and can balloon past the compressible context ceiling
(`Context length exceeded (272,884 tokens). Cannot compress further.`). We hit
this live: one profile's Bot Chat had 35M cumulative input tokens.

**Fix** — archive + rename the bloated Bot Chat so the next peer DM creates a fresh one:
```bash
hermes -p <profile> sessions rename <bot-chat-id> "__archived-bot-chat"
hermes -p <profile> sessions archive --title "__archived-bot-chat" --yes
```
Recoverable — nothing deleted.

**Prevention:** the daily gateway restart (6:25 AM ET) now clears ALL 4 profiles'
sessions, so Bot Chats are reset regularly instead of only gentech's.

## Delivery semantics

When a wake trigger both peer-DMs and uses cron `deliver: bot-chat:<profile>`,
you get double delivery. With peer DM live, set the cron job's `deliver` to
`local` — the peer DM is the sole live wake-up; `local` captures the reply to log.
