# MCP Server with Gradio Interface

This project provides an MCP (Model Context Protocol) server with a Gradio web
interface for 1 functions.

## Overview

This MCP server exposes the following functions as tools that can be called by
MCP clients:

### greet

**Signature:** `greet(name)`

**Description:** Generate a friendly greeting message.

Args: name: The name of the person to greet

Returns: A personalized greeting message

**Parameters:**

- `name` (str): Parameter description

**Example Prompts:**

- 1. Ask for an automated response with their name included.
- 2. Seek assistance in formulating an informal address or introduction.
- 3. Request help creating engaging opening phrases.
- 4. Need guidance on writing concise yet polite salutations.
- 5. Wish to create meaningful first interactions without prior knowledge about
     each other.

---

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the MCP server:

```bash
python server/mcp_server.py
```

3. Run the Gradio interface:

```bash
python server/gradio_interface.py
```

## Usage

### MCP Server

The MCP server can be used with any MCP client. The server exposes the following
tools:

| Function | Description | | -------- | ------------------------------------- |
| `greet` | Generate a friendly greeting message. |

Args: n... |

### Gradio Interface

The Gradio interface provides a web-based UI for testing the MCP functions:

- **Single Function**: If there's only one function, a simple interface is
  created
- **Multiple Functions**: If there are multiple functions, a tabbed interface is
  created

### Testing

Run the test client:

```bash
python client/mcp_client.py
```

## Project Structure

```
output/
├── server/           # MCP server files
│   ├── gradio_server.py
│   └── __init__.py
├── client/           # MCP client
│   └── mcp_client.py
├── README.md         # This file
└── requirements.txt  # Python dependencies
```

## Configuration

The server can be configured using the following options:

- `--share`: Enable Gradio sharing
- `--model-endpoint`: Use an OpenAI-compatible model endpoint
- `--preserve-docstrings`: Keep original docstrings
- `--local-model`: Specify local Hugging Face model
- `--env-file`: Load environment variables from .env file

## Development

This project was generated using the Gradio MCP Server Builder tool.

## License

This generated project inherits the CC BY-NC 4.0 license from
gradio-mcp-server-builder.

**You are free to:**

- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

**Under the following terms:**

- **Attribution** — You must give appropriate credit and indicate if changes
  were made
- **NonCommercial** — You may not use the material for commercial purposes

For more details, visit: <https://creativecommons.org/licenses/by-nc/4.0/>
