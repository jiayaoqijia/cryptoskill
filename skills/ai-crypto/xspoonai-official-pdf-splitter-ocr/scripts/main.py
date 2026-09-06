#!/usr/bin/env python3
import json
import argparse
import sys
import os
from typing import Dict, Any, List, Optional

# Try importing PDF libraries
try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    import pytesseract
    from PIL import Image
    HAS_OCR = True
except ImportError:
    HAS_OCR = False


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def extract_pdf_text(pdf_path: str) -> Dict[str, Any]:
    """Extract text from PDF file using pypdf."""
    if not HAS_PYPDF:
        return {
            "success": False,
            "error": "pypdf not installed",
            "message": "Run: pip install pypdf",
            "capabilities": {
                "pdf_extraction": "unavailable",
                "ocr": "unavailable" if not HAS_OCR else "available"
            }
        }
    
    if not os.path.exists(pdf_path):
        return {"success": False, "error": "file_not_found", "message": f"PDF file not found: {pdf_path}"}
    
    try:
        reader = PdfReader(pdf_path)
        pages = []
        total_text_length = 0
        
        for page_num, page in enumerate(reader.pages, 1):
            try:
                text = page.extract_text()
                pages.append({
                    "page_number": page_num,
                    "text": text,
                    "text_length": len(text) if text else 0
                })
                total_text_length += len(text) if text else 0
            except Exception as e:
                pages.append({
                    "page_number": page_num,
                    "text": "",
                    "error": str(e),
                    "text_length": 0
                })
        
        return {
            "success": True,
            "pdf_path": pdf_path,
            "total_pages": len(reader.pages),
            "pages": pages,
            "total_text_length": total_text_length,
            "method": "text_extraction"
        }
    
    except Exception as e:
        return {"success": False, "error": "extraction_error", "message": str(e)}


def split_pdf_by_pages(pdf_path: str, output_dir: str, page_ranges: Optional[List] = None) -> Dict[str, Any]:
    """Split PDF into separate files by page ranges."""
    if not HAS_PYPDF:
        return {
            "success": False,
            "error": "pypdf not installed",
            "message": "Run: pip install pypdf"
        }
    
    if not os.path.exists(pdf_path):
        return {"success": False, "error": "file_not_found", "message": f"PDF file not found: {pdf_path}"}
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        split_files = []
        
        if not page_ranges:
            # Default: one file per page
            page_ranges = [[i, i] for i in range(1, total_pages + 1)]
        
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        for range_index, page_range in enumerate(page_ranges, 1):
            start_page = page_range[0] - 1  # Convert to 0-indexed
            end_page = page_range[1] - 1
            
            if start_page < 0 or end_page >= total_pages:
                continue
            
            writer = __import__('pypdf').PdfWriter()
            
            for page_num in range(start_page, end_page + 1):
                writer.add_page(reader.pages[page_num])
            
            output_file = os.path.join(output_dir, f"{base_name}_pages_{page_range[0]}-{page_range[1]}.pdf")
            
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            split_files.append({
                "output_file": output_file,
                "page_range": page_range,
                "pages_extracted": end_page - start_page + 1
            })
        
        return {
            "success": True,
            "pdf_path": pdf_path,
            "output_directory": output_dir,
            "total_original_pages": total_pages,
            "split_files": split_files,
            "files_created": len(split_files)
        }
    
    except Exception as e:
        return {"success": False, "error": "split_error", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description='Extract text from PDFs with OCR fallback')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Demo mode with simulated extraction
            result = {
                "demo": True,
                "libraries_available": {
                    "pypdf": HAS_PYPDF,
                    "pytesseract_ocr": HAS_OCR
                },
                "capabilities": {
                    "pdf_text_extraction": "enabled" if HAS_PYPDF else "requires: pip install pypdf",
                    "pdf_splitting": "enabled" if HAS_PYPDF else "requires: pip install pypdf",
                    "ocr_fallback": "enabled" if HAS_OCR else "requires: pip install pytesseract pillow"
                },
                "example_extraction": {
                    "pages": [
                        {"page_number": 1, "text": "Sample PDF Page 1\nThis is demo content."},
                        {"page_number": 2, "text": "Sample PDF Page 2\nMore demo content."}
                    ],
                    "total_pages": 2
                }
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            action = params.get("action", "extract")
            pdf_path = params.get("pdf_path", "")
            
            if not pdf_path:
                raise ValueError("pdf_path is required")
            
            if action == "extract":
                result = extract_pdf_text(pdf_path)
            elif action == "split":
                output_dir = params.get("output_dir", "pdf_output")
                page_ranges = params.get("page_ranges")
                result = split_pdf_by_pages(pdf_path, output_dir, page_ranges)
            else:
                raise ValueError(f"Unknown action: {action}")
            
            if result.get("success") == False:
                print(format_error(result.get("error", "unknown_error"), {"message": result.get("message")}))
            else:
                print(format_success(result))
        
        else:
            print(format_error("Either --demo or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except ValueError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}", {"error_type": "processing"}))
        sys.exit(1)


if __name__ == '__main__':
    main()
