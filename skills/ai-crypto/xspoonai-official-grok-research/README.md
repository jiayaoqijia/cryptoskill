# Grok Research Skill

A powerful web research and synthesis tool adapted from `Frankieli123/grok-skill`. It allows SpoonOS agents to access real-time information through Grok-compatible APIs and receive structured responses with source citations.

## ✨ Features

- **Real-time Web Research**: Accesses live web data via Grok.
- **Structured Output**: Returns JSON containing `content` (synthesized answer) and `sources`.
- **Zero-Dependency**: Built using standard Python `urllib` for maximum compatibility.
- **SpoonOS Native**: Inherits from `BaseTool` for seamless agent integration.

## 🚀 Installation

1. Copy the `grok-research` folder to your workspace skills directory.
2. Ensure you are using a Python 3.x environment.
3. No additional pip packages are required (uses standard library).

## ⚙️ Configuration

The skill is configured via environment variables.

| Variable | Description | Example |
|----------|-------------|---------|
| `GROK_API_KEY` | Your Grok-compatible API key. | `sk-...` |
| `GROK_BASE_URL` | The endpoint URL (OpenAI-compatible). | `https://api.grok.com/v1` |
| `GROK_MODEL` | (Optional) Override the default model. | `grok-2-latest` |

## 📖 API Documentation

### Tool: `grok_research`

Performs deep web research and returns a synthesized result.

**Parameters:**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `query` | `string` | The search query or research task. | (Required) |
| `model` | `string` | Optional model override for this specific call. | `grok-2-latest` |

**Returns (`JSON string`):**

- `ok`: `boolean` - Whether the research was successful.
- `query`: `string` - The original query.
- `content`: `string` - The synthesized answer.
- `sources`: `array` - List of source objects (`url`, `title`, `snippet`).
- `error`: `string` - Error message (if `ok` is false).

## ⚠️ Error Handling

- **Missing Config**: If `GROK_API_KEY` or `GROK_BASE_URL` are not set, the tool returns a JSON object with `ok: false` and a descriptive error message.
- **API Errors**: HTTP errors (401, 404, 500, etc.) are caught and returned in the `error` and `detail` fields of the output.
- **Parsing Failures**: If the LLM doesn't return valid JSON, the tool uses regex to extract URLs and places the full text in the `raw` or `content` field.

## 🚀 Usage Examples

### 1. General Fact Checking
**Query**: "Who won the Best Actor at the latest Oscars?"
**Result**: Synthesis of news articles with links to official Oscar results and major news outlets.

### 2. Technical Research
**Query**: "What are the breaking changes in the latest version of Pydantic?"
**Result**: A list of changes extracted from GitHub releases and documentation, citing the exact URLs.

### 3. Time-Sensitive Status
**Query**: "Is the Ethereum mainnet currently experiencing high gas fees?"
**Result**: Current gas prices synthesized from block explorers and status pages.


