# screenshot-diff (Track: ai-productivity)

Compute pixel-level differences between screenshot images with visual annotations and metrics

## Overview

This skill analyzes differences between two images with detailed metrics and visual output. It highlights changed areas, calculates similarity scores, and produces annotated diff images. Perfect for visual regression testing, UI change detection, and image comparison workflows.

## Features

- **Pixel Comparison**: Precise pixel-by-pixel difference detection
- **Diff Visualization**: Generate annotated images showing changed areas
- **Similarity Metrics**: Calculate percentage similarity and change statistics
- **Region Detection**: Identify and report regions with significant changes
- **Color Difference**: Analyze color and intensity shifts
- **Threshold Configuration**: Adjust sensitivity for minimal vs. strict comparison
- **Multiple Formats**: Support PNG, JPG, WebP and other image formats
- **Performance Metrics**: Report comparison speed and memory usage

## Use Cases

- Visual regression testing in UI automation
- Detect unauthorized changes to website screenshots
- Compare before/after screenshots for design reviews
- Monitor for unexpected UI changes in production
- Validate responsive design across breakpoints
- Screenshot-based test failure analysis

## Quickstart
```bash
python3 scripts/main.py --help
```

## Example
```bash
python3 scripts/main.py --demo
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image1_path | string | Yes | Path to first image file |
| image2_path | string | Yes | Path to second image file (reference) |
| output_path | string | No | Path for diff output image |
| threshold | float | No | Pixel difference threshold (0-255, default: 5) |
| ignore_antialiasing | boolean | No | Ignore anti-aliased pixels - default: false |
| diff_mode | string | No | Diff visualization mode (highlight, overlay, blend) |
| regions | boolean | No | Report changed regions separately - default: false |
| metadata | boolean | No | Include image metadata in output - default: true |

## Example Output

```json
{
  "ok": true,
  "data": {
    "comparison": {
      "image1": "screenshot_before.png",
      "image2": "screenshot_after.png",
      "width": 1920,
      "height": 1080,
      "total_pixels": 2073600
    },
    "metrics": {
      "similarity_percentage": 94.5,
      "changed_pixels": 113652,
      "change_percentage": 5.5,
      "identical_pixels": 1959948
    },
    "diff_image": "screenshot_diff.png",
    "changed_regions": [
      {
        "region": "header",
        "bounds": {"x": 0, "y": 0, "width": 1920, "height": 80},
        "change_percentage": 12.3
      },
      {
        "region": "sidebar",
        "bounds": {"x": 0, "y": 80, "width": 200, "height": 1000},
        "change_percentage": 8.7
      }
    ]
  }
}
