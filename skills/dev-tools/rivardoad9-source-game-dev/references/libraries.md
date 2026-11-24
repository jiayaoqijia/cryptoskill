# 2D Web Game Library Knowledge Base

Reference for Phase 2 (Tech Stack Selection). Pick the smallest stack that
satisfies `GAME_SPEC.md`. Don't reach for a heavier library than the genre
needs — a word game does not need a physics engine.

## Full 2D engines (rendering + input + scenes + physics hooks bundled)

- **Phaser 4** — the default choice for most genres, and the current major
  version (a ground-up WebGL2 renderer rewrite that keeps the v3 API, so
  existing Phaser 3 knowledge/code carries over). Batteries-included: scene
  management, sprites/animation, Arcade/Matter physics built in, tilemaps,
  input (keyboard/mouse/touch/gamepad unified), audio, camera, and a
  GPU-batched sprite layer for very high sprite counts. Huge ecosystem and
  docs. Good fit for: platformers, shooters, runners, top-down action, most
  "normal" 2D games. Slight overkill for something as simple as a word
  game. If Phase 0 finds an existing project already on Phaser 3, stay on
  v3 rather than force an upgrade mid-project — the API is close enough
  that the rest of this file's guidance still applies.
- **Kaplay** (formerly Kaboom.js) — very fast to prototype in, terse
  declarative API, built-in simple physics/collision. Good fit for game-jam
  style prototypes and simpler arcade genres. Less ecosystem/tooling depth
  than Phaser for anything that grows past a prototype.
- **excalibur.js** — TypeScript-first, clean actor/scene model, built-in
  physics and collision. Good middle ground if the project is TS and wants
  less "magic" than Phaser's global config style.
- **melonJS** — mature, tilemap-centric (native Tiled support), decent for
  tile-based platformers/RPGs specifically.

## Lower-level rendering (no built-in game loop/physics — use when you want control)

- **PixiJS (v8)** — pure 2D renderer, WebGPU-first with automatic WebGL
  fallback, extremely fast, no scene/physics opinions at all. Its
  `ParticleContainer` handles very large particle/sprite counts (orders of
  magnitude beyond what a naive per-sprite approach manages). Use when the
  game needs custom rendering (particle-heavy, shader effects, non-standard
  camera work) and you're willing to hand-roll the game loop and input
  handling, or pair it with a physics lib below. Note WebGPU is now
  supported across all major browsers (Safari added it in late 2025), but
  this only matters once you're pushing rendering limits — not a default
  concern for a solo 2D project.

## Physics engines (pair with PixiJS, or use standalone with Canvas)

- **Matter.js** — the default pick for anything ragdoll/stickman/physics-sandbox,
  and for casual 2D physics generally. Rigid bodies, constraints, composite
  bodies (built for jointed ragdolls), collision events, easiest docs/API
  of the options here. Phaser also ships a Matter.js integration
  (`physics: { matter: {...} }`) if you want Phaser's scene/input layer plus
  real physics instead of Phaser's lighter arcade physics. Comfortable up
  to roughly a couple hundred active bodies at 60fps — fine for the vast
  majority of 2D games (a handful of ragdolls, normal platformer/puzzle
  physics). Note it's been "alpha" for years but is stable in practice;
  maintained mostly by one person, which is a minor bus-factor risk worth
  knowing about, not a reason to avoid it.
- **Rapier2D** (Rust compiled to WASM, by Dimforge) — escalate to this only
  if Matter.js is actually the bottleneck: bullet-hell shooters with
  thousands of active projectiles, physics-heavy simulations with large
  numbers of bodies, or anything needing to comfortably hold 1000+ active
  bodies at 60fps. Faster and more scalable than Matter.js by a wide
  margin at high body counts, but adds real cost — async WASM
  initialization, a larger bundle, and a less beginner-friendly API. Don't
  reach for this by default; start with Matter.js and only migrate if a
  Phase 5 test actually shows Matter.js struggling under the game's real
  body count.
- **Planck.js** — Box2D port. Heavier/more "correct" than Matter for precise
  simulation; use if the game leans hard into physics accuracy (vehicle
  physics, precise stacking) rather than loose ragdoll fun.
- **p2.js** — effectively unmaintained (no meaningful updates in years).
  Avoid for new projects; if an existing project (Phase 0) already depends
  on it, that's fine to leave as-is rather than force a migration.

## Audio

- **Howler.js** — the standard choice when not using an engine's built-in
  audio (Phaser has its own sound manager already; use Howler if the stack
  is PixiJS-only or otherwise audio-manager-less). Handles playback,
  sprites, and basic spatial/stereo panning.
