# Configuration Guide

The Gradio MCP Builder supports comprehensive configuration through JSON files
for both logging and model behavior. This guide explains how to customize both
systems.

## Quick Start

```bash
# Use default configurations
python main.py input/functions.py

# Use custom configurations
python main.py input/functions.py --log-config config/examples/debug_logging.json --model-config config/examples/creative_model.json
```

## Logging Configuration

Control logging behavior through the `--log-config` parameter (default:
`log_config.json`).

### Default Logging Setup

The default configuration provides:

- **Console**: Clean INFO-level messages for user feedback
- **File**: Detailed DEBUG logs in `gradio_mcp_builder.log`
- **Error File**: ERROR-level logs in `gradio_mcp_builder_errors.log`

### Example Configurations

#### Debug Logging (`config/examples/debug_logging.json`)

Maximum verbosity for development and troubleshooting:

```bash
python main.py input/functions.py --log-config config/examples/debug_logging.json
```

Features:

- DEBUG level on console with timestamps and function names
- Comprehensive file logging with detailed formatting
- All components log to console for immediate feedback

#### Production Logging (`config/examples/production_logging.json`)

Optimized for production environments:

```bash
python main.py input/functions.py --log-config config/examples/production_logging.json
```

Features:

- Clean console output (INFO level only)
- Rotating log files to manage disk space
- JSON-formatted error logs for easy parsing
- Minimal logging for internal components

### Custom Logging Configuration

Create your own logging configuration by copying and modifying the examples:

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "custom": {
      "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "level": "INFO",
      "formatter": "custom"
    }
  },
  "loggers": {
    "gradio_mcp_builder": {
      "level": "INFO",
      "handlers": ["console"],
      "propagate": false
    }
  }
}
```

## Model Configuration

Control AI model behavior through the `--model-config` parameter (default:
`model_config.json`).

### Default Model Setup

The default configuration provides:

- Balanced creativity/precision (temperature: 0.7)
- Moderate response length (300 tokens)
- Device-optimized settings (CPU/MPS/CUDA)
- Standard prompt templates

### Example Configurations

#### Creative Model (`config/examples/creative_model.json`)

For detailed, creative docstrings and comprehensive test prompts:

```bash
python main.py input/functions.py --model-config config/examples/creative_model.json
```

Features:

- Higher creativity (temperature: 0.9)
- Longer responses (400 tokens)
- Detailed prompt templates
- 7 test prompts per function
- GPT-4 for API mode

#### Precise Model (`config/examples/precise_model.json`)

For concise, conservative output:

```bash
python main.py input/functions.py --model-config config/examples/precise_model.json
```

Features:

- Lower creativity (temperature: 0.3)
- Shorter responses (150 tokens)
- Concise prompt templates
- 3 test prompts per function
- Faster generation

### Key Configuration Sections

#### Generation Parameters

Control AI creativity and response length:

```json
{
  "local_model": {
    "generation_params": {
      "max_new_tokens": 300, // Response length
      "temperature": 0.7, // Creativity (0.1-1.0+)
      "top_p": 0.9, // Nucleus sampling
      "top_k": 50, // Top-k sampling
      "repetition_penalty": 1.1 // Avoid repetition
    }
  }
}
```

#### Prompt Templates

Customize how the AI is instructed:

````json
{
  "prompts": {
    "docstring_improvement": {
      "user_prompt_template": "Generate a docstring for {function_name}...",
      "cleanup_patterns": ["^```.*", "^Here's?.*"]
    },
    "test_prompt_generation": {
      "num_prompts": 5,
      "user_prompt_template": "Generate {num_prompts} test prompts..."
    }
  }
}
````

#### Device Optimization

Automatic optimization for different hardware:

```json
{
  "device_specific": {
    "cpu": {
      "torch_dtype": "float32",
      "device_map": { "": "cpu" }
    },
    "mps": {
      "torch_dtype": "float16",
      "device_map": null
    },
    "cuda": {
      "torch_dtype": "float16",
      "device_map": "auto"
    }
  }
}
```

## Combined Usage Examples

### Development Setup

Debug everything with creative output:

```bash
python main.py input/functions.py \
  --log-config config/examples/debug_logging.json \
  --model-config config/examples/creative_model.json \
  --verbose
```

### Production Setup

Clean logging with precise output:

```bash
python main.py input/functions.py \
  --log-config config/examples/production_logging.json \
  --model-config config/examples/precise_model.json \
  --device cuda
```

### Custom Combinations

Mix and match configurations:

```bash
# Creative model with production logging
python main.py input/functions.py \
  --log-config config/examples/production_logging.json \
  --model-config config/examples/creative_model.json

# Debug logging with precise model
python main.py input/functions.py \
  --log-config config/examples/debug_logging.json \
  --model-config config/examples/precise_model.json
```

## Creating Custom Configurations

### 1. Start with Examples

Copy an existing configuration that's closest to your needs:

```bash
cp config/examples/creative_model.json my_custom_model.json
cp config/examples/debug_logging.json my_custom_logging.json
```

### 2. Modify Parameters

Edit the JSON files to match your requirements:

```json
// For faster, more focused responses
{
  "local_model": {
    "generation_params": {
      "max_new_tokens": 100,
      "temperature": 0.4,
      "top_p": 0.8
    }
  }
}
```

### 3. Test and Iterate

Test your configuration and adjust as needed:

```bash
python main.py input/functions.py \
  --model-config my_custom_model.json \
  --log-config my_custom_logging.json
```

## Configuration Validation

Both configuration systems include robust error handling:

- **Missing files**: Graceful fallback to defaults
- **Invalid JSON**: Error logging with fallback
- **Missing parameters**: Automatic default substitution
- **Type errors**: Safe parameter conversion

## Environment Integration

Configurations work seamlessly with environment variables:

```bash
# Set API key for model endpoints
export OPENAI_API_KEY="your-api-key"

# Use environment-specific configs
python main.py input/functions.py \
  --model-config configs/${ENVIRONMENT}_model.json \
  --log-config configs/${ENVIRONMENT}_logging.json
```

## Troubleshooting

### Common Issues

1. **Configuration not loading**:
   - Check file path and permissions
   - Validate JSON syntax
   - Check logs for error messages

1. **Model parameters ignored**:
   - Verify parameter names match expected format
   - Check device compatibility
   - Review generation parameter limits

1. **Logging not working**:
   - Ensure log directory exists and is writable
   - Check formatter syntax
   - Verify handler configuration

### Debug Mode

Use debug logging to troubleshoot configuration issues:

```bash
python main.py input/functions.py \
  --log-config config/examples/debug_logging.json \
  --verbose
```

This provides maximum visibility into configuration loading and parameter
application.

## Best Practices

1. **Version control**: Keep configurations in source control
1. **Environment-specific**: Use different configs for dev/staging/prod
1. **Documentation**: Comment your custom configurations
1. **Testing**: Test configuration changes with sample inputs
1. **Monitoring**: Use appropriate logging levels for your environment
1. **Performance**: Balance creativity with speed based on your needs

The configuration system provides complete control over the CLI tool's behavior
while maintaining ease of use and robust defaults.
