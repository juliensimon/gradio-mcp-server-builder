# Gradio MCP Server Builder

A powerful CLI tool to automatically build MCP (Model Context Protocol) servers with Gradio from Python function files.

## Overview

The Gradio MCP Server Builder transforms your Python functions into complete, production-ready MCP servers with beautiful web interfaces. Simply decorate your functions with `@mcp.tool()` and let the builder handle the rest.

This tool addresses a common challenge in AI development: the gap between having useful Python functions and making them accessible through modern interfaces. Instead of manually building web servers, writing API endpoints, and creating user interfaces, the builder automates this entire process.

## Key Features

The builder provides several capabilities that streamline MCP server development. It uses AI-powered docstring improvement to automatically enhance your function documentation, making your tools more discoverable and user-friendly. The automatic interface generation creates beautiful Gradio interfaces that adapt based on your function count - single functions get focused interfaces while multiple functions receive tabbed navigation.

Performance optimization is built-in, with automatic detection and utilization of Metal Performance Shaders (MPS) on Mac systems. The tool supports flexible configuration through various model endpoints, allowing you to use local Hugging Face models or connect to OpenAI-compatible APIs. Environment integration is seamless with `.env` file support for secure configuration management.

## What You Get

When you run the builder, it generates a complete package ready for deployment. The output includes a fully functional MCP server that exposes your functions as tools, a web-based Gradio interface for testing and demonstration, an MCP client with sample prompts for each function, and comprehensive documentation with requirements files.

## Quick Start

Getting started with the Gradio MCP Server Builder is straightforward. First, install the tool by cloning the repository and installing dependencies. Then create your first MCP server by writing Python functions with the `@mcp.tool()` decorator. Run the builder to generate your server, then start it and test through the web interface.

The basic workflow involves creating input files containing your functions, running the builder to generate the server, and then deploying or testing the result. The builder handles all the complexity of MCP protocol implementation, Gradio interface creation, and documentation generation.

## Example Input

Your input files should contain functions decorated with `@mcp.tool()`. The builder supports various data types including basic types like strings and numbers, complex types like lists and dictionaries, and custom types that can be serialized to JSON.

Here's a simple example:

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

## Generated Interface

The builder automatically creates interfaces that adapt to your function structure. Single functions receive clean, focused interfaces with simple forms. Multiple functions get tabbed interfaces for easy navigation between different tools. All interfaces are responsive and work on both desktop and mobile devices, with real-time testing capabilities that let you try your functions directly in the browser.

## Advanced Features

Beyond basic server generation, the builder offers several advanced capabilities. Local model support allows you to use Hugging Face models locally for docstring improvement, while API integration connects to OpenAI-compatible endpoints. Custom configuration options let you fine-tune model behavior and logging, and environment variables provide secure configuration management. The tool includes performance optimization with automatic device detection for CPU, CUDA, and MPS.

## Documentation

The complete documentation provides detailed guides for every aspect of the tool. The installation guide covers setup across different platforms and environments. The quick start guide walks you through building your first MCP server in under five minutes. User guides explain input formats, command line options, and best practices. Configuration guides detail how to customize model behavior, logging, and server settings.

## Contributing

We welcome contributions from the community. The project is open source and available on GitHub, where you can report issues, suggest features, or submit pull requests. The codebase is well-structured and documented, making it accessible for new contributors.

## License

This project is licensed under CC BY-NC 4.0. This license allows you to share and adapt the material for non-commercial purposes, with appropriate attribution required.

---

**Ready to build your first MCP server?** Start with the [Quick Start Guide](getting-started/quickstart.md)!
