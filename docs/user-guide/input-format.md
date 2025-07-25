# Input File Format

Learn how to structure your Python files for the Gradio MCP Server Builder.

## File Structure

Your input files should be standard Python files with functions decorated with `@mcp.tool()`.

### Basic Structure

```python
# imports
import math
from typing import List, Dict

# constants (optional)
PI = math.pi
DEFAULT_TIMEOUT = 30

# helper functions (optional, not decorated)
def validate_input(value: float) -> bool:
    """Validate input value."""
    return value > 0

# MCP functions (required, decorated)
@mcp.tool()
def calculate_area(radius: float) -> float:
    """Calculate the area of a circle."""
    if not validate_input(radius):
        raise ValueError("Radius must be positive")
    return PI * radius ** 2
```

## Function Decorators

### Required: @mcp.tool()

Every function that should be exposed as an MCP tool must be decorated:

```python
@mcp.tool()
def my_function():
    pass
```

### Multiple Decorators

You can combine `@mcp.tool()` with other decorators:

```python
from functools import lru_cache

@mcp.tool()
@lru_cache(maxsize=128)
def expensive_calculation(n: int) -> int:
    """Perform expensive calculation with caching."""
    # ... calculation logic
    return result
```

## Function Signatures

### Parameter Types

The builder supports these parameter types:

#### Basic Types

```python
@mcp.tool()
def basic_types(
    text: str,
    number: int,
    decimal: float,
    flag: bool
) -> str:
    """Demonstrate basic types."""
    return f"Text: {text}, Number: {number}, Decimal: {decimal}, Flag: {flag}"
```

#### Complex Types

```python
from typing import List, Dict, Tuple, Optional, Union

@mcp.tool()
def complex_types(
    items: List[str],
    config: Dict[str, any],
    coordinates: Tuple[float, float],
    optional_value: Optional[str] = None,
    flexible_input: Union[int, float] = 0
) -> Dict:
    """Demonstrate complex types."""
    return {
        "items_count": len(items),
        "config_keys": list(config.keys()),
        "coordinates": coordinates,
        "optional": optional_value,
        "flexible": flexible_input
    }
```

#### Custom Types

```python
from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass
class User:
    name: str
    age: int

@mcp.tool()
def custom_types(
    status: Status,
    user: User
) -> Dict:
    """Demonstrate custom types."""
    return {
        "status": status.value,
        "user_name": user.name,
        "user_age": user.age
    }
```

### Default Values

You can provide default values for parameters:

```python
@mcp.tool()
def with_defaults(
    name: str,
    age: int = 25,
    city: str = "Unknown",
    active: bool = True
) -> Dict:
    """Function with default parameter values."""
    return {
        "name": name,
        "age": age,
        "city": city,
        "active": active
    }
```

### Variable Arguments

Support for `*args` and `**kwargs`:

```python
@mcp.tool()
def variable_args(
    base: float,
    *numbers: float,
    **options: Dict[str, any]
) -> Dict:
    """Function with variable arguments."""
    result = base
    for num in numbers:
        result += num
    
    return {
        "result": result,
        "count": len(numbers),
        "options": options
    }
```

## Return Types

### Single Return Values

```python
@mcp.tool()
def single_return(text: str) -> str:
    """Return a single string value."""
    return text.upper()
```

### Multiple Return Types

```python
from typing import Union, Tuple

@mcp.tool()
def multiple_returns(
    operation: str,
    a: float,
    b: float
) -> Union[float, str]:
    """Return different types based on operation."""
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
    else:
        return f"Unknown operation: {operation}"

@mcp.tool()
def tuple_return(x: float, y: float) -> Tuple[float, float]:
    """Return a tuple of values."""
    return (x * 2, y * 2)
```

### Complex Return Types

```python
from typing import List, Dict, Optional

@mcp.tool()
def complex_return(
    data: List[float]
) -> Dict[str, Union[float, List[float], None]]:
    """Return complex data structure."""
    if not data:
        return {"error": None, "stats": None, "data": []}
    
    return {
        "error": None,
        "stats": {
            "mean": sum(data) / len(data),
            "max": max(data),
            "min": min(data)
        },
        "data": sorted(data)
    }
```

## Docstrings

### Basic Docstring

```python
@mcp.tool()
def basic_docstring(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"
```

### Detailed Docstring

```python
@mcp.tool()
def detailed_docstring(
    radius: float,
    units: str = "meters"
) -> Dict[str, Union[float, str]]:
    """
    Calculate the area and circumference of a circle.
    
    This function takes a radius and calculates both the area and
    circumference of a circle with that radius.
    
    Args:
        radius: The radius of the circle (must be positive)
        units: The units of measurement (default: "meters")
        
    Returns:
        A dictionary containing:
            - area: The area of the circle
            - circumference: The circumference of the circle
            - units: The units used
            
    Raises:
        ValueError: If radius is negative or zero
        
    Example:
        >>> result = calculate_circle(5.0, "cm")
        >>> print(result)
        {'area': 78.54, 'circumference': 31.42, 'units': 'cm'}
    """
    if radius <= 0:
        raise ValueError("Radius must be positive")
    
    import math
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    
    return {
        "area": round(area, 2),
        "circumference": round(circumference, 2),
        "units": units
    }
```

## Error Handling

### Basic Error Handling

