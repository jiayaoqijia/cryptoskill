#!/usr/bin/env bash
# dirquick.sh — one-shot web recon sweep for a challenge base URL.
#
# Steps (all output lands in the -o dir, default recon/):
#   1. header dump of /                        -> recon/headers.txt
#   2. quick exposed-file probes               -> recon/exposed.txt (bodies of hits saved)
#      robots.txt sitemap.xml .git/HEAD .git/config .env .env.bak server-status
#      adminer.php phpmyadmin/ package.json composer.json backup.zip www.zip
#      source.zip site.zip index.php.bak index.php~ .index.php.swp dump.sql
#   3. ffuf content discovery                  -> recon/ffuf.json (+ live output)
#      wordlist: -w, else /usr/share/seclists common.txt, else bundled fallback list
#   4. optional -v vhost mode: fuzz Host: FUZZ.<domain> with the seclists DNS list
#      (skipped with a notice when the list is absent)   -> recon/vhosts.json
#
# Requires curl. ffuf: AUR (paru -S ffuf / ffuf-bin) or upstream binary from
# https://github.com/ffuf/ffuf/releases. When ffuf is missing, steps 1-2 still run,
# then the script prints an install hint and exits 1.
#
# Usage:
#   dirquick.sh [options] BASE_URL
#     -w WORDLIST   content wordlist (default: seclists common.txt or bundled)
#     -e EXTS       comma list of extensions for ffuf (e.g. .php,.html,.bak)
#     -d N          recursion depth N (default off)
#     -v            also fuzz vhosts (Host: FUZZ.<domain of BASE_URL>)
#     -t N          ffuf threads (default 40)
#     -o DIR        output dir (default recon)
#     -h            this help
#
# Examples:
#   dirquick.sh http://target:8080
#   dirquick.sh -e .php,.bak -d 2 -v http://target
set -euo pipefail

usage() { sed -n '2,/^set -euo/p' "$0" | sed '$d' | sed 's/^#\{1,\} \{0,1\}//'; }
die() { echo "dirquick.sh: $*" >&2; exit 1; }

WORDLIST="" EXTS="" DEPTH=0 VHOST=0 THREADS=40 OUT="recon"
[[ "${1:-}" == "--help" ]] && { usage; exit 0; }
while getopts "w:e:d:vt:o:h" opt; do
  case "$opt" in
    w) WORDLIST="$OPTARG" ;;
    e) EXTS="$OPTARG" ;;
    d) DEPTH="$OPTARG" ;;
    v) VHOST=1 ;;
    t) THREADS="$OPTARG" ;;
    o) OUT="$OPTARG" ;;
    h) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
done
shift $((OPTIND - 1))
[[ $# -eq 1 ]] || { usage >&2; die "exactly one BASE_URL required"; }
BASE="${1%/}"
[[ "$BASE" =~ ^https?:// ]] || die "BASE_URL must start with http:// or https://"

command -v curl >/dev/null || die "curl not found (sudo pacman -S curl)"
mkdir -p "$OUT"

# --- 1. headers -------------------------------------------------------------
curl -sS -m 15 -D "$OUT/headers.txt" -o /dev/null "$BASE" || true
echo "[*] headers of $BASE -> $OUT/headers.txt"

# --- 2. quick probes --------------------------------------------------------
PROBES=(robots.txt sitemap.xml .git/HEAD .git/config .env .env.bak .env.local
        server-status adminer.php phpmyadmin/ package.json composer.json
        backup.zip www.zip source.zip site.zip index.php.bak index.php~ .index.php.swp
        dump.sql database.sql)
: > "$OUT/exposed.txt"
for p in "${PROBES[@]}"; do
  code_size=$(curl -sS -m 8 -o /dev/null -w '%{http_code} %{size_download}' "$BASE/$p" 2>/dev/null) || code_size="000 0"
  read -r code size <<<"$code_size"
  if [[ "$code" != "404" && "$code" != "000" ]]; then
    echo "$code $size $BASE/$p" | tee -a "$OUT/exposed.txt"
    safe=$(printf '%s' "$p" | tr '/~' '__')
    curl -sS -m 8 -o "$OUT/probe_${code}_${safe}" "$BASE/$p" 2>/dev/null || true
  fi
done
[[ -s "$OUT/exposed.txt" ]] || echo "no quick-probe hits" | tee -a "$OUT/exposed.txt"

# --- ffuf (required for fuzzing) --------------------------------------------
if ! command -v ffuf >/dev/null; then
  echo "" >&2
  echo "dirquick.sh: ffuf not found — skipping content/vhost fuzzing." >&2
  echo "  install: paru -S ffuf      (AUR; or ffuf-bin)" >&2
  echo "  upstream: https://github.com/ffuf/ffuf/releases (binary on PATH)" >&2
  exit 1
fi

SECLISTS_DIR="/usr/share/seclists"
if [[ -z "$WORDLIST" ]]; then
  if [[ -f "$SECLISTS_DIR/Discovery/Web-Content/common.txt" ]]; then
    WORDLIST="$SECLISTS_DIR/Discovery/Web-Content/common.txt"
  else
    # bundled fallback: common CTF paths (~90 entries)
    WORDLIST="$OUT/bundled-wordlist.txt"
    cat > "$WORDLIST" <<'EOF'
admin
administrator
api
api/v1
assets
auth
backup
backups
bin
cache
cgi-bin
composer.json
composer.lock
config
console
css
dashboard
data
db
debug
dev
dist
docs
download
downloads
env
etc
files
flag
flags
graphql
health
home
html
images
img
inc
include
includes
index.php.bak
index.php~
js
lib
locale
login
media
node_modules
old
panel
private
public
qa
reports
secret
server
server-status
setup
src
static
status
swagger
swagger-ui
temp
test
tests
tmp
tools
upload
uploads
user
users
vendor
version
web.config
wp-admin
wp-content
wp-includes
xmlrpc.php
.backup
.env.bak
.git/HEAD
EOF
    echo "[*] seclists not installed -> using bundled wordlist ($WORDLIST)"
  fi
fi
echo "[*] content fuzz: $BASE/FUZZ  wordlist=$WORDLIST"

ffuf_args=(-u "$BASE/FUZZ" -w "$WORDLIST" -ac -t "$THREADS" -of json -o "$OUT/ffuf.json")
[[ -n "$EXTS" ]] && ffuf_args+=(-e "$EXTS")
[[ "$DEPTH" -gt 0 ]] && ffuf_args+=(-recursion -recursion-depth "$DEPTH")
ffuf "${ffuf_args[@]}"

# --- 4. vhost mode ----------------------------------------------------------
if [[ "$VHOST" -eq 1 ]]; then
  DNS_LIST="$SECLISTS_DIR/Discovery/DNS/subdomains-top1million-5000.txt"
  if [[ -f "$DNS_LIST" ]]; then
    domain=$(printf '%s' "$BASE" | sed -E 's#^[a-z]+://([^/:]+).*#\1#')
    baseline=$(curl -sS -m 10 -H "Host: zz-random-junk.$domain" "$BASE" 2>/dev/null | wc -c) || baseline=0
    echo "[*] vhost fuzz: Host: FUZZ.$domain (baseline size $baseline)"
    ffuf -u "$BASE" -w "$DNS_LIST" -H "Host: FUZZ.$domain" -fs "$baseline" \
         -t "$THREADS" -of json -o "$OUT/vhosts.json"
  else
    echo "[!] vhost fuzz skipped: $DNS_LIST missing (paru -S seclists)" >&2
  fi
fi

echo "[*] done. artifacts in $OUT/: $(ls "$OUT" | tr '\n' ' ')"
