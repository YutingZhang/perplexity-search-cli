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
    """Search the web using the Perplexity AI API. Returns an answer with source citations.

    Args:
        query: The search query or question to ask.
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


if __name__ == "__main__":
    main()
