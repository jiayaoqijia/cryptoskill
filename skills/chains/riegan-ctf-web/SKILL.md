---
name: ctf-web
description: Use when a challenge is a web application: a URL or host:port to attack, a login form, an admin bot, a source zip or Dockerfile for a website; when the user mentions SQLi, XSS, SSTI, LFI/RFI, XXE, SSRF, deserialization, JWT or session tokens, IDOR, CSRF, GraphQL, file upload, cookie stealing, CORS or CSP, request smuggling; or when a flag should be extracted from a website, and for white-box source review of challenge web apps.
---

# CTF web — map the app, pick the bug class, deliver

Workspace layout, remote gate, flag logging: sibling skill `ctf`. **All live testing
against remote targets is gated by the router's rules** — mirror locally whenever the
challenge ships source (`php -S 127.0.0.1:8000`, `python3 -m http.server 8000`,
`scripts/ctf python app.py`, or `podman` for provided Dockerfiles/images; details in
`references/tooling.md`). Craft and verify payloads on the mirror, replay the final
exploit remotely once approved.

## Triage — map the app (first 10 minutes)

1. Record in `notes.md`: entry URL, ports, stack guess, auth model, whether an admin
   bot exists, whether source was provided.
2. Answer the map questions:

| Question | How |
|---|---|
| Stack / language? | headers (`Server`, `X-Powered-By`), cookie names (`PHPSESSID`/`JSESSIONID`/`laravel_session`/`connect.sid`), 404 page — `references/recon.md` |
| Routes? | robots/sitemap, JS bundles, wayback, ffuf — `references/recon.md` |
| Hidden params? | `scripts/ctf arjun -u URL -m GET` |
| Session mechanism? | cookie flags, JWT? → `scripts/jwt-inspect.py "$TOKEN"` |
| Admin bot? | client-side challenge: `references/client.md` (exfil section first) |
| Source available? | switch to Playbook → source-audit flow |

3. Low-hanging fruit sweep (minutes, wins events):

| Check | Payoff |
|---|---|
| `/.git/HEAD`, `.env`, `backup.zip`, `.bak`/`~`/`.swp` files | full source / secrets |
| `/robots.txt`, `/sitemap.xml`, wayback CDX | hidden endpoints |
| `/swagger`, `/openapi.json`, `/graphql` introspection | complete API surface |
| `/server-status`, `/actuator/env`, `/phpmyadmin`, `/adminer.php` | config or DB leak |
| default creds (`admin:admin` ...) | instant login — `references/auth.md` |
| JWT in any header/cookie | none / weak secret / confusion — `references/auth.md` |
| `package.json`, `.js.map` source maps | hidden routes, versions |

One command runs probes + fuzzing: `skills/ctf-web/scripts/dirquick.sh -e .php,.bak -v http://target:port`
(remote gate applies; run it against local mirrors freely).

4. If the flag format appears in any response, log it per the router, keep going for
   the intended path anyway (organizers often plant decoys).

## Playbook

### Flow A — source-audit (source zip / Dockerfile given)

1. Identify language + framework from deps (`package.json`, `composer.json`,
   `requirements.txt`, `pom.xml`, `go.mod`). Find the router/controllers: every
   endpoint with its params, and every middleware (auth, body parsing).
2. Grep the sinks, then trace each hit back to user input:

| Language | Grep sink list |
|---|---|
| PHP | `unserialize\(`, `include`, `require`, `eval\(`, `assert\(`, `system\(`, `shell_exec\(`, `passthru\(`, `exec\(`, `popen\(`, `proc_open`, `preg_replace` with `/e`, backticks, `move_uploaded_file\(`, `simplexml_load_string\(`, `DOMDocument->load`, `curl_exec\(`, `md5\(`+`==`, `extract\(`, `header('Location` |
| Python | `pickle`, `yaml.load`, `eval\(`, `exec\(`, `os.system`, `subprocess`, `render_template_string`, `requests.get(` with user URL, f-string/format SQL, `jinja2.Environment` |
| Node | `child_process`, `exec`, `execSync`, `spawn`, `eval\(`, `new Function`, `serialize`, deep `merge`/`extend`/`_.set` (proto pollution), `res.redirect(`, `jwt.verify`, `Object.assign` |
| Java | `readObject`, `ObjectInputStream`, `Runtime.getRuntime`, `ProcessBuilder`, `SpelExpressionParser`, `Velocity`, `Statement`/`executeQuery` with concat, `<%=`, JSP EL `${}`, `XMLDecoder` |
| Any | SQL built by concatenation/`${}`; `==` vs `===`; `jwt.decode` (not verify); `Crypto` with `aes-128-ecb`; `random` for tokens |

3. Match sink to bug class table (below), build the payload against a local mirror,
   then fire at the remote target (gated).
4. No obvious sink? Audit business logic: register/login flows, IDOR on every
   object reference, race-prone endpoints (balance/coupon/vote), mass assignment.

### Flow B — blackbox (no source)

1. Recon sweep (`references/recon.md`): fingerprint, exposed files, dirs, vhosts,
   param mining, wayback.
2. Injection probes on every input point, one class at a time — error/boolean/time
   triage in `references/injection.md`.
3. Auth surface: default creds, JWT/session weaknesses, OAuth flow, IDOR/mass
   assignment — `references/auth.md`.
