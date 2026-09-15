import { createPublicClient, http } from "viem";
import { base } from "viem/chains";
import { BASE_RPC_URL } from "./constants.js";

export const client = createPublicClient({
  chain: base,
  transport: http(BASE_RPC_URL, {
    // The public Base RPC rate-limits bursts of eth_call requests (this project
    // makes many, one per pool per epoch window). Retry with backoff rather than
    // failing the whole run on a transient "over rate limit" response.
    retryCount: 6,
    retryDelay: 1500,
    batch: true,
  }),
});
