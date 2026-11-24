---
name: game-dev
description: >-
  Use when the user wants to build, prototype, or architect a 2D browser
  game — e.g. "make a game", "build a platformer/shooter/word game/stickman
  game", "let's build a 2D game", or any request to start game systems from
  scratch for the web. Drives a strict discovery-interview → system-by-system
  build-and-test loop, using in-browser testing after every system.
license: MIT
---

# 2D Game Dev — Build & Test Loop

## Scope

This skill is for **2D, browser-based games** (HTML5/Canvas/WebGL via JS or TS).
If the user wants 3D, a native (non-web) target, or a specific engine like
Unity/Unreal/Godot, say so explicitly and ask whether they still want you to
proceed with adapted guidance — don't silently force it into the web mold.

## The discipline this skill enforces

Solo game projects die from two things: never nailing down what the game
actually is, and building five systems in parallel none of which actually
work. This skill exists to prevent both. Follow the phases below **in
order**. Do not skip the interview. Do not build more than one system at a
time. Do not mark a system done without watching it work in a real browser.

---

## Phase 0 — Resume / Existing-Project Check (run this before anything else)

Before doing anything else, check the project root:

1. **`GAME_SPEC.md` already exists** → this is a resumed project, not a new
   one. Read `GAME_SPEC.md` and `SYSTEMS.md` in full. Do **not** re-run the
   Phase 1 interview. Jump straight to Phase 4 and continue at the first
   system in `SYSTEMS.md` that isn't `done`. Briefly confirm your read of
   where things stand with the user before writing any code, in case
   something changed since the last session.
2. **No `GAME_SPEC.md`, but a project already exists** (a `package.json`,
   an existing `src/`, etc.) → an established project the skill wasn't
   used to start. Don't scaffold over it. Read what's there (stack,
   structure, existing game logic), then run Phase 1 to establish
   `GAME_SPEC.md`, and do Phase 3 adapted to build `SYSTEMS.md` and a dev
   level *around* the existing code rather than a fresh scaffold.
3. **Neither exists** → genuinely new project. Proceed to Phase 1 normally.

---

## Phase 1 — Discovery Interview (new projects only — see Phase 0)

Never assume genre, platform, or scope on the user's behalf. Ask, using
`AskUserQuestion`.

### Round 1 — always ask these together

