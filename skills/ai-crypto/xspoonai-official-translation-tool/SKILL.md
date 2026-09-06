# Translation Tool

Multi-language translation tool for text, code comments, and technical documentation.

## Description

A powerful translation skill that enables seamless translation between multiple languages. Perfect for translating technical documentation, code comments, API responses, and general text content. Supports multiple translation providers including Google Translate and DeepL.

## Features

- Translate text between 100+ languages
- Translate code comments while preserving code structure
- Batch translation for multiple text blocks
- Support for technical terminology
- Multiple translation provider support
- Auto-detect source language

## Usage Examples

### Basic Text Translation

```
Translate "Hello, world!" to Spanish
```

### Code Comment Translation

```
Translate the comments in this Python code to Chinese:
# This function calculates the total price
def calculate_total(items):
    # Sum all item prices
    return sum(item.price for item in items)
```

### Technical Documentation

```
Translate this API documentation to Japanese:
"This endpoint returns a list of all users in the system..."
```

## Tools Available

- `translate_text`: Translate text from one language to another
- `translate_code_comments`: Translate comments in code files
- `detect_language`: Auto-detect the language of given text
- `batch_translate`: Translate multiple text blocks at once

## Configuration

You can configure the default translation provider in the skill settings:
- `provider`: "google" or "deepl" (default: "google")
- `target_language`: Default target language (default: "en")

## Attribution

Created by ETHPanda for the SpoonOS AI-Enhanced Productivity Challenge.

## License

MIT License
