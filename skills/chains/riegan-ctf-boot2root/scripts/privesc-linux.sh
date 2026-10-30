#!/usr/bin/env bash
# privesc-linux.sh - fast local privesc enumeration for Linux CTF boxes.
# Copy to the target (e.g. /tmp) and run with bash. Pure bash + coreutils,
# find, grep; colorless by design (output is usually piped/logs). ~seconds.
# Usage: bash privesc-linux.sh [--help]
# Order mirrors references/privesc-linux.md: sudo -l first (fastest win).
set -u

[ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ] && { sed -n '2,7p' "$0"; exit 0; }

hdr() { printf '\n===== %s =====\n' "$1"; }

hdr "identity/host"
id; hostname 2>/dev/null || uname -n; uname -a; cat /etc/issue 2>/dev/null

hdr "sudo -l (try password if asked)"
sudo -n -l 2>&1 || sudo -l 2>&1

hdr "capabilities"
if command -v getcap >/dev/null; then timeout 5 getcap -r / 2>/dev/null; else echo "getcap: not installed"; fi

hdr "cron"
command -v crontab >/dev/null 2>&1 && crontab -l 2>&1 || echo "crontab: not installed"
cat /etc/crontab 2>/dev/null
ls -la /etc/cron.d /etc/cron.daily /var/spool/cron 2>/dev/null

hdr "suid/sgid"
PRUNE='-not -path /proc/* -not -path /sys/* -not -path /dev/* -not -path /run/* -not -path /snap/* -not -path /usr/share/* -not -path /usr/lib* -not -path /var/lib/*'
# shellcheck disable=SC2086  (PRUNE is a word list by design)
timeout 5 find / -xdev -perm -4000 -type f $PRUNE 2>/dev/null
timeout 5 find / -xdev -perm -2000 -type f $PRUNE 2>/dev/null

hdr "writable /etc/passwd"
ls -la /etc/passwd /etc/shadow 2>/dev/null

hdr "writable dirs and PATH hijack candidates"
echo "PATH=$PATH"
# shellcheck disable=SC2086
timeout 5 find / -xdev -writable -type d -not -path '/proc/*' -not -path '/sys/*' -not -path '/dev/*' -not -path '/tmp/*' -not -path '/run/*' $PRUNE 2>/dev/null | head -30
# world-writable files outside homes that root might execute
timeout 5 find /etc /usr/local /opt -writable -type f 2>/dev/null | head -20

hdr "network (pivots, local services)"
ss -tulpn 2>/dev/null || netstat -tulpn 2>/dev/null

hdr "users"
cut -d: -f1,3 /etc/passwd | grep -v 'nobody\|:[0-9]\{4,\}' 2>/dev/null

hdr "credential hunting"
for f in ~/.bash_history /root/.bash_history /home/*/.bash_history; do
    [ -f "$f" ] && { echo "--- $f"; grep -aiE 'passw|ssh|sudo|su |mysql|ftp|curl.*-u|http' "$f" 2>/dev/null | head -20; }
done
timeout 5 grep -rnaiE 'passwo?rd|secret|api[_-]?key' /home/*/.ssh /var/www /opt /srv /etc 2>/dev/null | grep -vE '/proc|Binary' | head -30
ls -la /home/*/.ssh /root/.ssh /var/backups 2>/dev/null
env | grep -iE 'pass|key|token|secret'

hdr "history of note: kernel exploits are LAST resort (see references/privesc-linux.md)"
echo "kernel: $(uname -r)  distro: $(head -1 /etc/os-release 2>/dev/null)"
printf '\n===== done =====\n'
