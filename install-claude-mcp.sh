#!/usr/bin/env bash
# Install perplexity-search-cli as a Claude Code MCP server (PPWebSearch tool)
set -e

if ! command -v perplexity-install-claude-mcp &>/dev/null; then
    echo "Error: perplexity-install-claude-mcp not found."
    echo "Install it first:  pip install 'perplexity-search-cli[mcp]'"
    exit 1
fi

perplexity-install-claude-mcp
