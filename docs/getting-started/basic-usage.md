# Basic Usage

Learn the fundamentals of using the Gradio MCP Server Builder.

## Command Line Interface

The main command format is:

```bash
python main.py [input_files] [options]
```

### Basic Command

```bash
python main.py input/functions.py
```

### Multiple Input Files

```bash
python main.py input/file1.py input/file2.py input/file3.py
```

### With Options

```bash
python main.py input/functions.py \
    --share \
    --model-endpoint http://localhost:8000 \
    --preserve-docstrings \
    --local-model custom-model \
    --output-dir custom-output \
    --env-file .env
```

## Command Line Options

| Option                     | Description                                       | Default                    |
| -------------------------- | ------------------------------------------------- | -------------------------- |
| `input_files`              | One or more Python files containing MCP functions | Required                   |
| `--share`                  | Enable Gradio sharing for public access           | `False`                    |
| `--model-endpoint`         | Use an OpenAI-compatible model endpoint           | `None` (local model)       |
| `--preserve-docstrings`    | Keep original docstrings                          | `False` (improve them)     |
| `--local-model`            | Specify local Hugging Face model                  | `HuggingFaceTB/SmolLM3-3B` |
| `--output-dir`             | Output directory for generated files              | `output`                   |
| `--env-file`               | Path to .env file for parameter passing           | `None`                     |
| `--device`                 | Device for model inference (cpu/mps/cuda)         | `mps`                      |
| `--port`                   | Port for the generated server                     | `7860`                     |
| `--disable-sample-prompts` | Disable sample prompt generation                  | `False`                    |
| `--log-config`             | Path to logging configuration file                | `json/log_config.json`     |
| `--model-config`           | Path to model configuration file                  | `json/model_config.json`   |
| `--log-file`               | Path to log file                                  | `log/builds/output.log`    |

## Input File Format

Your input files should contain functions decorated with `@mcp.tool()`:

### Basic Function

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
```

### Function with Helper Functions

```python
import json
from pathlib import Path

# Helper function (not decorated)
def load_data(filename: str) -> dict:
    """Load data from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

@mcp.tool()
def process_data(filename: str, operation: str) -> dict:
    """Process data from a file with specified operation."""
    data = load_data(filename)
    # Process data based on operation
    return {"result": f"Processed {operation} on {len(data)} items"}
```

### Function with Constants

```python
import math

# Module constants
PI = math.pi
GRAVITY = 9.81

@mcp.tool()
def calculate_circle_area(radius: float) -> float:
    """Calculate the area of a circle."""
    return PI * radius ** 2

@mcp.tool()
def calculate_falling_distance(time: float) -> float:
    """Calculate distance fallen under gravity."""
    return 0.5 * GRAVITY * time ** 2
```

## Function Requirements

### Required Decorator

Every function must be decorated with `@mcp.tool()`:

```python
@mcp.tool()  # Required
def my_function():
    pass
```

### Type Hints

Use type hints for all parameters and return values:

```python
@mcp.tool()
def process_text(text: str, max_length: int) -> str:
    """Process text with length limit."""
    return text[:max_length]
```

### Docstrings

Include docstrings for all functions:

```python
@mcp.tool()
def calculate_bmi(weight: float, height: float) -> float:
    """
    Calculate Body Mass Index.

    Args:
        weight: Weight in kilograms
        height: Height in meters

    Returns:
        BMI value
    """
    return weight / (height ** 2)
```

## Supported Data Types

The builder supports these Python types:

- **Basic Types**: `str`, `int`, `float`, `bool`
- **Complex Types**: `list`, `dict`, `tuple`
- **Optional Types**: `Optional[str]`, `Union[int, float]`
- **Custom Types**: Any type that can be serialized to JSON

### Type Examples

```python
from typing import List, Dict, Optional, Union

@mcp.tool()
def process_list(items: List[str]) -> List[str]:
    """Process a list of strings."""
    return [item.upper() for item in items]

@mcp.tool()
def create_user(name: str, age: int, preferences: Optional[Dict] = None) -> Dict:
    """Create a user with optional preferences."""
    user = {"name": name, "age": age}
    if preferences:
        user["preferences"] = preferences
    return user

@mcp.tool()
def calculate_result(value: Union[int, float]) -> float:
    """Calculate result from numeric value."""
    return float(value) * 2.5
```

## Error Handling

### Basic Error Handling

```python
@mcp.tool()
def safe_divide(a: float, b: float) -> float:
    """Safely divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### Custom Exceptions

```python
class ValidationError(Exception):
    pass

@mcp.tool()
def validate_age(age: int) -> bool:
    """Validate age is reasonable."""
    if age < 0 or age > 150:
        raise ValidationError(f"Age {age} is not reasonable")
    return True
```

## Import Statements

The builder automatically handles imports:

```python
import math
import json
from pathlib import Path
from typing import List, Dict

@mcp.tool()
def complex_calculation(data: List[float]) -> Dict[str, float]:
    """Perform complex calculations."""
    return {
        "sum": sum(data),
        "mean": sum(data) / len(data),
        "max": max(data),
        "min": min(data)
    }
```

## Output Structure

The builder generates this structure:

```
output/
├── server/           # MCP server files
│   ├── gradio_server.py
│   └── __init__.py
├── client/           # MCP client
│   └── mcp_client.py
├── README.md         # Generated documentation
├── requirements.txt  # Python dependencies
└── config.json      # Configuration
```

## Running Generated Servers

### Start the Server

```bash
cd output
python server/gradio_server.py
```

### Access the Interface

- **Local**: <http://127.0.0.1:7860>
- **Network**: <http://0.0.0.0:7860> (if configured)
- **Public**: <https://xxx.gradio.live> (if using --share)

### Test the Client

```bash
cd output
python client/mcp_client.py
```

## Environment Variables

Create a `.env` file for configuration:

```env
# Model configuration
MODEL_ENDPOINT=http://localhost:8000
LOCAL_MODEL=custom-model
DEVICE=cuda

# Server configuration
PORT=8080
SHARE=true

# Logging
LOG_LEVEL=DEBUG
```

Then use:

```bash
python main.py input/functions.py --env-file .env
```

## Next Steps

- **[Input Format Guide](../user-guide/input-format.md)** - Detailed input
  specifications
- **[Command Line Options](../user-guide/command-line.md)** - Complete option
  reference
- **[Configuration Guide](../configuration/overview.md)** - Customize behavior
