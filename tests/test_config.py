"""
Unit tests for the config module.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from source.config import Config

# Add source to path
sys.path.insert(0, str(Path(__file__).parent.parent / "source"))


class TestConfig:
    """Test class for Config functionality."""

    def test_config_initialization_basic(self):
        """Test basic config initialization."""
        input_files = [Path("input/test.py")]
        config = Config(input_files=input_files)

        assert config.input_files == input_files
        assert not config.share
        assert config.model_endpoint is None
        assert not config.preserve_docstrings
        assert config.local_model == "HuggingFaceTB/SmolLM3-3B"
        assert config.device == "mps"
        assert config.output_dir == Path("output")
        assert config.model_config == "json/model_config.json"
        assert config.log_file == "log/builds/output.log"
        assert config.port == 7860
        assert not config.disable_sample_prompts

    def test_config_initialization_with_all_options(self):
        """Test config initialization with all options."""
        input_files = [Path("input/test.py")]
        config = Config(
            input_files=input_files,
            share=True,
            model_endpoint="http://localhost:8000",
            preserve_docstrings=True,
            local_model="custom-model",
            device="cpu",
            output_dir=Path("custom-output"),
            model_config="custom/model.json",
            log_file="custom/log.log",
            port=8080,
            disable_sample_prompts=True,
        )

        assert config.input_files == input_files
        assert config.share
        assert config.model_endpoint == "http://localhost:8000"
        assert config.preserve_docstrings
        assert config.local_model == "custom-model"
        assert config.device == "cpu"
        assert config.output_dir == Path("custom-output")
        assert config.model_config == "custom/model.json"
        assert config.log_file == "custom/log.log"
        assert config.port == 8080
        assert config.disable_sample_prompts

    @patch("pathlib.Path.mkdir")
    def test_config_post_init_creates_directories(self, mock_mkdir):
        """Test that config creates output directories."""
        input_files = [Path("input/test.py")]
        config = Config(input_files=input_files)

        # Check that directories were created
        assert mock_mkdir.call_count == 3  # output_dir, server_dir, client_dir

        # Check directory paths
        assert config.server_dir == config.output_dir / "server"
        assert config.client_dir == config.output_dir / "client"

    def test_use_local_model_true(self):
        """Test use_local_model property when model_endpoint is None."""
        input_files = [Path("input/test.py")]
        config = Config(input_files=input_files)

        assert config.use_local_model is True

    def test_use_local_model_false(self):
        """Test use_local_model property when model_endpoint is set."""
        input_files = [Path("input/test.py")]
        config = Config(input_files=input_files, model_endpoint="http://localhost:8000")

        assert config.use_local_model is False

    def test_model_name_local(self):
        """Test model_name property for local model."""
        input_files = [Path("input/test.py")]
        config = Config(input_files=input_files, local_model="custom-model")

        assert config.model_name == "custom-model"

    def test_model_name_openai_compatible(self):
        """Test model_name property for OpenAI-compatible model."""
        input_files = [Path("input/test.py")]
        config = Config(input_files=input_files, model_endpoint="http://localhost:8000")

        assert config.model_name == "openai-compatible"

    def test_is_mac_with_mps_true(self):
        """Test is_mac_with_mps property when device is mps."""
        input_files = [Path("input/test.py")]
        config = Config(input_files=input_files, device="mps")

        assert config.is_mac_with_mps is True

    def test_is_mac_with_mps_false_cpu(self):
        """Test is_mac_with_mps returns False when device is cpu."""
        input_files = [Path("input/test.py")]
        config = Config(input_files=input_files, device="cpu")

        assert config.is_mac_with_mps is False

    def test_is_mac_with_mps_false_cuda(self):
        """Test is_mac_with_mps returns False when device is cuda."""
        input_files = [Path("input/test.py")]
        config = Config(input_files=input_files, device="cuda")

        assert config.is_mac_with_mps is False

    def test_config_with_string_output_dir(self):
        """Test config with string output directory."""
        input_files = [Path("input/test.py")]
        config = Config(input_files=input_files, output_dir=Path("string-output"))

        assert config.output_dir == Path("string-output")

    def test_config_multiple_input_files(self):
        """Test config with multiple input files."""
        input_files = [Path("input/test1.py"), Path("input/test2.py")]
        config = Config(input_files=input_files)

        assert config.input_files == input_files
        assert len(config.input_files) == 2

    def test_config_device_options(self):
        """Test config with different device options."""
        input_files = [Path("input/test.py")]

        # Test MPS
        config_mps = Config(input_files=input_files, device="mps")
        assert config_mps.device == "mps"

        # Test CPU
        config_cpu = Config(input_files=input_files, device="cpu")
        assert config_cpu.device == "cpu"

        # Test CUDA
        config_cuda = Config(input_files=input_files, device="cuda")
        assert config_cuda.device == "cuda"

    def test_config_port_validation(self):
        """Test config with different port values."""
        input_files = [Path("input/test.py")]

        # Test default port
        config_default = Config(input_files=input_files)
        assert config_default.port == 7860

        # Test custom port
        config_custom = Config(input_files=input_files, port=8080)
        assert config_custom.port == 8080

        # Test another custom port
        config_custom2 = Config(input_files=input_files, port=9000)
        assert config_custom2.port == 9000

    def test_config_model_config_paths(self):
        """Test config with different model config paths."""
        input_files = [Path("input/test.py")]

        # Test default path
        config_default = Config(input_files=input_files)
        assert config_default.model_config == "json/model_config.json"

        # Test custom path
        config_custom = Config(
            input_files=input_files, model_config="custom/path/config.json"
        )
        assert config_custom.model_config == "custom/path/config.json"

    def test_config_log_file_paths(self):
        """Test config with different log file paths."""
        input_files = [Path("input/test.py")]

        # Test default path
        config_default = Config(input_files=input_files)
        assert config_default.log_file == "log/builds/output.log"

        # Test custom path
        config_custom = Config(input_files=input_files, log_file="custom/log/file.log")
        assert config_custom.log_file == "custom/log/file.log"

    def test_config_disable_sample_prompts(self):
        """Test config with disable_sample_prompts option."""
        input_files = [Path("input/test.py")]

        # Test default (False)
        config_default = Config(input_files=input_files)
        assert config_default.disable_sample_prompts is False

        # Test enabled (True)
        config_disabled = Config(input_files=input_files, disable_sample_prompts=True)
        assert config_disabled.disable_sample_prompts is True

    def test_config_validation_methods(self):
        """Test the validation methods work correctly."""
        input_files = [Path("input/test.py")]

        # Test local model usage
        config_local = Config(input_files=input_files, model_endpoint=None)
        assert config_local.use_local_model is True
        assert config_local.model_name == config_local.local_model

        # Test remote model usage
        config_remote = Config(
            input_files=input_files, model_endpoint="http://example.com"
        )
        assert config_remote.use_local_model is False
        assert config_remote.model_name == "openai-compatible"

    @patch("pathlib.Path.mkdir")
    def test_config_directory_structure(self, mock_mkdir):
        """Test that all required directories are set up correctly."""
        input_files = [Path("input/test.py")]
        config = Config(input_files=input_files)

        # Check all directory attributes exist
        assert hasattr(config, "server_dir")
        assert hasattr(config, "client_dir")

        # Check directory paths are correct
        assert config.server_dir == config.output_dir / "server"
        assert config.client_dir == config.output_dir / "client"

        # Check mkdir was called for each directory
        expected_calls = [config.output_dir, config.server_dir, config.client_dir]
        assert mock_mkdir.call_count == len(expected_calls)


if __name__ == "__main__":
    pytest.main([__file__])
