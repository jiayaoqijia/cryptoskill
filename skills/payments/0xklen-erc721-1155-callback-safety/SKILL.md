---
name: erc721-1155-callback-safety
description: Use when a contract mints, transfers or escrows ERC-721/1155 tokens, or implements a receiver hook. Prevents reentrancy via onERC721Received/onERC1155Received and approval-scope bugs.
---

# ERC-721/1155 callback and approval safety

`safeTransferFrom` calls the recipient, and that callback is an external call into attacker code — mint and transfer logic must be reentrancy-safe and approval semantics checked.

## Procedure

1. Locate every safe transfer and callback: `grep -nE 'safeTransferFrom|safeBatchTransferFrom|onERC721Received|onERC1155Received|isApprovedForAll|setApprovalForAll' -r src/`.
2. For any contract implementing a receiver, confirm it returns the exact selector or the transfer reverts:

```solidity
function onERC721Received(address, address, uint256, bytes calldata) external pure returns (bytes4) {
    return IERC721Receiver.onERC721Received.selector; // 0x150b7a02
}
```

3. Apply checks-effects-interactions around every `_safeMint`/`_safeTransfer`: record the token as owned BEFORE the callback, so a re-entrant `receive` cannot mint twice from the same allowance.
4. Check the mint path: `_safeMint` calls the recipient, so a public mint must increment supply and set the owner before calling it.
5. In ERC-1155, batch callbacks (`onERC1155BatchReceived`) are separate and must also be handled.
6. Verify approval scope: `setApprovalForAll(operator, true)` grants ALL tokens forever; a marketplace approval should be per-token or time-limited.
7. Check `_isApprovedOrOwner` usage on burn/transfer so an approved operator cannot drain beyond the tokens it was granted.
8. Test reentrancy with an attacker contract that re-enters `mint` from its `onERC721Received`.
9. Confirm `supportsInterface(0x80ac58cd)` (721) / `0xd9b67a26` (1155) is implemented if the contract is a token.
10. Run `forge test --match-test testERC721Reentry -vvvv` and inspect the trace for a second entry.

## Pitfalls

- `_safeMint` before updating a per-user mint counter, letting the callback re-enter and mint an extra token.
- Returning the wrong selector (e.g. `bytes4(keccak256("onERC721Received()"))`) so real wallets reject safe transfers.
- ERC-1155 `safeTransferFrom` calls the receiver even when `to` is the sender, re-entering unexpectedly.
- Forgetting that `setApprovalForAll` cannot be scoped: one compromised operator drains the whole collection.
- Reading an ERC-721 `ownerOf` after transfer inside the callback — it is stale until the mint completes.

## Verification

    forge test --match-test "testERC721|testERC1155" -vvvv

Pass: the reentrancy test reverts or the token count is unchanged after the callback. The selector test asserts `supportsInterface(0x150b7a02) == true` for a receiver.

Report each callback site, the selector returned, and the safeMint ordering.
