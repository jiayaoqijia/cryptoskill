---
name: review-xss-output-encoding
description: Use when user-controlled data may land in HTML, attributes, or the DOM. Traces sinks and contexts, applies context-aware encoding or a sanitiser for rich text, and verifies with a payload.
---

# Review XSS output encoding

Cross-site scripting is a context bug: the same string is safe in a JS string literal and lethal in
an HTML body. Fix it by encoding at the point of output, matching the encoding to where the value
lands, never by stripping characters on input.

## Procedure

1. Find the DOM sinks that bypass auto-escaping:

       rg -n "dangerouslySetInnerHTML|innerHTML|outerHTML|document\.write|insertAdjacentHTML|v-html" src/
       rg -n "eval\(|new Function\(|setTimeout\(['\"]|location\.href\s*=|\.src\s*=" src/

2. Find the server-side interpolation that does not escape for its context:

       rg -n '\{\{\{ *[a-z]|\| *safe|innerHTML *=' src/ templates/    # Jijia/Django/Handlebars "untrusted"

3. Classify each sink's context — HTML body, attribute value, URL, JS string, CSS — and encode for
   *that* context. HTML-escape `< > & " '`; for a JS string also escape `\` and line terminators; for
   a URL percent-encode.

4. Rely on the framework's auto-escaping and do not defeat it. In React keep text in
   `{value}`; in Django leave `{{ value }}` as-is; in Jinja2 do not add `|safe`.

5. For rich text (comments, markdown, CMS fields), the input is intentionally HTML. Sanitise it
   with a maintained allowlist library rather than a regex:

       # Node
       const clean = DOMPurify.sanitize(dirty, { ALLOWED_TAGS: ['b','i','a','p'], ALLOWED_ATTR: ['href'] });
       # Python
       import bleach
       clean = bleach.clean(dirty, tags=["b","i","a","p"], attributes={"a":["href"]})

6. Set a Content-Security-Policy as defence in depth (`audit-security-response-headers`), accepting
   that CSP is a backstop, not a substitute for encoding.

7. Verify by injecting a payload into every user-controlled field and confirming it renders as text.
   Use a marker that is inert unless it executes:

       value="><img src=x onerror=alert(document.domain)>"

## Pitfalls

- Escaping for HTML but interpolating into a `<script>` block leaves the value in a JS context.
- `\` + `escapeHtml` before building an attribute is often still wrong; encode per context instead.
- DOMPurify defaults allow `href="javascript:..."`; pass a URI policy or allowlist schemes.
- Markdown renderers that allow raw HTML reintroduce XSS; disable raw HTML or sanitise the output.
- Server-side templating that auto-escapes still breaks when a value is put back through `|safe`
  or `{{{ }}}` for "formatting".
- React escapes text but not `href={userUrl}`; `javascript:` in an href still fires.

## Verification

    curl -s "https://app.example.com/?q=%22%3E%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E" \
      | rg -o '<img src=x onerror=alert\(1\)>' && echo "VULNERABLE (raw payload echoed)"

Pass: the payload appears HTML-encoded (`&lt;img ...&gt;`) and never as live markup, and the
sanitiser output contains no event-handler attributes. Report each sink, its context, and the
encoding or sanitiser applied.
