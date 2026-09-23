# CDP / E2E Proof Surfaces

A Perps tab screenshot proves market data only when a non-zero price or position value is visible or a CDP state assertion confirms live data; a navigated route over a loading skeleton is not proof.

- **Perps tab screenshot treated as market-data-loaded proof** — a screenshot of the Perps tab can show a navigated route (e.g., `/perps/market/BTC`) while the page body is still a loading skeleton. Route navigation is *not* evidence that prices, positions, or market data have loaded. Before citing a screenshot as market-data proof, confirm a non-zero price or position value is visible in the image, or pair it with a CDP state assertion that confirms live data is present.
