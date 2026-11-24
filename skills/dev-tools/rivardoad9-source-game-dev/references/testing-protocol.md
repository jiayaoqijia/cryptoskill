# Browser Testing Protocol

Run this after implementing every single system in Phase 4/5 of `SKILL.md`,
and again in full during Phase 6 (assembly playtest). Never mark a system
`done` in `SYSTEMS.md` on code inspection alone — it must be observed
working in an actual browser.

## Step 0 — Serve the project

Make sure the dev server (Vite, etc.) is running and reachable at its local
URL before attempting any browser step. Start it in the background if it
isn't already running. Once it's up, **leave it running for the rest of the
build loop** — Vite's HMR picks up changes automatically, so there's no
need to restart it between systems. Only restart it if it actually crashes
or the config changes.

## Step 1 — Choose the browser tool

Prefer **claude-in-chrome** over Playwright when it's available — it drives
the user's real Chrome session, so what you see is exactly what they'd see,
and it doesn't require a separate headless browser install.

1. Invoke the `claude-in-chrome` skill first. It requires site-level
   permission to be granted for the local dev server's origin
   (e.g. `http://localhost:5173`) before any `mcp__claude-in-chrome__*` tool
   will work.
2. If the skill reports it's unavailable, or the required permission isn't
   granted and the user doesn't grant it when asked, **fall back to
   Playwright** instead of blocking the build loop on it. Use the
   `mcp__plugin_playwright_playwright__*` tools directly (no separate skill
   invocation needed for those).
3. Don't ask the user to choose up front — try claude-in-chrome, fall back
   silently to Playwright, and just mention once which one you're using.
4. **If neither is actually usable** (both tools unavailable, or Playwright
   isn't installed and the user doesn't want to install it) — stop. Do not
   mark the system `done` based on reading the code. Tell the user
   automated in-browser verification isn't possible right now, log the
   system as `pending` with that note in `SYSTEMS.md`, and ask them to
   either enable one of the two tools or manually verify the system
   themselves before you continue to the next one.

## Step 2 — The per-system test cycle

For the system just implemented:

1. Navigate to the dev level's route/entry for that system (see
   `references/dev-level.md` for how the dev level exposes per-system
   entry points).
2. Exercise the system the way a player actually would: send the real
   input it responds to (key presses for movement/jump, clicks/taps for
   shooting or UI, drag for touch gestures, etc.) — don't just load the
   page and assume it works from a screenshot of the idle state.
3. Take a screenshot (or a couple, before/after the interaction) to
   visually confirm the expected change happened.
4. Read the browser console. Any error or warning tied to the system under
   test is a failure, even if the visual looked right.
5. Compare what happened against what `GAME_SPEC.md`/`SYSTEMS.md` say this
   system should do. "Nothing crashed" is not the bar — the specific,
   expected behavior must be observed.
6. **Pass:** log a short note in `SYSTEMS.md` (what was tested, what was
   observed) and mark the system `done`.
   **Fail:** fix the implementation and repeat this cycle on the same
   system. Do not proceed to the next system in a failing state.

## Step 3 — Full playtest (Phase 6 only)

Once every system is individually `done`:

1. Play through actual assembled content start-to-finish using the chosen
   browser tool, not just the dev level in isolation.
2. If multiple platforms were declared in `GAME_SPEC.md` (mobile + desktop),
   repeat the playthrough simulating each input mode — touch/tap sequences
   for mobile, keyboard/mouse for desktop. Don't assume one input mode's
   pass implies the other works.
3. Record findings in `PLAYTEST.md`: what worked, what broke, anything that
   felt off even if technically functional (timing, feel, unclear UI).

## Notes on tool mechanics

- Playwright's `browser_console_messages` and `browser_network_requests`
  are useful for catching silent failures (a failed asset fetch, a thrown
  exception that didn't visibly break rendering).
- Prefer `browser_snapshot`/accessibility-tree inspection over screenshots
  alone when checking DOM-based UI (e.g. a word game's letter grid) — it
  catches state that a screenshot can miss.
- When using claude-in-chrome, remember it's driving the user's real
  browser session — avoid leaving many stray tabs open; close what you open
  once a test cycle is done.
