# Pattern Library — design-threat-review

Not grep sinks — repeatable threat→detector→criterion shapes. Grow via MISSES.md.

| Design shape | Threat (STRIDE) | Detector skill | Acceptance criterion (checkable) |
|---|---|---|---|
| Unprivileged actor submits content; privileged actor opens it (review, ticket, message, upload name) | Tampering + Elevation → staff-origin XSS → ATO | injection-flaws + framework skill (laravel Step 4 privilege-direction) | content passes an escaper before formatting in EVERY staff view (list AND detail), or is purified at write |
| Moderation/approval workflow on submitted content | Elevation — approval guarantees a privileged viewer opens attacker input | course-platform-security §6.5 | same as above, PLUS the pending state never short-circuits rendering |
| Free preview / sample of paid content | Info disclosure → paid content free | course-platform-security §3 | preview response is server-side limited to N items — field selection verified, not just access |
| Webhook/postback creates or unlocks something of value | Spoofing + Repudiation → free goods | flow-security (F8), auth-review | signature verification required before ANY state write; replay rejected |
| Catalog/listing shows unpublished or private items | Info disclosure → roadmap/private-catalog leak | course-platform-security §2 | every public read path filters status+visibility, including counts/facets/sitemaps |
| Entitlement granted by anything other than paid fulfillment | Elevation → free enrollment | flow-security, course-platform-security §4 | enrollment written only by status-guarded fulfillment or role-middleware admin grant |
| Cross-cohort / multi-tenant data fetch by bare ID | Info disclosure → tenant bleed | auth-review tenant-scope census, course skill §5 | reads scoped by the caller's membership record, never by request-supplied tenant/cohort ID |
