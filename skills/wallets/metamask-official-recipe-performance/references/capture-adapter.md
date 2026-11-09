# Capture adapter contract

The screen adapter owns checkout, instrumentation, restart and real UI actions.
The kit intentionally supplies no private bridge, navigation recipe or source
patcher. Reuse the flow's existing harness/collector, or prepare one before the
series. Python 3 and an executable adapter are required on the measurement host.

The driver calls:

```text
./capture-block.sh STATE REQUESTED_REF ABSOLUTE_BLOCK_DIR ROUNDS
```

The adapter must finish the block before returning. On its owned checkout it:

1. Selects the requested exact commit; restores only its own instrumentation
   and original ref on exit/failure. Never reset unrelated files. Apply the same
   measurement patch in each state, retain its diff/hash and verify the served
   bundle changed as intended. A checkout alone does not reload Metro's bundle.
2. Restarts the same app/dev client, reinstalls probes lost on restart and
   verifies the fixture, actual sampler configuration and unobscured control.
3. Settles for the fixed interval and performs one untimed warm-up per scenario.
4. Resets the per-open probe, invokes the real action, then collects every rAF
   callback through and beyond the end mark. A wait after tapping is collection
   time, not the metric's window. Exit nonzero for setup/capture failures.
5. Writes exactly ROUNDS raw captures per scenario. Keep source/build/device and
   sampler readback, invocation and failure logs alongside them. Do not change
   product values to manufacture a measurement.

These are the original public command forms to compose into the adapter, with
the recipe and its `out`/`rounds` parameters defined for the chosen screen:

```bash
"$HARNESS" call app.lifecycle command=restart --adapter mobile --target "$REPO" --json
"$HARNESS" run "$FLOW_RECIPE" out="$BLOCK_DIR/data" rounds="$ROUNDS" \
  --adapter mobile --target "$REPO" --hud show --artifacts-dir "$BLOCK_DIR/recipe-run" --json
adb -s "$ANDROID_SERIAL" shell input tap "$TAP_X" "$TAP_Y"
adb -s "$ANDROID_SERIAL" shell input keyevent KEYCODE_BACK
```

Bind the physical device, Android emulator serial or iOS simulator UDID and the harness target explicitly. For iOS, use the resolved harness/simulator UI actions instead of adb. Do not assume the active device,
coordinates or a recipe parameter exists. The last two commands illustrate UI
actions inside the prepared flow; they are not an extra tap after the recipe.

Each `data/timed-N.json` is this object, or a JSON string encoding it:

```json
{
  "marks": [{"n": "press", "t": 1000}, {"n": "open-complete", "t": 2000}],
  "frames": [900, 1100, 1500, 2100],
  "traces": [{"n": "Screen Interactive", "ph": "s", "t": 1050}, {"n": "Screen Interactive", "ph": "e", "t": 2000}],
  "calls": [["event", "Screen Viewed", "viewed", 2100]]
}
```

`traces` and `calls` are optional. The first occurrence of each mark/span phase
is used. An end-mark list requires every named mark and takes their maximum,
not a subsequent layout caused by a later re-render. `--event` matches the call's third field and uses its fourth as the JS
timestamp. Do not mix host wall time with these monotonic timestamps.

For existing exports, the reporter also reads `blocks.txt` lines such as
`a1 baseline status=pass`, with `--rounds` supplied explicitly. Preserve the
alternating block order and use `--scenario` to describe its actual raw layout.
