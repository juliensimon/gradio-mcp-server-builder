# Quick Start

Build your first MCP server in under 5 minutes!

## 🚀 Your First MCP Server

Let's create a simple MCP server that can add numbers and greet users.

### Step 1: Create Your Input File

Create a file called `my_functions.py`:

```python
@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def greet_user(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}! Welcome to your first MCP server."
```

### Step 2: Build the Server

Run the builder:

```bash
python main.py my_functions.py --preserve-docstrings
```

### Step 3: Run Your Server

```bash
cd output
python server/gradio_server.py
```

### Step 4: Test Your Server

Open your browser to `http://127.0.0.1:7860` and test your functions!

## 🎯 What Just Happened?

The builder automatically:

1. **Parsed** your Python functions
2. **Generated** a complete MCP server
3. **Created** a beautiful Gradio interface
4. **Built** an MCP client for testing
5. **Generated** documentation and requirements

## 📁 Generated Files

```
output/
├── server/
│   ├── gradio_server.py    # Your MCP server
│   └── __init__.py
├── client/
│   └── mcp_client.py       # Test client
├── README.md               # Documentation
├── requirements.txt        # Dependencies
└── config.json            # Configuration
```

## 🔧 Try Different Examples

### Single Function Server

```python
@mcp.tool()
def calculate_area(radius: float) -> float:
    """Calculate the area of a circle."""
    import math
    return math.pi * radius ** 2
```

### Multi-Function Server

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

## 🎨 Interface Types

### Single Function Interface
When you have one function, you get a clean, focused interface with a simple form.

### Multi-Function Interface
When you have multiple functions, you get a tabbed interface for easy navigation.

## 🚀 Advanced Quick Start

### With Custom Configuration

```bash
# Use a different model
python main.py my_functions.py --local-model "microsoft/DialoGPT-medium"

# Enable sharing (public URL)
python main.py my_functions.py --share

# Custom output directory
python main.py my_functions.py --output-dir my_server
```

### With Environment Variables

Create a `.env` file:

```env
MODEL_ENDPOINT=http://localhost:8000
LOCAL_MODEL=custom-model
DEVICE=cuda
```

Then run:

```bash
python main.py my_functions.py --env-file .env
```

## 🔍 Testing Your Server

### Via Gradio Interface
- Open the web interface
- Enter parameters
- Click "Submit"
- See results instantly

### Via MCP Client
```bash
cd output
python client/mcp_client.py
```

### Via Direct Import
```python
import sys
sys.path.append('output/server')
import gradio_server

result = gradio_server.add_numbers(5, 3)
print(result)  # 8.0
```

## 🎯 Next Steps

Now that you've built your first server:

- **[Basic Usage](basic-usage.md)** - Learn more about input formats
- **[Configuration Guide](../configuration/overview.md)** - Customize behavior

## 🆘 Need Help?

- Review the [Input Format Guide](../user-guide/input-format.md)
- Open an issue on [GitHub](https://github.com/julien/gradio-mcp-server-builder/issues)

---

**Congratulations!** You've successfully built your first MCP server. 🎉 