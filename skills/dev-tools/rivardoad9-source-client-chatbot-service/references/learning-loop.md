# Loop belajar: chat gagal jadi aturan baru (retention feature)

Files: `~/rapel-usaha/learn.py` + `bot.py usul`. Documented for the user in `RENCANA-BOT.md`.
This is the part that stops a bot from being a one-shot delivery: every chat the bot could not
answer becomes a rule, so the config keeps growing from the CLIENT's own traffic. Sell it as
"makin lama makin banyak yang kejawab", not as "AI".

## Commands

```bash
python3 bot.py usul --demo        # 14 canned unanswered chats, temp DB, production untouched
python3 bot.py usul               # from the real alerts table of a client
python3 bot.py usul --apply       # write config_usaha.json (backup first) + mark alerts handled
python3 bot.py usul --tanpa-llm   # fallback path when the LLM API is down -> placeholder drafts
```

Flow: unanswered chats (`store.alerts_open()`) → cluster → LLM drafts `{kunci, balasan}` → print for
owner approval → `--apply` writes the config and marks those alerts handled.

## Design rules (each one bought with a defect)

1. **Cluster with the overlap coefficient, not Jaccard** (threshold ≈0.6). SME chats are short and
   wildly uneven in length; Jaccard never groups two phrasings of the same question. Overlap
   coefficient makes "20 customers asking the same thing" collapse into ONE proposal.
2. **Bind proposals to clusters by an explicit group number, never `zip()`.** Asked to echo
   `"grup": 2`, the model's output order can shift; zipping silently attaches a proposal to the wrong
   example chats. Clusters the model skipped get a raw fallback draft instead of being dropped.
3. **Validate every proposed trigger key against that cluster's real chats** — drop any trigger whose
   core words never appear in them. Otherwise the model invents a plausible-sounding phrase the
   customers never type, i.e. a rule that can never fire.
4. **Prompt-level anti-hallucination, verbatim in the prompt:** never invent price, hours, or stock;
   if only the owner knows the answer the draft must say it will be checked with admin. Verified:
   "terima gopay ga kak" produced "untuk pembayaran pakai GoPay akan kami cek dulu ke admin", NOT an
   invented "bisa kak". A bot that invents an answer costs the client money and costs you the client.
5. **`--apply` must be reversible and atomic-ish:** copy `config_usaha.json` to `.bak-<YYYYMMDD-HHMM>`
   before writing, and only mark the alerts handled after the write succeeds. Re-running must not
   double-add rules.
6. **Prove `--apply` in a sandbox copy first** (`cp -r ~/rapel-usaha /tmp/rapel_apply_test`, point
   `RAPEL_DB` inside it), then assert the production config's rule count is unchanged.
7. **Keep the runtime rules-first.** Deterministic rules answer the bulk (instant, free, identical
   every time); the model's job is DRAFTING new rules offline, not answering every message live.
8. **LLM credentials come from the existing env files** (`~/flowmetrix-ai-agent/.env`,
   `~/.hermes/.env` — `DEEPSEEK_*`), never hardcoded, never echoed. `--tanpa-llm` keeps the feature
   usable when the API is unreachable or the key is absent.

## Evidence to quote to a client (10 Okt 2026)

14 unanswered chats → 6 clusters → 6 proposals → `--apply` → config 20 → 26 rules, backup written,
14 alerts marked handled → the same chats then answered by the new rules (gopay → cek admin,
kirim Bekasi → area check, catering 50 porsi → admin). Run the loop in front of the owner during the
audit: watching their own unanswered chats turn into automatic answers is the closing moment.