1. **Game type/genre.** Offer concrete options plus a free-type escape hatch:
   Platformer · Side-scroller / endless runner · Shooter (top-down / arcade /
   bullet-hell) · Stickman or ragdoll physics · Puzzle · Word game ·
   Simulation / idle · Top-down adventure or action · Other (let them
   describe it in their own words — never force a freeform idea into one of
   the listed buckets if it doesn't fit).
2. **Target platform.** Desktop (keyboard/mouse) · Mobile (touch) · Both.
   This decides input abstraction and layout from the start, not as an
   afterthought.
3. **Art approach.** Placeholder/programmer art (ship fast, swap later) ·
   Pixel art · Vector/flat shapes · "I already have assets."
4. **Scope.** Quick prototype (one core loop, a handful of systems) · Full
   small game (multiple levels/content, a polish pass).

### Round 2 — genre-specific follow-ups

Derive 2–4 follow-up questions from whatever genre came out of Round 1.
Don't ask a static checklist — pick what's actually decision-relevant. Examples:

- **Platformer:** jump feel (floaty vs snappy)? Single screen or multi-level? Enemies/hazards?
- **Side-scroller/runner:** auto-scroll or player-driven? Endless or level-based? Obstacle pattern style?
- **Shooter:** perspective (top-down/side-on)? Free movement or rail? How complex are bullet patterns?
- **Stickman/ragdoll:** physics-driven skeleton or animated? Combat, sandbox, or platformer-with-ragdoll?
- **Word game:** curated word list or full dictionary? Single-player or turn-based multiplayer? Grid-based or freeform?
- **Simulation/idle:** what's being simulated? Real-time or tick-based? How deep is the progression/economy?
- **Puzzle:** core mechanic (match / physics / logic)? Level-based or endless/procedural?
- **Other (freeform description):** ask them to state the core loop in one sentence, then confirm your read of it back to them before proceeding — don't guess silently.

### Write the spec

Once both rounds are answered, write `GAME_SPEC.md` in the project root
using `references/game-spec.template.md` as the structure: genre, platform
target(s), art approach, scope, every genre-specific answer, plus a
one-paragraph "core loop" summary in your own words. This file is the
**source of truth** for the rest of the build — every later phase reads it,
and scope creep beyond it requires asking the user first, not deciding
unilaterally.

---

## Phase 2 — Tech Stack Selection

Read `references/libraries.md` — it's a curated knowledge base of the 2D
web game libraries available (engines, physics, audio, tilemaps, word-list
sources, mobile input, bundler). Pick the smallest stack that actually
satisfies `GAME_SPEC.md`. Default bundler is Vite unless there's a reason
not to. State the chosen stack and a one-line reason to the user; only ask
for confirmation if two real options are genuinely close and the tradeoff
matters to them (e.g. Phaser vs. raw PixiJS when physics needs are unclear).

---

## Phase 3 — Scaffold

1. If Phase 0 found an existing project, skip fresh scaffolding entirely —
   map the existing code onto the system list in step 3 below, and add the
   dev level alongside the existing structure instead of replacing it.
   Otherwise, scaffold the project with the chosen bundler/library.
2. If the project isn't already a git repository, run `git init` now. The
   checkpoint commits in Phase 4 depend on it, and it's cheap to set up
   before any code exists.
3. Build the **dev level** — a persistent sandbox scene/route used to test
   systems in isolation, per `references/dev-level.md`. This is not
   throwaway scaffolding: it stays in the repo for the life of the project
   as the QA harness.
4. Write `SYSTEMS.md` using `references/systems.template.md` as the
   structure — the build checklist. Derive the initial system list from
   `GAME_SPEC.md` (genre + platform), e.g.: input/controls, core movement,
   collision, camera, the genre-defining mechanic, UI/HUD, audio, mobile
   touch input (if mobile was requested), save/progress (if the scope calls
   for it), level/content loading. Each row: system name, status
   (`pending` / `building` / `testing` / `done`), test notes. Show this
   list to the user before starting Phase 4 so the build order is visible
   and correctable.

---

## Phase 4 — Build Loop (strict — this is the core of the skill)

Non-negotiable rules:

1. Build **exactly one system at a time**, in `SYSTEMS.md` order top to
   bottom. Reorder only when a real dependency forces it, and note why in
   the file when you do.
2. Never write code for the next system before the current one is tested.
3. The instant a system is implemented, test it in the dev level (Phase 5)
   before touching anything else.
4. A failed test means fix-and-retest the **same** system. Do not move on
   carrying a known-broken system.
5. Only mark a system `done` in `SYSTEMS.md` after watching it pass in an
   actual browser per Phase 5 — "the code looks right" is not a pass.
6. Immediately after marking a system `done`, commit it (`git add` the
   changed files + `SYSTEMS.md`, commit with a message naming the system).
   This is the rollback point if a later system's changes break something
   already working — don't batch multiple systems into one commit.
7. Once every system in the list is individually verified, proceed to
   Phase 6.

---

## Phase 5 — Testing Protocol (run after every single system)

Read `references/testing-protocol.md` and follow it exactly. In short:
prefer `claude-in-chrome` when it's available and permitted for the local
dev server; otherwise fall back to Playwright. Every test cycle: serve the
project, load the dev level for the system under test, exercise it,
screenshot, read the console for errors, confirm the expected behavior
actually happened, then log the result (pass/fail + note) in `SYSTEMS.md`.

---

## Phase 6 — Assembly & Playtest

Once all systems pass individually, wire them together into real
levels/content per `GAME_SPEC.md`. Do a full playthrough using the same
browser-testing tool from Phase 5, exercising every platform target that
was declared (simulate touch input if mobile was in scope, keyboard/mouse
if desktop was). Log findings in `PLAYTEST.md`.

### When is it actually done

Check against the scope declared in `GAME_SPEC.md`:

- **Quick prototype** — done once the core loop is playable start-to-finish
  with no crashes and every declared system passes its test. Rough edges
  (placeholder art staying placeholder, no audio polish, minimal content)
  are expected and fine — don't gold-plate a prototype.
- **Full small game** — done once, in addition to the above: there's more
  than one level/content unit, the polish pass the user asked for in Phase
  1 has actually happened (not just planned), and the full playtest above
  has been run on every declared platform with no open issues in
  `PLAYTEST.md`.

If it's unclear which bar has been met, ask the user rather than declaring
the project finished unilaterally.

---

## Ongoing discipline

- `GAME_SPEC.md` and `SYSTEMS.md` are living documents — re-read them at the
  start of any later session before continuing work, instead of re-deriving
  context from scratch.
- Never expand scope beyond `GAME_SPEC.md` without asking the user first.
- If the user asks for something new mid-build, add it to `GAME_SPEC.md` and
  `SYSTEMS.md` explicitly rather than quietly folding it into the current system.
