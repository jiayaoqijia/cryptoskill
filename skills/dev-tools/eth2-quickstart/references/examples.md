# Example Requests

Use these examples when an agent or user needs a concrete starting prompt.

## Bootstrap A Fresh Host

```text
Use the eth2-quickstart skill to bootstrap this Ubuntu host for an Ethereum node. Choose a sensible default client stack, keep the flow non-interactive where possible, and stop before any destructive step that needs my confirmation.
```

## Recommend Server Size

```text
Use the eth2-quickstart skill to recommend an appropriate server for this node. Tell me the baseline disk, RAM, CPU, and OS requirements first, then explain whether my target host is good enough for production, RPC use, or only test usage.
```

## Resume After Reboot

```text
Use the eth2-quickstart skill to resume node installation after the Phase 1 reboot boundary. Prefer explicit client flags and verify health with doctor --json when done.
```

## Plan The Next Install Step

```text
Use the eth2-quickstart skill to inspect this host and tell me the next safe install action. Start with plan --json, explain whether Phase 1, Phase 2, or the Monad installer is needed, and do not apply anything until I confirm.
```

## Check Node Health

```text
Use the eth2-quickstart skill to inspect this node. Show me the doctor --json result, explain any failing checks, and use logs only if needed for RCA.
```

## Safe Cleanup

```text
Use the eth2-quickstart skill to show me what default node data cleanup would remove on this host. Start with a dry-run and do not remove secrets, wallets, or validator keys.
```

## Routine Operations

```text
Use the eth2-quickstart skill to stop this node cleanly, show me its current service status, and tell me what would be needed to start it again.
```
