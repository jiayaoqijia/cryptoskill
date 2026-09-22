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

## 4 — Monitoring & alerting config (A09 deep checks)

Alerting is where "logs exist" becomes "attacks noticed". In-repo evidence CAN prove presence — look for it before writing "not assessed":

```bash
rg --files -g '*alert*' -g 'prometheus*.yml' -g 'rules*.yml' -g '*monitoring*' -g 'alarms*' -g '*.tf' | head
rg -n -i "alertmanager|pagerduty|cloudwatch.*alarm|aws_sns|azmonitor|google_monitoring|datadog_monitor|sentry" -g '*.yml' -g '*.yaml' -g '*.tf' -g '*.json' | head
```

- **No alert-routing config anywhere** + auth/payment surfaces exist → MEDIUM finding: "no detection signals for credential attacks" (name the 2-3 rules that should exist: auth-failure spike per account/IP, admin-action anomaly, error-rate spike)
- Alert rules present but none keyed on security events (only CPU/latency) → same finding, gentler
- Positive signals to note: `ratelimit` alerts, login-failure dashboards, WAF/log-based rules (`cloudwatch_log_metric_filter` on auth events)
- Still unverifiable (SaaS-only config) → **"not assessed"** with what to check on the vendor side

- Log retention + immutability (append-only sink, WORM storage)
- Request correlation IDs in logs (absent → LOW; investigation friction)

## Reporting

List: missing audit events (endpoint by endpoint), forging sinks (`file:line`),
overly verbose configs. Close with the readiness question — *"Can you answer
'who changed X, when?' for the three most sensitive operations?"* If no, the
gap is real even without a grep hit.
