# Gradio MCP Server Builder

A powerful CLI tool to automatically build MCP (Model Context Protocol) servers with Gradio from Python function files.

## 🚀 Overview

Transform your Python functions into complete, production-ready MCP servers with beautiful web interfaces. Simply decorate your functions with `@mcp.tool()` and let the builder handle the rest.

## ✨ Key Features

- **🤖 AI-Powered Docstring Improvement**: Automatically enhance function documentation
- **🎨 Automatic Interface Generation**: Creates beautiful Gradio interfaces
- **⚡ MPS Optimization**: Optimized for Mac with Metal Performance Shaders
- **🔧 Flexible Configuration**: Support for various model endpoints
- **📦 Complete Package**: Generates server, client, and documentation

## 🏃‍♂️ Quick Start

### Installation

```bash
git clone https://github.com/julien/gradio-mcp-server-builder.git
cd gradio-mcp-server-builder
pip install -r requirements.txt
```

### Your First MCP Server

1. **Create your functions** (`my_functions.py`):
```python
@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def greet_user(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"
```

2. **Build the server**:
```bash
python main.py my_functions.py --preserve-docstrings
```

3. **Run your server**:
```bash
cd output && python server/gradio_server.py
```

4. **Test it**: Open http://127.0.0.1:7860 in your browser!

## 📖 Documentation

📚 **Full Documentation** - Complete guides, examples, and API reference

### Local Development
```bash
# Serve documentation locally
./serve-docs.sh

# Or manually
mkdocs serve --dev-addr 127.0.0.1:8001
```

Then visit http://127.0.0.1:8001

- **[Installation Guide](docs/getting-started/installation.md)** - Get up and running
- **[Quick Start Guide](docs/getting-started/quickstart.md)** - Your first MCP server
- **[User Guide](docs/user-guide/input-format.md)** - Learn the basics
- **[Configuration Guide](docs/configuration/overview.md)** - Customize behavior
- **[Examples](docs/examples/basic-examples.md)** - See it in action

## 🎯 What You Get

```bash
python main.py input/functions.py
```

**Output:**
- ✅ **MCP Server**: Complete server exposing your functions as tools
- ✅ **Gradio Interface**: Web-based UI for testing and demonstration
- ✅ **MCP Client**: Ready-to-use client with sample prompts
- ✅ **Documentation**: Comprehensive README and requirements

## 🔧 Advanced Usage

```bash
# Use custom model
python main.py functions.py --local-model "microsoft/DialoGPT-medium"

# Enable sharing (public URL)
python main.py functions.py --share

# Use OpenAI-compatible endpoint
python main.py functions.py --model-endpoint http://localhost:8000

# Custom output directory
python main.py functions.py --output-dir my_server
```

## 🎨 Generated Interface

The builder automatically creates beautiful interfaces:

- **Single Function**: Clean, focused interface
- **Multiple Functions**: Tabbed interface for easy navigation
- **Responsive Design**: Works on desktop and mobile
- **Real-time Testing**: Try your functions directly in the browser

## 🚀 Advanced Features

- **Local Model Support**: Use Hugging Face models locally
- **API Integration**: Connect to OpenAI-compatible endpoints
- **Custom Configuration**: Fine-tune model behavior and logging
- **Environment Variables**: Secure configuration management
- **Performance Optimization**: Automatic device detection

## 📚 Learn More

- **[Configuration Guide](docs/configuration/overview.md)** - Customize every aspect
- **[Advanced Topics](docs/advanced/custom-models.md)** - Deep dive into features
- **[API Reference](docs/api/builder.md)** - Programmatic usage
- **[Examples](docs/examples/basic-examples.md)** - Real-world examples

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](docs/contributing/development.md) for details.

## 📄 License

This project is licensed under CC BY-NC 4.0. See [LICENSE](LICENSE) for details.

---

**Ready to build your first MCP server?** Start with the [Quick Start Guide](docs/getting-started/quickstart.md)! 