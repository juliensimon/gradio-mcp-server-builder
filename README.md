# Gradio MCP Server Builder

A CLI tool to automatically build MCP (Model Context Protocol) servers with Gradio from Python function files.

## Overview

This tool takes Python files containing functions decorated with `@mcp.tool()` and automatically generates:

- **MCP Server**: A complete MCP server that exposes your functions as tools
- **Gradio Interface**: A web-based UI (single interface or tabbed interface based on function count)
- **Test Client**: A test client with sample prompts for each function
- **Unit Tests**: Comprehensive unit tests for all functions
- **Documentation**: README and requirements files

## Features

- **AI-Powered Docstring Improvement**: Uses local Hugging Face models or OpenAI-compatible endpoints to improve function docstrings
- **Automatic Interface Generation**: Creates Gradio interfaces (single or tabbed) based on the number of functions
- **MPS Optimization**: Automatically optimizes for Mac with MPS when available
- **Flexible Configuration**: Support for various model endpoints and configuration options
- **Environment Variable Support**: Load configuration from `.env` files
- **Comprehensive Testing**: Generates unit tests and test clients

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gradio-mcp-server-builder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python main.py input/sample-input.py
```

This will:
- Parse the input file for functions with `@mcp.tool()` decorators
- Improve docstrings using the default local model
- Generate a complete MCP server with Gradio interface
- Create test files and documentation

### Advanced Usage

```bash
python main.py input/file1.py input/file2.py \
    --share \
    --model-endpoint http://localhost:8000 \
    --preserve-docstrings \
    --local-model custom-model \
    --output-dir custom-output \
    --env-file .env
```

### Command Line Options

- `input_files`: One or more Python files containing MCP functions
- `--share`: Enable Gradio sharing for public access
- `--model-endpoint`: Use an OpenAI-compatible model endpoint instead of local model
- `--preserve-docstrings`: Keep original docstrings (default: improve them)
- `--local-model`: Specify local Hugging Face model (default: HuggingFaceTB/SmolLM3-3B)
- `--output-dir`: Output directory for generated files (default: output)
- `--env-file`: Path to .env file for parameter passing

## Input File Format

Your input files should contain functions decorated with `@mcp.tool()`:

```python
@mcp.tool()
def add_floats(a: float, b: float) -> float:
    """
    Add two floating point numbers.
    
    Args:
        a: First floating point number
        b: Second floating point number
        
    Returns:
        The sum of a and b
    """
    return a + b

@mcp.tool()
def multiply_floats(a: float, b: float) -> float:
    """Multiply two floating point numbers."""
    return a * b
```

## Output Structure

The tool generates the following structure:

```
output/
├── server/           # MCP server files
│   ├── gradio_server.py
│   └── __init__.py
├── client/           # MCP client
│   └── mcp_client.py
├── README.md         # Generated documentation
└── requirements.txt  # Python dependencies
```

## Running the Generated Server

1. Navigate to the output directory:
```bash
cd output
```

2. Install the generated requirements:
```bash
pip install -r requirements.txt
```

3. Run the MCP server:
```bash
python server/mcp_server.py
```

4. Run the Gradio interface:
```bash
python server/gradio_interface.py
```

## Testing

### Run the CLI tool tests:
```bash
pytest tests/
```

### Test the generated client:
```bash
cd output
python client/test_client.py
```

## Configuration

### Environment Variables

Create a `.env` file to configure the tool:

```env
# Model configuration
OPENAI_API_KEY=your-api-key
MODEL_ENDPOINT=http://localhost:8000
LOCAL_MODEL=custom-model

# Gradio configuration
GRADIO_SHARE=true

# Output configuration
OUTPUT_DIR=custom-output
```

### Model Options

**Local Models**: The tool supports local Hugging Face models for docstring improvement. Default is `HuggingFaceTB/SmolLM3-3B`.

**OpenAI-Compatible Endpoints**: You can use any OpenAI-compatible API endpoint by setting the `--model-endpoint` parameter.

**MPS Optimization**: On Mac with MPS support, the tool automatically optimizes inference performance.

## Examples

### Single Function
If your input file has one function, a simple Gradio interface is created.

### Multiple Functions
If your input file has multiple functions, a tabbed interface is created with each function in its own tab.

### Sample Input
See `input/sample-input.py` for an example with arithmetic functions.

## Development

### Project Structure

```
gradio-mcp-server-builder/
├── source/           # Main source code
│   ├── cli.py       # CLI interface
│   ├── config.py    # Configuration management
│   ├── parser.py    # Python file parser
│   ├── docstring_improver.py  # AI docstring improvement
│   ├── gradio_generator.py    # Gradio interface generation
│   ├── builder.py   # Main builder orchestration
│   └── file_generators.py     # File generation components
├── tests/           # Unit tests
├── input/           # Sample input files
├── main.py          # Entry point
├── requirements.txt # Dependencies
└── README.md        # This file
```

### Adding New Features

1. **New File Generators**: Add new classes to `file_generators.py`
2. **New CLI Options**: Update `cli.py` and `config.py`
3. **New Model Support**: Extend `docstring_improver.py`

### Testing

The project uses pytest for testing. Run tests with:

```bash
pytest tests/ -v
```

For coverage:

```bash
pytest tests/ --cov=source --cov-report=html
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

**You are free to:**
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

**Under the following terms:**
- **Attribution** — You must give appropriate credit and indicate if changes were made
- **NonCommercial** — You may not use the material for commercial purposes

See the [LICENSE](LICENSE) file for the full license text, or visit https://creativecommons.org/licenses/by-nc/4.0/ for more details.

## Author

**Julien Simon** - [julien@julien.org](mailto:julien@julien.org)

## Acknowledgments

- Built with [Gradio](https://gradio.app/) for web interfaces
- Uses [MCP](https://modelcontextprotocol.io/) for tool communication
- Powered by Hugging Face Transformers for local AI inference 