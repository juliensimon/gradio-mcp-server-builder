"""
Gradio interface generator for MCP functions.
"""

from typing import Dict, List

from .parser import MCPFunction


class GradioGenerator:
    """Generates Gradio interfaces for MCP functions."""

    def __init__(self, config):
        self.config = config

    def generate_gradio_interface(
        self, mcp_functions: List[MCPFunction], improved_docstrings: Dict[str, str]
    ) -> str:
        """Generate Gradio interface code."""
        if len(mcp_functions) == 1:
            return self._generate_single_interface(
                mcp_functions[0], improved_docstrings[mcp_functions[0].name]
            )
        else:
            return self._generate_tabbed_interface(mcp_functions, improved_docstrings)

    def _generate_single_interface(
        self, func: MCPFunction, improved_docstring: str
    ) -> str:
        """Generate a single Gradio interface for one function."""
        params = self._extract_params_from_signature(func.signature)

        inputs = []
        for param_name, param_type in params:
            if param_type == "float":
                inputs.append(f'gr.Number(label="{param_name}", value=1.0)')
            elif param_type == "int":
                inputs.append(f'gr.Number(label="{param_name}", value=1, precision=0)')
            elif param_type == "bool":
                inputs.append(f'gr.Checkbox(label="{param_name}", value=False)')
            else:  # str or other
                inputs.append(f'gr.Textbox(label="{param_name}", value="")')

        # Generate example inputs
        examples = []
        for param_name, param_type in params:
            if param_type == "float":
                examples.append("1.5")
            elif param_type == "int":
                examples.append("1")
            elif param_type == "bool":
                examples.append("True")
            else:
                examples.append('"hello"')

        inputs_str = ",\n            ".join(inputs)
        return f'''
import gradio as gr
from server.mcp_server import {func.name}

def interface():
    return gr.Interface(
        fn={func.name},
        inputs=[
            {inputs_str},
        ],
        outputs=gr.Textbox(label="Result"),
        title="{func.name.replace('_', ' ').title()}",
        description="""{improved_docstring}""",
        examples=[
            [{', '.join(examples)}]
        ]
    )

if __name__ == "__main__":
    interface().launch(share={self.config.share})
'''

    def _generate_tabbed_interface(
        self, functions: List[MCPFunction], improved_docstrings: Dict[str, str]
    ) -> str:
        """Generate a tabbed Gradio interface for multiple functions."""
        tab_interfaces = []

        for func in functions:
            params = self._extract_params_from_signature(func.signature)

            inputs = []
            for param_name, param_type in params:
                if param_type == "float":
                    inputs.append(f'gr.Number(label="{param_name}", value=1.0)')
                elif param_type == "int":
                    inputs.append(
                        f'gr.Number(label="{param_name}", value=1, precision=0)'
                    )
                elif param_type == "bool":
                    inputs.append(f'gr.Checkbox(label="{param_name}", value=False)')
                else:  # str or other
                    inputs.append(f'gr.Textbox(label="{param_name}", value="")')

            # Generate example inputs
            examples = []
            for param_name, param_type in params:
                if param_type == "float":
                    examples.append("1.5")
                elif param_type == "int":
                    examples.append("1")
                elif param_type == "bool":
                    examples.append("True")
                else:
                    examples.append('"hello"')

            inputs_str = ",\n                    ".join(inputs)
            tab_interface = f'''
        with gr.Tab("{func.name.replace('_', ' ').title()}"):
            gr.Interface(
                fn={func.name},
                inputs=[
                    {inputs_str},
                ],
                outputs=gr.Textbox(label="Result"),
                description="""{improved_docstrings[func.name]}""",
                examples=[
                    [{', '.join(examples)}]
                ]
            )'''
            tab_interfaces.append(tab_interface)

        return f"""
import gradio as gr
from server.mcp_server import {', '.join([func.name for func in functions])}

def interface():
    with gr.Blocks() as demo:
        gr.Markdown("# MCP Server Interface")
        gr.Markdown("Multiple function interface for MCP server")

        with gr.Tabs():
{''.join(tab_interfaces)}

    return demo

if __name__ == "__main__":
    interface().launch(share={self.config.share})
"""

    def _generate_examples(self, func: MCPFunction) -> str:
        """Generate example inputs for a function."""
        import inspect

        sig = inspect.signature(func.func)
        params = list(sig.parameters.keys())

        # Generate simple examples based on parameter types
        examples = []
        for param in params:
            param_info = sig.parameters[param]
            if param_info.annotation == float:
                examples.append("1.5")
            elif param_info.annotation == int:
                examples.append("1")
            elif param_info.annotation == str:
                examples.append('"test"')
            elif param_info.annotation == bool:
                examples.append("True")
            else:
                examples.append('"test"')

        return f"[{', '.join(examples)}]"

    def _extract_params_from_signature(self, signature: str):
        """Extract parameters from signature string."""
        # Parse signature like "(a: float, b: float) -> float"
        if not signature.startswith("("):
            return []

        # Extract parameter part
        param_part = signature.split(")")[0][1:]  # Remove '(' and everything after ')'

        params = []
        if param_part.strip():
            for param in param_part.split(","):
                param = param.strip()
                if ":" in param:
                    name, type_str = param.split(":", 1)
                    name = name.strip()
                    type_str = type_str.strip()
                    params.append((name, type_str))
                else:
                    params.append((param, "str"))  # Default to str

        return params
