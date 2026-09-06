#!/usr/bin/env python3

import json
import argparse
import sys
import subprocess
import re
import time
from pathlib import Path
from datetime import datetime


# Test suite configuration
TEST_CONFIG = {
    "timeout": 10,
    "demo_test_skills": [
        "/Users/sambitsargam/Desktop/spoon-skills-pack/ai-productivity/api-webhook-signer/scripts/main.py",
        "/Users/sambitsargam/Desktop/spoon-skills-pack/enterprise-skills/security-deps-audit/scripts/main.py",
        "/Users/sambitsargam/Desktop/spoon-skills-pack/platform-challenge/skill-ci-checklist/scripts/main.py"
    ]
}


def format_success(data):
    """Format successful JSON response."""
    return json.dumps({"ok": True, "data": data})


def format_error(error):
    """Format error JSON response."""
    return json.dumps({"ok": False, "error": error})


def test_shebang(script_path):
    """Verify script has correct shebang."""
    try:
        with open(script_path, 'r') as f:
            first_line = f.readline()
        
        is_valid = first_line.strip() == "#!/usr/bin/env python3"
        return {
            "passed": is_valid,
            "first_line": first_line.strip() if not is_valid else "#!/usr/bin/env python3",
            "issue": None if is_valid else "Shebang line is incorrect"
        }
    except Exception as e:
        return {"passed": False, "error": str(e)}


def test_demo_mode(script_path):
    """Test script with --demo flag."""
    try:
        start_time = time.time()
        result = subprocess.run(
            ["python3", str(script_path), "--demo"],
            capture_output=True,
            text=True,
            timeout=TEST_CONFIG["timeout"]
        )
        elapsed_ms = (time.time() - start_time) * 1000
        
        # Validate JSON output
        try:
            data = json.loads(result.stdout)
            has_ok = "ok" in data
            ok_true = data.get("ok") is True
            
            return {
                "passed": result.returncode == 0 and has_ok and ok_true,
                "exit_code": result.returncode,
                "valid_json": True,
                "has_ok_field": has_ok,
                "ok_value": data.get("ok"),
                "execution_time_ms": elapsed_ms,
                "output_size_bytes": len(result.stdout)
            }
        except json.JSONDecodeError as e:
            return {
                "passed": False,
                "exit_code": result.returncode,
                "valid_json": False,
                "error": f"Output is not valid JSON: {str(e)[:100]}",
                "execution_time_ms": elapsed_ms
            }
    except subprocess.TimeoutExpired:
        return {"passed": False, "error": f"Timeout after {TEST_CONFIG['timeout']}s"}
    except Exception as e:
        return {"passed": False, "error": str(e)}


def test_params_mode(script_path):
    """Test script with --params flag."""
    test_params = json.dumps({"test": "parameter"})
    
    try:
        start_time = time.time()
        result = subprocess.run(
            ["python3", str(script_path), "--params", test_params],
            capture_output=True,
            text=True,
            timeout=TEST_CONFIG["timeout"]
        )
        elapsed_ms = (time.time() - start_time) * 1000
        
        try:
            data = json.loads(result.stdout)
            has_ok = "ok" in data
            
            return {
                "passed": has_ok,
                "exit_code": result.returncode,
                "valid_json": True,
                "has_ok_field": has_ok,
                "execution_time_ms": elapsed_ms
            }
        except json.JSONDecodeError as e:
            return {
                "passed": False,
                "exit_code": result.returncode,
                "valid_json": False,
                "error": "Output is not valid JSON",
                "execution_time_ms": elapsed_ms
            }
    except subprocess.TimeoutExpired:
        return {"passed": False, "error": f"Timeout after {TEST_CONFIG['timeout']}s"}
    except Exception as e:
        return {"passed": False, "error": str(e)}


