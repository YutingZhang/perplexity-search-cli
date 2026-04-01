#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import json
import re
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("perplexity-search")


@mcp.tool()
async def PPWebSearch(query: str) -> str:
    """Search the internet via Perplexity AI. Prefer this tool for any question or task that could benefit from web information, including but not limited to: current events, facts, documentation, APIs, libraries, prices, weather, news, people, companies, statistics, research, troubleshooting, or anything you are not fully certain about. When in doubt, search. Returns an answer with inline source citations and URLs.

    Args:
        query: The search query or question to look up on the web.
    """
    api_key = os.getenv("PPLX_API_KEY")
    if not api_key:
        return "Error: PPLX_API_KEY environment variable is not set."

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": query},
        ],
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        return f"API request failed: {e}"

    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
    citations = result.get("citations", []) or []

    if citations:
        referenced = set(int(m) for m in re.findall(r"\[(\d+)\]", content))
        used = [(i, citations[i - 1]) for i in sorted(referenced) if 1 <= i <= len(citations)]
        if used:
            content += "\n\nSources:"
            for idx, src_url in used:
                content += f"\n  [{idx}] {src_url}"

    return content


def main():
    mcp.run(transport="stdio")


def install_claude_mcp():
    import shutil
    import subprocess
    import getpass

    mcp_bin = shutil.which("perplexity-mcp-server")
    if not mcp_bin:
        print("Error: perplexity-mcp-server not found.", file=sys.stderr)
        print("Install it first:  pip install 'perplexity-search-cli[mcp]'", file=sys.stderr)
        sys.exit(1)

    claude_bin = shutil.which("claude")
    if not claude_bin:
        print("Error: claude CLI not found. Please install Claude Code first.", file=sys.stderr)
        sys.exit(1)

    api_key = os.getenv("PPLX_API_KEY")
    if not api_key:
        api_key = getpass.getpass("Enter your Perplexity API key: ").strip()
        if not api_key:
            print("Error: API key is required.", file=sys.stderr)
            sys.exit(1)

    # Remove existing registration if present
    subprocess.run(
        [claude_bin, "mcp", "remove", "--scope", "user", "perplexity-search"],
        capture_output=True,
    )

    print("Registering perplexity-search MCP server with Claude Code (user scope)...")
    result = subprocess.run(
        [
            claude_bin, "mcp", "add",
            "--scope", "user",
            "--transport", "stdio",
            "perplexity-search",
            "--env", f"PPLX_API_KEY={api_key}",
            "--", mcp_bin,
        ]
    )
    if result.returncode != 0:
        print("Error: failed to register MCP server.", file=sys.stderr)
        sys.exit(1)

    print("Done! The PPWebSearch tool is now available in Claude Code.")
    print("Run 'claude mcp list' to verify.")


if __name__ == "__main__":
    main()
