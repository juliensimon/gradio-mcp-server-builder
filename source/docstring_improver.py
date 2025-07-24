"""
Docstring improvement and test prompt generation using AI models.
"""

import os
import re
import time
from typing import List, Optional

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from .config import Config
from .model_config import ModelConfigLoader
from .logging_config import get_logger


class DocstringImprover:
    """Handles improving docstrings and generating test prompts using AI models."""
    
    def __init__(self, config: Config):
        """Initialize the docstring improver."""
        self.config = config
        self.logger = get_logger("docstring_improver")
        self.model_config_loader = ModelConfigLoader(config.model_config)
        self._model = None
        self._tokenizer = None
        self._printed_improving_message = False
        
        self.logger.debug(f"Initialized DocstringImprover with config: {config}")
    
    def _print_improving_message_once(self):
        """Print the improving message only once, when we actually start improving."""
        if not self._printed_improving_message and not self.config.preserve_docstrings:
            self.logger.info("Improving docstrings...")
            self._printed_improving_message = True

    def _clean_docstring_syntax(self, docstring: str) -> str:
        """Clean docstring to prevent syntax errors and force proper format."""
        if not docstring:
            return "Function documentation."
        
        # Remove multiple consecutive quotes
        docstring = re.sub(r'"{3,}', '"""', docstring)
        docstring = re.sub(r"'{3,}", "'''", docstring)
        
        # Remove extra quotes at the beginning and end
        docstring = docstring.strip('\'"')
        
        # Aggressively remove any lines that look like instructions or meta-commentary
        lines = docstring.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Skip lines that look like instructions or meta-commentary
            skip_patterns = [
                r'^make sure',
                r'^please',
                r'^note',
                r'^also note',
                r'^for example',
                r'^lastly',
                r'^ensure',
                r'^currently',
                r'^generated',
                r'^corrected',
                r'^accurate',
                r'^standard',
                r'^compliant',
                r'^formatted',
                r'^version',
                r'^include exactly',
                r'^additional output',
                r'^outside these markers',
                r'^assumptions',
                r'^contents inside',
                r'^guessing',
                r'^unless explicitly',
                r'^leave out',
                r'^assume which',
                r'^special cases',
                r'^edge conditions',
                r'def\s+\w+\(',
                r'^```',
                r'here\'?s',
                r'revised',
                r'triple quotes',
                r'markers'
            ]
            
            # Check if line matches any skip pattern
            should_skip = False
            for pattern in skip_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    should_skip = True
                    break
            
            if should_skip:
                continue
                
            # Remove asterisks and other markdown formatting
            line = re.sub(r'^\*+\s*', '', line)
            line = re.sub(r'\s*\*+$', '', line)
            
            # Remove leading/trailing asterisks
            if line.startswith('*') and line.endswith('*') and len(line) > 2:
                line = line[1:-1].strip()
            
            # Only add substantial lines
            if line and len(line) > 3:
                cleaned_lines.append(line)
        
        # Join lines back together
        docstring = '\n'.join(cleaned_lines).strip()
        
        # Ensure it doesn't contain problematic characters
        docstring = re.sub(r'["""]{4,}', '"""', docstring)
        
        # If the result is empty, too short, or contains suspicious content, use fallback
        suspicious_phrases = [
            'make sure', 'include exactly', 'triple quotes', 'wait wait', 
            'i see you', 'much shorter', 'last response', 'just return',
            'markdown', 'section', 'better still', 'even better',
            'without markdown', 'plain doc', 'separate them',
            'i\'d say', 'simply', 'as follows', 'or even'
        ]
        
        contains_suspicious = any(phrase in docstring.lower() for phrase in suspicious_phrases)
        
        if (not docstring or 
            len(docstring) < 10 or 
            contains_suspicious or
            '###' in docstring or 
            '####' in docstring or
            'returns' not in docstring.lower() and 'args' not in docstring.lower() and len(docstring) > 50):
            return "Function documentation."
        
        return docstring
    
    def _create_template_docstring(self, function_name: str, signature: str, current_docstring: str) -> str:
        """Create a simple template-based docstring when AI generation fails."""
        # If we have a decent current docstring, use it
        if current_docstring and len(current_docstring) > 10 and 'no docstring' not in current_docstring.lower():
            return current_docstring
        
        # Parse signature to get parameters
        import re
        param_match = re.search(r'\((.*?)\)', signature)
        params = []
        
        if param_match:
            param_str = param_match.group(1).strip()
            if param_str:
                # Simple parameter parsing
                for param in param_str.split(','):
                    param = param.strip()
                    if ':' in param:
                        param_name = param.split(':')[0].strip()
                        param_type = param.split(':')[1].strip()
                        params.append(f"{param_name} ({param_type}): Parameter description")
                    elif param and param != 'self':
                        params.append(f"{param}: Parameter description")
        
        # Create a basic docstring
        if params:
            param_section = "\n\nArgs:\n    " + "\n    ".join(params)
            return f"{function_name.replace('_', ' ').title()} function.{param_section}\n\nReturns:\n    Operation result"
        else:
            return f"{function_name.replace('_', ' ').title()} function that performs the specified operation."
    
    def improve_function_docstring(self, function_name: str, current_docstring: str, signature: str) -> str:
        """Improve a function's docstring using AI."""
        if self.config.preserve_docstrings:
            return current_docstring
        
        self.logger.debug(f"Improving docstring for function: {function_name}")
        
        # Use configurable prompt template
        prompt = self.model_config_loader.format_prompt(
            "docstring",
            function_name=function_name,
            signature=signature,
            current_docstring=current_docstring or 'No docstring provided',
            fallback=f"Improve docstring for {function_name}"
        )
        
        try:
            generated = self._generate_text(prompt)
            
            # Use configurable text cleanup
            cleaned = self.model_config_loader.clean_generated_text(generated, "docstring")
            
            # Additional docstring-specific cleaning to prevent syntax errors
            cleaned = self._clean_docstring_syntax(cleaned)
            
            # If cleaning resulted in a fallback, create a better template-based docstring
            if cleaned == "Function documentation.":
                cleaned = self._create_template_docstring(function_name, signature, current_docstring)
            
            result = cleaned if cleaned else current_docstring or f"Performs {function_name} operation."
            self.logger.debug(f"Successfully improved docstring for {function_name}")
            return result
            
        except Exception as e:
            self.logger.warning(f"Failed to improve docstring for {function_name}: {e}")
            
            # Use template-based fallback instead of relying on model config
            return self._create_template_docstring(function_name, signature, current_docstring)
    
    def generate_test_prompts(self, function_name: str, docstring: str, signature: str) -> List[str]:
        """Generate sample test prompts for an MCP function."""
        self.logger.debug(f"Generating test prompts for function: {function_name}")
        
        # Use configurable prompt template
        model_config = self.model_config_loader.load_config()
        num_prompts = model_config.prompts.test_prompt_generation.get("num_prompts", 3)
        
        prompt = self.model_config_loader.format_prompt(
            "test_prompts",
            function_name=function_name,
            signature=signature,
            docstring=docstring,
            num_prompts=num_prompts,
            fallback=f"Generate test prompts for {function_name}"
        )
        
        try:
            response = self._generate_text(prompt)
            # Simple parsing - split by newlines and clean up
            prompts = [line.strip() for line in response.split('\n') if line.strip()]
            result = prompts[:num_prompts]  # Return configured number of prompts
            self.logger.debug(f"Generated {len(result)} test prompts for {function_name}")
            return result
        except Exception as e:
            self.logger.warning(f"Failed to generate test prompts for {function_name}: {e}")
            
            # Use configurable fallback
            fallback_template = model_config.fallback.test_prompt_template
            return [fallback_template.format(function_name=function_name)]
    
    def _generate_text(self, prompt: str) -> str:
        """Generate text using the configured model."""
        if self.config.use_local_model:
            return self._generate_with_local_model(prompt)
        else:
            return self._generate_with_api(prompt)
    
    def _generate_with_local_model(self, prompt: str) -> str:
        """Generate text using a local Hugging Face model."""
        if self._model is None or self._tokenizer is None:
            model_config = self.model_config_loader.load_config()
            
            # Use configured model name or fall back to CLI parameter
            model_name = self.config.local_model or model_config.local_model.default_model
            
            self.logger.info(f"Loading local model: {model_name}")
            self.logger.info(f"Loading model on {self.config.device}")
            
            try:
                # Get device-specific configuration
                device_config = self.model_config_loader.get_device_config(self.config.device)
                model_loading_config = model_config.local_model.model_loading.copy()
                model_loading_config.update(device_config)
                
                # Load tokenizer with configured parameters
                tokenizer_params = model_config.local_model.tokenizer_params.copy()
                self._tokenizer = AutoTokenizer.from_pretrained(model_name)
                
                # Set pad token if not already set to avoid attention mask warnings
                if self._tokenizer.pad_token is None:
                    self._tokenizer.pad_token = self._tokenizer.eos_token
                
                # Load model with device-specific configuration
                if self.config.device == "cpu":
                    self._model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        torch_dtype=getattr(torch, model_loading_config.get("torch_dtype", "float32")),
                        device_map=model_loading_config.get("device_map", {"": "cpu"}),
                        low_cpu_mem_usage=model_loading_config.get("low_cpu_mem_usage", True)
                    )
                else:
                    torch_dtype_str = model_loading_config.get("torch_dtype", "float16")
                    torch_dtype = getattr(torch, torch_dtype_str) if isinstance(torch_dtype_str, str) else torch_dtype_str
                    
                    self._model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        torch_dtype=torch_dtype,
                        low_cpu_mem_usage=model_loading_config.get("low_cpu_mem_usage", True)
                    )
                    self._model = self._model.to(self.config.device)
                
                self.logger.info(f"Using {self.config.device} device")
                self.logger.info(f"Model device: {next(self._model.parameters()).device}")
                
                # Print improving message now that model is ready
                if not self._printed_improving_message and not self.config.preserve_docstrings:
                    self.logger.info("Improving docstrings...")
                    self._printed_improving_message = True
                    
            except Exception as e:
                self.logger.error(f"Failed to load model {model_name}: {e}")
                raise
        
        try:
            # Get configurable generation parameters
            gen_params = self.model_config_loader.get_generation_params(use_local=True)
            
            # Tokenize the prompt with proper attention mask handling
            inputs = self._tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512, padding=True)
            
            # Ensure we have an attention mask
            if 'attention_mask' not in inputs:
                inputs['attention_mask'] = torch.ones_like(inputs['input_ids'])
            
            # Move to device
            inputs = {k: v.to(self.config.device) for k, v in inputs.items()}
            
            # Generate response with configurable parameters
            with torch.no_grad():
                outputs = self._model.generate(
                    inputs['input_ids'],
                    attention_mask=inputs['attention_mask'],
                    pad_token_id=self._tokenizer.eos_token_id,
                    **gen_params
                )
            
            # Decode and extract the generated part
            full_response = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            generated_text = full_response[len(prompt):].strip()
            
            self.logger.debug(f"Generated text (length: {len(generated_text)})")
            return generated_text
            
        except Exception as e:
            self.logger.error(f"Error during text generation: {e}")
            return "Error generating text"
    
    def _generate_with_api(self, prompt: str) -> str:
        """Generate text using an OpenAI-compatible API endpoint."""
        self.logger.debug("Generating text using API endpoint")
        
        try:
            import openai
            
            model_config = self.model_config_loader.load_config()
            
            # Configure OpenAI client
            client = openai.OpenAI(
                base_url=self.config.model_endpoint,
                api_key=os.getenv("OPENAI_API_KEY", "dummy-key")
            )
            
            # Get configurable generation parameters
            gen_params = self.model_config_loader.get_generation_params(use_local=False)
            request_params = model_config.api_model.request_params
            
            # Use configured model name
            model_name = model_config.api_model.default_model
            
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                timeout=request_params.get("timeout", 30),
                **gen_params
            )
            
            result = response.choices[0].message.content.strip()
            self.logger.debug(f"API generated text (length: {len(result)})")
            return result
            
        except Exception as e:
            self.logger.error(f"Error during API text generation: {e}")
            return "Error generating text with API" 