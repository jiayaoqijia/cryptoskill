# Hermes Gateway Configuration — Troubleshooting

## Home Channel Configuration Error

### Symptom
Gateway crash-loops with:
```
TypeError: string indices must be integers, not 'str'
```

### Cause
The `home_channel` entries in `config.yaml` use a flat string format instead of the required dict format.

**Wrong (string format):**
```yaml
home_channel: telegram:-1003863540828
```

**Correct (dict format):**
```yaml
home_channel:
  platform: telegram
  chat_id: "-1003863540828"
```

### Locations to Check
1. `display.platforms.telegram.home_channel`
2. `gateway.platforms.<platform>.home_channel`
3. Top-level platform configs (e.g., `kapso.home_channel`)

### Fix
Replace all string-format `home_channel` entries with the dict format:

```yaml
home_channel:
  platform: telegram
  chat_id: "-YOUR_CHAT_ID"
```

### Environment Variable Format
If using `${TELEGRAM_HOME_CHANNEL}`, ensure the env var contains only the chat ID:
```
TELEGRAM_HOME_CHANNEL=-1003863540828
```

Then reference it as:
```yaml
home_channel:
  platform: telegram
  chat_id: ${TELEGRAM_HOME_CHANNEL}
```

### Verification
After fixing, validate the config:
```bash
python3 -c "import yaml; yaml.safe_load(open('/root/.hermes/profiles/gentech/config.yaml'))"
```

Then restart the gateway:
```bash
hermes gateway restart --profile gentech
```

### Related
- Gateway logs: `/root/.hermes/profiles/gentech/logs/gateway.log`
- Exit diagnostics: `/root/.hermes/profiles/gentech/logs/gateway-exit-diag.log`
