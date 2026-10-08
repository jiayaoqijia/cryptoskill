---
name: build-an-incident-timeline-from-timestamps
description: Use when reconstructing an incident — merges deploy, alert, log and chat timestamps into one UTC-ordered, source-tagged timeline before any narrative is written.
---

# Build an incident timeline from timestamps

Postmortems go wrong when the story is written before the facts are ordered. Build the timeline first: every event with its source and a UTC timestamp, sorted. The narrative then falls out of the gaps.

## Procedure

1. Fix the timezone first. Convert everything to UTC and record the source clock for each line. A timeline mixing local pod time with UTC chat time is worse than no timeline.

2. Pull machine events into one tab-separated file, one event per line, `ts<TAB>source<TAB>event`:
       kubectl get events --sort-by=.lastTimestamp \
         -o custom-columns=TIME:.lastTimestamp,REASON:.reason,MSG:.message > k8s-events.tsv
       git log --since="6 hours ago" --pretty='%cI%x09git%x09%h %s' >> timeline.tsv

3. Add human events from chat and ticket exports with their own timestamps:
       jq -r '.[] | "\(.ts)\tslack\t\(.user): \(.text)"' incident-export.json >> timeline.tsv

4. Include observability markers: the first alert fired and the metric-deviation onset. The onset usually precedes the alert by minutes, and that gap is itself a finding:
       curl -s 'localhost:9090/api/v1/query?query=rate(err[1m])>0.02&time=<T0-1h>'

5. Sort, dedupe, and clamp to the incident window ± 30 min:
       sort -k1,1 timeline.tsv | awk '!seen[$0]++' > timeline-sorted.tsv

6. Mark two anchors explicitly: `T0` is the first customer impact (not the first alert); `Tresolved` is when impact ended (metric back under threshold, not "we stopped looking"). Derive MTTD = T0→alert, MTTM = alert→mitigation, MTTR = T0→Tresolved.

7. Leave gaps visible. "07:14 deploy, 07:31 alert" is a 17-minute blind spot worth naming; filling it with prose hides a missing detection.

## Pitfalls

- Pulling timestamps from unsynchronised clocks without noting skew — 30 s of node skew reorders events and invents causality.
- Using the deploy time as the cause without evidence. Mark causal claims as hypotheses on separate lines from the fact lines.
- Taking T0 as the alert time, which understates customer impact and flatters the SLO.
- Mixing local browser or chat display time with UTC server time in a single column.

## Verification

    wc -l timeline-sorted.tsv                             # sum of sources minus dupes
    awk -F'\t' '{print $1}' timeline-sorted.tsv | sort -c  # sorted ascending
    grep -c 'T0\|Tresolved' timeline-sorted.tsv           # both anchors present

Report: event count by source, the two anchors with MTTD/MTTM/MTTR, and the single largest unexplained gap named as a detection finding.
