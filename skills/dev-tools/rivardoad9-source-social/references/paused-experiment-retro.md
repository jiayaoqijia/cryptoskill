# Retro of a paused posting experiment (Threads case)

Use when the user asks "how did that automation we ran actually perform" for a social lane that has
been paused for weeks. The report is a reconstruction from local artifacts, not a vibe summary — every
number must trace to a file, an API response, or the public profile.

## Where the evidence lives

- `~/.hermes/threads_outreach/post_results.log` — one block per run (`=== Promo <ts> ===`) with
  `OK MAIN -> media_id=…`, `TEXT: …`, `LINK: …`, and `OK <id> -> … is_reply=true` per reply. Count
  published posts (`OK MAIN`), replies (`is_reply=true`), and real failures from this file.
- `~/.hermes/threads_outreach/commented.json` — flat list of post IDs that received an outreach
  comment (no timestamps: it gives volume, not cadence).
- `~/.hermes/threads_outreach/auto_clarify.log` — inbound comments detected on own posts; the only
  place an organic question from a stranger shows up.
- `~/threads_engagement.md` / `~/threads_analysis.md` — per-post engagement snapshots and the full
  text archive. Snapshots are point-in-time; say so instead of implying they are current.
- The cron jobs themselves (`hermes cron list`) give the cadence and the exact pause date.

## Reading the numbers honestly

- Median and max per-post views beat averages; one outlier carries the average.
- Split posts by intent before judging: promo vs shareable fact vs story. Aggregate engagement across
  mixed intents answers nothing.
- **No per-post attribution = no sales claim.** A generic store link (`lynk.id/<user>`) cannot tell you
  which post converted. Report "zero attributable" and name the measurement gap as a finding; do not
  dress up silence as failure or success.
- Reply/outreach volume is not performance. Report the conversion: comments sent → inbound questions.
  A 1-2% reply rate from a few hundred comments is the realistic ceiling and worth stating plainly.

## When the Graph API token is expired

A 400 `OAuthException` / "Session has expired" is expected for a lane paused past the 60-day token
life. Do not retry and do not report the lane as broken. For a last-known public figure, fetch the
profile with a crawler UA and regex the embedded JSON:

```python
req = urllib.request.Request("https://www.threads.net/@<handle>",
                             headers={"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"})
h = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
re.findall(r'"follower_count":(\d+)', h)   # also: meta og:description → "N Followers • M Threads"
```

That yields follower count, total threads, and recent like counts without auth — enough for a retro,
not enough for per-post reach. Say which one you are quoting.

## Findings that generalize to small accounts

- Posting volume into a near-zero-follower audience does not create reach; the account needs one post
  that escapes before frequency matters.
- Screenshot-able facts (price comparisons, survey numbers, "turns out the opposite is true") travel;
  direct promo sits at single-digit views. Keep promo at ~10% of the mix, not the majority.
- Outreach converts better than posting but at a low rate, and at high volume it reads as spam and
  invites platform limits. Cap it (~10/day), keep it relevant and human.
- Technical reliability is not success: a lane can post 100+ items with a 99% success rate and still
  produce zero business outcome. Report both, separately.

## Reboot checklist (before resuming any paused lane)

1. Re-auth and store the token with its expiry; add a cron reminder ~7 days before expiry (a silent
   token death looks identical to a broken job).
2. Cut cadence to 1 post/day and rebalance the mix toward shareable content.
3. Give every post a unique tracked link (or a redirect with a per-post parameter) so clicks become
   attributable.
4. Log daily views/likes/replies to SQLite so the next retro has time series, not one snapshot.
5. Write the kill criteria into the job description before enabling: e.g. "30 days with no post above
   N views and zero attributed clicks → pause again". An experiment without a stop rule just becomes
   background noise.
