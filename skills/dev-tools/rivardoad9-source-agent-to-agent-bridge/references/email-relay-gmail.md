# Email relay over Gmail (working structure)

Verified shape of a bridge between Hermes and a partner agent that has its own address. Gmail scopes
needed: `gmail.readonly`, `gmail.modify`, `gmail.send`, `gmail.settings.basic`.

## Token handling

Read `~/.hermes/google_token.json`; if `expires_at` has passed, POST to `https://oauth2.googleapis.com/token`
with `grant_type=refresh_token`, the client id/secret, and the stored refresh token, then write the new
access token and `expires_at` back. Never print the token or key material into chat.

## Inbound search

```
GET /gmail/v1/users/me/messages?q=from:<addr> newer_than:7d&maxResults=20
GET /gmail/v1/users/me/messages/{id}?format=full
```

Extract the first `text/plain` part by walking `payload.parts`; cut quoted history at
`On ... wrote:` / `-----Original Message`. Keep a `seen` list of message ids plus `baseline_ms` captured at
install, and only process messages whose `internalDate >= baseline_ms`.

## Reply in the same thread

`POST /gmail/v1/users/me/messages/send` with `{"raw": base64url(MIME), "threadId": <inbound threadId>}` and
headers `To`, `From`, `Subject` (`Re:` prefix once), `In-Reply-To` and `References` set to the inbound
`Message-ID`. For attachments:

```python
m = MIMEMultipart("mixed")
m.attach(MIMEText(text, "plain", "utf-8"))
part = MIMEBase(maintype, subtype)
part.set_payload(open(path, "rb").read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", "attachment", filename=os.path.basename(path))
m.attach(part)
```

## Keeping it silent

Create the label once (`POST /gmail/v1/users/me/labels`), then two filters:

```json
{"criteria": {"from": "<addr>"}, "action": {"addLabelIds": ["<label>"], "removeLabelIds": ["INBOX", "UNREAD"]}}
{"criteria": {"to":   "<addr>"}, "action": {"addLabelIds": ["<label>"], "removeLabelIds": ["INBOX", "UNREAD"]}}
```

`GET /gmail/v1/users/me/settings/filters` first to avoid duplicates. Backfill the existing thread with
`POST /messages/{id}/modify` using the same label add and INBOX/UNREAD removal.

## Cron

```text
name: <agent> bridge — check email every 10 minutes
no_agent: true
script: agent_bridge.py
schedule: every 10 minutes
deliver: local            # nothing reaches chat on a normal run
failure_deliver: origin   # a broken bridge must surface
```

The script prints only when it handled a message; empty stdout sends nothing at all.

## Block list used before the agent turn

```python
BLOCK_RE = re.compile(r"""(?ix)
\brm\s+-[rf] | \bhapus(kan)?\b | \btimpa\b | \bmkfs\b | \bdd\s+if= | \bshutdown\b |
\bdrop\s+(table|database)\b | \btruncate\s+table\b | \bdelete\s+from\b |
\.env\b | private[ _-]?key | api[ _-]?key | secret | password | passwd | credential |
access[ _-]?token | refresh[ _-]?token | ssh[ _-]?key | \bseed\s+phrase\b |
\bgit\s+push\s+(-f|--force) | \bgit\s+reset\s+--hard | \bchmod\s+777 |
\bcurl[^\n|]*\|\s*(ba)?sh | \bwget[^\n|]*\|\s*(ba)?sh | \bwithdraw\b | \btransfer\s+funds\b
""")
```

Verify with paired examples before trusting it: benign task text must pass, credential and delete text
must block. Match on Indonesian and English verbs — the partner agent mirrors the user's language.
