#!/usr/bin/env python3
"""
Gradio MCP Server Builder - Main Entry Point

A CLI tool to automatically build MCP servers with Gradio from Python function files.

Copyright (c) 2025 Julien Simon <julien@julien.org>
Licensed under CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/
"""

import sys
from pathlib import Path

from source.cli import main

# Add source to path
sys.path.insert(0, str(Path(__file__).parent / "source"))


if __name__ == "__main__":
    sys.exit(main())
