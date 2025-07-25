# Command Line Options

Complete reference for all command line options available in the Gradio MCP
Server Builder.

## Basic Syntax

```bash
python main.py [input_files] [options]
```

## Input Files

### Positional Arguments

| Argument | Description | Required | | ------------- |
------------------------------------------------- | -------- | | `input_files` |
One or more Python files containing MCP functions | Yes |

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

| Option | Description | Default | Example | | -------------- |
------------------------------------ | -------- | ------------------------ | |
`--output-dir` | Output directory for generated files | `output` |
`--output-dir my_server` | | `--port` | Port for the generated server | `7860` |
`--port 8080` |

### Model Configuration

| Option                                    | Description                | Default            | Example          |     | ------------------ |
| ----------------------------------------- | -------------------------- | ------------------ | ---------------- | --- | ------------------ |
| ----------------------------------------- |                            | `--local-model`    | Local Hugging    |
| Face model name                           | `HuggingFaceTB/SmolLM3-3B` |
| `--local-model microsoft/DialoGPT-medium` |                            | `--model-endpoint` |
| OpenAI-compatible API endpoint            | `None`                     |
| `--model-endpoint http://localhost:8000`  |                            | `--device`         | Device for model |
| inference                                 | `mps`                      | `--device cuda`    |

### Behavior Control

| Option | Description | Default | Example | | -------------------------- |
-------------------------------- | ------- | -------------------------- | |
`--preserve-docstrings` | Keep original docstrings | `False` |
`--preserve-docstrings` | | `--disable-sample-prompts` | Disable sample prompt
generation | `False` | `--disable-sample-prompts` | | `--share` | Enable Gradio
sharing | `False` | `--share` |

### Configuration Files

| Option                             | Description                    | Default        | Example                       |        | ---------------- |
| ---------------------------------- | ------------------------------ | -------------- | ----------------------------- | ------ | ---------------- |
| ---------------------------------- |                                | `--env-file`   | Path to .env file             | `None` |
| `--env-file .env`                  |                                | `--log-config` | Path to logging configuration |
| `json/log_config.json`             | `--log-config custom_log.json` |                | `--model-config`              |
| Path to model configuration        | `json/model_config.json`       |
| `--model-config custom_model.json` |                                | `--log-file`   | Path to log file              |
| `log/builds/output.log`            | `--log-file custom.log`        |

## Detailed Option Reference

### --output-dir

Specify the output directory for generated files.

```bash
# Default output directory
python main.py functions.py

# Custom output directory
python main.py functions.py --output-dir my_custom_server

# Relative path
python main.py functions.py --output-dir ./builds/server_v1

# Absolute path
python main.py functions.py --output-dir /Users/me/projects/my_server
```

**Generated Structure:**

```
my_custom_server/
├── server/
│   ├── gradio_server.py
│   └── __init__.py
├── client/
│   └── mcp_client.py
├── README.md
├── requirements.txt
└── config.json
```

### --port

Set the port for the generated Gradio server.

```bash
# Default port (7860)
python main.py functions.py

# Custom port
python main.py functions.py --port 8080

# High port number
python main.py functions.py --port 9000
```

**Note:** The port must be available and you must have permission to bind to it.

### --local-model

Specify a local Hugging Face model for docstring improvement.

```bash
# Default model
python main.py functions.py

# Different model
python main.py functions.py --local-model "microsoft/DialoGPT-medium"

# Large model (requires more memory)
python main.py functions.py --local-model "gpt2-large"

# Custom model from your account
python main.py functions.py --local-model "username/custom-model"
```

**Popular Models:**

`HuggingFaceTB/SmolLM3-3B` is the default model that provides a good balance of
speed and quality. For faster processing with smaller models, consider
`microsoft/DialoGPT-medium` or `gpt2`. If you need better quality and can afford
the larger model size, `gpt2-medium` offers improved results.

### --model-endpoint

Use an OpenAI-compatible API endpoint instead of a local model.

```bash
# Local model (default)
python main.py functions.py

# OpenAI API
python main.py functions.py --model-endpoint https://api.openai.com/v1

# Local Ollama
python main.py functions.py --model-endpoint http://localhost:11434/v1

# Custom API
python main.py functions.py --model-endpoint https://api.example.com/v1
```

**Environment Variables:** When using API endpoints, you may need to set
environment variables:

```bash
# For OpenAI
export OPENAI_API_KEY="your-api-key"

# For custom endpoints
export API_KEY="your-api-key"
```

### --device

Specify the device for model inference.

```bash
# Automatic detection (default)
python main.py functions.py

# CPU only
python main.py functions.py --device cpu

# CUDA GPU
python main.py functions.py --device cuda

# MPS (Apple Silicon)
python main.py functions.py --device mps
```

**Device Support:**

**CPU** works on all systems but provides slower processing. **CUDA** is
available only on NVIDIA GPUs and offers the fastest performance for model
inference. **MPS** is exclusive to Apple Silicon Macs and provides fast
acceleration without requiring CUDA.

### --preserve-docstrings

Keep original docstrings instead of improving them with AI.

```bash
# Improve docstrings (default)
python main.py functions.py

# Keep original docstrings
python main.py functions.py --preserve-docstrings
```

**Use Cases:**

Use this option when you have well-written docstrings that you want to preserve
exactly. It's also useful for faster builds since it skips AI processing
entirely. Choose this option when you want to maintain exact wording, for
testing and development scenarios, when working with sensitive or proprietary
information, or when you have domain-specific knowledge that AI models might
miss or misinterpret.

