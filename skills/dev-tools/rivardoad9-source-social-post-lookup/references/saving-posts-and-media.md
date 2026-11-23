# "Simpan post ini" — saving a social post as durable evidence (14 Sep 2026)

Trigger: the user pastes a post link and says *save this* / "simpan, siapa tau jadi project kita".
Saving the URL is **not** saving the post — every media URL on Instagram/X carries an expiry
(`?oe=6AAD613F`, ~days), so a note holding only links goes blind within a week.

## What to persist

1. **Fetch the media to disk now** (`curl -sL -A "Mozilla/5.0" <media_url> -o file.jpg`) while the
   signed URL is still valid, and store it next to the note (Obsidian convention here:
   `attachments/<topic>-<n>.jpg`, embedded with `![Bukti](attachments/…)`).
2. **Store the canonical post URL, not only the share link.** Share tokens are opaque and the
   canonical form (`/@user/post/<shortcode>`) is what the user can re-open later.
3. **Transcript, don't summarise, the screenshots.** A promo post's text is the pitch; its
   screenshot holds the numbers (dashboard PnL, fee table, criteria list, address bar). Quote the
   numbers as-is, then analyse separately.
4. **Write the analysis into the same note**: what it claims, what is unverified, what it would take
   to check, and how it maps to what the user already owns. A note that is only a link + a summary
   is not worth saving.
5. **Verify the note can actually reach the user.** The vault here is git-synced, and
   `vault_sync.sh` deliberately no-ops when `origin` is missing — check
   `git remote get-url origin` in the vault before implying the note is now on their devices.

## Threads share links: Jina works (corrects the earlier pessimistic note)

`https://www.threads.com/share/<token>/` (a 9-char share code — not base64url, so the truncation
diagnostic in SKILL.md does not apply):

```bash
curl -sIL -A "<desktop UA>" "https://www.threads.com/share/<token>/"     # 200, no redirect, JS shell only
curl -s "https://r.jina.ai/https://www.threads.com/share/<token>/" -H "X-Return-Format: markdown"
```

The Jina render returned the real post: author handle, post text, the **canonical post URL**, and
every image URL. So try Jina on the share URL **first** and only ask for a Copy-link form if it comes
back as the login shell. `references/threads-instagram.md` still describes the ordering as
"share tokens are usually mangled — ask for the copied link"; this measurement supersedes that.

## X posts: the same rule, different endpoints

See `references/x-twitter.md` for the two no-login endpoints. The lesson that generalises: **when a
post's payload carries images, the images are the evidence** — download and transcribe them, and quote
the URL visible in a screenshot's address bar (one product review post was served from a `*-dev.`
hostname, which the text never mentioned).
