FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .

CMD ["chainguard-mcp", "mcp"]
