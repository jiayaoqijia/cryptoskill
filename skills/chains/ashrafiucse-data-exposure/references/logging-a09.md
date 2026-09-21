# A09 Logging & Monitoring Pack (OWASP)

Detection for missing security logging (CWE-778), log forging (CWE-117), and
monitoring gaps. Load when the audit needs OWASP A09 coverage or the project
has auth/admin surfaces.

## 1 — Audit-event coverage

Security events that MUST produce a log line with actor, action, target, timestamp:

> login success/failure · password change/reset · MFA change · role/permission
> change · data export/deletion · admin actions · payment-critical operations

Find the handlers, then check each for logging:

```bash
rg -l -i "def login|@app\.route\(.*login|router\.(post|get)\(['\"].*(login|signin)|signIn|@PostMapping\(.*(login|signin)"
rg -l -i "password|reset|mfa|role|permission|admin|export|delete" | head -20
```

For each hit file: `rg -n -i "log(ger|ging)?|audit|console\." <file>` — no match →
finding: **"security-relevant endpoint with no audit logging"** (Medium; High for
admin/payment endpoints).

Positive signals (controls done right — note them): django-axes, Rails `audited`
gem + lograge, Java audit frameworks, structured logging with redaction (pino
redact, structlog processor).

## 2 — Log forging / injection (CWE-117)

```bash
rg -n -i "(logger?\.\w+|console\.(log|info|warn|error)|logging\.\w+)\(.*(req\.headers|user.?agent|x-forwarded-for|referer|req\.(query|body|params))"
```

Headers are fully attacker-controlled. Any raw header/param reaching a log call
without CRLF stripping → Medium. Fix: sanitize control characters
(`value.replace(/[\r\n]/g, '')`) or log field-by-field via structured logging.

## 3 — Verbosity config

```bash
rg -n -i "log(level|_level)?\s*[:=]\s*[\"']?(debug|trace)" -g '*.yml' -g '*.yaml' -g '*.json' -g '*.toml' -g '*.env*' -g '*.conf' -g '*.py' -g '*.js' -g '*.ts'
```

debug/trace in prod-looking config → Medium (noise hides real attacks; may leak
data — cross-check `../SKILL.md` Step 2).

## 4 — Monitoring hooks (report-level; grep can't prove absence)

Unless evidence exists in-repo, mark as **"not assessed"** rather than guessing:
- Error-rate / auth-failure-spike alerting (Sentry, CloudWatch alarms, PagerDuty config present?)
- Log retention + immutability (append-only sink, WORM storage)
- Request correlation IDs in logs (absent → LOW; investigation friction)

## Reporting

List: missing audit events (endpoint by endpoint), forging sinks (`file:line`),
overly verbose configs. Close with the readiness question — *"Can you answer
'who changed X, when?' for the three most sensitive operations?"* If no, the
gap is real even without a grep hit.
