# Unit Test Generator Skill

The **Unit Test Generator** skill solves the "blank page problem" for testing. It analyzes your Python files and automatically creates a matching test file with test functions for every class and method found.

## Features

- **AST Parsing**: Safely analyzes code structure without executing it.
- **Smart Scaffolding**: Creates `test_class_method` for methods and `test_function` for functions.
- **Pytest Ready**: Generates code compatible with the standard `pytest` framework.
- **Non-Destructive**: Will not overwrite existing test files by default (unless forced).

## Usage

### Parameters

- `file_path` (string, required): Path to the source Python file.
- `output_dir` (string, optional): Directory to save tests (default: `tests/`).
- `force` (boolean, optional): Overwrite existing files (default: `False`).

### Example Agent Prompts

> "Generate unit tests for 'src/utils.py'."
> "Create a test skeleton for all files in the 'models' folder."

### Output

Returns a JSON object with:
- `generated_file`: Path to the created test file.
- `stats`: Number of tests generated.

## Setup

No external dependencies required! Just Python 3.
