# Gradio MCP Server Builder

A powerful CLI tool to automatically build MCP (Model Context Protocol) servers with Gradio from Python function files.

## 🚀 Overview

The Gradio MCP Server Builder transforms your Python functions into complete, production-ready MCP servers with beautiful web interfaces. Simply decorate your functions with `@mcp.tool()` and let the builder handle the rest.

## ✨ Key Features

- **🤖 AI-Powered Docstring Improvement**: Automatically enhance function documentation using local or cloud models
- **🎨 Automatic Interface Generation**: Creates beautiful Gradio interfaces (single or tabbed) based on your functions
- **⚡ MPS Optimization**: Optimized for Mac with Metal Performance Shaders
- **🔧 Flexible Configuration**: Support for various model endpoints and extensive customization
- **🌍 Environment Integration**: Seamless `.env` file support for configuration
- **📦 Complete Package**: Generates server, client, and documentation in one command

## 🎯 What You Get

```bash
python main.py input/functions.py
```

**Output:**
- ✅ **MCP Server**: Complete server exposing your functions as tools
- ✅ **Gradio Interface**: Web-based UI for testing and demonstration
- ✅ **MCP Client**: Ready-to-use client with sample prompts
- ✅ **Documentation**: Comprehensive README and requirements

## 🏃‍♂️ Quick Start

```bash
# Install
pip install -r requirements.txt

# Create your first MCP server
python main.py input-samples/input-hello-world/hello_world.py

# Run the generated server
cd output && python server/gradio_server.py
```

## 📖 Documentation

- **[Installation](getting-started/installation.md)** - Get up and running
- **[Quick Start](getting-started/quickstart.md)** - Your first MCP server
- **[User Guide](user-guide/input-format.md)** - Learn the basics
- **[Configuration](configuration/overview.md)** - Customize behavior


## 🔧 Example Input

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

## 🎨 Generated Interface

The builder automatically creates a beautiful Gradio interface:

- **Single Function**: Clean, focused interface
- **Multiple Functions**: Tabbed interface for easy navigation
- **Responsive Design**: Works on desktop and mobile
- **Real-time Testing**: Try your functions directly in the browser

## 🚀 Advanced Features

- **Local Model Support**: Use Hugging Face models locally
- **API Integration**: Connect to OpenAI-compatible endpoints
- **Custom Configuration**: Fine-tune model behavior and logging
- **Environment Variables**: Secure configuration management
- **Performance Optimization**: Automatic device detection and optimization

## 📚 Learn More

- **[Configuration Guide](configuration/overview.md)** - Customize every aspect

## 🤝 Contributing

We welcome contributions! See our [GitHub repository](https://github.com/julien/gradio-mcp-server-builder) for details.

## 📄 License

This project is licensed under CC BY-NC 4.0. See [LICENSE](../LICENSE) for details.

---

**Ready to build your first MCP server?** Start with the [Quick Start Guide](getting-started/quickstart.md)!
