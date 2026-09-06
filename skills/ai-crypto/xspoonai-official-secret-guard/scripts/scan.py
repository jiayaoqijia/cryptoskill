import sys
import subprocess
import re

# ================= CONFIGURATION =================
# Define common regex patterns for sensitive information here.
# You can extend this dictionary as needed.
SECRET_PATTERNS = {
    "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
    "AWS Secret Key": r"(?i)aws_secret_access_key\s*=\s*['\"][A-Za-z0-9/+=]{40}['\"]",
    "OpenAI API Key": r"sk-[a-zA-Z0-9\-]{20,}",
    "GitHub Token": r"ghp_[a-zA-Z0-9]{36}",
    "Private Key Header": r"-----BEGIN [A-Z ]+ PRIVATE KEY-----",
    "Generic API Key": r"(?i)(api_key|secret_token|access_token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]"
}
# =================================================

def get_staged_diff():
    """Get the diff content from the git staged area."""
    try:
        # Check if there are staged files
        check = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
        if check.returncode == 0:
            print("✅ Staged area is empty. Nothing to scan.")
            sys.exit(0)
            
        # Get the actual diff
        result = subprocess.run(
            ["git", "diff", "--cached"], 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            errors='ignore'
        )
        return result.stdout
    except FileNotFoundError:
        print("❌ Error: 'git' command not found. Please ensure Git is installed.")
        sys.exit(1)

def mask_secret(content, pattern_name):
    """Simple masking to hide sensitive data in logs, showing only prefix."""
    # Logic: Show first 4 chars for keys, otherwise mask completely
    if "KEY" in pattern_name.upper():
        return content[:4] + "*" * 10
    return "***MASKED***"

def main():
    print("🔍 Starting Secret Guard scan on staged area...")
    diff_content = get_staged_diff()
    
    current_file = "Unknown File"
    found_issues = []

    lines = diff_content.splitlines()
    
    for line in lines:
        # 1. Identify the file currently being processed
        if line.startswith("+++ b/"):
            current_file = line[6:] # Remove '+++ b/' prefix
            continue
            
        # 2. Check only added lines (starts with +, ignore header +++)
        if line.startswith("+") and not line.startswith("+++"):
            clean_line = line[1:].strip() # Remove '+' and whitespace
            
            # 3. Check against all regex patterns
            for secret_type, pattern in SECRET_PATTERNS.items():
                match = re.search(pattern, clean_line)
                if match:
                    matched_content = match.group(0)
                    masked = mask_secret(matched_content, secret_type)
                    found_issues.append({
                        "file": current_file,
                        "type": secret_type,
                        "content": masked
                    })

    # 4. Output results
    if found_issues:
        print("\n⚠️  WARNING: Potential sensitive information found in staged area!")
        print("="* 50)
        for issue in found_issues:
            print(f"📁 File: {issue['file']}")
            print(f"🔴 Type: {issue['type']}")
            print(f"🔒 Content: {issue['content']}")
            print("-" * 30)
        print("="* 50)
        print("Please confirm if this information should be public before committing.\n")
        # Return non-zero exit code to signal failure (blocks commit if used as hook)
        sys.exit(1) 
    else:
        print("\n✅ Scan Passed: No obvious secrets found.")
        sys.exit(0)

if __name__ == "__main__":
    main()