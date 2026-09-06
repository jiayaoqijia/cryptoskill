#!/usr/bin/env python3
"""Execute and validate skill examples from documentation"""
import json
import argparse
import sys
import re
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List


# Real skill examples metadata
SKILL_EXAMPLES = {
    "api-webhook-signer": {
        "examples": [
            {
                "id": 1,
                "name": "Sign webhook request",
                "command": "python3 scripts/main.py --demo",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            },
            {
                "id": 2,
                "name": "Verify HMAC signature",
                "command": "python3 scripts/main.py --params '{\"action\": \"verify\", \"signature\": \"...\"}'",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            }
        ]
    },
    "security-deps-audit": {
        "examples": [
            {
                "id": 1,
                "name": "Audit dependencies",
                "command": "python3 scripts/main.py --demo",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            },
            {
                "id": 2,
                "name": "Check specific CVE",
                "command": "python3 scripts/main.py --params '{\"dependencies\": [{\"name\": \"log4j\", \"version\": \"2.14.1\"}]}'",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            }
        ]
    },
    "test-suggestions": {
        "examples": [
            {
                "id": 1,
                "name": "Generate test cases",
                "command": "python3 scripts/main.py --demo",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            },
            {
                "id": 2,
                "name": "Analyze function for tests",
                "command": "python3 scripts/main.py --params '{\"code\": \"def hello(): pass\"}'",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            }
        ]
    },
    "skill-ci-checklist": {
        "examples": [
            {
                "id": 1,
                "name": "Validate skill quality",
                "command": "python3 scripts/main.py --demo",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            },
            {
                "id": 2,
                "name": "Check specific skill",
                "command": "python3 scripts/main.py skill-ci-checklist",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            }
        ]
    },
    "skill-coverage-map": {
        "examples": [
            {
                "id": 1,
                "name": "Analyze all tracks",
                "command": "python3 scripts/main.py --demo",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            },
            {
                "id": 2,
                "name": "Analyze specific track",
                "command": "python3 scripts/main.py --track web3-core-operations",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            }
        ]
    },
    "skill-doc-index": {
        "examples": [
            {
                "id": 1,
                "name": "Build documentation index",
                "command": "python3 scripts/main.py --demo",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            },
            {
                "id": 2,
                "name": "Search documentation",
                "command": "python3 scripts/main.py --search security",
                "expected_output_fields": ["ok", "data"],
                "expected_type": "json"
            }
        ]
    }
}


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details=None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def extract_examples_from_markdown(md_content: str) -> List[Dict[str, Any]]:
    """Extract code examples from markdown content."""
    examples = []
    code_block_pattern = r'```(?:bash|shell|python)?\n(.*?)```'
    matches = re.findall(code_block_pattern, md_content, re.DOTALL)
    
    for idx, code in enumerate(matches):
        code = code.strip()
        if code and ("python scripts/main.py" in code or "python3 scripts/main.py" in code):
            examples.append({
                "example_id": idx + 1,
                "code": code,
                "language": "bash",
                "extracted": True
            })
    
    return examples


def validate_json_output(output_str: str) -> Dict[str, Any]:
    """Validate JSON output format."""
    try:
        parsed = json.loads(output_str)
        validation = {
            "valid": True,
            "format": "json",
            "has_ok_field": "ok" in parsed,
            "has_data_field": "data" in parsed if "ok" in parsed and parsed.get("ok") else False,
            "structure": "valid" if "ok" in parsed else "missing_ok_field"
        }
        return validation
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "format": "invalid_json",
            "error": str(e)
        }


