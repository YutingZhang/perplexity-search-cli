# Perplexity Search CLI

A command line interface for interacting with the Perplexity AI API.

## Features

- Query the Perplexity API from command line
- Accepts input from arguments or stdin
- Supports API key from environment variable or command line
- Source citations with inline cross-references (enabled by default)
- Optionally save full JSON responses to file
- Clean, formatted output
- Claude Code MCP integration (PPWebSearch tool)

## Installation

Install directly from PyPI:
```bash
pip install perplexity-search-cli
```

With MCP server support (for Claude Code integration):
```bash
pip install 'perplexity-search-cli[mcp]'
```

### From source
```bash
git clone https://github.com/yourusername/perplexity-search-cli.git
cd perplexity-search-cli
pip install .            # CLI only
pip install '.[mcp]'    # with MCP server support
```

### Development install
```bash
git clone https://github.com/yourusername/perplexity-search-cli.git
cd perplexity-search-cli
pip install -e '.[mcp]'
```

## Usage

Basic query:
```bash
perplexity-search-cli -p "Your question" -k YOUR_API_KEY
```

Using environment variable:
```bash
export PPLX_API_KEY=YOUR_API_KEY
perplexity-search-cli -p "Your question"
```

Pipe input from stdin:
```bash
echo "Your question" | perplexity-search-cli -k YOUR_API_KEY
```

Save full JSON response:
```bash
perplexity-search-cli -p "Your question" -k YOUR_API_KEY -o response.json
```

## Options

```
  -h, --help            show help message
  -p PROMPT, --prompt PROMPT
                        Prompt to send to Perplexity API
  -k API_KEY, --api-key API_KEY
                        Perplexity API key (or set PPLX_API_KEY env var)
  -o OUTPUT, --output OUTPUT
                        Path to save full JSON response
  -n, --no-citations    Disable printing source citations
  --params PARAMS       Additional API parameters as JSON string
```

## Citations

By default, source URLs referenced in the response are printed below the content:

```
The speed of light is approximately 299,792 km/s [1] in a vacuum [2].

Sources:
  [1] https://en.wikipedia.org/wiki/Speed_of_light
  [2] https://physics.nist.gov/...
```

To disable citations:
```bash
perplexity-search-cli -p "Your question" --no-citations
```

## Example with Additional Parameters

```bash
perplexity-search-cli -p "Your question" -k YOUR_API_KEY \
  --params '{"temperature": 0.7, "max_tokens": 100}'
```

## Claude Code MCP Integration

This package can be registered as a Claude Code MCP server, exposing a `PPWebSearch` tool.

### Install with MCP support

```bash
pip install 'perplexity-search-cli[mcp]'
```

### Register with Claude Code

```bash
export PPLX_API_KEY=YOUR_API_KEY
./install-claude-mcp.sh
```

Or register manually:
```bash
claude mcp add --transport stdio perplexity-search \
  --env PPLX_API_KEY=YOUR_API_KEY \
  -- perplexity-mcp-server
```

Verify with `claude mcp list` or `/mcp` inside Claude Code.

## Requirements

- Python 3.6+
- requests
- mcp[cli] (optional, for Claude Code integration)

## Publishing New Versions

1. Update version in pyproject.toml
2. Commit changes
3. Create a new git tag:
```bash
git tag vX.Y.Z  # match version in pyproject.toml
git push origin vX.Y.Z
```

The GitHub Action will automatically:
- Build the package
- Publish to PyPI when tags are pushed
