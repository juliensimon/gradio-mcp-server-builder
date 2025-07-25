"""
Parser for extracting MCP functions from Python files using AST analysis.
"""

import ast
import inspect
from pathlib import Path
from typing import Any, Dict, List

from .logging_config import get_logger


class MCPFunction:
    """Represents an MCP function with its metadata."""

    def __init__(self, name: str, func: Any, docstring: str, signature: str):
        self.name = name
        self.func = func
        self.docstring = docstring
        self.signature = signature
        try:
            self.source_code = inspect.getsource(func)
            self.line_number = inspect.getsourcelines(func)[1]
        except (OSError, TypeError):
            # Fallback for functions that can't get source
            self.source_code = f"def {name}{signature}:\n    pass"
            self.line_number = 1

    def __repr__(self) -> str:
        return f"MCPFunction(name='{self.name}', signature='{self.signature}')"


class MCPParser:
    """Parser for extracting MCP functions and metadata from Python files."""

    def __init__(self):
        self.logger = get_logger("parser")
        self.mcp_functions: List[MCPFunction] = []
        self.other_functions: List[MCPFunction] = []
        self.module_docstring: str = ""

        self.logger.debug("Initialized MCPParser")

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a Python file and extract mcp functions."""
        self.logger.debug(f"parsing file: {file_path}")

        # Reset for each file
        self.mcp_functions = []
        self.other_functions = []
        module_imports = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract module docstring and imports
            tree = ast.parse(content)
            self.module_docstring = ast.get_docstring(tree) or ""
            self.logger.debug(
                f"extracted module docstring (length: {len(self.module_docstring)})"
            )

            # Extract module-level imports
            for node in tree.body:
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_imports.append(f"import {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        if node.names[0].name == "*":
                            module_imports.append(f"from {node.module} import *")
                        else:
                            names = [alias.name for alias in node.names]
                            module_imports.append(
                                f"from {node.module} import {', '.join(names)}"
                            )

            # Find functions with @mcp.tool() decorator and helper functions using AST
            mcp_function_count = 0
            helper_functions = []
            module_constants = []

            # Extract module-level constants/variables (only top-level assignments)
            for node in tree.body:  # Only look at top-level nodes
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            try:
                                # Extract the complete assignment including multi-line
                                # values
                                lines = content.split("\n")
                                start_line = (
                                    node.lineno - 1
                                )  # Convert to 0-based indexing

                                # Find the end of the assignment by looking for the next
                                # statement at the same indentation level
                                assignment_indent = len(lines[start_line]) - len(
                                    lines[start_line].lstrip()
                                )
                                end_line = len(lines)

                                for i in range(start_line + 1, len(lines)):
                                    line = lines[i]
                                    if line.strip():  # Non-empty line
                                        current_indent = len(line) - len(line.lstrip())
                                        # If we find a line at the same or less
                                        # indentation that starts a new statement
                                        if current_indent <= assignment_indent and (
                                            line.strip().startswith("def ")
                                            or line.strip().startswith("class ")
                                            or line.strip().startswith("@")
                                            or (
                                                "=" in line
                                                and not line.strip().startswith("#")
                                            )
                                        ):
                                            end_line = i
                                            break

                                # Extract the complete multi-line assignment
                                constant_lines = lines[start_line:end_line]
                                if constant_lines:
                                    # Join lines and clean up
                                    constant_def = "\n".join(constant_lines).strip()
                                    if (
                                        constant_def
                                        and not constant_def.startswith("#")
                                        and "=" in constant_def
                                    ):
                                        module_constants.append(constant_def)
                                        self.logger.debug(
                                            f"found module constant: {target.id} = {len(constant_def)} chars"
                                        )
                            except Exception as e:
                                self.logger.warning(
                                    f"failed to extract constant {target.id}: {e}"
                                )

            # Look at top-level nodes to avoid nested functions
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    # Handle standalone functions
                    has_mcp_decorator = any(
                        isinstance(decorator, ast.Call)
                        and isinstance(decorator.func, ast.Attribute)
                        and isinstance(decorator.func.value, ast.Name)
                        and decorator.func.value.id == "mcp"
                        and decorator.func.attr == "tool"
                        for decorator in node.decorator_list
                    )
                    if has_mcp_decorator:
                        try:
                            func_source = self._extract_function_source(content, node)
                            docstring = ast.get_docstring(node) or ""
                            signature = self._build_signature_string(node)
                            mcp_func = MCPFunction(
                                node.name, None, docstring, signature
                            )
                            mcp_func.source_code = func_source
                            mcp_func.line_number = node.lineno
                            mcp_func.module_imports = module_imports
                            self.mcp_functions.append(mcp_func)
                            mcp_function_count += 1
                            self.logger.debug(
                                f"found mcp function: {node.name} at line {node.lineno}"
                            )
                        except Exception as e:
                            self.logger.warning(
                                f"failed to process mcp function {node.name}: {e}"
                            )
                    else:
                        # Collect helper functions (non-MCP functions)
                        try:
                            func_source = self._extract_function_source(content, node)
                            docstring = ast.get_docstring(node) or ""
                            signature = self._build_signature_string(node)
                            helper_func = MCPFunction(
                                node.name, None, docstring, signature
                            )
                            helper_func.source_code = func_source
                            helper_func.line_number = node.lineno
                            helper_func.module_imports = module_imports
                            helper_functions.append(helper_func)
                            self.logger.debug(
                                f"found helper function: {node.name} at line {node.lineno}"
                            )
                        except Exception as e:
                            self.logger.warning(
                                f"failed to process helper function {node.name}: {e}"
                            )
                elif isinstance(node, ast.ClassDef):
                    # Handle class methods
                    for class_node in node.body:
                        if isinstance(class_node, ast.FunctionDef):
                            has_mcp_decorator = any(
                                isinstance(decorator, ast.Call)
                                and isinstance(decorator.func, ast.Attribute)
                                and isinstance(decorator.func.value, ast.Name)
                                and decorator.func.value.id == "mcp"
                                and decorator.func.attr == "tool"
                                for decorator in class_node.decorator_list
                            )
                            if has_mcp_decorator:
                                try:
                                    func_source = self._extract_function_source(
                                        content, class_node
                                    )
                                    docstring = ast.get_docstring(class_node) or ""
                                    signature = self._build_signature_string(class_node)
                                    mcp_func = MCPFunction(
                                        class_node.name, None, docstring, signature
                                    )
                                    mcp_func.source_code = func_source
                                    mcp_func.line_number = class_node.lineno
                                    mcp_func.module_imports = module_imports
                                    self.mcp_functions.append(mcp_func)
                                    mcp_function_count += 1
                                    self.logger.debug(
                                        f"found mcp class method: {class_node.name} at line {class_node.lineno}"
                                    )
                                except Exception as e:
                                    self.logger.warning(
                                        f"failed to process mcp class method {class_node.name}: {e}"
                                    )
                            else:
                                # Collect helper class methods (non-MCP functions)
                                try:
                                    func_source = self._extract_function_source(
                                        content, class_node
                                    )
                                    docstring = ast.get_docstring(class_node) or ""
                                    signature = self._build_signature_string(class_node)
                                    helper_func = MCPFunction(
                                        class_node.name, None, docstring, signature
                                    )
                                    helper_func.source_code = func_source
                                    helper_func.line_number = class_node.lineno
                                    helper_func.module_imports = module_imports
                                    helper_functions.append(helper_func)
                                    self.logger.debug(
                                        f"found helper class method: {class_node.name} at line {class_node.lineno}"
                                    )
                                except Exception as e:
                                    self.logger.warning(
                                        f"failed to process helper class method {class_node.name}: {e}"
                                    )

            self.logger.info(
                f"successfully parsed {file_path.name}: {mcp_function_count} mcp functions found"
            )

            return {
                "mcp_functions": self.mcp_functions,
                "helper_functions": helper_functions,
                "module_constants": module_constants,
                "other_functions": self.other_functions,
                "module_docstring": self.module_docstring,
                "module_imports": module_imports,
                "content": content,
            }

        except Exception as e:
            self.logger.error(f"failed to parse file {file_path}: {e}")
            raise

    def _extract_function_source(self, content: str, node: ast.FunctionDef) -> str:
        """Extract the complete source code for a function from the original content."""
        self.logger.debug(f"Extracting source for function: {node.name}")

        lines = content.split("\n")

        # Find the start of the function (including decorators)
        start_line = node.lineno - 1  # Convert to 0-based indexing

        # Look for decorators before the function
        for i in range(start_line - 1, -1, -1):
            line = lines[i].strip()
            if line.startswith("@"):
                start_line = i
            elif line and not line.startswith("#"):
                break

        # Find the end of the function by looking for the next function or class
        # at the same indentation level
        func_indent = len(lines[node.lineno - 1]) - len(lines[node.lineno - 1].lstrip())
        end_line = len(lines)

        for i in range(node.lineno, len(lines)):
            line = lines[i]
            if line.strip():  # Non-empty line
                current_indent = len(line) - len(line.lstrip())
                # If we find a line at the same or less indentation that starts a new
                # definition
                if current_indent <= func_indent and (
                    line.strip().startswith("def ")
                    or line.strip().startswith("class ")
                    or line.strip().startswith("@")
                ):
                    end_line = i
                    break

        result = "\n".join(lines[start_line:end_line])
        self.logger.debug(
            f"Extracted {end_line - start_line} lines of source for {node.name}"
        )
        return result

    def _build_signature_string(self, node: ast.FunctionDef) -> str:
        """Build a signature string from an AST FunctionDef node."""
        self.logger.debug(f"Building signature for function: {node.name}")

        args = []

        # Handle regular arguments
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            args.append(arg_str)

        signature = f"({', '.join(args)})"

        # Add return annotation if present
        if node.returns:
            signature += f" -> {ast.unparse(node.returns)}"

        self.logger.debug(f"Built signature for {node.name}: {signature}")
        return signature
