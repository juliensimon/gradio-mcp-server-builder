#!/usr/bin/env python3
"""
Test suite for the GradioMCPBuilder class.
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from source.builder import GradioMCPBuilder
from source.config import Config
from source.parser import MCPFunction


class TestGradioMCPBuilder(unittest.TestCase):
    """Test cases for GradioMCPBuilder."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = Config(
            input_files=[Path("test_input.py")],
            output_dir=Path("test_output"),
            preserve_docstrings=False,
            disable_sample_prompts=False
        )
        self.builder = GradioMCPBuilder(self.config)

    def test_builder_initialization(self):
        """Test builder initialization."""
        assert self.builder.config == self.config
        assert hasattr(self.builder, 'logger')
        assert hasattr(self.builder, 'parser')
        assert hasattr(self.builder, 'docstring_improver')
        assert hasattr(self.builder, 'gradio_generator')
        assert hasattr(self.builder, 'server_generator')
        assert hasattr(self.builder, 'client_generator')

        assert hasattr(self.builder, 'doc_generator')
        assert hasattr(self.builder, 'req_generator')
        assert self.builder.mcp_functions == []
        assert self.builder.helper_functions == []
        assert self.builder.module_constants == []
        assert self.builder.improved_docstrings == {}
        assert self.builder.test_prompts == {}

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    @patch('pathlib.Path.exists', return_value=True)
    @patch.object(Path, 'write_text')
    def test_build_success(self, mock_write_text, mock_exists, mock_mkdir, mock_file_open):
        """Test successful build process."""
        # Mock parser results
        mock_function = MagicMock()
        mock_function.name = 'test_func'
        mock_function.docstring = 'Original docstring'

        parser_result = {
            'mcp_functions': [mock_function],
            'helper_functions': [],
            'module_constants': [],
            'other_functions': [],
            'module_docstring': 'Test module',
            'module_imports': [],
            'content': 'test content'
        }

        with patch.object(self.builder.parser, 'parse_file', return_value=parser_result), \
             patch.object(self.builder.docstring_improver, 'improve_function_docstring', return_value='improved doc'), \
             patch.object(self.builder.docstring_improver, 'generate_test_prompts', return_value=['prompt1']), \
             patch.object(self.builder.server_generator, 'generate_server', return_value='server content'), \
             patch.object(self.builder.server_generator, 'generate_init_file', return_value='server init'), \
             patch.object(self.builder.client_generator, 'generate_client', return_value='client content'), \
             patch.object(self.builder.doc_generator, 'generate_readme', return_value='readme content'), \
             patch.object(self.builder.req_generator, 'generate_requirements', return_value='requirements content'), \
             patch.object(self.builder, '_generate_config_file') as mock_config_gen, \
             patch.object(self.builder.logger, 'info'), \
             patch.object(self.builder.logger, 'debug'), \
             patch.object(self.builder.logger, 'error'):

            self.builder.build()

            # Verify function was added
            assert len(self.builder.mcp_functions) == 1
            assert self.builder.mcp_functions[0].name == 'test_func'
            # Verify all generators were called
            mock_config_gen.assert_called_once()

    def test_parse_input_files(self):
        """Test parsing input files."""
        mock_function1 = MagicMock()
        mock_function1.name = 'func1'
        mock_function2 = MagicMock()
        mock_function2.name = 'func2'

        parser_result = {
            'mcp_functions': [mock_function1, mock_function2],
            'helper_functions': [],
            'module_constants': [],
            'other_functions': [],
            'module_docstring': 'Test module',
            'module_imports': [],
            'content': 'test content'
        }

        with patch.object(self.builder.parser, 'parse_file', return_value=parser_result):
            self.builder._parse_input_files()

            assert len(self.builder.mcp_functions) == 2
            assert self.builder.mcp_functions[0].name == 'func1'
            assert self.builder.mcp_functions[1].name == 'func2'

    def test_parse_input_files_no_functions(self):
        """Test parsing input files with no MCP functions."""
        parser_result = {
            'mcp_functions': [],
            'helper_functions': [],
            'module_constants': [],
            'other_functions': [],
            'module_docstring': 'Test module',
            'module_imports': [],
            'content': 'test content'
        }

        with patch.object(self.builder.parser, 'parse_file', return_value=parser_result):
            with self.assertRaises(ValueError) as context:
                self.builder._parse_input_files()

            assert "No MCP functions found in input files" in str(context.exception)

    def test_improve_docstrings(self):
        """Test docstring improvement."""
        mock_function = MagicMock()
        mock_function.name = 'test_func'
        mock_function.docstring = 'Original docstring'
        self.builder.mcp_functions = [mock_function]

        with patch.object(self.builder.docstring_improver, 'improve_function_docstring', return_value='improved doc') as mock_improve:
            self.builder._improve_docstrings()

            # Function should be processed
            mock_improve.assert_called_once_with('test_func', 'Original docstring', mock_function.signature)
            assert self.builder.improved_docstrings['test_func'] == 'improved doc'

    def test_improve_docstrings_preserve_original(self):
        """Test docstring improvement when preserving originals."""
        self.builder.config.preserve_docstrings = True
        mock_function = MagicMock()
        mock_function.name = 'test_func'
        mock_function.docstring = 'Original docstring'
        self.builder.mcp_functions = [mock_function]

        with patch.object(self.builder.docstring_improver, 'improve_function_docstring') as mock_improve:
            self.builder._improve_docstrings()

            # Should not call improve when preserving
            mock_improve.assert_not_called()
            assert self.builder.improved_docstrings['test_func'] == 'Original docstring'

    def test_improve_docstrings_with_error(self):
        """Test docstring improvement when error occurs."""
        mock_function = MagicMock()
        mock_function.name = 'test_func'
        mock_function.docstring = 'Original docstring'
        self.builder.mcp_functions = [mock_function]

        with patch.object(self.builder.docstring_improver, 'improve_function_docstring', side_effect=Exception("Test error")) as mock_improve:
            self.builder._improve_docstrings()

            # Should fallback to original docstring
            assert self.builder.improved_docstrings['test_func'] == 'Original docstring'

    def test_generate_test_prompts(self):
        """Test test prompt generation."""
        mock_function = MagicMock()
        mock_function.name = 'func1'
        mock_function.docstring = 'test docstring'
        mock_function.signature = '(a: int)'
        self.builder.mcp_functions = [mock_function]
        # Set up the improved_docstrings as would be done by _improve_docstrings
        self.builder.improved_docstrings = {'func1': 'improved test docstring'}

        with patch.object(self.builder.docstring_improver, 'generate_test_prompts', return_value=['prompt1']) as mock_generate:
            self.builder._generate_test_prompts()

            mock_generate.assert_called_once_with('func1', 'improved test docstring', '(a: int)')
            assert 'func1' in self.builder.test_prompts
            assert self.builder.test_prompts['func1'] == ['prompt1']

    def test_generate_test_prompts_with_error(self):
        """Test test prompt generation when error occurs."""
        mock_function = MagicMock()
        mock_function.name = 'func1'
        mock_function.signature = '(a: int)'
        self.builder.mcp_functions = [mock_function]
        self.builder.improved_docstrings = {'func1': 'improved test docstring'}

        with patch.object(self.builder.docstring_improver, 'generate_test_prompts', side_effect=Exception("Test error")):
            self.builder._generate_test_prompts()

            # Should fallback to empty list
            assert self.builder.test_prompts['func1'] == []

    @patch('pathlib.Path.mkdir')
    def test_create_output_directories(self, mock_mkdir):
        """Test output directory creation."""
        self.builder._create_output_directories()

        # Should create multiple directories
        assert mock_mkdir.call_count >= 3  # output_dir and subdirectories (server, client)

    @patch('pathlib.Path.write_text')
    def test_generate_server_files(self, mock_write_text):
        """Test server file generation."""
        with patch.object(self.builder.server_generator, 'generate_server', return_value='server content') as mock_gen_server, \
             patch.object(self.builder.server_generator, 'generate_init_file', return_value='init content') as mock_gen_init:

            self.builder._generate_server_files()

            # Should generate both server and init files
            mock_gen_server.assert_called_once()
            mock_gen_init.assert_called_once()
            assert mock_write_text.call_count == 2  # server file + init file

    @patch('pathlib.Path.write_text')
    def test_generate_client_files(self, mock_write_text):
        """Test client file generation."""
        with patch.object(self.builder.client_generator, 'generate_client', return_value='client content') as mock_gen:

            self.builder._generate_client_files()

            mock_gen.assert_called_once_with(self.builder.mcp_functions, self.builder.test_prompts)
            mock_write_text.assert_called_once()



    @patch('pathlib.Path.write_text')
    def test_generate_documentation(self, mock_write_text):
        """Test documentation generation."""
        with patch.object(self.builder.doc_generator, 'generate_readme', return_value='readme content') as mock_gen:

            self.builder._generate_documentation()

            mock_gen.assert_called_once_with(self.builder.mcp_functions, self.builder.improved_docstrings, self.builder.test_prompts)
            mock_write_text.assert_called_once()

    @patch('pathlib.Path.write_text')
    def test_generate_requirements(self, mock_write_text):
        """Test requirements file generation."""
        with patch.object(self.builder.req_generator, 'generate_requirements', return_value='requirements content') as mock_gen:

            self.builder._generate_requirements()

            mock_gen.assert_called_once()
            mock_write_text.assert_called_once()

    def test_generate_config_file(self):
        """Test config file generation."""
        with patch('builtins.open', mock_open()) as mock_file, \
             patch('json.dump') as mock_json_dump:

            self.builder._generate_config_file()

            # Should open the config file and write JSON
            mock_file.assert_called()
            mock_json_dump.assert_called_once()

    def test_builder_with_helper_functions(self):
        """Test builder handles helper functions correctly."""
        mock_mcp_func = MagicMock()
        mock_mcp_func.name = 'mcp_func'
        mock_helper_func = MagicMock()
        mock_helper_func.name = 'helper_func'

        parser_result = {
            'mcp_functions': [mock_mcp_func],
            'helper_functions': [mock_helper_func],
            'module_constants': ['CONSTANT = 42'],
            'other_functions': [],
            'module_docstring': 'Test module',
            'module_imports': [],
            'content': 'test content'
        }

        with patch.object(self.builder.parser, 'parse_file', return_value=parser_result):
            self.builder._parse_input_files()

            assert len(self.builder.mcp_functions) == 1
            assert len(self.builder.helper_functions) == 1
            assert len(self.builder.module_constants) == 1
            assert self.builder.mcp_functions[0].name == 'mcp_func'
            assert self.builder.helper_functions[0].name == 'helper_func'

    def test_builder_error_handling(self):
        """Test builder error handling."""
        with patch.object(self.builder.parser, 'parse_file', side_effect=Exception("Parse error")):
            with self.assertRaises(Exception):
                self.builder._parse_input_files()


if __name__ == '__main__':
    unittest.main()