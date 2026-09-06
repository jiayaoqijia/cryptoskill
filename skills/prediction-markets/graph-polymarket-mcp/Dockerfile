# Generated for Glama MCP server inspection
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY tsconfig.json ./
COPY src/ ./src/
RUN npm run build

# Run the MCP server
CMD ["node", "build/index.js"]
