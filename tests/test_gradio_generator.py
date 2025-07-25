#!/usr/bin/env python3
"""
Unit tests for the GradioGenerator class.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from source.config import Config
from source.gradio_generator import GradioGenerator

# Add source to path
sys.path.insert(0, str(Path(__file__).parent.parent / "source"))


class TestGradioGenerator:
    """Test class for GradioGenerator functionality."""

    def test_gradio_generator_initialization(self):
        """Test GradioGenerator initialization."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        assert generator.config == config

    def test_generate_gradio_interface_single(self):
        """Test generating interface for a single function."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        # Mock function
        mock_func = MagicMock()
        mock_func.name = "test_function"
        mock_func.signature = "(name: str) -> str"

        improved_docstrings = {"test_function": "Test function that greets someone."}

        result = generator.generate_gradio_interface([mock_func], improved_docstrings)

        assert isinstance(result, str)
        assert "gr.Interface" in result
        assert "test_function" in result
        assert "Test function that greets someone" in result
        assert 'if __name__ == "__main__":' in result
        assert ".launch(" in result

    def test_generate_gradio_interface_multiple(self):
        """Test generating interface for multiple functions."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        # Mock functions
        mock_func1 = MagicMock()
        mock_func1.name = "function_one"
        mock_func1.signature = "(a: int, b: int) -> int"

        mock_func2 = MagicMock()
        mock_func2.name = "function_two"
        mock_func2.signature = "(text: str) -> str"

        functions = [mock_func1, mock_func2]
        improved_docstrings = {
            "function_one": "Adds two numbers together.",
            "function_two": "Processes text input.",
        }

        result = generator.generate_gradio_interface(functions, improved_docstrings)

        assert isinstance(result, str)
        assert "gr.Blocks" in result
        assert "gr.Tab" in result
        assert "function_one" in result
        assert "function_two" in result
        assert "Function One" in result  # Title case conversion
        assert "Function Two" in result
        assert "Adds two numbers together" in result
        assert "Processes text input" in result

    def test_generate_single_interface_with_share(self):
        """Test generating single interface with sharing enabled."""
        config = Config(input_files=[Path("test.py")], share=True)
        generator = GradioGenerator(config)

        mock_func = MagicMock()
        mock_func.name = "test_function"
        mock_func.signature = "(name: str) -> str"

        result = generator._generate_single_interface(mock_func, "Test docstring")

        assert "share=True" in result

    def test_generate_tabbed_interface_with_share(self):
        """Test generating tabbed interface with sharing enabled."""
        config = Config(input_files=[Path("test.py")], share=True)
        generator = GradioGenerator(config)

        mock_func = MagicMock()
        mock_func.name = "test_function"
        mock_func.signature = "(arg: str) -> str"

        result = generator._generate_tabbed_interface(
            [mock_func], {"test_function": "Test docstring"}
        )

        assert "share=True" in result

    def test_extract_params_from_signature_string_param(self):
        """Test extracting string parameter from signature."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        params = generator._extract_params_from_signature("(name: str) -> str")

        assert len(params) == 1
        assert params[0] == ("name", "str")

    def test_extract_params_from_signature_int_param(self):
        """Test extracting integer parameter from signature."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        params = generator._extract_params_from_signature("(num: int) -> int")

        assert len(params) == 1
        assert params[0] == ("num", "int")

    def test_extract_params_from_signature_float_param(self):
        """Test extracting float parameter from signature."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        params = generator._extract_params_from_signature("(value: float) -> float")

        assert len(params) == 1
        assert params[0] == ("value", "float")

    def test_extract_params_from_signature_bool_param(self):
        """Test extracting boolean parameter from signature."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        params = generator._extract_params_from_signature("(flag: bool) -> str")

        assert len(params) == 1
        assert params[0] == ("flag", "bool")

    def test_extract_params_from_signature_multiple_params(self):
        """Test extracting multiple parameters from signature."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        params = generator._extract_params_from_signature(
            "(name: str, age: int, height: float, active: bool) -> str"
        )

        assert len(params) == 4
        assert params[0] == ("name", "str")
        assert params[1] == ("age", "int")
        assert params[2] == ("height", "float")
        assert params[3] == ("active", "bool")

    def test_extract_params_from_signature_no_params(self):
        """Test extracting from function with no parameters."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        params = generator._extract_params_from_signature("() -> str")

        assert len(params) == 0

    def test_extract_params_from_signature_no_types(self):
        """Test extracting from signature without type annotations."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        params = generator._extract_params_from_signature("(name, age) -> str")

        assert len(params) == 2
        assert params[0] == ("name", "str")  # defaults to str
        assert params[1] == ("age", "str")  # defaults to str

    def test_title_case_conversion(self):
        """Test function name to title case conversion."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        # Test in the context of tabbed interface
        mock_func = MagicMock()
        mock_func.name = "calculate_area_of_circle"
        mock_func.signature = "(radius: float) -> float"

        result = generator._generate_tabbed_interface(
            [mock_func], {"calculate_area_of_circle": "Calculates area"}
        )

        assert "Calculate Area Of Circle" in result

    def test_interface_imports(self):
        """Test that generated interfaces include necessary imports."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        mock_func = MagicMock()
        mock_func.name = "test_function"
        mock_func.signature = "(arg: str) -> str"

        # Test single interface
        single_result = generator._generate_single_interface(
            mock_func, "Test docstring"
        )
        assert "import gradio as gr" in single_result

        # Test tabbed interface
        tabbed_result = generator._generate_tabbed_interface(
            [mock_func], {"test_function": "Test docstring"}
        )
        assert "import gradio as gr" in tabbed_result

    def test_interface_function_imports(self):
        """Test that generated interfaces import the functions."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        mock_func1 = MagicMock()
        mock_func1.name = "function_one"
        mock_func1.signature = "(arg: str) -> str"

        mock_func2 = MagicMock()
        mock_func2.name = "function_two"
        mock_func2.signature = "(arg: int) -> int"

        # Test single function import
        single_result = generator._generate_single_interface(
            mock_func1, "Test docstring"
        )
        assert "from server.mcp_server import function_one" in single_result

        # Test multiple function imports
        tabbed_result = generator._generate_tabbed_interface(
            [mock_func1, mock_func2],
            {"function_one": "Test 1", "function_two": "Test 2"},
        )
        assert (
            "from server.mcp_server import function_one, function_two" in tabbed_result
        )

    def test_input_generation_for_different_types(self):
        """Test that different parameter types generate appropriate Gradio inputs."""
        config = Config(input_files=[Path("test.py")])
        generator = GradioGenerator(config)

        # Test string input
        mock_func_str = MagicMock()
        mock_func_str.name = "str_func"
        mock_func_str.signature = "(text: str) -> str"

        result = generator._generate_single_interface(mock_func_str, "String function")
        assert "gr.Textbox" in result

        # Test float input
        mock_func_float = MagicMock()
        mock_func_float.name = "float_func"
        mock_func_float.signature = "(value: float) -> float"

        result = generator._generate_single_interface(mock_func_float, "Float function")
        assert "gr.Number" in result
        assert "value=1.0" in result

        # Test int input
        mock_func_int = MagicMock()
        mock_func_int.name = "int_func"
        mock_func_int.signature = "(num: int) -> int"

        result = generator._generate_single_interface(mock_func_int, "Int function")
        assert "gr.Number" in result
        assert "precision=0" in result

        # Test bool input
        mock_func_bool = MagicMock()
        mock_func_bool.name = "bool_func"
        mock_func_bool.signature = "(flag: bool) -> bool"

        result = generator._generate_single_interface(mock_func_bool, "Bool function")
        assert "gr.Checkbox" in result


if __name__ == "__main__":
    pytest.main([__file__])
