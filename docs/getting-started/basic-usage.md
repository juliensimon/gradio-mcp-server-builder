# Basic Usage

Learn the fundamentals of using the Gradio MCP Server Builder.

## Command Line Interface

The main command format is:

```bash
python main.py [input_files] [options]
```

### Basic Command

```bash
python main.py input/functions.py
```

### Multiple Input Files

```bash
python main.py input/file1.py input/file2.py input/file3.py
```

### With Options

```bash
python main.py input/functions.py \
    --share \
    --model-endpoint http://localhost:8000 \
    --preserve-docstrings \
    --local-model custom-model \
    --output-dir custom-output
```

## Command Line Options

### Core Options

- **`--device`** - Device for inference (default: `mps`)
  - Options: `cpu`, `mps`, `cuda`
  - Example: `--device cuda`

- **`--disable-sample-prompts`** - Disable generation of sample prompts
  - Default: False
  - Example: `--disable-sample-prompts`

- **`--local-model`** - Local Hugging Face model to use
  - Default: `HuggingFaceTB/SmolLM3-3B`
  - Example: `--local-model microsoft/DialoGPT-medium`

- **`--log-config`** - Path to logging configuration file
  - Default: `json/log_config.json`
  - Example: `--log-config config/debug.json`

- **`--log-file`** - Log file name
  - Default: `log/builds/output.log`
  - Example: `--log-file custom.log`

- **`--model-config`** - Path to model configuration file
  - Default: `json/model_config.json`
  - Example: `--model-config config/custom.json`

- **`--model-endpoint`** - OpenAI-compatible model endpoint URL
  - Default: None
  - Example: `--model-endpoint http://localhost:8000`

- **`--output-dir`** - Output directory
  - Default: `output`
  - Example: `--output-dir my_server`

- **`--port`** - Server port
  - Default: `7860`
  - Example: `--port 8080`

- **`--preserve-docstrings`** - Keep original docstrings
  - Default: False
  - Example: `--preserve-docstrings`

- **`--share`** - Enable Gradio sharing
  - Default: False
  - Example: `--share`

- **`--verbose`, `-v`** - Enable verbose logging
  - Default: False
  - Example: `--verbose`

## Quick Start Examples

### 1. Simple Build

```bash
# Basic build with default settings
python main.py functions.py
```

This creates:

- MCP server in `output/server/`
- Test client in `output/client/`
- Documentation in `output/README.md`

### 2. Custom Output

```bash
# Build with custom output directory
python main.py functions.py --output-dir my_server

# Build with custom port
python main.py functions.py --port 8080
```

### 3. Model Configuration

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

### 4. Logging and Debugging

```bash
# Enable verbose logging
python main.py functions.py --verbose

# Use custom logging configuration
python main.py functions.py --log-config config/examples/debug_logging.json

# Specify custom log file
python main.py functions.py --log-file log/custom_build.log
```

### 5. Advanced Options

```bash
# Preserve original docstrings
python main.py functions.py --preserve-docstrings

# Enable Gradio sharing (creates public URL)
python main.py functions.py --share

# Disable sample prompt generation
python main.py functions.py --disable-sample-prompts
```

## Device Options

The `--device` option controls which hardware to use for model inference:

- **`cpu`** - CPU inference
  - Use case: When no GPU is available or for compatibility

- **`mps`** - Apple Silicon GPU (Metal Performance Shaders)
  - Use case: Mac with M1/M2/M3 chips (default)

- **`cuda`** - NVIDIA GPU
  - Use case: Windows/Linux with NVIDIA GPU

## Complete Example

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

## What Gets Generated

After running the command, you'll find:

```
output/
├── server/
│   ├── gradio_server.py     # Main Gradio interface
│   └── __init__.py          # Package initialization
├── client/
│   └── mcp_client.py       # MCP client with examples
├── README.md                # Documentation
└── requirements.txt         # Dependencies
```

### Running the Generated Server

```bash
cd output
python server/gradio_server.py
```

Then visit `http://127.0.0.1:7860` (or your custom port) in your browser.

### Testing with the MCP Client

```bash
cd output
python client/mcp_client.py
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

- **[Input Format](user-guide/input-format.md)** - Learn how to write MCP
  functions
- **[Configuration](configuration/overview.md)** - Advanced configuration
  options
- **[Testing Guide](user-guide/testing.md)** - Comprehensive testing strategies
