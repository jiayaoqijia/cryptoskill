---
name: deprecation
domain: software-engineering/deprecation
trigger: "\"remove this feature\", \"retire this system\", \"sunset this endpoint\", \"we are shutting down that module\", \"move users off the old path\"."
anti_trigger: "Versioning and breaking-change rules for a live API contract; dropping a database column or table; release-note wording and README prose; the git mechanics of history clean-up."
scope: "Retiring a feature, system or internal API and moving its users"
status: "seedling"
---

# Deprecation

## Standard

- **Deprecation is a contract, not an event**: announce, deprecate, sunset with machine-readable signals, and always with a migration path.
- **SUNSET header** (RFC 8594; https://www.rfc-editor.org/rfc/rfc8594.html) advertises unresponsiveness at a date. **Deprecation header** (RFC 9745; https://www.rfc-editor.org/rfc/rfc9745.html) marks a surface as non-preferred but working. They are two signals, not one.
- **Google GA norm**: minimum one year of notice before a breaking change (https://docs.cloud.google.com/distributed-cloud/hosted/docs/latest/gdch/resources/support-deprecation).
- **Notice length is the highest-leverage lever**: 60-day notices produce reactive scrambles, while one-year notices produce proactive migrations. ⚠️ Source not cited inline; check the Sources list before relying on this figure.
- **Exceptions** that shorten notice: alpha or beta surfaces explicitly marked, security-driven removal, and provider-scheduled retirement.

## Decision rules

1. Name who is affected before you name the date. Production traffic per version answers that question.
2. Give a migration path in the announcement, or give a longer notice.
3. Deprecate first; remove only after usage falls to zero and the window closes.
4. Never break an old binary mid-cycle. Announce, nag, then hard-block with an update prompt.
5. Removing a live feature, a system or a public endpoint is **human-gated**. The agent gathers usage and drafts the plan.
6. Exempted from the long window: pre-GA surfaces, security removal, and provider retirement.
7. ⚠️ No corpus measurement of header adoption exists. Do not claim a share of clients that honour SUNSET.

## Procedure

1. Measure the users: count calls per version, per client, per month.
2. Write the retirement plan: what goes, what replaces it, the date ladder.
3. Set the notice window: one year for an external surface; shorter only for a listed exception.
4. Add the machine-readable signal:
   ```http
   Deprecation: @1688169599
   Sunset: Sat, 01 Nov 2026 00:00:00 GMT
   ```
5. Announce: what changes, the date, the migration steps, and the support contact.
6. Ship the replacement behind a flag (out of scope for this leaf: flag mechanics).
7. Report usage at each review point. A plan nobody measures never reaches zero.
8. Nudge the remaining users: a banner, a log line, a migration deadline.
9. Hard-block only after the sunset date, and keep the block message actionable.
10. Delete the code path and the tests that only served it.
11. Write the post-removal note: what broke, what to watch for.

## Anti-patterns

- Removing a surface with no announced replacement.
- A 60-day deadline on an API that external teams depend on.
- A deprecation announced in a changelog line nobody reads.
- Measuring usage once, at announcement time.
- A hard block with no upgrade path in the message.
- Deleting the old path the same week the last consumer ships.

## Done checklist

- [ ] Affected users measured per version.
- [ ] Replacement exists and works.
- [ ] Notice window set with a stated reason for its length.
- [ ] Deprecation and sunset signals emitted.
- [ ] Usage tracked to zero before removal.
- [ ] Human gate passed before the removal.

## Sources

- <https://theproductguy.in/blogs/api-governance-guide>
- <https://builtplain.com/app-review-rejection-playbook>
- https://www.rfc-editor.org/rfc/rfc8594.html · https://www.rfc-editor.org/rfc/rfc9745.html
