---
name: write-a-sunset-plan-for-a-feature
description: Use when retiring a feature, endpoint, or product. Plans the deprecation notice, the migration path, the data disposition, and the removal date so users are not stranded.
---

# Write a sunset plan for a feature

Removing something is a product change, not a cleanup. This skill plans the notice, the migration, and the data handling so a sunset does not become an incident.

## Procedure

1. Inventory who uses it: query the telemetry (`events.md`) or access logs for the last 90 days, and list the distinct accounts, not just the request count.
2. Classify users: `no usage`, `light`, `heavy`, and `automated` (bots, integrations); each needs a different migration message.
3. Pick the removal date with margin, and a freeze date after which no new usage is allowed; put both in `sunset.md`.
4. Write the notice with the three facts a user needs: what ends, when it ends, and the exact replacement with a link.
5. Define the migration path: an export, a redirect, a new endpoint, or a documented manual step. Test it end-to-end on a real account.
6. Decide data disposition: export to the user, retain under policy, or delete — with the retention rule and deletion method named, never "clean up later".
7. Set the escalation path for stragglers: who contacts heavy users directly, and by what date before removal.
8. Stage the removal: return `410 Gone` (or the platform equivalent) before physically deleting, so callers get a clear signal, not a 404.
9. After removal, confirm no traffic remains in the logs, then delete the code, the config, and the docs.
10. Confirm the replacement actually covers the use cases the old feature supported, not just the common one.
11. Give the removal its own monitoring window, watching for calls from callers you did not inventory.

12. Send at least two reminders before the freeze date, spaced so a vacation does not swallow them.

## Pitfalls

- Removing an API used by a partner's cron nobody told you about; check for automated callers first.
- Emailing only the admin, not the integration owner who actually calls it.
- A deprecation date with no migration tooling, leaving users to hand-port data.
- Deleting data the user was entitled to export under a retention policy.
- Leaving a 404 where a 410 and a message belong, which reads as a breakage.
- Announcing the sunset after disabling the endpoint, which strands users with no warning.
- Assuming a redirect is a drop-in replacement when the payload shapes differ.

- Removing docs before the code, so stragglers have nowhere to read the migration path.

## Verification

    grep -c 'users:\|date:\|replacement:' sunset.md; grep -cE '410|redirect|export' sunset.md

Report the distinct-user count, the removal date, and the migration path with its tested status.
