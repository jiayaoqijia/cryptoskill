#!/usr/bin/env node

import 'dotenv/config';
import { ZodError } from 'zod';
import { getConfig, isExecutionEnabled, isConfirmationRequired } from './env.js';
import { buildErrorResult, ExecutionDisabledError, ValidationError } from './errors.js';
import { budgetTracker } from './budgets.js';
import { confirmationStore } from './confirm.js';
import { runPipelineAndWait } from './pipeline.js';
import { out, exitWithError, getLogger } from './util.js';
import * as elsa from './elsaClient.js';
import {
  SearchTokenInputSchema,
  GetTokenPriceInputSchema,
  GetBalancesInputSchema,
  GetPortfolioInputSchema,
  AnalyzeWalletInputSchema,
  GetSwapQuoteInputSchema,
  ExecuteSwapDryRunInputSchema,
  ExecuteSwapConfirmedInputSchema,
  PipelineGetStatusInputSchema,
  PipelineSubmitTxHashInputSchema,
  PipelineRunAndWaitInputSchema,
  BudgetStatusInputSchema,
  GetLimitOrdersInputSchema,
  CreateLimitOrderInputSchema,
  CancelLimitOrderInputSchema,
  GetPerpPositionsInputSchema,
  OpenPerpPositionInputSchema,
  ClosePerpPositionInputSchema,
  GetTransactionHistoryInputSchema,
} from './types.js';
import type { ToolHandler, ToolRegistry, ToolResult, BudgetStatus } from './types.js';

// ============================================================================
// Tool Handlers
// ============================================================================

