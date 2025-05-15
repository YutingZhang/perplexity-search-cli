# Perplexity API CLI

A command line interface for interacting with the Perplexity AI API.

## Features

- Query the Perplexity API from command line
- Accepts input from arguments or stdin
- Supports API key from environment variable or command line
- Optionally save full JSON responses to file
- Clean, formatted output

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Basic query:
```bash
python3 perplexity_cli.py -p "Your question" -k YOUR_API_KEY
```

Using environment variable:
```bash
export PPLX_API_KEY=YOUR_API_KEY
python3 perplexity_cli.py -p "Your question"
```

Pipe input from stdin:
```bash
echo "Your question" | python3 perplexity_cli.py -k YOUR_API_KEY
```

Save full JSON response:
```bash
python3 perplexity_cli.py -p "Your question" -k YOUR_API_KEY -o response.json
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
```

## Requirements

- Python 3.6+
- requests package
