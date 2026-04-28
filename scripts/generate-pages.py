#!/usr/bin/env python3
"""Generate individual HTML pages for every skill in CryptoSkill.

Reads docs/skills.json and produces:
  - docs/skills/{category}/{skill-name}.html  (one per skill)
  - docs/skills/{category}/index.html          (one per category)
  - docs/sitemap.xml                           (regenerated with all URLs)

All pages are lightweight (<5 KB), static, and SEO-optimised.
"""

import html
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

# Trust manifest support — read TRUST.auto.yaml via the canonical safe parser.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from canonicalize import parse_canonical_yaml  # noqa: E402
except ImportError:
    parse_canonical_yaml = None  # graceful degradation if ruamel/rfc8785 missing

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
SKILLS_DIR = os.path.join(ROOT, "skills")
SKILLS_JSON = os.path.join(DOCS, "skills.json")
SITE = "https://cryptoskill.org"
GH_BLOB = "https://github.com/jiayaoqijia/cryptoskill/blob/main"
GH_TREE = "https://github.com/jiayaoqijia/cryptoskill/tree/main"

# Capabilities considered "negative-leaning red flags" — when true the UI
# surfaces them prominently. Order is the rendering order in the panel.
# Each entry is (key, label, hover-explanation).
RED_FLAG_CAPS = [
    ("can_move_funds",            "Can move funds",              "Sends or signs transactions; can move user funds"),
    ("requires_private_key",      "Requires private key",        "Asks the user for a key, mnemonic, or wallet config"),
    ("requires_hosted_operator",  "Requires hosted operator",    "Correct behavior depends on a specific company's running infrastructure"),
    ("uses_remote_install_script","Uses remote install script",  "Setup runs a script downloaded from the internet (curl|sh class)"),
    ("mutable_remote_runtime",    "Mutable remote runtime",      "Executes remote code whose behavior can change without a local diff"),
    ("can_install_code",          "Can install code",            "Runs npx, pip install, or downloads CLIs at install time"),
    ("can_execute_shell",         "Can execute shell",           "Runs arbitrary Bash"),
    ("can_browse_web",            "Can browse the web",          "Fetches arbitrary URLs"),
    ("can_write_files",           "Can write files",             "Edits the user's local files"),
    ("can_spawn_subagents",       "Can spawn sub-agents",        "Calls sub-skills or other agents"),
    ("auto_invocable",            "Auto-invocable",              "Will be invoked by the agent without explicit user prompt"),
]

# Plain-language hint shown next to each capability so a non-engineer can
# tell what the flag actually means in practice. Keep one short clause.
RED_FLAG_HINTS = {
    "can_move_funds":            "this skill can sign and send transactions on your behalf",
    "requires_private_key":      "you must hand over a private key, mnemonic, or wallet config",
    "requires_hosted_operator":  "depends on a third-party hosted service to function",
    "uses_remote_install_script":"setup pipes a remote shell script (curl | sh class)",
    "mutable_remote_runtime":    "runs remote code that can change behavior without a local diff",
    "can_install_code":          "installs software at setup time (npx, pip, brew, etc.)",
    "can_execute_shell":         "runs arbitrary shell commands on your machine",
    "can_browse_web":            "fetches arbitrary URLs at runtime",
    "can_write_files":           "writes to your local filesystem",
    "can_spawn_subagents":       "delegates to other skills or sub-agents",
    "auto_invocable":            "may be invoked by the agent without your explicit prompt",
}

# ── helpers ──────────────────────────────────────────────────────────

def esc(text):
    """HTML-escape a string, return empty string for None."""
    if text is None:
        return ""
    return html.escape(str(text), quote=True)


def url_path(text):
    """URL-encode a path segment for href contexts. Skill names and category
    ids in our catalog are kebab-case ASCII today, but defense-in-depth is
    cheap and prevents future-introduced unsafe chars from breaking out."""
    if text is None:
        return ""
    return quote(str(text), safe="-_.~")


