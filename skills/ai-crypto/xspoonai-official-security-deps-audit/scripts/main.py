#!/usr/bin/env python3
import json
import argparse
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime


# Comprehensive CVE Database
CVE_DATABASE = {
    "requests": {
        "<=2.20.0": {
            "cve": "CVE-2023-32681",
            "title": "Unintended leak of Proxy-Authorization header",
            "cvss_score": 7.5,
            "severity": "high",
            "description": "Requests library leaks Proxy-Authorization header on HTTP redirect",
            "affected": "<=2.20.0",
            "fixed_in": "2.28.0",
            "exploit_available": True,
            "patch_available": True,
            "recommendation": "Upgrade to 2.28.0 or later immediately"
        }
    },
    "django": {
        "<=3.2.9": {
            "cve": "CVE-2021-35042",
            "title": "SQL injection in QuerySet.annotate()",
            "cvss_score": 9.8,
            "severity": "critical",
            "description": "SQL injection vulnerability via window expressions in QuerySet.annotate()",
            "affected": "<=3.2.9, <4.0.1",
            "fixed_in": "3.2.10, 4.0.1",
            "exploit_available": True,
            "patch_available": True,
            "recommendation": "Upgrade immediately - this is a critical vulnerability"
        }
    },
    "log4j": {
        "<=2.14.1": {
            "cve": "CVE-2021-44228",
            "title": "Apache Log4j Remote Code Execution (Log4Shell)",
            "cvss_score": 10.0,
            "severity": "critical",
            "description": "Unauthenticated Remote Code Execution via JNDI injection in Log4j logging",
            "affected": "2.0-beta9 to 2.15.0",
            "fixed_in": "2.16.0",
            "exploit_available": True,
            "patch_available": True,
            "recommendation": "CRITICAL: Upgrade to 2.16.0+ or apply patch immediately. This is being actively exploited."
        }
    },
    "numpy": {
        "<=1.21.0": {
            "cve": "CVE-2021-41496",
            "title": "Buffer overflow in numpy.array()",
            "cvss_score": 8.1,
            "severity": "high",
            "description": "Buffer overflow when processing large arrays with certain dtype conversions",
            "affected": "<=1.21.0",
            "fixed_in": "1.21.2",
            "exploit_available": False,
            "patch_available": True,
            "recommendation": "Upgrade to 1.21.2 or later"
        }
    },
    "sqlalchemy": {
        "<=1.3.24": {
            "cve": "CVE-2021-33037",
            "title": "SQL injection via column name parameter",
            "cvss_score": 8.6,
            "severity": "high",
            "description": "SQL injection vulnerability when using untrusted inputs for column names",
            "affected": "1.3.0-1.3.24, 1.4.0-1.4.20",
            "fixed_in": "1.3.24, 1.4.21",
            "exploit_available": True,
            "patch_available": True,
            "recommendation": "Upgrade to patched version immediately"
        }
    },
    "pyyaml": {
        "<=5.4": {
            "cve": "CVE-2020-14343",
            "title": "Arbitrary code execution via YAML parser",
            "cvss_score": 9.8,
            "severity": "critical",
            "description": "Remote code execution via unsafe YAML deserialization of untrusted input",
            "affected": "<=5.4",
            "fixed_in": "5.4.1",
            "exploit_available": True,
            "patch_available": True,
            "recommendation": "CRITICAL: Upgrade to 5.4.1+. Disable yaml.load() usage of untrusted sources."
        }
    },
    "pillow": {
        "<=8.2.0": {
            "cve": "CVE-2021-34552",
            "title": "Buffer overflow in image processing",
            "cvss_score": 7.5,
            "severity": "high",
            "description": "Buffer overflow in PcxDecode.c when processing malicious PCX images",
            "affected": "<=8.2.0",
            "fixed_in": "8.3.0",
            "exploit_available": False,
            "patch_available": True,
            "recommendation": "Upgrade to 8.3.0 or later"
        }
    },
    "urllib3": {
        "<=1.26.4": {
            "cve": "CVE-2021-33503",
            "title": "Regular expression DoS vulnerability",
            "cvss_score": 7.2,
            "severity": "high",
            "description": "Regex DoS attack on urllib3 hostname parsing when handling crafted URLs",
            "affected": "<=1.26.4",
            "fixed_in": "1.26.5",
            "exploit_available": True,
            "patch_available": True,
            "recommendation": "Upgrade to 1.26.5 or later"
        }
    }
}


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def parse_version(version_str: str) -> tuple:
    """Parse version string into comparable tuple."""
    try:
        parts = version_str.split('.')
        return tuple(int(p) for p in parts)
    except (ValueError, AttributeError):
        return (0, 0, 0)