const MVP_TOOLS: ToolRegistry = {
  // -------------------------------------------------------------------------
  // A) elsa_search_token
  // -------------------------------------------------------------------------
  elsa_search_token: {
    validate: (args) => {
      const result = SearchTokenInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = SearchTokenInputSchema.parse(args);
      const result = await elsa.searchToken(input.query, input.limit);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // B) elsa_get_token_price
  // -------------------------------------------------------------------------
  elsa_get_token_price: {
    validate: (args) => {
      const result = GetTokenPriceInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = GetTokenPriceInputSchema.parse(args);
      const result = await elsa.getTokenPrice(input.token_address, input.chain);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // C) elsa_get_balances
  // -------------------------------------------------------------------------
  elsa_get_balances: {
    validate: (args) => {
      const result = GetBalancesInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = GetBalancesInputSchema.parse(args);
      const result = await elsa.getBalances(input.wallet_address);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // D) elsa_get_portfolio
  // -------------------------------------------------------------------------
  elsa_get_portfolio: {
    validate: (args) => {
      const result = GetPortfolioInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = GetPortfolioInputSchema.parse(args);
      const result = await elsa.getPortfolio(input.wallet_address);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // E) elsa_analyze_wallet
  // -------------------------------------------------------------------------
  elsa_analyze_wallet: {
    validate: (args) => {
      const result = AnalyzeWalletInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = AnalyzeWalletInputSchema.parse(args);
      const result = await elsa.analyzeWallet(input.wallet_address);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // F) elsa_get_swap_quote
  // -------------------------------------------------------------------------
  elsa_get_swap_quote: {
    validate: (args) => {
      const result = GetSwapQuoteInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = GetSwapQuoteInputSchema.parse(args);
      const result = await elsa.getSwapQuote(input);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // G) elsa_execute_swap_dry_run
  // -------------------------------------------------------------------------
  elsa_execute_swap_dry_run: {
    validate: (args) => {
      const result = ExecuteSwapDryRunInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = ExecuteSwapDryRunInputSchema.parse(args);

      // Always force dry_run=true
      const result = await elsa.executeSwap({
        ...input,
        dry_run: true,
      });

      const response: Record<string, unknown> = {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };

      // Issue confirmation token if enabled and response indicates valid swap plan
      if (isConfirmationRequired() && result.data.pipeline_id) {
        const confirmationToken = confirmationStore.issueToken(input);
        response.confirmation_token = confirmationToken;
        response.confirmation_expires_in_seconds = getConfig().ELSA_CONFIRMATION_TTL_SECONDS;
      }

      return response;
    },
  },

  // -------------------------------------------------------------------------
  // H) elsa_budget_status
  // -------------------------------------------------------------------------
  elsa_budget_status: {
    validate: (args) => {
      const result = BudgetStatusInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (_args) => {
      const status = budgetTracker.getStatus();
      return {
        ok: true,
        data: status,
      };
    },
  },

  // -------------------------------------------------------------------------
  // I) elsa_get_limit_orders
  // -------------------------------------------------------------------------
  elsa_get_limit_orders: {
    validate: (args) => {
      const result = GetLimitOrdersInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = GetLimitOrdersInputSchema.parse(args);
      const result = await elsa.getLimitOrders(input.wallet_address, input.chain);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // J) elsa_get_perp_positions
  // -------------------------------------------------------------------------
  elsa_get_perp_positions: {
    validate: (args) => {
      const result = GetPerpPositionsInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = GetPerpPositionsInputSchema.parse(args);
      const result = await elsa.getPerpPositions(input.wallet_address);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // K) elsa_get_transaction_history
  // -------------------------------------------------------------------------
  elsa_get_transaction_history: {
    validate: (args) => {
      const result = GetTransactionHistoryInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = GetTransactionHistoryInputSchema.parse(args);
      const result = await elsa.getTransactionHistory(input.wallet_address, input.chain, input.limit);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },
};

// ============================================================================
// Execution Tools (only registered if ELSA_ENABLE_EXECUTION_TOOLS=true)
// ============================================================================

const EXECUTION_TOOLS: ToolRegistry = {
  // -------------------------------------------------------------------------
  // I) elsa_execute_swap_confirmed
  // -------------------------------------------------------------------------
  elsa_execute_swap_confirmed: {
    validate: (args) => {
      const result = ExecuteSwapConfirmedInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = ExecuteSwapConfirmedInputSchema.parse(args);

      // Validate confirmation token if required
      confirmationStore.requireConfirmation(input.confirmation_token, {
        from_chain: input.from_chain,
        from_token: input.from_token,
        from_amount: input.from_amount,
        to_chain: input.to_chain,
        to_token: input.to_token,
        wallet_address: input.wallet_address,
        slippage: input.slippage,
      });

      const result = await elsa.executeSwap({
        from_chain: input.from_chain,
        from_token: input.from_token,
        from_amount: input.from_amount,
        to_chain: input.to_chain,
        to_token: input.to_token,
        wallet_address: input.wallet_address,
        slippage: input.slippage,
        dry_run: false,
      });

      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // J) elsa_pipeline_get_status
  // -------------------------------------------------------------------------
  elsa_pipeline_get_status: {
    validate: (args) => {
      const result = PipelineGetStatusInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = PipelineGetStatusInputSchema.parse(args);
      const result = await elsa.getPipelineStatus(input.pipeline_id);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // K) elsa_pipeline_submit_tx_hash
  // -------------------------------------------------------------------------
  elsa_pipeline_submit_tx_hash: {
    validate: (args) => {
      const result = PipelineSubmitTxHashInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = PipelineSubmitTxHashInputSchema.parse(args);
      const result = await elsa.submitTransactionHash(input.task_id, input.tx_hash);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // L) elsa_pipeline_run_and_wait
  // -------------------------------------------------------------------------
  elsa_pipeline_run_and_wait: {
    validate: (args) => {
      const result = PipelineRunAndWaitInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = PipelineRunAndWaitInputSchema.parse(args);
      return runPipelineAndWait(input);
    },
  },

  // -------------------------------------------------------------------------
  // M) elsa_create_limit_order
  // -------------------------------------------------------------------------
  elsa_create_limit_order: {
    validate: (args) => {
      const result = CreateLimitOrderInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = CreateLimitOrderInputSchema.parse(args);
      const result = await elsa.createLimitOrder(input);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // N) elsa_cancel_limit_order
  // -------------------------------------------------------------------------
  elsa_cancel_limit_order: {
    validate: (args) => {
      const result = CancelLimitOrderInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = CancelLimitOrderInputSchema.parse(args);
      const result = await elsa.cancelLimitOrder(input.wallet_address, input.order_id, input.chain);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // O) elsa_open_perp_position
  // -------------------------------------------------------------------------
  elsa_open_perp_position: {
    validate: (args) => {
      const result = OpenPerpPositionInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = OpenPerpPositionInputSchema.parse(args);
      const result = await elsa.openPerpPosition(input);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },

  // -------------------------------------------------------------------------
  // P) elsa_close_perp_position
  // -------------------------------------------------------------------------
  elsa_close_perp_position: {
    validate: (args) => {
      const result = ClosePerpPositionInputSchema.safeParse(args);
      if (!result.success) {
        return result.error.errors.map((e) => `${e.path.join('.')}: ${e.message}`).join('; ');
      }
      return null;
    },
    run: async (args) => {
      const input = ClosePerpPositionInputSchema.parse(args);
      const result = await elsa.closePerpPosition(input);
      return {
        ok: true,
        data: result.data,
        billing: result.billing,
        meta: result.meta,
      };
    },
  },
};

// ============================================================================
// Build Final Tool Registry
// ============================================================================

function buildToolRegistry(): ToolRegistry {
  const tools: ToolRegistry = { ...MVP_TOOLS };

  if (isExecutionEnabled()) {
    Object.assign(tools, EXECUTION_TOOLS);
  }

  return tools;
}

// ============================================================================
// CLI Main
// ============================================================================

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    exitWithError('Usage: npx tsx scripts/index.ts <tool_name> [json_args]');
  }

  const toolName = args[0];
  const rawArgs = args[1] || '{}';

  // Initialize config (validates env)
  try {
    getConfig();
  } catch (error) {
    exitWithError(error instanceof Error ? error.message : String(error));
  }

  const logger = getLogger();
  const TOOLS = buildToolRegistry();

  // Check if tool exists
  if (!TOOLS[toolName]) {
    // Check if it's an execution tool that's disabled
    if (EXECUTION_TOOLS[toolName] && !isExecutionEnabled()) {
      out(buildErrorResult(new ExecutionDisabledError()));
      process.exit(1);
    }

    exitWithError(`Unknown tool: ${toolName}. Available: ${Object.keys(TOOLS).join(', ')}`);
  }

  // Parse arguments
  let parsedArgs: unknown;
  try {
    parsedArgs = JSON.parse(rawArgs);
  } catch (error) {
    out(buildErrorResult(new ValidationError('Invalid JSON arguments', { raw: rawArgs })));
    process.exit(1);
  }

  const tool = TOOLS[toolName];

  // Validate arguments
  const validationError = tool.validate(parsedArgs);
  if (validationError) {
    out(buildErrorResult(new ValidationError(validationError)));
    process.exit(1);
  }

  // Execute tool
  try {
    logger.debug({ tool: toolName, args: parsedArgs }, 'Executing tool');
    const result = await tool.run(parsedArgs);
    out(result);
  } catch (error) {
    logger.error({ tool: toolName, error }, 'Tool execution failed');
    out(buildErrorResult(error));
    process.exit(1);
  }
}

main();
