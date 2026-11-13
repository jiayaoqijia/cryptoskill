---
name: monotonic-versus-wall
domain: software-engineering/monotonic-versus-wall
trigger: "Deciding which clock to read for a duration or a timestamp."
anti_trigger: "Not for cross-machine reasoning (that is clock-skew)."
scope: "The two clocks, their guarantees, and the failure of using the wrong one."
status: seedling
---

# Monotonic versus wall

## Standard

The wall clock tells you the time of day; the monotonic clock tells you how much time has passed since some arbitrary point. The wall clock can jump — synchronisation steps it, administrators reset it, virtual machines migrate it — so it is unsuitable for measuring intervals. The monotonic clock only ever moves forward, so it is unsuitable for telling anyone what time it is.

The classic bug is interval-by-subtraction of wall-clock reads: an NTP correction steps the clock back mid-request and the elapsed time comes out negative, or a migration nudges it forward and a retry storm is computed. The rule that prevents the whole class: durations from the monotonic clock, timestamps for humans and for ordering from the wall clock, and never a wall subtraction where a duration matters.

## Decision rules

- Use the monotonic clock for every duration: timeouts, retries, profiling, rate limits.
- Use the wall clock for timestamps that will be stored, displayed, or compared across processes.
- Never compute an elapsed interval by subtracting two wall-clock reads.
- Record which clock a measurement came from when the measurement will be compared with others.
- Check the deployed runtime's monotonic guarantee: some pause during suspend, which affects long timers.
- For high-resolution needs, verify the clock's resolution on the target platform rather than assuming.

## Procedure

1. Classify the need: how long, or when.
2. Select the clock from the classification.
3. Where a duration guards an action — timeout, retry — confirm the monotonic clock is actually used.
4. Record timestamps in UTC with the format from the storage leaf.
5. Verify on the target platform that the monotonic clock behaves as expected over a suspend.
6. Record the clock choice in the code review and the time policy.

## Anti-patterns

- Measuring latency with two reads of the time of day.
- Storing durations as pairs of wall timestamps instead of elapsed values.
- Assuming the runtime's monotonic clock never pauses.
- Mixing clock sources within one computation.
- Using the monotonic value as a timestamp because it looks like a big number.

## Done checklist

- [ ] Each need classified as duration or timestamp.
- [ ] Correct clock selected per use.
- [ ] No wall-clock subtraction guarding an action.
- [ ] Platform monotonic behaviour verified.
- [ ] Timestamps stored in the standard format.
- [ ] Choices recorded in the time policy.

## Sources

- Time representations and their use: <https://www.rfc-editor.org/rfc/rfc3339>
- POSIX clock types and guarantees: <https://pubs.opengroup.org/onlinepubs/9699919799/>
- Time in the Java platform: <https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/package-summary.html>
