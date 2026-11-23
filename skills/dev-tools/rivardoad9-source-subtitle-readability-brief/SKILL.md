---
name: subtitle-readability-brief
displayName: "Subtitle Readability Brief"
version: "1.0.0"
description: "Plan subtitle specs before transcribing or burning captions — CPS limits, line breaks, timing gaps, SRT/VTT rules, SDH cues, and platform targets for readable on-screen text."
triggerKeywords:
  - subtitle readability
  - caption timing plan
  - srt vtt guidelines
  - subtitle line length
  - characters per second subtitles
  - burn in subtitle plan
  - accessibility captions brief
  - sdh subtitle rules
  - subtitle qc before export
  - youtube subtitle specs
tags:
  - subtitle
  - youtube
  - transcribe
  - video
  - caption
license: "MIT"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Subtitle Readability Brief

## Purpose

Produce a **subtitle readability brief** before transcription, translation, or ffmpeg burn-in. Competitor skills **download, transcribe, or render** subtitles — this skill defines **how they should read on screen** so output isn’t too fast, too long, or inaccessible.

Does **not** run ffmpeg, Whisper, or download video. Planning only.

## When to use

Use when:

- Preparing captions for YouTube, Bilibili, TikTok, course video, or social clips
- Translating or adapting subtitles across languages
- Burning hardsubs (e.g. Chinese via Pillow/ffmpeg workflows)
- User asks about SRT/VTT format, CPS, line length, or SDH

## Safety and boundaries

**Do not** reproduce copyrighted dialogue from proprietary scripts unless the user provides the text.

**Do not** claim broadcast/legal compliance — note platform-specific limits; user verifies for their jurisdiction.

**Sensitive content:** flag if verbatim captions could harm privacy; recommend redaction.

## Required inputs

1. **Platform** — YouTube, Bilibili, Instagram, broadcast, internal LMS, other.
2. **Language(s)** — source and target if translation.
3. **Audience** — general, children, SDH/deaf/hard-of-hearing, ESL.
4. **Video type** — talking head, fast-cut montage, tutorial screencast, drama.
5. **Duration** — approximate length or “per 60s clip.”
6. **Style** — verbatim, clean verbatim (um removed), summarised.

## Default readability targets

Adjust in output; cite platform if known:

| Rule | Typical target |
|------|----------------|
| Max chars per line | 32–42 (Latin); fewer for CJK if dense |
| Max lines on screen | 2 |
| Max CPS (characters/sec) | 15–17 adult; 12–14 children |
| Min display time | 1.0s (0.83s absolute min for short tags) |
| Gap between cues | 2–4 frames minimum when cutting |

CJK: count **characters**; Latin: count **characters including spaces** per platform convention — state which you use.

## Workflow

1. Confirm platform + language + audience.
2. Set numeric limits (table above, tuned).
3. Define **line-breaking rules** (punctuation, clause boundaries, no orphan words).
4. Specify **SDH needs** (speaker IDs, `[music]`, sound effects) if applicable.
5. Output brief + sample cue rewrite if user provides a raw line.

## Output format

### Subtitle readability brief — {platform / language}

| Field | Value |
|-------|-------|
| Platform | … |
| Languages | … |
| Audience | … |
| Style | verbatim / clean / summary |
| Max chars/line | … |
| Max lines | … |
| Max CPS | … |
| File format | SRT / VTT / ASS / burn-in |

#### Timing rules

Bullets: min duration, max duration, reading speed exceptions for title cards.

#### Line-breaking rules

How to split long sentences; forbidden breaks (e.g. between article and noun).

#### SDH / accessibility

What to tag; speaker labels; when to describe audio.

#### Translation notes (if applicable)

Register, honorifics, reading speed in target language, expansion factor (~10–20% EN→DE).

#### QC checklist (before publish)

- [ ] No cue &gt; max CPS at display duration
- [ ] No more than max lines
- [ ] No overlap between cues
- [ ] Punctuation consistent
- [ ] On-screen text matches safe area (platform margin notes)

#### Sample cue (optional)

If user gave raw text, show one **before → after** cue with timestamps placeholder.

```srt
1
00:00:01,200 --> 00:00:04,000
First line within limits
Second line if needed
```

## Quality bar

- **Numbers are explicit** — not “keep lines short.”
- **Platform-aware** — call out YouTube vs short-form vertical differences.
- **Executor-ready** — ffmpeg/transcriber skills can apply limits directly.
- **Accessibility** — SDH section never skipped when audience needs it.

## Examples

**Good rule:** “Max 42 characters per line, max 17 CPS, break at clause commas, never split `don't` across lines.”

**Bad rule:** “Make subtitles readable.”

**Good SDH note:** “Prefix non-visible speaker changes with `>> ` and tag `[phone ringing]` for off-screen audio.”
