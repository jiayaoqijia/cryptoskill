---
name: rails-security
description: Audits Ruby on Rails applications for framework-specific vulnerabilities — SQL injection via interpolated where/order/find_by_sql, mass assignment through params.permit!, XSS via raw/html_safe/<%==, CSRF skips (protect_from_forgery absent, skip_before_action), missing authenticate/authorize before_actions, send_file/IO path traversal, open redirects via redirect_to(params), Marshal/Oj unsafe deserialization, send/public_send with params, committed secret_key_base, and force_ssl disabled. Use when the project has a Gemfile with rails or app/controllers.
license: MIT
---

# Rails Security

## Step 0 — Detect

```bash
rg -n "^\s*gem ['\"]rails" -g 'Gemfile'
ls app/controllers config 2>/dev/null
```

Record Rails version (Gemfile.lock), auth stack (Devise/etc.), deployment hints.

## Step 1 — SQL injection

```bash
rg -n "where\([\"'].*#\{|order\(params|find_by_sql|group\(params|pluck\(params|select\(params" app/
```

- `where("name = '#{params[:name]}'")` → Critical
- `order(params[:sort])` / `pluck(params[:col])` — column names can't be bound → High (allowlist required)
- Safe counterparts: `where(name: params[:name])`, `where("name = ?", ...)` → note as positives

## Step 2 — Mass assignment

```bash
rg -n "permit!|params\[:user\]$|\.update_attributes" app/
```

- `params.permit!` (or raw params hash) into `new`/`update` on models with role columns (`admin`, `role`, `credits`) → Critical
- Narrow `permit(:name, :email)` → safe; check listed columns for role leakage

## Step 3 — XSS

```bash
rg -n "<%= raw |\.html_safe|<%==" app/ app/views/
```

- `raw`/`html_safe`/`<%==` on user-derived values → High (ERB `<%= %>` escapes by default)

## Step 4 — CSRF & authz

```bash
rg -n "protect_from_forgery" app/controllers/application_controller.rb
rg -n "skip_before_action :verify_authenticity|skip_forgery_protection" app/
rg -n "before_action :authenticate|before_action :authorize" app/controllers/ | head
```

- No `protect_from_forgery` in ApplicationController (and Rails new-app default absent in API mode with cookie sessions) → High
- `skip_before_action :verify_authenticity_token` on non-webhook controllers → High
- Controllers with mutations but no `authenticate_*!` before_action → High
- Devise `current_user` absent + `Model.find(params[:id])` in show/edit → IDOR, High

## Step 5 — Files, redirects, dispatch

```bash
rg -n "send_file|File\.read|IO\.foreach|File\.open" app/
rg -n "redirect_to\s+(params|request\.referer)" app/
rg -n "\bsend\(|public_send\(" app/ | rg "params" | head
```

- `send_file(params[:path])` → traversal, High
- `render file: params[:path]` → arbitrary file read (CVE-2019-5418 pattern — Action View reads and returns the file); fixed rails versions still make this a design bug → High
- `render file:` with a first-party literal (`Rails.root.join(...)`) is fine
- `redirect_to(params[:return_to])` → open redirect (phishing/SSRF in OAuth flows), Medium/High
- `send(params[:method])` → arbitrary method dispatch, High

## Step 6 — Deserialization & config

```bash
rg -n "Marshal\.load|Oj\.load|YAML\.load\(" app/ config/
rg -n "secret_key_base" config/ -g '!*.lock' | head
rg -n "force_ssl" config/environments/
```

- `Marshal.load` / `Oj.load(mode: :object)` / `YAML.load` (non-safe) on external data → Critical
- `secret_key_base` committed in secrets.yml/initializers → Critical (session forgery)
- `config.force_ssl = false` in production.rb → Medium

## Reporting

Severity table above; fixes are idiomatic one-liners (`where(hash:)`, permit lists, `redirect_to` allowlist). Note strong-params/ORM positives. Dependency CVEs via `../dependency-vulns/SKILL.md`.
