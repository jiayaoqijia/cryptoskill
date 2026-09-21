#!/usr/bin/env python3
"""osv_scan.py - check project dependencies against the OSV.dev vulnerability database.

Usage:
    python3 osv_scan.py [project_root]

Requires: Python 3.8+, network access to api.osv.dev. No third-party packages.

Supported manifests:
  npm:      package-lock.json, yarn.lock, pnpm-lock.yaml
  python:   requirements.txt, Pipfile.lock, poetry.lock
  ruby:     Gemfile.lock
  rust:     Cargo.lock
  php:      composer.lock
  go:       go.sum
  java:     pom.xml, gradle.lockfile
  swift:    Package.resolved (v1 and v2)
  c/c++:    conan.lock
  dotnet:   packages.config
  dart:     pubspec.lock
  elixir:   mix.lock

Heuristic parsers - some exotic manifest formats may be missed; always also
review `dependency-vulns/SKILL.md` Step 2 (manifest hygiene).
"""
import json
import os
import re
import sys
import urllib.request

API = "https://api.osv.dev/v1"
SKIP_DIRS = {".git", "node_modules", "vendor", "target", "dist", "build",
             ".venv", "venv", "__pycache__", "coverage", ".next", ".terraform"}
MANIFEST_NAMES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "requirements.txt",
    "Pipfile.lock", "poetry.lock", "Gemfile.lock", "Cargo.lock",
    "composer.lock", "go.sum", "pom.xml", "packages.config", "pubspec.lock",
    "gradle.lockfile", "Package.resolved", "conan.lock", "mix.lock",
}


# ---------------------------------------------------------------- parsing

def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def pairs_ecosystem(deps, eco):
    return [(eco, n, v) for n, v in deps]


def parse_npm_lock(path):
    d = json.loads(read_text(path))
    out = set()
    for key, val in (d.get("packages") or {}).items():
        if key.startswith("node_modules/") and isinstance(val, dict) and "version" in val:
            name = key.split("node_modules/")[-1]
            out.add((name, val["version"]))
    if not out:  # lockfileVersion 1
        def walk(deps):
            for name, val in (deps or {}).items():
                if isinstance(val, dict):
                    if "version" in val:
                        out.add((name, val["version"]))
                    walk(val.get("dependencies"))
        walk(d.get("dependencies"))
    return pairs_ecosystem(out, "npm")


def parse_yarn_lock(path):
    out, name = set(), None
    for line in read_text(path).splitlines():
        s = line.strip()
        if not line.startswith(" ") and "@" in s and s.endswith(":") and not s.startswith("#"):
            base = s.rstrip(":").strip('"')
            parts = base.split("@")
            name = ("@" + parts[1]) if base.startswith("@") else parts[0]
        elif name and s.startswith('version "'):
            out.add((name, s.split('"')[1]))
            name = None
    return pairs_ecosystem(out, "npm")


def parse_pnpm_lock(path):
    out = set()
    for m in re.finditer(r"^\s{2,}(['\"]?)([\w@/.-]+)\1:\s*$\n(?:\s{4,}.*\n)*?\s{4,}version:\s*['\"]?([^'\"\s]+)",
                         read_text(path), re.M):
        out.add((m.group(2), m.group(3)))
    return pairs_ecosystem(out, "npm")


def parse_requirements(path):
    out = set()
    for line in read_text(path).splitlines():
        m = re.match(r"\s*([A-Za-z0-9_.\-]+)\s*==\s*([^\s;#]+)", line)
        if m:
            out.add(m.groups())
    return pairs_ecosystem(out, "PyPI")


def parse_pipfile_lock(path):
    d = json.loads(read_text(path))
    out = set()
    for section in ("default", "develop"):
        for name, val in (d.get(section) or {}).items():
            v = (val or {}).get("version", "").lstrip("=~<!")
            if v:
                out.add((name, v))
    return pairs_ecosystem(out, "PyPI")


def parse_poetry_lock(path):
    text = read_text(path)
    out = {(n, v) for n, v in re.findall(r'name\s*=\s*"([^"]+)"\s*\nversion\s*=\s*"([^"]+)"', text)}
    return pairs_ecosystem(out, "PyPI")