def execute_example(skill_name: str, example: Dict) -> Dict[str, Any]:
    """Execute a skill example and capture output."""
    skill_path = f"/Users/sambitsargam/Desktop/spoon-skills-pack"
    
    # Find skill in any track
    tracks = ["ai-productivity", "enterprise-skills", "platform-challenge", "web3-core-operations", "web3-data-intelligence"]
    skill_full_path = None
    
    for track in tracks:
        test_path = Path(skill_path) / track / skill_name
        if test_path.exists():
            skill_full_path = test_path
            break
    
    if not skill_full_path:
        return {
            "skill": skill_name,
            "example_id": example["id"],
            "executed": False,
            "error": f"Skill not found"
        }
    
    # Ensure python3 is used
    command = example["command"]
    if "python scripts/main.py" in command:
        command = command.replace("python scripts/main.py", "python3 scripts/main.py")
    
    result = {
        "skill": skill_name,
        "example_id": example["id"],
        "name": example.get("name", ""),
        "command": command,
        "executed": False
    }
    
    try:
        start_time = time.time()
        proc = subprocess.run(
            command,
            shell=True,
            cwd=str(skill_full_path),
            capture_output=True,
            text=True,
            timeout=10
        )
        elapsed_time = time.time() - start_time
        
        result["executed"] = True
        result["exit_code"] = proc.returncode
        result["execution_time_ms"] = round(elapsed_time * 1000, 2)
        result["success"] = proc.returncode == 0
        
        if proc.stdout:
            result["output"] = proc.stdout.strip()[:500]  # Limit output size
            result["output_validation"] = validate_json_output(proc.stdout)
        
        if proc.stderr and proc.returncode != 0:
            result["error"] = proc.stderr.strip()[:200]
    
    except subprocess.TimeoutExpired:
        result["executed"] = True
        result["error"] = "Execution timeout (10s)"
    except Exception as e:
        result["executed"] = True
        result["error"] = str(e)
    
    return result


def analyze_skill_examples(skill_name: str) -> Dict[str, Any]:
    """Analyze and execute all examples for a skill."""
    if skill_name not in SKILL_EXAMPLES:
        return {
            "skill": skill_name,
            "found": False,
            "error": f"No examples defined for {skill_name}"
        }
    
    skill_data = SKILL_EXAMPLES[skill_name]
    examples = skill_data.get("examples", [])
    
    results = {
        "skill": skill_name,
        "found": True,
        "total_examples": len(examples),
        "examples_executed": 0,
        "examples_successful": 0,
        "execution_summary": []
    }
    
    for example in examples:
        execution_result = execute_example(skill_name, example)
        results["execution_summary"].append(execution_result)
        
        if execution_result.get("executed"):
            results["examples_executed"] += 1
            if execution_result.get("success"):
                results["examples_successful"] += 1
    
    # Calculate success rate
    if results["examples_executed"] > 0:
        results["success_rate"] = round(
            (results["examples_successful"] / results["examples_executed"]) * 100, 1
        )
    
    return results


def generate_report(sample_skills: List[str] = None) -> Dict[str, Any]:
    """Generate comprehensive example execution report."""
    if sample_skills is None:
        sample_skills = list(SKILL_EXAMPLES.keys())[:3]  # First 3 skills
    
    report = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "total_skills_analyzed": len(sample_skills),
        "skills_analyzed": sample_skills,
        "execution_results": []
    }
    
    total_examples = 0
    total_executed = 0
    total_successful = 0
    
    for skill_name in sample_skills:
        skill_result = analyze_skill_examples(skill_name)
        report["execution_results"].append(skill_result)
        
        if skill_result.get("found"):
            total_examples += skill_result.get("total_examples", 0)
            total_executed += skill_result.get("examples_executed", 0)
            total_successful += skill_result.get("examples_successful", 0)
    
    report["summary"] = {
        "total_examples": total_examples,
        "examples_executed": total_executed,
        "examples_successful": total_successful,
        "overall_success_rate": round(
            (total_successful / total_executed * 100) if total_executed > 0 else 0, 1
        )
    }
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Execute and validate skill examples')
    parser.add_argument('--demo', action='store_true', help='Run demo mode with sample skills')
    parser.add_argument('--skill', type=str, help='Analyze specific skill examples')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Demo mode - analyze sample skills
            report = generate_report(["api-webhook-signer", "security-deps-audit", "skill-ci-checklist"])
            print(format_success(report))
        
        elif args.skill:
            # Analyze specific skill
            result = analyze_skill_examples(args.skill)
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            action = params.get("action", "analyze")
            
            if action == "analyze":
                skill = params.get("skill")
                if skill:
                    result = analyze_skill_examples(skill)
                else:
                    result = generate_report(params.get("skills"))
                print(format_success(result))
            
            else:
                raise ValueError(f"Unknown action: {action}")
        
        else:
            print(format_error("Either --demo, --skill, or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()
