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

The decorator tells the builder that this function should be exposed as an MCP tool. The type hints help the builder understand the expected input and output types, which it uses to generate appropriate interface components. The docstrings are crucial for MCP tool discovery—they help AI assistants and other systems understand what your tools do and when to use them.

### Step 2: Build the Server

Run the builder with your input file. The `--preserve-docstrings` flag keeps your original docstrings instead of improving them with AI, which speeds up the build process for this quick start. For production use, consider letting the AI improve your docstrings for better MCP tool discovery, but always review the results for accuracy.

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

The generated server provides multiple ways to test your functions. The web interface offers immediate visual feedback and is perfect for manual testing and demonstrations. The intelligent test client provides natural language interaction and is ideal for conversational testing and exploration. You can also import and use your functions directly in Python scripts for automated testing.

### Using the Test Client

The builder automatically generates an intelligent test client that uses the `smolagents` library to interact with your server. This test client provides natural language interaction, allowing you to test your functions through conversational requests.

#### What is smolagents?

`smolagents` is a lightweight library for creating intelligent agents that can interact with MCP servers. It provides a simple, intuitive interface for connecting to MCP servers, discovering available tools, and executing function calls. The generated client uses smolagents to create an intelligent agent that can:

- Connect to your MCP server automatically
- Discover all available tools and their capabilities
- Understand natural language requests and map them to appropriate tools
- Execute function calls with proper parameter handling
- Provide conversational responses with results
- Handle complex multi-step interactions

For a detailed explanation of how the agent client works, see the [Agent Client Guide](../user-guide/agent-client.md).

#### Running the Test Client

To use the test client, navigate to your output directory and run:

```bash
cd output
python client/mcp_client.py
```

The test client will start and launch a web-based chat interface. You can interact with it using natural language, asking questions like "Calculate the area of a circle with radius 5" or "What functions are available?" The client will automatically understand your requests and use the appropriate tools.

For example, if you have a function called `calculate_area` that takes a `radius` parameter, you can ask:
- "Calculate the area of a circle with radius 5"
- "What's the area of a circle with radius 10 meters?"
- "Compute the area for radius 3.14"

#### How the Client Works

The generated client creates an intelligent agent using smolagents and presents it through a Gradio chat interface. When you run the client:

1. **Connection**: It automatically connects to your running MCP server
2. **Tool Discovery**: It queries the server to discover all available tools and their metadata
3. **Agent Creation**: It initializes a local language model (SmolLM3-3B by default) to power the agent
4. **Chat Interface**: It launches a web-based chat interface where you can interact naturally
5. **Natural Language Processing**: The agent understands your requests and automatically selects appropriate tools
6. **Execution**: It executes the selected tools with proper parameters and returns conversational responses
7. **Error Handling**: It gracefully handles errors and provides helpful feedback

#### Client Features

The generated client includes several advanced features:

**Intelligent Agent**: The client creates an AI agent powered by a local language model that can understand natural language requests and automatically select appropriate tools.

**Natural Language Interface**: Instead of selecting from menus, you can simply chat with the agent using natural language. For example, "Calculate the area of a circle with radius 5" or "What's 10 plus 20?"

**Automatic Tool Selection**: The agent automatically determines which tool to use based on your request, eliminating the need to manually select functions.

**Conversational Responses**: The agent provides natural, conversational responses that include both the results and helpful explanations.

**Web-Based Interface**: A beautiful Gradio chat interface makes interaction intuitive and accessible from any browser.

**Local Model Support**: The agent runs entirely locally using the SmolLM3-3B model, ensuring privacy and fast response times.

#### Integration with Other Tools

The smolagents-based client is designed to work seamlessly with other MCP-compatible tools and frameworks. You can:

- Use it as a reference for integrating your server with other MCP clients
- Extend it to add custom functionality or testing capabilities
- Use it as a starting point for building more sophisticated MCP applications
- Share it with users who want to test your server programmatically
- Integrate it with other AI frameworks and tools that support MCP
- Use it as a foundation for building conversational AI applications

#### Customizing the Client

The generated client code is fully customizable. You can modify it to:

- Change the language model used by the agent (e.g., use a different Hugging Face model)
- Customize the agent's behavior and response style
- Add custom error handling or logging
- Implement additional testing scenarios
- Add batch processing capabilities
- Integrate with other testing frameworks
- Add custom parameter validation logic
- Modify the chat interface appearance and functionality

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

## Testing Your Build

The Gradio MCP Server Builder includes comprehensive testing capabilities to ensure your generated servers work correctly. The project uses pytest for testing and includes several types of tests.

### Running the Builder's Tests

To run the builder's own tests and ensure everything is working correctly:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=source

# Run specific test files
pytest tests/test_builder.py
pytest tests/test_input_samples.py

# Run tests matching a pattern
pytest -k "test_builder"
```

### Testing Generated Servers

After building a server, you can test it in several ways:

1. **Web Interface Testing**: Use the generated Gradio interface to test functions interactively
2. **Test Client Testing**: Use the intelligent test client for natural language interaction and conversational testing
3. **Direct Function Testing**: Import and test functions directly in Python scripts
4. **End-to-End Testing**: Run the complete server and test all functionality

### Test Coverage

The test suite covers:
- **Unit Tests**: Individual components like the builder, parser, and generators
- **Integration Tests**: End-to-end workflows from input files to generated servers
- **Input Sample Tests**: Testing with various input file formats and configurations
- **Configuration Tests**: Testing different configuration options and edge cases

### Continuous Integration

The project includes GitHub Actions workflows that automatically run tests on pull requests and commits. This ensures that all changes maintain compatibility and functionality.

## Next Steps

Now that you've successfully built your first server and understand how to test it, explore the detailed documentation to learn about input formats, configuration options, and advanced features. The input format guide explains how to structure your functions for optimal results. The configuration guide shows how to customize model behavior and logging. The command line reference provides complete details on all available options.

## Need Help?

If you encounter issues during the quick start, the input format guide provides detailed information about function requirements and best practices. For technical problems or feature requests, the project's GitHub repository includes issue tracking and community support. The documentation includes troubleshooting sections for common problems and configuration guides for advanced usage. 