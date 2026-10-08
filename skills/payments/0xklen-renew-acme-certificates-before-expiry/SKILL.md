---
name: renew-acme-certificates-before-expiry
description: Use when running or auditing TLS certificates issued by ACME (Let's Encrypt, ZeroSSL). Automate renewal on a schedule, prove the renewal path actually works, and alert on expiry as a backstop rather than as the primary trigger.
---

# Renew ACME certificates before expiry

A certificate that expires takes the whole site down, and "cron will handle it" is not a plan until
you have watched it renew and reload. Automate the happy path and keep a hard expiry alarm behind it.

## Procedure

1. Inventory what is issued and when each expires:
   ```bash
   certbot certificates 2>/dev/null | grep -E 'Certificate Name|Expiry'
   ```
   For files not managed by certbot, read the date off the wire (see `debug-tls-handshake-with-openssl`).
2. Run a dry run first — it exercises the ACME challenge without touching the live cert:
   ```bash
   certbot renew --dry-run
   ```
   This is the only proof that DNS/HTTP-01 challenges still solve.
3. Install a renewal timer and confirm it is enabled, not just present:
   ```bash
   systemctl list-timers | grep certbot
   systemctl status certbot.timer --no-pager
   ```
4. Renew well inside the 30-day window; certbot renews at 30 days left by default:
   ```bash
   certbot renew --deploy-hook 'systemctl reload nginx'
   ```
   The `--deploy-hook` reload is what actually serves the new cert; without it the file changes and the
   running server keeps the old one in memory.
5. For wildcard or DNS-01 certs, verify the provider credential still has rights:
   ```bash
   certbot renew --dry-run --preferred-challenges dns
   ```
6. Add an independent expiry monitor so a broken renewal is loud, not silent:
   ```bash
   echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
     | openssl x509 -noout -enddate
   ```
   Alert when `notAfter` is under 14 days.
7. After a real renewal, confirm the served cert changed — not just the file on disk:
   ```bash
   openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null \
     | openssl x509 -noout -serial
   ```

## Pitfalls

- Certbot renews asynchronously to a timer; a cert that "should" renew can sit until someone runs it manually.
- A `--deploy-hook` that fails (reload without sudo, wrong unit name) renews the file but never reloads.
- Rate limits on Let's Encrypt (5 duplicate certs/week) turn a retry loop into a week-long outage.
- HTTP-01 challenges break when the site forces HTTPS or redirects the `.well-known` path.
- Wildcard certs *require* DNS-01; an HTTP-01 config silently fails for them.
- Monitoring only the file's mtime misses a server that loaded an old cert at start and never reloads.
- The backup/monitor host may not be able to reach the ACME server (egress firewall), failing only in prod.

## Verification

    certbot renew --dry-run && \
    echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
      | openssl x509 -noout -enddate

Pass means the dry run reports "simulated renewal succeeded" and the served cert's `notAfter` is
more than 14 days out. Report the serial before and after a real renewal to prove the reload happened.
