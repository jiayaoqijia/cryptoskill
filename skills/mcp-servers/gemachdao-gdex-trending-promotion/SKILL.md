---
name: gdex-trending-promotion
description: Paid trending-slot promotion — book featured slots on the trending feed and check booking status
---

# GDEX: Trending Promotion

Book paid trending slots so a token appears in the platform's promoted
trending feed for a defined period.

## When to Use

- A token creator / marketer wants to buy visibility for their token
- Listing the available trending packages, prices, and durations
- Checking the booking status of a previously-registered slot

## Prerequisites

- `@gemachdao/gdex-skill` installed
- Authenticated via shared API key or wallet sign-in — see **gdex-authentication**
- For paid bookings: a managed-custody `computedData` payload, OR a
  user wallet able to pay on-chain (depending on backend deployment)

## Backend Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET`  | `/v1/trending/list` | Currently active / booked promoted tokens |
| `GET`  | `/v1/trending/options` | Available slot packages, durations, prices |
| `POST` | `/v1/trending/register` | Register / pay for a trending slot |
| `GET`  | `/v1/trending/booking_status` | Check booking status |

## SDK Usage

```typescript
import { GdexSkill } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(process.env.GDEX_API_KEY!);

// 1. List available packages
const options = await skill.getTrendingOptions();

// 2. Register a slot
const booking = await skill.registerTrending({
  tokenAddress: '0x...',
  chain: 8453,
  slot: 'gold',
  durationHours: 24,
  userId: '0xUserControlWallet',
  computedData,                  // when paying via managed custody
});

// 3. Poll status
const status = await skill.getTrendingBookingStatus({
  bookingId: booking.bookingId as string,
});
```

## Notes

- Packages (slots) and pricing are configured server-side and may change.
- The backend returns a `bookingId` from `register` that should be persisted
  for status polling.
- Booking status values are typically `pending_payment`, `active`, or
  `expired`.
