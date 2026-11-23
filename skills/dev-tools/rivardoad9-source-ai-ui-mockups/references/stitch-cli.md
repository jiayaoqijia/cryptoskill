# Stitch CLI — command & payload reference

Package: `@google/stitch` (v0.12.1 at time of writing). No global install needed; run the bundled CLI by path.

```bash
npm i --no-audit --no-fund @google/stitch
export STITCH_API_KEY="$(cat ~/.hermes/secrets/google_stitch.key)"
S="node node_modules/@google/stitch/dist/cli.js"
```

## Commands actually used

| Command | Purpose | Notes |
|---|---|---|
| `$S status` | auth check | prints `authenticated`, `authMethod`, `verified`, masked key |
| `$S find projects --json` | list projects | `data.items[].name` = `projects/<id>` |
| `$S generate screen --new-project "X" --title "Y" --device DESKTOP --prompt "..." --json` | new project + first screen | `--title` allowed only here |
| `$S generate screen --project <id> --device MOBILE --prompt "..." --json` | extra screen, same design system | no `--title` |
| `$S get project <id> --json` | design theme, fonts, DESIGN.md | returns `designTheme.designMd`, `colorMode`, `bodyFontFamily` |

Generation takes roughly 1–3 minutes per screen; give the command a 300 s+ timeout.

## generate JSON — fields worth reading

```jsonc
{
  "success": true,
  "data": {
    "screen": {
      "title": "Zemiz Studio - Dashboard Ringkasan",
      "width": "2560",
      "imageUrl": "https://stitch.googleapis.com/v1/projects/<pid>/files/<fid>:download",
      "agentText": "…the model's own description of what it built…",
      "suggestions": ["…next screens it thinks you want…"]
    }
  }
}
```

`suggestions` is a useful source of screen ideas for the same project; `agentText` explains the layout in the user's language and is handy for your hand-off summary.

## Downloading the rendered PNG

```bash
curl -s -H "X-Goog-Api-Key: $STITCH_API_KEY" "$IMAGE_URL" -o raw.json
```

Response shape:

```json
{ "imageMetadata": { "mimeType": "png" }, "dataString": "iVBORw0KGgoAAAANSUhEUg…" }
```

Decode:

```python
import json, base64
from PIL import Image
d = json.load(open('raw.json'))
open('shot.png', 'wb').write(base64.b64decode(d['dataString']))
print(Image.open('shot.png').size)   # e.g. (2560, 3146) desktop, (780, 2642) mobile
```

If the same curl produced HTML instead, `base64.b64decode` throws `UnicodeEncodeError: 'ascii' codec can't encode character '\u2318'` — that id is the HTML export. Write `d['dataString']` to a `.html` file verbatim; it is a usable starting point for implementation.

## Error messages seen

| Message | Cause | Fix |
|---|---|---|
| `VALIDATION_ERROR … --title on 'stitch generate screen' only names a newly created project` | `--title` passed with `--project` | drop `--title` |
| `find screens` → `items: []` | design-type project doesn't populate the screens list | use the `generate` JSON instead |

## Presenting

Render sizes are 2x: a 1400-wide downscale is legible in Telegram and stays under photo size limits. Tall mobile renders (780×2642) should be sent at ~520 wide to avoid aggressive recompression.
