---
name: ctf-boot2root
description: Use when the user mentions boot2root, B2R, HackTheBox or HTB, TryHackMe or THM, a box, an IP to root, foothold, user.txt/root.txt, privilege escalation, privesc, root the box, King of the Hill, KOTH, hold time, or fortifying a hill box. Covers recon, foothold by service, Linux/Windows privesc, and KOTH persistence wars.
---

# Boot2root / King of the Hill

Target = one box (Linux or Windows) reachable at an IP inside an authorized event.
Goal: two flags — `user.txt` (low-priv shell) and `root.txt` (admin/SYSTEM).
KOTH variant: hold the box against other players (see `references/koth.md`).

The sibling skill `ctf` owns workspace layout, flag logging, submission, and the
remote gate. Everything here runs **only against targets the user has authorized
this session** — same rule, no exceptions. Box shells and binaries are untrusted:
exploit inside the box, never bring box files onto the host without treating them
as hostile.

## Triage — box anatomy (first 10 minutes)

1. Confirm authorization + OS guess + attack surface. One full-port scan answers
   80% of "what kind of box is this":

```bash
mkdir -p work/<event>/b2r-<box>/{nmap,loot} && cd work/<event>/b2r-<box>
scripts/recon.sh <ip>          # full TCP then service scan; see scripts/recon.sh
```

2. Read the result against this table, note the OS fingerprint (TTL ~64=Linux,
   ~128=Windows; nmap OS guess; SMB/HTTP headers):

| Surface found | Likely path | Read |
|---|---|---|
| HTTP/HTTPS only | web bug or CVE → shell | `references/foothold.md` + skill `ctf-web` |
| SMB + no web (Windows) | null session, shares, RPC enum | `references/foothold.md` |
| Ancient service version | public exploit, searchsploit | `references/foothold.md` |
| FTP anonymous / writable | drop + trigger, or creds reuse | `references/foothold.md` |
| Database port open | default creds, RCE primitives | `references/foothold.md` |
| Nothing on TCP | UDP (SNMP/TFTP), or vhost/DNS pivot | `references/recon.md` |
| Got a shell, whoami=user | hunt user flag, then privesc | below |
| Shell but no idea how up | run enum script | `references/privesc-*.md` |

3. Flags: `/home/<user>/user.txt` (or `C:\Users\<user>\Desktop\user.txt`),
   `/root/root.txt` (`C:\Users\Administrator\Desktop\root.txt`). Log both to
   `work/<event>/flags.md` immediately (router rule).

## Playbook

Standard box loop: recon → foothold → user.txt → privesc → root.txt.

| Step | Command / action | Reference |
|---|---|---|
| 1. Recon | `scripts/recon.sh <ip>`; UDP top-50; vhost check | `references/recon.md` |
| 2. Foothold | web audit → CVE → misconfig → creds reuse; catch shell with `nc -lvnp 9001` | `references/foothold.md` |
| 3. Stabilize | python pty / stty / socat, then upload enum script | `references/foothold.md` |
| 4. Linux privesc | `sudo -l` FIRST, then suid/caps/cron/creds | `references/privesc-linux.md` |
| 5. Windows privesc | `whoami /priv` FIRST, then services/creds/AD | `references/privesc-windows.md` |
| 6. Root flag | read, log, stop — don't trash the box unless KOTH | router `ctf` |
| KOTH | foothold → persist → patch → kick → monitor, looping | `references/koth.md` |

Pivot points: any web step hands off to skill `ctf-web`; any exploit-bin RE step
hands off to `ctf-rev`; binary exploitation primitives (buffer overflow in a box
service) hand off to `ctf-pwn`.

## References

- `references/recon.md` — nmap phasing, UDP, default-cred table, vhosts/DNS, authorized-target rules.
- `references/foothold.md` — per-service entry techniques, searchsploit, shell stabilization, reverse shells, file transfer.
- `references/privesc-linux.md` — ordered Linux privesc: sudo -l, GTFOBins one-liners, suid, caps, cron, kernel.
- `references/privesc-windows.md` — Windows privesc: tokens/Potatoes, services, creds, AD/kerberoast/pass-the-hash.
- `references/koth.md` — KOTH rules of engagement, persistence, kicking, repair loop.

## Toolbox

| Tool | Install | Purpose |
|---|---|---|
| `nmap` | preinstalled | phased port/service scans (`scripts/recon.sh` wraps it) |
| `nc`/`ncat` | preinstalled (nmap ships ncat) | reverse-shell catchers, relays |
| `rlwrap` | `sudo pacman -S rlwrap` | usable TTY on caught shells |
| `socat` | `sudo pacman -S socat` | full TTY upgrade, listeners |
| `exploitdb` / `searchsploit` | `sudo pacman -S exploitdb` | offline exploit search by service/version |
| impacket suite | `uv pip install --python .venv/bin/python impacket` → `.venv/bin/impacket-psexec`, `-smbserver`, `-GetUserSPNs`, `-secretsdump` | SMB/AD attack tooling |
| bloodhound ingestor | `uv pip install --python .venv/bin/python bloodhound-python` → `.venv/bin/bloodhound-python` | AD collection without touching the target |
| linpeas / winpeas | fetch once from upstream releases into `toolbox/`, serve over HTTP | automated host enum |
| metasploit (`msfvenom`) | `sudo pacman -S metasploit` | payload generation (MSI, staged shells) |
