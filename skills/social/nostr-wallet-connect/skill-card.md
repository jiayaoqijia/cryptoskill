## Description: <br>
Financial capability for AI entities - pay Lightning invoices, check balance, and create invoices via Nostr Wallet Connect (NIP-47). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vveerrgg](https://clawhub.ai/user/vveerrgg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external agent builders use this skill to give an agent scoped Lightning Network wallet actions through Nostr Wallet Connect, including balance checks, invoice creation, payment lookup, transaction listing, and invoice payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables Lightning wallet payment actions and the security summary says it lacks strong approval or spending boundaries for real-money transactions. <br>
Mitigation: Use a dedicated low-balance wallet or restricted NWC connection, require manual approval for every payment, and verify invoice amount and description out of band. <br>
Risk: The NWC connection string authorizes wallet requests and exposure could permit unauthorized payments. <br>
Mitigation: Store the connection string only in environment variables or a secrets manager, avoid logging it, and rotate it if exposure is suspected. <br>
Risk: Payment behavior depends on external NWC-compatible wallets and Nostr relays. <br>
Mitigation: Check balance before payment, set an appropriate timeout, and confirm payment state with invoice lookup or transaction history. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/HumanjavaEnterprises/nwc.app.OC-python.src) <br>
- [PyPI package](https://pypi.org/project/nostrwalletconnect/) <br>
- [ClawHub release page](https://clawhub.ai/vveerrgg/nostrwalletconnect) <br>
- [NostrKey skill](https://clawhub.ai/vveerrgg/nostrkey) <br>
- [NSE Orchestrator](https://clawhub.ai/vveerrgg/nse) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes async NWCClient usage examples and environment variable setup guidance.] <br>

## Skill Version(s): <br>
0.1.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
