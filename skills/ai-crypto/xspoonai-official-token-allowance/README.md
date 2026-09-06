# Token Allowance Manager Skill

The **Token Allowance Manager** skill provides SpoonOS agents with granular control over ERC20 token permissions. This is essential for secure DeFi operations, allowing agents to "unlock" tokens for swapping/lending only when needed and "lock" them afterwards.

## Features

- **Check Allowance**: Query how much a spender contract is allowed to move.
- **Approve**: Grant permission for a specific amount.
- **Revoke**: Reset allowance to 0 (security best practice).
- **Infinite Approval**: Option to grant max uint256 approval (use with caution).

## Usage

### Parameters

- `action` (string, required): One of `check`, `approve`, `revoke`.
- `token_address` (string, required): Address of the ERC20 token contract.
- `spender_address` (string, required): Address of the contract to approve/check (e.g., Uniswap Router).
- `amount` (float, optional): Amount to approve (required for `approve` unless `infinite` is True).
- `infinite` (boolean, optional): If True, approves `2**256 - 1` (default: False).
- `rpc_url` (string, optional): RPC endpoint (defaults to env `WEB3_RPC_URL`).
- `private_key` (string, optional): Signer key (defaults to env `PRIVATE_KEY`).

### Example Agent Prompts

> "Check how much USDT the Uniswap Router can spend from my wallet."
> "Approve 500 DAI for the Aave Lending Pool."
> "Revoke the allowance for the old SushiSwap contract."

### Output

Returns a JSON object with:
- `action`: The performed action.
- `token`: Token address.
- `spender`: Spender address.
- `allowance`: Current allowance (for 'check').
- `transaction_hash`: Hash of the approval/revoke tx (if applicable).

## Setup

Requires `web3` python library.
```bash
pip install web3
```
