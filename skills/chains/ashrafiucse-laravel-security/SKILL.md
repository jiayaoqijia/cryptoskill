---
name: laravel-security
description: Audits Laravel (PHP) applications for framework-specific vulnerabilities — mass assignment via missing fillable/guarded, SQL injection through DB::raw/whereRaw/orderByRaw concatenation, Blade raw output XSS, CSRF middleware exclusions, committed APP_KEY enabling cookie-forgery RCE chains, APP_DEBUG in production, routes without auth middleware, path traversal in file downloads, and dev tools (debugbar/telescope) in production dependencies. Use when the project has composer.json with laravel/framework, an artisan file, app/Models, or Blade views.
license: MIT
---

# Laravel Security

## Step 0 — Detect

```bash
rg -n "laravel/framework" -g 'composer.json' ; ls artisan app routes config 2>/dev/null
```

Record Laravel version (composer.json/lock), PHP version, and whether Sanctum/Passport/Fortify are in use.

## Step 1 — Config & env (the Laravel RCE chain)

```bash
git ls-files | rg -i '(^|/)\.env($|\.)'
rg -n "APP_DEBUG\s*=\s*true|APP_ENV\s*=\s*production" -g '.env*'
rg -n "APP_KEY" -g '.env*' -g 'config/app.php' | head -3
```

- **Committed `.env` / `APP_KEY`** → **Critical**: leaked APP_KEY lets attackers forge encrypted cookies; with older serializable-cookie sessions or queued-job payloads this chains to RCE via PHP deserialization gadgets. Fix: rotate APP_KEY (`php artisan key:generate`), purge from history, treat all session data as compromised.
- `APP_DEBUG=true` with `APP_ENV=production` → High (stack traces; historically .env disclosure via error pages).
- `config/session.php`: `secure`/`http_only` false → Medium; `same_site` null → Medium.

## Step 2 — Mass assignment (privilege escalation)

```bash
rg -n "fillable|guarded" app/Models/ | head
rg -n "::create\(|::update\(|forceFill|unguard" app/ routes/ | head -20
rg -n "Model::unguard\(true\)|ShouldAutoSize" app/Providers/ 2>/dev/null
```

For each model feeding `::create/update` with request data:
- No `$fillable`/`$guarded` (both default open-ish; `$guarded=[]` explicitly wide) + `$request->all()`/`$request->validated()` including role-ish columns (`is_admin`, `role`, `user_id`, `price`) → **Critical** (attacker self-promotes by adding `is_admin=1` to the POST).
- `Model::unguard()` globally → same finding, repo-wide.
- Fix: explicit `$fillable` allowlist + `$request->only([...])` / typed FormRequests.

## Step 3 — SQL injection

```bash
rg -n "DB::raw|whereRaw|orderByRaw|selectRaw|havingRaw|DB::select\(|DB::statement\(" app/ routes/
```

- Raw expressions with concatenation/interpolation of request data → Critical
- Query builder with bindings (`where('name', $req->name)`) → safe, note as positive
- `orderBy($request->input('sort'))` — column names can't be bound; must be allowlisted → Medium/High

## Step 4 — Blade XSS

```bash
rg -n '\{!!' -g '*.blade.php' .
rg -n '\{!!' -g '*.blade.php' . | wc -l   # census FIRST: know the full inventory size
```

**Census, don't sample.** Glob to `*.blade.php` — the bare pattern also matches React/TSX `aria-invalid={!!…}` noise that crowds out real hits. Run `wc -l` before reading: every raw echo in the inventory gets an explicit disposition (verified-safe / finding / not-assessed). `head`-truncating this list is how review-moderation XSS ships to production. For repos >50 hits, triage by author privilege first (below), but never leave the tail unexamined.

Every `{!! !!}` with a variable that traces to user input is a finding — then triage by **privilege direction**, which sets the severity:

| Author of the raw content | Viewer of the page | Severity |
|---|---|---|
| Unprivileged (student/customer/guest form: reviews, tickets, messages, submission text, uploaded filenames) | Privileged (admin/moderator/staff) | **Critical** — fires in the staff origin → session-riding requests → account takeover. Moderation queues guarantee a privileged viewer opens it. |
| Privileged (admin/instructor-authored: descriptions, embeds, templates) | Unprivileged/everyone | High (public) / Medium (authenticated) |
| Same privilege | same | Medium |

Blade's `{{ }}` escapes; `{!! !!}` exists only to bypass. `nl2br()` is NOT an escape — `{!! nl2br($x) !!}` is a raw echo. Check `{{ $x }}` + `|raw`? (Blade has no `|raw`; Twig confusion = false positive).

