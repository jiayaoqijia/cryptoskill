---
name: bind-consent-to-a-stated-purpose
description: Use when building or auditing a consent flow and the wording, scope, or audit trail is unclear. Record purpose, notice version, and proof of action, then gate processing on a current grant.
---

# Bind consent to a stated purpose

Consent that does not name a purpose cannot be relied on. This skill records what was agreed, when, and for exactly which use, and enforces it at call time.

## Procedure

1. Write each purpose as a discrete record id: `purpose_id = "marketing_email_2024"`. Vague wording such as "improve services" fails.

2. Store the consent event append-only, never mutate: `(subject_id, purpose_id, granted_at, text_version, source, method, revoked_at)`.

3. Pin the exact wording by hash so you can prove what the user saw: store `text_sha256` of the notice that was displayed.

4. Capture the unbundled choice: separate rows for analytics, marketing, and personalisation. A single checkbox is not valid consent for three purposes.

5. Capture proof of the action: IP, user agent, and the click itself, not the page load. A scripted consent event is not consent.

6. Gate processing on a fresh lookup every time:
   `select 1 from consent where subject_id=$1 and purpose_id=$2 and revoked_at is null and granted_at > now() - interval '24 months'`

7. Make revocation as easy as grant and propagate it through every downstream system within a defined SLA (for example 24h to the email provider).

8. Log the check result (granted or denied) per message so a complaint is answerable from logs alone.

9. Re-consent on any material wording change; a new purpose is a new consent, never an edit to the old row.

## Pitfalls

- Pre-ticked boxes and implied consent fail in GDPR-style regimes; record an affirmative act.
- Bundling consent into terms acceptance invalidates it for optional processing.
- Deleting the row on revocation erases proof that consent ever existed; revoke with a timestamp instead.
- A suppression list keyed only on email fails when the address changes; also key on the person identifier.
- Consent drift: an old purpose string lingers in code while the notice changed underneath it; match on `purpose_id` and version.

## Verification

    psql "$CONSENT_DB" -c "select purpose_id, count(*) filter (where revoked_at is null) active, count(*) total from consent group by 1 order by 1"

Report the active count per purpose, the newest notice version in use, and any system still sending on a revoked grant.
