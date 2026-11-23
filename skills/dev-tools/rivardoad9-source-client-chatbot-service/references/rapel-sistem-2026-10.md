# Sistem Rapel — build state & go-live detail (per 10 Okt 2026)

Live on this server at `~/rapel-usaha/`. Productised SME service: chat pelanggan kejawab otomatis +
rekap harian ke pemilik. Selling side lives in `money-radar`; this file is the build/delivery record.

## Layout

```
bot.py             CLI: telegram | wa | recap | export | selftest | pesan | demo
core.py            handle(channel, chat_id, pengirim, teks, msg_id) -> {jenis, balasan[], order, alert_admin}
store.py           sqlite: orders / pending / alerts / seen   (RAPEL_DB env, read AT IMPORT)
cfg.py             .env loader (does not override existing env)
engine.py          v0 rules core: 20 auto-reply rules, alias-based order parsing, ongkir/minimal, recap
channels/telegram.py   long polling; handle_update(token, owner_chat_id, update, send_fn=None)
channels/whatsapp.py   parse_inbound() + handle_payload() + Graph API send + stdlib webhook server
config_usaha.json  ONE file per client: menu (aliases+prices), rules, ongkir, minimal_order, fallback
tests/selftest.py  25 assertions, temp DB, zero network
RENCANA-BOT.md     tool requirements, costs, n8n verdict, go-live checklist
.env.example       TELEGRAM_* / WA_* / RAPEL_CHANNEL / RAPEL_DB
```

## Commands

```bash
cd ~/rapel-usaha
python3 bot.py selftest     # 25/25, temp DB via RAPEL_DB set before imports; production untouched
python3 bot.py demo         # v0 prop: 15 chats -> 100% answered, 4 orders, 21:00 recap
python3 bot.py telegram     # needs TELEGRAM_BOT_TOKEN + TELEGRAM_OWNER_CHAT_ID
python3 bot.py wa           # needs WA_ACCESS_TOKEN / WA_PHONE_NUMBER_ID / WA_VERIFY_TOKEN
python3 bot.py recap        # sends to owner itself, prints NOTHING on success (safe for cron)
python3 bot.py export       # CSV of today's orders (shape ready for a Sheets layer)
```

## Harness coverage (25 assertions)

FAQ answered · partial order → pending asks name+address · continuation logs order with correct total ·
pending cleared after logging · one-message complete order · address parsing · pending + unrelated
question answered without dropping the order · added item merged (not overwritten) · unknown message →
owner alert row · ongkir free above threshold · minimum-order note · duplicate inbound msg_id → no double
order · recap counts + rupiah + "butuh admin" line · real Meta webhook payload end-to-end with fake
sender · Telegram update end-to-end with fake sender · owner `/rekap` command.

Two bugs this harness caught before any client saw the code (both were shipping in the first draft):
the pending-continuation refill made an `if not items` guard dead (so a stray question could consume the
half-order), and a new menu item replaced previously collected items instead of merging.

## Status / what is deliberately not wired

- Telegram: code complete, **waiting on the BotFather token** (owner action, ~2 min). Then message the
  bot once and read `chat.id` from `getUpdates` for `TELEGRAM_OWNER_CHAT_ID`.
- WhatsApp: code complete (webhook + sender), **no credentials by design** — Meta assets are created in
  the CLIENT's name after a deposit. Nothing to do until there is a paying client.
- No systemd unit and no recap cron created yet, on purpose: they get created at go-live, per client.
  Recap cron pattern: `no_agent` job running `python3 bot.py recap` at the client's closing time
  (script sends itself → empty stdout → no duplicate delivery).

## Meta / WhatsApp go-live detail

1. Client's Business Manager → app (Business type) → add the WhatsApp product.
2. Dedicated number for the API; a number already active in the regular WhatsApp app cannot be used.
3. System User token (permanent) + `WA_PHONE_NUMBER_ID` + WABA id → `.env`.
4. Webhook: needs a stable HTTPS URL with a valid cert → domain (~Rp150rb/yr) + cloudflared **named**
   tunnel. Quick tunnels are rejected in practice because the URL changes on every restart.
5. `GET` verify: `hub.mode=subscribe` + `hub.verify_token` → echo `hub.challenge`.
   `POST`: parse `entry[].changes[].value.messages[]`, answer HTTP 200 immediately.
6. Inside the 24-hour customer-service window free-form text is allowed. The 21:00 owner recap goes to
   the owner's own number, which also chats daily — otherwise it needs an approved template.

## Per-client workflow

Copy `config_usaha.json` → fill `menu` (with `alias`) + `aturan` (20 frequent questions) → point
`RAPEL_DB` at a per-client sqlite file → demo on Telegram during the audit → after the deposit, wire the
client's own WA number and credentials → systemd + recap cron → train one human at the client.

## Adapter skeleton (the reusable pattern)

```python
# channels/<provider>.py
def parse_inbound(payload): ...            # transport payload -> [{chat_id, pengirim, teks, msg_id}]
def send(chat_id, text) -> bool: ...       # transport send; return success, never raise
def handle_payload(payload, owner_id, send_fn=None):
    send_fn = send_fn or send              # injectable => tests need no network
    for m in parse_inbound(payload):
        h = core.handle(CHANNEL, m["chat_id"], m["pengirim"], m["teks"], msg_id=m["msg_id"])
        if h.get("duplikat"): continue     # provider retried the same delivery
        for b in h["balasan"]: send_fn(m["chat_id"], b)
        if h.get("alert_admin") and owner_id: send_fn(owner_id, h["alert_admin"])
```
