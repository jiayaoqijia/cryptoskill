---
name: agent-reach-channels
version: 1.0.0
author: Hermes Agent
description: Use when a task needs YouTube search or X/Reddit reads.
license: MIT
metadata:
  hermes:
    tags: [youtube, twitter, reddit, scraper, agent-reach, vps]
    related_skills: [external-repo-vetting, youtube-content, clipping-content]
---

# Agent Reach channels (this VPS)

## When to Use

Use when a task needs: a YouTube search without the Data API, video metadata/subtitles for
clipping or research, or reading/searching X/Twitter and Reddit from this server. Do NOT use for
generic web reading or search — Hermes' own `web_extract` / `web_search` already cover those.

Agent-Reach (`github.com/Panniantong/Agent-Reach`, MIT, ~98k stars) is an installer + doctor +
router, **not a scraper**: it picks a backend per platform and the work is done by upstream tools
(yt-dlp, gh, twitter-cli, rdt-cli, OpenCLI, Jina Reader, feedparser).

Install location on this box (persistent, outside scratch):

| Path | What |
|------|------|
| `~/.agent-reach/venv` | uv venv (Python 3.12) with yt-dlp, agent-reach CLI, twitter-cli |
| `~/.agent-reach/src` | repo clone (for `doctor`, updates, reading docs/install.md) |
| `~/.agent-reach/venv/bin/agent-reach` | health check per channel |
| `~/.agent-reach/venv/bin/yt-dlp` | YouTube search + metadata |
| `~/.agent-reach/venv/bin/twitter` | X/Twitter read+search (needs cookies) |

## Commands that are verified working

```bash
YT=~/.agent-reach/venv/bin/yt-dlp
# search without any API key (flat = fast, titles only)
$YT --no-warnings --flat-playlist --print "%(title)s | %(channel)s" "ytsearch5:<query>"
# video metadata (no download)
$YT --no-warnings --skip-download --print "%(title)s|%(upload_date)s|%(duration)s|%(view_count)s" "<url>"
# channel status (output is Chinese by default)
~/.agent-reach/venv/bin/agent-reach doctor
```

`ytsearch` is the cheapest way to find source videos for clipping/content research without the
YouTube Data API. `--flat-playlist` avoids resolving every video (much faster).

## Channel status on THIS VPS (verified by running)

Working, zero config: Jina Reader (web to markdown), RSS, V2EX, Bilibili search (basic), gh CLI,
YouTube search + metadata, `ytsearch`.

Broken/blocked here:

1. **YouTube subtitle download is bot-gated from this IP** — `--write-auto-subs` fails with
   "Sign in to confirm you're not a bot" and silently writes no `.vtt`. Metadata + search still work.
   Do not treat that as "no transcript available": the transcript panel on the watch page loads in the
   real browser even while the player is gated. Use the browser-transcript-panel reference inside the
   `youtube-content` skill before reaching for cookies or a proxy. Never promise a
   transcript from yt-dlp until a `.vtt` file actually appears on disk.
2. **X/Twitter and Reddit have no zero-config path.** `twitter search` without cookies fails with
   "make sure you are logged into x.com in your browser". Requires user-owned cookies.
3. Any channel needing Chrome (OpenCLI: Reddit/Facebook/Instagram/Xiaohongshu subtitles) is dead
   here — this box is headless.

## Verify an X post without API or cookies (re-verified 31 Okt 2026)

Buat konfirmasi "user beneran sudah posting", `api.vxtwitter.com` dan `api.fxtwitter.com` dua-duanya
keyless dan hidup; coba vxtwitter dulu karena JSON-nya datar, fxtwitter cadangan karena membungkus
semuanya di objek `tweet`. Rantai yang jalan di box ini:

