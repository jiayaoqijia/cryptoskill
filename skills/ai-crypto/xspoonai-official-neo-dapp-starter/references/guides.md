# Guides & Best Practices

## Customization Guide

### Adding a New Page

```typescript
// 1. Create page component
// src/ui/my-feature/my-component.tsx
'use client';
import { FC, ComponentProps } from 'react';

export const MyComponent: FC<ComponentProps<'div'>> = (props) => {
  return <div {...props}>My Feature</div>;
};

// 2. Create page route
// src/app/my-feature/page.tsx
import { MyComponent } from '@/ui/my-feature/my-component';

export default function Page() {
  return (
    <div className="container">
      <h1>My Feature</h1>
      <MyComponent className="mt-4" />
    </div>
  );
}
```

### Adding a New Token Operation

```typescript
// 1. Add API function in src/lib/apis/tokens.ts
export async function getTokenInfo(params: {
  chainId: ChainId;
  scriptHash: string;
}) {
  const [symbol, decimals] = await Promise.all([
    getSymbol(params),
    getDecimals(params),
  ]);
  return { symbol, decimals };
}

// 2. Add React Query hook in src/lib/hooks/tokens.ts
export function useTokenInfo(params: GetDecimalsParams | SkipToken) {
  return useQuery({
    queryKey: ["tokenInfo", params],
    queryFn: params !== skipToken ? () => getTokenInfo(params) : skipToken,
    staleTime: Infinity,
  });
}
```

### Adding a New Contract Interaction

```typescript
// Example: Calling a custom contract method
import {
  invokeRead,
  invoke,
  waitForTransaction,
} from "@/lib/utils/neo/actions";

// Read-only call
const result = await invokeRead({
  chainId: ChainId.Mainnet,
  scriptHash: "0xYourContractHash",
  operation: "myReadMethod",
  args: [{ type: "String", value: "hello" }],
});

// State-changing call (requires connected wallet)
const { transactionHash } = await invoke({
  chainId: ChainId.Mainnet,
  account: connectedAddress,
  scriptHash: "0xYourContractHash",
  operation: "myWriteMethod",
  args: [{ type: "Integer", value: "42" }],
  signers: [
    { account: addressToScriptHash(connectedAddress), scopes: "CalledByEntry" },
  ],
});

// Wait for confirmation
const applicationLog = await waitForTransaction({
  chainId: ChainId.Mainnet,
  hash: transactionHash,
});
```

## Best Practices

1. **Always use Testnet first**: Develop and test on Testnet before deploying to Mainnet
2. **Validate addresses**: Use `isAddress()` from `misc.ts` before any address operations
3. **Validate script hashes**: Use `isScriptHash()` before contract interactions
4. **Check wallet connection**: Use `ensureCurrentConnectorReady()` before state-changing operations
5. **Use BigNumber.js for amounts**: Never use floating-point for token calculations
6. **Use staleTime: Infinity**: For immutable data like token `decimals` and `symbol`
7. **Handle all error types**: Provide meaningful user feedback for each error category
8. **Use the @Catch decorator**: For consistent error handling in connector implementations
9. **Secure environment variables**: Never expose private keys in frontend code
10. **Follow the abstract Connector pattern**: When adding new wallet integrations
11. **Use `skipToken`**: To conditionally skip React Query fetches instead of conditional hooks
12. **Keep API routes at the edge**: Use `export const runtime = 'edge'` for low-latency responses
13. **Use `withResponse`**: Wrap all API handlers for consistent error serialization
14. **Invalidate queries after mutations**: As demonstrated in `useTransfer` hook
15. **Leverage TypeScript strict mode**: All types should be explicit, avoid `any`

## Security Warnings

- **Never expose private keys** in frontend code or environment variables prefixed with `NEXT_PUBLIC_`
- **Verify contract script hashes** before any invocation — confirm against official sources
- **Validate all user inputs** (addresses, amounts, script hashes) before blockchain operations
- **Use `CalledByEntry` scope** for signers unless broader scope is explicitly required
- **Check wallet version compatibility** before allowing connections (enforced by `connectorMinimumVersions`)
- **Be cautious of unverified contracts** — always verify contract source code and audit status
- **Use Testnet for development** — never test with real assets on Mainnet
- **Implement rate limiting** on API routes to prevent abuse
- **Keep dependencies updated** — regularly run `pnpm audit` for security vulnerabilities

## Example Queries

1. "Create a new Neo N3 dApp using this starter template"
2. "Add a new page that displays NEP-17 token holdings for the connected wallet"
3. "Integrate a new wallet connector for Neon Wallet"
4. "Show me how to call a custom smart contract method from this template"
5. "Add a token swap interface using a Neo DEX contract"
6. "Deploy this dApp to Cloudflare Pages"
7. "Add a new API route that fetches blockchain data"
8. "How do I switch between Mainnet and Testnet?"
9. "Add an NFT gallery page that reads NEP-11 token data"
10. "Implement batch contract invocations for multiple transfers"
11. "Add NeoFura API integration for advanced wallet analytics"
12. "Create a governance voting page for a DAO smart contract"
13. "Add transaction history page with pagination"
14. "Customize the theme colors and add a brand logo"
15. "Add automated testing for the token transfer flow"

## Context Variables

- `{{action}}`: Operation to perform (create, configure, add-connector, add-token, add-page, deploy)
- `{{network}}`: Target network (mainnet, testnet)
- `{{connector}}`: Wallet connector type (neoline, onegate, custom)
- `{{deployment_target}}`: Deployment platform (vercel, cloudflare)
- `{{script_hash}}`: Smart contract script hash
- `{{token}}`: Token identifier (symbol or script hash)

## Resources

- [Neo N3 Documentation](https://docs.neo.org) — Official Neo documentation
- [Neo Developer Portal](https://developers.neo.org) — Developer resources and tutorials
- [neon-core SDK](https://github.com/CityOfZion/neon-js) — City of Zion's Neo JavaScript SDK
- [Neo dAPI](https://github.com/nickkelly1/neo-dapi) — Neo dAPI standard
- [NeoFura API](https://neofura.ngd.network) — Advanced Neo N3 data API
- [Next.js Documentation](https://nextjs.org/docs) — Next.js framework docs
- [shadcn/ui](https://ui.shadcn.com) — Component library documentation
- [Jotai](https://jotai.org) — Atomic state management docs
- [TanStack Query](https://tanstack.com/query) — React Query documentation
- [Tailwind CSS](https://tailwindcss.com) — Utility-first CSS framework
- [Cloudflare Pages](https://pages.cloudflare.com) — Edge deployment platform
- [Vercel](https://vercel.com) — Next.js deployment platform
