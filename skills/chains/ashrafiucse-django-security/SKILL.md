---
name: django-security
description: Audits Django (Python) applications for framework-specific vulnerabilities — raw()/extra() SQL injection, mark_safe and |safe filter XSS, SSTI via Template() with user strings, ModelForm fields='__all__' mass assignment, settings misconfigurations (DEBUG=True, ALLOWED_HOSTS=['*'], insecure cookie flags, hardcoded SECRET_KEY), missing login_required/permission checks (IDOR), weak password hashers, and django-cors-headers wildcards. Use when the project has manage.py, settings.py, or Django in requirements.
license: MIT
---

# Django Security

## Step 0 — Detect

```bash
rg -n "^[Dd]jango" -g 'requirements*.txt' -g 'pyproject.toml' -g 'Pipfile*' -g 'poetry.lock'
ls manage.py **/settings.py 2>/dev/null || rg --files -g 'settings.py' | head -3
```

Record Django version, auth setup (django.contrib.auth vs custom), and deployment target hints.

## Step 1 — Settings

```bash
rg -n "DEBUG|ALLOWED_HOSTS|SECRET_KEY|CSRF_COOKIE|SESSION_COOKIE|SECURE_" -g 'settings*.py' -g 'settings/*.py'
```

| Finding | Severity |
|---|---|
| Hardcoded `SECRET_KEY` (not env) | High (Critical if repo is public — session forgery, password-reset tokens) |
| `DEBUG = True` in prod settings | High (stack traces; historically settings disclosure) |
| `ALLOWED_HOSTS = ['*']` | Medium → host-header poisoning of password-reset links (High when reset flows exist) |
| `CSRF_COOKIE_SECURE` / `SESSION_COOKIE_SECURE` False/absent | Medium |
| `SECURE_SSL_REDIRECT` absent behind plain HTTP | Medium |
| `PASSWORD_HASHERS` with MD5/SHA1 hasher | Critical (weak password storage) |
| django-cors-headers: `CORS_ALLOW_ALL_ORIGINS=True` (+ credentials) | Medium/Critical |

## Step 2 — SQL injection

```bash
rg -n "\.raw\(|\.extra\(|cursor\.execute" --type py
```

- `Model.objects.raw(f"...{request...}")` / `.raw("... %s" % var)` → Critical
- `.extra(where=[f"...{...}"])` → Critical
- ORM field lookups (`filter(name__icontains=q)`) → safe, note as positive

## Step 3 — XSS / template injection

```bash
rg -n "mark_safe\s*\(" --type py
rg -n "\|safe\b" -g '*.html' -g '*.htm'
rg -n "Template\(|Engine\(\)\.from_string" --type py
```

Census, don't sample: count and disposition EVERY hit. (Do not combine these into one command — `--type py` and a `-g '*.html'` glob in the same invocation silently drop the `.py` hits, i.e. every `mark_safe` in views.) Severity by privilege direction per `../injection-flaws/SKILL.md` (XSS table): unprivileged author → privileged viewer = Critical.

- `mark_safe(user_data)` → reflected High; stored unprivileged→staff (moderation/support/grading) Critical
- `{{ var|safe }}` in templates on user-derived vars → same triage
- `autoescape=False` in `Template()`/loader options → High
- `Template(user_string)` (string built from input) → SSTI, Critical

## Step 4 — Mass assignment

```bash
rg -n "fields = '__all__'|exclude = .*ModelForm|modelform_factory" --type py
```

- `ModelForm` with `fields = '__all__'` on models with role/flag columns (`is_superuser`, `is_staff`, `role`, `balance`) → High/Critical
- `Model(**request.POST.dict())` / manual `form = X(request.POST)` without restricting → same
- Fix: explicit field allowlists; `request.POST` is user-controlled wholesale.

## Step 5 — Authorization

```bash
rg -n "login_required|LoginRequiredMixin|permission_required|@user_passes_test" --type py
rg -n "def (view|detail|edit|delete)" --type py | head -20
```

- Object views without ownership check (`Model.objects.get(pk=request.GET['id'])` returned directly) → IDOR, High
- Class-based views missing `LoginRequiredMixin` on data mutation → High
- `@staff_member_required` on endpoints exposing PII → verify minimum role

## Step 6 — Files & misc

```bash
rg -n "request\.FILES|FileField|MEDIA" --type py
rg -n "pickle|eval\(|exec\(" --type py | head
```

- Uploads with original filenames served from MEDIA (executable content + Apache/nginx PHP exec) → Medium/High
- `pickle` in custom session/queue serialization → Critical
- `django-debug-toolbar` in non-dev requirements → Medium
- File responses built from request paths → traversal, High

## Reporting

Severity table above; fixes are one-liners mostly (field allowlists, decorators, settings flags). Note ORM usage as a positive control. Dependency CVEs via `../dependency-vulns/SKILL.md`.
