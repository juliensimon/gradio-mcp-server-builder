"""
Logging configuration for the Gradio MCP Builder.
"""

import json
import logging
import logging.config
from pathlib import Path
from typing import Any, Dict


def setup_logging(
    config_path: str = "log_config.json", log_file: str = "output.log"
) -> None:
    """
    Setup logging configuration from JSON file.

    Args:
        config_path: Path to the logging configuration JSON file
        log_file: Name of the log file to use
    """
    config_file = Path(config_path)

    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = json.load(f)

            # Update file handler filenames with the custom log file name
            _update_log_filenames(config, log_file)

            logging.config.dictConfig(config)
        except (json.JSONDecodeError, Exception) as e:
            # Fallback to basic logging if config file is invalid
            logging.basicConfig(
                level=logging.INFO,
                format="%(levelname)s - %(message)s",
                handlers=[logging.StreamHandler(), logging.FileHandler(log_file)],
            )
            logging.error(f"Failed to load logging config from {config_path}: {e}")
    else:
        # Default logging configuration if no config file exists
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(), logging.FileHandler(log_file)],
        )
        logging.warning(
            f"Logging config file {config_path} not found. Using default configuration."
        )


def _update_log_filenames(config: Dict[str, Any], log_file: str) -> None:
    """
    Update log file names in the configuration.

    Args:
        config: Logging configuration dictionary
        log_file: Custom log file name to use
    """
    # Create the log directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    handlers = config.get("handlers", {})

    # Update main log file handlers
    for handler_name, handler_config in handlers.items():
        if handler_config.get("class") in [
            "logging.FileHandler",
            "logging.handlers.RotatingFileHandler",
        ]:
            current_filename = handler_config.get("filename", "")

            # Update specific log files based on pattern
            if "gradio_mcp_builder.log" in current_filename:
                handler_config["filename"] = log_file
            elif "app.log" in current_filename:
                handler_config["filename"] = log_file
            elif "debug.log" in current_filename:
                handler_config["filename"] = log_file
            elif current_filename in [
                "gradio_mcp_builder_errors.log",
                "errors.log",
                "error.log",
            ]:
                # Keep error log separate but update extension to match
                log_path = Path(log_file)
                error_log_path = (
                    log_path.parent / f"{log_path.stem}_errors{log_path.suffix}"
                )
                handler_config["filename"] = str(error_log_path)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: Name of the logger (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(f"gradio_mcp_builder.{name}")


def log_function_call(func):
    """
    Decorator to log function calls with arguments and return values.

    Args:
        func: Function to decorate

    Returns:
        Decorated function
    """

    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__.split(".")[-1])
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed with error: {e}")
            raise

    return wrapper


def log_step(step_name: str, logger: logging.Logger = None):
    """
    Context manager to log the start and completion of a step.

    Args:
        step_name: Name of the step being logged
        logger: Logger to use (defaults to main logger)
    """

    class StepLogger:
        def __init__(self, name: str, log: logging.Logger):
            self.name = name
            self.logger = log or get_logger("main")

        def __enter__(self):
            self.logger.debug(f"Starting {self.name}...")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                self.logger.debug(f"Completed {self.name}")
            else:
                self.logger.error(f"Failed {self.name}: {exc_val}")

    return StepLogger(step_name, logger)
