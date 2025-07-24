"""
Unit tests for the CLI module.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add source to path
sys.path.insert(0, str(Path(__file__).parent.parent / "source"))

from source.cli import create_parser, main


class TestCLI:
    """Test class for CLI functionality."""

    def test_parse_args_basic(self):
        """Test basic argument parsing."""
        parser = create_parser()
        args = parser.parse_args(['input/test.py'])
        assert [str(f) for f in args.input_files] == ['input/test.py']
        assert not args.share
        assert args.model_endpoint is None
        assert not args.preserve_docstrings
        assert args.local_model == "HuggingFaceTB/SmolLM3-3B"
        assert str(args.output_dir) == "output"
        assert args.device == "mps"
        assert not args.disable_sample_prompts
        assert args.log_config == "json/log_config.json"
        assert args.log_file == "log/builds/output.log"
        assert args.model_config == "json/model_config.json"
        assert args.port == 7860
        assert not args.verbose

    def test_parse_args_with_all_options(self):
        """Test argument parsing with all options."""
        parser = create_parser()
        args = parser.parse_args([
            'input/test1.py',
            'input/test2.py',
            '--share',
            '--model-endpoint', 'http://localhost:8000',
            '--preserve-docstrings',
            '--local-model', 'test-model',
            '--output-dir', 'custom-output',
            '--device', 'cpu',
            '--disable-sample-prompts',
            '--log-config', 'custom/log.json',
            '--log-file', 'custom/log.log',
            '--model-config', 'custom/model.json',
            '--port', '8080',
            '--verbose'
        ])
        assert [str(f) for f in args.input_files] == ['input/test1.py', 'input/test2.py']
        assert args.share
        assert args.model_endpoint == 'http://localhost:8000'
        assert args.preserve_docstrings
        assert args.local_model == 'test-model'
        assert str(args.output_dir) == 'custom-output'
        assert args.device == 'cpu'
        assert args.disable_sample_prompts
        assert args.log_config == 'custom/log.json'
        assert args.log_file == 'custom/log.log'
        assert args.model_config == 'custom/model.json'
        assert args.port == 8080
        assert args.verbose

    def test_parse_args_device_choices(self):
        """Test device argument choices."""
        parser = create_parser()

        # Test valid choices
        for device in ['cpu', 'mps', 'cuda']:
            args = parser.parse_args(['input/test.py', '--device', device])
            assert args.device == device

        # Test invalid choice
        with pytest.raises(SystemExit):
            parser.parse_args(['input/test.py', '--device', 'invalid'])

    def test_parse_args_verbose_short_form(self):
        """Test verbose argument short form."""
        parser = create_parser()
        args = parser.parse_args(['input/test.py', '-v'])
        assert args.verbose

    def test_parse_args_multiple_input_files(self):
        """Test parsing multiple input files."""
        parser = create_parser()
        args = parser.parse_args(['file1.py', 'file2.py', 'file3.py'])
        expected = ['file1.py', 'file2.py', 'file3.py']
        assert [str(f) for f in args.input_files] == expected

    def test_parse_args_path_conversion(self):
        """Test that output_dir is properly converted to Path."""
        parser = create_parser()
        args = parser.parse_args(['input/test.py', '--output-dir', '/custom/path'])
        assert isinstance(args.output_dir, Path)
        assert str(args.output_dir) == '/custom/path'

    def test_parse_args_port_type(self):
        """Test that port is properly converted to int."""
        parser = create_parser()
        args = parser.parse_args(['input/test.py', '--port', '9000'])
        assert isinstance(args.port, int)
        assert args.port == 9000

    def test_parse_args_invalid_port(self):
        """Test invalid port argument."""
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(['input/test.py', '--port', 'not_a_number'])

    @patch('source.cli.GradioMCPBuilder')
    @patch('source.cli.Config')
    @patch('source.cli.setup_logging')
    @patch('source.cli.get_logger')
    @patch('pathlib.Path.exists')
    def test_main_success(self, mock_exists, mock_get_logger, mock_setup_logging, mock_config, mock_builder):
        """Test successful main execution."""
        # Mock file existence
        mock_exists.return_value = True

        # Mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Mock config and builder
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance

        mock_builder_instance = MagicMock()
        mock_builder.return_value = mock_builder_instance

        with patch('sys.argv', ['cli.py', 'input/test.py']):
            result = main()

            assert result == 0
            mock_setup_logging.assert_called_once()
            mock_config.assert_called_once()
            mock_builder.assert_called_once_with(mock_config_instance)
            mock_builder_instance.build.assert_called_once()

    @patch('source.cli.get_logger')
    @patch('source.cli.setup_logging')
    @patch('pathlib.Path.exists')
    def test_main_file_not_exists(self, mock_exists, mock_setup_logging, mock_get_logger):
        """Test main when input file doesn't exist."""
        mock_exists.return_value = False
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        with patch('sys.argv', ['cli.py', 'nonexistent.py']):
            result = main()

            assert result == 1
            mock_logger.error.assert_called()

    @patch('source.cli.get_logger')
    @patch('source.cli.setup_logging')
    @patch('pathlib.Path.exists')
    def test_main_not_python_file(self, mock_exists, mock_setup_logging, mock_get_logger):
        """Test main when input file is not a Python file."""
        mock_exists.return_value = True
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        with patch('sys.argv', ['cli.py', 'input/test.txt']):
            result = main()

            assert result == 1
            mock_logger.error.assert_called()

    @patch('source.cli.GradioMCPBuilder')
    @patch('source.cli.Config')
    @patch('source.cli.setup_logging')
    @patch('source.cli.get_logger')
    @patch('pathlib.Path.exists')
    def test_main_builder_error(self, mock_exists, mock_get_logger, mock_setup_logging, mock_config, mock_builder):
        """Test main when builder raises an exception."""
        # Mock file existence
        mock_exists.return_value = True

        # Mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Mock config and builder
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance

        mock_builder_instance = MagicMock()
        mock_builder_instance.build.side_effect = Exception("Build failed")
        mock_builder.return_value = mock_builder_instance

        with patch('sys.argv', ['cli.py', 'input/test.py']):
            result = main()

            assert result == 1
            mock_logger.error.assert_called()

    @patch('source.cli.GradioMCPBuilder')
    @patch('source.cli.Config')
    @patch('source.cli.setup_logging')
    @patch('source.cli.get_logger')
    @patch('pathlib.Path.exists')
    def test_main_keyboard_interrupt(self, mock_exists, mock_get_logger, mock_setup_logging, mock_config, mock_builder):
        """Test main when KeyboardInterrupt is raised."""
        # Mock file existence
        mock_exists.return_value = True

        # Mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Mock config and builder
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance

        mock_builder_instance = MagicMock()
        mock_builder_instance.build.side_effect = KeyboardInterrupt()
        mock_builder.return_value = mock_builder_instance

        with patch('sys.argv', ['cli.py', 'input/test.py']):
            result = main()

            assert result == 1
            mock_logger.warning.assert_called()

    @patch('source.cli.setup_logging')
    @patch('source.cli.get_logger')
    @patch('pathlib.Path.exists')
    def test_main_verbose_logging(self, mock_exists, mock_get_logger, mock_setup_logging):
        """Test main with verbose logging enabled."""
        mock_exists.return_value = True
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Mock logging.getLogger to return a mock root logger
        mock_root_logger = MagicMock()
        mock_named_logger = MagicMock()

        with patch('sys.argv', ['cli.py', 'input/test.py', '--verbose']), \
             patch('logging.getLogger') as mock_logging_get_logger, \
             patch('source.cli.Config') as mock_config, \
             patch('source.cli.GradioMCPBuilder') as mock_builder:

            # Configure mocks
            mock_logging_get_logger.side_effect = lambda name=None: mock_root_logger if name is None else mock_named_logger
            mock_config_instance = MagicMock()
            mock_config.return_value = mock_config_instance
            mock_builder_instance = MagicMock()
            mock_builder.return_value = mock_builder_instance

            result = main()

            # Should succeed
            assert result == 0
            # Verbose logging should be enabled
            mock_logger.debug.assert_called()

    @patch('source.cli.GradioMCPBuilder')
    @patch('source.cli.Config')
    @patch('source.cli.setup_logging')
    @patch('source.cli.get_logger')
    @patch('pathlib.Path.exists')
    def test_main_config_creation(self, mock_exists, mock_get_logger, mock_setup_logging, mock_config, mock_builder):
        """Test that Config is created with correct arguments."""
        mock_exists.return_value = True
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        mock_builder_instance = MagicMock()
        mock_builder.return_value = mock_builder_instance

        with patch('sys.argv', [
            'cli.py', 'test.py',
            '--share',
            '--preserve-docstrings',
            '--local-model', 'custom-model',
            '--device', 'cpu',
            '--output-dir', 'custom-output',
            '--port', '8080',
            '--disable-sample-prompts'
        ]):
            result = main()

            assert result == 0

            # Check that Config was called with correct arguments
            mock_config.assert_called_once()
            call_args = mock_config.call_args[1]  # keyword arguments

            assert call_args['share'] == True
            assert call_args['preserve_docstrings'] == True
            assert call_args['local_model'] == 'custom-model'
            assert call_args['device'] == 'cpu'
            assert str(call_args['output_dir']) == 'custom-output'
            assert call_args['port'] == 8080
            assert call_args['disable_sample_prompts'] == True


if __name__ == '__main__':
    pytest.main([__file__])