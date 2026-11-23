---
name: social-post-lookup
description: "Resolve social post tokens/links and verify they exist."
---

# Social Post Lookup

Use when: the user pastes a share token / post ID / link ("ini thread gw", "cek post ini") and wants it identified or read. Goal: turn the opaque token into a canonical URL, verify the post exists, and extract what content is reachable without login.

## General method

1. Identify the platform from the token/URL shape (short base62 code vs long opaque base64url token; host).
2. Build the canonical URL and probe cheaply: `curl -sL -A "<desktop UA>" <url>` and inspect `<title>`, og: tags, canonical link, redirect target.
3. A JS-shell response (generic `<title>`, no og:/canonical, empty body innerText) = client-side login wall, NOT a real page. Do not conclude "not found" from it.
4. Distinguish real states with a server-side rendering route (per-platform notes): the renderer can surface the true 404 page behind the wall.
5. Check the token itself for truncation before blaming the site (below).

## Truncation diagnostic (base64url tokens)

Opaque platform tokens (Threads share tokens, etc.) are base64url. If `len(token) % 4 == 1`, the token is IMPOSSIBLE for base64 (stripped-padding base64 is 0/2/3 mod 4) — the paste is truncated. Stop probing; ask for the canonical share link (Share → Copy link).

## Per-platform notes

- **Threads / Instagram**: `references/threads-instagram.md` — anonymous access reality, the probe ladder, and the one renderer that penetrates the login wall.
