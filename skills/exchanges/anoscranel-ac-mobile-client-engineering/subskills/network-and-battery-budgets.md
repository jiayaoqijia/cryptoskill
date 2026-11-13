---
name: network-and-battery-budgets
domain: software-engineering/network-and-battery-budgets
trigger: "Setting data, latency, and power budgets for a mobile client."
anti_trigger: "Not for server-side performance, and not for web vitals."
scope: "Data, latency, and power budgets on a device you do not control."
status: seedling
---

# Network and battery budgets

## Standard

A mobile client spends three resources that the server does not: the user's data allowance, the battery, and the radio's wake time. Each has a cost that is invisible in a development environment on wifi and mains power, and each becomes visible in the field as a one-star review about battery drain or a complaint about data use on a metered plan.

Budgets make the cost explicit before it is spent. A screen gets a stated allowance in kilobytes and in radio wake-ups, a sync gets a frequency and a size, and a background task gets a power budget it must not exceed. The budget is then measured on a real device under a throttled network, because the emulator and the office wifi both hide the cost.

Primary sources: <https://developer.android.com/> and <https://developer.apple.com/>.

## Decision rules

- Record the data budget per screen and per sync operation, in kilobytes.
- Record the radio wake-up budget: how often the app causes the radio to power up.
- Record the background execution budget and the platform's limits on it.
- Record the behaviour on a metered connection, which may differ from wifi.
- Record the measurement method and the device class used.
- Record the battery cost of any continuous location, sensor, or polling use.

## Procedure

1. Record the budget per screen and per background task.
2. Measure the current cost on a throttled network and a real device.
3. Compare measured against budget and record the gap.
4. Record the platform's background execution limits and how the app respects them.
5. Define the metered-connection behaviour.
6. Re-measure after each release and record the trend.

## Anti-patterns

- Measuring only on wifi and mains power.
- Polling on a fixed interval regardless of app state.
- Requesting continuous location without a stated need.
- Assuming background execution is unlimited.
- Setting a budget and never measuring against it.

## Done checklist

- [ ] Data budget per screen recorded.
- [ ] Wake-up budget recorded.
- [ ] Background execution limits recorded.
- [ ] Metered behaviour recorded.
- [ ] Measurement method and device recorded.
- [ ] Trend recorded after release.

The budget's value comes from being enforced at review rather than discovered in a review: a pull request that adds a network call or a polling loop can be checked against the stated allowance, and without that check the budget is a document rather than a constraint.


## Sources

- Android performance and power guidance: <https://developer.android.com/>
- Apple energy efficiency guidance: <https://developer.apple.com/>
- Web performance measurement reference: <https://www.w3.org/>
