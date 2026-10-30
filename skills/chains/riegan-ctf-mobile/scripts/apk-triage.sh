#!/usr/bin/env bash
# apk-triage.sh — static first-look triage for an Android APK (CTF).
#
# Pure static analysis: never executes the challenge app. Produces:
#   <outdir>/file-list.txt        every zip entry name
#   <outdir>/extracted/           the unzipped APK tree (untrusted — grep only)
#   <outdir>/secrets.txt          hardcoded-key/secret pattern hits
#   <outdir>/urls.txt             unique http(s) endpoints
#   <outdir>/manifest-summary.txt apktool manifest quick-look (if apktool present)
#   <outdir>/apktool/             apktool decode (resources+manifest, no smali)
#   <outdir>/report.txt           everything below, tee'd
#
# Usage:
#   apk-triage.sh <file.apk> [outdir]        default outdir: ./apk-out
#   apk-triage.sh --help
#
# Requirements: unzip, file, grep, awk, sort (base system).
# Optional: apktool (sudo pacman -S apktool) — without it the manifest pass is
# skipped with a hint instead of failing.
set -euo pipefail

usage() {
    cat <<'EOF'
apk-triage.sh — static first-look triage for an Android APK (CTF).
Usage: apk-triage.sh <file.apk> [outdir]      (default outdir: ./apk-out)
Needs: unzip, file, grep, awk. Optional: apktool (sudo pacman -S apktool)
       enables the AndroidManifest/resources quick-look pass.
Static analysis only — never runs the app. See header comment for outputs.
EOF
    exit "${1:-0}"
}

case "${1:-}" in
    -h|--help) usage 0 ;;
esac

