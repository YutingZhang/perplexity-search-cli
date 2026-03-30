#!/usr/bin/env bash
# Install perplexity-search-cli as a Claude Code MCP server (PPWebSearch tool)
set -e

# Resolve the perplexity-mcp-server command path
MCP_BIN=$(command -v perplexity-mcp-server 2>/dev/null) || true

if [ -z "$MCP_BIN" ]; then
    echo "Error: perplexity-mcp-server not found."
    echo "Install it first:  pip install 'perplexity-search-cli[mcp]'"
    exit 1
fi

# Check for API key
if [ -z "$PPLX_API_KEY" ]; then
    read -rp "Enter your Perplexity API key: " PPLX_API_KEY
    if [ -z "$PPLX_API_KEY" ]; then
        echo "Error: API key is required."
        exit 1
    fi
fi

# Remove existing registration if present
claude mcp remove --scope user perplexity-search 2>/dev/null || true

echo "Registering perplexity-search MCP server with Claude Code (user scope)..."
claude mcp add --scope user --transport stdio perplexity-search \
    --env "PPLX_API_KEY=$PPLX_API_KEY" \
    -- "$MCP_BIN"

echo "Done! The PPWebSearch tool is now available in Claude Code."
echo "Run 'claude mcp list' to verify."
