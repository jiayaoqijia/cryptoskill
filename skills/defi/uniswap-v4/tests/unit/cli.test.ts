/**
 * Unit tests for CLI arg parser.
 */
import { describe, it, expect } from "vitest";
import { parseArgs } from "../../src/lib/cli.js";

describe("parseArgs", () => {
  it("parses --key value pairs", () => {
    const { flags } = parseArgs(["--chain", "base", "--rpc", "http://localhost"]);
    expect(flags["chain"]).toBe("base");
    expect(flags["rpc"]).toBe("http://localhost");
  });

  it("parses --key=value pairs", () => {
    const { flags } = parseArgs(["--chain=ethereum"]);
    expect(flags["chain"]).toBe("ethereum");
  });

  it("parses boolean flags", () => {
    const { booleans } = parseArgs(["--json", "--help"]);
    expect(booleans.has("json")).toBe(true);
    expect(booleans.has("help")).toBe(true);
  });

  it("parses positional arguments", () => {
    const { positional } = parseArgs(["0xABC", "--chain", "base", "0xDEF"]);
    expect(positional).toEqual(["0xABC", "0xDEF"]);
  });

  it("rejects --private-key flag (space-separated)", () => {
    expect(() => parseArgs(["--private-key", "0xDEAD"])).toThrow(
      "disabled for security"
    );
  });

  it("rejects --private-key=value flag (equals form)", () => {
    expect(() => parseArgs(["--private-key=0xDEADBEEF"])).toThrow(
      "disabled for security"
    );
  });

  it("handles mixed args", () => {
    const { flags, booleans } = parseArgs([
      "--token-in", "ETH",
      "--token-out", "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "--amount", "10000000000000000",
      "--json",
    ]);
    expect(flags["token-in"]).toBe("ETH");
    expect(flags["amount"]).toBe("10000000000000000");
    expect(booleans.has("json")).toBe(true);
  });
});
