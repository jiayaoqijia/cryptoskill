#!/usr/bin/env node
import { readFile } from "node:fs/promises";
import { basename, resolve } from "node:path";
import { PinataSDK } from "pinata";
import { parseArgs, requiredEnv } from "./common.mjs";

async function main() {
  const args = parseArgs(process.argv);
  const filePath = args.file;
  if (!filePath) throw new Error("Missing --file path/to/agent-card.json");

  const pinataJwt = args.pinataJwt ?? requiredEnv("PINATA_JWT");
  const pinataGateway = args.pinataGateway ?? process.env.PINATA_GATEWAY;
  const pinata = new PinataSDK({
    pinataJwt,
    ...(pinataGateway ? { pinataGateway } : {}),
  });

  const resolved = resolve(filePath);
  const fileBuffer = await readFile(resolved);
  const file = new File([fileBuffer], basename(resolved), { type: "application/json" });
  const uploadResult = await pinata.upload.public.file(file);
  const cid = uploadResult.cid;
  const tokenUri = `ipfs://${cid}`;

  console.log(
    JSON.stringify(
      {
        status: "ok",
        cid,
        tokenUri,
        gatewayUrl: pinataGateway ? `https://${pinataGateway}/ipfs/${cid}` : null,
      },
      null,
      2
    )
  );
}

main().catch((err) => {
  const message = err instanceof Error ? err.message : String(err);
  console.error(`upload-pinata.mjs error: ${message}`);
  process.exit(1);
});