def test_error_handling(script_path):
    """Test script handles invalid input gracefully."""
    invalid_json = "not{valid}json"
    
    try:
        result = subprocess.run(
            ["python3", str(script_path), "--params", invalid_json],
            capture_output=True,
            text=True,
            timeout=TEST_CONFIG["timeout"]
        )
        
        try:
            data = json.loads(result.stdout)
            # Should have ok:false with error field
            returns_error_gracefully = data.get("ok") is False and "error" in data
            
            return {
                "passed": returns_error_gracefully,
                "valid_json": True,
                "error_handling_correct": returns_error_gracefully,
                "error_message": data.get("error", "No error message")[:100]
            }
        except json.JSONDecodeError:
            return {
                "passed": False,
                "valid_json": False,
                "error": "Should return valid JSON error response"
            }
    except subprocess.TimeoutExpired:
        return {"passed": False, "error": f"Timeout after {TEST_CONFIG['timeout']}s"}
    except Exception as e:
        return {"passed": False, "error": str(e)}


def test_imports(script_path):
    """Verify required imports are present."""
    try:
        with open(script_path, 'r') as f:
            content = f.read()
        
        required = ["import json", "import argparse", "def main()"]
        missing = [req for req in required if req not in content]
        
        return {
            "passed": len(missing) == 0,
            "imports_present": [req for req in required if req in content],
            "imports_missing": missing
        }
    except Exception as e:
        return {"passed": False, "error": str(e)}


def test_script(script_path):
    """Run complete test suite on script."""
    script_path = Path(script_path)
    
    if not script_path.exists():
        return format_error(f"Script not found: {script_path}")
    
    try:
        # Run all tests
        tests = {
            "shebang": test_shebang(script_path),
            "imports": test_imports(script_path),
            "demo_mode": test_demo_mode(script_path),
            "params_mode": test_params_mode(script_path),
            "error_handling": test_error_handling(script_path)
        }
        
        # Calculate results
        total_tests = len(tests)
        passed_tests = sum(1 for test in tests.values() if test.get("passed", False))
        success_rate = (passed_tests / total_tests) * 100
        
        result = {
            "script_path": str(script_path),
            "tests_passed": passed_tests,
            "tests_total": total_tests,
            "success_rate_percent": success_rate,
            "all_passed": passed_tests == total_tests,
            "test_results": tests,
            "timestamp": datetime.now().isoformat()
        }
        
        return format_success(result)
    except Exception as e:
        return format_error(f"Test execution error: {e}")


def demo_test_suite():
    """Run demo test suite on sample scripts."""
    demo_data = {
        "demo": True,
        "timestamp": datetime.now().isoformat(),
        "scripts_tested": [],
        "summary": {}
    }
    
    # Test each demo script
    for script_path in TEST_CONFIG["demo_test_skills"]:
        script = Path(script_path)
        if script.exists():
            result_json = test_script(script_path)
            result = json.loads(result_json)
            if result.get("ok"):
                demo_data["scripts_tested"].append(result["data"])
    
    # Calculate aggregate
    if demo_data["scripts_tested"]:
        total_tests = sum(s["tests_total"] for s in demo_data["scripts_tested"])
        total_passed = sum(s["tests_passed"] for s in demo_data["scripts_tested"])
        
        demo_data["summary"] = {
            "total_scripts": len(demo_data["scripts_tested"]),
            "total_tests": total_tests,
            "total_passed": total_passed,
            "overall_success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 100,
            "all_pass": all(s["all_passed"] for s in demo_data["scripts_tested"])
        }
    
    return format_success(demo_data)


def main():
    parser = argparse.ArgumentParser(description="Test skill scripts for correctness")
    parser.add_argument("--demo", action="store_true", help="Run demo test suite")
    parser.add_argument("--params", type=str, help="JSON parameters with script_path")
    parser.add_argument("--script", type=str, help="Path to script to test")
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            print(demo_test_suite())
        elif args.params:
            params = json.loads(args.params)
            script_path = params.get("script_path", "scripts/main.py")
            print(test_script(script_path))
        elif args.script:
            print(test_script(args.script))
        else:
            print(demo_test_suite())
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
