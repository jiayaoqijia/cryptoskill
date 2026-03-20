import {
  TokenResponse,
  QuoteResponse,
} from '@defuse-protocol/one-click-sdk-typescript';

// Groups tokens by blockchain
export function groupTokensByBlockchain(
  tokens: TokenResponse[],
): Record<string, TokenResponse[]> {
  return tokens.reduce(
    (acc, token) => {
      if (!acc[token.blockchain]) {
        acc[token.blockchain] = [];
      }
      acc[token.blockchain].push(token);
      return acc;
    },
    {} as Record<string, TokenResponse[]>,
  );
}

// Displays tokens grouped by chain in a formatted table
export function displayTokensByBlockchain(tokens: TokenResponse[]): void {
  const tokensByBlockchain = groupTokensByBlockchain(tokens);
  const sortedBlockchains = Object.keys(tokensByBlockchain).sort();

  sortedBlockchains.forEach((blockchain) => {
    // Sort tokens within each blockchain by symbol
    const sortedTokens = tokensByBlockchain[blockchain].sort((a, b) =>
      a.symbol.localeCompare(b.symbol),
    );

    console.log(`\n━━━ Chain: ${blockchain.toUpperCase()} ━━━`);
    console.table(
      sortedTokens.map((token) => ({
        Symbol: token.symbol,
        Price: token.price || 'N/A',
        'Asset ID': token.assetId || 'N/A',
      })),
    );
  });
}

export function displaySwapCostTable(quote: QuoteResponse) {
  const amountInUsd = Number(quote.quote?.amountInUsd) || 0;
  const amountOutUsd = Number(quote.quote?.amountOutUsd) || 0;
  const swapCost = (amountInUsd - amountOutUsd).toFixed(4);

  console.log(`
┌─────────────────────┬──────────────┐
│ Swap Cost Breakdown │ USD Value    │
├─────────────────────┼──────────────┤
│ Amount In           │ $${amountInUsd.toFixed(4).padStart(10)}  │
│ Amount Out          │ $${amountOutUsd.toFixed(4).padStart(10)}  │
│ ─────────────────── │ ──────────── │
│ Total Swap Cost     │ $${swapCost.padStart(10)}  │
└─────────────────────┴──────────────┘
`);
}