4. File/URL surfaces: uploads, `?file=` params, importers (SSRF) — `references/deser-files.md`.
5. Admin bot / browser-only behavior: `references/client.md`.
6. Escalate breadth (deeper wordlists, more params) and depth (chain two bugs:
   LFI+log poison, open redirect+OAuth, XSS+CSRF) before concluding.

### Bug class index

| Bug class | Preconditions | Reference |
|---|---|---|
| SQLi (manual + sqlmap), NoSQL, command injection, SSTI, XSLT, LDAP | any user input reaching a query/parser/shell/template | `references/injection.md` |
| JWT/session/OAuth/IDOR/mass assignment/race/CSRF/default creds | any auth or object reference | `references/auth.md` |
| Deserialization (PHP/Python/Java/Ruby/YAML/Node), LFI/RFI, php://filter chain, log poisoning, upload bypasses, XXE, SSRF | user data unserialized / included / fetched | `references/deser-files.md` |
| XSS + admin bot, CSP bypass, prototype pollution, postMessage, CORS, smuggling, cache poisoning, open redirect | client-side render or bot | `references/client.md` |
| Recon: fingerprint, ffuf, exposed source, vhosts, wayback, param mining | always first (Flow B) | `references/recon.md` |
| Proxies (mitmproxy/Burp), browsers, websockets, listeners, local mirrors | tooling for all of the above | `references/tooling.md` |

## References

- `references/recon.md` — manual Wappalyzer-style fingerprinting, quick exposed-file
  probes, git-dumper, source maps, Swagger/GraphQL introspection, ffuf patterns
  (extensions/recursion/multi-wordlist/vhost), wayback CDX, arjun.
- `references/injection.md` — SQLi triage + UNION method + sqlmap, NoSQL `$ne`/`$regex`/
  `$where`, command injection channels, SSTI engine decision tree + per-engine RCE
  payloads, SpEL/OGNL/EL, XSLT, LDAP.
- `references/auth.md` — JWT attack table (none/crack/RS→HS confusion/kid/jku/x5u),
  session bugs, OAuth flows, IDOR methodology, mass assignment, races, CSRF,
  default creds, register/login logic flaws.
- `references/deser-files.md` — PHP/Python/Java/Ruby/YAML/Node deserialization,
  phar, LFI path list + wrappers, php://filter chain RCE, log/session poisoning,
  upload bypass table, XXE, SSRF (ports, cloud metadata, gopher, rebinding), SVG XSS.
- `references/client.md` — XSS contexts + exfil listeners (HTTP/WebSocket, HttpOnly
  workaround), CSP bypass table, prototype pollution (client + Node RCE gadget),
  postMessage, CORS, request smuggling basics, cache poisoning, open redirect.
- `references/tooling.md` — mitmproxy scripting, Burp install, sqlmap via proxy,
  ffuf modes, websocat, interactsh, local mirrors, workspace hygiene.

## Scripts in this skill

| Script | Purpose |
|---|---|
| `scripts/dirquick.sh` | one-shot recon: header dump, exposed-file probes, ffuf content (+ optional vhost); falls back to a bundled wordlist without seclists |
| `scripts/jwt-inspect.py` | JWT decode + suspicious-flag triage + optional HMAC wordlist crack (stdlib only) |

## Toolbox

| Tool | Install | Purpose |
|---|---|---|
| `ffuf` | `paru -S ffuf` (AUR) or https://github.com/ffuf/ffuf/releases | content/vhost/param fuzzing |
| `seclists` | `paru -S seclists` (AUR; → `/usr/share/seclists`) or clone github.com/danielmiessler/SecLists | wordlists |
| `sqlmap` | `sudo pacman -S sqlmap` | automated SQL injection |
| `mitmproxy` | `sudo pacman -S mitmproxy` | scriptable intercepting proxy |
| Burp Suite | `paru -S burpsuite` (AUR) or upstream community jar | manual proxy, Repeater/Intruder, races |
| `websocat` | `sudo pacman -S websocat` | websocket client + listener |
| `httpie` | `sudo pacman -S httpie` | ergonomic HTTP client |
| `hashcat` | `sudo pacman -S hashcat` | `-m 16500` JWT secret cracking |
| `php` | `sudo pacman -S php` | local mirrors, phar/phpggc payload crafting |
| `git-dumper` | `uv tool install git-dumper` | recover exposed `.git/` |
| `arjun` | `uv pip install --python .venv/bin/python arjun` | hidden parameter discovery |
| `jwt_tool` | clone github.com/ticarpi/jwt_tool + `uv pip install --python .venv/bin/python pycryptodomex` | JWT forgery/attack suite |
| `tplmap` | clone github.com/epinna/tplmap | SSTI detection + auto-RCE |
| `ysoserial` | clone github.com/frohoff/ysoserial + `mvn package` | Java deserialization payloads |
| `phpggc` | clone github.com/ambionics/phpggc | PHP gadget chains (Laravel...) |
| `php_filter_chain_generator` | clone github.com/synacktiv/php_filter_chain_generator | php://filter → RCE chain |
| `Gopherus` | clone github.com/tarunkant/Gopherus | gopher:// SSRF payloads |
| `interactsh-client` | `go install -v github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest` | out-of-band callback host |
| browser tool | built into this agent (skill `agent-browser`) | interactive apps, login flows, bot debugging |

Report files to the user with the flag; log to `work/<event>/flags.md` per the router.
