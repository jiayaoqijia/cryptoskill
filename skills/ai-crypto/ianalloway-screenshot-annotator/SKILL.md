---
name: screenshot-annotator
description: "Capture, annotate, and share screenshots with AI-powered descriptions using Peekaboo."
homepage: https://github.com/ianalloway/openclaw-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "📸",
        "os": ["darwin"],
        "requires": { "bins": ["peekaboo", "curl"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "openclaw/tap/peekaboo",
              "bins": ["peekaboo"],
              "label": "Install Peekaboo (brew)",
            },
          ],
      },
  }
---

# Screenshot Annotator

Capture screenshots with automatic UI element annotation and AI-powered descriptions. Built on top of Peekaboo for macOS UI automation.

## Features

- Capture full screen, specific windows, or regions
- Automatically annotate UI elements with clickable IDs
- Generate AI descriptions of what's on screen
- Save annotated screenshots with metadata
- Compare before/after screenshots
- Create step-by-step visual guides

## Requirements

- macOS with Screen Recording permissions
- Peekaboo CLI installed (`brew install openclaw/tap/peekaboo`)

## Quick Start

### Capture and annotate current screen
```bash
peekaboo see --annotate --path /tmp/annotated-screen.png
```

### Capture specific app window
```bash
peekaboo see --app "Safari" --annotate --path /tmp/safari-annotated.png
```

### Capture with AI analysis
```bash
peekaboo see --annotate --analyze "Describe the main UI elements and their purpose" --path /tmp/analyzed.png
```

## Common Workflows

### Document a bug
```bash
# 1. Capture the problematic state
peekaboo see --app "MyApp" --annotate --path /tmp/bug-screenshot.png

# 2. Get element IDs for the bug report
peekaboo list windows --app "MyApp" --json

# 3. Describe what's wrong
peekaboo see --app "MyApp" --analyze "Identify any UI issues or anomalies"
```

### Create a tutorial
```bash
# Step 1: Capture initial state
peekaboo see --app "Finder" --annotate --path /tmp/step1.png

# Step 2: Click on target element
peekaboo click --on B3 --app "Finder"

# Step 3: Capture result
peekaboo see --app "Finder" --annotate --path /tmp/step2.png
```

### Compare UI states
```bash
# Before
peekaboo see --app "Settings" --path /tmp/before.png

# Make changes...

# After
peekaboo see --app "Settings" --path /tmp/after.png

# Analyze differences
peekaboo see --app "Settings" --analyze "Compare this to the previous state and describe changes"
```

## Advanced Usage

### Capture specific region
```bash
peekaboo image --mode region --region 100,100,800,600 --path /tmp/region.png
```

### Capture with retina resolution
```bash
peekaboo image --mode screen --retina --path /tmp/retina-screen.png
```

### Capture menu bar
```bash
peekaboo menubar list --json
peekaboo see --mode menubar --annotate --path /tmp/menubar.png
```

### Batch capture all windows
```bash
for app in "Safari" "Finder" "Terminal"; do
  peekaboo see --app "$app" --annotate --path "/tmp/${app}-annotated.png"
done
```

## Output Formats

Screenshots are saved as PNG by default. Use `--format jpg` for JPEG output.

The `--json` flag outputs metadata including:
- Window dimensions and position
- Annotated element IDs and locations
- Timestamp and app info

## Tips

1. Always use `peekaboo see --annotate` before clicking to identify element IDs
2. Use `--analyze` with specific prompts for better AI descriptions
3. Combine with `peekaboo click` and `peekaboo type` for automated workflows
4. Check permissions with `peekaboo permissions` if captures fail

## Author

Created by [Ian Alloway](https://github.com/ianalloway) - Data Scientist specializing in AI/ML.

## License

MIT License
