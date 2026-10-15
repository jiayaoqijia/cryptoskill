#!/bin/bash

# Upload metadata to IPFS via Pinata API
# Usage: ./upload-to-ipfs.sh <path-to-json-file>

set -e

FILE="${1:-/root/genTech-agent-kit/erc-8004/agent-metadata-fixed.json}"

if [ ! -f "$FILE" ]; then
    echo "❌ File not found: $FILE"
    exit 1
fi

echo "📤 Uploading to IPFS..."
echo "   File: $FILE"
echo ""

# Check for PINATA_KEY
if [ -z "$PINATA_KEY" ] && [ -z "$PINATA_JWT" ]; then
    echo "⚠️  PINATA_KEY or PINATA_JWT not set in .env"
    echo ""
    echo "   Option 1: Set PINATA_JWT in .env (recommended)"
    echo "   Option 2: Set PINATA_KEY (older API key style)"
    echo ""
    echo "   Get JWT from: https://app.pinata.cloud/keys"
    echo ""
    echo "   Then run:"
    echo "     export PINATA_JWT='your-jwt-token'"
    echo "     $0 $FILE"
    exit 1
fi

# Use JWT if available (newer), fall back to API key
if [ -n "$PINATA_JWT" ]; then
    AUTH_HEADER="Authorization: Bearer $PINATA_JWT"
else
    AUTH_HEADER="pinata_api_key: $PINATA_KEY"
fi

# Upload via Pinata API
RESPONSE=$(curl -s -X POST "https://api.pinata.cloud/pinning/pinFileToIPFS" \
    -H "Content-Type: multipart/form-data" \
    -H "$AUTH_HEADER" \
    -F "file=@$FILE;type=application/json" \
    -F "pinataMetadata={\"name\":\"gentech-agent-metadata\",\"keyvalues\":{\"agent\":\"gentech-labs\"}}")

# Extract CID
CID=$(echo "$RESPONSE" | jq -r '.IpfsHash // .cid // empty')

if [ -z "$CID" ] || [ "$CID" = "null" ]; then
    echo "❌ Upload failed:"
    echo "$RESPONSE"
    exit 1
fi

echo "✅ Upload successful!"
echo ""
echo "   IPFS CID: $CID"
echo "   Gateway: https://gateway.pinata.cloud/ipfs/$CID"
echo "   IPFS URL: ipfs://$CID"
echo ""
echo "📝 Next: Update on-chain via setTokenURI()"
echo ""
echo "   Command (with your wallet):"
echo "   cast send <CONTRACT_ADDRESS> 'setTokenURI(uint256,string)' <TOKEN_ID> \"ipfs://$CID\" --rpc-url <RPC_URL>"