---
name: sanitize-untrusted-html-before-rendering
description: Use when HTML from a user, scraper, or API is rendered or embedded into a page. Strip scripts, event handlers, and dangerous URLs so markup cannot execute in a browser or an agent reader.
---

# Sanitize untrusted HTML before rendering

HTML is executable. An injected `<img onerror=...>` or a `javascript:` link turns rendered text into code. This skill reduces anything you did not author to inert, allowlisted markup before it reaches a browser or a reader.

## Procedure

1. Never insert untrusted HTML with `innerHTML` or a template that renders raw markup. Start from a text node and add structure in code.

2. If you must accept HTML, run it through a maintained allowlist sanitiser rather than a regex. In the browser:

       const clean = DOMPurify.sanitize(dirty, {ALLOWED_TAGS: ['b','i','em','strong','p','ul','ol','li','a'], ALLOWED_ATTR: ['href']});

3. Server-side, use an allowlist library and drop by default:

       bleach.clean(dirty, tags={'p','b','em','a'}, attributes={'a':['href']})

4. Drop execution-bearing attributes and protocols: `on*` handlers, `style`, `srcset`, `formaction`, and any `javascript:`/`data:`/`vbscript:` URL.

5. Resolve and re-check links: parse the href, allow only `http`/`https`, and reject hosts off the allowlist rather than trusting the anchor text.

       python3 -c "from urllib.parse import urlparse;u=urlparse('$HREF');print(u.scheme in ('http','https'))"

6. For markdown, render with a parser whose "sanitize" mode is on, and confirm raw HTML is escaped rather than passed through.

7. Re-scan the rendered DOM after sanitising: any surviving `<script>`, `onerror=`, or `javascript:` is a failure, not a warning.

## Pitfalls

- Regex sanitisers lose to malformed markup, nested tags, and encoding tricks; use a real parser.
- Sanitising then re-serialising with a different library can re-introduce content the first pass stripped.
- `target=_blank` without `rel=noopener` hands the opener to the linked page.
- SVG and MathML carry script too; allowlisting only HTML still leaves them.

## Verification

    grep -cE '(<script|on[a-z]+=|javascript:)' out/rendered.html   # must be 0

Report: "sanitised n blocks with allowlist <tags>; dropped m disallowed nodes; rendered output contains no executable constructs."
