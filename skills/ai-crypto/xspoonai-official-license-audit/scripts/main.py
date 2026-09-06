#!/usr/bin/env python3
import json
import argparse
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime


# Comprehensive license database with classifications
LICENSE_DATABASE = {
    # Permissive licenses (least restrictive)
    "MIT": {
        "category": "permissive",
        "risk": "low",
        "requires_disclosure": False,
        "commercial_friendly": True,
        "description": "Simple permissive license with minimal restrictions"
    },
    "Apache-2.0": {
        "category": "permissive",
        "risk": "low",
        "requires_disclosure": False,
        "commercial_friendly": True,
        "description": "Permissive license with explicit grant of patent rights"
    },
    "BSD-2-Clause": {
        "category": "permissive",
        "risk": "low",
        "requires_disclosure": False,
        "commercial_friendly": True,
        "description": "Simple 2-clause BSD license"
    },
    "BSD-3-Clause": {
        "category": "permissive",
        "risk": "low",
        "requires_disclosure": False,
        "commercial_friendly": True,
        "description": "BSD license with non-endorsement clause"
    },
    "ISC": {
        "category": "permissive",
        "risk": "low",
        "requires_disclosure": False,
        "commercial_friendly": True,
        "description": "Simple permissive license"
    },
    "MPL-2.0": {
        "category": "weak-copyleft",
        "risk": "medium",
        "requires_disclosure": True,
        "commercial_friendly": True,
        "description": "Weak copyleft - file-level reciprocity"
    },
    
    # Weak copyleft licenses
    "LGPL-2.1": {
        "category": "weak-copyleft",
        "risk": "medium",
        "requires_disclosure": True,
        "commercial_friendly": False,
        "description": "Library GPL - requires disclosure for library use"
    },
    "LGPL-3.0": {
        "category": "weak-copyleft",
        "risk": "medium",
        "requires_disclosure": True,
        "commercial_friendly": False,
        "description": "Library GPL v3 - may have restrictions on linking"
    },
    
    # Strong copyleft licenses (most restrictive)
    "GPL-2.0": {
        "category": "copyleft",
        "risk": "high",
        "requires_disclosure": True,
        "commercial_friendly": False,
        "description": "Strong copyleft - derivative works must be GPL-licensed"
    },
    "GPL-3.0": {
        "category": "copyleft",
        "risk": "high",
        "requires_disclosure": True,
        "commercial_friendly": False,
        "description": "GPLv3 with tivoization restrictions"
    },
    "AGPL-3.0": {
        "category": "copyleft",
        "risk": "critical",
        "requires_disclosure": True,
        "commercial_friendly": False,
        "description": "Affero GPL - includes network use clause"
    }
}


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details=None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def normalize_license(license_str: str) -> str:
    """Normalize license string to standard SPDX identifier."""
    if not license_str:
        return "Unknown"
    
    # Remove common variations and normalize to title case
    normalized = license_str.strip()
    normalized = normalized.replace(" License", "").replace(" Licence", "")
    normalized = normalized.replace(" OR ", " OR ").replace(" AND ", " AND ")
    
    # Normalize to uppercase for DB lookup, but preserve original for display
    return normalized if normalized else "Unknown"


def classify_license(license_str: str) -> Optional[Dict[str, Any]]:
    """Classify a license and return its metadata."""
    normalized = normalize_license(license_str)
    
    # Direct match (case-insensitive)
    for db_license, metadata in LICENSE_DATABASE.items():
        if db_license.upper() == normalized.upper() or normalized.upper() == db_license:
            return metadata
    
    # Partial match (e.g., "GPL-2.0 or later" -> "GPL-2.0")
    for db_license, metadata in LICENSE_DATABASE.items():
        if db_license.upper() in normalized.upper() or normalized.upper().startswith(db_license.upper()):
            return metadata
    
    # Unknown license
    return {
        "category": "unknown",
        "risk": "unknown",
        "requires_disclosure": None,
        "commercial_friendly": False,
        "description": "Unknown or unrecognized license"
    }


