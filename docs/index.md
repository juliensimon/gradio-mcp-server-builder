# Gradio MCP Server Builder

A powerful CLI tool to automatically build MCP (Model Context Protocol) servers
with Gradio from Python function files.

## What is MCP?

The Model Context Protocol (MCP) is a standard that enables AI assistants and
other tools to discover and use your functions. Think of it as a universal
language that lets AI systems understand what your code can do and how to use
it.

**Why MCP matters:**

**AI Integration** - Make your functions available to ChatGPT, Claude, and other
AI assistants. Your tools become part of the AI ecosystem, allowing users to
interact with your functionality through natural language.

**Tool Discovery** - AI systems can automatically find and understand your
tools. The protocol provides metadata that helps AI assistants determine when
and how to use your functions.

**Standard Protocol** - Works with any MCP-compatible client or framework.
You're not locked into a specific platform or implementation.

**No API Design** - Focus on your functions, not API endpoints. The protocol
handles the communication layer automatically.

## Overview

The Gradio MCP Server Builder transforms your Python functions into complete,
production-ready MCP servers with beautiful web interfaces. Simply decorate your
functions with `@mcp.tool()` and let the builder handle the rest.

This tool addresses a common challenge in AI development: the gap between having
useful Python functions and making them accessible through modern interfaces.
Instead of manually building web servers, writing API endpoints, and creating
user interfaces, the builder automates this entire process.

## Key Features

The builder provides several capabilities that streamline MCP server
development. It uses AI-powered docstring improvement to automatically enhance
your function documentation, making your tools more discoverable and
user-friendly. The automatic interface generation creates beautiful Gradio
interfaces that adapt based on your function count - single functions get
focused interfaces while multiple functions receive tabbed navigation.

Performance optimization is built-in, with automatic detection and utilization
of Metal Performance Shaders (MPS) on Mac systems. The tool supports flexible
configuration through various model endpoints, allowing you to use local Hugging
Face models or connect to OpenAI-compatible APIs. Environment integration is
seamless with `.env` file support for secure configuration management.

## What You Get

When you run the builder, it generates a complete package ready for deployment.
The output includes a fully functional MCP server that exposes your functions as
tools, a web-based Gradio interface for testing and demonstration, an
intelligent test client built with smolagents for natural language interaction,
and comprehensive documentation with requirements files.

The generated test client uses the smolagents library to provide intelligent
testing capabilities. It automatically discovers your server's tools,
understands natural language requests, and provides conversational responses.
This test client serves as both a powerful testing tool and a reference
implementation for integrating your server with other MCP-compatible
applications.

## Quick Start

Getting started with the Gradio MCP Server Builder is straightforward. First,
install the tool by cloning the repository and installing dependencies. Then
create your first MCP server by writing Python functions with the `@mcp.tool()`
decorator. Run the builder to generate your server, then start it and test
through the web interface.

The basic workflow involves creating input files containing your functions,
running the builder to generate the server, and then deploying or testing the
result. The builder handles all the complexity of MCP protocol implementation,
Gradio interface creation, and documentation generation.

## Example Input

Your input files should contain functions decorated with `@mcp.tool()`. The
builder supports various data types including basic types like strings and
numbers, complex types like lists and dictionaries, and custom types that can be
serialized to JSON.

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

The builder automatically creates interfaces that adapt to your function
structure. Single functions receive clean, focused interfaces with simple forms.
Multiple functions get tabbed interfaces for easy navigation between different
tools. All interfaces are responsive and work on both desktop and mobile
devices, with real-time testing capabilities that let you try your functions
directly in the browser.

## Advanced Features

Beyond basic server generation, the builder offers several advanced
capabilities. Local model support allows you to use Hugging Face models locally
for docstring improvement, while API integration connects to OpenAI-compatible
endpoints. Custom configuration options let you fine-tune model behavior and
logging, and environment variables provide secure configuration management. The
tool includes performance optimization with automatic device detection for CPU,
CUDA, and MPS.

The intelligent test client provides advanced testing and integration
capabilities. It automatically discovers server tools, understands natural
language requests, and provides conversational responses. This test client can
be customized for specific testing scenarios or extended to integrate with other
MCP-compatible frameworks and applications. The agent client guide provides
detailed information about its architecture, configuration, and usage patterns.

## Quick Reference

### For Beginners

**[Installation](getting-started/installation.md)** - Get the tool running on
your system with step-by-step instructions for different platforms and
environments.

**[Quick Start](getting-started/quickstart.md)** - Build your first server in 5
minutes with a guided tutorial that covers the complete workflow from function
creation to testing.

**[Input Format](user-guide/input-format.md)** - Learn how to write MCP
functions with proper decorators, type hints, and docstrings for optimal tool
discovery.

### For Advanced Users

**[Command Line Options](user-guide/command-line.md)** - Complete CLI reference
with all available options, configuration flags, and advanced usage patterns.

**[Configuration](configuration/overview.md)** - Customize behavior and models
with detailed configuration options for different deployment scenarios.

**[Testing Guide](user-guide/testing.md)** - Comprehensive testing strategies
including unit tests, integration tests, and end-to-end validation.

**[Agent Client](user-guide/agent-client.md)** - Understand the intelligent test
client architecture and learn how to customize it for your specific needs.

### Common Commands

```bash
# Basic build
python main.py functions.py

# With AI docstring improvement
python main.py functions.py --local-model "HuggingFaceTB/SmolLM3-3B"

# Custom output and port
python main.py functions.py --output-dir my_server --port 8080

# Preserve original docstrings
python main.py functions.py --preserve-docstrings
```

## Documentation

The complete documentation provides detailed guides for every aspect of the
tool. The installation guide covers setup across different platforms and
environments. The quick start guide walks you through building your first MCP
server in under five minutes. User guides explain input formats, command line
options, testing procedures, and best practices. Configuration guides detail how
to customize model behavior, logging, and server settings.

## Contributing

We welcome contributions from the community. The project is open source and
available on GitHub, where you can report issues, suggest features, or submit
pull requests. The codebase is well-structured and documented, making it
accessible for new contributors.

## License

This project is licensed under CC BY-NC 4.0. This license allows you to share
and adapt the material for non-commercial purposes, with appropriate attribution
required.

---

**Ready to build your first MCP server?** Start with the
[Quick Start Guide](getting-started/quickstart.md)!