def parse_gemfile_lock(path):
    out, in_gems = set(), False
    for line in read_text(path).splitlines():
        if re.match(r"^[A-Z]+$", line.strip()):
            in_gems = line.strip() == "GEM"
            continue
        if in_gems and line.startswith("    ") and not line.lstrip().startswith("#"):
            m = re.match(r"\s{4}([A-Za-z0-9_:.\-]+)\s+\(([^)]+)\)", line)
            if m:
                out.add(m.groups())
    return pairs_ecosystem(out, "RubyGems")


def parse_cargo_lock(path):
    text = read_text(path)
    out = {(n, v) for n, v in re.findall(r'name\s*=\s*"([^"]+)"\s*\nversion\s*=\s*"([^"]+)"', text)}
    return pairs_ecosystem(out, "crates.io")


def parse_composer_lock(path):
    d = json.loads(read_text(path))
    out = set()
    for section in ("packages", "packages-dev"):
        for pkg in d.get(section) or []:
            if pkg.get("name") and pkg.get("version"):
                out.add((pkg["name"], pkg["version"].lstrip("v")))
    return pairs_ecosystem(out, "Packagist")


def parse_go_sum(path):
    out = set()
    for line in read_text(path).splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1].startswith("v") and not parts[0].endswith("/go.mod"):
            out.add((parts[0], parts[1]))
    return pairs_ecosystem(out, "Go")


def parse_pom_xml(path):
    text = read_text(path)
    out = set()
    for block in re.findall(r"<dependency>.*?</dependency>", text, re.S):
        g = re.search(r"<groupId>([^<]+)</groupId>", block)
        a = re.search(r"<artifactId>([^<]+)</artifactId>", block)
        v = re.search(r"<version>([^<]+)</version>", block)
        if g and a and v and "$" not in v.group(1):
            out.add((f"{g.group(1)}:{a.group(1)}", v.group(1)))
    return pairs_ecosystem(out, "Maven")


def parse_gradle_lock(path):
    # Lines: group:artifact:version=configuration(s)
    out = set()
    for line in read_text(path).splitlines():
        m = re.match(r"^([^=#\s]+)=\S+", line.strip())
        if m:
            parts = m.group(1).split(":")
            if len(parts) == 3:
                out.add((f"{parts[0]}:{parts[1]}", parts[2]))
    return pairs_ecosystem(out, "Maven")


def parse_package_resolved(path):
    # v1: {"object": {"pins": [{"package", "repositoryURL", "state"}]}}
    # v2: {"pins": [{"identity", "location", "state"}]}
    d = json.loads(read_text(path))
    out = set()
    pins = d.get("pins") or (d.get("object") or {}).get("pins") or []
    for pin in pins:
        ver = (pin.get("state") or {}).get("version")
        name = pin.get("location") or pin.get("repositoryURL") or pin.get("package")
        if ver and name:
            out.add((name, ver.lstrip("v")))
    return pairs_ecosystem(out, "SwiftURL")


def parse_conan_lock(path):
    # refs: name/version#revision%context or name/version@user/channel#rev
    d = json.loads(read_text(path))
    out = set()
    refs = list(d.get("requires") or []) + list(d.get("build_requires") or [])
    for ref in refs:
        ref = ref.split("%")[0].split("#")[0].split("@")[0]
        parts = ref.split("/")
        if len(parts) >= 2:
            out.add((parts[0], parts[1]))
    return pairs_ecosystem(out, "ConanCenter")


def parse_mix_lock(path):
    # Erlang map: %{ "name": {:hex, :name, "version", ...} } ("=>" in older files;
    # :path and :git deps have no version and are skipped)
    out = set()
    for m in re.finditer(r'"([^"]+)"\s*(?::|=>)\s*\{:hex,\s*:[\w.\-]+,\s*"([^"]+)"',
                         read_text(path)):
        out.add(m.groups())
    return pairs_ecosystem(out, "Hex")


def parse_packages_config(path):
    text = read_text(path)
    out = {(i, v) for i, v in re.findall(r'<package\s+id="([^"]+)"\s+version="([^"]+)"', text)}
    return pairs_ecosystem(out, "NuGet")


def parse_pubspec_lock(path):
    text = read_text(path)
    out = {(n, v) for n, v in re.findall(
        r'^  ([\w_]+):\n(?:    .*\n)*?    version:\s*["\']?([^"\'\s]+)', text, re.M)}
    return pairs_ecosystem(out, "Pub")


