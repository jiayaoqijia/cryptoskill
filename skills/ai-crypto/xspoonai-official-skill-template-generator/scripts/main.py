#!/usr/bin/env python3

import json
import argparse
import sys
from datetime import datetime


# Template types with boilerplate configurations
TEMPLATE_TYPES = {
    "basic": {
        "description": "Basic skill with minimal structure",
        "features": ["demo mode", "params mode", "JSON I/O"]
    },
    "analyzer": {
        "description": "Skill for analyzing and validating data",
        "features": ["data validation", "scoring", "detailed feedback"]
    },
    "processor": {
        "description": "Skill for processing and transforming data",
        "features": ["input validation", "processing logic", "output formatting"]
    },
    "monitor": {
        "description": "Skill for monitoring and tracking metrics",
        "features": ["metric collection", "time windows", "aggregation"]
    }
}

TRACKS = [
    "ai-productivity",
    "enterprise-skills",
    "platform-challenge",
    "web3-core-operations",
    "web3-data-intelligence"
]


def format_success(data):
    """Format successful JSON response."""
    return json.dumps({"ok": True, "data": data})


def format_error(error):
    """Format error JSON response."""
    return json.dumps({"ok": False, "error": error})


def generate_skill_md(name, track, description, version="1.0.0"):
    """Generate SKILL.md content."""
    return f"""---
name: {name}
track: {track}
version: {version}
summary: {description}
---

## Overview

{description}

## Inputs

JSON parameters for skill execution with customizable options.

## Outputs

Standard JSON response format with `ok` field and `data` payload.
"""


def generate_main_py(skill_name):
    """Generate scripts/main.py content."""
    return f"""#!/usr/bin/env python3

import json
import argparse
import sys
from datetime import datetime


def format_success(data):
    \"\"\"Format successful JSON response.\"\"\"
    return json.dumps({{"ok": True, "data": data}})


def format_error(error):
    \"\"\"Format error JSON response.\"\"\"
    return json.dumps({{"ok": False, "error": error}})


def process_skill(params):
    \"\"\"Process skill logic with parameters.\"\"\"
    # Add your skill implementation here
    result = {{
        "skill_name": "{skill_name}",
        "timestamp": datetime.now().isoformat(),
        "status": "success",
        "params_received": params
    }}
    return result


def demo_mode():
    \"\"\"Run skill in demo mode.\"\"\"
    result = {{
        "demo": True,
        "skill_name": "{skill_name}",
        "timestamp": datetime.now().isoformat(),
        "sample_output": {{
            "message": "Demo execution successful",
            "status": "ready for customization"
        }}
    }}
    return result


def main():
    parser = argparse.ArgumentParser(description="{skill_name} - Skill implementation")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    parser.add_argument("--params", type=str, help="JSON parameters")
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            print(format_success(demo_mode()))
        elif args.params:
            params = json.loads(args.params)
            result = process_skill(params)
            print(format_success(result))
        else:
            print(format_error("Either --demo or --params must be provided"))
            sys.exit(1)
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {{e}}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Error: {{e}}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
"""


def generate_readme(skill_name, description):
    """Generate README.md content."""
    return f"""# {skill_name}

{description}

## Overview

This skill provides functionality for {description.lower()}.

## Features

- Feature 1: Add your features here
- Feature 2: Each feature should be documented
- Feature 3: Include real use cases

## Usage

Run the skill with demo mode or custom parameters:

```bash
# Demo mode
python3 scripts/main.py --demo

# With parameters
python3 scripts/main.py --params '{{"param1": "value1"}}'
```

## Use Cases

- Use case 1: Describe when to use this skill
- Use case 2: Provide real-world examples
- Use case 3: Show integration patterns

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1 | string | No | Add parameter documentation |
| param2 | string | No | Each parameter should be described |

## Example Output

```json
{{
  "ok": true,
  "data": {{
    "demo": true,
    "skill_name": "{skill_name}",
    "status": "success"
  }}
}}
```
"""


