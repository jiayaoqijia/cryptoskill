# ckETH / ckERC20: frontend module (TypeScript)

Install the dependencies, then generate bindings for the minter from its deployed interface. The `@icp-sdk/canisters/cketh` wrapper lacks `deposit_erc20`, `deposit_eth` and `withdrawal_status`.

```bash
npm i @icp-sdk/core@^6 @icp-sdk/canisters@^4 @dfinity/utils@^5 viem@^2 @dfinity/ic-pub-key@^1
icp canister metadata sv3dd-oaaaa-aaaar-qacoa-cai candid:service -n ic > cketh_minter.did
npx @icp-sdk/bindgen --did-file ./cketh_minter.did --out-dir ./src/bindings
```

Pass the identity that owns the tokens: the user's Internet Identity or signer agent for a non-custodial app. Every function takes the context returned by `ckEth(identity)`. Amounts are `bigint` in the token's smallest unit (wei for ckETH, 10^6 for ckUSDC; read `icrc1_decimals`).

```typescript
import { HttpAgent, type Identity } from "@icp-sdk/core/agent";
import { Principal } from "@icp-sdk/core/principal";
import { IcrcLedgerCanister } from "@icp-sdk/canisters/ledger/icrc";
import { encodePrincipalToEthAddress } from "@icp-sdk/canisters/cketh";
import { ecdsa } from "@dfinity/ic-pub-key";
import { createActor } from "./bindings/cketh_minter";
import { createPublicClient, createWalletClient, custom, http, erc20Abi, parseAbi, toHex, type Address, type Hex } from "viem";
import { publicKeyToAddress } from "viem/accounts";
import { mainnet } from "viem/chains";

const CKETH_MINTER = Principal.fromText("sv3dd-oaaaa-aaaar-qacoa-cai");
const CKETH_LEDGER = Principal.fromText("ss2fx-dyaaa-aaaar-qacoq-cai");

export async function ckEth(identity: Identity) {
  const agent = await HttpAgent.create({ identity });
  return { minter: createActor(CKETH_MINTER.toText(), { agent }),
           ledger: (id: Principal) => IcrcLedgerCanister.create({ agent, canisterId: id }) };
}
type Ctx = Awaited<ReturnType<typeof ckEth>>;

export async function listCkErc20Tokens({ minter }: Ctx) {
  const info = await minter.get_minter_info();
  const min = new Map((info.minimum_deposit_amounts ?? []).map((m) => [m.erc20_contract_address.toLowerCase(), m.minimum_deposit_amount]));
  return (info.supported_ckerc20_tokens ?? []).map((t) => ({
    symbol: t.ckerc20_token_symbol, erc20Address: t.erc20_contract_address, ledgerId: t.ledger_canister_id,
    minDeposit: min.get(t.erc20_contract_address.toLowerCase()),
  }));
}

// Flow A — called with the USER's identity; tokens are minted to (user, subaccount).
export async function getErc20DepositAddress({ minter }: Ctx, erc20Address: string, subaccount?: Uint8Array) {
  const res = await minter.deposit_erc20({ erc20_contract_address: erc20Address, mode: { __kind__: "Unsponsored", Unsponsored: { subaccount } } });
  if (res.__kind__ === "Err") throw new Error(res.Err.__kind__);
  if (res.Ok.minimum_deposit_amount === 2n ** 256n - 1n) throw new Error("deposits unavailable for this token");
  return res.Ok; // { address, minimum_deposit_amount, status: Scanning | AwaitingSweep }
}
export async function getEthDepositAddress({ minter }: Ctx, subaccount?: Uint8Array) {
  const res = await minter.deposit_eth({ mode: { __kind__: "Unsponsored", Unsponsored: { subaccount } } });
  if (res.__kind__ === "Err") throw new Error(res.Err.__kind__);
  return res.Ok;
}
export function deriveEthDepositAddress(owner: Principal, subaccount = new Uint8Array(32)): Address { // display/verify only
  const master = ecdsa.secp256k1.PublicKeyWithChainCode.forMainnetKey("key_1");
  const path = new ecdsa.secp256k1.DerivationPath([CKETH_MINTER.toUint8Array(), new Uint8Array([1]), owner.toUint8Array(), subaccount]);
  const { x, y } = master.deriveSubkeyWithChainCode(path).public_key.toAffinePoint();
  return publicKeyToAddress(`0x04${x.toString(16).padStart(64, "0")}${y.toString(16).padStart(64, "0")}`);
}

// Flow B — user signs on Ethereum with an injected wallet (window.ethereum).
const HELPER_ABI = parseAbi([
  "function depositEth(bytes32 principal, bytes32 subaccount) payable",
  "function depositErc20(address erc20Address, uint256 amount, bytes32 principal, bytes32 subaccount)",
]);
export async function depositViaHelper({ minter }: Ctx, ethereum: { request(...a: any[]): Promise<any> },
  owner: Principal, amount: bigint, erc20Address?: Address, subaccount = new Uint8Array(32)): Promise<Hex> {
  const info = await minter.get_minter_info();
  const helper = info.deposit_with_subaccount_helper_contract_address as Address | undefined;
  if (!helper) throw new Error("helper not configured");
  const args = [encodePrincipalToEthAddress(owner) as Hex, toHex(subaccount, { size: 32 })] as const;
  const wallet = createWalletClient({ chain: mainnet, transport: custom(ethereum) });
  const pub = createPublicClient({ chain: mainnet, transport: http() });
  const [account] = await wallet.requestAddresses();
  if (!erc20Address)
    return wallet.writeContract({ account, chain: mainnet, address: helper, abi: HELPER_ABI, functionName: "depositEth", args, value: amount });
  if (!(info.supported_ckerc20_tokens ?? []).some((t) => t.erc20_contract_address.toLowerCase() === erc20Address.toLowerCase()))
    throw new Error("unsupported ERC-20: funds would be lost");
  const allowance = await pub.readContract({ address: erc20Address, abi: erc20Abi, functionName: "allowance", args: [account, helper] });
  if (allowance < amount) {
    for (const value of allowance > 0n ? [0n, amount] : [amount]) { // USDT: reset to 0 first
      const h = await wallet.writeContract({ account, chain: mainnet, address: erc20Address, abi: erc20Abi, functionName: "approve", args: [helper, value] });
      await pub.waitForTransactionReceipt({ hash: h });
    }
  }
  return wallet.writeContract({ account, chain: mainnet, address: helper, abi: HELPER_ABI, functionName: "depositErc20", args: [erc20Address, amount, ...args] });
}

// Withdrawals — called with the identity that owns the ck tokens.
const spender = { owner: CKETH_MINTER, subaccount: [] as [] };
export async function withdrawEth(ctx: Ctx, recipient: string, amountWei: bigint) {
  await ctx.ledger(CKETH_LEDGER).approve({ spender, amount: amountWei });
  const res = await ctx.minter.withdraw_eth({ recipient, amount: amountWei });
  if (res.__kind__ === "Err") throw new Error(res.Err.__kind__);
  return res.Ok.block_index; // withdrawal id
}
export async function withdrawErc20(ctx: Ctx, ckErc20LedgerId: Principal, recipient: string, amount: bigint) {
  const price = await ctx.minter.eip_1559_transaction_price({ ckerc20_ledger_id: ckErc20LedgerId });
  await ctx.ledger(CKETH_LEDGER).approve({ spender, amount: (price.max_transaction_fee * 3n) / 2n });
  await ctx.ledger(ckErc20LedgerId).approve({ spender, amount });
  const res = await ctx.minter.withdraw_erc20({ ckerc20_ledger_id: ckErc20LedgerId, recipient, amount });
  if (res.__kind__ === "Err") throw new Error(res.Err.__kind__);
  return res.Ok.cketh_block_index; // withdrawal id
}
export async function withdrawalStatus({ minter }: Ctx, id: bigint) {
  const [d] = await minter.withdrawal_status({ __kind__: "ByWithdrawalId", ByWithdrawalId: id });
  return d?.status;
}
```
