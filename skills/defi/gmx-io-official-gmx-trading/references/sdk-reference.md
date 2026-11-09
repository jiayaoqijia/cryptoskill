# GmxApiSdk reference

Checked against the published `@gmx-io/sdk@2.2.1` declarations and implementation. [SDK v2 docs](https://docs.gmx.io/docs/sdk/v2/), [order examples](https://docs.gmx.io/docs/sdk/v2/examples/), and [source](https://github.com/gmx-io/gmx-interface/tree/release/sdk/src/clients/v2) provide the maintained upstream reference.

## Setup and signer

Use the read-only client without a signer. Prefer an existing wallet adapter implementing `IAbstractSigner` for writes. The optional `PrivateKeySigner` example below is for a user who explicitly selected local signing: inject the key through their secret manager into an isolated signing process, never through chat, shell arguments, generated source or model-visible output. Do not read `.env` or wallet files to discover a key. RPC is only needed for on-chain approvals, Classic orders and contract reads; Express signing alone needs no RPC.

The snippets below share this setup and use `await` inside an async function. Compile TypeScript to CommonJS, or use the equivalent `require()` imports in `.cjs` scripts.

```typescript
import {
  GmxApiSdk, PrivateKeySigner, getGasPaymentTokens, parsePrepareOrderError,
  type PrepareOrderRequest, type PrepareOrderResponse,
} from "@gmx-io/sdk/v2";
import { getContract } from "@gmx-io/sdk/configs/contracts";
import { getMarketByLabel, getMarketIndexToken, type MarketLabel } from "@gmx-io/sdk/configs/markets";
import { getTokenBySymbol } from "@gmx-io/sdk/configs/tokens";
import { getBatchTypedData, getExpressContractAddress } from "@gmx-io/sdk/utils/express";
import { convertToContractPrice, parseContractPrice } from "@gmx-io/sdk/utils/tokens";
import {
  createPublicClient, getAddress, hashTypedData, http, isAddress, isAddressEqual,
  maxUint256, parseUnits, zeroAddress, zeroHash, type Hex,
} from "viem";
import { arbitrum } from "viem/chains";

const chainId = 42161;
const sdk = new GmxApiSdk({ chainId });
const privateKey = process.env.GMX_PRIVATE_KEY;
const rpcUrl = process.env.GMX_RPC_URL;
if (!privateKey || !/^0x[0-9a-fA-F]{64}$/.test(privateKey) || !rpcUrl) {
  throw new Error("Provide GMX_PRIVATE_KEY and GMX_RPC_URL securely for this write example");
}
const signer = new PrivateKeySigner(privateKey as Hex, { chain: arbitrum, rpcUrl });
const account = signer.address;
const publicClient = createPublicClient({ chain: arbitrum, transport: http(rpcUrl) });

// API data mixes checksummed and lowercase addresses; placeholders such as "<GM-ADDRESS>" are not addresses
const sameAddress = (a: string, b: string) =>
  isAddress(a, { strict: false }) && isAddress(b, { strict: false }) && isAddressEqual(a, b);
```

For browser/hardware wallets, implement `address`, `signTypedData(domain, types, value)`, and `signMessage(message)`. Optional `sendTransaction({ to, data, value })` is required for wallet-sent transactions; it carries no fee fields, so use a viem wallet client when a write needs explicit `maxFeePerGas` / `maxPriorityFeePerGas` (see [Classic mode](#classic-mode)). `signTypedData` implementations such as `PrivateKeySigner` sign the first struct in `types`; only pass typed data you rebuilt locally (see below). Before any wallet write, verify the wallet/RPC chain ID and signer account against the authorized chain/account; setting viem's `chain` option alone does not verify the remote RPC.

For modern TypeScript, type-check with `module: "ESNext"` and `moduleResolution: "bundler"`; Node16 resolution encounters the SDK's declaration packaging issues. A Node-compatible bundle can keep package imports external so the SDK uses its working CommonJS entry point:

```bash
npm install --save-dev --save-exact --ignore-scripts esbuild@0.28.2
./node_modules/.bin/esbuild script.ts --bundle --platform=node --format=cjs --packages=external --outfile=script.cjs
node script.cjs
```

## Resolve the market and tokens

`symbol` includes the pool suffix. The ETH pool below is an example requested market, not a default trading choice. Use the user's exact selection and reject ambiguous matches.

```typescript
const requestedSymbol = "ETH/USD [WETH-USDC]";
// Trusted addresses and decimals come from the installed SDK registry, not API reads
const registryMarket = getMarketByLabel(chainId, requestedSymbol as MarketLabel);
const usdc = getTokenBySymbol(chainId, "USDC", { isSynthetic: false });
const indexToken = getMarketIndexToken(chainId, registryMarket.marketTokenAddress);
const markets = await sdk.fetchMarkets();
const market = markets.find((m) => m.symbol === requestedSymbol && !m.isSpotOnly);
if (!market || !market.isListed || !sameAddress(market.marketTokenAddress, registryMarket.marketTokenAddress)) {
  throw new Error("Requested perpetual market is unavailable or does not match the SDK registry");
}
if (!sameAddress(usdc.address, registryMarket.longTokenAddress) && !sameAddress(usdc.address, registryMarket.shortTokenAddress)) {
  throw new Error("Selected collateral is not a collateral token of this pool");
}
const positions = await sdk.fetchPositionsInfo({ address: account, includeRelatedOrders: true });
const orders = await sdk.fetchOrders({ address: account });
const capacity = await sdk.getTradingCapacity({ symbol: market.symbol, direction: "long" });
```

Compare addresses with `sameAddress`, never `===`. `getMarketByLabel()` and `getTokenBySymbol()` throw for markets/tokens missing from the installed registry; upgrade the SDK rather than trusting an API-only address. `fetchMarkets()` returns `MarketWithTiers[]`; inspect `leverageTiers`, `minPositionSizeUsd` and `minCollateralUsd`. `getTradingCapacity()` returns USD amounts (`availableLiquidity`, `baseAvailableLiquidity`, `jitAvailableLiquidity`) and `marketDataStatus` / `jitDataStatus`. Capacity is not a reservation or proof that an account qualifies for JIT; review prepare-time validation too.

## Balances and ERC-20 approval

```typescript
const payAmount = parseUnits("100", usdc.decimals);
const balances = await sdk.fetchWalletBalances({ address: account });
const allowances = await sdk.fetchAllowances({ address: account, spender: "router" });
const allowance = allowances.find((t) => sameAddress(t.address, usdc.address))?.allowance ?? 0n;
// USDC also pays the Express relay fee by default; cap it within the user's authorization
const maxRelayFee = parseUnits("2", usdc.decimals);
const requiredAllowance = payAmount + maxRelayFee;

if (allowance < requiredAllowance) {
  const approval = sdk.buildApproveTransaction({
    tokenAddress: usdc.address,
    spender: "router",
    amount: requiredAllowance,
  });
  // Send only within the user's authorization, then confirm mining.
  const approvalHash = await signer.sendTransaction(approval);
  const receipt = await publicClient.waitForTransactionReceipt({ hash: approvalHash as Hex });
  if (receipt.status !== "success") throw new Error("Token approval reverted");
}
```

`"router"` resolves to `SyntheticsRouter`, not `ExchangeRouter` or a relay router. Supplying `amount` avoids the builder's unlimited-approval default. Native coin has no ERC-20 approval.

Express pays the relay fee in the request's `gasPaymentToken`, which must be an address from `getGasPaymentTokens(chainId)`. The default is the first entry: USDC on Arbitrum and Avalanche, USDM on MegaETH. Every Express action pulls the input and the relay fee through the same `SyntheticsRouter` allowance, so when the input token also pays gas, an approval of exactly `payAmount` fails at relay time. Approve the input plus the authorized fee cap (`maxRelayFee` above), and reject a prepared `relayParams.fee.feeAmount` above that cap. Do not silently enlarge approvals.

## Prepare an increase

```typescript
const request: PrepareOrderRequest = {
  kind: "increase",
  symbol: market.symbol,
  direction: "long",
  orderType: "market",
  size: parseUnits("500", 30),
  collateralToken: usdc.symbol,
  collateralToPay: { amount: payAmount, token: usdc.symbol },
  slippage: 30,
  gasPaymentToken: usdc.address,
  mode: "express",
  from: account,
};
const prepared = await sdk.prepareOrder(request);
console.log(prepared.estimates, prepared.warnings, prepared.validationWarnings);
```

This example requests $500 notional with 100 USDC input; fees and an existing position affect resulting leverage. The v2 request has no v1 `leverage` or `payAmount` field. Use `direction: "short"` for a short. Discover allowable collateral instead of assuming all longs require WETH.

Before signing, inspect `estimates` (including effective `sizeDeltaUsd`, fees, impact and capacity), both warning arrays, and `expiresAt`. The server may adjust an almost-full close to a full close. An expired preparation needs a fresh review. `parsePrepareOrderError(error)` decodes a caught SDK `HttpError` from preparation; `isPrepareOrderError()` tests an already parsed value. Handle invalid parameters, missing markets/tokens/positions, unavailable routes, and insufficient liquidity without widening the user's limits.

## Verify the prepared action

API estimates and warnings are display data, not authorization. SDK `signOrder()` checks only the signing domain (any of several relay routers), non-empty `types` and create-order receivers. It does not check amounts, prices, markets, update/cancel actions or `relayParams`, and the signed `Batch` carries `relayParams` only as a hash. A compromised API could therefore get a changed notional, a subaccount grant, or `relayParams.externalCalls` that move the account's router-approved tokens signed. Do not sign the API's `typedData`. Rebuild it locally from the `batchParams` and `relayParams` you will submit, check those, and sign the rebuilt copy:

```typescript
type ExpectedIncrease = {
  market: string; collateralToken: string; isLong: boolean;
  sizeDeltaUsd: bigint; collateralAmount: bigint;
  acceptablePriceLimit: bigint; // contract price: max for longs, min for shorts
  maxExecutionFee: bigint; maxRelayFee: bigint; maxDeadlineSeconds: number;
};

function buildVerifiedExpressTypedData(prepared: PrepareOrderResponse, expected: ExpectedIncrease) {
  if (prepared.mode !== "express" || prepared.payloadType !== "typed-data") {
    throw new Error("Expected an Express signing payload");
  }
  // Read named fields only; never iterate API objects to find them
  const { batchParams, relayParams, typedData } = prepared.payload;
  const { externalCalls, tokenPermits, fee, deadline } = relayParams;
  const now = Math.floor(Date.now() / 1000);

  const externalCallLists = [
    externalCalls.sendTokens, externalCalls.sendAmounts, externalCalls.externalCallTargets,
    externalCalls.externalCallDataList, externalCalls.refundTokens, externalCalls.refundReceivers,
  ];
  if (tokenPermits.length !== 0 || externalCallLists.some((list) => list.length !== 0)) {
    throw new Error("Unexpected token permits or external calls");
  }
  if (!getGasPaymentTokens(chainId).some((token) => sameAddress(token, fee.feeToken)) ||
      !sameAddress(fee.feeToken, usdc.address) || BigInt(fee.feeAmount) > expected.maxRelayFee) {
    throw new Error("Unexpected relay fee");
  }
  if (BigInt(deadline) <= BigInt(now) || BigInt(deadline) > BigInt(now + expected.maxDeadlineSeconds)) {
    throw new Error("Stale or unbounded deadline");
  }
  if (batchParams.updateOrderParams.length !== 0 || batchParams.cancelOrderParams.length !== 0 ||
      batchParams.createOrderParams.length !== 1) {
    throw new Error("Unexpected actions in batch");
  }

  // Only orderPayload is signed; ignore the unsigned params/tokenTransfersParams siblings
  const order = batchParams.createOrderParams[0].orderPayload;
  const { addresses, numbers } = order;
  const acceptablePrice = BigInt(numbers.acceptablePrice);
  if (
    !sameAddress(addresses.receiver, account) ||
    !(sameAddress(addresses.cancellationReceiver, zeroAddress) || sameAddress(addresses.cancellationReceiver, account)) ||
    !sameAddress(addresses.callbackContract, zeroAddress) ||
    !sameAddress(addresses.uiFeeReceiver, zeroAddress) ||
    !sameAddress(addresses.market, expected.market) ||
    !sameAddress(addresses.initialCollateralToken, expected.collateralToken) ||
    addresses.swapPath.length !== 0 ||
    order.orderType !== 2 || // MarketIncrease
    order.isLong !== expected.isLong ||
    order.referralCode !== zeroHash ||
    BigInt(numbers.sizeDeltaUsd) !== expected.sizeDeltaUsd ||
    BigInt(numbers.initialCollateralDeltaAmount) !== expected.collateralAmount ||
    BigInt(numbers.executionFee) > expected.maxExecutionFee ||
    BigInt(numbers.callbackGasLimit) !== 0n ||
    (expected.isLong ? acceptablePrice > expected.acceptablePriceLimit : acceptablePrice < expected.acceptablePriceLimit)
  ) {
    throw new Error("Prepared order does not match the authorized intent");
  }

  const rebuilt = getBatchTypedData({
    chainId, batchParams, relayParams, account,
    relayRouterAddress: getExpressContractAddress(chainId, { isSubaccount: false, isMultichain: false, scope: "order" }),
  });
  const digest = (data: typeof rebuilt) => hashTypedData({ ...data, primaryType: "Batch" } as Parameters<typeof hashTypedData>[0]);
  if (Object.keys(rebuilt.types)[0] !== "Batch" || digest(typedData) !== digest(rebuilt)) {
    throw new Error("API typed data does not match the submitted batch");
  }
  return rebuilt;
}
```

This example covers one market increase on the main account. Adapt the checks for each supported action and reject anything else: TP/SL and TWAP add one `createOrderParams` entry per order (check every type, trigger and size), edits use `updateOrderParams[].updatePayload`, and cancellations use `cancelOrderParams[].orderKey`. Derive `acceptablePriceLimit` from an independent price and the user's slippage, converted with `convertToContractPrice(price, indexToken.decimals)` from `@gmx-io/sdk/utils/tokens`. Order creation binds a non-zero `referralCode` to an account that has none, so require `zeroHash` unless the user supplied a code. `dataList` carries server metadata and is not empty.

For Classic mode, decode every inner `multicall` item and allowlist calls per operation: create is `sendWnt`/`sendTokens` to `OrderVault` then `createOrder`; edit is an optional `sendWnt` to `OrderVault` then `updateOrder`; cancel is `cancelOrder`. Reject everything else, including `sendTokens`/`sendNativeToken` to other receivers, claim functions and `makeExternalCalls`. Check the `createOrder` fields as above and the total native value, then simulate the reviewed transaction before broadcasting. Use the reviewed SDK registry for address checks, not a replacement address supplied in an API error or token description.

## Sign and submit Express

Sign only the rebuilt typed data, then submit the same `batchParams` and `relayParams`. Reuse the same SDK instance for preparation, submission and status.

```typescript
async function submitVerified(prepared: PrepareOrderResponse, expected: ExpectedIncrease) {
  const typedData = buildVerifiedExpressTypedData(prepared, expected);
  const signature = await signer.signTypedData(typedData.domain, typedData.types, typedData.message);
  const submitted = await sdk.submitOrder({
    mode: "express",
    requestId: prepared.requestId,
    from: account,
    signature,
    eip712Data: {
      batchParams: prepared.payload.batchParams,
      relayParams: prepared.payload.relayParams,
    },
  });
  // Submit can return HTTP 200 with a failed relay
  if (submitted.status === "relay_failed" || submitted.status === "relay_reverted") {
    throw new Error(`Relay rejected ${submitted.requestId}: ${submitted.error?.message ?? submitted.status}`);
  }
  return submitted;
}

const submitted = await submitVerified(prepared, {
  market: registryMarket.marketTokenAddress,
  collateralToken: usdc.address,
  isLong: true,
  sizeDeltaUsd: request.size!,
  collateralAmount: payAmount,
  // User-authorized limits: worst entry price and native execution fee
  acceptablePriceLimit: convertToContractPrice(parseUnits("3100", 30), indexToken.decimals),
  maxExecutionFee: parseUnits("0.001", 18),
  maxRelayFee,
  maxDeadlineSeconds: 3_600,
});
```

Persist the request ID, chain, account and intended operation before submission. The API has no idempotency key: recovery is by `requestId` only, and submit/status bodies with extra fields are rejected with HTTP 400. Preserve the same signed request on any retry. A signed Express payload can authorize a trade until its deadline; keep retry material in access-controlled storage, never in chat, public logs or committed files.

Do not use `executeExpressOrder()`. It prepares, signs and submits in one call, so there is no point to run the checks above, and on an instance with a generated subaccount it also signs a default subaccount grant.

## Track creation and execution

```typescript
async function waitForOrder(requestId: string, waitFor: "created" | "executed") {
  const deadline = Date.now() + 60_000;
  while (Date.now() < deadline) {
    const status = await sdk.fetchOrderStatus({ requestId });
    // relay_unknown (missing from the SDK type) means the relay outcome is undetermined: keep polling
    if (["cancelled", "relay_failed", "relay_reverted"].includes(status.status)) {
      throw new Error(JSON.stringify(status));
    }
    if (status.status === "executed" || (waitFor === "created" && status.status === "created")) {
      return status;
    }
    await new Promise((resolve) => setTimeout(resolve, 2_000));
  }
  throw new Error(`Still unresolved: ${requestId}. Reconcile this request before retrying.`);
}

const result = await waitForOrder(submitted.requestId, "executed");
const refreshedPositions = await sdk.fetchPositionsInfo({ address: account });
```

Status progression includes `prepared`, `relay_accepted`, `relay_pending`, `relay_submitted`, `created`, then `executed` or `cancelled`; relay failures are `relay_failed` / `relay_reverted`. The API also returns `relay_unknown` when the relay outcome is undetermined (for example after an HTTP 503 on submit); the SDK status type lacks it, so treat it as unresolved, not failed. Inspect `error`, `cancellationReason`, `createdTxnHash`, `executionTxnHash` and `orderKeys`. Use `"created"` for resting limit/stop orders, then monitor triggers separately.

The status `orderKeys` list can miss keys of a multi-order batch. For TP/SL and TWAP, read every `OrderCreated` event from the `createdTxnHash` receipt's `EventEmitter` logs and track each key, rather than treating one execution or disappearance as completion of the entire strategy. API reads can lag confirmed chain state.

## Close or reduce the exact position

```typescript
const currentPositions = await sdk.fetchPositionsInfo({ address: account });
const position = currentPositions.find((p) =>
  sameAddress(p.marketAddress, registryMarket.marketTokenAddress) &&
  p.isLong && sameAddress(p.collateralTokenAddress, usdc.address)
);
if (!position) throw new Error("Selected position was not found");

const closePrepared = await sdk.prepareOrder({
  kind: "decrease",
  symbol: market.symbol,
  direction: position.isLong ? "long" : "short",
  orderType: "market",
  size: position.sizeInUsd,
  collateralToken: usdc.symbol,
  receiveToken: usdc.symbol,
  keepLeverage: false,
  slippage: 30,
  mode: "express",
  from: account,
});
```

Review and submit `closePrepared` through the same flow. For a partial close use the authorized USD size. `keepLeverage: true` withdraws collateral proportionally; `false` retains collateral on partial decreases. A full close releases remaining collateral. There is no need for v1 `getDecreasePositionAmounts()` or `createDecreaseOrder()` here.

## Edit, cancel, or change collateral

These are alternative preparation calls; do not run them all as one script. Get the selected order from a fresh `fetchOrders()` result and the position from `fetchPositionsInfo()`. Verify ownership and the exact intended target. The result uses the same review/sign/submit path.

```typescript
async function prepareEdit(orderKey: string, changes: { size?: bigint; triggerPrice?: bigint; acceptablePrice?: bigint }) {
  const order = (await sdk.fetchOrders({ address: account })).find((o) => o.key === orderKey);
  if (!order || !sameAddress(order.account, account)) throw new Error("Selected order was not found");
  if (sameAddress(order.marketAddress, zeroAddress)) throw new Error("Swap orders cannot be edited");
  const { decimals } = getMarketIndexToken(chainId, getAddress(order.marketAddress));
  // fetchOrders() returns contract prices; the edit API expects USD30 and fills omitted prices wrongly
  const keep = (price: bigint) =>
    price === 0n ? undefined : price === maxUint256 ? price : parseContractPrice(price, decimals);
  return sdk.prepareEditOrder({
    orderIds: [orderKey],
    newSize: changes.size ?? (order.sizeDeltaUsd > 0n ? order.sizeDeltaUsd : undefined),
    newTriggerPrice: changes.triggerPrice ?? keep(order.triggerPrice),
    newAcceptablePrice: changes.acceptablePrice ?? keep(order.acceptablePrice),
    mode: "express",
    from: account,
  });
}

async function prepareCancel(orderKey: string) {
  return sdk.prepareCancelOrder({
    orderId: orderKey, mode: "express", from: account,
  });
}

async function prepareCollateralChange(amount: bigint, slippage: number) {
  const target = (await sdk.fetchPositionsInfo({ address: account })).find((p) =>
    sameAddress(p.marketAddress, registryMarket.marketTokenAddress) &&
    p.isLong && sameAddress(p.collateralTokenAddress, usdc.address)
  );
  if (!target) throw new Error("Selected position was not found");
  return sdk.prepareCollateral({
    operation: "withdraw", positionKey: target.contractKey, amount, slippage, mode: "express", from: account,
  });
}
```

Always send `newTriggerPrice` and `newAcceptablePrice`. When either is omitted, the API reuses the stored contract price and converts it a second time, which collapses it to about zero: a long loses its slippage protection, a short can never fill, a long stop-loss never fires and a long take-profit fires at once. Keep unchanged values by converting the `fetchOrders()` price with `parseContractPrice(price, indexTokenDecimals)`. Leave out stored zeros (the API rejects 0) and pass `maxUint256` unchanged. Swap orders cannot be edited (`Market not found`). An edit resets `validFromTime`, so cancel TWAP parts instead of editing them. Editing also supports `newAutoCancel` and `executionFeeTopUp`.

Cancellation supports explicit `orderIds`, or `all: true` only when all-account cancellation is intended. `positionKey` is the position's bytes32 `contractKey`; `position.key` (`account:market:collateral:isLong`) returns `Position not found`. Collateral `amount` is in collateral-token units, not USD30. A withdrawal sets a minimum output of the amount's USD value less `slippage` (30 bps by default), so pass the user-authorized slippage. Monitor the affected order/position after edits and cancellations.

## Classic mode

`IAbstractSigner.sendTransaction()` cannot carry fee fields, so send Classic orders with a viem wallet client for the same verified account:

```typescript
import exchangeRouterAbi from "@gmx-io/sdk/abis/ExchangeRouter";
import { createWalletClient, decodeFunctionData } from "viem";
import { privateKeyToAccount } from "viem/accounts";

const walletClient = createWalletClient({
  account: privateKeyToAccount(privateKey as Hex), chain: arbitrum, transport: http(rpcUrl),
});
const classic = await sdk.prepareOrder({ ...request, mode: "classic" });
if (classic.payloadType !== "transaction" || !sameAddress(classic.payload.to, getContract(chainId, "ExchangeRouter"))) {
  throw new Error("Unexpected Classic transaction");
}
const outer = decodeFunctionData({ abi: exchangeRouterAbi, data: classic.payload.data });
if (outer.functionName !== "multicall") throw new Error("Expected an ExchangeRouter multicall");
const orderVault = getContract(chainId, "OrderVault");
const calls = (outer.args[0] as readonly Hex[]).map((data) => decodeFunctionData({ abi: exchangeRouterAbi, data }));
for (const call of calls) {
  const args = call.args as readonly unknown[];
  const allowed =
    (call.functionName === "sendWnt" && sameAddress(args[0] as string, orderVault)) ||
    (call.functionName === "sendTokens" && sameAddress(args[1] as string, orderVault)) ||
    call.functionName === "createOrder";
  if (!allowed) throw new Error(`Unexpected call: ${call.functionName}`);
}
// Check every createOrder's params and the total native value against the authorized action, then simulate.

const hash = await walletClient.sendTransaction({
  to: classic.payload.to,
  data: classic.payload.data,
  value: BigInt(classic.payload.value ?? "0"),
  maxPriorityFeePerGas: 0n, // Arbitrum: the API's execution fee has no priority-fee allowance
});
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Order creation reverted");
```

On Arbitrum the API prices the execution fee at the network gas price plus 30%, with no priority-fee allowance, while the contract requires `executionFee >= adjustedGasLimit * tx.gasprice`. A wallet tip above roughly 30% of the gas price makes creation revert with `InsufficientExecutionFee`, so send without a priority fee or raise `executionFeeBufferBps` within the user's fee limit. Simulate with the same fee fields: `eth_call` and `eth_estimateGas` without them run at `tx.gasprice = 0`, so any execution fee passes.

Do not pass Classic calldata to `signOrder()` or assume Express relay status tracks a wallet-broadcast transaction. Read the creation receipt's `EventEmitter` logs to obtain all order keys; follow keeper execution/cancellation and refetch positions/orders. A successful creation receipt alone does not establish trade execution.

## One-click trading and GMX Account

The SDK's one-click helpers do not enforce the user's limits. `activateSubaccount()` signs the API's approval after checking only the domain and subaccount address, not `maxAllowedCount`, `expiresAt` or the nonce. It requests the later of the on-chain and requested expiry and keeps an existing broader grant. `sdk.signSubaccountApproval()` validates nothing on an instance that has not generated a subaccount, and `executeExpressOrder()` auto-signs a default grant (current count + 90 actions, 7 days) when none is usable. The subaccount key is derived from the main wallet's signature of a fixed message, so that signature is equivalent to the subaccount private key and yields the same subaccount as the web app's one-click session.

For explicitly authorized delegated trading:

1. Read the current grant on-chain: `DataStore.containsAddress(subaccountListKey(account), subaccount)`, `getUint` of `subaccountActionCountKey`, `maxAllowedSubaccountActionCountKey` and `subaccountExpiresAtKey` (keys from `@gmx-io/sdk/configs/dataStore` with `SUBACCOUNT_ORDER_ACTION`), and `SubaccountGelatoRelayRouter.subaccountApprovalNonces(account)`.
2. Prepare the approval with `prepareSubaccountApproval()`. Before the main signer signs, rebuild it with `getSubaccountApprovalTypedData()` from `@gmx-io/sdk/utils/subaccount` using the authorized `expiresAt`, `maxAllowedCount` and the on-chain nonce, and require an equal `hashTypedData` digest with primary type `SubaccountApproval`. `maxAllowedCount` is the cumulative action cap, not the number of additional actions.
3. Sign the rebuilt approval and pass it explicitly as `subaccountApproval` with `subaccountAddress` on each prepare call. Verify each subaccount batch like the main-account flow, rebuilding with `subaccountApprovalHash` (`hashSubaccountApproval()`) and the subaccount relay router. Subaccount batches revert with non-empty external calls, but every other check applies.
4. Never use `activateSubaccount()` defaults or `executeExpressOrder()` for delegated trading.
5. Revoke with `SubaccountRouter.removeSubaccount(subaccount)` from the main account. `clearSubaccount()` only clears local state.

GMX Account funding methods are a separate surface: `buildSameChainDepositTxn`, `buildSameChainWithdrawTxn`, `executeSameChainDeposit`, `executeSameChainWithdraw`, `prepareCrossChainDeposit`, `executeCrossChainDeposit`, and the cross-chain withdraw prepare/sign/submit/status helpers. Follow their exported request types and [official examples](https://docs.gmx.io/docs/sdk/v2/examples/). Settlement-chain funding support is narrower than general trading-chain support; MegaETH is not a settlement chain in 2.2.1. These methods do not mint/burn GM or GLV liquidity tokens.