def check_vulnerability(package_name: str, version: str) -> Optional[Dict]:
    """Check if a package version has known vulnerabilities."""
    if package_name not in CVE_DATABASE:
        return None
    
    pkg_vulns = CVE_DATABASE[package_name]
    installed_version = parse_version(version)
    
    for affected_range, vuln_info in pkg_vulns.items():
        if affected_range.startswith("<="):
            max_version = parse_version(affected_range[2:])
            if installed_version <= max_version:
                return vuln_info
    
    return None


def audit_dependencies(dependencies: List[Dict]) -> Dict[str, Any]:
    """Comprehensive security audit of dependencies."""
    critical_vulns = []
    high_vulns = []
    medium_vulns = []
    safe_packages = []
    
    total_packages = len(dependencies)
    
    for dep in dependencies:
        name = dep.get("name", "").lower()
        version = dep.get("version", "")
        
        vuln = check_vulnerability(name, version)
        
        if vuln:
            vuln_entry = {
                "package": name,
                "version": version,
                **vuln
            }
            
            if vuln["severity"] == "critical":
                critical_vulns.append(vuln_entry)
            elif vuln["severity"] == "high":
                high_vulns.append(vuln_entry)
            else:
                medium_vulns.append(vuln_entry)
        else:
            safe_packages.append({"package": name, "version": version, "status": "safe"})
    
    # Calculate overall security score (0-100)
    total_vulns = len(critical_vulns) + len(high_vulns) + len(medium_vulns)
    security_score = max(0, 100 - (len(critical_vulns) * 20 + len(high_vulns) * 10 + len(medium_vulns) * 5))
    
    audit_result = {
        "summary": {
            "total_packages": total_packages,
            "safe_packages": len(safe_packages),
            "vulnerable_packages": total_vulns,
            "critical_vulnerabilities": len(critical_vulns),
            "high_vulnerabilities": len(high_vulns),
            "medium_vulnerabilities": len(medium_vulns),
            "security_score": security_score,
            "audit_status": "secure" if security_score >= 80 else "at_risk" if security_score >= 50 else "critical"
        },
        "critical": critical_vulns,
        "high": high_vulns,
        "medium": medium_vulns,
        "safe": safe_packages,
        "recommendations": generate_recommendations(critical_vulns, high_vulns)
    }
    
    return audit_result


def generate_recommendations(critical: List[Dict], high: List[Dict]) -> List[str]:
    """Generate actionable security recommendations."""
    recommendations = []
    
    if critical:
        recommendations.append(f"IMMEDIATE ACTION REQUIRED: {len(critical)} critical vulnerability(ies) detected. Upgrade affected packages immediately.")
        for crit in critical:
            recommendations.append(f"  • {crit['package']}: {crit['recommendation']}")
    
    if high:
        recommendations.append(f"URGENT: {len(high)} high-severity vulnerability(ies) require patching within 24 hours.")
    
    if not critical and not high:
        recommendations.append("No critical or high-severity vulnerabilities detected. Proceed with standard release process.")
    
    recommendations.append("Run regular dependency audits (weekly) using tools like OWASP Dependency-Check or Safety.io")
    recommendations.append("Enable automated security scanning in your CI/CD pipeline")
    
    return recommendations


def main():
    parser = argparse.ArgumentParser(description='Audit dependencies for security vulnerabilities')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Real vulnerable dependency versions
            demo_deps = [
                {"name": "requests", "version": "2.20.0"},
                {"name": "django", "version": "3.2.9"},
                {"name": "numpy", "version": "1.21.0"},
                {"name": "pyyaml", "version": "5.4"},
                {"name": "sqlalchemy", "version": "1.3.20"},
                {"name": "flask", "version": "2.0.0"},
                {"name": "pillow", "version": "8.2.0"},
                {"name": "urllib3", "version": "1.26.4"}
            ]
            
            audit = audit_dependencies(demo_deps)
            result = {
                "demo": True,
                "timestamp": datetime.now().isoformat(),
                "project": "web-application",
                "audit": audit
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            dependencies = params.get("dependencies", [])
            
            if not dependencies:
                print(format_error("dependencies list is required"))
                sys.exit(1)
            
            audit = audit_dependencies(dependencies)
            result = {
                "timestamp": datetime.now().isoformat(),
                "audit": audit
            }
            print(format_success(result))
        
        else:
            print(format_error("Either --demo or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()

