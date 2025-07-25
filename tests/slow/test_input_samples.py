#!/usr/bin/env python3
"""
Comprehensive test suite for all input samples.
Tests server building, startup, and MCP functionality.
"""

import json
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import List

import pytest


@pytest.fixture(scope="session")
def temp_output_dir():
    """Create a temporary output directory for tests."""
    temp_dir = Path(tempfile.mkdtemp(prefix="mcp_test_"))
    yield temp_dir
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


class TestInputSamples:
    """Test all input sample examples."""

    def build_sample(
        self, sample_files: List[str], output_dir: Path, project_root: Path
    ) -> subprocess.CompletedProcess:
        """Build a sample using the CLI."""
        cmd = [
            sys.executable,
            "main.py",
            *sample_files,
            "--preserve-docstrings",
            "--disable-sample-prompts",
            "--output-dir",
            str(output_dir),
            "--log-file",
            f"log/builds/test_{int(time.time())}.log",
        ]

        return subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes
        )

    def test_basic_hello_world_build(self, temp_output_dir, project_root):
        """Test building the basic hello world example."""
        sample_files = ["input-samples/input-hello-world/hello_world.py"]
        result = self.build_sample(
            sample_files, temp_output_dir / "basic", project_root
        )

        assert result.returncode == 0, f"Build failed: {result.stderr}"
        assert "Successfully built MCP server" in result.stdout

        # Check generated files exist
        server_dir = temp_output_dir / "basic" / "server"
        assert (server_dir / "gradio_server.py").exists()
        assert (server_dir / "__init__.py").exists()

        client_dir = temp_output_dir / "basic" / "client"
        assert (client_dir / "mcp_client.py").exists()

        assert (temp_output_dir / "basic" / "README.md").exists()
        assert (temp_output_dir / "basic" / "requirements.txt").exists()

    def test_simple_math_build(self, temp_output_dir, project_root):
        """Test building the simple math operations example."""
        sample_files = ["input-samples/input-simple/math_operations.py"]
        result = self.build_sample(
            sample_files, temp_output_dir / "simple_math", project_root
        )

        assert result.returncode == 0, f"Build failed: {result.stderr}"
        assert "Successfully built MCP server" in result.stdout

        # Check generated files exist
        server_dir = temp_output_dir / "simple_math" / "server"
        assert (server_dir / "gradio_server.py").exists()

    def test_simple_geometry_build(self, temp_output_dir, project_root):
        """Test building the simple geometry example."""
        sample_files = ["input-samples/input-simple/geometry.py"]
        result = self.build_sample(
            sample_files, temp_output_dir / "simple_geo", project_root
        )

        assert result.returncode == 0, f"Build failed: {result.stderr}"
        assert "Successfully built MCP server" in result.stdout

        # Check generated files exist
        server_dir = temp_output_dir / "simple_geo" / "server"
        assert (server_dir / "gradio_server.py").exists()

    def test_simple_combined_build(self, temp_output_dir, project_root):
        """Test building combined simple examples (multi-function server)."""
        sample_files = [
            "input-samples/input-simple/math_operations.py",
            "input-samples/input-simple/geometry.py",
        ]
        result = self.build_sample(
            sample_files, temp_output_dir / "simple_combined", project_root
        )

        assert result.returncode == 0, f"Build failed: {result.stderr}"
        assert "Successfully built MCP server" in result.stdout

        # Check generated files exist
        server_dir = temp_output_dir / "simple_combined" / "server"
        assert (server_dir / "gradio_server.py").exists()

        # Check that it contains multiple functions
        server_code = (server_dir / "gradio_server.py").read_text()
        assert "add_numbers" in server_code
        assert "multiply_numbers" in server_code
        assert "circle_area" in server_code
        assert "rectangle_area" in server_code
        assert "gr.Blocks" in server_code  # Should use tabbed interface


class TestServerStartup:
    """Test that generated servers start successfully."""

    def start_server_thread(self, server_path: Path, port: int) -> threading.Thread:
        """Start a server in a background thread."""

        def run_server():
            try:
                import sys

                sys.path.insert(0, str(server_path.parent))
                import gradio_server

                gradio_server.demo.launch(
                    server_name="127.0.0.1",
                    server_port=port,
                    share=False,
                    quiet=True,
                    mcp_server=True,
                )
            except Exception as e:
                print(f"Server startup error: {e}")

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        return thread

    def test_basic_server_startup(self, temp_output_dir, project_root):
        """Test that basic server starts successfully."""
        # Build the basic example
        sample_files = ["input-samples/input-hello-world/hello_world.py"]
        result = self.build_sample(
            sample_files, temp_output_dir / "startup_basic", project_root
        )
        assert result.returncode == 0

        # Test server startup
        server_path = temp_output_dir / "startup_basic" / "server" / "gradio_server.py"
        thread = self.start_server_thread(server_path, 7870)

        # Give server time to start
        time.sleep(3)

        # Check if thread is still running (server started)
        assert thread.is_alive(), "Server thread should be running"

    def test_simple_server_startup(self, temp_output_dir, project_root):
        """Test that simple combined server starts successfully."""
        # Build the simple combined example
        sample_files = [
            "input-samples/input-simple/math_operations.py",
            "input-samples/input-simple/geometry.py",
        ]
        result = self.build_sample(
            sample_files, temp_output_dir / "startup_simple", project_root
        )
        assert result.returncode == 0

        # Test server startup
        server_path = temp_output_dir / "startup_simple" / "server" / "gradio_server.py"
        thread = self.start_server_thread(server_path, 7871)

        # Give server time to start
        time.sleep(3)

        # Check if thread is still running (server started)
        assert thread.is_alive(), "Server thread should be running"

    def build_sample(
        self, sample_files: List[str], output_dir: Path, project_root: Path
    ) -> subprocess.CompletedProcess:
        """Build a sample using the CLI."""
        cmd = [
            sys.executable,
            "main.py",
            *sample_files,
            "--preserve-docstrings",
            "--disable-sample-prompts",
            "--output-dir",
            str(output_dir),
            "--log-file",
            f"log/builds/test_startup_{int(time.time())}.log",
        ]

        return subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes
        )


