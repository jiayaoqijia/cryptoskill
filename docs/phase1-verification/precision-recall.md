# Phase 1 precision / recall (auto-generated)

Critical-subset gating per TRUST.md §"Pass bar — recall floors".
Recall is reported as the one-sided Wilson 95% lower confidence bound.

| capability | TP | FP | FN | precision | recall_lcb | floor | min_N | gate |
|---|---|---|---|---|---|---|---|---|
| can_move_funds | 0 | 0 | 0 | nan | nan | 0.90 | 50 | UNDER-VALIDATED (positives 0/50, recall_lcb nan/0.90) |
| requires_private_key | 0 | 0 | 0 | nan | nan | 0.90 | 50 | UNDER-VALIDATED (positives 0/50, recall_lcb nan/0.90) |
| can_install_code | 0 | 0 | 0 | nan | nan | 0.85 | 50 | UNDER-VALIDATED (positives 0/50, recall_lcb nan/0.85) |
| uses_remote_install_script | 0 | 0 | 0 | nan | nan | 0.85 | 30 | UNDER-VALIDATED (positives 0/30, recall_lcb nan/0.85) |
| requires_hosted_operator | 0 | 0 | 0 | nan | nan | 0.80 | 50 | UNDER-VALIDATED (positives 0/50, recall_lcb nan/0.80) |

Non-critical capabilities (recall reported, not gated):

| capability | TP | FP | FN | precision |
|---|---|---|---|---|
| auto_invocable | 0 | 0 | 0 | nan |
| can_execute_shell | 0 | 0 | 0 | nan |
| can_write_files | 0 | 0 | 0 | nan |
| can_browse_web | 0 | 0 | 0 | nan |
| can_spawn_subagents | 0 | 0 | 0 | nan |
| mutable_remote_runtime | 0 | 0 | 0 | nan |
