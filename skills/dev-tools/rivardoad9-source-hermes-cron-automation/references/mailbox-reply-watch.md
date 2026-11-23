# Watching a mailbox for a reply (no Google SDK, no OAuth dance per run)

Pattern for "tell me when <company> approves my request / sends the key / replies". Shape: `no_agent`
cron running a stdlib script that refreshes an existing OAuth token, lists matching messages, diffs
against a state file, and prints only new ones.

## Credentials

A previously authorized user token lives at `~/.hermes/google_token.json` and already contains
`refresh_token`, `client_id`, `client_secret`, `token_uri` (the same file `gmail_autofile.py` and the
Gmail filter scripts use). Refresh it yourself — `googleapiclient` is not guaranteed under
`/usr/bin/python3`:

```python
POST <token_uri>  grant_type=refresh_token&client_id=..&client_secret=..&refresh_token=..
-> {"access_token": ...}          # then Authorization: Bearer <access_token>
```

Never re-run the consent flow from a cron job; if the refresh token is revoked the job should say so in
one line rather than dying with a traceback (that line is also the only failure signal the user gets).

## Query

Keep the Gmail-side `q` narrow and the local filter looser:

```
newer_than:30d ((from:vendor.com) OR (subject:"API key") OR (subject:"API access"))
```

Then require the word you care about (`vendor`, `api key`) to appear across From + Subject + body before
formatting — this stops a subject-only match from firing on unrelated mail.

## Rules that make it safe

| Concern | Rule |
|---|---|
| First run | Missing/`seeded: false` state → store current ids and print **nothing**. Never mail the user their own backlog. |
| Dedupe | Keep the last ~300 message ids; alert once per id regardless of how many ticks overlap. |
| Secrets in the body | If the reply contains a key, write it to a dedicated file (`chmod 600`) and print only "disimpan di <path>". Never echo it to chat — the transcript is a log. |
| Envelope details | Report From, Subject, WIB timestamp and a short snippet: enough to judge without opening Gmail. |
| Subject drift | Vendors reply from a personal address with `Re: whatever`; a `from:`+`subject:` query will miss it. Tell the user this limit up front and widen the query when they name the sender. |
| Cadence | Every 3h is cheap and still feels prompt for approval mail; a daily sweep reads as neglect. |

## Test before trusting silence

A `--test` flag that fetches the newest message in the mailbox through the same header/snippet render
path proves token refresh + parsing + formatting in one call, without touching state and without
faking a vendor mail. Then run for real: empty output plus `seeded: true` in the state file is the pass.

## Working instance

- `~/.hermes/scripts/element_api_watch.py` — Element marketplace API-key reply watcher, every 3h,
  `no_agent`, `deliver=origin`; state `~/.hermes/data/element_api_watch.json`; extracted key to
  `~/.hermes/element_api_key.txt`.
