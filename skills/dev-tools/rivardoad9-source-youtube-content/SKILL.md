---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs."
version: 1.0.0
author: Teknium (teknium1), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [YouTube, Video, Transcripts, Media]
    related_skills: []
---

# YouTube Content Tool

## When to use

Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, or wants to extract and reformat content from any YouTube video. Transforms transcripts into structured content (chapters, summaries, threads, blog posts).

Extract transcripts from YouTube videos and convert them into useful formats.

## Setup

Use `terminal` with the Python from a PM-prepared Hermes source checkout. The
`youtube` extra declares the helper's dependency; do not install packages into
Hermes with raw pip or project-discovering `uv run`.

From that checkout, first follow the isolated development-home setup in
[Package Management](https://hermes-agent.nousresearch.com/docs/reference/package-management#developer-workflow),
then prepare the extra and reactivate before running the helper:

```bash
source ./activate
python -c "import pm; pm.sync_venv(['youtube'], explicit=True)"
source ./activate
python -c "import youtube_transcript_api; print(youtube_transcript_api.__file__)"
```

On Windows, use `. .\activate.ps1` instead of `source ./activate`. If the terminal
runs on a different host or in a sandbox, use an explicitly isolated helper
environment there, not the agent's production environment. Run every command
below with the interpreter whose import check succeeded.

## Helper Script

`SKILL_DIR` is the directory containing this SKILL.md file. The script accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
python SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
python SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
python SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

## Output Formats

After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps
- **Process & thinking** (triggered by "pelajarin prosesnya", "cara kerjanya", "thinking-nya"): the operator's method,
  not a summary. Order: (1) hard numbers he states about himself — capital, result, loss, allocation — each with a
  timestamp; (2) his procedure as ordered steps, each with the timestamp where he says it; (3) the mental models behind
  it, one line each, with the mechanism instead of a slogan; (4) what is transferable to this user and what is not,
  stated separately; (5) 3–5 verbatim quotes that stand alone. Keep his own caveats and risk statements in the output —
  never present a trader's method as a validated strategy, and keep the distinction between "what he does" and
  "what you should do" explicit.

### Example — Chapters Output

```
00:00 Introduction — host opens with the problem statement
03:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

## Workflow

1. **Fetch** the transcript using `terminal` and the prepared Python with `--text-only --timestamps`.
2. **Validate**: confirm the output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript. If still empty, tell the user the video likely has transcripts disabled.
3. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
5. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.

## Fallback when the transcript API is blocked (cloud/datacenter IPs)

YouTube refuses `youtube_transcript_api` and the caption endpoints behind it from datacenter IPs, so on this host the
helper can return nothing even for a video whose transcript panel is fully populated. Skip the transcript-aggregator
sites (`youtubetotranscript`, `youtubetranscript`) — from a datacenter host they bot-wall or render as empty JS shells,
so they only cost round trips. Ladder that works:

1. **Read metadata in the browser first** — `goto_url` the watch page, click `tp-yt-paper-button#expand`, then read
   `#description-inline-expander` for the full description, chapters and links; title/channel/view count are in the
   page body. This alone often answers a "what does this video claim" question.
2. **Establish that captions exist** — `https://<invidious-host>/api/v1/captions/<VIDEO_ID>` still *lists* the available
   languages even when the instance refuses to serve the caption content (0-byte body). Use the language list, not the body.
3. **Open the watch page in the real browser and collect the transcript panel.** This is the primary path and it
   works even when the player is bot-gated: the "Sign in to confirm you're not a bot" strip blocks playback, not the
   transcript. Click `#expand`, click the button whose exact text is `Show transcript`, then scroll the panel
   `ytd-engagement-panel-section-list-renderer[target-id*=transcript]` to the bottom in a loop and accumulate its
   `innerText` into a dedupe set (the panel is virtualized — one read returns only the first handful of segments).
   Full recipe, selectors and parser: `references/browser-transcript-panel.md`.
4. **Only if the browser itself is blocked, delegate to the TinyFish agent with `browser_profile: "stealth"`** — goal:
   open the video, click 'Show transcript', scroll to the end, return the transcript verbatim without summarizing.
   Expect clipping: a ~20-minute video comes back cut near halfway, so the second call asks for the missing range by
   timestamp ("return the transcript from 09:30 to the end") instead of repeating the first half. A run that exceeds
   the call timeout is not a failure signal — check whether the transcript already arrived before re-running.
5. **Never trust auto-captions for names or numbers.** They mangle tickers and prices ("5 dolar" for 85, "0,56" for
   0,0056). Re-verify every level against live market data — the video's figures are claims, not quotes.

## Error Handling

- **Transcript disabled**: tell the user; suggest they check if subtitles are available on the video page.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript, then note the actual language to the user.
- **Dependency missing**: repeat PM preparation and reactivation above, then verify the helper uses that Python. Do not repair the selected generation with pip.
