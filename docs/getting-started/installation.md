# Installation

Get the Gradio MCP Server Builder up and running on your system.

## Prerequisites

Before installing the Gradio MCP Server Builder, ensure you have **Python 3.8+** installed on your system. The tool is built with modern Python features and requires a recent Python version. You'll also need **Git** for cloning the repository and **pip** for installing Python packages.

### System Requirements

**macOS** - Version 10.15+ (Catalina) is required for MPS support, which provides accelerated performance on Apple Silicon Macs.

**Linux** - Any modern distribution should work, with full support for CPU and CUDA acceleration.

**Windows** - Windows 10+ is supported, though with limited MPS support compared to macOS.

## Installation Methods

### Method 1: Clone and Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/juliensimon/gradio-mcp-server-builder.git
cd gradio-mcp-server-builder

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Install from PyPI (Future)

```bash
pip install gradio-mcp-server-builder
```

### Method 3: Development Installation

```bash
# Clone the repository
git clone https://github.com/juliensimon/gradio-mcp-server-builder.git
cd gradio-mcp-server-builder

# Install in development mode
pip install -e .
```

## Dependencies

The tool automatically installs these key dependencies when you run the installation commands. **Gradio** provides the web interface framework for your generated servers. **Transformers** enables Hugging Face model support for local AI processing. **PyTorch** powers local model inference with support for CPU, CUDA, and MPS acceleration.

**Requests** handles HTTP client functionality for API calls to external services. **Pydantic** provides data validation and serialization for your function parameters and return values. **Python-dotenv** manages environment variables for secure configuration handling.

## Optional Dependencies

For enhanced functionality, consider installing:

```bash
# For CUDA support (NVIDIA GPUs)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For additional model formats
pip install accelerate

# For development
pip install pytest black flake8
```

## Verification

Test your installation:

```bash
# Check if the tool is available
python main.py --help

# Run a quick test
python main.py input-samples/input-hello-world/hello_world.py --preserve-docstrings
```

## Configuration Files

The tool uses several configuration files that are created automatically during installation. The `json/model_config.json` file contains model behavior configuration including default models, performance settings, and API endpoints. The `json/log_config.json` file manages logging configuration with different verbosity levels and output formats. The `config/examples/` directory contains example configurations that demonstrate different setup scenarios and can be used as templates for custom configurations.

## Environment Setup

### macOS with MPS (Recommended)

If you're on macOS with Apple Silicon, the tool automatically detects and uses MPS:

```bash
# No additional setup required
python main.py input/functions.py
```

### CUDA Setup (NVIDIA GPUs)

For NVIDIA GPUs, install CUDA-enabled PyTorch:

```bash
# Install CUDA PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Use CUDA device
python main.py input/functions.py --device cuda
```

### CPU-Only Setup

For CPU-only systems:

```bash
# Use CPU device
python main.py input/functions.py --device cpu
```

## Troubleshooting

### Common Issues

**Import Error: No module named 'torch'**
```bash
pip install torch
```

**MPS not available on macOS**
- Ensure you're on macOS 12.3+ with Apple Silicon
- Update PyTorch: `pip install --upgrade torch`

**CUDA not detected**
- Install CUDA PyTorch: `pip install torch --index-url https://download.pytorch.org/whl/cu118`
- Verify CUDA installation: `nvidia-smi`

**Permission Denied**
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Getting Help

- Open an issue on [GitHub](https://github.com/juliensimon/gradio-mcp-server-builder/issues)
- Review the [Configuration Guide](../configuration/overview.md)

## Next Steps

Once installed, proceed to:

- **[Quick Start](quickstart.md)** - Build your first MCP server
- **[Basic Usage](basic-usage.md)** - Learn the fundamentals
- **[Configuration Guide](../configuration/overview.md)** - Customize the tool 