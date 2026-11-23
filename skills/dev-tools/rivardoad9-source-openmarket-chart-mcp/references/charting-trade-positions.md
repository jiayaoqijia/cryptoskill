# Putting a plan on the chart and drawing the position

For "chart it and draw the trade position yourself" after a screening run. The API record is the deliverable; the PNG is
evidence for the chat. Verify every write from `chart_show`, never from a text read of the rendered image.

## 1. One workspace per ticker on the free plan
`chart_grid` refuses more than a 1-cell grid and `chart_layout` more than 2 panes (`plan_limit`, message names the
numbers), so do not burn calls on `3H` for a three-name plan. Instead:
```bash
om_call.py chart_create '{"name":"Hermes NEAR","symbol":"NEARUSDT","exchange":"BINANCE_FUTURES","interval":"15m"}'
```
Returns `workspaceId` + `url` (`https://openmarket.xyz/chart/<id>`). `chart_keep {"name":..., "workspace":"<id>"}`
renames and promotes it (same id, same link, expiry cleared); it can answer `selection_busy` transiently, so retry after
a few seconds rather than renaming by recreating.
`chart_grid` takes `symbols` as OBJECTS — `[{"symbol":"NEARUSDT","exchange":"BINANCE_FUTURES"}]` — and rejects
`"BINANCE_FUTURES:NEARUSDT"` strings (`expected object, received string`); the `EXCHANGE:SYMBOL` ref form belongs to
`watchlist_*` only.

## 2. Decorate the pane
`chart_indicator_add` with `indicatorType: EMA` and `settings: {"period":20,"colors":["#2962FF"],"width":1}` — EMA20
blue and EMA50 orange (`#FF9800`) carry the entry and the invalidation level, so two lines per pane is enough (free plan
allows 3 indicators per pane). Omit `workspaceId` only when acting on the user's active workspace; pass it when the plan
lives in its own workspace.

## 3. Draw the trade
Enumerate the drawing tools once with `chart_drawing_schema {}`: it returns `anchorFormat {role, time (epoch ms), price}`
plus every tool with its `anchorCount` and roles. `LongPosition` takes roles `entry`, `stop`, `target`.
```python
anchors = [{"role":"entry","time":t_entry,"price":5.44},
           {"role":"stop", "time":t_later,"price":5.345},
           {"role":"target","time":t_later,"price":5.63}]
```
Anchor the entry at the entry-bar time and stop/target a later time (e.g. +12h) so the tool renders as a box with width
instead of a flat line at one timestamp. Use the bar timestamps the candle call returned; epoch ms is scenario time.
The response carries `drawingId`.

## 4. Make the box visible, then screenshot
A position tool extends to the RIGHT of the last candle, so a default-window render cuts it off and the PNG looks like
nothing was drawn. Set the window to cover the whole box first, then shoot:
```bash
om_call.py chart_view '{"workspaceId":"<id>","chartIndex":0,"startTime":<ms>,"endTime":<ms>}'
om_call.py chart_screenshot '{"workspaceId":"<id>"}'   # image content block, base64
```
`startTime`/`endTime` are epoch MILLISECONDS (seconds are refused); a window from a few hours before the last bar to a
few hours past the box end works. `chart_view` and `chart_screenshot` work on a workspace with no live session.
`chart_screenshot` returns an image block, not text — decode it and send the PNG (one per ticker), but do not try to
read the entry/stop numbers off the image: axis labels that small come back wrong. Confirm the numbers from the anchors.

## 4b. Replacing a stale position — and the pane has to match BEFORE you draw
Redrawing the same ticker each session piles boxes on top of each other. Read what is already there with
`chart_drawing_list {"workspaceId":..,"chartIndex":0}` (list key: `marks`; `chart_show` returns the same list under
`drawings`), take `drawingId` where `tool` is `LongPosition`/`ShortPosition`, and clear them with
`chart_drawing_remove {"workspaceId":..,"chartIndex":0,"ids":[...]}`. The parameter is **`ids`**; `drawingIds` is rejected
and ignored, which is exactly how one pane ends up with two overlapping boxes.
Force the pane to the symbol and interval the box assumes before anchoring anything: `chart_symbol` then
`chart_interval {"interval":"15m"}`. A time box on a coarser pane is refused — "LongPosition spans 12h of chart time but
the pane's bars are 1d: it renders as a zero-width sliver" — and the ticker is left with a fresh workspace and no drawing
at all. A reused workspace can also be sitting on the WRONG symbol (created for ADA, pane on SOLUSDT): read `panes` back
after the write, not before only.

## 5. Verification before reporting
`chart_show {"workspaceId":"<id>"}` returns `panes` (symbol, exchange, interval), every `indicator` with settings, and
`drawings` with each `tool` and its anchor prices — that single read is the proof to quote when telling the user the
position is saved. `chart_drawing_list` gives the same for one pane. Report the exact entry/stop/target you anchored,
name each workspace, and say plainly that his pre-existing workspace was not touched.

## 6. Honest framing
Name the plan limit that shaped the layout (per-ticker workspaces instead of one grid) so the user is not left wondering
why; offer the upgrade only as a fact, not as a pitch. If he asks for edits later, the tool is his to drag, restyle or
delete in the UI.