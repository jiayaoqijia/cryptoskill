---
name: point-in-time-integrity
domain: investing/point-in-time-integrity
trigger: "Checking whether a dataset's history is what was known at the time."
anti_trigger: "Not for predicting returns, and not for backtest validation."
scope: "Backfill, restatement, and the difference between history and reconstruction."
status: seedling
---

# Point-in-time integrity

## Standard

A point-in-time dataset records what was observable on each date. Its opposite is a reconstructed dataset, assembled later from current records and then presented as history. The difference is decisive for any backtest: a reconstruction knows which entities survived, which values were later restated, and which relationships held, and a strategy tested on it is being tested on information that did not exist.

The most common reconstruction is the vendor who starts with today's universe and codes backwards. Every company that failed is missing, every data point reflects its final restated value, and the resulting series is cleaner than anything a participant could have seen. Testing for this requires asking when each record was first available, and checking whether the vendor can supply that field.

Primary sources: <https://www.sec.gov/investor> and <https://www.nber.org/>.

## Decision rules

- Record whether the dataset includes a first-available timestamp per record.
- Record whether the universe is the historical one at each date.
- Record whether values are as-reported or restated.
- Record any field that is present now but could not have been at the time.
- Test by comparing a sample of records with the archived original where available.
- Where point-in-time data cannot be obtained, record the leakage explicitly.

## Procedure

1. Ask for the first-available field and inspect it.
2. Check universe membership at several historical dates.
3. Compare a sample against archived sources.
4. Identify fields that are reconstructed.
5. Record the leakage and its likely direction.
6. Write the integrity assessment.

## Anti-patterns

- Accepting a history without a first-available timestamp.
- Assuming restatements are rare enough to ignore.
- Using a current index membership list as the historical universe.
- Treating a vendor's statement that data is point-in-time as verification.
- Ignoring leakage because the backtest looks reasonable.

## Done checklist

- [ ] First-available field checked.
- [ ] Universe membership checked at dates.
- [ ] Sample compared with archives.
- [ ] Reconstructed fields identified.
- [ ] Leakage direction recorded.
- [ ] Assessment written.

The clearest test is a corporate failure: take a company that no longer exists and ask the vendor for its records on the dates they were current, since a reconstructed dataset will either omit it or show values adjusted after the fact, and both are visible immediately.


## Sources

- Filing archives for point-in-time verification: <https://www.sec.gov/edgar/search/>
- Research on look-ahead bias: <https://www.nber.org/>
- Disclosure framework: <https://www.sec.gov/investor>