```bash
# 1) dapat post id dari timeline (Jina Reader, keyless). WAJIB bust cache, lihat pitfall di bawah
TS=$(date +%s)
curl -s "https://r.jina.ai/https://x.com/<handle>?ts=$TS" | grep -o 'x.com/<handle>/status/[0-9]*'
# 2) metadata per post — vxtwitter: field datar
curl -s 'https://api.vxtwitter.com/<handle>/status/<id>'
#    pakai date_epoch atau text; cek teksnya mengandung tag + nomor yang diharapkan
# 2b) cadangan fxtwitter — semuanya di dalam objek `tweet`
curl -s 'https://api.fxtwitter.com/<handle>/status/<id>'
#    pakai tweet.created_timestamp (epoch) atau tweet.created_at ("Thu Oct 29 13:45:56 +0000 2026")
#    tweet.replying_to != null  -> itu reply, bukan post baru
# 3) cadangan terakhir: oembed, dapat teks + tanggal tapi tanpa jam
curl -s 'https://publish.twitter.com/oembed?url=https://twitter.com/<handle>/status/<id>&omit_script=1'
```

Pitfall yang bikin alarm palsu: kalau verifikasi gagal (HTTPError), jangan anggap "belum posting" —
itu bikin cron nag terus walau user sudah posting. Log kegagalan lalu keluar senyap, biarkan cron
pengingat generik yang jaga. Id pertama di halaman timeline bisa post pinned: ambil beberapa id dan
pilih timestamp paling baru, bukan ids[0].

**Timeline Jina bisa balik versi cache yang belum memuat post hari ini.** Gejalanya: user bilang
"done", tapi id terbaru yang kebaca masih post kemarin — lalu jawabannya jadi "nggak bisa verifikasi"
padahal postnya ada. Selalu tambahkan `?ts=$(date +%s)` di URL profil (atau header `x-no-cache: true`)
sebelum menyimpulkan apa pun, dan kalau id terbaru tetap lebih tua dari yang diharapkan, bilang
"cache-nya stale" — jangan bilang postnya tidak ada.

## Redundant here (do not install)

Jina Reader and Exa search duplicate Hermes' own `web_extract` / `web_search` (TinyFish provider).
V2EX, Bilibili, XiaoHongShu, Xueqiu, Boss直聘 are China-platform channels with no use for this user.

## Pitfalls

- A venv inside `~/.hermes/cache/scratch` is pruned after 24h — always install to `~/.agent-reach/`.
- `uv venv` ships no `pip`. Install with `uv pip install --python <venv>/bin/python <pkgs>`
  (`export PATH=~/.hermes/bin:$PATH` first). There is no pipx on this box.
- Upstream CLIs are third-party, young, and some are stale: twitter-cli (last push May 2026),
  rdt-cli has no license (created Mar 2026). If X changes its API, expect breakage — re-test before
  trusting, and never build a scheduled job on top of them without a health check.
- The repo's install guide is written for an agent to execute: it forbids `sudo`, writes only under
  `~/.agent-reach/`, and defaults to a read-only check (`install --env=auto`). `--system` must never
  run without explicit user approval; `--dry-run` shows what it would do.
- The README carries an explicit "no token/crypto affiliation" warning: any coin or fee-claim
  program using the Agent Reach name is a scam.

## Cookie channels (X / Reddit) — procedure if the user approves

Never type a password and never accept cookies in chat. Working agreement with this user:

1. User creates a **secondary** X account for research (main account stays out — cookies grant full
   account access and non-browser API access risks a ban).
2. Cookies come from the Cookie-Editor browser extension → Export → Header String, and the user
   pastes them **into a file on disk** (mode 600), not into the chat.
3. `twitter-cli` reads `TWITTER_AUTH_TOKEN` / `TWITTER_CT0` from the environment at call time; set
   them inline for the call, never export them into a persistent profile file.
4. Reddit on a server = `rdt-cli` + cookie (anonymous endpoints are blocked, no zero-config path).

## Updating

```bash
cd ~/.agent-reach/src && git pull --depth 50
~/.hermes/bin/uv pip install --python ~/.agent-reach/venv/bin/python ~/.agent-reach/src
```
