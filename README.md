# Gradio MCP Server Builder

> **Generate MCP servers with Gradio interfaces from Python functions**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-green.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![CI](https://github.com/juliensimon/gradio-mcp-server-builder/workflows/CI/badge.svg)](https://github.com/juliensimon/gradio-mcp-server-builder/actions/workflows/ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## Table of Contents

- [What It Does](#what-it-does)
- [Example Functions](#example-functions)
- [Getting Started](#getting-started)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Examples](#examples)
- [Documentation](#documentation)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

Transform your Python functions into MCP (Model Context Protocol) servers with Gradio web interfaces. No web development skills required - just focus on your core functionality.

## What It Does

The builder generates:

- **MCP Server** - Exposes your functions as callable tools
- **Gradio Interface** - Web UI for testing and demonstration
- **Documentation** - README, API docs, and examples
- **Test Client** - For testing the server

## Example Functions

### Math Functions

```python
@mcp.tool()
def calculate_circle_area(radius: float) -> float:
    """Calculate the area of a circle."""
    return 3.14159 * radius * radius

@mcp.tool()
def solve_quadratic(a: float, b: float, c: float) -> str:
    """Solve a quadratic equation ax² + bx + c = 0."""
    # Your math logic here
    return "Solution: x = ..."
```

### Text Processing

```python
@mcp.tool()
def count_words(text: str) -> int:
    """Count the number of words in a text."""
    return len(text.split())

@mcp.tool()
def analyze_sentiment(text: str) -> str:
    """Analyze the sentiment of a text (positive/negative/neutral)."""
    # Your analysis logic here
    return "This text is positive"
```

## Getting Started

### Visual Demo

Here's what the tool generates for you:

![Generating the server](images/1-generating-the-input-simple-server.webp)

*Building an MCP server from Python functions*

![Server UI](images/2-ui-of-the-input-simple-server.webp)

*The generated Gradio server interface*

![Client listing tools](images/3-ui-of-the-input-simple-client-listing-tools.webp)

*MCP client interface showing available tools*

![Client calling function](images/4-ui-of-the-input-simple-client-calling-a-function.webp)

*Using the client to call a function*

![Terminal output](images/5-terminal-output-of-the-input-simple-client-calling-a-function.webp)

*Terminal output showing the function execution*

### Quick Start

1. **Install dependencies:**
```bash
git clone https://github.com/juliensimon/gradio-mcp-server-builder.git
cd gradio-mcp-server-builder
pip install -r requirements.txt
```

2. **Write your functions:**
```python
@mcp.tool()
def greet_user(name: str) -> str:
    """Generate a friendly greeting message."""
    return f"Hello, {name}! Welcome to your first MCP server!"

@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
```

3. **Generate and run:**
```bash
python main.py my_functions.py --preserve-docstrings
cd output && python server/gradio_server.py
```

4. **Test at** <http://127.0.0.1:7860>

## How It Works

The tool transforms your Python functions into a complete MCP server with web interface:

![Server generation process](images/1-generating-the-input-simple-server.webp)

### Process

1. **Function Parsing** - Extracts `@mcp.tool()` decorated functions
2. **Server Generation** - Creates MCP server with validation and error handling
3. **Interface Creation** - Builds responsive Gradio UI based on function signatures
4. **Documentation** - Generates README, API docs, and examples

### Generated Interface

![Generated Gradio interface](images/2-ui-of-the-input-simple-server.webp)

- Input fields match your function parameters
- Multiple functions get a tabbed interface
- Responsive and mobile-friendly design

## Configuration

### Basic Options

```bash
# Preserve original docstrings (don't enhance with AI)
python main.py functions.py --preserve-docstrings

# Specify output directory
python main.py functions.py --output-dir my_server

# Enable Gradio sharing (creates public URL)
python main.py functions.py --share
```

### Model Configuration

```bash
# Use a local Hugging Face model
python main.py functions.py --local-model "microsoft/DialoGPT-medium"

# Use an OpenAI-compatible endpoint
python main.py functions.py --model-endpoint http://localhost:8000
```

## Examples

Check the `input-samples/` directory for complete examples:

- `input-simple/` - Basic math and geometry functions
- `input-hello-world/` - Minimal example
- `input-advanced/` - Complex data processing tasks

## Documentation

- **[Quick Start Guide](docs/getting-started/quickstart.md)** - Step-by-step tutorial
- **[User Guide](docs/user-guide/input-format.md)** - Function format requirements
- **[Configuration Guide](docs/configuration/overview.md)** - Advanced configuration

### Local Documentation

```bash
./serve-docs.sh
```

Then visit <http://127.0.0.1:8001>

## Development

### Setup

```bash
# Quick setup
./setup-dev.sh

# Or manual setup
pip install -r requirements-dev.txt
pre-commit install
```

### Testing

```bash
# Fast tests (CI)
python -m pytest tests/ -v --ignore=tests/slow/

# Slow tests (local development)
./run-slow-tests.sh
```

### Code Quality

The project uses pre-commit hooks for automatic code formatting and linting. See [tests/slow/README.md](tests/slow/README.md) for detailed testing information.

## Contributing

We welcome contributions! Please check existing issues before submitting changes.

**Before submitting a pull request:**
1. Set up the development environment
2. Ensure all pre-commit hooks pass
3. Add tests for new functionality
4. Update documentation as needed

## License

This project is licensed under CC BY-NC 4.0. You're free to use it for personal and educational projects, but commercial use requires permission.

---

**Next Steps**: Start with the [Quick Start Guide](docs/getting-started/quickstart.md) to build your first server.
