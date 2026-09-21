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
  - `Referrer-Policy`, `Permissions-Policy` → LOW
- **TLS**: `ssl_protocols` still includes TLSv1/TLSv1.1 → HIGH; self-signed or expired certs referenced → HIGH; HTTP→HTTPS redirect missing → MEDIUM
- **Cookies**: flags `HttpOnly`, `Secure`, `SameSite` on auth/session cookies (details in `../auth-review/SKILL.md`)

## 3 — CORS

```bash
rg -n -i "access-control-allow-origin|cors\(|allow_origins|origin.*\*"
```
- `Access-Control-Allow-Origin: *` **combined with** `Allow-Credentials: true` → impossible per spec; if framework silently reflects origin instead → **CRITICAL** (any site reads authenticated data)
- Origin reflection/echo of `Origin` header or regex like `https?://.*\.example.com` (matches `evilexample.com` — missing anchored dot) → HIGH
- Wildcard without credentials → LOW/MEDIUM (still enumerates data)

## 4 — Debug & exposure

```bash
rg -n -i "debug\s*=\s*true|debug\s*:\s*true|app\.debug|debug_mode"
rg -n -i "traceback|stack.?trace|display_errors\s*=\s*on|show_exceptions"
```
- Django `DEBUG=True` / Flask `debug=True` / Laravel `APP_DEBUG=true` in prod-looking config → HIGH (stack traces, env leaks, Werkzeug debugger = RCE)
- Verbose error responses leaking SQL, paths, versions → MEDIUM
- Default creds in configs (`admin/admin`, `postgres/postgres` in docker-compose) → HIGH in prod context, LOW in clearly-local compose
- Exposed sensitive files: `.git/` served, `.env` in webroot, `*.bak`, `.DS_Store`, `dump.sql`, `phpinfo()` pages → HIGH
- Admin/health/debug endpoints (`/actuator/*` with env/heapdump, `/debug`, `/admin`) without auth → CRITICAL (Spring env/heapdump leaks credentials)

## 5 — CI/CD pipelines (supply chain)

```bash
rg -n "pull_request_target|secrets\.|curl.*\|\s*(ba)?sh|sudo|GITHUB_TOKEN|persist-credentials" .github/workflows/ 2>/dev/null
```
- `pull_request_target` + checkout of PR head + secrets usage → **CRITICAL** (fork PRs run with base repo secrets)
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

## Reporting

Table of config → issue → severity → exact config change. Config findings are usually cheap fixes; order the fix list by severity then by effort (these often come first after secrets).
