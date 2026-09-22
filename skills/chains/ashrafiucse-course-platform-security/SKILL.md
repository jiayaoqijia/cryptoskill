---
name: course-platform-security
description: Audits course-selling / e-learning platforms for domain-specific security — catalog gating truth (draft/unpublished/private course exposure to public), preview-vs-full-content leaks, enrollment state machines (free enrollment without paid order), cohort/multi-cohort access control (student of cohort A reading cohort B), and persona-driven route checks (admin-only surfaces reachable by public/student). Use when the project sells or gates digital courses/content — look for courses, lessons, enrollments, cohorts, orders, subscriptions, previews.
license: MIT
---

# Course Platform Security

Domain skill built from the three personas. Walk every surface as each
persona — findings live where a persona reaches something that isn't theirs.

## 1 — Map the domain model

```bash
rg -n -i "course|lesson|module|enrollment|cohort|preview|curriculum|subscription" -g '**/models/**' -g '**/entities/**' -g '*.prisma' -g 'schema*' | head -25
rg -n -i "(enroll|purchase|checkout|access|entitle)" -g '*routes*' -g '*controller*' | head -20
```

Record: course lifecycle states (draft → published → archived? private?),
enrollment sources (order/webhook/admin-grant/subscription), cohort model
(if any), preview mechanism, content storage/signing.

## 2 — Gating truth (public persona)

The public catalog must only expose what is published AND public.
```bash
rg -n "courses?\.(find|where|all|select)" -g '*.js' -g '*.ts' -g '*.py' -g '*.rb' | head
```
- List/search endpoints returning draft/unpublished/private courses → **High**
  (hidden product roadmap + private catalog leaks; PR-sensitive)
- Detail endpoints rendering unpublished courses by id (no 404 on
  `status != published`) → High — check the 404 branch actually filters status
- Sitemap/feeds/search-index endpoints including gated courses → Medium
- **Safe shape**: `where({ status: 'published', visibility: 'public' })` on
  EVERY read path the public persona can reach, including counts and facets.

## 3 — Preview vs full content (public persona)

```bash
rg -n -i "preview|sample|trial|first.?lesson" -g '*controller*' -g '*routes*' -g '*resolver*' | head
```
- Preview endpoints returning the FULL lesson/video/module payload → **Critical**
  (paid content free; check field selection, not just access)
- Unsigned/expiring-missing media URLs in preview responses that also serve
  full content → High (URL guessing/replay)
- "Free first lesson" logic that trusts client-sent lesson index → Medium

## 4 — Enrollment as a state machine (student + flow)

Ties into `../flow-security/SKILL.md` (F1/F5 classes) — enrollment is the
terminal artifact of order→payment:
```bash
rg -n -i "enrollment.*(create|insert|save)|grant.*access" -g '*.js' -g '*.py' | head
```
- Enrollment created without a PAID order/artifact check (admin-grant paths
  must be separately authorized) → **Critical** (free enrollment)
- Webhook-driven enrollment without signature verification → Critical
- Self-enrollment endpoints allowing arbitrary `courseId` + `userId` from
  body → Critical
- **Safe shape**: enrollment granted only by the payment fulfillment path
  (status-guarded) or an admin-grant route with role middleware.

## 5 — Cohort / multi-cohort access (student persona)

```bash
rg -n -i "cohort|batch|class_?id|group_?id" -g '*.js' -g '*.py' -g '*.rb' | head
```
- Materials/lessons/live-sessions fetched by courseId WITHOUT the student's
  cohort scope → **High/Critical** (cross-cohort read; per-object authz is not
  enough — the cohort IS the tenant; see multi-tenant census in `../auth-review/SKILL.md`)
- Cohort-switching via request body (`req.body.cohortId`) instead of the
  enrollment record → Critical
- Progress/completion written cross-cohort (student A completing for B) → High

## 6 — Admin surfaces (admin persona — and everyone else)

```bash
rg -n -i "admin|manage|catalog|publish|price|coupon" -g '*routes*' -g '*controller*' | head
```
Route-census every admin route: course create/update/publish, price change,
coupon mint, refund, user management. Any reachable without role middleware →
**Critical** (price tamper + free-publish chains). Coupon minting and price
changes are money operations — same state-machine rules as flow-security.

## 7 — Reporting

Tag findings with the persona that reaches them (`public:`, `student:`,
`admin:`) and the class (GATING / PREVIEW / ENROLLMENT / COHORT / ADMIN).
Chains matter here: unpublished-catalog leak + preview-full-content =
competitor scraping; enrollment-bypass + cohort-IDOR = free full access at
scale. Cite the invariant violated, not just the line.

## False-positive discipline

- Legit "coming soon" previews intentionally showing full first lesson
  (check the product flag before flagging free-first-lesson)
- Admin-grant enrollment endpoints WITH role middleware = by design
- Internal LMS (no public persona): skip §2/§3, keep §4/§5/§6