class TestMCPFunctionality:
    """Test MCP functionality of generated servers."""

    def test_basic_mcp_functions(self, temp_output_dir, project_root):
        """Test MCP functions in basic example."""
        # Build the basic example
        sample_files = ["input-samples/input-hello-world/hello_world.py"]
        result = self.build_sample(
            sample_files, temp_output_dir / "mcp_basic", project_root
        )
        assert result.returncode == 0

        # Import and test the server
        server_path = temp_output_dir / "mcp_basic" / "server"
        sys.path.insert(0, str(server_path))

        try:
            # Force reimport
            if "gradio_server" in sys.modules:
                del sys.modules["gradio_server"]
            import gradio_server

            # Test greet function
            result = gradio_server.greet("MCP Test")
            assert isinstance(result, str)
            assert "MCP Test" in result
            assert "Hello" in result

            # Test demo object exists and is correct type
            assert hasattr(gradio_server, "demo")
            import gradio as gr

            assert isinstance(gradio_server.demo, gr.Interface)

        finally:
            # Clean up sys.path and modules
            if str(server_path) in sys.path:
                sys.path.remove(str(server_path))
            if "gradio_server" in sys.modules:
                del sys.modules["gradio_server"]

    def test_simple_mcp_functions(self, temp_output_dir, project_root):
        """Test MCP functions in simple example."""
        # Build the simple combined example
        sample_files = [
            "input-samples/input-simple/math_operations.py",
            "input-samples/input-simple/geometry.py",
        ]
        result = self.build_sample(
            sample_files, temp_output_dir / "mcp_simple2", project_root
        )
        assert result.returncode == 0

        # Import and test the server
        server_path = temp_output_dir / "mcp_simple2" / "server"
        sys.path.insert(0, str(server_path))

        try:
            # Force reimport
            if "gradio_server" in sys.modules:
                del sys.modules["gradio_server"]
            import gradio_server

            # Test math functions
            assert gradio_server.add_numbers(5, 3) == 8
            assert gradio_server.multiply_numbers(4, 7) == 28

            # Test geometry functions
            import math

            area = gradio_server.circle_area(2)
            expected = math.pi * 4  # π * r²
            assert abs(area - expected) < 0.001

            assert gradio_server.rectangle_area(3, 4) == 12

            # Test demo object exists and is correct type
            assert hasattr(gradio_server, "demo")
            import gradio as gr

            assert isinstance(gradio_server.demo, gr.Blocks)

        finally:
            # Clean up sys.path and modules
            if str(server_path) in sys.path:
                sys.path.remove(str(server_path))
            if "gradio_server" in sys.modules:
                del sys.modules["gradio_server"]

    def build_sample(
        self, sample_files: List[str], output_dir: Path, project_root: Path
    ) -> subprocess.CompletedProcess:
        """Build a sample using the CLI."""
        cmd = [
            sys.executable,
            "main.py",
            *sample_files,
            "--preserve-docstrings",
            "--disable-sample-prompts",
            "--output-dir",
            str(output_dir),
            "--log-file",
            f"log/builds/test_mcp_{int(time.time())}.log",
        ]

        return subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes
        )


class TestGeneratedClients:
    """Test generated MCP clients."""

    def test_basic_client_generation(self, temp_output_dir, project_root):
        """Test that basic client is generated correctly."""
        # Build the basic example
        sample_files = ["input-samples/input-hello-world/hello_world.py"]
        result = self.build_sample(
            sample_files, temp_output_dir / "client_basic", project_root
        )
        assert result.returncode == 0

        # Check client file
        client_path = temp_output_dir / "client_basic" / "client" / "mcp_client.py"
        assert client_path.exists()

        client_code = client_path.read_text()
        # Client should use MCP tools dynamically, not hardcode function names
        assert "MCPClient" in client_code
        assert "get_tools()" in client_code
        # Since we use --disable-sample-prompts, no specific examples should be hardcoded
        assert "create_agent_interface" in client_code

    def test_simple_client_generation(self, temp_output_dir, project_root):
        """Test that simple client is generated correctly."""
        # Build the simple combined example
        sample_files = [
            "input-samples/input-simple/math_operations.py",
            "input-samples/input-simple/geometry.py",
        ]
        result = self.build_sample(
            sample_files, temp_output_dir / "client_simple", project_root
        )
        assert result.returncode == 0

        # Check client file
        client_path = temp_output_dir / "client_simple" / "client" / "mcp_client.py"
        assert client_path.exists()

        client_code = client_path.read_text()
        # Client should use MCP tools dynamically, not hardcode function names
        assert "MCPClient" in client_code
        assert "get_tools()" in client_code
        # Since we use --disable-sample-prompts, no specific examples should be hardcoded
        assert "create_agent_interface" in client_code

    def build_sample(
        self, sample_files: List[str], output_dir: Path, project_root: Path
    ) -> subprocess.CompletedProcess:
        """Build a sample using the CLI."""
        cmd = [
            sys.executable,
            "main.py",
            *sample_files,
            "--preserve-docstrings",
            "--disable-sample-prompts",
            "--output-dir",
            str(output_dir),
            "--log-file",
            f"log/builds/test_client_{int(time.time())}.log",
        ]

        return subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
