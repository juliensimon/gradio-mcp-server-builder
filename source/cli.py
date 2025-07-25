#!/usr/bin/env python3
"""
Command-line interface for the Gradio MCP Server Builder.

Copyright (c) 2025 Julien Simon <julien@julien.org>
Licensed under CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/
"""

import argparse
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from .builder import GradioMCPBuilder
from .config import Config
from .logging_config import get_logger, setup_logging


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Build MCP servers with Gradio interfaces",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # === MANDATORY ARGUMENTS (alphabetical) ===
    parser.add_argument(
        "input_files",
        nargs="+",
        type=Path,
        help="Input Python files containing MCP functions",
    )

    # === OPTIONAL ARGUMENTS (alphabetical) ===
    parser.add_argument(
        "--device",
        type=str,
        default="mps",
        choices=["cpu", "mps", "cuda"],
        help="Device for inference (default: mps)",
    )

    parser.add_argument(
        "--disable-sample-prompts",
        action="store_true",
        help="Disable generation of sample prompts for the client",
    )

    parser.add_argument(
        "--local-model",
        type=str,
        default="HuggingFaceTB/SmolLM3-3B",
        help="Local Hugging Face model to use (default: HuggingFaceTB/SmolLM3-3B)",
    )

    parser.add_argument(
        "--log-config",
        type=str,
        default="json/log_config.json",
        help="Path to logging configuration file (default: json/log_config.json)",
    )

    parser.add_argument(
        "--log-file",
        type=str,
        default="log/builds/output.log",
        help="Log file name (default: log/builds/output.log)",
    )

    parser.add_argument(
        "--model-config",
        type=str,
        default="json/model_config.json",
        help="Path to model configuration file (default: json/model_config.json)",
    )

    parser.add_argument(
        "--model-endpoint", type=str, help="OpenAI-compatible model endpoint URL"
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Output directory (default: output)",
    )

    parser.add_argument(
        "--port", type=int, default=7860, help="Server port (default: 7860)"
    )

    parser.add_argument(
        "--preserve-docstrings",
        action="store_true",
        help="Keep original docstrings (don't improve them)",
    )

    parser.add_argument("--share", action="store_true", help="Enable Gradio sharing")

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging (sets console to DEBUG level)",
    )

    return parser


def main() -> int:
    """Main entry point for the CLI."""
    # Load environment variables first
    load_dotenv()

    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_config, args.log_file)
    logger = get_logger("cli")

    # Adjust logging level if verbose is enabled
    if args.verbose:
        # Set all loggers to DEBUG level
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # Also set all named loggers to DEBUG
        for name in [
            "builder",
            "parser",
            "generators",
            "model_config",
            "docstring_improver",
        ]:
            named_logger = logging.getLogger(f"gradio_mcp_builder.{name}")
            named_logger.setLevel(logging.DEBUG)

        # Find console handler and set to DEBUG level
        for handler in root_logger.handlers:
            if hasattr(handler, "stream") and (
                handler.stream == sys.stdout
                or getattr(handler.stream, "name", "") == "<stdout>"
                or handler.__class__.__name__ == "StreamHandler"
            ):
                handler.setLevel(logging.DEBUG)
                break

        logger.debug("Enabled verbose logging (DEBUG level)")

    logger.info("Starting MCP server build process")
    logger.debug(f"Command line arguments: {vars(args)}")

    try:
        # Validate input files
        for input_file in args.input_files:
            if not input_file.exists():
                logger.error(f"Input file does not exist: {input_file}")
                return 1
            if not input_file.suffix == ".py":
                logger.error(f"Input file must be a Python file: {input_file}")
                return 1

        logger.info(f"Validated {len(args.input_files)} input file(s)")

        # Create configuration
        config = Config(
            input_files=args.input_files,
            share=args.share,
            model_endpoint=args.model_endpoint,
            preserve_docstrings=args.preserve_docstrings,
            local_model=args.local_model,
            device=args.device,
            output_dir=args.output_dir,
            model_config=args.model_config,
            log_file=args.log_file,
            port=args.port,
            disable_sample_prompts=args.disable_sample_prompts,
        )

        logger.debug(f"Created configuration: {config}")

        # Build the MCP server
        builder = GradioMCPBuilder(config)
        builder.build()

        logger.info(f"Successfully built MCP server in {config.output_dir}/")
        return 0

    except KeyboardInterrupt:
        logger.warning("Build process interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Error building MCP server: {e}")
        logger.debug("Full traceback:", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