PARSERS = {
    "package-lock.json": parse_npm_lock,
    "yarn.lock": parse_yarn_lock,
    "pnpm-lock.yaml": parse_pnpm_lock,
    "requirements.txt": parse_requirements,
    "Pipfile.lock": parse_pipfile_lock,
    "poetry.lock": parse_poetry_lock,
    "Gemfile.lock": parse_gemfile_lock,
    "Cargo.lock": parse_cargo_lock,
    "composer.lock": parse_composer_lock,
    "go.sum": parse_go_sum,
    "pom.xml": parse_pom_xml,
    "gradle.lockfile": parse_gradle_lock,
    "Package.resolved": parse_package_resolved,
    "conan.lock": parse_conan_lock,
    "mix.lock": parse_mix_lock,
    "packages.config": parse_packages_config,
    "pubspec.lock": parse_pubspec_lock,
}


# ---------------------------------------------------------------- OSV API

def http_json(url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def severity_of(vuln):
    spec = (vuln.get("database_specific") or {}).get("severity")
    if spec:
        return spec.upper()
    for aff in vuln.get("affected") or []:
        eco = aff.get("ecosystem_specific") or {}
        if isinstance(eco.get("severity"), str):
            return eco["severity"].upper()
    return "UNKNOWN"


def fixed_versions(vuln):
    fixed = set()
    for aff in vuln.get("affected") or []:
        for rng in aff.get("ranges") or []:
            for ev in rng.get("events") or []:
                if "fixed" in ev:
                    fixed.add(ev["fixed"])
    return sorted(fixed)


def query_osv(packages):
    results = {}
    queries = [{"package": {"ecosystem": eco, "name": name}, "version": ver}
               for eco, name, ver in packages]
    for i in range(0, len(queries), 500):
        chunk = queries[i:i + 500]
        try:
            resp = http_json(f"{API}/querybatch", {"queries": chunk})
        except Exception as exc:
            print(f"[!] batch query failed: {exc}", file=sys.stderr)
            continue
        for query, res in zip(chunk, resp.get("results", [])):
            ids = [v["id"] for v in res.get("vulns", [])]
            if ids:
                key = (query["package"]["ecosystem"], query["package"]["name"], query["version"])
                results[key] = ids
    return results


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    packages, manifests = set(), []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if fname in MANIFEST_NAMES:
                path = os.path.join(dirpath, fname)
                try:
                    found = PARSERS[fname](path)
                except Exception as exc:
                    print(f"[!] parse error {path}: {exc}", file=sys.stderr)
                    continue
                if found:
                    manifests.append(os.path.relpath(path, root))
                    packages.update(found)

    if not packages:
        print("No dependency manifests found (or none parseable).")
        return

    print(f"Scanned {len(manifests)} manifest(s), {len(packages)} unique package@version pairs.\n")
    results = query_osn = query_osv(sorted(packages))

    total = 0
    detail_fetches = 0
    DETAIL_LIMIT = 30  # bound API traffic; the rest are reported as IDs only
    for (eco, name, ver), ids in sorted(results.items()):
        for vid in ids:
            total += 1
            line = f"[VULN] {eco}:{name}@{ver}  {vid}"
            if detail_fetches >= DETAIL_LIMIT:
                print(f"{line}\n      (details skipped; see https://osv.dev/vulnerability/{vid})")
                continue
            detail_fetches += 1
            try:
                vuln = http_json(f"{API}/vulns/{vid}")
                aliases = ",".join(a for a in vuln.get("aliases", []) if a.startswith("CVE")) or "-"
                summary = (vuln.get("summary") or vuln.get("details", ""))[:110].replace("\n", " ")
                fixed = ",".join(fixed_versions(vuln)) or "none listed"
                print(f"{line}\n      aliases: {aliases}\n      severity: {severity_of(vuln)}  fixed in: {fixed}\n      {summary}")
            except Exception:
                print(f"{line}\n      (details unavailable; see https://osv.dev/vulnerability/{vid})")

    print(f"\n{total} vulnerabilit(ies) across {len(results)} package(s).")
    print("Reachability matters: prioritize deps whose code the app actually imports.")


if __name__ == "__main__":
    main()
