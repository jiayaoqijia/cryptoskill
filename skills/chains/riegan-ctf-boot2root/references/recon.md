# Recon methodology (boot2root)

Authorized targets only. The router gate applies to every packet: scan only IPs
the user has green-lit for this event. Port-scanning infrastructure you don't
own (even "just to check") is out of scope — no exceptions.

Phasing matters: full TCP port discovery first, deep scans only on found ports.
Scanning 65535 ports with `-sC -sV` wastes the whole night.

## Phase 1 — full TCP port sweep

```bash
nmap -p- --min-rate 2000 -oA nmap/allports <target>
```

- `--min-rate 2000` forces ≥2000 pps; on a local event VPN this finishes in
  a few minutes. Drop to `--min-rate 500` only if results look lossy
  (retransmit-heavy, services you know are up showing closed).
- Output triple `nmap/allports.{nmap,gnmap,xml}` — the wrapper
  `scripts/recon.sh` does this for you.

## Phase 2 — service/version/script scan on open ports only

```bash
nmap -sV -sC -p 22,80,443,3306 -oA nmap/enumerate <target>
```

- `-sV` version probes, `-sC` default script set (safe). Add `-O` for OS
  fingerprint if phase 1 didn't settle it.
- Targeted extras: `--script vuln`, `--script smb-vuln* -p 139,445`,
  `--script ftp-anon -p 21`.

## Phase 3 — UDP top ports (slow, run async while working foothold)

```bash
nmap -sU --top-ports 50 -oA nmap/udp <target>      # needs root
```

UDP pays off on: SNMP (161), TFTP (69), SMB over UDP, mDNS, and forgotten
services. A full `-sU -p-` is almost never worth it on event VPNs.

## Default-credential / anonymous awareness per service

Try these the moment the port shows open — they are free wins on easy boxes.

| Service / port | Check | Command |
|---|---|---|
| FTP 21 | anonymous login | `ftp <target>` → user `anonymous`, any password; look for writable dirs (`put test.txt`) |
| SMB 139/445 | null session + share list | `smbclient -L //<target> -N`; then `smbclient //<target>/<share> -N` |
| SNMP 161 | community `public`/`private` | `snmpwalk -v2c -c public <target>` (pacman `net-snmp`) |
| RDP 3389 | cred reuse from other findings | `xfreerdp /u:<user> /p:<pw> /v:<target>` |
| MySQL 3306 | root:no-password | `mysql -h <target> -u root -p` (try empty) |
| MSSQL 1433 | sa:no-password | `impacket-mssqlclient <user>:<pw>@<target> -windows-auth` |
| MongoDB 27017 | unauthenticated | `mongosh mongodb://<target>:27017` |
| Redis 6379 | unauthenticated | `redis-cli -h <target>` then `INFO` |
| PostgreSQL 5432 | postgres:postgres | `psql -h <target> -U postgres` |
| Telnet 23 | default device creds | banner first, try root/admin variants |
| SSH 22 | never default-cred; check weak/key reuse | `ssh -i <key> <user>@<target>` |

Cred reuse: every password or hash found in one service gets replayed against
every other login surface (SSH, SMB, RDP, web logins, databases). Track attempts
in `notes.md`.

## Web service handoff

Any HTTP/HTTPS port (including odd ones like 8080, 8443, 5000) goes to the
`ctf-web` skill for directory brute forcing, source audit, and vuln classes.
Minimum boot2root pass before handing off:

```bash
curl -sI http://<target>/            # server header, framework hints
nmap --script http-title,http-enum -p80,443 <target>
```

## Vhosts and DNS

If the box runs a nameserver (53) or Apache/NGINX with name-based vhosts:

```bash
dig axfr @<target> <zone>                       # zone transfer attempt
dnsrecon -d <domain> -n <target>                # pacman dnsrecon, or scripts
gobuster vhost -u http://<target> -w toolbox/subdomains.txt
```

Add discovered hostnames to `/etc/hosts` (needs sudo — ask/document) pointing at
the target and rescan the web ports; different vhost often means different app.

## Notes discipline

Record in `notes.md`: every open port + version string verbatim, every anonymous
login that worked, every cred tried. Version strings are what phase-2 foothold
search (searchsploit) keys on.
