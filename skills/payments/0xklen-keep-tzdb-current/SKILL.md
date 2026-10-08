---
name: keep-tzdb-current
description: Use when a service stores or converts timezones — update and pin the IANA tz database, because governments change offsets and a stale copy silently computes the wrong instant.
---

# Keep the tz database current

Timezone rules are data, and states change them (Chile, Morocco, Kazakhstan and dozens more have moved within the last few years). A stale tz database is not a bug in your code — until a scheduled job fires an hour off — so treat tzdata like any other dependency you patch.

## Procedure

1. Find every tzdata source in the stack — OS, language runtime, container, and any vendored copy:
```
dpkg -l tzdata 2>/dev/null; pip show tzdata tzdata 2>/dev/null; python3 -c "import zoneinfo; print(zoneinfo.TZPATH)"
npm ls --all 2>/dev/null | grep -i tzdata
```
2. Check the version actually loaded, not just the installed file:
```
python3 -c "import importlib.metadata as m; print('tzdata', m.version('tzdata'))"
zdump -v America/Santiago | tail -4
```
3. Pin the data source explicitly so it does not depend on the host. In Python, install the `tzdata` wheel and prefer it over the system copy in containers:
```
pip install "tzdata>=2025.1"     # pure-Python fallback used when /usr/share/zoneinfo is absent
```
4. Update on a cadence and on news of a change; IANA publishes ~4-6 releases a year:
```
apt-get update && apt-get install -y --only-upgrade tzdata
pip install -U tzdata
```
5. Add a check that fails CI when the data is older than a threshold:
```python
import importlib.metadata as m, datetime as dt
v = m.version("tzdata")  # 2025.1 -> year 2025
assert int(v.split(".")[0]) >= 2025, f"tzdata stale: {v}"
```
6. Keep Node/Browser data in sync: browsers carry their own ICU data, so server and client can differ. Compare a known-changed rule:
```js
Intl.DateTimeFormat("en", {timeZone:"America/Santiago", timeZoneName:"short"}).format(new Date())
```
7. After any upgrade, re-run the DST test matrix and diff `zdump` output for the zones you schedule against.

## Pitfalls

- A container built with `--no-install-recommends` may ship no tzdata at all; `ZoneInfo` then silently falls back to UTC instead of erroring.
- Upgrading tzdata can change a stored business-date mapping retroactively; historical reports can shift. Freeze the rule for past periods if that matters (e.g. financial ledgers).
- Java bundles its own tzdb in the JDK; upgrading the OS package does not help the JVM until the JDK is patched.
- Locking a dependency without pinning tzdata means two builds a month apart can produce different schedules from identical code.
- Browsers update ICU on their own cadence, so a correct server can still render a stale offset client-side; the server is the source of truth.

## Verification

```
python3 -c "import importlib.metadata as m; print(m.version('tzdata'))" && zdump -v Europe/London | grep 2026 | head -2
```
A version at or above the latest IANA release and a `zdump` that shows the current 2026 transitions = the data is live. Report: "tzdata pinned at the current release, CI fails below the year threshold, zones re-checked with `zdump` after upgrade."
