#!/usr/bin/env python3
import json
import argparse
import sys
import os
from typing import Dict, Any, Optional

# Try importing PIL/Pillow for image operations
try:
    from PIL import Image, ImageChops, ImageDraw
    import numpy as np
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def compare_images(image1_path: str, image2_path: str, save_diff: bool = False, 
                   output_path: Optional[str] = None) -> Dict[str, Any]:
    """Compare two images for differences using PIL."""
    if not HAS_PIL:
        return {
            "success": False,
            "error": "PIL not installed",
            "message": "Run: pip install pillow numpy"
        }
    
    if not os.path.exists(image1_path):
        return {"success": False, "error": "file_not_found", "message": f"Image 1 not found: {image1_path}"}
    
    if not os.path.exists(image2_path):
        return {"success": False, "error": "file_not_found", "message": f"Image 2 not found: {image2_path}"}
    
    try:
        img1 = Image.open(image1_path)
        img2 = Image.open(image2_path)
        
        # Get image properties
        img1_size = img1.size
        img2_size = img2.size
        img1_mode = img1.mode
        img2_mode = img2.mode
        
        # Check if images are identical
        if img1_size != img2_size or img1_mode != img2_mode:
            size_match = img1_size == img2_size
            mode_match = img1_mode == img2_mode
            
            return {
                "success": True,
                "image1": os.path.abspath(image1_path),
                "image2": os.path.abspath(image2_path),
                "image1_size": img1_size,
                "image2_size": img2_size,
                "image1_mode": img1_mode,
                "image2_mode": img2_mode,
                "size_match": size_match,
                "mode_match": mode_match,
                "identical": False,
                "similarity_percent": 0,
                "differences_found": True,
                "difference_reason": "Dimensions or color mode mismatch"
            }
        
        # Resize img2 to match img1 if needed for comparison
        if img1_size != img2_size:
            img2_resized = img2.resize(img1_size)
        else:
            img2_resized = img2
        
        # Convert to same mode if different
        if img1_mode != img2_mode:
            if img1_mode == 'RGBA' or img2_resized.mode == 'RGBA':
                img1_cmp = img1.convert('RGBA')
                img2_cmp = img2_resized.convert('RGBA')
            else:
                img1_cmp = img1.convert('RGB')
                img2_cmp = img2_resized.convert('RGB')
        else:
            img1_cmp = img1
            img2_cmp = img2_resized
        
        # Calculate difference
        diff = ImageChops.difference(img1_cmp, img2_cmp)
        diff_stats = diff.getextrema()
        
        # Check if images are identical
        is_identical = diff.getbands()[0] if diff.getbands() else None
        if is_identical:
            is_identical = not any(diff.getextrema()[i][1] > 0 for i in range(len(diff.getbands())))
        
        # Calculate similarity percentage
        if HAS_PIL:
            try:
                diff_array = np.array(diff)
                max_possible_error = 255 * diff_array.size
                actual_error = np.sum(diff_array)
                similarity_percent = max(0, 100 * (1 - actual_error / max_possible_error))
            except:
                similarity_percent = 100 if is_identical else 0
        else:
            similarity_percent = 100 if is_identical else 0
        
        result = {
            "success": True,
            "image1": os.path.abspath(image1_path),
            "image2": os.path.abspath(image2_path),
            "image1_size": img1_size,
            "image2_size": img2_size,
            "identical": is_identical,
            "similarity_percent": round(similarity_percent, 2),
            "differences_found": not is_identical
        }
        
        # Generate diff image if requested
        if save_diff and not is_identical:
            if output_path is None:
                output_path = "diff_result.png"
            
            # Create diff visualization
            diff_vis = diff.convert('RGB')
            diff_vis.save(output_path)
            result["diff_image_saved"] = os.path.abspath(output_path)
        
        return result
    
    except Exception as e:
        return {"success": False, "error": "comparison_error", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description='Compare screenshots for visual regression')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            result = {
                "demo": True,
                "libraries_available": {
                    "PIL_Pillow": HAS_PIL,
                    "numpy": HAS_PIL  # numpy comes with PIL
                },
                "capabilities": {
                    "image_comparison": "enabled" if HAS_PIL else "requires: pip install pillow numpy",
                    "diff_visualization": "enabled" if HAS_PIL else "unavailable"
                },
                "example_comparison": {
                    "image1": "baseline.png",
                    "image2": "current.png",
                    "similarity_percent": 98.5,
                    "differences_found": True,
                    "diff_image": "diff_result.png"
                }
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            image1 = params.get("image1", "")
            image2 = params.get("image2", "")
            
            if not image1 or not image2:
                raise ValueError("Both image1 and image2 are required")
            
            save_diff = params.get("save_diff", False)
            output_path = params.get("output_path")
            
            result = compare_images(image1, image2, save_diff, output_path)
            
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
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()
