# Changelog

## v0.3.0

### Security

- **Input sanitization for all user-supplied arguments in `helio.sh`**
  - Added `validate_input` function that rejects values containing shell metacharacters, URL-unsafe characters, and path traversal sequences (`..`)
  - Allowlist: `a-zA-Z0-9._@:/-` — covers Helio IDs, currency symbols, wallet addresses, and decimal amounts
  - Validated arguments: `symbol` (currency-id, create-paylink), `amount` (create-paylink), `paylink_id` (charge, transactions, disable, enable)
  - Mitigates URL path traversal and terminal output injection when arguments are interpolated into curl URLs and echo statements
  - Addresses code scanner findings from v0.2.0 review

