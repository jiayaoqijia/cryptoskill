---
name: map-third-party-data-processors
description: Use when you must name every vendor receiving personal data and the fields each one gets. Discover recipients from real egress traffic, then record purpose, fields, and region.
---

# Map third-party data processors

Every vendor you send personal data to is a recipient you must be able to name and constrain. This skill builds that list from real traffic, not from a CRM of intended vendors.

## Procedure

1. Discover recipients from egress, not memory. Snapshot outbound endpoints over a week:
   `rg -o "https://[a-z0-9.-]+" src/ | sort -u` and cross-check against proxy or DNS logs.

2. For each domain capture: vendor name, purpose, data fields, processing region, DPA status, sub-processors, and retention.

3. Classify each as processor (acts on your instruction) or controller (decides the purpose). A self-serve analytics tool may be a controller, not a processor.

4. Verify the processing region from the endpoint host and the vendor's residency setting, never from the marketing page.

5. Confirm a signed DPA exists with the correct legal entity and covers the data categories you actually send.

6. Record the exact fields sent by reading the payload code, then minimise: remove any field the vendor does not need for the stated purpose.

7. Track sub-processors. A vendor's CDN, error tracker, or email delivery provider is a further recipient you must list.

8. Alert on new egress: a weekly diff of this week's domains against last week's must be empty or reviewed by a human.

9. Re-review annually and on any vendor change, and keep the register in version control.

## Pitfalls

- Client-side SDKs phone home from the browser and are invisible to server-side grep; check the network tab and the CSP `connect-src`.
- A "free" tool funded by data brokerage is likely a controller that sells data, not a processor acting for you.
- Support tools hold whatever the user typed into a ticket; treat the helpdesk as a high-risk recipient.
- A residency dropdown in a dashboard does not guarantee storage location; get the processing location in writing.
- A vendor acquiring another company silently changes the recipient; monitor vendor corporate changes.

## Verification

    comm -13 <(sort last-week-domains.txt) <(sort this-week-domains.txt)   # expect empty or investigated

Report the vendor count, the fields sent to each, and any egress domain not on the register.
