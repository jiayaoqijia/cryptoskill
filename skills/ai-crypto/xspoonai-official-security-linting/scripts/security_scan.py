#!/usr/bin/env python3
"""
Security Scan Tool - Automated security linting using Bandit.

Author: SpoonOS Contributor
Version: 1.0.0
"""

import json
import subprocess
import sys
import shutil
from typing import Dict, Any, Optional

# Attempt to import BaseTool, handle running standalone for testing
try:
    from spoon_ai.tools.base import BaseTool
except ImportError:
    # Mock for standalone testing/verification if spoon_ai not installed
    from pydantic import BaseModel, Field
    class BaseTool(BaseModel):
        name: str
        description: str
        parameters: dict
        async def execute(self, **kwargs): pass

from pydantic import Field

class SecurityScanTool(BaseTool):
    name: str = "security_scan"
    description: str = "Scans Python code for security vulnerabilities using Bandit."
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "path": {
                "type": "string", 
                "description": "File or directory path to scan"
            },
            "recursive": {
                "type": "boolean", 
                "description": "Scan recursively (default: True)",
                "default": True
            },
            "format": {
                "type": "string",
                "description": "Output format (json, txt)",
                "default": "json"
            }
        },
        "required": ["path"]
    })

    async def execute(self, path: str, recursive: bool = True, format: str = "json") -> str:
        """
        Executes the bandit security scan.
        """
        # Ensure bandit is available
        if not shutil.which("bandit"):
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "bandit"])
            except subprocess.CalledProcessError:
                return "Error: Bandit is not installed and could not be installed automatically."

        # Construct command
        cmd = [sys.executable, "-m", "bandit"]
        if recursive:
            cmd.append("-r")
        
        if format == "json":
            cmd.extend(["-f", "json"])
        else:
            cmd.extend(["-f", "txt"])
            
        cmd.append(path)

        try:
            # Bandit returns exit code 1 if issues are found, which is expected
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=False
            )
            
            # If JSON format, try to parse and return formatted JSON string
            if format == "json":
                try:
                    data = json.loads(result.stdout)
                    return json.dumps(data, indent=2)
                except json.JSONDecodeError:
                    return f"Error parsing JSON output. Raw output:\n{result.stdout}\nErrors:\n{result.stderr}"
            
            return result.stdout + "\n" + result.stderr

        except Exception as e:
            return f"Error running security scan: {str(e)}"

# Standalone execution for testing
if __name__ == "__main__":
    import asyncio
    
    async def main():
        tool = SecurityScanTool()
        if len(sys.argv) > 1:
            path = sys.argv[1]
        else:
            print("Usage: python security_scan.py <path>")
            return

        print(f"Scanning {path}...")
        result = await tool.execute(path=path)
        print(result)

    asyncio.run(main())
