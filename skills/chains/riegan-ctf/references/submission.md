# Flag submission (CTFd, rCTF)

Always behind the router's remote gate. Prefer API over browser — scriptable, retryable,
and avoids burning attempts on typos.

## Detect the platform

- CTFd: page footer/source mentions `CTFd`, URLs like `/challenges`, `/scoreboard`.
- rCTF: URLs like `/chals`, React app by redpwn.
- Others (Hackazon, custom): fall back to manual submission by the user.

## CTFd (API token: Settings → Access Tokens → Generate)

```bash
BASE=https://<event-domain>
TOKEN=<api-token>

# list challenges: id, name, category, value, solve count
curl -s -H "Authorization: Token $TOKEN" -H 'Content-Type: application/json' \
     "$BASE/api/v1/challenges" | jq '.data[] | {id,name,category,value,solves}'

# optional: read one challenge's description/hints/tags/files
curl -s -H "Authorization: Token $TOKEN" "$BASE/api/v1/challenges/<id>" | jq .data

# submit a flag (response .data.status: "correct" | "incorrect" | "already_solved")
curl -s -X POST -H "Authorization: Token $TOKEN" -H 'Content-Type: application/json' \
     -d '{"challenge_id": <id>, "submission": "flag{...}"}' \
     "$BASE/api/v1/challenges/attempt" | jq .data.status
```

Rate limits and per-challenge attempt caps exist: check rules before brute-guessing.
Never lock out teammates by spamming submissions.

## rCTF (auth token from browser session: `Authorization: Bearer < authToken >`)

```bash
BASE=https://<event-domain>
AUTH=<auth-token-from-browser>

# list challenges
curl -s -H "Authorization: Bearer $AUTH" "$BASE/api/v1/challs" | jq '.data[] | {id,name,category,points}'

# submit (known userId; check response .data.correct — true/false)
curl -s -X POST -H "Authorization: Bearer $AUTH" -H 'Content-Type: application/json' \
     -H "Accept: application/json" \
     -d "{\"submission\":\"flag{...}\",\"challengeId\":\"<id>\",\"userId\":\"<uid>\"}" \
     "$BASE/api/v1/challs/<id>/submit" | jq .data
```

rCTF submissions are rate-limited globally (wrong flags cost the whole team for a
cooldown window) — submit only high-confidence flags.

## Hygiene

- Trim whitespace/newlines from flags; preserve case exactly as found.
- Re-derive the flag from the artifact if submission says "incorrect" before retrying.
- Log outcome (correct/incorrect/already_solved) in `work/<event>/flags.md`.
