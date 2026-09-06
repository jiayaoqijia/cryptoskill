import { describe, expect, test } from 'bun:test';
import * as fs from 'node:fs';
import * as path from 'node:path';
import {
  daoVoteArgsSchema,
  daoWithdrawArgsSchema,
  tokenApproveArgsSchema,
} from '../../src/mcp/schemas.js';

const ROOT = path.resolve(import.meta.dir, '..', '..');
const MCP_SERVER_PATH = path.join(ROOT, 'src', 'mcp', 'server.ts');
const MCP_SCHEMA_PATH = path.join(ROOT, 'src', 'mcp', 'schemas.ts');

describe('mcp schema quality', () => {
  test('high-frequency vote tools use explicit schema objects', () => {
    const source = fs.readFileSync(MCP_SERVER_PATH, 'utf-8');
    expect(source.includes('args: daoVoteArgsSchema')).toBeTrue();
    expect(source.includes('args: tokenApproveArgsSchema')).toBeTrue();
    expect(source.includes('args: daoWithdrawArgsSchema')).toBeTrue();
    expect(source.includes('args: bpVoteArgsSchema')).toBeTrue();
    expect(source.includes('args: bpChangeVoteArgsSchema')).toBeTrue();
    expect(source.includes('args: bpWithdrawArgsSchema')).toBeTrue();
    expect(source.includes('proposalType: networkProposalTypeSchema')).toBeTrue();
    expect(source.includes('action: networkProposalActionSchema')).toBeTrue();
  });

  test('send-mode tools include signer and signerContext schema', () => {
    const source = fs.readFileSync(MCP_SERVER_PATH, 'utf-8');
    expect(source.includes('signer: signerInputSchema')).toBeTrue();
    expect(source.includes('signerContext: signerInputSchema')).toBeTrue();
  });

  test('explicit schemas expose key fields for AI parameter construction', () => {
    const schemaSource = fs.readFileSync(MCP_SCHEMA_PATH, 'utf-8');
    expect(schemaSource.includes('export const daoVoteArgsSchema')).toBeTrue();
    expect(schemaSource.includes('proposalId: z.string().min(1).optional()')).toBeTrue();
    expect(schemaSource.includes('votingItemId: z.string().min(1).optional()')).toBeTrue();
    expect(schemaSource.includes('voteOption: z.number().int()')).toBeTrue();
    expect(schemaSource.includes('voteAmount: z.number().int().nonnegative()')).toBeTrue();
    expect(schemaSource.includes('export const tokenApproveArgsSchema')).toBeTrue();
    expect(schemaSource.includes('spender: z.string().min(1)')).toBeTrue();
    expect(schemaSource.includes('symbol: z.string().min(1)')).toBeTrue();
    expect(schemaSource.includes('amount: z.number().int().nonnegative()')).toBeTrue();
    expect(schemaSource.includes('withdrawAmount: z.number().int().positive()')).toBeTrue();
    expect(schemaSource.includes('export const bpVoteArgsSchema')).toBeTrue();
    expect(schemaSource.includes('candidatePubkey: z.string().min(1)')).toBeTrue();
    expect(schemaSource.includes('amount: z.number().positive()')).toBeTrue();
  });

  test('dao vote schema accepts proposalId alias and direct votingItemId', () => {
    expect(daoVoteArgsSchema.safeParse({
      proposalId: 'proposal-1',
      voteOption: 0,
      voteAmount: 100,
    }).success).toBeTrue();

    expect(daoVoteArgsSchema.safeParse({
      votingItemId: 'proposal-1',
      voteOption: 0,
      voteAmount: 100,
    }).success).toBeTrue();
  });

  test('dao vote schema rejects missing or conflicting target ids', () => {
    const missing = daoVoteArgsSchema.safeParse({
      voteOption: 0,
      voteAmount: 100,
    });
    const conflicting = daoVoteArgsSchema.safeParse({
      proposalId: 'proposal-1',
      votingItemId: 'proposal-2',
      voteOption: 0,
      voteAmount: 100,
    });

    expect(missing.success).toBeFalse();
    expect(conflicting.success).toBeFalse();
  });

  test('dao withdraw schema requires new dao-friendly fields and rejects voteRecordId', () => {
    expect(daoWithdrawArgsSchema.safeParse({
      daoId: 'dao-1',
      withdrawAmount: 100,
      proposalId: 'proposal-1',
    }).success).toBeTrue();

    expect(daoWithdrawArgsSchema.safeParse({
      daoId: 'dao-1',
      withdrawAmount: 100,
      votingItemIds: ['proposal-1'],
    }).success).toBeTrue();

    const deprecated = daoWithdrawArgsSchema.safeParse({
      daoId: 'dao-1',
      withdrawAmount: 100,
      proposalId: 'proposal-1',
      voteRecordId: 'vote-record-1',
    });
    const missingTarget = daoWithdrawArgsSchema.safeParse({
      daoId: 'dao-1',
      withdrawAmount: 100,
    });

    expect(deprecated.success).toBeFalse();
    expect(missingTarget.success).toBeFalse();
  });

  test('token approve schema accepts required fields', () => {
    expect(tokenApproveArgsSchema.safeParse({
      spender: 'spender-1',
      symbol: 'AIBOUNTY',
      amount: 200000000,
    }).success).toBeTrue();
  });
});
