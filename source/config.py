"""
Configuration management for the Gradio MCP Server Builder.

Copyright (c) 2025 Julien Simon <julien@julien.org>
Licensed under CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class Config:
    """Configuration for the Gradio MCP Builder."""
    input_files: List[Path]
    share: bool = False
    model_endpoint: Optional[str] = None
    preserve_docstrings: bool = False
    local_model: str = "HuggingFaceTB/SmolLM3-3B"
    device: str = "mps"
    output_dir: Path = Path("output")
    model_config: str = "json/model_config.json"
    log_file: str = "log/builds/output.log"
    port: int = 7860
    disable_sample_prompts: bool = False
    
    def __post_init__(self):
        """Validate and set up configuration after initialization."""
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up subdirectories
        self.server_dir = self.output_dir / "server"
        self.client_dir = self.output_dir / "client"
        self.tests_dir = self.output_dir / "tests"
        
        # Create subdirectories
        for directory in [self.server_dir, self.client_dir, self.tests_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @property
    def use_local_model(self) -> bool:
        """Whether to use a local model instead of an API endpoint."""
        return self.model_endpoint is None
    
    @property
    def model_name(self) -> str:
        """Get the model name to use."""
        return self.local_model if self.use_local_model else "openai-compatible"
    
    @property
    def is_mac_with_mps(self) -> bool:
        """Whether the current device is set to MPS."""
        return self.device == "mps" 