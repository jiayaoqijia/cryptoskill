---
name: locale-formatting
domain: software-engineering/locale-formatting
trigger: "Formatting dates, numbers, and currency for a locale."
anti_trigger: "Not for time zone policy design, and not for translation."
scope: "Dates, times, time zones, calendars, numbers, and currency."
status: seedling
---

# Locale formatting

## Standard

A date written as a number pair is ambiguous between day-first and month-first conventions, and a number with a comma separator means one thing in one locale and another elsewhere. Locale formatting exists because those conventions are not universal, and a hard-coded format is a defect that only appears for users outside the developer's locale.

Time zones are a separate correctness problem from formatting. A timestamp stored without a zone cannot be rendered correctly for a user in another zone, and a recurring event scheduled in local time crosses daylight-saving boundaries differently than a fixed interval would. Currency has the same shape: the currency code and the formatting locale are independent decisions, and conflating them produces a price displayed in the wrong symbol.

Primary sources: <https://cldr.unicode.org/> and <https://www.iana.org/time-zones>.

## Decision rules

- Record the formatting locale source: user preference, device locale, or an explicit setting.
- Record the storage format for timestamps, which should carry an offset or be UTC.
- Record the calendar system used for display and whether alternatives are supported.
- Record the currency code as distinct from the formatting locale.
- Record the rounding and presentation rules for money, including the minor unit.
- Record the behaviour for a user travelling across time zones.

## Procedure

1. Record where the formatting locale comes from.
2. Record the stored representation of every timestamp.
3. Record the display calendar and any alternate calendars.
4. Separate the currency code from the locale and record both.
5. Record the money rounding rule and its minor unit.
6. Test across a daylight-saving transition and a time zone change.

## Anti-patterns

- Formatting a date with a hard-coded pattern.
- Storing a local time without an offset.
- Using the display locale to infer the currency.
- Rounding money with a binary floating type.
- Assuming a day has twenty-four hours when scheduling recurring events.

## Done checklist

- [ ] Locale source recorded.
- [ ] Timestamp storage recorded with offset or UTC.
- [ ] Calendar recorded.
- [ ] Currency code separated from locale.
- [ ] Money rounding rule recorded.
- [ ] DST and travel cases tested.

The daylight-saving case deserves a concrete test because it is the one that fails silently: an event scheduled for a fixed local time must shift with the transition, an interval must not, and a scheduler that stores only a local timestamp cannot distinguish the two. Testing across one transition in each direction reveals which behaviour the code actually implements.


## Sources

- Unicode CLDR formatting data: <https://cldr.unicode.org/>
- IANA time zone database: <https://www.iana.org/time-zones>
- W3C date and time formats: <https://www.w3.org/International/>
