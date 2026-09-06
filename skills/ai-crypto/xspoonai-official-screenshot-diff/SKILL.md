---
name: screenshot-diff
track: ai-productivity
version: 0.1.0
summary: Compute pixel diffs between images
---

## Description

Compute simple pixel diffs between two images. Useful for visual regression testing and screenshot comparison in automation workflows.

## Inputs

```json
{
  "image1": "Path or base64 of first image",
  "image2": "Path or base64 of second image",
  "threshold": "Pixel difference threshold"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "diff_percentage": "5.2%",
    "changed_pixels": 1250,
    "identical": false
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Compare Images
```bash
echo '{"image1":"before.png","image2":"after.png"}' | python3 scripts/main.py
```

## Examples

### Example 1: Visual Regression Test
```bash
$ echo '{"image1":"screenshot1.png","image2":"screenshot2.png"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "diff_percentage": "2.3%",
    "changed_pixels": 450,
    "identical": false
  }
}
```

## Error Handling

When an error occurs, the skill returns:

```json
{
  "ok": false,
  "error": "Error description",
  "details": {
    "image1": "File not found"
  }
}
```
