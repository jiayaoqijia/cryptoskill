#!/usr/bin/env bun
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import packageJson from '../../package.json';
import { asMcpResult } from './output.js';
import { MCP_TOOL_DESCRIPTORS } from '../tooling/tool-descriptors.js';

const server = new McpServer({
  name: 'aelfscan-skill',
  version: packageJson.version,
});

for (const descriptor of MCP_TOOL_DESCRIPTORS) {
  server.registerTool(
    descriptor.mcpName,
    {
      description: descriptor.description,
      inputSchema: descriptor.inputSchema,
    },
    async (input: Record<string, unknown>) => {
      const validatedInput = descriptor.parse(input);
      const result = await descriptor.handler(validatedInput);
      return asMcpResult(result, descriptor.outputPolicy);
    },
  );
}

const transport = new StdioServerTransport();
await server.connect(transport);
