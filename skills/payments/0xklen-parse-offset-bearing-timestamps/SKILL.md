---
name: parse-offset-bearing-timestamps
description: Use when reading a timestamp from an API, log or CSV — parse it with its offset intact and reject strings that carry no zone instead of guessing UTC.
---

# Parse offset-bearing timestamps

Half of all time bugs are parse bugs: `Z` treated as local, a space separator accepted where a `T` was required, a fractional second dropped. Parse strictly, keep the offset, and fail loudly on a stamp that has none.

## Procedure

1. Know the shapes you must accept. RFC 3339 / ISO-8601 allow `Z`, `+00:00`, `-05:00`, fractional seconds and a `T` or space separator:
```
rg -n -o '\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?' sample.log | sort -u | head
```
2. Parse with a library that preserves the offset; Python's `fromisoformat` handles `Z` only from 3.11:
```python
from datetime import datetime, timezone
def parse(s: str) -> datetime:
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if d.tzinfo is None:
        raise ValueError(f"naive timestamp, refusing: {s!r}")
    return d
```
3. For the long tail of formats, pin the format explicitly rather than guessing:
```python
datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f%z")
```
4. Never let a parser silently apply the machine's timezone. If the stamp has no offset, quarantine the record and fix the producer:
```
rg -n 'created_at"[^,]*[^Z0-9"]"' payloads/*.json   # offset-less values
```
5. Normalize to UTC for storage and comparison, but keep the offset if it is evidence:
```python
utc = d.astimezone(timezone.utc)
```
6. Watch the `+0000` vs `+00:00` and `-0000` forms: `%z` accepts both, but `-0000` semantically means "unknown offset" in some producers.
7. Round-trip test a mixed fixture of every accepted shape before shipping.

## Pitfalls

- `datetime.fromisoformat("2026-03-01T14:00:00Z")` raises on Python < 3.11; code that "worked" in one environment fails in another.
- `pandas.to_datetime` with `utc=False` on a mix of `Z` and offsetless strings yields object dtype; arithmetic then errors or silently drops rows.
- JavaScript `Date.parse("2026-03-01 14:00:00")` is implementation-defined; Safari and Node can disagree by hours.
- Dropping fractional seconds reorders events logged within the same second; keep microseconds or use a sequence number.
- Truncating `+05:30` to `+05` shifts India by 30 minutes with no error anywhere.

## Verification

```
python3 -c "from datetime import datetime; [print(repr(s), datetime.fromisoformat(s.replace('Z','+00:00'))) for s in ['2026-03-01T14:00:00Z','2026-03-01T14:00:00+05:30','2026-03-01T14:00:00.123Z']]"
```
All three parse to offset-aware datetimes with distinct UTC instants = the parser is preserving offsets. Report: "parser accepts Z / +hh:mm / fractional; offset-less input raises; mixed fixture round-trips."
