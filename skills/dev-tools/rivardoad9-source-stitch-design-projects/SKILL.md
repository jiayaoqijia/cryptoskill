---
name: stitch-design-projects
description: "Build or recreate UI screens in Google Stitch via MCP."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [stitch, mcp, ui, design, figma, html]
    related_skills: [design-md, figma-design-review, ai-ui-mockups]
---

# Stitch design projects

## When to use

Use when the user wants a UI built or recreated in Google Stitch: "bikin di Stitch", "recreate
Figma ini di Stitch", "kasih link project Stitch". Not for building a web app — Stitch is a design
tool; the deliverable is a project of screens the user can open and edit.

## Access

Stitch is reached over MCP at `https://stitch.googleapis.com/mcp` with an API key in
`X-Goog-Api-Key`. The key lives in `~/.hermes/secrets/stitch_api_key` (mode 600). Register it in
`~/.hermes/.env` as `STITCH_API_KEY` and reference `${STITCH_API_KEY}` in the `mcp_servers:` block of
`config.yaml`; never print the key back to chat.

**An MCP server added to config mid-session is not registered as a tool until the gateway
restarts.** Do not conclude the capability is missing: call the endpoint directly with JSON-RPC
(`scripts/stitch_rpc.py`) while the config change waits for a restart.

## Procedure

1. **Create the project** and hand the user the link immediately — that is usually the real question.
   `create_project {title}` returns `name: projects/<id>`; the URL is
   `https://stitch.withgoogle.com/projects/<id>`.
2. **Seed the design system with `upload_design_md {projectId, designMdBase64}`.** Write DESIGN.md
   with the user's tokens first (see `design-md`); Stitch uses it as the source of truth for type,
   color and radius. It returns a screen instance used as the preview.
3. **Create each screen with `generate_screen_from_text {projectId, prompt, deviceType: MOBILE}`.**
   There is no import-a-screen call: a screen must exist before it can be updated. Reuse an existing
   `designSystem` asset id on later calls so the model does not drift.
4. **Overwrite the HTML with `update_screen` and push the screenshot in the same call.**
   `update_screen {name, htmlCodeBase64, screenshotBase64, updateMask:["html_code","screenshot"]}`.
   HTML alone is not enough: the project keeps showing the generated preview until `screenshotBase64`
   replaces it, which reads to the user as "bedanya design" — the screen visibly does not match.
   Render your own HTML to PNG at the frame size first (headless Chromium, scale 2), push both, then
   re-download the screen screenshot and compare hashes: equal hash = the user sees your design. Encode the HTML base64 (UTF-8) and keep one self-contained
   document per screen: inline CSS, no external fonts beyond a Google Fonts link, no local file paths.
5. **Verify each screen** with `download_file` on the screen's `screenshot.name` (or open the project
   URL) before moving on. A 200 from `update_screen` is not a rendered screen. The file is JSON with a
   base64 `dataString`, not a raw PNG — decode before viewing or the image reader rejects it.
6. **Batch.** One screen per call is the norm; report progress per batch rather than promising all of
   them at once. Keep the generated HTML in a working dir so a failed push can be retried without
   regenerating.

## Figma as the source

See `references/figma-to-stitch.md` for the extraction recipe (tokens, frames, PNG export, the
rasterized-text trap) and the fidelity order that survives review.

## Numbered rules that came from real attempts

1. **`create_design_system_from_design_md` is not guaranteed by `projectId` + `deviceType` alone** —
   a call with only those returned `Request contains an invalid argument`. Read its full input schema
   (`tools/list`), check `list_design_systems` afterwards, and treat the `upload_design_md` step as the
   part that definitely lands.
2. **Frame size is a hard constraint.** Set the HTML body to the user's frame (e.g. 390×844) and let
   content overflow vertically; do not let the document grow wider or Stitch shows a shrunken page.
3. **Every interactive control needs its states drawn,** not just the happy path: checkbox checked and
   unchecked, switch on/off, radio selected/unselected, button default/pressed/disabled/loading, field
   empty/filled/focus/error/disabled, badges success/pending/failed. The user asks for this explicitly
   because their Figma usually stops at the default state.
4. **Copy comes from the design, not from imagination.** Recreating a screen means the same strings,
   same numbers, same labels. If a label is unreadable, say so instead of inventing plausible text.
5. **No device chrome.** Do not draw the phone status bar (time, signal, battery) or the home
   indicator: the screen starts at the app header. Do's standing rule for every mockup.
5. **Never publish or share a Stitch project without being asked.** Default visibility is private;
   leave it that way.

## Verification

- Project exists and is owned by the user: `get_project {name: "projects/<id>"}` → `sharingSettings`
  shows their email as `OWNER`.
- Screen count grows as batches land: `list_screens {projectId}`.
- The pushed HTML round-trips: `download_file` the `html_code` file and diff the first lines against
  what you sent.
- Screenshot, not JSON, is the proof the design looks right.
