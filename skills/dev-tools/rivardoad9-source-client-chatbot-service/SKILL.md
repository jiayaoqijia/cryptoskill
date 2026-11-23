---
name: client-chatbot-service
description: "Use when building a client chat bot (WA/Telegram)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [chatbot, whatsapp, telegram, umkm, adapters, delivery, automation]
    related_skills: [money-radar, webhook-receivers, lynk-id]
---

# Client Chatbot Service — bangun & kirim bot chat buat klien usaha

Use when: the user asks "bisa bikin bot WA?", wants a Telegram bot for a business, needs an
auto-reply + daily-recap service for an SME client, or is going live for a new client after a deposit.
`money-radar` governs SELLING it (audit call, pricing, deposit gate). This skill governs BUILDING and
DELIVERING it.

## Channel decision — settle this before writing a line of code

| | Telegram | WhatsApp Cloud API (official Meta) |
|---|---|---|
| Where SME customers actually are | No | **Yes** — a warung's customers live in WA |
| Setup cost/time | one @BotFather token, ~2 min | Business Manager + app + dedicated number + token + webhook |
| Needs public HTTPS / domain | **No** (long polling) | **Yes** — Meta requires a valid cert |
| Quick cloudflared tunnel OK? | n/a | **No** — URL rotates on restart, webhook breaks. Needs named tunnel + domain (~Rp150rb/yr) |
| Free-form replies | always | only inside the 24-hour customer-service window; outside it needs an approved template |
| Cost per client | Rp0 | free service-reply quota, then per-reply (verify the current rate before quoting) |
| Role | **demo door** (close the audit) | **product door** (delivery) |

Rule of thumb to state out loud to the user: build the core channel-agnostic, demo on Telegram today,
plug WA only when a client has paid and their own number/assets exist. Never let the channel choice
leak into business logic.

Also mandatory before WA: the number used for the API **cannot** be a number already active in the
regular WhatsApp app — that single constraint is what makes most people give up, so raise it early.

## Architecture that survives client #2 … #10

```
core.py                 one path of business logic; returns DATA, never transport calls
  handle(channel, chat_id, pengirim, teks, msg_id) -> {jenis, balasan[], order, alert_admin}
channels/telegram.py    long polling; injectable send_fn
channels/whatsapp.py    Graph API sender + stdlib http.server webhook; injectable send_fn
store.py                sqlite: orders / pending / alerts / seen
config_usaha.json       ONE file per client: menu, rules, ongkir, minimum, recap time
bot.py                  CLI entry: telegram | wa | recap | export | selftest | pesan | demo
```

- Adapters translate transport ⇄ core and nothing else. A second channel must never require touching core.
- `handle()` returns a list of replies plus an optional owner alert — the adapter decides how to deliver.
- New client = copy the config JSON and edit it. If a new client needs code, the config boundary is wrong.
- Recap must be a CLI verb that sends via the API itself and prints **nothing** on success (cron silence;
  otherwise `deliver=origin` double-sends the same message).

## Testing: write the harness before the channel is live

The harness is cheap and it is the difference between a demo that closes and a demo that loses the order
in front of the client. Two real bugs were found by the harness in this exact build, both invisible in a
happy-path demo: (a) any later message swallowed a half-finished order, (b) adding a menu item overwrote
the items already collected.

Harness rules:
1. **Set the DB env var BEFORE importing the store module** — the path is read at import time, so
   `os.environ["X_DB"] = tempfile…; import store` in that order, or the test writes to production.
2. Drive the adapters with a **fake `send_fn`** so the whole path (payload → parse → core → reply) is
   asserted with zero network.
3. Always include: FAQ path, partial order → pending, identity continuation → logged with correct total,
   ongkir free-threshold, minimum-order note, added-item merge, duplicate inbound id, unknown message →
   owner alert, recap numbers, and a real provider payload (Meta webhook JSON and a Telegram update dict).
4. Assert numbers, not vibes (`total == 64000`, `qty == 3`), and print PASS/FAIL per scenario with the
   offending value. Exit non-zero on failure.

## State-machine pitfalls (order chat is never one message)

1. **Never guard on "items empty".** A continuation message fills items from pending, so an
   `if not items` guard is dead code. Guard on facts about THIS message: did it bring a new menu?
   did it carry name/address?
2. **Merge, never overwrite.** "tambah 1 es jeruk" must add to the pending order, not replace it.
3. **Dedupe inbound message ids.** WA retries webhook deliveries; without a `seen` table the same
   order is logged twice. Telegram rarely retries but the guard is free.
4. **Answer the WA webhook with HTTP 200 fast**, regardless of processing outcome, or Meta retries forever.
5. **One bad message must not kill the loop** — per-update try/except in polling; per-request try/except
   in the webhook handler.
6. **Markdown/formatting fallback**: retry the send as plain text when the provider rejects the parse
   mode — customer text routinely breaks it.
7. Pending state needs a TTL (~60 min); an abandoned half-order must not resurrect hours later.

## n8n vs a small Python service (answer this once, honestly)

n8n is fine for prototypes and for the user's internal automation (push recap to Sheets, notify them).
For a service sold to clients it loses on three counts: another process to keep alive with logic outside
git, no real test harness (node-by-node UI clicking), and state management that needs an extra DB/Redis.
Plus per-execution pricing on the cloud tier — every customer message is one execution. Recommend Python
for the customer path, n8n as glue.

## Go-live checklist per client (realistically 1–2 hours after deposit)

1. Demo bot (Telegram) live → run the 30-minute audit with 20 real chats from the client's own customers.
2. Transcribe the client's 20 most frequent questions into their config JSON (rules + menu).
3. Client-facing channel: their Business Manager, their app, **their** dedicated number, their token —
   assets in the client's name, or you own a liability.
4. Put the long-running process under systemd; never nohup from a shell.
5. Cron the recap verb at the client's closing time; verify silence on success.
6. Train one human at the client: how to read the recap, where the CSV/Sheet lives, when to answer manually.

## Pitfalls

- **Don't wire the client-facing channel before a deposit exists** — this is the `money-radar` gate. A
  direct user instruction ("bikin bot WA-nya") is executed: build it channel-agnostic, leave WA behind
  missing credentials, and say plainly that credentials come after the deposit.
- Never use unofficial WA gateways (Fonnte/Wablas) on a client's main number — the ban risk lands on the
  client, and that is your fault.
- Don't sell vocabulary ("AI agent") to an SME; sell the outcome (chat kejawab, rekap tiap jam 9 malam).
  When asked, say honestly which part is rules and which part is a model.
- Don't add a dashboard/login/multi-user for client #1. The config file and the CSV are the product.
- Quote provider prices (per-reply rates, free quotas) only after verifying them in the same session —
  numbers copied from a project README are a snapshot, not a commitment.

## Files

- `references/rapel-sistem-2026-10.md` — the live Sistem Rapel build on this server: file layout,
  exact commands, harness coverage, per-client config workflow, and the Meta/WA go-live detail.
