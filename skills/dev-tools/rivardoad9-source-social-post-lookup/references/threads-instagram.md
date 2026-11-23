# Threads / Instagram post access (observed 2026-08, plain VM, no login)

Goal: read a threads.net post from an opaque post token.

## What anonymous access looks like (all login-walled)

- `curl -sL -A "<desktop UA>" https://www.threads.net/post/<id>` → HTTP 200
  (threads.net → threads.com redirect) but the body is a JS shell:
  `<title>Threads</title>`, NO og: tags, no canonical, no content strings
  (`"username"`, `"text"` absent), body innerText empty. It is a client-side
  login wall, not a real page.
- `https://www.threads.com/oembed?url=<post-url>` → 301 → `/login/?next=.../oembed/` —
  the oEmbed endpoint is NOT public for posts.
- Anonymous GraphQL: POST `https://www.threads.net/api/graphql` with
  `variables={"postID":"<id>","__relay_internal__pv__IsCreatorsContentRelayParam":false,"__relay_internal__pv__IsM5VideoParam":false}`,
  `doc_id=5587632691339264`, headers `X-IG-App-ID: 238260118697367`,
  `X-FB-LSD: <lsd>`, Referer/Origin, cookies from a prior page GET →
  still returns the login HTML shell, not JSON. Needs a real logged-in
  session. (The LSD token is extractable from the page HTML:
  `"LSD",[],{"token":"..."}`.)
- Wayback `available` API can 429 from a VM — retry once over https with a
  pause, or fall back to the CDX index later.

## The one route that penetrates: Jina Reader (anonymous worked)

```bash
curl -s "https://r.jina.ai/https://www.threads.net/post/<id>" -H "X-Return-Format: markdown"
```

Rendered the page server-side and revealed the TRUE state behind the wall:
Threads' 404 page ("The link's not working or the page is gone"). So a Jina
render distinguishes "post doesn't exist / bad ID" from "login wall" —
validate user-supplied IDs with it before concluding anything. (Anonymous
Jina is unreliable in general and often 401/Turnstile; try it once, then
stop if it 401s.)

## Canonical URL format

Share → Copy link yields `https://www.threads.net/@username/post/<shortcode>`
(short base62-ish code). Long opaque tokens pasted from app share sheets are
a web share-token format and frequently get mangled/truncated in transit —
if the token fails the truncation diagnostic (see SKILL.md), the 404 is
expected; ask for the copied link instead of hammering the API.
