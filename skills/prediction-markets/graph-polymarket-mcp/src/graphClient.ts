export class GraphClientError extends Error {
  constructor(
    message: string,
    public readonly statusCode?: number,
    public readonly graphErrors?: unknown[]
  ) {
    super(message);
    this.name = "GraphClientError";
  }
}

export async function querySubgraph(
  ipfsHash: string,
  query: string,
  variables?: Record<string, unknown>
): Promise<unknown> {
  const apiKey = process.env.GRAPH_API_KEY;
  if (!apiKey) {
    throw new GraphClientError(
      "GRAPH_API_KEY environment variable is required. " +
        "Get one at https://thegraph.com/studio/apikeys/"
    );
  }

  const url = `https://gateway.thegraph.com/api/${apiKey}/deployments/id/${ipfsHash}`;

  const body: Record<string, unknown> = { query };
  if (variables && Object.keys(variables).length > 0) {
    body.variables = variables;
  }

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new GraphClientError(
      `Graph API returned HTTP ${response.status}: ${response.statusText}`,
      response.status
    );
  }

  const json = (await response.json()) as {
    data?: unknown;
    errors?: unknown[];
  };

  if (json.errors && json.errors.length > 0) {
    // Distinguish "your query is wrong" from "nobody is serving this data". The gateway reports
    // both as GraphQL errors, but they need opposite responses: one is fixed by rewriting the
    // query, the other cannot be fixed by the caller at all. Left undistinguished, a model retries
    // a rewritten query against a subgraph no indexer serves, forever.
    const text = JSON.stringify(json.errors);
    if (/subgraph not found/i.test(text)) {
      throw new GraphClientError(
        `Subgraph ${ipfsHash} is not currently served on The Graph Network — no indexer is ` +
          `allocated to this deployment, so it cannot answer any query. This is an availability ` +
          `problem, not a query problem: do not retry with a different query. Use list_subgraphs ` +
          `to pick another subgraph covering the same data.`,
        undefined,
        json.errors
      );
    }
    if (/bad indexers/i.test(text)) {
      throw new GraphClientError(
        `Subgraph ${ipfsHash} has indexers allocated but none returned a usable response ` +
          `(gateway reported "bad indexers"). Often transient — retrying the same query later may ` +
          `work. If it persists, the deployment needs re-indexing. Raw: ${text}`,
        undefined,
        json.errors
      );
    }
    throw new GraphClientError(`GraphQL errors: ${text}`, undefined, json.errors);
  }

  return json.data;
}
