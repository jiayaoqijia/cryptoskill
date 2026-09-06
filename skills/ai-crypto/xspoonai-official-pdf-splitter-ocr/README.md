# pdf-splitter-ocr (Track: ai-productivity)

Split PDF files by page and apply OCR to extract searchable text from scanned documents

## Overview

This skill enables PDF manipulation with splitting and optical character recognition (OCR). It can split PDF files into individual pages, merge PDF pages, and extract text from scanned documents using OCR technology. Useful for document processing pipelines and making PDFs searchable.

## Features

- **PDF Splitting**: Extract specific pages or split PDF into individual pages
- **PDF Merging**: Combine multiple PDFs into a single file
- **OCR Processing**: Convert scanned images to searchable text
- **Page Extraction**: Extract pages by range or individual selection
- **Text Extraction**: Get text content from PDF pages
- **Batch Processing**: Process multiple PDFs efficiently
- **Quality Settings**: Configure OCR accuracy vs. speed tradeoff
- **Format Preservation**: Maintain original formatting where possible

## Use Cases

- Extract individual pages from multi-page scanned documents
- Make scanned documents searchable with OCR
- Split invoices and receipts for automated processing
- Merge multiple PDF reports into single document
- Extract text from contract PDFs for analysis
- Process archived scanned records in bulk

## Quickstart
```bash
python3 scripts/main.py --help
```

## Example
```bash
python3 scripts/main.py --demo
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| pdf_file | string | Yes | Path to input PDF file |
| operation | string | Yes | Operation to perform (split, merge, extract, ocr) |
| pages | string | No | Page range (e.g., "1-5,10,15-20") |
| output_dir | string | No | Directory for output files |
| output_format | string | No | Output format (pdf, png, jpg, txt) |
| ocr_enabled | boolean | No | Enable OCR processing - default: false |
| ocr_language | string | No | OCR language (eng, fra, spa, deu, etc.) |
| dpi | integer | No | Resolution for image conversion (72-600) |
| cleanup | boolean | No | Delete original after processing - default: false |

## Example Output

```json
{
  "ok": true,
  "data": {
    "operation": "split",
    "input_file": "document.pdf",
    "total_pages": 50,
    "pages_processed": 50,
    "output_files": [
      "document_page_001.pdf",
      "document_page_002.pdf",
      "document_page_003.pdf"
    ],
    "ocr_results": {
      "pages_with_text": 45,
      "pages_scanned": 50,
      "total_text_chars": 125634,
      "confidence": 0.92
    },
    "processing_time_seconds": 23.45
  }
}
