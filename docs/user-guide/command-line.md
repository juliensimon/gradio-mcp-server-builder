# Command Line Options

Complete reference for all command line options available in the Gradio MCP
Server Builder.

## Basic Syntax

```bash
python main.py [input_files] [options]
```

## Input Files

### Positional Arguments

- **`input_files`** - One or more Python files containing MCP functions
  (required)

### Examples

```bash
# Single file
python main.py functions.py

# Multiple files
python main.py file1.py file2.py file3.py

# With wildcards (shell expansion)
python main.py input/*.py
```

## Core Options

### Output Configuration

- **`--output-dir`** - Output directory for generated files
  - Default: `output`
  - Example: `--output-dir my_server`

- **`--port`** - Port for the generated server
  - Default: `7860`
  - Example: `--port 8080`

### Model Configuration

- **`--local-model`** - Local Hugging Face model to use
  - Default: `HuggingFaceTB/SmolLM3-3B`
  - Example: `--local-model microsoft/DialoGPT-medium`

- **`--model-endpoint`** - OpenAI-compatible model endpoint URL
  - Default: None
  - Example: `--model-endpoint http://localhost:8000`

- **`--model-config`** - Path to model configuration file
  - Default: `json/model_config.json`
  - Example: `--model-config config/custom_model.json`

- **`--device`** - Device for inference
  - Default: `mps`
  - Example: `--device cuda`

### Logging Configuration

- **`--log-config`** - Path to logging configuration file
  - Default: `json/log_config.json`
  - Example: `--log-config config/debug.json`

- **`--log-file`** - Log file name
  - Default: `log/builds/output.log`
  - Example: `--log-file custom.log`

- **`--verbose`, `-v`** - Enable verbose logging (sets console to DEBUG level)
  - Default: False
  - Example: `--verbose`

### Behavior Options

- **`--preserve-docstrings`** - Keep original docstrings (don't improve them)
  - Default: False
  - Example: `--preserve-docstrings`

- **`--share`** - Enable Gradio sharing
  - Default: False
  - Example: `--share`

- **`--disable-sample-prompts`** - Disable generation of sample prompts for the
  client
  - Default: False
  - Example: `--disable-sample-prompts`

## Device Options

The `--device` option controls which hardware to use for model inference:

- **`cpu`** - CPU inference
  - Use case: When no GPU is available or for compatibility

- **`mps`** - Apple Silicon GPU (Metal Performance Shaders)
  - Use case: Mac with M1/M2/M3 chips (default)

- **`cuda`** - NVIDIA GPU
  - Use case: Windows/Linux with NVIDIA GPU

## Examples

### Basic Usage

```bash
# Simple build with default settings
python main.py functions.py

# Build with custom output directory
python main.py functions.py --output-dir my_server

# Build with custom port
python main.py functions.py --port 8080
```

### Model Configuration

```bash
# Use a local Hugging Face model
python main.py functions.py --local-model "microsoft/DialoGPT-medium"

# Use an OpenAI-compatible endpoint
python main.py functions.py --model-endpoint http://localhost:8000

# Use CPU for inference
python main.py functions.py --device cpu

# Use NVIDIA GPU
python main.py functions.py --device cuda
```

### Logging and Debugging

```bash
# Enable verbose logging
python main.py functions.py --verbose

# Use custom logging configuration
python main.py functions.py --log-config config/examples/debug_logging.json

# Specify custom log file
python main.py functions.py --log-file log/custom_build.log
```

### Advanced Options

```bash
# Preserve original docstrings
python main.py functions.py --preserve-docstrings

# Enable Gradio sharing (creates public URL)
python main.py functions.py --share

# Disable sample prompt generation
python main.py functions.py --disable-sample-prompts
```

### Complete Example

```bash
python main.py input/functions.py \
    --share \
    --model-endpoint http://localhost:8000 \
    --preserve-docstrings \
    --local-model custom-model \
    --output-dir custom-output \
    --device cuda \
    --verbose \
    --log-config config/examples/debug_logging.json
```

## Environment Variables

The tool automatically loads environment variables from a `.env` file if
present. Common variables include:

- `OPENAI_API_KEY` - For OpenAI API access
- `HUGGINGFACE_TOKEN` - For Hugging Face model access
- `MODEL_ENDPOINT` - Default model endpoint URL

## Configuration Files

### Model Configuration

The `--model-config` option allows you to specify custom model behavior:

```json
{
  "temperature": 0.7,
  "max_tokens": 1000,
  "top_p": 0.9,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0
}
```

### Logging Configuration

The `--log-config` option allows you to customize logging behavior:

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "standard": {
      "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "level": "INFO",
      "formatter": "standard"
    }
  },
  "root": {
      "handlers": ["console"],
    "level": "INFO"
  }
}
```

## Tips and Best Practices

1. **Start Simple**: Begin with `--preserve-docstrings` to test your functions
1. **Use Verbose Logging**: Enable `--verbose` when troubleshooting
1. **Test Locally**: Use `--device cpu` for compatibility testing
1. **Custom Output**: Use `--output-dir` to organize multiple builds
1. **Share Carefully**: Only use `--share` when you want public access
1. **Monitor Logs**: Check log files for detailed build information

## Next Steps

- **[Input Format](input-format.md)** - Learn how to write MCP functions
- **[Configuration](../configuration/overview.md)** - Advanced configuration
  options
- **[Testing Guide](testing.md)** - Comprehensive testing strategies