if [ $# -lt 1 ] || [ ! -f "$1" ]; then
    echo "error: give an existing .apk file as first argument (try --help)" >&2
    exit 1
fi

APK=$1
OUT=${2:-apk-out}
mkdir -p "$OUT"    # before the pipeline: tee opens report.txt up-front

# --- everything runs inside one block so the whole report is tee'd -------------
{
    echo "== apk-triage: $APK =="
    file "$APK"
    sha256sum "$APK"

    if ! unzip -l "$APK" >/dev/null 2>&1; then
        echo "FATAL: not a zip/apk (unzip -l failed) — check 'file' output above" >&2
        exit 1
    fi

    unzip -Z1 "$APK" >"$OUT/file-list.txt"

    echo "== inventory =="
    echo "dex files:    $(grep -cE '^classes[0-9]*\.dex$' "$OUT/file-list.txt" || true)"
    echo "ABIs:         $(grep -oE '^lib/[^/]+/' "$OUT/file-list.txt" | sort -u | tr '\n' ' ')"
    echo "native libs:  $(grep -cE '^lib/[^/]+/.*\.so$' "$OUT/file-list.txt" || true)"
    echo "assets files: $(grep -cE '^assets/' "$OUT/file-list.txt" || true)"
    echo "res/raw files:$(grep -cE '^res/raw/' "$OUT/file-list.txt" || true)"
    echo "-- framework fingerprints --"
    grep -E 'libapp\.so|libflutter\.so|index\.android\.bundle|libil2cpp\.so|Assembly-CSharp\.dll|\.pck$|www/index\.html' \
        "$OUT/file-list.txt" || echo "  (none of: flutter/RN/unity-mono/il2cpp/godot/cordova)"
    echo "-- notable assets --"
    grep -E '^assets/' "$OUT/file-list.txt" | grep -viE '\.(png|jpg|webp|gif|ttf|otf|mp3|ogg)$' | head -20 || true

    # --- extract (hostile tree: grep/read only, never execute) ------------------
    rm -rf "$OUT/extracted"
    mkdir -p "$OUT/extracted"
    unzip -oq "$APK" -d "$OUT/extracted"

    # --- secret sweep ------------------------------------------------------------
    echo
    echo "== secret sweep (patterns: see android-recon.md §5) =="
    {
        grep -rnaE \
            -e 'AKIA[0-9A-Z]{16}' \
            -e 'AIza[0-9A-Za-z_-]{35}' \
            -e 'ghp_[0-9A-Za-z]{36}' \
            -e 'xox[baprs]-[0-9A-Za-z-]{10,}' \
            -e 'sk_live_[0-9a-zA-Z]{20,}' \
            -e '-----BEGIN [A-Z ]*PRIVATE KEY-----' \
            -e 'eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.' \
            -e 'firebaseio\.com|firebaseapp\.com|\.appspot\.com' \
            -e '[a-zA-Z0-9_]{2,16}\{[^}]{4,}\}' \
            "$OUT/extracted"
        grep -rinaE \
            -e "(api[_-]?key|apikey|secret|token|passw(or)?d)[\"' ]*[:=][^ ]{3,}" \
            -e 'password="[^"]+"' \
            "$OUT/extracted" \
            | grep -vE '\.(png|jpg|webp|gif|arsc)$'
    } >"$OUT/secrets.txt" || true
    echo "hits: $(grep -c . "$OUT/secrets.txt" || true) (full list: $OUT/secrets.txt)"
    head -25 "$OUT/secrets.txt" || true

    # --- endpoints ---------------------------------------------------------------
    grep -rohaE 'https?://[A-Za-z0-9._~:/?#@!$&*+,;=%-]+' "$OUT/extracted" \
        | sort -u >"$OUT/urls.txt" || true
    echo
    echo "== endpoints: $(grep -c . "$OUT/urls.txt" || true) unique (urls.txt) =="
    head -15 "$OUT/urls.txt" || true

    # --- firebase config ---------------------------------------------------------
    echo
    echo "== firebase config =="
    found_fb=0
    while IFS= read -r gs; do
        found_fb=1
        echo "-- $gs"
        grep -E -A1 '"(api_key|current_api_key|database_url|project_id|storage_bucket)"' "$gs" \
            | grep -E '(:|")' | head -12 || true
    done < <(find "$OUT/extracted" -name 'google-services.json' -type f)
    [ "$found_fb" = 0 ] && echo "  no google-services.json found"

    # --- manifest quick-look (optional apktool) -----------------------------------
    echo
    echo "== manifest quick-look =="
    if command -v apktool >/dev/null 2>&1; then
        if apktool d -s -f "$APK" -o "$OUT/apktool" >/dev/null 2>&1; then
            M="$OUT/apktool/AndroidManifest.xml"
            {
                echo "package: $(grep -m1 -oE 'package="[^"]*"' "$M")"
                echo "flags:   $(grep -oE 'android:(debuggable|allowBackup|usesCleartextTraffic)="[^"]*"' "$M" | tr '\n' ' ')"
                echo "nsc:     $(grep -oE 'android:networkSecurityConfig="[^"]*"' "$M" || echo '(none)')"
                echo
                echo "-- exported components (explicit) --"
                grep -B2 -nE 'android:exported="true"' "$M" || echo "  none explicit"
                echo "-- deep-link schemes --"
                grep -oE 'android:scheme="[^"]*"' "$M" || echo "  none"
                echo "-- provider authorities --"
                grep -oE 'android:authorities="[^"]*"' "$M" || echo "  none"
                echo "-- permissions --"
                grep -oE '<uses-permission [^>]+>' "$M" | head -25 || true
                echo
                echo "NOTE: pre-Android-12 targeting: intent-filter without exported=\"false\""
                echo "      still means exported. Read the full file for intent filters."
            } >"$OUT/manifest-summary.txt" || true
            cat "$OUT/manifest-summary.txt"
            echo
            echo "full decode (smali included): apktool d \"$APK\" -o <dir>"
        else
            echo "apktool decode FAILED (malformed/res-fused apk?) — try: apktool d \"$APK\""
        fi
    else
        echo "apktool not installed — skipping manifest pass."
        echo "install with: sudo pacman -S apktool"
        echo "binary-only fallback: the zip's AndroidManifest.xml is binary XML (not readable)"
    fi

    echo
    echo "== next steps =="
    echo "jadx:      ~/tools/jadx/bin/jadx -d jadx-out \"$APK\"   (see android-recon.md §4)"
    echo "manifest:  $OUT/manifest-summary.txt (if apktool ran)"
    echo "secrets:   $OUT/secrets.txt   endpoints: $OUT/urls.txt"
    echo "bug-class: references/android-vulns.md — components, WebView, providers..."
} | tee "$OUT/report.txt"
