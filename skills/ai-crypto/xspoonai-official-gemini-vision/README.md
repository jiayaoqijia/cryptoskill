# Gemini Vision Analyzer Skill

This skill provides a robust interface to Google's Gemini Vision API (specifically optimized for `gemini-2.5-flash`), enabling AI agents to "see" and analyze images.

## Features

*   **Production Ready**: Includes exponential backoff retry logic for handling `429 Resource Exhausted` errors.
*   **Proxy Support**: Automatically detects and uses `HTTPS_PROXY` or `HTTP_PROXY` environment variables, making it usable in all network environments.
*   **Mock Mode**: Toggle `MOCK_VISION=true` to simulate API responses without making actual network calls—perfect for unit testing and CI/CD.
*   **Structured Output**: Forces the LLM to return valid JSON, parsing it automatically into a Python dictionary.

## Installation

This skill requires the `google-generativeai` package.

```bash
pip install google-generativeai pydantic pillow
```

## Usage

### Basic Usage

```python
from scripts.main import vision_analyze

# Read image
with open("test.jpg", "rb") as f:
    img_data = f.read()

# Call skill
result = await vision_analyze(
    image=img_data,
    prompt="Is there a cat in this photo?"
)

if result["is_valid"]:
    print(f"Analysis: {result['description']}")
```

### Advanced Usage (Validation)

You can restrict the output to specific labels:

```python
result = await vision_analyze(
    image=img_data,
    prompt="Classify the vehicle",
    valid_labels=["car", "truck", "motorcycle"]
)
```

## Configuration

| Environment Variable | Description | Default |
|----------------------|-------------|---------|
| `GEMINI_API_KEY` | **Required**. Get from Google AI Studio. | - |
| `HTTPS_PROXY` | HTTP/HTTPS proxy URL. | - |
| `MOCK_VISION` | Enable mock responses (`true`/`false`). | `false` |
| `GEMINI_MODEL` | Specific Gemini model version. | `gemini-2.5-flash` |

## Error Handling

The skill returns a dictionary even in case of failure, ensuring your agent doesn't crash.

*   **Success**: `{"is_valid": True, ...}`
*   **Failure**: `{"is_valid": False, "description": "Error message...", ...}`

Common errors handled:
*   `429 Quota Exceeded`: Automatically retried up to 3 times.
*   `JSONDecodeError`: Handled if the model fails to output valid JSON.
*   `NetworkError`: Handled via proxy configuration.
