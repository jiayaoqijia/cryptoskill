import { createWalletClient, http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';
import { getConfig } from './env.js';
import { getPipelineStatus, submitTransactionHash } from './elsaClient.js';
import { PipelineTimeoutError, PipelineTaskError } from './errors.js';
import { getLogger, writeAuditLog, sleep, mapTransactionData, nowMs } from './util.js';
import type { PipelineRunResult, PipelineTask, TransactionData, MetaInfo } from './types.js';

// ============================================================================
// Trade Wallet Client
// ============================================================================

function getTradeWalletClient() {
  const config = getConfig();
  const privateKey = config.TRADE_PRIVATE_KEY ?? config.PAYMENT_PRIVATE_KEY;
  const account = privateKeyToAccount(privateKey as `0x${string}`);

  return createWalletClient({
    account,
    chain: base,
    transport: http(config.BASE_RPC_URL),
  });
}

// ============================================================================
// Pipeline Executor
// ============================================================================

export async function runPipelineAndWait(params: {
  pipeline_id: string;
  timeout_seconds: number;
  poll_interval_seconds: number;
  mode: 'local_signer' | 'external_signer';
}): Promise<PipelineRunResult> {
  const logger = getLogger();
  const startTime = nowMs();
  const timeoutMs = params.timeout_seconds * 1000;
  const pollIntervalMs = params.poll_interval_seconds * 1000;

  const txHashes: string[] = [];
  const taskResults: Array<{
    task_id: string;
    status: string;
    tx_hash?: string;
    tx_data?: TransactionData;
  }> = [];

  logger.info({ pipeline_id: params.pipeline_id, mode: params.mode }, 'Starting pipeline execution');

  while (true) {
    // Check timeout
    if (nowMs() - startTime > timeoutMs) {
      logger.warn({ pipeline_id: params.pipeline_id }, 'Pipeline timeout reached');
      throw new PipelineTimeoutError(
        'Pipeline execution timed out',
        {
          pipeline_id: params.pipeline_id,
          timeout_seconds: params.timeout_seconds,
          last_status: taskResults.length > 0 ? taskResults[taskResults.length - 1].status : 'unknown',
        }
      );
    }

    // Poll for status
    const statusResult = await getPipelineStatus(params.pipeline_id);
    const pipelineStatus = statusResult.data;

    logger.debug({ pipeline_id: params.pipeline_id, status: pipelineStatus.status }, 'Pipeline status');

    // Process tasks - API returns tasks as 'status' array
    const tasks = pipelineStatus.status || [];
    for (const task of tasks) {
      const existingResult = taskResults.find((r) => r.task_id === task.task_id);

      if (task.status === 'sign_pending') {
        // Task needs signing - use evm_tx_data from API
        const rawTxData = task.evm_tx_data || task.tx_data;

        if (params.mode === 'external_signer') {
          // Return for external signing
          if (!existingResult || existingResult.status !== 'sign_pending') {
            const txData = rawTxData ? mapTransactionData(rawTxData) : undefined;
            taskResults.push({
              task_id: task.task_id,
              status: 'sign_pending',
              tx_data: txData,
            });
          }
        } else {
          // Local signing
          if (!rawTxData) {
            throw new PipelineTaskError(
              'Task requires signing but no tx_data provided',
              { task_id: task.task_id, status: task.status }
            );
          }

          logger.info({ task_id: task.task_id }, 'Signing and broadcasting transaction');

          try {
            const txData = mapTransactionData(rawTxData);
            const walletClient = getTradeWalletClient();

            // Broadcast transaction
            const txHash = await walletClient.sendTransaction({
              to: txData.to as `0x${string}`,
              data: txData.data as `0x${string}`,
              value: txData.value ? BigInt(txData.value) : undefined,
              gas: txData.gas ? BigInt(txData.gas) : undefined,
              maxFeePerGas: txData.maxFeePerGas ? BigInt(txData.maxFeePerGas) : undefined,
              maxPriorityFeePerGas: txData.maxPriorityFeePerGas ? BigInt(txData.maxPriorityFeePerGas) : undefined,
            });

            logger.info({ task_id: task.task_id, tx_hash: txHash }, 'Transaction broadcast');
            txHashes.push(txHash);

            // Write audit log for signed transaction
            writeAuditLog({
              type: 'pipeline_tx_signed',
              pipeline_id: params.pipeline_id,
              task_id: task.task_id,
              tx_hash: txHash,
            });

            // Submit hash to Elsa
            await submitTransactionHash(task.task_id, txHash);

            // Update task result
            const idx = taskResults.findIndex((r) => r.task_id === task.task_id);
            if (idx >= 0) {
              taskResults[idx] = { task_id: task.task_id, status: 'submitted', tx_hash: txHash };
            } else {
              taskResults.push({ task_id: task.task_id, status: 'submitted', tx_hash: txHash });
            }
          } catch (error) {
            logger.error({ task_id: task.task_id, error }, 'Failed to sign/broadcast transaction');
            throw new PipelineTaskError(
              `Failed to sign transaction: ${error instanceof Error ? error.message : String(error)}`,
              { task_id: task.task_id, status: task.status }
            );
          }
        }
      } else if (task.status === 'success') {
        // Task completed
        const idx = taskResults.findIndex((r) => r.task_id === task.task_id);
        if (idx >= 0) {
          taskResults[idx].status = 'success';
          if (task.tx_hash) taskResults[idx].tx_hash = task.tx_hash;
        } else {
          taskResults.push({
            task_id: task.task_id,
            status: 'success',
            tx_hash: task.tx_hash,
          });
        }
        if (task.tx_hash && !txHashes.includes(task.tx_hash)) {
          txHashes.push(task.tx_hash);
        }
      } else if (task.status === 'failed' || task.status === 'abandoned') {
        throw new PipelineTaskError(
          `Task failed: ${task.description || task.status}`,
          { task_id: task.task_id, status: task.status, description: task.description }
        );
      }
    }

    // Check for external signer mode with pending tasks
    if (params.mode === 'external_signer') {
      const pendingTasks = taskResults.filter((t) => t.status === 'sign_pending');
      if (pendingTasks.length > 0) {
        const meta: MetaInfo = {
          latency_ms: nowMs() - startTime,
          endpoint: '/api/get_transaction_status',
          timestamp: new Date().toISOString(),
        };

        return {
          ok: true,
          status: 'needs_external_signature',
          pipeline_id: params.pipeline_id,
          tasks: taskResults,
          tx_hashes: txHashes,
          meta,
        };
      }
    }

    // Check for terminal states - derive from task statuses
    const allTasksComplete = tasks.length > 0 && tasks.every(t => t.status === 'success');
    const anyTaskFailed = tasks.some(t => t.status === 'failed' || t.status === 'abandoned');

    if (allTasksComplete) {
      const meta: MetaInfo = {
        latency_ms: nowMs() - startTime,
        endpoint: '/api/get_transaction_status',
        timestamp: new Date().toISOString(),
      };

      return {
        ok: true,
        status: 'success',
        pipeline_id: params.pipeline_id,
        tasks: taskResults,
        tx_hashes: txHashes,
        meta,
      };
    }

    if (anyTaskFailed) {
      const meta: MetaInfo = {
        latency_ms: nowMs() - startTime,
        endpoint: '/api/get_transaction_status',
        timestamp: new Date().toISOString(),
      };

      return {
        ok: true,
        status: 'failed',
        pipeline_id: params.pipeline_id,
        tasks: taskResults,
        tx_hashes: txHashes,
        meta,
      };
    }

    // Wait before next poll
    await sleep(pollIntervalMs);
  }
}
