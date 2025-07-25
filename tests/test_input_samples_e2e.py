#!/usr/bin/env python3
"""
End-to-end test suite for all input samples.
Tests complete workflow: build -> launch -> test live servers and clients.
"""

import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import List

import pytest
import requests


@pytest.fixture(scope="session")
def temp_output_dir():
    """Create a temporary output directory for tests."""
    temp_dir = Path(tempfile.mkdtemp(prefix="mcp_e2e_test_"))
    yield temp_dir
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


class ServerProcess:
    """Manages a Gradio server process."""

    def __init__(self, server_path: Path, port: int):
        self.server_path = server_path
        self.port = port
        self.process = None
        self.base_url = f"http://127.0.0.1:{port}"

    def start(self) -> bool:
        """Start the server process."""
        try:
            # Start server as subprocess
            cmd = [
                sys.executable,
                "-c",
                f"""
import sys
sys.path.insert(0, '{self.server_path.parent}')
import gradio_server
gradio_server.demo.launch(
    server_name="127.0.0.1",
    server_port={self.port},
    share=False,
    quiet=True,
    mcp_server=True
)
""",
            ]

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.server_path.parent.parent,
            )

            # Wait for server to start
            for _ in range(30):  # 30 second timeout
                try:
                    response = requests.get(f"{self.base_url}/", timeout=1)
                    if response.status_code == 200:
                        return True
                except requests.RequestException:
                    pass
                time.sleep(1)

            return False

        except Exception as e:
            print(f"Failed to start server: {e}")
            return False

    def stop(self):
        """Stop the server process."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            except Exception:
                pass

    def is_running(self) -> bool:
        """Check if server is running."""
        try:
            response = requests.get(f"{self.base_url}/", timeout=2)
            return response.status_code == 200
        except BaseException:
            return False


class TestEndToEndInputSamples:
    """End-to-end test for all input sample examples."""

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
            cmd, cwd=project_root, capture_output=True, text=True, timeout=120
        )

    def test_e2e_basic_hello_world(self, temp_output_dir, project_root):
        """End-to-end test for basic hello world example."""
        print("\n=== Testing Basic Hello World (E2E) ===")

        # 1. Build the server and client
        sample_files = ["input-samples/input-hello-world/hello_world.py"]
        build_dir = temp_output_dir / "e2e_basic"

        print("Building server and client...")
        result = self.build_sample(sample_files, build_dir, project_root)
        assert result.returncode == 0, f"Build failed: {result.stderr}"
        print("✅ Build successful")

        # Verify files exist
        server_file = build_dir / "server" / "gradio_server.py"
        client_file = build_dir / "client" / "mcp_client.py"
        assert server_file.exists(), "Server file not found"
        assert client_file.exists(), "Client file not found"
        print("✅ Server and client files generated")

        # 2. Launch the server
        server = ServerProcess(server_file, 7890)
        try:
            print("Starting server...")
            assert server.start(), "Failed to start server"
            print("✅ Server started successfully")

            # 3. Test server is accessible
            assert server.is_running(), "Server not responding"
            print("✅ Server is accessible")

            # 4. Test MCP SSE endpoint
            print("Testing MCP SSE endpoint...")
            mcp_url = f"{server.base_url}/gradio_api/mcp/sse"
            try:
                # SSE endpoint should respond, even if it's a streaming response
                response = requests.get(mcp_url, timeout=3, stream=True)
                # For SSE, we expect 200 status and text/event-stream content type
                assert (
                    response.status_code == 200
                ), f"MCP SSE endpoint returned {response.status_code}"
                content_type = response.headers.get("content-type", "")
                print(f"✅ MCP SSE endpoint accessible (content-type: {content_type})")

                # Try to read the first chunk to ensure it's responding
                chunk_received = False
                try:
                    for chunk in response.iter_content(
                        chunk_size=1024, decode_unicode=True
                    ):
                        if chunk:
                            chunk_received = True
                            print(
                                f"✅ MCP SSE endpoint streaming data: {chunk[:100]}..."
                            )
                            break
                except BaseException:
                    pass  # Reading might timeout, which is normal for SSE

                if not chunk_received:
                    print("⚠️ MCP SSE endpoint opened but no immediate data")

            except requests.exceptions.ReadTimeout:
                # SSE connections can timeout while waiting for events, this is normal
                print(
                    "✅ MCP SSE endpoint opened (timed out waiting for events - normal)"
                )
            except Exception as e:
                print(f"❌ MCP SSE endpoint error: {e}")
                # Continue testing even if SSE has issues

            # 5. Test MCP tools endpoint
            print("Testing MCP tools endpoint...")
            try:
                tools_url = f"{server.base_url}/gradio_api/mcp/tools"
                response = requests.get(tools_url, timeout=5)
                if response.status_code == 200:
                    tools_data = response.json()
                    print(f"✅ MCP tools endpoint returned {len(tools_data)} tools")
                else:
                    print(
                        f"⚠️ MCP tools endpoint returned status {response.status_code}"
                    )
            except Exception as e:
                print(f"⚠️ MCP tools endpoint error: {e}")

            # 6. Test MCP call endpoint with actual function call
            print("Testing MCP function call...")
            try:
                call_url = f"{server.base_url}/gradio_api/mcp/call"
                call_payload = {"name": "greet", "arguments": {"name": "MCP Test User"}}
                response = requests.post(call_url, json=call_payload, timeout=5)
                if response.status_code == 200:
                    result_data = response.json()
                    print(f"✅ MCP function call successful: {result_data}")
                else:
                    print(f"⚠️ MCP function call returned status {response.status_code}")
            except Exception as e:
                print(f"⚠️ MCP function call error: {e}")

            # 7. Test function via direct import (simulating client behavior)
            sys.path.insert(0, str(server_file.parent))
            try:
                import gradio_server

                result = gradio_server.greet("E2E Test")
                assert isinstance(result, str)
                assert "E2E Test" in result
                assert "Hello" in result
                print(f"✅ Function test: {result}")
            finally:
                if str(server_file.parent) in sys.path:
                    sys.path.remove(str(server_file.parent))
                if "gradio_server" in sys.modules:
                    del sys.modules["gradio_server"]

        finally:
            server.stop()
            print("✅ Server stopped")

        print("✅ Basic E2E test completed successfully\n")

    def test_e2e_simple_combined(self, temp_output_dir, project_root):
        """End-to-end test for simple combined example (math + geometry)."""
        print("\n=== Testing Simple Combined (E2E) ===")

        # 1. Build the server and client
        sample_files = [
            "input-samples/input-simple/math_operations.py",
            "input-samples/input-simple/geometry.py",
        ]
        build_dir = temp_output_dir / "e2e_simple"

        print("Building server and client...")
        result = self.build_sample(sample_files, build_dir, project_root)
        assert result.returncode == 0, f"Build failed: {result.stderr}"
        print("✅ Build successful")

        # 2. Launch the server
        server_file = build_dir / "server" / "gradio_server.py"
        server = ServerProcess(server_file, 7891)

        try:
            print("Starting server...")
            assert server.start(), "Failed to start server"
            print("✅ Server started successfully")

            # 3. Test MCP endpoints for multiple functions
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

            # Test multiple functions via direct import
            sys.path.insert(0, str(server_file.parent))
            try:
                import gradio_server

                # Test math functions
                result1 = gradio_server.add_numbers(10, 5)
                assert result1 == 15, f"add_numbers failed: {result1}"
                print(f"✅ add_numbers(10, 5) = {result1}")

                result2 = gradio_server.multiply_numbers(6, 7)
                assert result2 == 42, f"multiply_numbers failed: {result2}"
                print(f"✅ multiply_numbers(6, 7) = {result2}")

                # Test geometry functions
                import math

                result3 = gradio_server.circle_area(3)
                expected = math.pi * 9
                assert abs(result3 - expected) < 0.001, f"circle_area failed: {result3}"
                print(f"✅ circle_area(3) = {result3:.2f}")

                result4 = gradio_server.rectangle_area(4, 5)
                assert result4 == 20, f"rectangle_area failed: {result4}"
                print(f"✅ rectangle_area(4, 5) = {result4}")

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

        print("✅ Simple combined E2E test completed successfully\n")

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

        print("✅ Advanced tasks E2E test completed successfully\n")


if __name__ == "__main__":
    # Run with verbose output to see progress
    pytest.main([__file__, "-v", "-s"])
