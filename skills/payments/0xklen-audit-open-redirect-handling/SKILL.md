---
name: audit-open-redirect-handling
description: Use when a parameter controls a redirect target, such as next= or returnTo=. Tests protocol-relative, backslash, and javascript: bypasses, and confines targets to relative paths.
---

# Audit open redirect handling

An open redirect turns your trusted domain into a phishing launchpad and can leak OAuth tokens or
session identifiers when the redirect target is a path the app appends data to. The safe rule is to
accept only a relative path on your own origin, never an absolute URL from input.

## Procedure

1. Find redirect sinks driven by a request parameter:

       rg -n "redirect\(|RedirectResponse|res\.redirect|Location:|window\.location|history\.replaceState" src/ \
         | rg -i "next|return|returnTo|redirect|continue|url|goto|target"

2. Identify exactly what the code does with the value: `urlparse`, prefix check, equality against an
   allowlist, or nothing.

3. Probe with the bypass family against staging and record the `Location` header:

       for v in 'https://evil.example' '//evil.example' '/\evil.example' '\\\\evil.example' \
                '/%09/evil.example' 'https:evil.example' 'javascript:alert(1)' 'data:text/html,x'; do \
         echo "== $v"; \
         curl -s -o /dev/null -D - "https://app.example.com/login?next=$v" | rg -i '^location:'; \
       done

4. Fix by accepting a relative path only. Reject anything with a scheme or a network location:

       from urllib.parse import urlparse
       def safe_next(raw, default="/"):
           p = urlparse(raw)
           if p.scheme or p.netloc:            # absolute or protocol-relative
               return default
           if not raw.startswith("/") or raw.startswith("//"):
               return default
           return raw

   Note `//evil.example` parses with `netloc='evil.example'`, so the netloc check already rejects it.

5. Prefer an indirect reference: keep an allowlist map of `?next=settings` → `/account/settings` and
   never echo a raw path. This also blocks chained redirects.

6. Reject backslashes and encoded slash variants; some stacks treat `\` as `/` and `%2f` as a path
   separator. Decode once, then check.

7. Apply the same check when the target is stored (a `return_url` saved in the session) — validate
   at use, not just at save.

## Pitfalls

- A prefix check `target.startswith("https://app.example.com")` accepts
  `https://app.example.com.evil.example`.
- `//evil.example` is protocol-relative and is missed by a check that only looks for `http`.
- `/\evil.example` and `\/evil.example` are treated as absolute by some browsers.
- `javascript:` and `data:` in a client-side `location.href =` render without a network round trip.
- Allowlisting by URL parse but then string-concatenating the raw value reintroduces the hole.
- OAuth `redirect_uri` validation is a stricter, separate control — do not reuse this loose check
  for it.

## Verification

    for v in '//evil.example' 'https://evil.example' '/\evil.example' 'javascript:alert(1)'; do \
      loc=$(curl -s -o /dev/null -D - "https://app.example.com/login?next=$v" | rg -i '^location:'); \
      echo "$v -> $loc"; \
    done

Pass: every `Location` stays on the app origin (or falls back to the default) for all payloads.
Report the redirect parameter, the payloads tested, and the confinement rule applied.
