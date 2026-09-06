#!/usr/bin/env python3
"""
Documentation Generator - Auto-generate Markdown API docs.
Author: SpoonOS Contributor
Version: 1.0.0
"""

import ast
import os
import sys
import json
from typing import List, Dict, Any, Optional

# Attempt to import BaseTool, handle running standalone for testing
try:
    from spoon_ai.tools.base import BaseTool
except ImportError:
    from pydantic import BaseModel, Field
    class BaseTool(BaseModel):
        name: str
        description: str
        parameters: dict
        async def execute(self, **kwargs): pass

from pydantic import Field

class DocGeneratorTool(BaseTool):
    name: str = "generate_docs"
    description: str = "Generates Markdown API documentation from a Python file."
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the python source file"
            },
            "output_file": {
                "type": "string",
                "description": "Path to save the markdown output"
            }
        },
        "required": ["file_path"]
    })

    async def execute(self, file_path: str, output_file: str = None) -> str:
        """
        Parses the python file and generates markdown docs.
        """
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
        except Exception as e:
            return f"Error parsing file: {e}"

        filename = os.path.basename(file_path)
        module_name = filename.replace(".py", "")
        
        markdown_lines = [f"# API Reference: `{module_name}`", ""]
        
        def get_args(args: ast.arguments) -> str:
            arg_list = []
            # Handle positional args
            defaults_offset = len(args.args) - len(args.defaults)
            for i, arg in enumerate(args.args):
                arg_str = arg.arg
                if arg.annotation:
                    # Basic annotation stringification attempt
                    if isinstance(arg.annotation, ast.Name):
                        arg_str += f": {arg.annotation.id}"
                    elif isinstance(arg.annotation, ast.Str):
                         arg_str += f": {arg.annotation.s}"
                    # Skip complex types for simplicity or expand later
                
                # Check for default
                if i >= defaults_offset:
                    default_node = args.defaults[i - defaults_offset]
                    if isinstance(default_node, ast.Constant):
                        arg_str += f" = {repr(default_node.value)}"
                    elif isinstance(default_node, ast.Name):
                         arg_str += f" = {default_node.id}"
                
                arg_list.append(arg_str)
            
            return ", ".join(arg_list)

        def process_function(node: ast.FunctionDef, indent_level=0):
            indent_str = "#" * (indent_level + 2)
            args_str = get_args(node.args)
            markdown_lines.append(f"{indent_str} `def {node.name}({args_str})`")
            docstring = ast.get_docstring(node)
            if docstring:
                markdown_lines.append("")
                markdown_lines.append(docstring.strip())
            markdown_lines.append("")

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Top level functions
                # Filter out ones defined inside classes (ast.walk visits everything flatly)
                # But wait, ast.walk is depth-first? No, it yields all nodes.
                # To get structure, we should iterate body manually.
                pass 

        # Correct approach: iterate top-level body
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith("_"):
                    process_function(node, indent_level=0)
            
            elif isinstance(node, ast.ClassDef):
                if not node.name.startswith("_"):
                    markdown_lines.append(f"## Class `{node.name}`")
                    docstring = ast.get_docstring(node)
                    if docstring:
                        markdown_lines.append(docstring.strip())
                    markdown_lines.append("")
                    
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            if not item.name.startswith("_") or item.name == "__init__":
                                process_function(item, indent_level=1)

        output_content = "\n".join(markdown_lines)
        
        if not output_file:
            output_file = f"{module_name}_API.md"
            
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output_content)
        except Exception as e:
            return f"Error writing output file: {e}"

        return json.dumps({
            "message": "Documentation generated successfully",
            "generated_file": output_file,
            "preview": output_content[:200] + "..."
        }, indent=2)

if __name__ == "__main__":
    import asyncio
    
    async def main():
        tool = DocGeneratorTool()
        if len(sys.argv) > 1:
            target = sys.argv[1]
            print(f"Generating docs for {target}...")
            res = await tool.execute(file_path=target)
            print(res)
        else:
            print("Usage: python doc_gen.py <file_path>")

    asyncio.run(main())
