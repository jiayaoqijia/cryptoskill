# Documentation Generator Skill

The **Documentation Generator** skill automates the tedious task of writing API documentation. It scans your Python files, extracts structure and docstrings, and produces a clean Markdown reference.

## Features

- **AST Parsing**: Accurate extraction of classes, methods, and functions.
- **Signature Extraction**: Includes type hints and default values in the documentation.
- **Docstring Support**: Formatting existing docstrings into the output.
- **Markdown Output**: Ready-to-use markdown for wikis or READMEs.

## Usage

### Parameters

- `file_path` (string, required): Path to the source Python file.
- `output_file` (string, optional): Path to save the markdown output (default: `{filename}_API.md`).

### Example Agent Prompts

> "Generate API documentation for 'src/backend/api.py'."
> "Create a markdown reference for the 'User' class in 'models.py'."

### Output

Returns a JSON object with:
- `generated_file`: Path to the created markdown file.
- `preview`: The first few lines of the generated documentation.

## Setup

No external dependencies required! Just Python 3.
