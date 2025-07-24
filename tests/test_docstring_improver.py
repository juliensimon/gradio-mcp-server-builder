#!/usr/bin/env python3
"""
Unit tests for the DocstringImprover class.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add source to path
sys.path.insert(0, str(Path(__file__).parent.parent / "source"))

from source.docstring_improver import DocstringImprover
from source.config import Config


class TestDocstringImprover:
    """Test class for DocstringImprover functionality."""

    def test_docstring_improver_initialization(self):
        """Test DocstringImprover initialization."""
        config = Config(input_files=[Path("test.py")])
        improver = DocstringImprover(config)

        assert improver.config == config
        assert hasattr(improver, 'logger')
        assert hasattr(improver, 'model_config_loader')
        assert improver._model is None
        assert improver._tokenizer is None
        assert not improver._printed_improving_message

    def test_print_improving_message_once(self):
        """Test that improving message is only printed once."""
        config = Config(input_files=[Path("test.py")])
        improver = DocstringImprover(config)

        with patch.object(improver.logger, 'info') as mock_info:
            # First call should print message
            improver._print_improving_message_once()
            mock_info.assert_called_once_with("Improving docstrings...")

            # Second call should not print message again
            mock_info.reset_mock()
            improver._print_improving_message_once()
            mock_info.assert_not_called()

    def test_print_improving_message_preserve_docstrings(self):
        """Test that improving message is not printed when preserving docstrings."""
        config = Config(input_files=[Path("test.py")], preserve_docstrings=True)
        improver = DocstringImprover(config)

        with patch.object(improver.logger, 'info') as mock_info:
            improver._print_improving_message_once()
            mock_info.assert_not_called()

    def test_clean_docstring_syntax(self):
        """Test docstring cleaning functionality."""
        config = Config(input_files=[Path("test.py")])
        improver = DocstringImprover(config)

        # Test with good docstring
        clean_docstring = "This is a clean docstring."
        result = improver._clean_docstring_syntax(clean_docstring)
        assert "This is a clean docstring." in result

        # Test with empty docstring
        result = improver._clean_docstring_syntax("")
        assert result == "Function documentation."

        # Test with extra quotes
        messy_docstring = '"""This has extra quotes"""'
        result = improver._clean_docstring_syntax(messy_docstring)
        assert "This has extra quotes" in result

    @patch.object(DocstringImprover, '_generate_text')
    def test_improve_function_docstring(self, mock_generate):
        """Test improving function docstring."""
        config = Config(input_files=[Path("test.py")])
        improver = DocstringImprover(config)

        mock_generate.return_value = "Improved docstring for test function."

        result = improver.improve_function_docstring("test_func", "Original docstring", "(arg: str)")

        assert isinstance(result, str)
        assert len(result) > 0
        mock_generate.assert_called_once()

    @patch.object(DocstringImprover, '_generate_text')
    def test_generate_test_prompts(self, mock_generate):
        """Test generating test prompts."""
        config = Config(input_files=[Path("test.py")])
        improver = DocstringImprover(config)

        mock_generate.return_value = "Test the test_func function with various inputs\nVerify the output format\nCheck edge cases"

        result = improver.generate_test_prompts("test_func", "Test function docstring", "(arg: str)")

        assert isinstance(result, list)
        assert len(result) > 0
        mock_generate.assert_called_once()

    @patch.object(DocstringImprover, '_generate_with_local_model')
    def test_generate_text_local(self, mock_generate_local):
        """Test generating text with local model."""
        config = Config(input_files=[Path("test.py")], model_endpoint=None)
        improver = DocstringImprover(config)

        mock_generate_local.return_value = "Generated text"

        result = improver._generate_text("Test prompt")

        assert result == "Generated text"
        mock_generate_local.assert_called_once_with("Test prompt")

    @patch.object(DocstringImprover, '_generate_with_api')
    def test_generate_text_api(self, mock_generate_api):
        """Test generating text with API."""
        config = Config(input_files=[Path("test.py")], model_endpoint="http://localhost:8000")
        improver = DocstringImprover(config)

        mock_generate_api.return_value = "Generated text"

        result = improver._generate_text("Test prompt")

        assert result == "Generated text"
        mock_generate_api.assert_called_once_with("Test prompt")

    def test_create_template_docstring(self):
        """Test template docstring creation."""
        config = Config(input_files=[Path("test.py")])
        improver = DocstringImprover(config)

        # Test with decent existing docstring - should return original
        result = improver._create_template_docstring("test_func", "(name: str)", "Original docstring")
        assert result == "Original docstring"

        # Test with poor/empty docstring - should generate template
        result = improver._create_template_docstring("test_func", "(name: str)", "")
        assert isinstance(result, str)
        assert "Test Func" in result
        assert "name" in result

        # Test with no docstring indicator
        result = improver._create_template_docstring("test_func", "(name: str)", "no docstring")
        assert isinstance(result, str)
        assert "Test Func" in result

    @patch('torch.cuda.is_available', return_value=False)
    @patch('transformers.AutoTokenizer.from_pretrained')
    @patch('transformers.AutoModelForCausalLM.from_pretrained')
    def test_generate_with_local_model_mocked(self, mock_model_class, mock_tokenizer_class, mock_cuda):
        """Test generating with local model (mocked)."""
        config = Config(input_files=[Path("test.py")], model_endpoint=None)
        improver = DocstringImprover(config)

        # Mock tokenizer
        mock_tokenizer = MagicMock()
        mock_tokenizer.pad_token = None
        mock_tokenizer.eos_token = "<eos>"
        mock_tokenizer.return_value = {"input_ids": [[1, 2, 3]], "attention_mask": [[1, 1, 1]]}
        mock_tokenizer.decode.return_value = "Generated text"
        mock_tokenizer_class.return_value = mock_tokenizer

        # Mock model
        mock_model = MagicMock()
        mock_output = MagicMock()
        mock_output.sequences = [[1, 2, 3, 4, 5]]
        mock_model.generate.return_value = mock_output
        mock_model_class.return_value = mock_model

        with patch.object(improver.model_config_loader, 'load_config') as mock_load_config, \
             patch.object(improver.model_config_loader, 'get_device_config', return_value={}), \
             patch.object(improver.model_config_loader, 'get_generation_params', return_value={}):

            # Mock the config structure
            mock_config = MagicMock()
            mock_config.local_model.default_model = "test-model"
            mock_config.local_model.model_loading = {}
            mock_config.local_model.tokenizer_params = {}
            mock_load_config.return_value = mock_config

            result = improver._generate_with_local_model("Test prompt")

            assert isinstance(result, str)
            mock_tokenizer_class.assert_called_once()
            mock_model_class.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__])