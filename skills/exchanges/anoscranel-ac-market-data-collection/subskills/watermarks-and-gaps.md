---
name: watermarks-and-gaps
domain: crypto-trading/watermarks-and-gaps
trigger: "Watermarking on max(last_as_of); gap detection; backfill policy; how a silent gap corrupts a study (and how to prove a series is gap-free)."
anti_trigger: "Not for the analysis itself, not for the trade record or risk budget."
scope: "Watermarking on max(last_as_of); gap detection; backfill policy; how a silent gap corrupts a study (and how to prove a series is gap-free)."
status: seedling
---

# Watermarks and Gaps

## Standard
Continuous market data series require strict watermark tracking based on `max(last_as_of)` timestamps to prevent temporal misalignment and missing records. A robust pipeline maintains explicit watermark state, performs automated gap detection across expected polling intervals, and executes deterministic backfill procedures when temporal discontinuities are identified. Proving a dataset is gap-free is a mandatory prerequisite for quantitative research.

Primary sources for the claims in this step: <https://bybit-exchange.github.io/docs/v5/intro> and <https://kafka.apache.org/documentation/>.

## Decision rules
- **Watermark definition:** The pipeline watermark must track `max(last_as_of)` across successfully persisted records, representing the exact high-water mark of ingested temporal coverage.
- **Gap detection threshold:** Any temporal delta between consecutive records exceeding `1.5 * polling_interval` triggers an automated gap alert and initiates backfill protocols.
- **Append-only backfill:** Backfilled data frames must be inserted into their chronological storage partitions without altering existing watermark sequences until fully verified.
- **Silent gap prohibition:** Datasets containing unmitigated temporal gaps cannot be used for high-precision econometric studies or cascade forensics without explicit missingness documentation.

## Procedure
1. Inspect the ingestion directory and parse all available data files to extract exchange timestamps and receipt timestamps (`last_as_of`).
2. Sort records chronologically and compute time deltas between adjacent sampling points across the entire series.
3. Identify all intervals where the delta exceeds the pre-registered maximum allowable polling threshold.
4. Query upstream historical endpoints specifically for the identified missing temporal windows.
5. Ingest backfilled payloads, verify their exact coverage of the missing window, and append them to storage.
6. Re-run chronological validation to confirm zero remaining gaps before declaring the dataset gap-free.

## Anti-patterns
- **Relying on system time:** Using local collection machine clock time instead of exchange-reported timestamps or strict receipt watermarks (`last_as_of`).
- **Overwriting historical files:** Inserting backfilled records by editing past files rather than maintaining chronological partition integrity.
- **Ignoring small gaps:** Disregarding minor multi-minute gaps in high-frequency series that may coincide with crucial liquidation cascade events.
- **Unverified backfills:** Assuming backfill API calls returned complete data without verifying record counts and temporal boundaries.

## Done checklist
- [ ] Watermark state accurately tracks `max(last_as_of)` across all ingested data partitions.
- [ ] Automated gap detection scans series and flags temporal deltas exceeding polling thresholds.
- [ ] Backfill procedures retrieve missing windows and integrate records without modifying past files.
- [ ] Final validation confirms complete chronological continuity and zero silent gaps.

## Sources
- Apache Kafka Documentation. (2026). Stream processing watermarks and event-time tracking semantics. Retrieved from https://kafka.apache.org/documentation/
- TimescaleDB Documentation. (2026). Managing hyper-tables, time-series gaps, and temporal interpolation in financial datasets. Retrieved from https://docs.timescale.com/
- Bybit Exchange. (2026). WebSocket sequence numbers and gap detection best practices. Retrieved from https://bybit-exchange.github.io/docs/v5/intro
- CoinGlass Analytics. (2026). Handling API timestamp anomalies and historical data reconstruction. Retrieved from https://www.coinglass.com/
