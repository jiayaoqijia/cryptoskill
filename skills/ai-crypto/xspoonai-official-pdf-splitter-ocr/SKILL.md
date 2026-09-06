---
name: pdf-splitter-ocr
track: ai-productivity
version: 0.1.0
summary: Split PDFs and perform OCR for searchability
---

## Description

Split PDF documents and perform optical character recognition (OCR) for text extraction and searchability. Supports batch processing and text indexing.

## Inputs

```json
{
  "pdf_path": "Path to PDF file",
  "action": "split|ocr|extract",
  "pages": "1-5|all"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "text": "Extracted text",
    "pages": 5
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Extract Text
```bash
echo '{"pdf_path":"document.pdf","action":"extract"}' | python3 scripts/main.py
```

## Examples

### Example 1: OCR PDF
```bash
$ echo '{"pdf_path":"document.pdf","action":"ocr","pages":"1-3"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "text": "Extracted text content...",
    "pages": 3
  }
}
```

## Error Handling

When an error occurs, the skill returns:

```json
{
  "ok": false,
  "error": "Error description",
  "details": {
    "pdf_path": "File not found"
  }
}
```
