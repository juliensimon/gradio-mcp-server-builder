# Gradio MCP Server Builder

> **Generate MCP servers with Gradio interfaces from Python functions**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-green.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![CI](https://github.com/juliensimon/gradio-mcp-server-builder/workflows/CI/badge.svg)](https://github.com/juliensimon/gradio-mcp-server-builder/actions/workflows/ci.yml)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Gradio](https://img.shields.io/badge/Gradio-Interface-orange.svg)](https://gradio.app/)
[![MCP](https://img.shields.io/badge/MCP-Server-purple.svg)](https://modelcontextprotocol.io/)

## Table of Contents

[![TOC](https://img.shields.io/badge/Table%20of%20Contents-%F0%9F%93%8B-blue.svg)](#table-of-contents)

- [What It Does](#what-it-does)
- [Example Functions](#example-functions)
- [Getting Started](#getting-started)
- [How It Works](#how-it-works)
- [Configuration Options](#configuration-options)
- [Limitations and Considerations](#limitations-and-considerations)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Documentation](#documentation)
- [Development Setup](#development-setup)
- [Contributing](#contributing)
- [License](#license)

You have Python functions that you'd like to expose as web services. Maybe
you've built utilities for data processing, calculations, or text analysis. You
could build a web interface from scratch, but that takes time and requires web
development skills.

This tool helps you create MCP (Model Context Protocol) servers with Gradio web
interfaces from your existing Python functions. It handles the boilerplate code
so you can focus on your core functionality.

## What It Does

The builder takes your Python functions and generates:

- An MCP server that exposes your functions as tools
- A Gradio web interface for testing and demonstration
- Documentation and example usage
- A client for testing the server

## Example Functions

Here are some typical use cases:

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

### Data Conversion

```python
@mcp.tool()
def convert_temperature(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

@mcp.tool()
def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a number as currency."""
    return f"{currency} {amount:.2f}"
```

## Getting Started

### Prerequisites

- Python 3.8+
- Basic familiarity with Python functions
- Virtual environment (recommended to avoid dependency conflicts)

### Installation

```bash
git clone https://github.com/juliensimon/gradio-mcp-server-builder.git
cd gradio-mcp-server-builder

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Create Your First Server

1. **Write your functions** in a file called `my_functions.py`:

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

2. **Generate the server**:

```bash
python main.py my_functions.py --preserve-docstrings
```

3. **Run the generated server**:

```bash
cd output && python server/gradio_server.py
```

4. **Test the interface** at <http://127.0.0.1:7860>

**Note**: When you're done working with the project, you can deactivate the
virtual environment with `deactivate`.

## How It Works

### Function Parsing

The tool parses your Python file and extracts functions decorated with
`@mcp.tool()`. It analyzes the function signatures, docstrings, and type hints
to understand what your functions do.

### Server Generation

It generates an MCP server that:

- Exposes your functions as callable tools
- Handles parameter validation
- Provides proper error handling
- Includes logging and monitoring

### Interface Creation

The Gradio interface is automatically created based on your function signatures:

- Input fields match your function parameters
- Output displays are formatted appropriately
- Multiple functions get a tabbed interface
- The interface is responsive and mobile-friendly

### Documentation

The tool generates:

- README with usage examples
- API documentation
- Sample client code
- Configuration files

## Configuration Options

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

# Load configuration from environment file
python main.py functions.py --env-file .env
```

## Limitations and Considerations

- **Function Complexity**: The tool works best with pure functions that have
  clear inputs and outputs
- **Dependencies**: Your functions' dependencies need to be available in the
  generated environment
- **Type Hints**: While not required, type hints help the tool generate better
  interfaces
- **Docstrings**: Good docstrings improve the generated documentation and AI
  enhancements
- **Error Handling**: The tool provides basic error handling, but complex error
  scenarios may need manual adjustment

## Project Structure

```
output/
├── server/           # MCP server implementation
│   ├── gradio_server.py
│   └── __init__.py
├── client/           # Test client
│   └── mcp_client.py
├── README.md         # Generated documentation
└── requirements.txt  # Dependencies
```

## Examples

Check the `input-samples/` directory for complete examples:

- `input-simple/` - Basic math and geometry functions
- `input-hello-world/` - Minimal example
- `input-advanced/` - Complex data processing tasks

## Documentation

- **[Installation Guide](docs/getting-started/installation.md)** - Detailed
  setup
- **[Quick Start Guide](docs/getting-started/quickstart.md)** - Step-by-step
  tutorial
- **[User Guide](docs/user-guide/input-format.md)** - Function format
  requirements
- **[Configuration Guide](docs/configuration/overview.md)** - Advanced
  configuration

### Local Documentation

```bash
./serve-docs.sh
```

Then visit <http://127.0.0.1:8001>

## Development Setup

For contributors and developers:

### Quick Setup

```bash
# Run the development setup script
./setup-dev.sh
```

### Manual Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Code Quality

The project uses pre-commit hooks to maintain code quality:

[![Black](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)
[![isort](https://img.shields.io/badge/Imports-isort-blue.svg)](https://pycqa.github.io/isort/)
[![flake8](https://img.shields.io/badge/Linting-flake8-yellow.svg)](https://flake8.pycqa.org/)
[![Prettier](https://img.shields.io/badge/Formatting-Prettier-orange.svg)](https://prettier.io/)
[![Markdownlint](https://img.shields.io/badge/Markdown-lint-green.svg)](https://github.com/DavidAnson/markdownlint)

- **Black**: Code formatting
- **isort**: Import sorting
- **autopep8**: Auto-fix PEP 8 violations
- **flake8**: Linting
- **prettier**: Format markdown, JSON, YAML
- **markdownlint**: Markdown linting

Run manually: `pre-commit run --all-files`

### Testing

The project has two test suites:

#### Fast Tests (CI)
```bash
# Run all fast tests (excludes slow tests)
python -m pytest tests/ -v --ignore=tests/slow/
```

#### Slow Tests (Local Development)
```bash
# Run all slow tests (server building, startup, E2E)
./run-slow-tests.sh

# Or run specific slow test files
python -m pytest tests/slow/test_input_samples.py -v
python -m pytest tests/slow/test_advanced_samples.py -v
python -m pytest tests/slow/test_input_samples_e2e.py -v
```

**Test Categories:**
- **Fast Tests**: Unit tests, parser tests, builder tests (run in CI)
- **Slow Tests**: Server building, startup verification, end-to-end tests (run locally)

See [tests/slow/README.md](tests/slow/README.md) for detailed information about slow tests.

### Auto-Fixing Everything

Pre-commit hooks automatically fix all code quality issues:

```bash
# Pre-commit handles everything automatically on every commit
git add .
git commit -m "Your changes"  # All auto-fixing happens here

# Or run manually
pre-commit run --all-files
```

**Auto-fixing tools configured:**

- **Python**: Black, isort, autopep8, autoflake
- **Markdown**: mdformat, prettier, markdownlint
- **General**: trailing whitespace, end-of-file fixes
- **Other**: JSON, YAML formatting with prettier

## Contributing

We welcome contributions. Please check the existing issues and discussions
before submitting changes.

**Before submitting a pull request:**

1. Set up the development environment
1. Ensure all pre-commit hooks pass
1. Add tests for new functionality
1. Update documentation as needed

## License

This project is licensed under CC BY-NC 4.0. You're free to use it for personal
and educational projects, but commercial use requires permission.

---

**Next Steps**: Start with the
[Quick Start Guide](docs/getting-started/quickstart.md) to build your first
server.
# CI Test