## Step 5 — CSRF

```bash
rg -n "except" app/Http/Middleware/VerifyCsrfToken.php bootstrap/app.php 2>/dev/null
rg -n "withoutMiddleware|WithoutMiddleware" app/ routes/
```

- `$except` with `'*'` → High; with real routes → verify the handler is genuinely webhook-only (state-changing → High)
- Laravel 11+: `validateCsrfTokens(except: [...))` in `bootstrap/app.php`

## Step 6 — Authorization

```bash
rg -n "middleware\(" routes/ | head -20
rg -n "Gate::before|Gate::define|policy|authorize\(" app/ | head -20
```

- State-changing/admin routes without `auth` middleware → High
- `Gate::before(fn () => true)` unconditional allow → Critical
- Policies existing but not auto-discovered + no `authorize()` calls in controllers → flag as "authz unmapped" (Medium, needs verification)

## Step 7 — Files, uploads, misc

```bash
rg -n "response\(\)->download|Storage::(download|get|put)|\->store\(" app/
rg -n "debugbar|telescope|ignition" composer.json composer.lock 2>/dev/null
rg -n "eval\(|unserialize\(|assert\(" app/
```

- `download(storage_path('app/' . $request->input(...)))` → path traversal, High
- Uploads without `validated()` mimes/size rules stored on public disk → Medium/High
- debugbar/telescope in require (not require-dev) → Medium
- `unserialize` on user data → Critical (with APP_KEY leak = full RCE chain, cross-reference Step 1)

## Step 8 — Feature flags & outbound-email amplification

Plan-constrained tenants are authenticated ADMINS whose capability should be plan-gated — menu-level hiding is cosmetic. (Incident class, 2026-09-23 user report: one trial tenant blasted 1200+ emails in ~2 minutes via an ungated compose route + global-default import flag.) The attacker persona is an admin the PLAN should stop, not one auth should stop.

```bash
# flag census: every define + its default, then every use site
rg -n "Feature::(define|active|for)" app/ modules/ config/
# which routes actually carry the feature middleware
rg -n "feature:" routes/ modules/ routes/ app/ 2>/dev/null
# email-triggering endpoints and their throttles
rg -n "Route::(get|post)" routes/ modules/ routes/ | rg -i "send-|verif|subscribe|reset"
rg -n "throttle:" routes/ modules/ routes/
# blast fan-out: jobs that load unbounded sets and send per row
rg -n "::query\(\)->get\(\)|::all\(\)" app/ modules/
rg -n "Mail::to\(|Mail::send\(" app/ modules/
# pennant store + whether deploys purge stored values
rg -n "'store'" config/pennant.php
rg -n "pennant:purge" deploy/ scripts/
```

- **Flag gated in UI only** — flag checked in Blade/menu or inside the JOB, but its routes lack `->middleware('feature:...')` → **Critical**: the route is the enforcement point; the in-job check is defense-in-depth, not the gate
- `Feature::define('<capability>', true)` for import/email/SMS flags defaulting true globally → High (plan gating absent; per-plan closures are the safe shape)
- **Pennant staleness** — database store + no `pennant:purge` in any deploy script → Medium: reverting a default does NOT clear stored per-scope values; any scope resolved during a true-default window keeps true until purged
- **Blast amplification** — one request → N outbound emails: a dispatched job loads `Model::query()->get()` unbounded and sends per row, no cap, no route `throttle:` → **Critical** (one request = whole mailing list; attacker-controlled subject/body = phishing from your own domain). Flow class F9, `../flow-security/SKILL.md`
- **Public email-triggering endpoints** — `send-verification-link`-style GET (side effect on a GET!) or `subscribe` POST, public, unthrottled, no captcha → **Critical** (enumerating IDs over a public sender = mail bomb with zero auth)
- `$request->all()` into a compose DTO (free-text subject/body) → High (mass assignment + platform-domain phishing)
- Safe shapes: `feature:` middleware on the route AND `Feature::active` re-checked in the job; `->limit()` recipient cap + per-tenant daily quota consumed ATOMICALLY inside the job (queued jobs outlive flag flips — the quota check must not be check-then-act on the HTTP side); POST + signed URL + `throttle:` for verification links; FormRequest for compose; verified-recipients-only targeting

## Reporting

Severity table above. Fixes are usually short — give exact code (`protected $fillable = ['name','email'];`, `whereRaw('name = ?', [$name])`). Cross-reference dependency CVEs via `../dependency-vulns/SKILL.md` (composer.lock).
