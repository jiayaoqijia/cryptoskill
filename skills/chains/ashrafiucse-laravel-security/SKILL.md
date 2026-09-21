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
rg -n '\{!!' resources/views/
```

Every `{!! !!}` with a variable that traces to user input → High (Blade's `{{ }}` escapes; `{!! !!}` exists only to bypass). Check `{{ $x }}` + `|raw`? (Blade has no `|raw`; Twig confusion = false positive).

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

## Reporting

Severity table above. Fixes are usually short — give exact code (`protected $fillable = ['name','email'];`, `whereRaw('name = ?', [$name])`). Cross-reference dependency CVEs via `../dependency-vulns/SKILL.md` (composer.lock).
