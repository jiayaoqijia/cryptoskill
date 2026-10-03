---
name: gdex-retailer-onboarding
description: Retailer partner integrations — list branded onboarding partners that white-label the GDEX trading stack
---

# GDEX: Retailer Onboarding

Inspect the list of registered retailer partners — third-party brands that
white-label the GDEX trading stack and have their own branded onboarding
experience.

## When to Use

- Building a partner-aware onboarding flow that routes users to their
  retailer's branded sign-up
- Surfacing partner branding (logo, theme, name) at the application level

## Prerequisites

- `@gemachdao/gdex-skill` installed
- No authentication required (public retailer registry)

## Backend Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET`  | `/v1/retailer` | List registered retailer integrations |

## SDK Usage

```typescript
import { GdexSkill } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
const retailers = await skill.getRetailers();
// Optionally filter by retailer slug / identifier:
const single = await skill.getRetailers({ retailer: 'partner-slug' });
```

## Notes

- The retailer registry is the source of truth for the partner-onboarding
  routing layer — clients should treat it as authoritative.
- Per-retailer schema (logo, theme, redirect URLs) is determined by the
  backend deployment.
