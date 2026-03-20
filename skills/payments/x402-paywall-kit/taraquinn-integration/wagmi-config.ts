/**
 * Wagmi configuration for taraquinn.ai USDC payments.
 *
 * Add to the app root (e.g., _app.tsx or layout.tsx) wrapped in WagmiProvider.
 *
 * Prerequisites:
 *   npm install wagmi viem @tanstack/react-query
 *
 * Usage:
 *   import { WagmiProvider } from "wagmi";
 *   import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
 *   import { wagmiConfig } from "./wagmi-config";
 *
 *   const queryClient = new QueryClient();
 *
 *   <WagmiProvider config={wagmiConfig}>
 *     <QueryClientProvider client={queryClient}>
 *       {children}
 *     </QueryClientProvider>
 *   </WagmiProvider>
 */

import { http, createConfig } from "wagmi";
import { base, baseSepolia } from "wagmi/chains";
import { injected, walletConnect } from "wagmi/connectors";

export const wagmiConfig = createConfig({
  chains: [base, baseSepolia],
  connectors: [
    injected(), // MetaMask, Coinbase Wallet, etc.
    // Uncomment and add your WalletConnect project ID for mobile wallet support:
    // walletConnect({ projectId: process.env.NEXT_PUBLIC_WC_PROJECT_ID! }),
  ],
  transports: {
    [base.id]: http(),
    [baseSepolia.id]: http(),
  },
});