def safe_jsonld(obj):
    """Serialize JSON-LD safely for embedding in <script type='application/ld+json'>.
    Escapes '<' so a stray '</script>' inside a string can't terminate the
    surrounding script element, and escapes line/paragraph separators that
    are valid in JSON but not in HTML script contexts."""
    return (
        json.dumps(obj, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(" ", "\\u2028")
        .replace(" ", "\\u2029")
    )


def grade_color(grade):
    if grade in ("A+", "A"):
        return "#22c55e"
    if grade in ("A-", "B+", "B"):
        return "#3b82f6"
    if grade in ("B-", "C+", "C"):
        return "#eab308"
    return "#ef4444"


def risk_color(gate):
    if gate == "PASS":
        return "#22c55e"
    return "#ef4444"


def category_display(cat_id, categories):
    """Return (display name, icon) for a category id."""
    info = categories.get(cat_id, {})
    return info.get("name", cat_id.replace("-", " ").title()), info.get("icon", "")


# ── Trust manifest helpers (TRUST.md §"File viewer", §"UI: red flags first") ──

def load_trust_manifest(category, skill_name):
    """Read TRUST.auto.yaml for a skill, return parsed dict or None."""
    if parse_canonical_yaml is None:
        return None
    path = Path(SKILLS_DIR) / category / skill_name / "TRUST.auto.yaml"
    if not path.exists():
        return None
    try:
        return parse_canonical_yaml(path.read_text(encoding="utf-8"))
    except Exception:
        # An ill-formed manifest must not break page generation.
        return None


def _cap_field(caps, key):
    """Return (value, confidence, source) tri-state for a capability key."""
    raw = (caps or {}).get(key)
    if isinstance(raw, dict):
        return raw.get("value"), raw.get("confidence"), raw.get("source")
    return raw, None, None


def _red_flag_summary(trust):
    """Return (n_true, n_unknown) over the eleven negative-leaning caps.
    Both numbers matter for the badge: 0 known true + 7 unknown is NOT the
    same as 0 known true + 0 unknown, and the UI must not collapse them."""
    if not trust:
        return None
    caps = trust.get("capabilities") or {}
    n_true = 0
    n_unknown = 0
    for key, _label, _hover in RED_FLAG_CAPS:
        v, _, _ = _cap_field(caps, key)
        if v is True:
            n_true += 1
        elif v is None or v == "unknown":
            n_unknown += 1
    return n_true, n_unknown


def _red_flag_count(trust):
    """Backwards-compat: just the true count."""
    s = _red_flag_summary(trust)
    return None if s is None else s[0]


def _capability_row(key, label, hover, value, confidence, source, group):
    """One row in the grouped capability list.

    Each row carries: state icon (sized + colored), label, hint sentence,
    confidence dot. We deliberately drop the verbose "medium / extracted"
    pills that previously appeared on every row — they were visual noise
    that didn't help a user pick out the actual red flags.
    """
    icon_map  = {"true": "&#x26A0;",        "false": "&#x2713;",       "unknown": "?"}
    aria_map  = {"true": "Yes — red flag",  "false": "No — cleared",   "unknown": "Not measured"}
    conf_dot = ""
    if value in (True, False) and confidence:
        conf_dot = (
            f"<span class='trust-cap-confidence trust-cap-confidence--{esc(confidence)}'"
            f" title='{esc(confidence)} confidence ({esc(source or 'unknown')})'"
            f" aria-label='{esc(confidence)} confidence based on {esc(source or 'unknown')} evidence'></span>"
        )
    hint = RED_FLAG_HINTS.get(key, hover)
    return (
        f"<li class='trust-cap-v2' data-state='{group}'>"
        f"  <span class='trust-cap-icon' aria-label='{aria_map[group]}' title='{aria_map[group]}'>{icon_map[group]}</span>"
        f"  <div class='trust-cap-body'>"
        f"    <span class='trust-cap-label'>{esc(label)}</span>"
        f"    <span class='trust-cap-hint'>{esc(hint)}</span>"
        f"  </div>"
        f"  {conf_dot}"
        f"</li>"
    )


def _capability_section(title, kicker, group_class, rows):
    """Render one of the three grouped capability sections (flags / cleared /
    not measured). Hidden when the group is empty — no point printing
    'Cleared (0)'."""
    if not rows:
        return ""
    count = len(rows)
    return (
        f"<section class='trust-cap-group trust-cap-group--{group_class}'>"
        f"  <header class='trust-cap-group-header'>"
        f"    <span class='trust-cap-group-count'>{count}</span>"
        f"    <span class='trust-cap-group-title'>{esc(title)}</span>"
        f"    <span class='trust-cap-group-kicker'>{esc(kicker)}</span>"
        f"  </header>"
        f"  <ul class='trust-cap-list-v2'>{''.join(rows)}</ul>"
        f"</section>"
    )


def trust_panel_html(trust, category, skill_name):
    """Render the per-skill Trust Manifest panel.

    Honest defaults per TRUST.md §"UI: red flags first":
    - Stage renders 'not yet evaluated' until Phase 3 rosette computed
    - Capability list shows ALL eleven, with tri-state value
    - Audits section says 'no audits attempted' (distinct from "audited and clean")
    - Ingredients section shows detected hosted operators only (Phase 1)
    - Source links: GitHub blob + raw TRUST.auto.yaml + tree
    """
    cat_q = url_path(category)
    skill_q = url_path(skill_name)
    blob_skill = f"{GH_BLOB}/skills/{cat_q}/{skill_q}/SKILL.md"
    blob_trust = f"{GH_BLOB}/skills/{cat_q}/{skill_q}/TRUST.auto.yaml"
    blob_source = f"{GH_BLOB}/skills/{cat_q}/{skill_q}/SOURCE.md"
    tree_dir = f"{GH_TREE}/skills/{cat_q}/{skill_q}"

    if trust is None:
        return f"""
    <h2 id="trust">Trust profile</h2>
    <div class="trust-panel">
      <p class="trust-empty">We haven't scanned this skill yet — every capability should be considered <strong>unknown</strong> until we do.</p>
      <div class="trust-source-links">
        <a href="{blob_skill}" target="_blank" rel="noopener">View SKILL.md &rarr;</a>
        <a href="{tree_dir}" target="_blank" rel="noopener">Browse directory &rarr;</a>
      </div>
    </div>"""

    # Group capabilities by state so the user reads the most important
    # group first (red flags), then the cleared list, then unmeasured.
    caps = trust.get("capabilities") or {}
    flag_rows, clear_rows, unknown_rows = [], [], []
    for key, label, hover in RED_FLAG_CAPS:
        v, conf, src = _cap_field(caps, key)
        if v is True:
            flag_rows.append(_capability_row(key, label, hover, v, conf, src, "true"))
        elif v is False:
            clear_rows.append(_capability_row(key, label, hover, v, conf, src, "false"))
        else:
            unknown_rows.append(_capability_row(key, label, hover, v, conf, src, "unknown"))

    n_true, n_false, n_unknown = len(flag_rows), len(clear_rows), len(unknown_rows)

    # Quick summary pills under the heading — let a user see the breakdown
    # in <1 second before deciding to read the detail sections.
    quick_pills = (
        f"<div class='trust-quick-pills'>"
        f"  <span class='trust-pill trust-pill--flags'>{n_true} red flag{'s' if n_true != 1 else ''}</span>"
        f"  <span class='trust-pill trust-pill--clear'>{n_false} cleared</span>"
        f"  <span class='trust-pill trust-pill--unknown'>{n_unknown} not measured</span>"
        f"</div>"
    )

    sections = (
        _capability_section(
            "Red flags",
            "things this skill can do that affect your security or funds",
            "flags", flag_rows,
        )
        + _capability_section(
            "Cleared by scanner",
            "we scanned the skill's text & scripts and found no evidence of these",
            "clear", clear_rows,
        )
        + _capability_section(
            "Not measured yet",
            "scanner couldn't make a confident call — treat as a possible red flag",
            "unknown", unknown_rows,
        )
    )

    # Ingredient list — Phase 1 surfaces detected_hosted_operators only;
    # the full CycloneDX BOM lands in Phase 2.
    operators = trust.get("detected_hosted_operators") or []
    if operators:
        ing_items = "".join(
            f"<li class='trust-ingredient'>"
            f"<span class='trust-ingredient-kind'>service</span> "
            f"<code>{esc(op)}</code>"
            f"</li>" for op in operators
        )
        ingredients = f"""
      <h3 class="trust-subhead">Ingredients (services this skill talks to)</h3>
      <p class="trust-help">External services this skill needs in order to work. The skill's behavior depends on these services being up, honest, and unchanged. Today we only show services we recognize from a curated list of ~50 well-known hosts (exchanges, RPC providers, data APIs); a complete dependency list — including every package, library, and binary the skill installs or imports — is on the roadmap.</p>
      <ul class="trust-ingredient-list">{ing_items}</ul>"""
    else:
        ingredients = """
      <h3 class="trust-subhead">Ingredients (services this skill talks to)</h3>
      <p class="trust-empty trust-help">We did not find any well-known hosted services in this skill's text or scripts. <strong>This does NOT mean the skill is local-only</strong> — it might use services we don't yet recognize, or talk to them through code paths our scanner can't reach. A complete dependency list (every package, library, and binary, with integrity hashes) is on the roadmap; today we only show recognized hosts.</p>"""

    # Execution mode summary
    modes = trust.get("execution_modes") or []
    if modes:
        mode_label = esc(modes[0].get("label") or "unknown")
        mode_desc = esc(modes[0].get("description") or "")
        mode_html = f"""
      <h3 class="trust-subhead">Execution mode</h3>
      <p class="trust-mode"><code>{mode_label}</code> {mode_desc}</p>"""
    else:
        mode_html = ""

    # Audits — TRUST.md §"Audits — evidence-of-absence vs absence-of-evidence"
    audits = trust.get("audits") or []
    if audits:
        rows = []
        for a in audits:
            rev = (a.get("reviewer") or {})
            rows.append(
                f"<li class='trust-audit'>"
                f"<strong>{esc(rev.get('name'))}</strong> "
                f"<span class='trust-tier trust-tier--{esc(rev.get('tier','unverified'))}'>{esc(rev.get('tier','unverified'))}</span>"
                f" &middot; subject <code>{esc(a.get('subject'))}</code>"
                f" &middot; {esc(a.get('date',''))}"
                f"</li>"
            )
        audits_html = f"""
      <h3 class="trust-subhead">Audits</h3>
      <ul class="trust-audit-list">{''.join(rows)}</ul>"""
    else:
        audits_html = """
      <h3 class="trust-subhead">Audits</h3>
      <p class="trust-empty trust-help"><strong>No one has audited this skill yet.</strong> That is different from &ldquo;audited and clean&rdquo; &mdash; it just means no professional reviewer (a security firm, the CryptoSkill team, or a verified independent researcher) has signed off on it. There are no audit reports to read.
      <a href="../../TRUST.md" target="_blank" rel="noopener">How reviewer levels work &rarr;</a></p>"""

    stage = trust.get("stage")
    # "Stage" is borrowed from L2BEAT (Stage 0/1/2 trust ladder). Until we
    # compute the underlying evidence in a future release, we leave the
    # label off entirely rather than show internal jargon.
    stage_text = "trust grade not computed yet" if stage is None else esc(str(stage))
    extractor = esc(trust.get("generator") or "extract-capabilities")
    hostlist_v = esc(trust.get("hostlist_version") or "n/a")

    return f"""
    <h2 id="trust">Trust profile <span class="trust-stage-pill">{stage_text}</span></h2>
    {quick_pills}
    <p class="trust-help">Capabilities below are detected automatically by an open-source scanner that reads the skill's text and scripts (see <a href="../../TRUST.md" target="_blank" rel="noopener">how this is computed</a>). <strong>Not measured</strong> means the scanner couldn't make a confident call &mdash; it is NOT a green check, and you should treat it as a possible red flag until a human or a stronger scanner has measured it.</p>
    <div class="trust-panel">
{sections}
{mode_html}
{ingredients}
{audits_html}
      <p class="trust-source-links">
        <a href="{blob_skill}" target="_blank" rel="noopener">SKILL.md &rarr;</a>
        <a href="{blob_source}" target="_blank" rel="noopener">SOURCE.md &rarr;</a>
        <a href="{blob_trust}" target="_blank" rel="noopener">TRUST.auto.yaml &rarr;</a>
        <a href="{tree_dir}" target="_blank" rel="noopener">Browse directory &rarr;</a>
      </p>
      <p class="trust-foot">Auto-generated by {extractor} &middot; hosted-service list version {hostlist_v} &middot; <a href="../../TRUST.md" target="_blank" rel="noopener">how this is computed</a></p>
    </div>"""


# ── page templates ───────────────────────────────────────────────────

def skill_page_html(skill, categories):
    s = skill
    name = esc(s["name"])
    display = esc(s.get("displayName", s["name"]))
    desc = esc(s.get("description", ""))
    desc_short = desc[:160] if len(desc) > 160 else desc
    cat = s.get("category", "")
    cat_display, cat_icon = category_display(cat, categories)
    author = esc(s.get("author", "unknown"))
    version = esc(s.get("version", "1.0.0"))
    tags = s.get("tags", [])

    score = s.get("score", {})
    total = score.get("total", "")
    grade = score.get("grade", "")
    risk_gate = score.get("risk_gate", "")

    # Trust manifest data (TRUST.auto.yaml). May be None if not yet computed.
    trust = load_trust_manifest(cat, s["name"])
    trust_html = trust_panel_html(trust, cat, s["name"])
    summary = _red_flag_summary(trust)
    flag_badge = ""
    if summary is not None:
        n_true, n_unknown = summary
        title = f"{n_true} true, {n_unknown} unknown of 11 capability flags"
        if n_true == 0 and n_unknown == 0:
            flag_badge = f'<span class="skill-badge trust-flag-badge trust-flag-zero" title="{title}">0 known flags</span>'
        elif n_true == 0 and n_unknown > 0:
            # Don't paint the badge green when most capabilities are simply unmeasured.
            flag_badge = f'<span class="skill-badge trust-flag-badge trust-flag-mostly-unknown" title="{title}">0 known &middot; {n_unknown} unknown</span>'
        else:
            plural = "s" if n_true != 1 else ""
            flag_badge = f'<span class="skill-badge trust-flag-badge trust-flag-some" title="{title}">{n_true} flag{plural}</span>'

    # Build tags HTML
    tags_html = ""
    for t in tags:
        tags_html += f'<span class="skill-tag">{esc(t)}</span>\n'

    # Grade + risk badge
    grade_badge = ""
    if grade:
        gc = grade_color(grade)
        grade_badge = f'<span class="skill-badge" style="background:rgba({_hex_to_rgb(gc)},0.12);color:{gc}">{esc(grade)}</span>'

    risk_badge = ""
    if risk_gate:
        rc = risk_color(risk_gate)
        risk_badge = f'<span class="skill-badge" style="background:rgba({_hex_to_rgb(rc)},0.12);color:{rc}">{esc(risk_gate)}</span>'

    # Quality section
    quality_html = ""
    if total != "":
        quality_html = f"""
    <h2>Quality Score</h2>
    <div class="skill-meta" style="margin-top:8px">
      <span>Score: <strong>{esc(str(total))}/100</strong></span>
      <span>Grade: <strong>{esc(grade)}</strong></span>
      <span>Risk Gate: <strong>{esc(risk_gate)}</strong></span>
    </div>"""

    # JSON-LD — encode URL segments and escape `<` so a stray `</script>`
    # inside a string field cannot terminate the surrounding script element.
    ld_json = safe_jsonld({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": s.get("displayName", s["name"]),
        "description": s.get("description", ""),
        "applicationCategory": "DeveloperApplication",
        "url": f"{SITE}/skills/{url_path(cat)}/{url_path(s['name'])}.html",
        "author": {"@type": "Organization", "name": s.get("author", "unknown")},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    })

    canonical_url = f"{SITE}/skills/{url_path(cat)}/{url_path(s['name'])}.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{display} - CryptoSkill | Crypto AI Agent Skill</title>
  <meta name="description" content="{desc_short}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{display} - CryptoSkill">
  <meta property="og:description" content="{desc_short}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:site_name" content="CryptoSkill">
  <meta property="og:image" content="{SITE}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{display} - CryptoSkill">
  <meta name="twitter:description" content="{desc_short}">
  <meta name="twitter:site" content="@cryptaborgs">
  <meta name="twitter:image" content="{SITE}/og-image.png">
  <link rel="icon" href="../../favicon.ico" sizes="any">
  <link rel="icon" type="image/png" href="../../favicon.png" sizes="32x32">
  <link rel="apple-touch-icon" href="../../apple-touch-icon.png">
  <link rel="stylesheet" href="../../styles.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-3VP1G7H67L"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-3VP1G7H67L');</script>
  <script type="application/ld+json">{ld_json}</script>
</head>
<body>
  <nav class="navbar"><div class="container">
    <a href="../../" class="nav-logo"><img src="../../icon.png" width="28" height="28" alt="CryptoSkill" style="border-radius:6px"> CryptoSkill</a>
    <ul class="nav-links" id="navLinks">
      <li><a href="../../#official">Official</a></li>
      <li><a href="../../#skills">Skills</a></li>
      <li><a href="../../#categories">Categories</a></li>
      <li><a href="../../#how-it-works">How It Works</a></li>
      <li><a href="https://github.com/jiayaoqijia/cryptoskill" target="_blank" rel="noopener">GitHub</a></li>
    </ul>
    <div class="nav-right">
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">
        <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
        <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      </button>
      <button class="mobile-toggle" id="mobileToggle" aria-label="Toggle menu"><span></span><span></span><span></span></button>
    </div>
  </div></nav>

  <div class="legal-content" style="padding-top:100px">
    <nav class="breadcrumb">
      <a href="../../">Home</a> &rsaquo; <a href="../../#categories">{esc(cat_display)}</a> &rsaquo; {display}
    </nav>

    <h1>{display}</h1>
    <div class="skill-meta">
      <span class="skill-badge">{esc(cat_display)}</span>
      <span>by @{author}</span>
      <span>v{version}</span>
      {grade_badge}
      {risk_badge}
      {flag_badge}
    </div>
    <p class="skill-page-desc">{desc}</p>

    <h2>Install</h2>
    <div class="install-cmd"><span class="prompt">$</span> <code>cp -r cryptoskill/skills/{esc(cat)}/{name} .claude/skills/</code></div>
    <div class="install-cmd"><span class="prompt">$</span> <code>clawhub install {name}</code></div>

    <h2>Tags</h2>
    <div class="skill-tags" style="margin-bottom:32px">
      {tags_html}
    </div>
{quality_html}

{trust_html}

    <h2>Source</h2>
    <p><a href="https://github.com/jiayaoqijia/cryptoskill/tree/main/skills/{esc(cat)}/{name}" target="_blank" rel="noopener">View on GitHub &rarr;</a></p>
  </div>

  <footer class="footer"><div class="container">
    <div class="footer-left"><span class="footer-brand">CryptoSkill</span><span class="footer-text">Built for the crypto community</span></div>
    <div class="footer-links">
      <a href="https://github.com/jiayaoqijia/cryptoskill" target="_blank" rel="noopener"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg> GitHub</a>
      <a href="../../#official">Official</a>
      <a href="../../#skills">Skills</a>
      <a href="../../#categories">Categories</a>
      <a href="../../terms.html">Terms</a>
      <a href="../../privacy.html">Privacy</a>
    </div>
  </div></footer>

  <script>
    var t=document.getElementById('themeToggle'),s=localStorage.getItem('theme');
    if(s)document.documentElement.setAttribute('data-theme',s);
    t.addEventListener('click',function(){{var c=document.documentElement.getAttribute('data-theme'),n=c==='light'?'dark':'light';document.documentElement.setAttribute('data-theme',n);localStorage.setItem('theme',n)}});
    var m=document.getElementById('mobileToggle'),nl=document.getElementById('navLinks');
    m.addEventListener('click',function(){{nl.classList.toggle('open')}});
  </script>
</body>
</html>"""


def category_index_html(cat_id, skills, categories):
    """Generate an index page listing all skills in a category."""
    cat_display, cat_icon = category_display(cat_id, categories)
    cat_desc = categories.get(cat_id, {}).get("description", "")
    title = f"{cat_display} - Crypto AI Agent Skills | CryptoSkill"
    desc_meta = f"Browse {len(skills)} {cat_display.lower()} crypto AI agent skills and MCP servers. {esc(cat_desc)}."

    # Build skill list
    rows = ""
    for s in sorted(skills, key=lambda x: x.get("displayName", x["name"])):
        sname = esc(s["name"])
        sdisplay = esc(s.get("displayName", s["name"]))
        sdesc = esc(s.get("description", ""))[:120]
        grade = s.get("score", {}).get("grade", "")
        gc = grade_color(grade) if grade else ""
        grade_span = f'<span class="skill-badge" style="background:rgba({_hex_to_rgb(gc)},0.12);color:{gc}">{esc(grade)}</span>' if grade else ""
        # Trust flag count from per-skill TRUST.auto.yaml — null when manifest absent.
        trust = load_trust_manifest(cat_id, s["name"])
        summary = _red_flag_summary(trust)
        if summary is None:
            flag_span = ""
        else:
            n_true, n_unknown = summary
            title = f"{n_true} true, {n_unknown} unknown of 11 capability flags"
            if n_true == 0 and n_unknown == 0:
                flag_span = f'<span class="skill-badge trust-flag-badge trust-flag-zero" title="{title}">0 known flags</span>'
            elif n_true == 0 and n_unknown > 0:
                flag_span = f'<span class="skill-badge trust-flag-badge trust-flag-mostly-unknown" title="{title}">0 known &middot; {n_unknown} unknown</span>'
            else:
                plural = "s" if n_true != 1 else ""
                flag_span = f'<span class="skill-badge trust-flag-badge trust-flag-some" title="{title}">{n_true} flag{plural}</span>'
        rows += f"""      <a href="{sname}.html" class="cat-skill-row">
        <span class="cat-skill-name">{sdisplay}</span>
        {grade_span}
        {flag_span}
        <span class="cat-skill-desc">{sdesc}</span>
      </a>\n"""

    ld_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"{cat_display} Crypto AI Skills",
        "description": desc_meta,
        "url": f"{SITE}/skills/{cat_id}/",
        "isPartOf": {"@type": "WebSite", "name": "CryptoSkill", "url": SITE},
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{desc_meta}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE}/skills/{esc(cat_id)}/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{desc_meta}">
  <meta property="og:url" content="{SITE}/skills/{esc(cat_id)}/">
  <meta property="og:site_name" content="CryptoSkill">
  <meta property="og:image" content="{SITE}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{desc_meta}">
  <meta name="twitter:site" content="@cryptaborgs">
  <meta name="twitter:image" content="{SITE}/og-image.png">
  <link rel="icon" href="../../favicon.ico" sizes="any">
  <link rel="icon" type="image/png" href="../../favicon.png" sizes="32x32">
  <link rel="apple-touch-icon" href="../../apple-touch-icon.png">
  <link rel="stylesheet" href="../../styles.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-3VP1G7H67L"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-3VP1G7H67L');</script>
  <script type="application/ld+json">{ld_json}</script>
</head>
<body>
  <nav class="navbar"><div class="container">
    <a href="../../" class="nav-logo"><img src="../../icon.png" width="28" height="28" alt="CryptoSkill" style="border-radius:6px"> CryptoSkill</a>
    <ul class="nav-links" id="navLinks">
      <li><a href="../../#official">Official</a></li>
      <li><a href="../../#skills">Skills</a></li>
      <li><a href="../../#categories">Categories</a></li>
      <li><a href="../../#how-it-works">How It Works</a></li>
      <li><a href="https://github.com/jiayaoqijia/cryptoskill" target="_blank" rel="noopener">GitHub</a></li>
    </ul>
    <div class="nav-right">
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">
        <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
        <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      </button>
      <button class="mobile-toggle" id="mobileToggle" aria-label="Toggle menu"><span></span><span></span><span></span></button>
    </div>
  </div></nav>

  <div class="legal-content" style="padding-top:100px">
    <nav class="breadcrumb">
      <a href="../../">Home</a> &rsaquo; <a href="../../#categories">Categories</a> &rsaquo; {esc(cat_display)}
    </nav>

    <h1>{cat_icon} {esc(cat_display)}</h1>
    <p class="skill-page-desc">{esc(cat_desc)} &mdash; {len(skills)} skills available.</p>

    <div class="cat-skill-list">
{rows}    </div>
  </div>

  <footer class="footer"><div class="container">
    <div class="footer-left"><span class="footer-brand">CryptoSkill</span><span class="footer-text">Built for the crypto community</span></div>
    <div class="footer-links">
      <a href="https://github.com/jiayaoqijia/cryptoskill" target="_blank" rel="noopener"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg> GitHub</a>
      <a href="../../#official">Official</a>
      <a href="../../#skills">Skills</a>
      <a href="../../#categories">Categories</a>
      <a href="../../terms.html">Terms</a>
      <a href="../../privacy.html">Privacy</a>
    </div>
  </div></footer>

  <script>
    var t=document.getElementById('themeToggle'),s=localStorage.getItem('theme');
    if(s)document.documentElement.setAttribute('data-theme',s);
    t.addEventListener('click',function(){{var c=document.documentElement.getAttribute('data-theme'),n=c==='light'?'dark':'light';document.documentElement.setAttribute('data-theme',n);localStorage.setItem('theme',n)}});
    var m=document.getElementById('mobileToggle'),nl=document.getElementById('navLinks');
    m.addEventListener('click',function(){{nl.classList.toggle('open')}});
  </script>
</body>
</html>"""


def _hex_to_rgb(hex_color):
    """Convert #rrggbb to 'r,g,b'."""
    h = hex_color.lstrip("#")
    return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"


def generate_sitemap(skill_pages, category_ids):
    """Generate sitemap.xml with all pages."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = []

    # Static pages
    urls.append(f'  <url><loc>{SITE}/</loc><changefreq>daily</changefreq><priority>1.0</priority><lastmod>{today}</lastmod></url>')
    urls.append(f'  <url><loc>{SITE}/terms.html</loc><changefreq>monthly</changefreq><priority>0.3</priority></url>')
    urls.append(f'  <url><loc>{SITE}/privacy.html</loc><changefreq>monthly</changefreq><priority>0.3</priority></url>')

    # Category index pages
    for cat_id in sorted(category_ids):
        urls.append(f'  <url><loc>{SITE}/skills/{cat_id}/</loc><changefreq>weekly</changefreq><priority>0.8</priority><lastmod>{today}</lastmod></url>')

    # Individual skill pages
    for cat, name in sorted(skill_pages):
        urls.append(f'  <url><loc>{SITE}/skills/{cat}/{name}.html</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>')

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""


# ── main ─────────────────────────────────────────────────────────────

def main():
    if not os.path.exists(SKILLS_JSON):
        print(f"ERROR: {SKILLS_JSON} not found", file=sys.stderr)
        sys.exit(1)

    with open(SKILLS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    skills = data.get("skills", [])
    categories = data.get("categories", {})

    if not skills:
        print("No skills found in skills.json")
        sys.exit(1)

    # Group skills by category
    by_cat = {}
    for s in skills:
        cat = s.get("category", "uncategorized")
        by_cat.setdefault(cat, []).append(s)

    # Ensure all categories from skills are in the dict (handle 'dex' etc.)
    for cat in by_cat:
        if cat not in categories:
            categories[cat] = {
                "name": cat.replace("-", " ").title(),
                "icon": "",
                "description": f"{cat.replace('-', ' ').title()} skills",
            }

    skill_pages = []
    total_skill_pages = 0
    total_cat_pages = 0

    # Generate skill pages
    for cat, cat_skills in by_cat.items():
        cat_dir = os.path.join(DOCS, "skills", cat)
        os.makedirs(cat_dir, exist_ok=True)

        for s in cat_skills:
            page_html = skill_page_html(s, categories)
            page_path = os.path.join(cat_dir, f"{s['name']}.html")
            with open(page_path, "w", encoding="utf-8") as f:
                f.write(page_html)
            skill_pages.append((cat, s["name"]))
            total_skill_pages += 1

        # Generate category index
        cat_html = category_index_html(cat, cat_skills, categories)
        idx_path = os.path.join(cat_dir, "index.html")
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(cat_html)
        total_cat_pages += 1

    # Generate sitemap
    sitemap = generate_sitemap(skill_pages, by_cat.keys())
    with open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    print(f"Generated {total_skill_pages} skill pages across {total_cat_pages} categories")
    print(f"Updated sitemap.xml with {len(skill_pages) + total_cat_pages + 3} URLs")


if __name__ == "__main__":
    main()
