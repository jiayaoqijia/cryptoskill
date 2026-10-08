---
name: forecast-storage-exhaustion-and-alert
description: Use when disks fill without warning. Fits a growth rate to capacity metrics and alerts on projected time-to-full, not on a static percentage.
---

# Forecast Storage Exhaustion and Alert

A "80% full" alert fires too late on a fast-growing volume and never on a slow one that recycles. Alert on the projected time until full, derived from the observed fill rate, so there is time to act before writes fail.

## Procedure

1. Export capacity and usage over time: `df -h --output=source,pcent,target`, or Prometheus `node_filesystem_avail_bytes` / `kubelet_volume_stats_used_bytes`.
2. Compute fill rate over a stable window (7-14 days) to avoid a single backup spiking the slope: `rate(node_filesystem_avail_bytes[7d])`.
3. Project time-to-full: `predict_linear(node_filesystem_avail_bytes[7d], 30*24*3600) < 0`.
4. Alert on the projection with two horizons: warn at "full within 14 days", page at "full within 48 hours".
5. Use the same pattern for databases (`pg_database_size`), object buckets (`aws cloudwatch get-metric-statistics` on `BucketSizeBytes`), and log indices.
6. Exclude the expected sawtooth (a nightly backup that recycles) from the trend so it does not mask real growth.
7. Set a hard floor alarm too — below 5% free, alert regardless of trend, because a sudden flood defeats any projection.
8. Record the runbook action per volume: expand, tier to colder storage, or enable expiry — and who owns it.
9. Re-tune the window after a traffic change; a rate fit to pre-migration data forecasts the wrong future.

## Pitfalls

- Static thresholds: a volume growing 2%/day at 60% full is 20 days from death and the 80% alert never gives you 20 days.
- Fitting the slope including the nightly backup write burst, so every volume looks like it fills in hours.
- `predict_linear` on a short range (1h) that is dominated by noise and flaps continuously.
- Monitoring only `used%` and missing inode exhaustion, which fails writes at low byte usage — watch `node_filesystem_files_free`.
- Forgetting that a managed database reserves a copy of its size for vacuum or WAL, so "50% full" is functionally near-full.
- Alerting to a channel no one owns; an unowned capacity alert is an outage scheduled for later.
- Not re-baselining after a retention change removes the growth source, leaving a permanently firing alert that gets muted.

## Verification

    # promql: volume projected to fill within 48h
    predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[7d], 48*3600) < 0
    df -h --output=pcent / | tail -n1    # current headroom for context

The projection rule exists, fires only on genuine trends, and the runbook names the action and owner for each volume.

Report: "Added time-to-full alerts on <N> volumes (warn 14d, page 48h); current worst is <mount> at <p>% growing <r>%/day → <d> days."
