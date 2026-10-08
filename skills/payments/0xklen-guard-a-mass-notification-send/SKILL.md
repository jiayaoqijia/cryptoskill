---
name: guard-a-mass-notification-send
description: Use when code will send a notification, email or push to many recipients — ramps volume, uses a suppression list and a sandbox recipient so a broken message cannot reach the whole audience before anyone notices.
---

# Guard a mass notification send

A mass send is irreversible: once 200,000 emails are out, a broken link, a wrong segment or a duplicated send cannot be recalled. The guard is to make the blast radius grow only as fast as you can verify it, and to give one person a stop button that works between batches.

## Procedure

1. Build the recipient list as a *query* with a hard count, and freeze it before sending. Print the count and the segment definition; a "send to all users" whose definition nobody read is the classic incident:
       SELECT count(*) FROM users WHERE marketing_opt_in AND region='EU';  -- 182,441

2. Send to one recipient in a sandbox first — a real inbox you control — and check rendering, links, images and unsubscribe. Only then proceed.

3. Ramp: 1 → 100 → 1,000 → 10,000 → remainder, with a pause between rungs to read the bounce rate, complaint rate and error rate. Abort criteria stated up front: e.g. bounce > 2% or any provider 5xx.

4. Apply a suppression list *in the send code*, not in the list-building SQL: transactional-only, previously unsubscribed, and anyone who triggered a recent complaint. A suppressed address that receives the send is a deliverability and legal problem:
       recipients = [r for r in recipients if r.id not in current_suppression_set()]

5. Make the send idempotent per recipient per campaign, keyed on `(campaign_id, recipient_id)`, so a retried batch does not send twice:
       if redis.set(f"sent:{campaign}:{recipient}", 1, nx=True, ex=2592000) is None: skip

6. Give the operator a pause that works *between batches*: a flag checked by the worker before each batch, plus a provider-side pause if available. A pause implemented only in the API layer does nothing once the worker is running.

7. After the send, reconcile sent-count against the frozen list count and deliver the difference explanation (suppressed, bounced) — not just a green checkmark.

## Pitfalls

- Sending from a loop with no batching, so the pause/abort has no place to run and the send completes before anyone can react.
- A suppression list applied as an afterthought in the UI while the trigger path bypasses it, delivering to unsubscribed users.
- Missing or wrong `List-Unsubscribe` / `unsubscribe` link, turning a small mistake into a spam-complaint spike and a domain reputation hit.
- Testing in production by adding your own address only to find the template renders differently for real recipients.

## Verification

    # dry run against the frozen list, then a 1-recipient sandbox send
    python send_campaign.py --campaign spring --dry-run      # prints count + segment SQL
    python send_campaign.py --campaign spring --sandbox you@yourco.com
    # ramp with a pause: abort must stop remaining batches
    python send_campaign.py --campaign spring --ramp 1,100,1000 --abort-on-bounce 0.02
    redis-cli scard "sent:spring:*"                          # dedupe key protects retries

Report: the frozen list count and segment, the sandbox result, the ramp and abort thresholds, the suppression applied in code, and the post-send reconciliation of sent vs suppressed vs bounced.
