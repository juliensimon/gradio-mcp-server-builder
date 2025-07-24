# Model Configuration Guide

The Gradio MCP Builder supports extensive model configuration through the `model_config.json` file. This allows you to fine-tune model behavior, prompts, and performance parameters without modifying code.

## Configuration File Structure

The model configuration is organized into several sections:

### 1. Local Model Configuration (`local_model`)

Configure parameters for local Hugging Face models:

```json
{
  "local_model": {
    "default_model": "HuggingFaceTB/SmolLM3-3B",
    "generation_params": {
      "max_new_tokens": 300,
      "temperature": 0.9,
      "do_sample": true,
      "top_p": 0.95,
      "top_k": 40,
      "repetition_penalty": 1.2,
      "num_return_sequences": 1,
      "early_stopping": true,
      "length_penalty": 1.0
    },
    "device_specific": {
      "cpu": {
        "torch_dtype": "float32",
        "device_map": {"": "cpu"}
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
}
```

**Key Parameters:**
- **`max_new_tokens`**: Maximum tokens to generate (higher = longer responses)
- **`temperature`**: Creativity level (0.1 = conservative, 1.0+ = creative)
- **`top_p`**: Nucleus sampling threshold (0.9-0.95 recommended)
- **`top_k`**: Top-k sampling limit (40-50 typical)
- **`repetition_penalty`**: Prevents repetition (1.1-1.2 recommended)

### 2. API Model Configuration (`api_model`)

Configure parameters for OpenAI-compatible API endpoints:

```json
{
  "api_model": {
    "default_model": "gpt-3.5-turbo",
    "generation_params": {
      "max_tokens": 300,
      "temperature": 0.8,
      "top_p": 0.95,
      "frequency_penalty": 0.1,
      "presence_penalty": 0.1
    },
    "request_params": {
      "timeout": 30,
      "max_retries": 3,
      "retry_delay": 1.0
    }
  }
}
```

### 3. Prompt Configuration (`prompts`)

Customize prompt templates and text cleanup:

```json
{
  "prompts": {
    "docstring_improvement": {
      "user_prompt_template": "Generate ONLY a clean docstring for this function...",
      "cleanup_patterns": [
        "^```.*",
        "^Here's?.*",
        "^The function.*"
      ]
    },
    "test_prompt_generation": {
      "user_prompt_template": "Generate {num_prompts} different test prompts...",
      "num_prompts": 5
    }
  }
}
```

**Template Variables:**
- **Docstring prompts**: `{function_name}`, `{signature}`, `{current_docstring}`
- **Test prompt generation**: `{function_name}`, `{signature}`, `{docstring}`, `{num_prompts}`

### 4. Performance Configuration (`performance`)

Optimize model performance:

```json
{
  "performance": {
    "batch_size": 1,
    "gradient_checkpointing": false,
    "use_cache": true,
    "attention_implementation": "eager"
  }
}
```

### 5. Fallback Configuration (`fallback`)

Configure error handling and fallback behavior:

```json
{
  "fallback": {
    "docstring_template": "Performs {function_name} operation with optimized parameters.",
    "test_prompt_template": "Test {function_name} with various realistic inputs",
    "error_handling": {
      "max_retries": 3,
      "fallback_on_error": true,
      "log_errors": true
    }
  }
}
```

## Usage Examples

### Creative Docstrings

For more creative and detailed docstrings:

```json
{
  "local_model": {
    "generation_params": {
      "temperature": 0.9,
      "top_p": 0.95,
      "max_new_tokens": 400
    }
  }
}
```

### Conservative/Consistent Output

For more predictable, consistent output:

```json
{
  "local_model": {
    "generation_params": {
      "temperature": 0.3,
      "top_p": 0.8,
      "top_k": 20
    }
  }
}
```

### Custom Model

To use a different Hugging Face model:

```json
{
  "local_model": {
    "default_model": "microsoft/DialoGPT-medium",
    "generation_params": {
      "max_new_tokens": 150,
      "temperature": 0.7
    }
  }
}
```

### More Test Prompts

To generate more test prompts per function:

```json
{
  "prompts": {
    "test_prompt_generation": {
      "num_prompts": 7,
      "user_prompt_template": "Generate {num_prompts} varied, realistic test prompts for this MCP function..."
    }
  }
}
```

## CLI Integration

Specify a custom model configuration file:

```bash
python main.py input/functions.py --model-config custom_model.json
```

## Device-Specific Optimization

The configuration automatically optimizes for different devices:

- **CPU**: Uses `float32` precision, explicit CPU device mapping
- **MPS (Apple Silicon)**: Uses `float16` for better performance
- **CUDA**: Uses `float16` with automatic device mapping

## Logging Integration

Model configuration activities are logged:

```
2025-07-24 18:21:15 - gradio_mcp_builder.model_config - INFO - Successfully loaded model config from model_config.json
2025-07-24 18:21:15 - gradio_mcp_builder.model_config - DEBUG - Retrieved local model generation params: {'max_new_tokens': 300, 'temperature': 0.9, ...}
```

## Best Practices

1. **Start with defaults**: Use the provided `model_config.json` as a baseline
2. **Adjust gradually**: Make small changes to temperature/top_p first
3. **Test different models**: Try various Hugging Face models for your use case
4. **Monitor logs**: Check logs to see which parameters are being applied
5. **Balance creativity vs consistency**: Higher temperature = more creative but less predictable

## Troubleshooting

- **Model loading issues**: Check `torch_dtype` and `device_map` settings
- **Generation quality**: Adjust `temperature`, `top_p`, and `repetition_penalty`
- **Performance**: Modify `max_new_tokens` and enable `gradient_checkpointing` for large models
- **API timeouts**: Increase `timeout` in `request_params`

## Example Configurations

### For Code Documentation
```json
{
  "local_model": {
    "generation_params": {
      "temperature": 0.4,
      "max_new_tokens": 200,
      "repetition_penalty": 1.1
    }
  }
}
```

### For Creative Descriptions
```json
{
  "local_model": {
    "generation_params": {
      "temperature": 0.8,
      "max_new_tokens": 350,
      "top_p": 0.95
    }
  }
}
```

The model configuration system provides complete control over AI model behavior while maintaining ease of use and sensible defaults. 