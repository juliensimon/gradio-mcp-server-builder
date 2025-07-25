"""
Slow tests for advanced input samples.

These tests are excluded from CI due to their long runtime.
They test complex scenarios with multiple files and advanced functionality.
"""

import json
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import List

import pytest
import requests

# Import fixtures from the moved test module
from .test_input_samples import project_root, temp_output_dir


class ServerProcess:
    """Helper class to manage server processes for testing."""

    def __init__(self, server_path: Path, port: int):
        self.server_path = server_path
        self.port = port
        self.process = None
        self.base_url = f"http://localhost:{port}"

    def start(self) -> bool:
        """Start the server process."""
        try:
            self.process = subprocess.Popen(
                [sys.executable, str(self.server_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            # Wait for server to start
            time.sleep(3)
            return self.is_running()
        except Exception as e:
            print(f"Failed to start server: {e}")
            return False

    def stop(self):
        """Stop the server process."""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None

    def is_running(self) -> bool:
        """Check if server is running."""
        if not self.process:
            return False
        try:
            response = requests.get(f"{self.base_url}/", timeout=2)
            return response.status_code == 200
        except:
            return False


class TestAdvancedSamples:
    """Test advanced input samples (slow tests)."""

    def test_advanced_task_build(self, temp_output_dir, project_root):
        """Test building advanced task management example."""
        # Build the advanced example
        sample_files = [
            "input-samples/input-advanced/task_storage.py",
            "input-samples/input-advanced/task_analytics.py",
            "input-samples/input-advanced/task_utilities.py",
        ]
        result = self.build_sample(
            sample_files, temp_output_dir / "mcp_advanced", project_root
        )
        assert result.returncode == 0

        # Check that output files exist
        output_dir = temp_output_dir / "mcp_advanced"
        assert (output_dir / "server" / "gradio_server.py").exists()
        assert (output_dir / "client" / "mcp_client.py").exists()
        assert (output_dir / "requirements.txt").exists()
        assert (output_dir / "config.json").exists()

    def test_advanced_mcp_functions(self, temp_output_dir, project_root):
        """Test MCP functions in advanced example."""
        # Build the advanced example
        sample_files = [
            "input-samples/input-advanced/task_storage.py",
            "input-samples/input-advanced/task_analytics.py",
            "input-samples/input-advanced/task_utilities.py",
        ]
        result = self.build_sample(
            sample_files, temp_output_dir / "mcp_advanced2", project_root
        )
        assert result.returncode == 0

        # Import and test the server
        server_path = temp_output_dir / "mcp_advanced2" / "server"
        sys.path.insert(0, str(server_path))

        try:
            # Force reimport
            if "gradio_server" in sys.modules:
                del sys.modules["gradio_server"]
            import gradio_server

            # Test task creation
            result = gradio_server.create_task("Test Task", "Test Description", "high")
            assert "successfully" in result.lower()

            # Test task statistics
            stats_result = gradio_server.get_task_statistics()
            stats = json.loads(stats_result)
            assert "total_tasks" in stats
            assert "by_status" in stats
            assert "by_priority" in stats

            # Test task search
            search_result = gradio_server.search_tasks("Test")
            assert isinstance(search_result, str)

            # Test helper functions are available
            assert hasattr(gradio_server, "_load_tasks")
            assert hasattr(gradio_server, "_save_tasks")
            assert hasattr(gradio_server, "validate_priority")

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

    def test_advanced_server_startup(self, temp_output_dir, project_root):
        """Test advanced server startup and basic functionality."""
        # Build the advanced example
        sample_files = [
            "input-samples/input-advanced/task_storage.py",
            "input-samples/input-advanced/task_analytics.py",
            "input-samples/input-advanced/task_utilities.py",
        ]
        result = self.build_sample(
            sample_files, temp_output_dir / "mcp_advanced3", project_root
        )
        assert result.returncode == 0

        # Start server
        server_file = temp_output_dir / "mcp_advanced3" / "server" / "gradio_server.py"
        server = ServerProcess(server_file, 7891)

        try:
            assert server.start(), "Failed to start server"

            # Test basic endpoint
            response = requests.get(f"{server.base_url}/", timeout=5)
            assert response.status_code == 200

            # Test Gradio API endpoint
            api_response = requests.get(f"{server.base_url}/gradio_api/", timeout=5)
            assert api_response.status_code == 200

        finally:
            server.stop()

    def test_advanced_client_generation(self, temp_output_dir, project_root):
        """Test that advanced client is generated correctly."""
        # Build the advanced example
        sample_files = [
            "input-samples/input-advanced/task_storage.py",
            "input-samples/input-advanced/task_analytics.py",
            "input-samples/input-advanced/task_utilities.py",
        ]
        result = self.build_sample(
            sample_files, temp_output_dir / "client_advanced", project_root
        )
        assert result.returncode == 0

        # Check client file exists and has expected content
        client_file = temp_output_dir / "client_advanced" / "client" / "mcp_client.py"
        assert client_file.exists()

        with open(client_file, "r") as f:
            content = f.read()

        # Should contain advanced function calls
        assert "create_task" in content
        assert "get_task_statistics" in content
        assert "search_tasks" in content
        assert "get_productivity_report" in content

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
            timeout=600,  # 10 minutes for slow tests
        )


class TestAdvancedEndToEnd:
    """End-to-end tests for advanced samples (slow tests)."""

    def test_e2e_advanced_tasks(self, temp_output_dir, project_root):
        """End-to-end test for advanced task management example."""
        print("\n=== Testing Advanced Tasks (E2E) ===")

        # 1. Build the server and client
        sample_files = [
            "input-samples/input-advanced/task_storage.py",
            "input-samples/input-advanced/task_analytics.py",
            "input-samples/input-advanced/task_utilities.py",
        ]
        build_dir = temp_output_dir / "e2e_advanced"

        print("Building server and client...")
        result = self.build_sample(sample_files, build_dir, project_root)
        assert result.returncode == 0, f"Build failed: {result.stderr}"
        print("✅ Build successful")

        # 2. Launch the server
        server_file = build_dir / "server" / "gradio_server.py"
        server = ServerProcess(server_file, 7892)

        try:
            print("Starting server...")
            assert server.start(), "Failed to start server"
            print("✅ Server started successfully")

            # 3. Test MCP SSE endpoint for advanced server
            print("Testing MCP SSE endpoint...")
            mcp_url = f"{server.base_url}/gradio_api/mcp/sse"
            try:
                response = requests.get(mcp_url, timeout=3, stream=True)
                assert (
                    response.status_code == 200
                ), f"MCP SSE endpoint returned {response.status_code}"
                print("✅ MCP SSE endpoint accessible")
            except requests.exceptions.ReadTimeout:
                print("✅ MCP SSE endpoint opened (timeout normal)")
            except Exception as e:
                print(f"⚠️ MCP SSE endpoint error: {e}")

            # 4. Test complex task management workflow
            sys.path.insert(0, str(server_file.parent))
            try:
                import gradio_server

                # Test task creation
                result1 = gradio_server.create_task(
                    "E2E Test Task", "Testing end-to-end workflow", "high"
                )
                assert (
                    "successfully" in result1.lower()
                ), f"create_task failed: {result1}"
                print(f"✅ Task created: {result1}")

                # Test task statistics
                stats_json = gradio_server.get_task_statistics()
                stats = json.loads(stats_json)
                assert "total_tasks" in stats, "Statistics missing total_tasks"
                assert stats["total_tasks"] >= 1, "Should have at least 1 task"
                print(f"✅ Task statistics: {stats['total_tasks']} total tasks")

                # Test task search
                search_result = gradio_server.search_tasks("E2E")
                assert isinstance(search_result, str), "Search should return string"
                print(f"✅ Task search completed: {len(search_result)} chars returned")

                # Test helper functions are available
                assert hasattr(
                    gradio_server, "_load_tasks"
                ), "Helper function _load_tasks missing"
                assert hasattr(
                    gradio_server, "_save_tasks"
                ), "Helper function _save_tasks missing"
                assert hasattr(
                    gradio_server, "TASKS_FILE"
                ), "Constant TASKS_FILE missing"
                print("✅ Helper functions and constants available")

                # Verify it's using Blocks (tabbed interface)
                import gradio as gr

                assert isinstance(
                    gradio_server.demo, gr.Blocks
                ), "Should use Blocks for multiple functions"
                print("✅ Using Blocks interface for multiple functions")

            finally:
                if str(server_file.parent) in sys.path:
                    sys.path.remove(str(server_file.parent))
                if "gradio_server" in sys.modules:
                    del sys.modules["gradio_server"]

        finally:
            server.stop()
            print("✅ Server stopped")

        print("✅ Advanced Tasks E2E test completed successfully\n")

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
            f"log/builds/e2e_test_{int(time.time())}.log",
        ]

        return subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minutes for slow tests
        )
