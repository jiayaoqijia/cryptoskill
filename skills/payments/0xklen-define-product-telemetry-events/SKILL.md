---
name: define-product-telemetry-events
description: Use when a feature ships without a way to tell whether it works in the wild. Names the events, properties, and the decision each one informs before launch.
---

# Define product telemetry events

If you cannot see a feature used, you cannot tell success from silence. This skill defines the minimum events, each tied to a decision, so launch is measurable without logging everything.

## Procedure

1. For each launch question ("did users reach step 3?", "do retries succeed?") write one event name in `events.md`; an event with no question behind it is noise.
2. Name events `object_action` in past tense: `order_submitted`, `checkout_failed`, with no spaces or mixed camelCase.
3. List the properties each event carries: the dimensions you will group by (plan, platform, experiment cohort) and the identifiers you will join on (`user_id`, `session_id`, `order_id`).
4. Forbid free-text and unbounded values in properties; an error string or a URL path with an id belongs in a coarse `error_class`, never a raw message.
5. Exclude PII and secrets by construction: no email, no card, no token. Check property names against the PII inventory before shipping.
6. Map each event to the metric it feeds (funnel step, error rate, latency) and to the dashboard or alert that reads it.
7. Define the success threshold before launch, e.g. "step-3 conversion at least 40% within two weeks", so the data has a decision to make.
8. Version the event schema and log the change; a renamed property silently breaks every downstream chart.
9. Set a retention period per event and drop high-volume debug events after the experiment closes.
10. Confirm events fire once per logical action, not per render, so counts are not inflated by retries.

11. Document the event's owner team so schema questions reach the right people fast.

## Pitfalls

- Logging page views and calling it product analytics; views do not say whether a task completed.
- High-cardinality properties (a raw user id as a value, a full URL) that blow up query cost and storage.
- Capturing an email or address "just in case", creating a compliance liability.
- Events that fire for both success and failure under the same name, so failure is invisible.
- No owner or dashboard, so the event collects dust until an incident needs it.
- Instrumenting after launch, so the first cohort's behaviour is invisible.
- Sampling analytics without a plan for the rare error path you actually wanted to see.

- Adding a property because it is cheap to log, without a question it answers.

## Verification

    grep -cE '^[a-z]+_[a-z_]+' events.md; grep -inE 'email|token|password|card' events.md || echo no-pii

Report the event list, the decision each informs, and any property that could carry PII.
