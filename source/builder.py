"""
Main builder class for the Gradio MCP Server Builder.

Copyright (c) 2025 Julien Simon <julien@julien.org>
Licensed under CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/
"""

from typing import Dict, List

from .config import Config
from .docstring_improver import DocstringImprover
from .file_generators import (
    ClientGenerator,
    DocumentationGenerator,
    RequirementsGenerator,
    ServerGenerator,
)
from .gradio_generator import GradioGenerator
from .logging_config import get_logger, log_step
from .parser import MCPFunction, MCPParser


class GradioMCPBuilder:
    """Main builder class that orchestrates the MCP server generation process."""

    def __init__(self, config: Config):
        """Initialize the builder with configuration."""
        self.config = config
        self.logger = get_logger("builder")

        # Initialize components
        self.parser = MCPParser()
        self.docstring_improver = DocstringImprover(config)
        self.gradio_generator = GradioGenerator(config)
        self.server_generator = ServerGenerator(config)
        self.client_generator = ClientGenerator(config)
        self.doc_generator = DocumentationGenerator(config)
        self.req_generator = RequirementsGenerator(config)

        # Data storage
        self.mcp_functions: List[MCPFunction] = []
        self.helper_functions: List[MCPFunction] = []
        self.module_constants: List[str] = []
        self.improved_docstrings: Dict[str, str] = {}
        self.test_prompts: Dict[str, List[str]] = {}

        self.logger.debug(f"Initialized GradioMCPBuilder with config: {config}")

    def build(self) -> None:
        """Build the complete MCP server with Gradio interface."""
        with log_step("MCP server build", self.logger):
            self._parse_input_files()
            self._improve_docstrings()
            self._generate_test_prompts()
            self._create_output_directories()
            self._generate_server_files()
            self._generate_client_files()
            self._generate_documentation()
            self._generate_requirements()
            self._generate_config_file()

    def _parse_input_files(self) -> None:
        """Parse all input files and extract MCP functions."""
        with log_step("Parsing input files", self.logger):
            seen_constants = {}  # Track constants by name to avoid duplicates

            for input_file in self.config.input_files:
                self.logger.info(f"Parsing {input_file.name}...")
                try:
                    result = self.parser.parse_file(input_file)
                    self.mcp_functions.extend(result["mcp_functions"])
                    self.helper_functions.extend(result.get("helper_functions", []))

                    # Handle module constants with deduplication
                    for constant in result.get("module_constants", []):
                        # Extract constant name from the assignment
                        if "=" in constant:
                            const_name = constant.split("=")[0].strip()
                            if const_name not in seen_constants:
                                seen_constants[const_name] = constant
                                self.module_constants.append(constant)
                                self.logger.debug(
                                    f"Added unique constant: {const_name}"
                                )
                            else:
                                self.logger.debug(
                                    f"Skipped duplicate constant: {const_name}"
                                )

                    self.logger.debug(
                        f"Found {len(result['mcp_functions'])} MCP functions, {len(result.get('helper_functions', [
                        ]))} helper functions, and {len(result.get('module_constants', []))} constants in {input_file.name}"
                    )
                except Exception as e:
                    self.logger.error(f"Failed to parse {input_file}: {e}")
                    raise

            self.logger.info(f"Found {len(self.mcp_functions)} MCP functions total")

            if not self.mcp_functions:
                self.logger.error("No MCP functions found in input files")
                raise ValueError("No MCP functions found in input files")

    def _improve_docstrings(self) -> None:
        """Improve docstrings for all functions or preserve originals."""
        if self.config.preserve_docstrings:
            self.logger.info("Preserving original docstrings...")
            for func in self.mcp_functions:
                self.improved_docstrings[func.name] = func.docstring
        else:
            with log_step("Improving docstrings", self.logger):
                for func in self.mcp_functions:
                    self.logger.debug(f"Improving docstring for {func.name}")
                    try:
                        improved = self.docstring_improver.improve_function_docstring(
                            func.name, func.docstring, func.signature
                        )
                        self.improved_docstrings[func.name] = improved
                        self.logger.debug(
                            f"Successfully improved docstring for {func.name}"
                        )
                    except Exception as e:
                        self.logger.warning(
                            f"Failed to improve docstring for {func.name}: {e}"
                        )
                        self.improved_docstrings[func.name] = func.docstring

    def _generate_test_prompts(self) -> None:
        """Generate test prompts for all functions."""
        with log_step("Generating test prompts", self.logger):
            for func in self.mcp_functions:
                self.logger.debug(f"Generating test prompts for {func.name}")
                try:
                    prompts = self.docstring_improver.generate_test_prompts(
                        func.name, self.improved_docstrings[func.name], func.signature
                    )
                    self.test_prompts[func.name] = prompts
                    self.logger.debug(
                        f"Generated {len(prompts)} test prompts for {func.name}"
                    )
                except Exception as e:
                    self.logger.warning(
                        f"Failed to generate test prompts for {func.name}: {e}"
                    )
                    self.test_prompts[func.name] = []

    def _create_output_directories(self) -> None:
        """Create the output directory structure."""
        with log_step("Creating output directories", self.logger):
            directories = [
                self.config.output_dir,
                self.config.output_dir / "server",
                self.config.output_dir / "client",
            ]

            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
                self.logger.debug(f"Created directory: {directory}")

    def _generate_server_files(self) -> None:
        """Generate all server-related files."""
        with log_step("Generating server files", self.logger):
            try:
                # Generate Gradio server
                server_code = self.server_generator.generate_server(
                    self.mcp_functions,
                    self.helper_functions,
                    self.module_constants,
                    self.improved_docstrings,
                )
                server_file = self.config.output_dir / "server" / "gradio_server.py"
                server_file.write_text(server_code)
                self.logger.debug(f"Generated Gradio server: {server_file}")

                # Generate server __init__.py
                init_code = self.server_generator.generate_init_file(self.mcp_functions)
                init_file = self.config.output_dir / "server" / "__init__.py"
                init_file.write_text(init_code)
                self.logger.debug(f"Generated server __init__.py: {init_file}")

                self.logger.info("Successfully generated server files")
            except Exception as e:
                self.logger.error(f"Failed to generate server files: {e}")
                raise

    def _generate_client_files(self) -> None:
        """Generate client-related files."""
        with log_step("Generating client files", self.logger):
            try:
                client_code = self.client_generator.generate_client(
                    self.mcp_functions, self.test_prompts
                )
                client_file = self.config.output_dir / "client" / "mcp_client.py"
                client_file.write_text(client_code)
                self.logger.debug(f"Generated MCP client: {client_file}")

                self.logger.info("Successfully generated client files")
            except Exception as e:
                self.logger.error(f"Failed to generate client files: {e}")
                raise

    def _generate_documentation(self) -> None:
        """Generate documentation files."""
        with log_step("Generating documentation", self.logger):
            try:
                readme_content = self.doc_generator.generate_readme(
                    self.mcp_functions, self.improved_docstrings, self.test_prompts
                )
                readme_file = self.config.output_dir / "README.md"
                readme_file.write_text(readme_content)
                self.logger.debug(f"Generated README: {readme_file}")

                self.logger.info("Successfully generated documentation")
            except Exception as e:
                self.logger.error(f"Failed to generate documentation: {e}")
                raise

    def _generate_requirements(self) -> None:
        """Generate requirements.txt file."""
        with log_step("Generating requirements.txt", self.logger):
            try:
                requirements_content = self.req_generator.generate_requirements()
                requirements_file = self.config.output_dir / "requirements.txt"
                requirements_file.write_text(requirements_content)
                self.logger.debug(f"Generated requirements: {requirements_file}")

                self.logger.info("Successfully generated requirements.txt")
            except Exception as e:
                self.logger.error(f"Failed to generate requirements.txt: {e}")
                raise

    def _generate_config_file(self) -> None:
        """Generate configuration file for server and client coordination."""
        with log_step("Generating config file", self.logger):
            import json
            from datetime import datetime

            config_data = {
                "server_port": self.config.port,
                "client_port": self.config.port + 1,
                "mcp_sse_endpoint": f"http://127.0.0.1:{self.config.port}/gradio_api/mcp/sse",
                "generated_at": datetime.now().isoformat(),
            }

            config_file = self.config.output_dir / "config.json"
            with open(config_file, "w") as f:
                json.dump(config_data, f, indent=2)

            self.logger.debug(
                f"Generated config.json with server port {self.config.port}"
            )
