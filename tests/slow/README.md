# Slow Tests

This directory contains tests that are excluded from CI due to their long runtime. These tests validate complex scenarios with multiple files and advanced functionality.

## Test Categories

### Input Samples Tests (`test_input_samples.py`)
Complete test suite for input samples including:
- **Basic Hello World**: Simple single-function examples
- **Simple Math/Geometry**: Multiple function examples
- **Server Startup**: Tests that verify servers start correctly
- **MCP Functionality**: Tests that verify MCP functions work
- **Client Generation**: Tests that verify client code generation

### Advanced Samples Tests (`test_advanced_samples.py`)
- **test_advanced_task_build**: Tests building advanced task management example
- **test_advanced_mcp_functions**: Tests MCP functions in advanced example
- **test_advanced_server_startup**: Tests advanced server startup and functionality
- **test_advanced_client_generation**: Tests advanced client generation

### End-to-End Tests (`test_input_samples_e2e.py`)
Complete end-to-end test suite including:
- **test_e2e_basic_hello_world**: End-to-end test for basic hello world example
- **test_e2e_simple_combined**: End-to-end test for simple combined example
- **test_e2e_advanced_tasks**: End-to-end test for advanced task management

## Running Slow Tests

### Run all slow tests:
```bash
pytest -c pytest-slow.ini
```

### Run specific test files:
```bash
# Run input samples tests only
pytest tests/slow/test_input_samples.py -v

# Run advanced samples tests only
pytest tests/slow/test_advanced_samples.py -v

# Run end-to-end tests only
pytest tests/slow/test_input_samples_e2e.py -v
```

### Run with longer timeout:
```bash
pytest tests/slow/ --timeout=900 -v
```

## Why These Tests Are Slow

1. **Server Building**: All tests involve building complete Gradio servers from input files
2. **Server Startup**: Tests verify that generated servers start correctly and remain running
3. **Multiple Input Files**: Some tests process 3+ input files simultaneously
4. **Complex Processing**: Advanced examples have complex function signatures and logic
5. **Model Inference**: Docstring improvement may involve AI model calls
6. **End-to-End Workflows**: Complete workflow testing from build to execution
7. **Client Generation**: Tests verify that client code is generated correctly
8. **MCP Functionality**: Tests verify that MCP functions work correctly in generated servers

## CI Exclusion

These tests are automatically excluded from CI runs via:
- `pytest.ini` configuration with `--ignore=tests/slow/`
- Separate `pytest-slow.ini` for running slow tests locally

## When to Run Slow Tests

- Before major releases
- When modifying advanced functionality
- When changing the build process
- During local development of advanced features
- Before merging changes that affect multiple file processing