def generate_pull_md():
    """Generate pull.md template."""
    return """# Demo Output

Sample JSON output from --demo execution showing successful skill operation.

## Sample Execution

```bash
$ python3 scripts/main.py --demo
```

## Output

```json
{
  "ok": true,
  "data": {
    "demo": true,
    "status": "success",
    "timestamp": "2026-02-07T10:30:00.000000"
  }
}
```

## Validation

✓ Valid JSON output
✓ Has 'ok' field
✓ Has 'data' field
✓ Proper error handling
"""


def validate_params(name, track, description):
    """Validate template generation parameters."""
    errors = []
    
    if not name or not name.strip():
        errors.append("skill_name is required")
    elif not all(c.isalnum() or c == '-' for c in name):
        errors.append("skill_name should only contain alphanumeric characters and hyphens")
    
    if not track or track not in TRACKS:
        errors.append(f"track must be one of: {', '.join(TRACKS)}")
    
    if not description or not description.strip():
        errors.append("description is required")
    
    return errors


def generate_template(skill_name, track, description, template_type="basic"):
    """Generate complete skill template."""
    errors = validate_params(skill_name, track, description)
    
    if errors:
        return None, errors
    
    template = {
        "metadata": {
            "skill_name": skill_name,
            "track": track,
            "template_type": template_type,
            "generated_at": datetime.now().isoformat(),
            "version": "1.0.0"
        },
        "files": {
            "SKILL.md": generate_skill_md(skill_name, track, description),
            "README.md": generate_readme(skill_name, description),
            "pull.md": generate_pull_md(),
            "scripts/main.py": generate_main_py(skill_name)
        },
        "instructions": [
            "1. Review and customize SKILL.md metadata",
            f"2. Add business logic to scripts/main.py process_skill()",
            "3. Update README.md with real features and use cases",
            "4. Update pull.md with actual demo output after testing",
            "5. Commit and push changes"
        ]
    }
    
    return template, None


def demo_templates():
    """Generate demo output showing available templates."""
    demo_data = {
        "demo": True,
        "timestamp": datetime.now().isoformat(),
        "available_templates": TEMPLATE_TYPES,
        "available_tracks": TRACKS,
        "sample_generation": {
            "skill_name": "my-new-skill",
            "track": "ai-productivity",
            "description": "A new skill for automation",
            "template_type": "basic",
            "files_generated": ["SKILL.md", "README.md", "pull.md", "scripts/main.py"]
        },
        "template_creation_steps": [
            "Provide skill_name (alphanumeric with hyphens)",
            "Choose track from available options",
            "Write meaningful description",
            "Generate template",
            "Customize with business logic",
            "Test with --demo before committing"
        ]
    }
    
    return demo_data


def main():
    parser = argparse.ArgumentParser(description="Generate skill templates")
    parser.add_argument("--demo", action="store_true", help="Show available templates")
    parser.add_argument("--params", type=str, help="JSON parameters: skill_name, track, description")
    parser.add_argument("--list-templates", action="store_true", help="List available template types")
    
    args = parser.parse_args()
    
    try:
        if args.demo or not args.params:
            print(format_success(demo_templates()))
        elif args.list_templates:
            print(format_success({"templates": TEMPLATE_TYPES, "tracks": TRACKS}))
        elif args.params:
            params = json.loads(args.params)
            skill_name = params.get("skill_name", "")
            track = params.get("track", "ai-productivity")
            description = params.get("description", "")
            template_type = params.get("template_type", "basic")
            
            template, errors = generate_template(skill_name, track, description, template_type)
            
            if errors:
                print(format_error(f"Validation failed: {'; '.join(errors)}"))
                sys.exit(1)
            else:
                print(format_success(template))
        else:
            print(format_error("Provide --demo or --params"))
            sys.exit(1)
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
