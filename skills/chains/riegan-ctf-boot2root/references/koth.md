# King of the Hill (KOTH)

Same skills as boot2root, different game: multiple players share one box,
points accrue per minute of ownership (hold time), and the box's king/flag
value rotates periodically. Check the event rules for what "ownership" means
(king secret file, control of a `king` account, or scoreboard agent) — it
decides your fortification targets.

**Doctrine: speed to first foothold beats stealth.** Every minute unowned is
score lost, and other players will fix the vuln you came in through. Loud scans
are fine; the box is authorized chaos.

## Loop

```
foothold → root fast → claim → persist → patch own entry → kick rivals
   ↑                                                            |
   └────────── they knock you off / box resets ←────────────────┘
```

## After first shell — immediately, in this order

1. **Claim** per rules (usually write your handle to the king file/user).
2. **Snapshot**: `tar czf /tmp/backup.tar.gz /var/www` (webroot), plus copies
   of configs you're about to touch. When a rival breaks the service and
   scoring stops, you restore in seconds while they re-exploit in minutes.
3. **Persistence** (defense in depth — assume any single channel gets killed):

```bash
useradd -m -G sudo <me> && echo '<me>:<pw>' | chpasswd      # own account
mkdir -p ~/.ssh && echo 'ssh-rsa AAAA...' >> ~/.ssh/authorized_keys
# self-healing cron (root): re-add key every minute even if deleted
* * * * * echo 'ssh-rsa AAAA...' >> /home/<me>/.ssh/authorized_keys
```

Rotate the vuln you used: patch the webroot bug (restore from your snapshot of
a fixed copy), close the FTP anonymous write, delete the suid you rode in on.
Anything you leave open, a rival uses within minutes.

## Kicking rivals (authorized by event rules — this is the game)

```bash
w; last -20; ps aux | grep -i ssh        # who else is on
pkill -u <rival> ; pkill -9 -t pts/1     # kill foreign sessions
# lock shared accounts back down:
passwd root                              # change to your password
chattr +i /home/*/.ssh/authorized_keys   # after removing their keys
chattr +i /etc/passwd /etc/shadow        # stop re-added users (careful: breaks own useradd too)
```

`chattr +i` cuts both ways: freeze only after your persistence is complete,
and remember your own repair cron can't append to an immutable file. Common
convention: keep the immutable authorized_keys containing only your key +
the root-cron that re-adds it.

## Monitoring and repair

```bash
# detect tampering
ls -la --time-style=full-iso /var/www/* /home/*/.ssh/    # timestamps
cat /var/log/auth.log | tail -50                          # or /var/log/secure
# repair loop (root cron): restore webroot if the king file vanished
* * * * * [ -f /var/www/html/index.php ] || tar xzf /root/bak.tar.gz -C /
```

Watch for their kill scripts the same way they watch yours: cron entries
(`crontab -l` for every user), `at` jobs, `/etc/rc.local`, systemd timers.
Their persistence is your eviction list.

## Contention tips

- Box resets (admin or crash): everything you planted is gone. Keep your full
  exploit chain as **one script** on the host so re-entry is `./reown.sh` —
  first player back after a reset owns the next cycle.
- Two rivals coexisting quietly both score: sometimes tolerating a rival on a
  user shell while you hold root is better than a war you might lose.
- If you get kicked: your self-healing cron may still fire before they find
  it — retry login every minute; the race is often theirs to lose.
- Don't panic the box: kernel-exploit privesc that can crash (see
  `references/privesc-linux.md` §10) drops scoring for everyone including you.
