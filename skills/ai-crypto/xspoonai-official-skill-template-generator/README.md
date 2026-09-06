# skill-template-generator (Track: platform-challenge)

Generate boilerplate templates for new skill implementations

## Overview

This skill generates complete skill templates with proper structure, boilerplate code, and documentation. It streamlines skill creation by providing pre-configured, production-ready templates.

## Features

- **Template Generation**: Create complete skill directory structure
- **Boilerplate Code**: Generate main.py with argparse, JSON I/O, and error handling
- **Documentation Templates**: Pre-filled SKILL.md, README.md, and pull.md
- **Metadata Configuration**: Set skill name, track, version, and summary
- **Code Style Compliance**: Generate code following project standards
- **Multiple Templates**: Different templates for different skill types
- **Customization**: Configure generator with specific parameters

## Usage

Generate new skill templates:

```bash
# Show available templates
python3 scripts/main.py --demo

# Generate new skill template
python3 scripts/main.py --params '{"skill_name": "my-skill", "track": "ai-productivity", "description": "My skill description"}'

# Generate with template type
python3 scripts/main.py --params '{"skill_name": "my-skill", "template_type": "data-processor"}'
```

## Use Cases

- Kickstart new skill development
- Standardize skill structure across repository
- Reduce boilerplate coding overhead
- Ensure compliance with project standards
- Accelerate skill onboarding

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| skill_name | string | Yes | Name of new skill to generate |
| track | string | Yes | Track: ai-productivity, enterprise-skills, platform-challenge, web3-core-operations, web3-data-intelligence |
| description | string | No | Skill description for documentation |
| template_type | string | No | Template type: basic, processor, analyzer, validator |

## Example Output

Generated template for my-skill in ai-productivity track: directory structure created, SKILL.md with metadata, README.md with placeholders, pull.md template, scripts/main.py with argparse and JSON I/O. Ready to customize with business logic.
