# Transcript from the YouTube panel (datacenter IP)

Verified end-to-end on a headless VPS where `yt-dlp --write-auto-subs`, `youtube_transcript_api`, the
`timedtext` endpoint and Invidious caption bodies all return nothing. This path returned a complete
1h19m transcript (715 segments, 85k chars) in one browser session.

Start here, not with transcript-aggregator sites: those either bot-wall (Cloudflare) or render an
empty JS shell, and each attempt costs a round trip.

## 1. Open the watch page in the real browser

```python
new_tab("https://www.youtube.com/watch?v=<ID>")
wait_for_load()
```

The page can render with a `Sign in to confirm you're not a bot` strip. That strip blocks the
**player** (duration = NaN), not the transcript panel — keep going.

## 2. Expand the description, locate the button

```python
js("(() => { const e=document.querySelector('#expand'); if(e) e.click(); return true; })()")
js("(() => Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim().toLowerCase() === 'show transcript').length)()")
```

Several duplicates exist (hidden ones included). Click the first by exact `innerText`, not by class.

## 3. Collect the panel in a scroll loop

The panel is virtualized: only a slice of segments is in the DOM at any moment, so reading it once
gives you the first ~6 segments. Accumulate `innerText` into a dedupe set while pushing the scroller
to the bottom; stop after ~3 iterations with no growth.

```python
seen, prev, stall = set(), 0, 0
for i in range(45):
    js("""(() => {
      const p = document.querySelector('ytd-engagement-panel-section-list-renderer[target-id*=transcript]');
      if (p) { p.scrollTop = p.scrollHeight; }
      return true;
    })()""")
    time.sleep(1.2)
    t = js("(() => { const p=document.querySelector('ytd-engagement-panel-section-list-renderer[target-id*=transcript], ytd-transcript-renderer'); return p ? p.innerText : ''; })()")
    for line in (t or "").split("\n"):
        if line.strip(): seen[line.strip()] = True
    if len(seen) == prev:
        stall += 1
        if stall >= 3: break
    else:
        stall, prev = 0, len(seen)
```

Notes that cost time:

- The scroller element **varies by page variant**: `ytd-engagement-panel-section-list-renderer[target-id*=transcript]`,
  `ytd-transcript-renderer #segments`, and the panel's `#content` all appear in different rollouts and any of them can
  return null on a given day. Do not conclude a selector is "gone" — scroll every candidate that resolves, then read
  the container `innerText`. A loop wired to one selector that happens to be null looks identical to a stalled loop.
- Per-segment selectors (`ytd-transcript-segment-renderer`) exist on some variants and not others; reading the panel's
  `innerText` is the version-independent path and is what the parser in step 4 expects.
- Four iterations were enough for a 1h19m video; 45 is a safe ceiling.

## 4. Parse into timestamped lines

Panel text interleaves three line shapes: `mm:ss` (segment start), a verbose duration
(`1 hour, 18 minutes, 44 seconds`), then the text.

```python
import re
ts_re = re.compile(r"^\d{1,2}:\d{2}(?::\d{2})?$")
verbose = re.compile(r"^(\d+ (second|minute|hour)s?(, )?)+$", re.I)
# timestamp line starts a segment; drop verbose lines; append other lines to the current segment
```

Dedupe consecutive segments by their first 60 chars: scrolling re-emits overlapping rows.

## 5. Sanity check before trusting it

The last timestamp must equal the video duration (read it from the page body), and segment count
should scale with length (~9 segments/minute in speech). If the last timestamp is minutes short, the
scroll loop stopped early — rerun step 3 with more iterations rather than assuming the rest is
missing.

Auto-captions garble names, tickers and numbers. Treat every figure as a claim to re-verify against
live data, and quote verbatim only after checking the number appears consistently in context.
