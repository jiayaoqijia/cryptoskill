# DID Document Format

## Agent Card JSON

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareAgent",
  "name": "Trading Agent",
  "description": "Automated trading agent",
  "version": "1.0.0",
  "capabilities": [
    "market-analysis",
    "order-execution",
    "risk-management"
  ],
  "tools": [
    {
      "name": "get_price",
      "description": "Get token price"
    }
  ],
  "endpoints": {
    "invoke": "https://agent.example.com/invoke",
    "status": "https://agent.example.com/status"
  }
}
```

## DID Document JSON

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/v1"
  ],
  "id": "did:spoon:agent123",
  "controller": "did:spoon:agent123",
  "verificationMethod": [
    {
      "id": "did:spoon:agent123#keys-1",
      "type": "EcdsaSecp256k1VerificationKey2019",
      "controller": "did:spoon:agent123",
      "publicKeyHex": "0x..."
    }
  ],
  "authentication": [
    "did:spoon:agent123#keys-1"
  ],
  "service": [
    {
      "id": "did:spoon:agent123#agent-service",
      "type": "AgentService",
      "serviceEndpoint": "https://agent.example.com"
    }
  ]
}
```

## DID Method Syntax

```
did:spoon:<network>:<agent_id>

Examples:
- did:spoon:mainnet:agent123
- did:spoon:neox:trading_bot
- did:spoon:testnet:research_agent
```
