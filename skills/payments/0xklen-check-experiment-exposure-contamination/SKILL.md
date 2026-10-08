---
name: check-experiment-exposure-contamination
description: Use when experiment arms might not be independent. Checks for cross-arm leakage, assignment-after-exposure, and shared-identity contamination.
---

# Check Experiment Exposure Contamination

Randomisation assumes each unit sees one arm and only its own. Shared devices, shared accounts, and delayed logging break that, and the break is invisible in the summary table.

## Procedure

1. Confirm assignment precedes exposure. Join the first-exposure timestamp to the assignment timestamp; any exposure before assignment is a bug.
2. Check for units in both arms: an id present in the treatment and the control set is leakage:
   ```sql
   SELECT count(*) FROM (
     SELECT unit_id FROM exp_assignment WHERE variant = 'control'
     INTERSECT
     SELECT unit_id FROM exp_assignment WHERE variant = 'treatment'
   ) x;   -- must be 0
   ```
3. Look for shared-identity paths: same device_id, same payment instrument, same household IP, or account switching across arms.
4. For logged-out or pre-login surfaces, check whether the unit is the cookie and whether cookies are cleared between sessions.
5. Check exposure logging itself: an event fired only in the treatment client undercounts treatment exposure and biases the read.
6. Watch network spillover in marketplace, social, and auction products — one user's treatment changes another user's control experience.

## Pitfalls

- Trigger-based analysis ("only users who saw the feature") drops non-compliers asymmetrically and is no longer randomised.
- Cookie-based units undercount logged-out users and overcount shared browsers.
- Delayed exposure logging makes early funnel metrics look different when they are only slower to instrument.
- Two concurrent experiments on the same surface interact; check the mutual-exclusion list.
- A single shared kiosk or family account can place one user in both arms for weeks.

## Verification

    psql "$DSN" -c "SELECT variant, count(DISTINCT unit_id) FROM exp_exposure GROUP BY 1;"  # compare with assignment counts per arm

Report: "Assignment-then-exposure held, but 1,340 device_ids appear in both arms (shared browsers). Switched the unit to account_id and re-ran; arm sizes equalise."