```python
@mcp.tool()
def safe_operation(a: float, b: float, operation: str) -> float:
    """Perform safe mathematical operations."""
    if operation == "divide" and b == 0:
        raise ValueError("Cannot divide by zero")
    
    if operation == "sqrt" and a < 0:
        raise ValueError("Cannot calculate square root of negative number")
    
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    elif operation == "sqrt":
        import math
        return math.sqrt(a)
    else:
        raise ValueError(f"Unknown operation: {operation}")
```

### Custom Exceptions

```python
class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class ProcessingError(Exception):
    """Custom exception for processing errors."""
    pass

@mcp.tool()
def validate_and_process(data: Dict) -> Dict:
    """Validate and process data with custom exceptions."""
    # Validation
    if "name" not in data:
        raise ValidationError("Name is required")
    
    if "age" in data and (data["age"] < 0 or data["age"] > 150):
        raise ValidationError("Age must be between 0 and 150")
    
    # Processing
    try:
        result = {
            "name": data["name"].upper(),
            "age": data.get("age", "Unknown"),
            "processed": True
        }
        return result
    except Exception as e:
        raise ProcessingError(f"Failed to process data: {str(e)}")
```

## Imports and Dependencies

### Standard Library Imports

```python
import math
import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
```

### Third-Party Imports

```python
import requests
import numpy as np
import pandas as pd
from PIL import Image
```

### Local Imports

```python
from .utils import helper_function
from .models import User, Product
from .constants import DEFAULT_CONFIG
```

## Constants and Configuration

### Module Constants

```python
# Mathematical constants
PI = 3.14159
E = 2.71828
GRAVITY = 9.81

# Configuration constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
SUPPORTED_FORMATS = ["json", "csv", "xml"]

# API endpoints
API_BASE_URL = "https://api.example.com"
VERSION = "v1"
```

### Configuration Objects

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    timeout: int = 30
    retries: int = 3
    formats: List[str] = None
    
    def __post_init__(self):
        if self.formats is None:
            self.formats = ["json", "csv"]

# Global configuration
DEFAULT_CONFIG = Config()
```

## Helper Functions

### Utility Functions

```python
def validate_email(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency."""
    return f"{currency} {amount:.2f}"

def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Safely divide a by b with default value."""
    try:
        return a / b
    except ZeroDivisionError:
        return default
```

### Data Processing Functions

```python
def clean_text(text: str) -> str:
    """Clean and normalize text."""
    return text.strip().lower()

def validate_numeric_range(value: float, min_val: float, max_val: float) -> bool:
    """Validate value is within range."""
    return min_val <= value <= max_val

def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between units."""
    # Conversion logic here
    conversions = {
        ("km", "miles"): 0.621371,
        ("kg", "lbs"): 2.20462,
        ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32
    }
    
    key = (from_unit, to_unit)
    if key in conversions:
        conversion = conversions[key]
        if callable(conversion):
            return conversion(value)
        else:
            return value * conversion
    else:
        raise ValueError(f"Unsupported conversion: {from_unit} to {to_unit}")
```

## Best Practices

### Function Naming

- Use descriptive, lowercase names with underscores
- Avoid abbreviations unless widely understood
- Be consistent with naming conventions

```python
# Good
@mcp.tool()
def calculate_monthly_payment(principal: float, rate: float, years: int) -> float:
    pass

# Avoid
@mcp.tool()
def calc_pmt(p: float, r: float, t: int) -> float:
    pass
```

### Parameter Design

- Use meaningful parameter names
- Provide default values when appropriate
- Use type hints for all parameters
- Keep parameter lists manageable (5-7 parameters max)

### Error Handling

- Validate inputs early
- Use specific exception types
- Provide helpful error messages
- Handle edge cases gracefully

### Documentation

- Write clear, concise docstrings
- Include parameter descriptions
- Document return values
- Provide usage examples
- Note any side effects or limitations

## Common Patterns

### Data Validation Pattern

```python
@mcp.tool()
def process_user_data(user_data: Dict) -> Dict:
    """Process user data with validation."""
    # Validate required fields
    required_fields = ["name", "email", "age"]
    for field in required_fields:
        if field not in user_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate data types and ranges
    if not isinstance(user_data["age"], int) or user_data["age"] < 0:
        raise ValueError("Age must be a positive integer")
    
    if not validate_email(user_data["email"]):
        raise ValueError("Invalid email format")
    
    # Process data
    return {
        "name": user_data["name"].title(),
        "email": user_data["email"].lower(),
        "age": user_data["age"],
        "status": "validated"
    }
```

### Configuration Pattern

```python
@mcp.tool()
def configure_service(
    service_name: str,
    config: Dict,
    environment: str = "production"
) -> Dict:
    """Configure a service with validation."""
    # Validate service name
    if not service_name or len(service_name) < 3:
        raise ValueError("Service name must be at least 3 characters")
    
    # Validate environment
    valid_environments = ["development", "staging", "production"]
    if environment not in valid_environments:
        raise ValueError(f"Environment must be one of: {valid_environments}")
    
    # Apply configuration
    base_config = DEFAULT_CONFIG.copy()
    base_config.update(config)
    
    return {
        "service": service_name,
        "environment": environment,
        "config": base_config,
        "status": "configured"
    }
```

## Next Steps

- **[Command Line Options](command-line.md)** - Complete CLI reference
- **[Code Parsing and Analysis](code-parsing.md)** - Understand how the tool analyzes your code
- **[Configuration Guide](../configuration/overview.md)** - Customize behavior 