- **Tone.js** — only for rhythm/music-driven games that need actual sound
  synthesis, sequencing, or precise musical timing (beat-matching,
  generative music) rather than just playing audio files. Overkill for
  anything that just needs sound effects and background music — use
  Howler for that.

## Pathfinding & AI

Only needed for genres where entities navigate space autonomously
(top-down adventure/action with enemies, simulation games with agents).
Skip this section entirely for platformers/shooters/word games/puzzles
that don't need it.

- **PathFinding.js** — grid-based pathfinding (A*, Dijkstra, JPS). The
  right choice when the game world is tile/grid-based.
- **Yuka** — a standalone, engine-agnostic game-AI library: pathfinding
  (incl. navmesh), steering behaviors, state/goal-driven agent logic. Use
  when enemies/NPCs need more than "walk toward the player" — actual
  steering, patrol/pursue/flee behaviors, or a simple state machine per
  agent.

## Tilemaps / level content

- **Tiled** (external editor, free) + Phaser's/melonJS's native tilemap
  loaders — standard workflow for anything level-based with a grid.
- For non-grid or procedurally generated levels, skip Tiled entirely and
  generate level data as plain JSON consumed by the engine.

## Word games specifically

No physics/rendering engine needed — this genre is state machine + DOM/Canvas
UI + a word list. Options for the word source:
- Small curated list: ship a JSON array directly, easiest to control difficulty/theme.
- Full dictionary validation: an npm word-list package (e.g. `an-array-of-english-words`,
  `word-list`) bundled at build time, or a small local wordlist trimmed to
  common words to keep bundle size sane.
- Rendering: plain DOM+CSS is usually enough (grid of letter tiles); reach
  for Canvas/PixiJS only if there's animation-heavy juice involved.

## Placeholder ("programmer") art

When the user picked placeholder art in Phase 1, don't improvise — use one
of these two, decided by how much visual read the genre needs during
testing:

- **Drawn shapes** (default for the dev level and early systems) — solid-color
  rectangles/circles/polygons drawn via the engine's own graphics API
  (Phaser's `Graphics` object, or plain Canvas `fillRect`/`arc`). Zero asset
  pipeline, fastest to get a system testable. Use distinct colors per
  entity type (e.g. player = one color, enemies = another) so screenshots
  during testing are actually readable.
- **Kenney.nl asset packs** — free, CC0, no attribution required, large
  library of ready-made 2D sprite/tile/UI packs across most genres
  (platformer, shooter, RPG, UI). Use when the game needs to *feel* like a
  real game earlier (e.g. showing the user a build, or when shape-art would
  make playtesting the genre-defining mechanic hard to judge — a platformer's
  jump feel is easier to judge with a real character sprite than a box).

Don't spend time hunting for or generating bespoke placeholder art beyond
these two options — that's scope creep on a step that's explicitly meant to
be deferred.

## Mobile / touch input

- Phaser's unified input system already abstracts touch vs mouse — no extra
  library needed if using Phaser.
- For gesture-heavy needs beyond tap/drag (swipe, pinch, multi-touch
  gestures) on a non-Phaser stack, **Hammer.js** is the standard add-on.
- Always design touch targets and camera/viewport for the smallest declared
  target screen size when "mobile" or "both" was chosen in Phase 1 — don't
  bolt on mobile support after the fact.

## Bundler / project tooling

- **Vite** — default choice. Fast dev server with HMR, trivial TS support,
  simple production build. Use `npm create vite@latest` with the vanilla-ts
  or vanilla template as the starting point, then add the chosen game
  library as a dependency.

## Quick genre → default stack table

| Genre | Default stack |
|---|---|
| Platformer | Phaser 4 (arcade physics) |
| Side-scroller / runner | Phaser 4 (arcade physics) |
| Shooter (top-down/arcade) | Phaser 4 (arcade physics); escalate to Rapier2D only if bullet/enemy counts overwhelm Matter.js in testing |
| Stickman / ragdoll | Phaser 4 + Matter.js physics, or PixiJS + Matter.js directly |
| Puzzle | Phaser 4, or plain DOM+CSS if grid-based with no physics |
| Word game | Vite + TS, no engine — DOM/CSS UI + word-list JSON |
| Simulation / idle | Plain TS state machine + DOM/CSS or lightweight Canvas; add Yuka if agents need real navigation/steering |
| Top-down adventure/action | Phaser 4 (arcade physics); add PathFinding.js or Yuka if enemies need to navigate the map |

Treat this table as a default, not a mandate — deviate when `GAME_SPEC.md`
gives a concrete reason to (e.g. a puzzle game with heavy physics interactions
should use Matter.js despite the table's default). If Phase 0 finds an
existing project already on Phaser 3, PixiJS v7, or similar, don't force an
upgrade — these version notes are for new-project defaults only.
