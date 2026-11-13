---
name: series-design
domain: crypto-trading/series-design
trigger: "What makes a usable series: the 168-cell dowxhour notional example (one daily call, ~20 min/month); pre-registering the analysis BEFORE collecting; UTC discipline; units and aggregation rules."
anti_trigger: "Not for the analysis itself, not for the trade record or risk budget."
scope: "What makes a usable series: the 168-cell dowxhour notional example (one daily call, ~20 min/month); pre-registering the analysis BEFORE collecting; UTC discipline; units and aggregation rules."
status: seedling
---

# Series Design

## Standard
Building rigorous financial data series requires disciplined schema design, precise UTC temporal alignment, and pre-registered aggregation rules before data collection commences. Usable series eliminate ambiguity around timezone conversions, sampling frequency, and floating-point precision, enabling reproducible empirical research such as the 168-cell day-of-week by hour notional matrix.

Primary sources for the claims in this step: <https://pandas.pydata.org/docs/user_guide/timeseries.html> and <https://www.iso.org/iso-8601-date-and-time-format.html>.

## Decision rules
- **UTC temporal standard:** All timestamps within stored series must be strictly recorded and indexed in Coordinated Universal Time (UTC) using ISO 8601 format without local timezone offsets.
- **Pre-registered schemas:** Data series dimensions, aggregation windows, and metrics must be defined in a pre-registered configuration file before ingestion begins.
- **Efficient polling design:** Series collection schedules must balance temporal resolution against storage costs and rate limits (e.g., executing one daily aggregation call or hourly snapshot rather than excessive high-frequency polling where unwarranted).
- **Explicit unit declarations:** Every numerical column must declare its exact unit denomination (e.g., USD notional, native asset tokens, basis points, or funding rate decimals).

## Procedure
1. Define the analytical objective and specify the required temporal granularity (e.g., 168 cells representing 7 days times 24 UTC hours).
2. Author a schema definition document detailing column names, data types, unit scales, and primary keys.
3. Configure collection daemons to aggregate or sample raw feeds directly into the pre-registered schema format.
4. Establish automated validation scripts to check incoming data frames against schema constraints prior to disk persistence.
5. Execute trial collection runs for a limited window to verify storage layout, file naming conventions, and query performance.
6. Lock the series design configuration, prohibiting arbitrary schema modifications mid-collection.

## Anti-patterns
- **Local timezone contamination:** Storing timestamps with local system offsets or ambiguous timezone identifiers.
- **Ad-hoc schema evolution:** Altering column names or unit scales mid-stream without version migration scripts or documentation.
- **Unbounded floating-point precision:** Storing monetary values or rates as raw floating-point numbers subject to rounding errors instead of fixed-point representations.
- **Post-hoc metric definition:** Designing aggregation formulas after data collection has concluded, introducing researcher degrees of freedom.

## Done checklist
- [ ] All timestamps are stored and indexed strictly in UTC format.
- [ ] Series schemas, dimensions, and unit definitions are pre-registered in configuration files.
- [ ] Collection schedules optimize polling frequency against storage and rate-limit constraints.
- [ ] Automated schema validation enforces data integrity on every ingested frame.

## Sources
- ISO 8601 Standard. (2026). Data elements and interchange formats - Information interchange - Representation of dates and times. Retrieved from https://www.iso.org/iso-8601-date-and-time-format.html
- Pandas Documentation. (2026). Time series data structures, resampling, and timezone localization. Retrieved from https://pandas.pydata.org/docs/user_guide/timeseries.html
- Python Software Foundation. (2026). Decimal fixed-point and floating-point arithmetic. Retrieved from https://docs.python.org/3/library/decimal.html
- CoinGlass Analytics. (2026). Aggregating cryptocurrency derivatives and liquidation data into structured grids. Retrieved from https://www.coinglass.com/