**Important Note**: Docstrings are crucial for MCP tool discovery. AI
improvement can significantly enhance tool discoverability, but always review
generated docstrings for accuracy. Poor docstrings can make your tools difficult
for AI assistants to find and use effectively.

### --disable-sample-prompts

Disable generation of sample prompts for the MCP client.

```bash
# Generate sample prompts (default)
python main.py functions.py

# Disable sample prompts
python main.py functions.py --disable-sample-prompts
```

**Benefits:**

Disabling sample prompts results in faster builds and smaller generated files.
This option is ideal when you don't need sample prompts for your use case or
when you want to minimize the output size.

### --share

Enable Gradio sharing to create a public URL.

```bash
# Local only (default)
python main.py functions.py

# Public URL
python main.py functions.py --share
```

**Features:**

The sharing feature creates a public URL (e.g., `https://xxx.gradio.live`) that
makes your server accessible from anywhere on the internet. This URL is
temporary and expires when the server stops, making it perfect for demos and
sharing your work with others.

### --env-file

Load configuration from a .env file.

```bash
# No .env file (default)
python main.py functions.py

# Load from .env
python main.py functions.py --env-file .env

# Custom .env file
python main.py functions.py --env-file config.env
```

**Example .env file:**

```env
# Model configuration
MODEL_ENDPOINT=http://localhost:8000
LOCAL_MODEL=custom-model
DEVICE=cuda

# Server configuration
PORT=8080
SHARE=true

# Logging
LOG_LEVEL=DEBUG
```

### --log-config

Specify a custom logging configuration file.

```bash
# Default logging config
python main.py functions.py

# Custom logging config
python main.py functions.py --log-config config/debug_logging.json

# Production logging
python main.py functions.py --log-config config/production_logging.json
```

**Example logging config:**

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "detailed": {
      "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "level": "DEBUG",
      "formatter": "detailed"
    }
  },
  "loggers": {
    "gradio_mcp_builder": {
      "level": "DEBUG",
      "handlers": ["console"],
      "propagate": false
    }
  }
}
```

### --model-config

Specify a custom model configuration file.

```bash
# Default model config
python main.py functions.py

# Custom model config
python main.py functions.py --model-config config/creative_model.json

# Precise model config
python main.py functions.py --model-config config/precise_model.json
```

**Example model config:**

```json
{
  "local_model": {
    "default_model": "HuggingFaceTB/SmolLM3-3B",
    "generation_params": {
      "max_new_tokens": 300,
      "temperature": 0.7,
      "do_sample": true
    }
  },
  "prompts": {
    "docstring_improvement": {
      "user_prompt_template": "Improve this docstring..."
    }
  }
}
```

### --log-file

Specify the path for the log file.

```bash
# Default log file
python main.py functions.py

# Custom log file
python main.py functions.py --log-file logs/build.log

# Timestamped log file
python main.py functions.py --log-file logs/build_$(date +%Y%m%d_%H%M%S).log
```

## Common Usage Patterns

### Development Setup

```bash
# Fast development builds
python main.py functions.py \
    --preserve-docstrings \
    --disable-sample-prompts \
    --output-dir dev_output
```

### Production Setup

```bash
# Production-ready builds
python main.py functions.py \
    --model-config config/production_model.json \
    --log-config config/production_logging.json \
    --log-file logs/production_build.log \
    --output-dir production_server
```

### Testing Setup

```bash
# Testing with custom configuration
python main.py functions.py \
    --env-file test.env \
    --output-dir test_output \
    --port 9000
```

### Sharing Setup

```bash
# Public demo
python main.py functions.py \
    --share \
    --model-endpoint https://api.openai.com/v1 \
    --output-dir demo_server
```

## Environment Variables

You can also configure the tool using environment variables:

```bash
# Set environment variables
export GRADIO_MCP_OUTPUT_DIR="custom_output"
export GRADIO_MCP_PORT="8080"
export GRADIO_MCP_LOCAL_MODEL="microsoft/DialoGPT-medium"
export GRADIO_MCP_DEVICE="cuda"
export GRADIO_MCP_SHARE="true"

# Run without command line options
python main.py functions.py
```

**Supported Environment Variables:**

The tool supports several environment variables for configuration:
`GRADIO_MCP_OUTPUT_DIR` for custom output directories, `GRADIO_MCP_PORT` for
server port configuration, `GRADIO_MCP_LOCAL_MODEL` for specifying local models,
`GRADIO_MCP_MODEL_ENDPOINT` for API endpoints, `GRADIO_MCP_DEVICE` for device
selection, `GRADIO_MCP_SHARE` for sharing configuration,
`GRADIO_MCP_PRESERVE_DOCSTRINGS` for docstring preservation, and
`GRADIO_MCP_DISABLE_SAMPLE_PROMPTS` for disabling sample prompt generation.

## Help and Information

### Get Help

```bash
# Show help
python main.py --help

# Show version
python main.py --version
```

### Verbose Output

```bash
# Verbose logging
python main.py functions.py --log-config config/debug_logging.json
```

## Next Steps

**[Input Format Guide](input-format.md)** - Learn how to structure your input
files with proper decorators, type hints, and documentation for optimal results.

**[Code Parsing and Analysis](code-parsing.md)** - Understand how the tool
analyzes your code, including function detection, signature analysis, and
docstring processing.

**[Configuration Guide](../configuration/overview.md)** - Customize behavior and
settings to match your specific requirements and deployment environment.
