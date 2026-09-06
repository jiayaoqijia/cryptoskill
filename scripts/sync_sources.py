"""Refresh registry bundles from their recorded sources, without executing them.

Source URLs and downloaded files are data. Git revisions, bundle hashes and
owned paths are recorded only after a validated bundle is installed. Website
listings without an identifiable upstream skill remain listings.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import logging
import os
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
LOG = logging.getLogger("sync-sources")
RESERVED = {"SOURCE.md", "TRUST.md", "TRUST.auto.yaml", "bom.cdx.json"}
EXCLUDED = {".git", ".claude", ".DS_Store", "__MACOSX", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
MAX_DOWNLOAD = 64 * 1024 * 1024
MAX_BUNDLE = 16 * 1024 * 1024
MAX_FILES = 1000
SLUG = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9._-]*\Z")


class ArchiveFiles(dict):
    """Keep rejected entries visible so their bundles cannot be partial."""
    def __init__(self):
        super().__init__()
        self.rejected = set()
        self.modes = {}


def read_json(path, default=None):
    if not path.exists():
        return {} if default is None else default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp.replace(path)


def safe_path(name):
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts or "\\" in name or "\x00" in name:
        raise ValueError("unsafe upstream path")
    return path


def fetch(url, limit=MAX_DOWNLOAD):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in {
        "api.github.com", "codeload.github.com", "raw.githubusercontent.com", "clawhub.ai",
    }:
        raise ValueError("unsupported source host")
    headers = {"User-Agent": "CryptoSkill-Sync/2", "Accept": "application/json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if parsed.hostname == "api.github.com" and token:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=35) as response:
                body = response.read(limit + 1)
                if len(body) > limit:
                    raise ValueError("source exceeds download limit")
                return body
        except urllib.error.HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
            time.sleep(min(5, 2 ** attempt))
    raise RuntimeError("download failed")


def archive_files(body, zipped=False):
    """Read regular files only; never extract archive paths onto disk."""
    files = ArchiveFiles()
    total = 0
    archive = zipfile.ZipFile(io.BytesIO(body)) if zipped else tarfile.open(fileobj=io.BytesIO(body), mode="r:gz")
    with archive:
        members = archive.infolist() if zipped else archive
        for member in members:
            path = safe_path(member.filename if zipped else member.name)
            if not zipped:
                path = PurePosixPath(*path.parts[1:])  # GitHub's archive root
            if any(p.casefold() in {x.casefold() for x in EXCLUDED} for p in path.parts) or str(path) == ".":
                continue
            if zipped:
                mode = member.external_attr >> 16
                if member.is_dir():
                    continue
                if stat.S_ISLNK(mode):
                    raise ValueError("upstream archive contains a symlink")
                size = member.file_size
            else:
                if member.isdir():
                    continue
                if not member.isfile():
                    # Repositories may contain links outside a skill. Do not follow them.
                    files.rejected.add(str(path))
                    continue
                size = member.size
            total += size
            if total > 256 * 1024 * 1024 or len(files) >= 50000:
                raise ValueError("expanded repository exceeds limit")
            if size > MAX_BUNDLE:
                files.rejected.add(str(path))
                continue
            key = str(path)
            if key in files:
                raise ValueError("duplicate archive path")
            if zipped:
                files[key] = archive.read(member)
            else:
                with archive.extractfile(member) as stream:
                    files[key] = stream.read()
            files.modes[key] = 0o755 if (mode if zipped else member.mode) & 0o111 else 0o644
    return files


def github_bundle(repo, cached_revision=None):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ValueError("invalid repository name")
    result = subprocess.run(
        ["git", "ls-remote", f"https://github.com/{repo}.git", "HEAD"],
        capture_output=True, text=True, timeout=30,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    )
    sha = result.stdout.split()[0] if result.returncode == 0 and result.stdout.split() else ""
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("repository unavailable or HEAD could not be resolved")
    if sha == cached_revision:
        return sha, None
    files = archive_files(fetch(f"https://codeload.github.com/{repo}/tar.gz/{sha}"))
    return sha, files


def github_source(text):
    for url in re.findall(r"https://(?:github\.com|raw\.githubusercontent\.com)/[^\s)<>]+", text):
        parts = urllib.parse.urlsplit(url.rstrip('.,')).path.strip('/').split('/')
        if len(parts) >= 2 and all(SLUG.fullmatch(x) for x in parts[:2]):
            return '/'.join(parts[:2]).removesuffix('.git')
    return None


def skill_name(body):
    text = body.decode("utf-8", errors="replace")
    match = re.search(r"\A---\s*\n.*?^name:\s*([^\n]+)", text, re.M | re.S)
    return match.group(1).strip().strip("\"'") if match else ""


def select_skill(entry, files, previous):
    candidates = sorted(k for k in files if PurePosixPath(k).name.lower() == "skill.md")
    recorded = previous.get("path")
    if recorded:
        if recorded not in files:
            raise ValueError("recorded upstream skill removed; manual remapping required")
        return recorded
    source = entry["source"]
    for key in candidates:
        # Prefer an explicit raw/blob/tree URL recorded by bulk-add-skills.py.
        if f"/{key}" in source and (f"/{key})" in source or f"/{key}\n" in source or source.endswith('/' + key)):
            return key
    local_name = skill_name(entry["body"])
    names = {entry["slug"].casefold(), local_name.casefold()} - {""}
    scored = []
    for key in candidates:
        directory = PurePosixPath(key).parent.name
        upstream_name = skill_name(files[key])
        score = 0
        if files[key].strip() == entry["body"].strip():
            score = 100
        elif upstream_name.casefold() in names or directory.casefold() in names:
            score = 90
        elif directory and entry["slug"].casefold().endswith('-' + directory.casefold()):
            score = 70
        scored.append((score, key))
    scored.sort(reverse=True)
    if scored and scored[0][0] and (len(scored) == 1 or scored[0][0] > scored[1][0]):
        return scored[0][1]
    if len(candidates) == 1:
        return candidates[0]
    # Existing README snapshots can be refreshed as documentation; do not
    # replace a real SKILL.md with a README or guess among multiple skills.
    if not candidates and b"upstream README.md captured" in entry["body"]:
        readmes = sorted(k for k in files if k.lower() == "readme.md")
        if readmes:
            return readmes[0]
    raise ValueError("no unique upstream SKILL.md match" if candidates else "no upstream SKILL.md")


def bundle_files(files, path, entry=None):
    parent = PurePosixPath(path).parent
    if PurePosixPath(path).name.lower() == "readme.md":
        header = entry["body"].split(b"\n---\n\n", 1)[0]
        return {"SKILL.md": header + b"\n---\n\n" + files[path]}
    if any(PurePosixPath(name).is_relative_to(parent) for name in getattr(files, 'rejected', ())):
        raise ValueError('skill bundle contains links, special files, or oversized files')
    bundle = ArchiveFiles()
    for key, body in files.items():
        file_path = PurePosixPath(key)
        if not file_path.is_relative_to(parent):
            continue
        relative = file_path.relative_to(parent)
        if relative.parts[0].casefold() in {p.casefold() for p in RESERVED}:
            continue
        name = "SKILL.md" if key == path else str(relative)
        bundle[name] = body
        if key in getattr(files, 'modes', {}):
            bundle.modes[name] = files.modes[key]
    # Keep a repository license alongside skills stored below the root.
    for key, body in files.items():
        if '/' not in key and key.upper() in {"LICENSE", "LICENSE.MD", "LICENSE.TXT", "COPYING", "NOTICE"}:
            bundle.setdefault(key, body)
            bundle.modes[key] = getattr(files, 'modes', {}).get(key, 0o644)
    if len(bundle) > MAX_FILES or sum(map(len, bundle.values())) > MAX_BUNDLE:
        raise ValueError("skill bundle exceeds file or size limit")
    folded = [key.casefold() for key in bundle]
    if len(folded) != len(set(folded)):
        raise ValueError("case-colliding upstream filenames")
    return bundle


def dirty_skills(root):
    result = subprocess.run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
                            cwd=root, capture_output=True, check=True)
    dirty = set()
    for item in result.stdout.decode().split('\0'):
        path = item[3:] if len(item) >= 3 and item[2] == ' ' else item
        parts = path.split('/')
        if len(parts) >= 3 and parts[0] == 'skills':
            dirty.add('/'.join(parts[1:3]).casefold())
    return dirty


def cached_revision(group, state, repo):
    """Skip archives only when the last full scan and local file hashes agree."""
    revision = state.get("repositories", {}).get(repo)
    if not revision:
        return None
    for entry in group:
        pin = state["skills"].get(entry["key"], {})
        if pin.get("revision") != revision or not pin.get("files"):
            return None
        for name, digest in pin["files"].items():
            path = entry["destination"] / safe_path(name)
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                return None
            expected_mode = pin.get('modes', {}).get(name)
            if expected_mode is not None and bool(path.stat().st_mode & 0o111) != bool(expected_mode & 0o111):
                return None
    return revision


def install_bundle(destination, bundle, previous, source=None, dry_run=False, check=None):
    """Stage the complete result, validate it, then swap; retain local overlays."""
    if "SKILL.md" not in bundle or not bundle["SKILL.md"].strip():
        raise ValueError("missing or empty SKILL.md")
    hashes = {key: hashlib.sha256(value).hexdigest() for key, value in bundle.items()}
    modes = getattr(bundle, 'modes', {})
    if destination.is_symlink():
        raise ValueError('local bundle is a symlink')
    changed = any(not (destination / key).is_file() or (destination / key).read_bytes() != value
                  for key, value in bundle.items())
    changed = changed or (destination.exists() and any(
        p.name.lower() == 'skill.md' and p.name != 'SKILL.md' for p in destination.iterdir()))
    changed = changed or any(not (destination / key).exists() or
                            bool((destination / key).stat().st_mode & 0o111) != bool(mode & 0o111)
                            for key, mode in modes.items())
    removed = set(previous.get("files", {})) - set(bundle)
    changed = changed or any((destination / key).exists() for key in removed)
    if not changed:
        return False, hashes
    with tempfile.TemporaryDirectory(prefix="cryptoskill-stage-") as temp:
        stage = Path(temp) / "skill"
        if destination.exists():
            if any(p.is_symlink() for p in destination.rglob('*')):
                raise ValueError("local bundle contains symlinks")
            shutil.copytree(destination, stage)
        else:
            stage.mkdir()
        # Normalize legacy skill.md names on both case-sensitive and
        # case-insensitive filesystems before writing the incoming SKILL.md.
        for path in stage.iterdir():
            if path.name.lower() == 'skill.md' and path.name != 'SKILL.md':
                path.unlink()
        for key in removed:
            path = safe_path(key)
            if path.parts[0].casefold() not in {p.casefold() for p in RESERVED} and (stage / key).is_file():
                (stage / key).unlink()
        for key, body in bundle.items():
            path = safe_path(key)
            if path.parts[0].casefold() in {p.casefold() for p in RESERVED}:
                raise ValueError("upstream attempted to overwrite registry metadata")
            target = stage / key
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            if key in modes:
                target.chmod(modes[key])
        if source is not None and not (stage / "SOURCE.md").exists():
            (stage / "SOURCE.md").write_text(source, encoding="utf-8")
        if check:
            check(stage)
        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            # Same-filesystem staging makes the final renames atomic.
            with tempfile.TemporaryDirectory(prefix=".sync-", dir=destination.parent) as sibling:
                ready = Path(sibling) / "ready"
                backup = Path(sibling) / "backup"
                shutil.copytree(stage, ready)
                if destination.exists():
                    destination.rename(backup)
                try:
                    ready.rename(destination)
                except BaseException:
                    if backup.exists():
                        backup.rename(destination)
                    raise
    return True, hashes


def security_check(stage):
    # Reuse the registry's credential/obfuscation/exfiltration risk gate for
    # updates as well as additions, including official sources.
    if not hasattr(security_check, "scorer"):
        spec = importlib.util.spec_from_file_location("registry_score", ROOT / "scripts/score-skills.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        security_check.scorer = module
    _, _, passed, reasons = security_check.scorer.compute_security_score(stage)
    if not passed:
        raise ValueError("security gate: " + "; ".join(reasons))


def inventory(root):
    entries = []
    for category in sorted((root / "skills").iterdir()):
        if not category.is_dir() or category.is_symlink():
            continue
        for folder in sorted(category.iterdir()):
            if not folder.is_dir() or folder.is_symlink() or folder.name.startswith('.'):
                continue
            skill = next((p for p in folder.iterdir() if p.name.lower() == "skill.md"), None)
            if not skill:
                continue
            source = (folder / "SOURCE.md").read_text() if (folder / "SOURCE.md").exists() else ""
            entries.append({"key": f"{category.name}/{folder.name}", "category": category.name,
                            "slug": folder.name, "source": source, "body": skill.read_bytes(),
                            "repo": github_source(source), "destination": folder})
    return entries


def clawhub_bundle(entry):
    # Pin downloads to a version, and verify the recorded publisher first.
    match = re.search(r"clawhub\.ai/skills/([^/\s)]+)/([^/\s)]+)", entry["source"])
    if not match:
        raise ValueError("no recorded ClawHub owner/slug")
    owner, slug = match.groups()
    metadata = json.loads(fetch(f"https://clawhub.ai/api/v1/skills/{urllib.parse.quote(slug, safe='')}", 2 * 1024 * 1024))
    actual_owner = (metadata.get("owner") or {}).get("handle", "")
    if actual_owner.casefold() != owner.casefold():
        raise ValueError("ClawHub publisher changed or unavailable")
    moderation = metadata.get("moderation") or {}
    if moderation.get("isMalwareBlocked") or moderation.get("isSuspicious"):
        raise ValueError("ClawHub moderation flagged this skill")
    version = (metadata.get("latestVersion") or {}).get("version")
    if not version:
        raise ValueError("ClawHub has no downloadable version")
    query = urllib.parse.urlencode({"slug": slug, "version": version})
    body = fetch(f"https://clawhub.ai/api/v1/download?{query}")
    if not zipfile.is_zipfile(io.BytesIO(body)):
        raise ValueError("ClawHub source handoff requires explicit GitHub source mapping")
    files = archive_files(body, zipped=True)
    path = next((p for p in files if p.lower() == "skill.md"), None)
    if not path:
        raise ValueError("ClawHub archive has no root SKILL.md")
    return version, bundle_files(files, path)


def sync_registry(root=ROOT, official_repos=(), dry_run=False, workers=4, only_repo=None,
                  skip_clawhub=False, discover=True):
    entries = inventory(root)
    state_path = root / "scripts/source-lock.json"
    state = read_json(state_path, {"schema_version": 1, "skills": {}})
    previous = state["skills"]
    dirty = dirty_skills(root)
    report = {"generated_at": datetime.now(timezone.utc).isoformat(), "dry_run": dry_run,
              "results": [], "repositories": {}}
    groups = defaultdict(list)
    for entry in entries:
        if entry["repo"]:
            groups[entry["repo"].lower()].append(entry)
    configs = {f"{r['org']}/{r['repo']}".lower(): r for r in official_repos}
    for repo, group in groups.items():
        if repo in configs and configs[repo]['category'] == 'dev-tools':
            configs[repo] = {**configs[repo], 'category': Counter(e['category'] for e in group).most_common(1)[0][0]}
    # Existing multi-skill sources are also discovery targets. This covers
    # MoonPay, Circle, Bankr, etc. without another divergent hardcoded list.
    for repo, group in list(groups.items()):
        if repo not in configs and len(group) >= 2:
            official = all("**Classification**: OFFICIAL" in e["source"] for e in group)
            if official:
                category = Counter(e["category"] for e in group).most_common(1)[0][0]
                configs[repo] = {"category": category, "prefix": repo.split('/')[0] + "-official-"}
    for repo in configs:
        groups.setdefault(repo, [])
    if only_repo:
        groups = {repo: group for repo, group in groups.items() if repo == only_repo.lower()}

    def record(entry, status, detail=""):
        report["results"].append({"skill": entry["key"], "status": status, "detail": detail})

    def apply(entry, bundle, revision, path, repo=None, source=None):
        if entry["key"].casefold() in dirty:
            record(entry, "local_changes", "preserved local edits")
            return
        try:
            existed = entry["destination"].exists()
            changed, hashes = install_bundle(entry["destination"], bundle, previous.get(entry["key"], {}),
                                               source, dry_run=dry_run, check=security_check)
            record(entry, ("updated" if existed else "added") if changed else "unchanged")
            if not dry_run:
                previous[entry["key"]] = {"repo": repo, "path": path, "revision": revision, "files": hashes,
                                         "modes": getattr(bundle, 'modes', {})}
                if changed:
                    dates = read_json(root / "scripts/.skill-dates.json")
                    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
                    row = dates.setdefault('skills/' + entry["key"], {"added_at": now})
                    row["last_updated"] = now
                    write_json(root / "scripts/.skill-dates.json", dates)
                write_json(state_path, state)
        except (ValueError, OSError) as error:
            record(entry, "blocked", str(error))

    # Fetch independent repositories concurrently; installation stays serial.
    with ThreadPoolExecutor(max_workers=workers) as pool:
        pending = {pool.submit(github_bundle, repo, cached_revision(group, state, repo)): repo
                   for repo, group in groups.items()}
        for future in as_completed(pending):
            repo = pending.pop(future)
            group = groups[repo]
            try:
                revision, files = future.result()
            except Exception as error:
                detail = str(error) if not isinstance(error, subprocess.TimeoutExpired) else "repository request timed out"
                report["repositories"][repo] = {"status": "unavailable", "detail": detail}
                for entry in group:
                    record(entry, "unavailable", detail)
                LOG.warning("%s: %s", repo, detail)
                continue
            if files is None:
                report["repositories"][repo] = {"status": "unchanged", "revision": revision}
                for entry in group:
                    record(entry, "local_changes" if entry["key"].casefold() in dirty else "unchanged")
                LOG.info("%s unchanged; skipped archive", repo)
                continue
            report["repositories"][repo] = {"status": "fetched", "revision": revision}
            result_start = len(report["results"])
            used = set()
            for entry in group:
                try:
                    path = select_skill(entry, files, previous.get(entry["key"], {}))
                    used.add(path)
                    apply(entry, bundle_files(files, path, entry), revision, path, repo)
                except (ValueError, OSError) as error:
                    record(entry, "unresolved", str(error))
            config = configs.get(repo)
            if discover and config:
                candidates = sorted(k for k in files if PurePosixPath(k).name.lower() == "skill.md" and k not in used)
                for path in candidates:
                    # Exclude nested subskills within an already registered bundle.
                    if any(PurePosixPath(path).is_relative_to(PurePosixPath(p).parent) for p in used):
                        continue
                    name = skill_name(files[path]) or PurePosixPath(path).parent.name or repo.split('/')[1]
                    slug = config.get("prefix", "") + name
                    if not SLUG.fullmatch(slug):
                        continue
                    key = config["category"] + '/' + slug
                    if any(e["slug"].casefold() == slug.casefold() for e in entries):
                        continue
                    entry = {"key": key, "slug": slug, "category": config["category"],
                             "destination": root / "skills" / key}
                    attribution = (f"# Source Attribution\n\n- **Original Author**: {repo.split('/')[0]}\n"
                                   f"- **Source**: https://github.com/{repo}\n"
                                   f"- **Source URL**: https://github.com/{repo}/blob/{revision}/{path}\n"
                                   "- **License**: See bundled upstream license; otherwise NOASSERTION\n"
                                   f"- **Classification**: {'OFFICIAL' if config.get('official', True) else 'COMMUNITY'}\n")
                    try:
                        apply(entry, bundle_files(files, path), revision, path, repo, attribution)
                        entries.append(entry)
                    except ValueError as error:
                        record(entry, "blocked", str(error))
            if not dry_run and all(r['status'] in ('added', 'updated', 'unchanged')
                                   for r in report['results'][result_start:]):
                state.setdefault('repositories', {})[repo] = revision
                write_json(state_path, state)
            LOG.info("Fetched %s; processed %d registered entries", repo, len(group))

    claw_entries = [e for e in entries if not e.get("repo") and "clawhub.ai" in e.get("source", "")]
    if not skip_clawhub and not only_repo:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            pending = {pool.submit(clawhub_bundle, entry): entry for entry in claw_entries}
            for future in as_completed(pending):
                entry = pending.pop(future)
                try:
                    revision, bundle = future.result()
                    apply(entry, bundle, revision, "SKILL.md")
                except Exception as error:
                    record(entry, "unavailable", str(error))
                if len(pending) % 25 == 0:
                    LOG.info('ClawHub: %d/%d checked', len(claw_entries) - len(pending), len(claw_entries))
        LOG.info("Checked %d ClawHub sources", len(claw_entries))
    covered = {r["skill"] for r in report["results"]}
    for entry in entries:
        if entry["key"] not in covered:
            record(entry, "skipped" if only_repo or (skip_clawhub and entry in claw_entries) else "listing_only",
                   "source outside this run" if only_repo else "no fetchable skill source")
    report["results"].sort(key=lambda r: r["skill"])
    report["summary"] = dict(Counter(r["status"] for r in report["results"]))
    if not dry_run:
        write_json(root / "docs/sync-report.json", report)
    LOG.info("Source refresh: %s", report["summary"])
    return report
