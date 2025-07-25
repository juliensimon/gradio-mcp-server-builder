# Quick Start

Build your first MCP server in under 5 minutes with this step-by-step guide.

## Your First MCP Server

This guide walks you through creating a simple MCP server that can add numbers and greet users. By the end, you'll understand the basic workflow and have a working server to experiment with.

### Step 1: Create Your Input File

Start by creating a file called `my_functions.py` with some basic functions. The key requirement is that each function you want to expose as an MCP tool must be decorated with `@mcp.tool()`.

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

The decorator tells the builder that this function should be exposed as an MCP tool. The type hints help the builder understand the expected input and output types, which it uses to generate appropriate interface components.

### Step 2: Build the Server

Run the builder with your input file. The `--preserve-docstrings` flag keeps your original docstrings instead of improving them with AI, which speeds up the build process for this quick start.

```bash
python main.py my_functions.py --preserve-docstrings
```

The builder will parse your functions, analyze their signatures, and generate all the necessary files for a complete MCP server. You'll see progress messages as it works through each step.

### Step 3: Run Your Server

Navigate to the output directory and start the generated server:

```bash
cd output
python server/gradio_server.py
```

The server will start and display a URL where you can access the web interface. By default, this is `http://127.0.0.1:7860`.

### Step 4: Test Your Server

Open your browser to the displayed URL and you'll see a clean interface with your functions. You can enter parameters and test each function directly in the browser. The interface automatically adapts to your function signatures, providing appropriate input fields for each parameter.

## What Just Happened?

The builder performed several key operations to transform your simple Python functions into a complete MCP server. First, it parsed your input file to identify functions with the `@mcp.tool()` decorator. It analyzed the function signatures to understand parameter types and return values.

Next, it generated a complete MCP server that implements the Model Context Protocol, exposing your functions as tools that can be called by MCP clients. It created a Gradio web interface that provides a user-friendly way to test your functions. The builder also generated an MCP client with sample prompts for each function, and comprehensive documentation including a README and requirements file.

## Generated Files

The builder creates a well-organized directory structure in your output folder. The `server/` directory contains the main MCP server implementation and the Gradio interface. The `client/` directory holds a test client that demonstrates how to use your functions programmatically. Additional files include documentation, dependency lists, and configuration files.

## Try Different Examples

Once you've successfully built your first server, experiment with different function types to see how the builder adapts. Single functions create focused interfaces, while multiple functions generate tabbed interfaces for easy navigation.

For a single function server, try creating a function that calculates the area of a circle:

```python
@mcp.tool()
def calculate_area(radius: float) -> float:
    """Calculate the area of a circle."""
    import math
    return math.pi * radius ** 2
```

For a multi-function server, create several mathematical operations:

```python
@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## Interface Types

The builder automatically determines the best interface layout based on your function count. Single functions receive clean, focused interfaces with simple forms that make testing straightforward. Multiple functions get tabbed interfaces that organize each function into its own section, making navigation intuitive even with many tools.

## Advanced Quick Start

As you become comfortable with the basic workflow, you can explore more advanced features. Try using different models for docstring improvement, enable sharing to create public URLs, or use custom output directories for organization.

With custom configuration, you can specify different local models, enable Gradio sharing for public access, or use custom output directories. Environment variables provide another way to configure the tool, allowing you to set model endpoints, device preferences, and other options through `.env` files.

## Testing Your Server

The generated server provides multiple ways to test your functions. The web interface offers immediate visual feedback and is perfect for manual testing and demonstrations. The MCP client allows programmatic testing and integration with other tools. You can also import and use your functions directly in Python scripts for automated testing.

### Using the MCP Client

The builder automatically generates an MCP client with sample prompts for each function. This client demonstrates how to programmatically interact with your server and provides examples of the types of requests you can make.

To use the MCP client, navigate to your output directory and run:

```bash
cd output
python client/mcp_client.py
```

The client will start and display a menu of available functions. You can select any function to see sample prompts that demonstrate how to use it. These sample prompts are generated automatically based on your function's name, parameters, and docstring.

For example, if you have a function called `calculate_area` that takes a `radius` parameter, the client might show prompts like:
- "Calculate the area of a circle with radius 5"
- "What's the area of a circle with radius 10 meters?"
- "Compute the area for radius 3.14"

### Sample Prompt Generation

The builder uses intelligent prompt generation to create realistic examples for each function. It analyzes your function's purpose, parameter names, and docstring to generate prompts that users might naturally ask.

The prompt generation considers:
- Function names and their semantic meaning
- Parameter names and their expected values
- Docstring descriptions and examples
- Common use cases for similar functions

This feature helps users understand how to interact with your tools and provides a starting point for integration with other MCP clients or AI assistants.

### Direct Function Import

You can also test your functions directly by importing them into Python scripts:

```python
import sys
sys.path.append('output/server')
import gradio_server

# Test your functions directly
result = gradio_server.add_numbers(5, 3)
print(f"5 + 3 = {result}")

greeting = gradio_server.greet_user("Alice")
print(greeting)
```

This approach is useful for automated testing, integration with other Python code, or when you need to call your functions programmatically.

## Next Steps

Now that you've successfully built your first server, explore the detailed documentation to learn about input formats, configuration options, and advanced features. The input format guide explains how to structure your functions for optimal results. The configuration guide shows how to customize model behavior and logging. The command line reference provides complete details on all available options.

## Need Help?

If you encounter issues during the quick start, the input format guide provides detailed information about function requirements and best practices. For technical problems or feature requests, the project's GitHub repository includes issue tracking and community support. The documentation includes troubleshooting sections for common problems and configuration guides for advanced usage. 