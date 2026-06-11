# Stage 1: Build the Node environment for the Phoenix MCP Server
FROM node:24-alpine AS mcp-build
WORKDIR /mcp
RUN npm install -g @arizeai/phoenix-mcp@latest

# Stage 2: Build the Python Environment
FROM python:3.11-slim
WORKDIR /agent

# Pull Node binaries and global modules from Stage 1 for the MCP protocol
COPY --from=mcp-build /usr/local/bin /usr/local/bin
COPY --from=mcp-build /usr/local/lib/node_modules /usr/local/lib/node_modules

# Install lightweight web runtime requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY ./src ./src

# Expose production port (Cloud Run default)
EXPOSE 8080

# Spin up both the Phoenix collector instance and the FastAPI Agent Gateway simultaneously
CMD ["sh", "-c", "python -m phoenix.server.main --port 6006 & uvicorn src.main:app --host 0.0.0.0 --port 8080"]