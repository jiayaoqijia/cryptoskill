---
name: block-exfiltration-via-markdown-image-fetch
description: Use when you render or emit markdown, HTML, or chat messages containing text you did not fully author. Detect and strip remote-image and link fetches that would carry data out in a URL.
---

# Block exfiltration via markdown image fetch

A markdown image whose URL carries a secret leaks it the moment the message renders, because the client fetches it. This skill finds the auto-loading channels and neutralises them before output leaves your hands.

## Procedure

1. Search your intended output for any construct that triggers a fetch: markdown images, HTML `<img>`, iframes, CSS `url()`, and `<link rel=preload>`.

       grep -nE '!\[[^]]*\]\([^)]*\)|<img |url\(|src=' draft.md

2. Parse each URL and look for data appended to it — query strings, path segments, or fragments carrying anything beyond a static asset name:

       grep -oE 'https?://[^) "]+' draft.md | awk -F'[?]' 'NF>1{print $1}'

3. Rewrite remote images to plain text references or inline local ones. Emit the alt text plus the domain so a human can decide, rather than a client fetching blindly.

4. In HTML, forbid auto-fetch with a policy: a CSP of `img-src 'self' data:` blocks remote pixels when your renderer honours it.

5. Decode a suspect URL before trusting the "filename": base64 or hex in the path is the payload.

       printf '%s' "$SEG" | base64 -d 2>/dev/null | head -c 200

6. Strip tracking pixels sized `1x1` and any image whose host is not on the allowlist of legitimate CDNs your content uses.

7. Re-render and re-scan until the output contains no remote fetch, then check the wire once in a test client to confirm no request fires.

## Pitfalls

- A safe-looking `?id=` can be the secret; the client sends it whether or not the server logs it, and DNS leaks the subdomain.
- Pasting into a rich-text editor can re-fetch before your scan runs; sanitise in the data layer first.
- Markdown `[link](url)` is click-triggered, but many previewers prefetch it; treat links as fetch-capable too.
- Alt text and `srcset` are often overlooked and carry the same payload.

## Verification

    grep -cE '!\[[^]]*\]\(https?://|<img ' out/rendered.md   # must be 0 for non-allowlisted hosts

Report: "scanned <file>; remote-fetch constructs n found, n rewritten; remaining hosts <list> all allowlisted."
