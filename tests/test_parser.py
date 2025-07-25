#!/usr/bin/env python3
"""
Unit tests for the MCPParser class.
"""

import sys
import tempfile
from pathlib import Path

import pytest

from source.parser import MCPFunction, MCPParser

# Add source to path
sys.path.insert(0, str(Path(__file__).parent.parent / "source"))


class TestMCPFunction:
    """Test the MCPFunction class."""

    def test_mcp_function_creation(self):
        """Test MCPFunction object creation."""

        def dummy_func():
            """Test function"""

        func = MCPFunction("test_func", dummy_func, "Test docstring", "()")
        assert func.name == "test_func"
        assert func.func == dummy_func
        assert func.docstring == "Test docstring"
        assert func.signature == "()"

    def test_mcp_function_repr(self):
        """Test MCPFunction string representation."""
        func = MCPFunction("test_func", None, "Test docstring", "(arg: str)")
        expected = "MCPFunction(name='test_func', signature='(arg: str)')"
        assert repr(func) == expected


class TestMCPParser:
    """Test the MCPParser class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = MCPParser()

    def test_parser_initialization(self):
        """Test parser initialization."""
        parser = MCPParser()
        assert hasattr(parser, "logger")
        assert parser.mcp_functions == []
        assert parser.other_functions == []
        assert parser.module_docstring == ""

    def test_parse_file_with_mcp_functions(self):
        """Test parsing a file with MCP functions."""
        # Create a temporary Python file with MCP functions
        test_code = '''
"""Test module docstring."""
import mcp

@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

def helper_function():
    """A helper function without MCP decorator."""
    return "helper"

CONSTANT_VALUE = 42
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(test_code)
            temp_file = Path(f.name)

        try:
            result = self.parser.parse_file(temp_file)

            # Check structure
            assert "mcp_functions" in result
            assert "helper_functions" in result
            assert "module_constants" in result
            assert "other_functions" in result
            assert "module_docstring" in result
            assert "module_imports" in result
            assert "content" in result

            # Check MCP functions
            mcp_funcs = result["mcp_functions"]
            assert len(mcp_funcs) == 2

            # Check greet function
            greet_func = next((f for f in mcp_funcs if f.name == "greet"), None)
            assert greet_func is not None
            assert greet_func.docstring == "Greet someone by name."
            assert "(name: str)" in greet_func.signature

            # Check add_numbers function
            add_func = next((f for f in mcp_funcs if f.name == "add_numbers"), None)
            assert add_func is not None
            assert add_func.docstring == "Add two numbers together."
            assert "(a: float, b: float)" in add_func.signature

            # Check module docstring
            assert result["module_docstring"] == "Test module docstring."

            # Check helper functions
            assert len(result["helper_functions"]) >= 1

            # Check constants
            assert len(result["module_constants"]) >= 1

        finally:
            temp_file.unlink()

    def test_parse_file_no_mcp_functions(self):
        """Test parsing a file with no MCP functions."""
        test_code = '''
"""Module without MCP functions."""

def regular_function():
    """A regular function."""
    return "test"

SOME_CONSTANT = "value"
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(test_code)
            temp_file = Path(f.name)

        try:
            result = self.parser.parse_file(temp_file)

            # Should have no MCP functions
            assert len(result["mcp_functions"]) == 0

            # But should have other content
            assert result["module_docstring"] == "Module without MCP functions."
            assert len(result["helper_functions"]) >= 1
            assert len(result["module_constants"]) >= 1

        finally:
            temp_file.unlink()

    def test_parse_file_with_imports(self):
        """Test parsing a file with various import styles."""
        test_code = '''
import mcp
import json
from typing import List, Dict
from pathlib import Path

@mcp.tool()
def test_func():
    """Test function."""
    return "test"
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(test_code)
            temp_file = Path(f.name)

        try:
            result = self.parser.parse_file(temp_file)

            imports = result["module_imports"]
            assert any("import mcp" in imp for imp in imports)
            assert any("import json" in imp for imp in imports)
            assert any("from typing import List, Dict" in imp for imp in imports)
            assert any("from pathlib import Path" in imp for imp in imports)

        finally:
            temp_file.unlink()

    def test_parse_file_with_complex_signature(self):
        """Test parsing functions with complex signatures."""
        test_code = '''
import mcp
from typing import List, Optional, Dict, Any

@mcp.tool()
def complex_function(
    arg1: str,
    arg2: int = 10,
    arg3: Optional[List[str]] = None,
    *args,
    **kwargs
) -> Dict[str, Any]:
    """A function with complex signature."""
    return {"result": "test"}
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(test_code)
            temp_file = Path(f.name)

        try:
            result = self.parser.parse_file(temp_file)

            mcp_funcs = result["mcp_functions"]
            assert len(mcp_funcs) == 1

            func = mcp_funcs[0]
            assert func.name == "complex_function"
            # Should contain the main parameters
            assert "arg1: str" in func.signature
            assert "arg2: int" in func.signature

        finally:
            temp_file.unlink()

    def test_parse_file_invalid_syntax(self):
        """Test parsing a file with invalid Python syntax."""
        test_code = """
def invalid_syntax(
    missing_closing_paren
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(test_code)
            temp_file = Path(f.name)

        try:
            with pytest.raises(SyntaxError):
                self.parser.parse_file(temp_file)

        finally:
            temp_file.unlink()

    def test_parse_nonexistent_file(self):
        """Test parsing a nonexistent file."""
        nonexistent_file = Path("this_file_does_not_exist.py")

        with pytest.raises(FileNotFoundError):
            self.parser.parse_file(nonexistent_file)

    def test_parse_file_with_nested_functions(self):
        """Test parsing file with nested functions."""
        test_code = '''
import mcp

@mcp.tool()
def outer_function():
    """Outer function with nested function."""

    def nested_function():
        """This should not be picked up as MCP function."""
        return "nested"

    return nested_function()

def another_outer():
    """Non-MCP function."""

    @mcp.tool()  # This decorator inside should not count
    def incorrectly_decorated():
        return "wrong"

    return "outer"
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(test_code)
            temp_file = Path(f.name)

        try:
            result = self.parser.parse_file(temp_file)

            # Should only find the top-level MCP function
            mcp_funcs = result["mcp_functions"]
            assert len(mcp_funcs) == 1
            assert mcp_funcs[0].name == "outer_function"

        finally:
            temp_file.unlink()

    def test_parse_file_with_class_methods(self):
        """Test parsing file with class methods that have MCP decorators."""
        test_code = '''
import mcp

class TestClass:
    @mcp.tool()
    def method_with_mcp(self, value: str) -> str:
        """Method with MCP decorator."""
        return f"Method: {value}"

    def regular_method(self):
        """Regular method."""
        return "regular"

@mcp.tool()
def standalone_function():
    """Standalone MCP function."""
    return "standalone"
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(test_code)
            temp_file = Path(f.name)

        try:
            result = self.parser.parse_file(temp_file)

            mcp_funcs = result["mcp_functions"]
            # Should find both the method and standalone function
            assert len(mcp_funcs) == 2

            func_names = [f.name for f in mcp_funcs]
            assert "method_with_mcp" in func_names
            assert "standalone_function" in func_names

        finally:
            temp_file.unlink()


if __name__ == "__main__":
    pytest.main([__file__])