def audit_licenses(dependencies: List[Dict], policy: Optional[Dict] = None) -> Dict[str, Any]:
    """Perform comprehensive license audit against policy."""
    if policy is None:
        # Default policy: flag restrictive and copyleft licenses
        policy = {
            "forbidden_categories": ["copyleft", "agpl"],
            "forbidden_licenses": ["GPL-2.0", "GPL-3.0", "AGPL-3.0"],
            "warn_categories": ["weak-copyleft"],
            "allow_unknown": False
        }
    
    results = {
        "total_dependencies": len(dependencies),
        "parsed_licenses": {},
        "critical_issues": [],
        "warnings": [],
        "info": [],
        "summary": {
            "compliant": 0,
            "warnings": 0,
            "critical": 0,
            "unknown": 0
        }
    }
    
    for dep in dependencies:
        name = dep.get("name", "unknown")
        version = dep.get("version", "unknown")
        license_str = dep.get("license", "Unknown")
        
        metadata = classify_license(license_str)
        normalized = normalize_license(license_str)
        
        # Track parsed license
        if normalized not in results["parsed_licenses"]:
            results["parsed_licenses"][normalized] = {
                "count": 0,
                "packages": [],
                "metadata": metadata
            }
        
        results["parsed_licenses"][normalized]["count"] += 1
        results["parsed_licenses"][normalized]["packages"].append(f"{name}@{version}")
        
        # Evaluate against policy
        category = metadata.get("category", "unknown")
        risk = metadata.get("risk", "unknown")
        
        # Check for forbidden licenses
        if normalized in policy.get("forbidden_licenses", []):
            results["critical_issues"].append({
                "package": f"{name}@{version}",
                "license": normalized,
                "reason": f"Forbidden license: {metadata.get('description', '')}",
                "severity": "critical",
                "recommendation": "Replace with compatible alternative or obtain exception"
            })
            results["summary"]["critical"] += 1
        
        # Check for forbidden categories
        elif category in policy.get("forbidden_categories", []):
            results["critical_issues"].append({
                "package": f"{name}@{version}",
                "license": normalized,
                "reason": f"Forbidden category ({category}): {metadata.get('description', '')}",
                "severity": "critical",
                "recommendation": "Replace with compatible alternative"
            })
            results["summary"]["critical"] += 1
        
        # Check for warning categories
        elif category in policy.get("warn_categories", []):
            results["warnings"].append({
                "package": f"{name}@{version}",
                "license": normalized,
                "reason": f"Warning category ({category}): {metadata.get('description', '')}",
                "severity": "medium",
                "recommendation": "Review usage and ensure compliance"
            })
            results["summary"]["warnings"] += 1
        
        # Check for unknown licenses
        elif category == "unknown":
            if not policy.get("allow_unknown", True):
                results["warnings"].append({
                    "package": f"{name}@{version}",
                    "license": normalized,
                    "reason": "Unknown license - cannot validate compliance",
                    "severity": "low",
                    "recommendation": "Verify license terms manually"
                })
                results["summary"]["unknown"] += 1
            else:
                results["info"].append({
                    "package": f"{name}@{version}",
                    "license": normalized,
                    "note": "Unknown license - assumed acceptable per policy"
                })
        
        # Compliant
        else:
            results["summary"]["compliant"] += 1
            results["info"].append({
                "package": f"{name}@{version}",
                "license": normalized,
                "category": category,
                "risk": risk
            })
    
    # Calculate compliance score
    total = results["summary"]["compliant"] + results["summary"]["warnings"] + results["summary"]["critical"] + results["summary"]["unknown"]
    if total > 0:
        compliance_score = (results["summary"]["compliant"] / total) * 100
    else:
        compliance_score = 100
    
    results["compliance_score"] = round(compliance_score, 1)
    results["status"] = "compliant" if results["summary"]["critical"] == 0 else "non-compliant"
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Comprehensive license audit for project dependencies'
    )
    parser.add_argument('--demo', action='store_true', help='Run with realistic demo project')
    parser.add_argument('--params', type=str, help='JSON with dependencies and optional policy')
    parser.add_argument('--policy', type=str, help='Custom compliance policy')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Real demo: Common Python packages with mixed licenses
            demo_dependencies = [
                # Permissive licenses (compliant)
                {"name": "requests", "version": "2.28.1", "license": "Apache-2.0"},
                {"name": "flask", "version": "2.3.2", "license": "BSD-3-Clause"},
                {"name": "django", "version": "4.2.1", "license": "BSD-3-Clause"},
                {"name": "numpy", "version": "1.24.3", "license": "BSD-3-Clause"},
                {"name": "pandas", "version": "2.0.2", "license": "BSD-3-Clause"},
                {"name": "pytest", "version": "7.3.1", "license": "MIT"},
                {"name": "sqlalchemy", "version": "2.0.15", "license": "MIT"},
                {"name": "pydantic", "version": "1.10.9", "license": "MIT"},
                
                # Weak copyleft (warnings)
                {"name": "cryptography", "version": "40.0.2", "license": "Apache-2.0 or BSD"},
                
                # Strong copyleft (violations!)
                {"name": "ffmpeg-python", "version": "0.2.3", "license": "GPL-3.0"},
                {"name": "imagemagick", "version": "1.0.1", "license": "AGPL-3.0"},
            ]
            
            policy = {
                "forbidden_categories": ["copyleft"],
                "forbidden_licenses": ["GPL-2.0", "GPL-3.0", "AGPL-3.0"],
                "warn_categories": ["weak-copyleft"],
                "allow_unknown": True
            }
            
            audit = audit_licenses(demo_dependencies, policy)
            result = {
                "demo": True,
                "project_name": "sample-python-project",
                "audit_timestamp": datetime.now().isoformat(),
                "audit": audit
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            dependencies = params.get("dependencies", [])
            custom_policy = params.get("policy")
            
            if not dependencies:
                raise ValueError("'dependencies' array is required")
            
            # Validate dependencies format
            for dep in dependencies:
                if not isinstance(dep, dict) or "name" not in dep or "license" not in dep:
                    raise ValueError("Each dependency must have 'name' and 'license' fields")
            
            audit = audit_licenses(dependencies, custom_policy)
            result = {
                "project_name": params.get("project_name", "unnamed"),
                "audit_timestamp": datetime.now().isoformat(),
                "audit": audit
            }
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
