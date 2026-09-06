## Skill Overview

- **Name**: omnicaptions-translate
- **Track**: ai-productivity
- **Description**: Context-aware subtitle translation with bilingual output support for SRT/VTT/ASS files.
- **Attribution**: From ETHPanda (来自 ETHPanda)

## Demo: Effect Demonstration

### Agent Configuration

Option 1: SpoonReactSkill

```python
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(
    name="caption_demo_agent",
    skill_paths=["./ai-productivity"],
    scripts_enabled=True
)
await agent.activate_skill("omnicaptions-translate")
```

Option 2: Claude Code

```bash
cp -r ai-productivity/caption-translation/ .claude/skills/
```

### Input Prompt

```text
Translate ./samples/input.srt to Chinese with bilingual output.
```

### Intermediate Outputs

```text
Step 1: Agent activates skill "omnicaptions-translate"
  -> Mode: Claude native translation (default)

Step 2: Validate input subtitle file
  -> File format detected: srt

Step 3: Execute translation with context-aware batching
  -> Target language: zh
  -> Bilingual: true

Step 4: Write output file
  -> Output: ./samples/input_Claude_zh.srt
```

### Final Output

```text
Translation completed successfully.
- Input: ./samples/input.srt
- Target language: zh
- Bilingual: enabled
- Output: ./samples/input_Claude_zh.srt
```

### Screenshots (Required)

Please attach screenshots that show:
1. Agent with skill loaded
2. Input prompt processing
3. Intermediate execution trace
4. Final output

## Checklist

- [x] SKILL.md follows required format
- [x] README.md includes detailed documentation
- [x] Environment variables documented
- [ ] Screenshots of running example included
- [x] No API keys or secrets committed
