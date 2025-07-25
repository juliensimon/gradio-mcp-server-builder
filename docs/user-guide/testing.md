# Testing Guide

The Gradio MCP Server Builder includes comprehensive testing capabilities to ensure reliability and functionality. This guide covers testing the builder itself, testing generated servers, and best practices for maintaining quality.

## Overview

Testing is a crucial part of the development workflow. The project uses pytest as the primary testing framework and includes several types of tests to ensure comprehensive coverage. Understanding how to run and interpret these tests helps you verify that your builds are working correctly and that any customizations maintain compatibility.

## Testing the Builder

The builder itself includes an extensive test suite that validates all components and workflows. These tests ensure that the tool works correctly across different scenarios and configurations.

### Prerequisites

Before running tests, ensure you have the required dependencies:

```bash
pip install -r requirements.txt
```

The requirements include pytest and related testing libraries:
- `pytest>=7.0.0` - The main testing framework
- `pytest-cov>=4.0.0` - For coverage reporting
- `pytest-mock>=3.10.0` - For mocking and patching
- `requests>=2.28.0` - For HTTP testing

### Basic Test Commands

Run the complete test suite with these commands:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=source

# Run tests and generate HTML coverage report
pytest --cov=source --cov-report=html
```

### Test Categories

The test suite is organized into several categories:

#### Unit Tests

Unit tests validate individual components in isolation:

```bash
# Test the main builder class
pytest tests/test_builder.py

# Test the configuration system
pytest tests/test_config.py

# Test the CLI interface
pytest tests/test_cli.py

# Test the parser functionality
pytest tests/test_parser.py

# Test the docstring improver
pytest tests/test_docstring_improver.py

# Test the Gradio generator
pytest tests/test_gradio_generator.py
```

#### Integration Tests

Integration tests validate end-to-end workflows:

```bash
# Test input sample processing
pytest tests/test_input_samples.py

# Test end-to-end server generation and execution
pytest tests/test_input_samples_e2e.py
```

#### Selective Testing

Run specific tests or test patterns:

```bash
# Run tests matching a specific pattern
pytest -k "test_builder"

# Run tests in a specific file
pytest tests/test_builder.py::TestGradioMCPBuilder

# Run a specific test method
pytest tests/test_builder.py::TestGradioMCPBuilder::test_build_basic_server

# Run tests excluding certain patterns
pytest -k "not slow"
```

### Coverage Analysis

Understanding test coverage helps identify untested code:

```bash
# Generate coverage report
pytest --cov=source --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=source --cov-report=html
open htmlcov/index.html
```

The coverage report shows:
- **Line Coverage**: Percentage of code lines executed
- **Branch Coverage**: Percentage of code branches taken
- **Missing Lines**: Specific lines that weren't tested

### Test Configuration

Tests use configuration files and environment variables:

```bash
# Run tests with specific environment
MCP_MODEL_ENDPOINT=http://localhost:8000 pytest

# Run tests with debug logging
LOG_LEVEL=DEBUG pytest -v
```

## Testing Generated Servers

After building a server, you should test it thoroughly to ensure it works as expected. The builder provides multiple testing approaches.

### Web Interface Testing

The generated Gradio interface provides immediate visual testing:

1. **Start the server**:
   ```bash
   cd output
   python server/gradio_server.py
   ```

2. **Open the web interface** in your browser (usually `http://127.0.0.1:7860`)

3. **Test each function**:
   - Enter test parameters
   - Verify the output is correct
   - Test edge cases and error conditions
   - Check that the interface is responsive

### MCP Client Testing

The smolagents-based client provides programmatic testing:

```bash
# Start the MCP client
cd output
python client/mcp_client.py
```

Test scenarios:
- **Natural language requests**: "Calculate the area of a circle with radius 5"
- **Parameter validation**: Test with invalid inputs
- **Error handling**: Verify graceful error responses
- **Tool discovery**: Ensure all functions are available

### Direct Function Testing

Import and test functions directly in Python:

```python
import sys
sys.path.append('output/server')
import gradio_server

# Test basic functionality
result = gradio_server.add_numbers(5, 3)
assert result == 8

# Test error conditions
try:
    gradio_server.divide(10, 0)
    assert False, "Should have raised an error"
except ValueError:
    pass  # Expected error
```

### End-to-End Testing

Test the complete server workflow:

```bash
# Build a test server
python main.py input-samples/input-simple/geometry.py

# Start the server
cd output
python server/gradio_server.py &

# Test via MCP client
python client/mcp_client.py

# Stop the server
pkill -f gradio_server.py
```

## Testing Best Practices

Follow these practices to ensure comprehensive testing:

### Test Input Files

Create test input files that cover various scenarios:

```python
# test_basic.py
@mcp.tool()
def simple_function(x: int) -> int:
    """A simple test function."""
    return x * 2

# test_complex.py
@mcp.tool()
def complex_function(data: dict, options: list = None) -> dict:
    """A complex function with multiple parameters."""
    if options is None:
        options = []
    return {"result": data, "options": options}
```

### Test Different Configurations

Test with various builder configurations:

```bash
# Test with different models
python main.py input.py --local-model "HuggingFaceTB/SmolLM3-3B"
python main.py input.py --model-endpoint "http://localhost:8000"

# Test with different output directories
python main.py input.py --output custom_output

# Test with docstring preservation
python main.py input.py --preserve-docstrings
```

### Test Error Conditions

Verify that the builder handles errors gracefully:

- **Invalid input files**: Files with syntax errors
- **Missing dependencies**: Functions that import unavailable modules
- **Invalid configurations**: Malformed JSON config files
- **Network issues**: Unreachable model endpoints

### Performance Testing

Test performance with larger inputs:

```bash
# Test with many functions
python main.py large_input.py

# Test with complex parameter types
python main.py complex_input.py

# Monitor resource usage during builds
time python main.py input.py
```

## Continuous Integration

The project includes automated testing through GitHub Actions:

### GitHub Actions Workflow

The CI pipeline runs on every pull request and commit:

1. **Install dependencies**
2. **Run linting checks**
3. **Run unit tests**
4. **Run integration tests**
5. **Generate coverage reports**
6. **Upload artifacts**

### Local CI Simulation

Simulate the CI environment locally:

```bash
# Install in a clean environment
python -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt

# Run the full test suite
pytest --cov=source --cov-report=xml
```

## Troubleshooting Tests

Common test issues and solutions:

### Test Failures

**Import Errors**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

**Permission Errors**: Check file permissions
```bash
chmod +x tests/
```

**Timeout Errors**: Increase timeout for slow tests
```bash
pytest --timeout=300
```

### Coverage Issues

**Low Coverage**: Add tests for uncovered code
```bash
pytest --cov=source --cov-report=term-missing
```

**Missing Dependencies**: Install development dependencies
```bash
pip install pytest-cov pytest-mock
```

### Environment Issues

**Path Problems**: Ensure Python path includes project root
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Version Conflicts**: Use virtual environments
```bash
python -m venv test_env
source test_env/bin/activate
```

## Advanced Testing

### Custom Test Fixtures

Create custom test fixtures for specific scenarios:

```python
# conftest.py
import pytest
import tempfile
import os

@pytest.fixture
def temp_input_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("""
@mcp.tool()
def test_function(x: int) -> int:
    return x * 2
""")
        yield f.name
    os.unlink(f.name)
```

### Mock Testing

Use mocks to test external dependencies:

```python
@pytest.fixture
def mock_model_endpoint(monkeypatch):
    def mock_response(*args, **kwargs):
        return {"choices": [{"message": {"content": "Mocked response"}}]}
    
    monkeypatch.setattr("requests.post", mock_response)
```

### Property-Based Testing

Use hypothesis for property-based testing:

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_add_numbers_property(a, b):
    result = add_numbers(a, b)
    assert result == a + b
```

## Conclusion

Comprehensive testing ensures that your Gradio MCP Server Builder installations work correctly and that generated servers meet your requirements. Regular testing helps catch issues early and maintains code quality.

For more information about specific test scenarios or troubleshooting, refer to the project's GitHub repository or create an issue for support. 