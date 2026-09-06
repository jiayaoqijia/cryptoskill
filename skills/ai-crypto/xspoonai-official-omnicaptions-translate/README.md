# Caption Translation Skill (omnicaptions-translate)

This skill provides context-aware subtitle translation for SRT, VTT, and ASS files.

Attribution:
- From ETHPanda
- Chinese attribution: came from ETHPanda (来自 ETHPanda)

## Skill Overview

- Skill name: `omnicaptions-translate`
- Track: `ai-productivity`
- Category directory: `ai-productivity/caption-translation/`
- Primary use cases:
  - subtitle localization
  - bilingual subtitle output
  - context-preserving translation for long-form dialogue

## Supported Inputs and Outputs

| Item | Value |
|------|-------|
| Input formats | SRT, VTT, ASS |
| Output formats | SRT by default (can convert later as needed) |
| Languages | Any language supported by the selected model (common: `zh`, `ja`, `ko`, `en`, `es`, `fr`, `de`) |
| Bilingual mode | Supported |

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | No | Needed only when user explicitly chooses Gemini CLI translation |

### Engine Selection

| Engine | When to use |
|--------|-------------|
| Claude native | Default path, no API key required |
| Gemini CLI | Optional fallback when user asks for Gemini specifically |

## Usage Examples

### Example 1: Claude-native translation flow

Prompt example:

```text
Translate this subtitle file to Chinese with context awareness and keep natural spoken style.
```

Expected behavior:
1. Read subtitle file.
2. Translate in context-aware batches.
3. Save output with `_Claude_zh` suffix.

### Example 2: Gemini CLI bilingual output

```bash
omnicaptions translate input.srt -l zh --bilingual
```

Expected output filename:
- `input_Gemini_zh.srt`

### Example 3: Specify model

```bash
omnicaptions translate input.vtt -l ja -m gemini-3-pro-preview
```

## Error Handling

| Error Case | Handling |
|------------|----------|
| Missing input file | Return clear file-not-found message and stop |
| Unsupported language code | Return validation guidance with examples |
| Missing `GEMINI_API_KEY` for Gemini path | Ask user to provide API key or switch to Claude path |
| CLI failure | Return stderr summary and command context without exposing secrets |

## Quality Guidelines

1. Keep speaker voice and sentence continuity across lines.
2. Preserve timestamps and subtitle ordering exactly.
3. Keep terminology consistent for product/domain terms.
4. Prefer bilingual output during review cycles.

## Security Notes

1. Do not commit API keys, tokens, or local paths containing secrets.
2. Use environment variables for sensitive configuration.
3. Avoid printing full stack traces to end users.

## Demo Template for PR

Use this structure in the PR body:

```text
Input Prompt:
"Translate input.srt to zh with bilingual output"

Intermediate:
Step 1: Skill activated (omnicaptions-translate)
Step 2: File parsed and validated
Step 3: Translation executed with selected engine
Step 4: Output subtitle generated

Final Output:
"Translation complete. Output: input_Claude_zh.srt"
```

## Related Skills

- `omnicaptions:transcribe` for generating captions from media
- `omnicaptions:convert` for format conversion after translation
