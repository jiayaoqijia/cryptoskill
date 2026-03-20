import { describe, it, expect, vi } from "vitest";
import { type JsonRpcProvider } from "ethers";
import {
  makeProvider,
  fetchRpcChainId,
  assertRpcChain,
  assertHasBytecode,
} from "../../src/lib/provider.js";

// These tests are unit-level (no live RPC).
// We use a dummy RPC URL and rely on `staticNetwork: true` to avoid any network calls.

describe("provider helpers", () => {
  it("makeProvider commits to the configured chainId without contacting RPC", async () => {
    const provider = makeProvider("base", "http://127.0.0.1:0");
    const network = await provider.getNetwork();
    expect(Number(network.chainId)).toBe(8453);
    expect(network.name).toBe("base");
  });

  it("fetchRpcChainId parses hex chainId", async () => {
    const provider = {
      send: vi.fn(async () => "0x2105"),
    } as unknown as JsonRpcProvider;

    await expect(fetchRpcChainId(provider)).resolves.toBe(8453);
  });

  it("fetchRpcChainId throws on unexpected response type", async () => {
    const provider = {
      send: vi.fn(async () => 123),
    } as unknown as JsonRpcProvider;

    await expect(fetchRpcChainId(provider)).rejects.toThrow(/Unexpected eth_chainId response/);
  });

  it("assertRpcChain passes when chainId matches", async () => {
    const provider = {
      send: vi.fn(async () => "0x2105"),
    } as unknown as JsonRpcProvider;

    await expect(assertRpcChain(provider, "base")).resolves.toBeUndefined();
  });

  it("assertRpcChain throws on mismatch", async () => {
    const provider = {
      send: vi.fn(async () => "0x1"),
    } as unknown as JsonRpcProvider;

    await expect(assertRpcChain(provider, "base")).rejects.toThrow(/chainId mismatch/);
  });

  it("assertRpcChain wraps RPC errors", async () => {
    const provider = {
      send: vi.fn(async () => {
        throw new Error("boom");
      }),
    } as unknown as JsonRpcProvider;

    await expect(assertRpcChain(provider, "base")).rejects.toThrow(
      /RPC unreachable or invalid response: boom/
    );
  });

  it("assertHasBytecode passes when contract code exists", async () => {
    const provider = {
      getCode: vi.fn(async () => "0x1234"),
    } as unknown as JsonRpcProvider;

    await expect(
      assertHasBytecode(provider, "0x0000000000000000000000000000000000000001", "TestContract")
    ).resolves.toBeUndefined();
  });

  it("assertHasBytecode throws when address has no bytecode", async () => {
    const provider = {
      getCode: vi.fn(async () => "0x"),
    } as unknown as JsonRpcProvider;

    await expect(
      assertHasBytecode(provider, "0x0000000000000000000000000000000000000002", "TestContract")
    ).rejects.toThrow(/has no contract bytecode/);
  });
});
