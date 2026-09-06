# Error Recovery & Troubleshooting

## Contents

- [On Failure](#on-failure)
- [Error Codes](#error-codes)
- [Common Failures & Solutions](#common-failures--solutions)

## On Failure

1. Run `mm describe-screen`
2. Check the current screen:
   - `unlock` → enter password and submit
   - `home` → continue, but check for modals or blockers
   - `onboarding-*` → complete onboarding
   - `unknown` → take a screenshot and investigate
3. Query prior runs:
   ```bash
   mm knowledge-search "send"
   mm knowledge-sessions
   mm knowledge-last
   ```
4. Capture `mm screenshot --name "debug"` for diagnosis

## Error Codes

| Code                         | Meaning                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------ |
| `MM_SESSION_ALREADY_RUNNING` | Session exists — `mm cleanup` first                                            |
| `MM_NO_ACTIVE_SESSION`       | No session — `mm launch` first                                                 |
| `MM_LAUNCH_FAILED`           | Browser launch failed                                                          |
| `MM_INVALID_INPUT`           | Invalid parameters                                                             |
| `MM_TARGET_NOT_FOUND`        | Element not visible                                                            |
| `MM_TAB_NOT_FOUND`           | Tab not found                                                                  |
| `MM_CLICK_FAILED`            | Click failed (post-find)                                                       |
| `MM_CLICK_TIMEOUT`           | Click hung — may have completed; run `mm describe-screen`                      |
| `MM_TYPE_FAILED`             | Type failed (post-find)                                                        |
| `MM_TYPE_TIMEOUT`            | `fill()` timed out — `mm describe-screen` and retry                            |
| `MM_GETTEXT_FAILED`          | `get-text` failed (element detached) — re-target                               |
| `MM_GETTEXT_TIMEOUT`         | `textContent()` timed out                                                      |
| `MM_WAIT_TIMEOUT`            | Wait timeout exceeded                                                          |
| `MM_PAGE_CLOSED`             | Page closed during interaction — normal after some confirmations                |
| `MM_SCREENSHOT_FAILED`       | Screenshot capture failed                                                      |
| `MM_BATCH_TIMEOUT`           | `batchTimeoutMs` deadline exceeded                                             |
| `MM_CONTEXT_SWITCH_BLOCKED`  | Cannot switch context during active session                                    |
| `MM_SET_CONTEXT_FAILED`      | Context switch failed                                                          |
| `MM_CDP_BLOCKED`             | CDP method is in the destructive-blocklist                                     |
| `MM_CDP_FAILED`              | CDP command execution failed or timed out                                      |

## Common Failures & Solutions

| Symptom                                     | Likely Cause                 | Solution                                                      |
| ------------------------------------------- | ---------------------------- | ------------------------------------------------------------- |
| `MM_SESSION_ALREADY_RUNNING`                | Previous session not cleaned | `mm cleanup`                                                  |
| `MM_NO_ACTIVE_SESSION`                      | No browser running           | `mm launch`                                                   |
| Extension not loading                       | Extension not built          | `yarn build:test:webpack` then `mm launch`                    |
| `EADDRINUSE` port error                     | Orphan processes             | Check `.mm-server` for ports, kill orphaned process           |
| `MM_TARGET_NOT_FOUND`                       | Element not visible          | `mm describe-screen` to check state                           |
| `MM_WAIT_TIMEOUT`                           | Slow environment             | Increase `--timeout`, inspect screenshot                      |
| `MM_CLICK_TIMEOUT` / `MM_TYPE_TIMEOUT`      | Action hung                  | `mm describe-screen` to verify; retry with larger `--timeout` |
| `MM_GETTEXT_TIMEOUT` / `MM_GETTEXT_FAILED`  | Element detached             | `mm describe-screen` and re-target                            |
| `MM_PAGE_CLOSED`                            | Confirmation auto-closed     | Expected — `mm describe-screen` to find active page           |
| `MM_CDP_BLOCKED`                            | Destructive CDP method       | Use a non-blocked method                                      |
| `MM_CDP_FAILED`                             | Invalid CDP params           | Check method & params; retry with `--timeout` (max 30000)     |
| `MM_CONTEXT_SWITCH_BLOCKED`                 | Active session               | `mm cleanup` before `mm set-context`                          |
| Fixtures not available                      | Running in prod context      | `mm set-context e2e`                                          |
| Stale a11yRefs after navigate               | Refs not refreshed           | `mm describe-screen` for fresh refs                           |
