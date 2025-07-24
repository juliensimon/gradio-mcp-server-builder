"""
Model configuration management for the Gradio MCP Builder.
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .logging_config import get_logger


@dataclass
class LocalModelConfig:
    """Configuration for local Hugging Face models."""
    default_model: str
    generation_params: Dict[str, Any]
    tokenizer_params: Dict[str, Any]
    model_loading: Dict[str, Any]
    device_specific: Dict[str, Dict[str, Any]]


@dataclass
class ApiModelConfig:
    """Configuration for API-based models."""
    default_model: str
    generation_params: Dict[str, Any]
    request_params: Dict[str, Any]


@dataclass
class PromptConfig:
    """Configuration for prompt templates and cleanup."""
    docstring_improvement: Dict[str, Any]
    test_prompt_generation: Dict[str, Any]


@dataclass
class PerformanceConfig:
    """Performance-related configuration."""
    batch_size: int
    gradient_checkpointing: bool
    use_cache: bool
    attention_implementation: str


@dataclass
class FallbackConfig:
    """Fallback configuration for error handling."""
    docstring_template: str
    test_prompt_template: str
    error_handling: Dict[str, Any]


@dataclass
class ModelConfig:
    """Complete model configuration."""
    local_model: LocalModelConfig
    api_model: ApiModelConfig
    prompts: PromptConfig
    performance: PerformanceConfig
    fallback: FallbackConfig


class ModelConfigLoader:
    """Loads and manages model configuration from JSON file."""
    
    def __init__(self, config_path: str = "model_config.json"):
        """Initialize the config loader."""
        self.config_path = Path(config_path)
        self.logger = get_logger("model_config")
        self._config: Optional[ModelConfig] = None
        
        self.logger.debug(f"Initialized ModelConfigLoader with path: {config_path}")
    
    def load_config(self) -> ModelConfig:
        """Load configuration from JSON file."""
        if self._config is not None:
            return self._config
        
        self.logger.debug(f"Loading model config from: {self.config_path}")
        
        if not self.config_path.exists():
            self.logger.warning(f"Model config file not found: {self.config_path}")
            return self._create_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
            
            self._config = self._parse_config(config_data)
            self.logger.info(f"Successfully loaded model config from {self.config_path}")
            return self._config
            
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            self.logger.error(f"Failed to load model config: {e}")
            self.logger.warning("Using default configuration")
            return self._create_default_config()
    
    def _parse_config(self, config_data: Dict[str, Any]) -> ModelConfig:
        """Parse configuration data into structured config objects."""
        
        local_model = LocalModelConfig(
            default_model=config_data["local_model"]["default_model"],
            generation_params=config_data["local_model"]["generation_params"],
            tokenizer_params=config_data["local_model"]["tokenizer_params"],
            model_loading=config_data["local_model"]["model_loading"],
            device_specific=config_data["local_model"]["device_specific"]
        )
        
        api_model = ApiModelConfig(
            default_model=config_data["api_model"]["default_model"],
            generation_params=config_data["api_model"]["generation_params"],
            request_params=config_data["api_model"]["request_params"]
        )
        
        prompts = PromptConfig(
            docstring_improvement=config_data["prompts"]["docstring_improvement"],
            test_prompt_generation=config_data["prompts"]["test_prompt_generation"]
        )
        
        performance = PerformanceConfig(
            batch_size=config_data["performance"]["batch_size"],
            gradient_checkpointing=config_data["performance"]["gradient_checkpointing"],
            use_cache=config_data["performance"]["use_cache"],
            attention_implementation=config_data["performance"]["attention_implementation"]
        )
        
        fallback = FallbackConfig(
            docstring_template=config_data["fallback"]["docstring_template"],
            test_prompt_template=config_data["fallback"]["test_prompt_template"],
            error_handling=config_data["fallback"]["error_handling"]
        )
        
        return ModelConfig(
            local_model=local_model,
            api_model=api_model,
            prompts=prompts,
            performance=performance,
            fallback=fallback
        )
    
    def _create_default_config(self) -> ModelConfig:
        """Create a default configuration when file is missing or invalid."""
        self.logger.info("Creating default model configuration")
        
        local_model = LocalModelConfig(
            default_model="HuggingFaceTB/SmolLM3-3B",
            generation_params={
                "max_new_tokens": 200,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9,
                "top_k": 50,
                "repetition_penalty": 1.1
            },
            tokenizer_params={
                "max_length": 512,
                "truncation": True,
                "padding": True,
                "return_tensors": "pt"
            },
            model_loading={
                "torch_dtype": "auto",
                "low_cpu_mem_usage": True,
                "trust_remote_code": False
            },
            device_specific={
                "cpu": {"torch_dtype": "float32", "device_map": {"": "cpu"}},
                "mps": {"torch_dtype": "float16", "device_map": None},
                "cuda": {"torch_dtype": "float16", "device_map": "auto"}
            }
        )
        
        api_model = ApiModelConfig(
            default_model="gpt-3.5-turbo",
            generation_params={
                "max_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            },
            request_params={
                "timeout": 30,
                "max_retries": 3,
                "retry_delay": 1.0
            }
        )
        
        prompts = PromptConfig(
            docstring_improvement={
                "user_prompt_template": "Generate ONLY a clean docstring for this function. Return just the docstring text, nothing else.\n\nFunction: {function_name}\nSignature: {signature}\nCurrent docstring: {current_docstring}\n\nReturn ONLY the docstring content (without triple quotes) that explains:\n- What the function does\n- Parameters and their types\n- Return value and type\n\nDocstring:",
                "cleanup_patterns": ["^```.*", "^Here's?.*", "^The function.*", "^Revised.*", "def .*"]
            },
            test_prompt_generation={
                "user_prompt_template": "Generate {num_prompts} different test prompts that a user might ask to invoke this MCP function.\n\nFunction: {function_name}\nSignature: {signature}\nDocstring: {docstring}\n\nGenerate {num_prompts} natural language prompts that would trigger this function. Make them varied and realistic:",
                "num_prompts": 3
            }
        )
        
        performance = PerformanceConfig(
            batch_size=1,
            gradient_checkpointing=False,
            use_cache=True,
            attention_implementation="eager"
        )
        
        fallback = FallbackConfig(
            docstring_template="Performs {function_name} operation.",
            test_prompt_template="Test {function_name} with various inputs",
            error_handling={"max_retries": 2, "fallback_on_error": True, "log_errors": True}
        )
        
        return ModelConfig(
            local_model=local_model,
            api_model=api_model,
            prompts=prompts,
            performance=performance,
            fallback=fallback
        )
    
    def get_device_config(self, device: str) -> Dict[str, Any]:
        """Get device-specific configuration."""
        config = self.load_config()
        device_config = config.local_model.device_specific.get(device, {})
        
        self.logger.debug(f"Retrieved device config for {device}: {device_config}")
        return device_config
    
    def get_generation_params(self, use_local: bool = True) -> Dict[str, Any]:
        """Get generation parameters for local or API models."""
        config = self.load_config()
        
        if use_local:
            params = config.local_model.generation_params.copy()
            self.logger.debug(f"Retrieved local model generation params: {params}")
        else:
            params = config.api_model.generation_params.copy()
            self.logger.debug(f"Retrieved API model generation params: {params}")
        
        return params
    
    def format_prompt(self, prompt_type: str, **kwargs) -> str:
        """Format a prompt template with the given variables."""
        config = self.load_config()
        
        if prompt_type == "docstring":
            template = config.prompts.docstring_improvement["user_prompt_template"]
        elif prompt_type == "test_prompts":
            template = config.prompts.test_prompt_generation["user_prompt_template"]
        else:
            self.logger.warning(f"Unknown prompt type: {prompt_type}")
            return kwargs.get("fallback", "")
        
        try:
            formatted = template.format(**kwargs)
            self.logger.debug(f"Formatted {prompt_type} prompt (length: {len(formatted)})")
            return formatted
        except KeyError as e:
            self.logger.error(f"Missing variable for {prompt_type} prompt: {e}")
            return kwargs.get("fallback", "")
    
    def clean_generated_text(self, text: str, prompt_type: str = "docstring") -> str:
        """Clean generated text using configured cleanup patterns."""
        config = self.load_config()
        
        if prompt_type == "docstring":
            patterns = config.prompts.docstring_improvement.get("cleanup_patterns", [])
        else:
            patterns = []
        
        cleaned_lines = []
        for line in text.strip().split('\n'):
            line = line.strip()
            
            # Skip lines matching cleanup patterns
            skip_line = False
            for pattern in patterns:
                if re.match(pattern, line):
                    skip_line = True
                    break
            
            if not skip_line and line:
                cleaned_lines.append(line)
        
        result = '\n    '.join(cleaned_lines) if cleaned_lines else text
        self.logger.debug(f"Cleaned text from {len(text)} to {len(result)} characters")
        return result 