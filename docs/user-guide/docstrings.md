# Docstrings and MCP Tool Discovery

Docstrings play a critical role in the MCP (Model Context Protocol) ecosystem, serving as the primary mechanism for tool discovery and understanding. When you expose functions as MCP tools, their docstrings become the interface that other systems use to understand what your tools do, what parameters they expect, and how to use them effectively.

## The Importance of Docstrings in MCP

In the MCP protocol, docstrings are not just documentation—they are the communication bridge between your tools and the systems that use them. AI assistants, other MCP clients, and automated systems rely heavily on docstring content to:

- **Discover available tools** and understand their capabilities
- **Determine when to use each tool** based on the user's intent
- **Provide appropriate parameters** by understanding expected inputs
- **Explain results** to users by referencing the tool's purpose
- **Generate natural language descriptions** for tool selection

Without clear, comprehensive docstrings, your MCP tools become difficult to discover and use effectively. Poor docstrings can lead to tools being ignored, misused, or called with incorrect parameters.

## Docstring Requirements for MCP Tools

Effective MCP tool docstrings should include several key components:

**Function Purpose**: A clear, concise description of what the function does and when it should be used. This helps AI systems determine if the tool is appropriate for a given task.

**Parameter Descriptions**: Detailed explanations of each parameter, including their types, expected values, and any constraints or requirements. This information is crucial for proper tool invocation.

**Return Value Information**: Description of what the function returns, including the data type and any important details about the output format.

**Usage Examples**: Practical examples showing how to use the function with typical parameters. These help both AI systems and human users understand the tool's intended use.

**Error Conditions**: Information about when the function might fail or return errors, helping users understand potential issues.

## Writing Effective Docstrings

When writing docstrings for your MCP tools, follow these best practices:

**Be Specific and Descriptive**: Instead of "Processes data," write "Converts temperature values from Celsius to Fahrenheit with optional unit specification."

**Include Parameter Details**: For each parameter, explain what it represents, what values are acceptable, and any important constraints.

**Provide Context**: Explain when and why someone would use this tool, helping AI systems understand the tool's role in workflows.

**Use Clear Language**: Write in simple, direct language that both humans and AI systems can understand easily.

**Include Examples**: Show realistic usage examples that demonstrate typical use cases.

Here's an example of a well-written docstring:

```python
@mcp.tool()
def calculate_loan_payment(principal: float, annual_rate: float, years: int) -> float:
    """
    Calculate the monthly payment for a fixed-rate loan.
    
    This function computes the monthly payment amount for a loan with fixed interest
    rate and term. It's useful for financial planning, loan comparisons, and
    mortgage calculations.
    
    Args:
        principal: The loan amount in dollars (must be positive)
        annual_rate: Annual interest rate as a percentage (e.g., 5.5 for 5.5%)
        years: Loan term in years (must be between 1 and 30)
    
    Returns:
        Monthly payment amount in dollars, rounded to 2 decimal places
    
    Raises:
        ValueError: If principal is negative or years is outside valid range
    
    Example:
        >>> calculate_loan_payment(200000, 4.5, 30)
        1013.37
    """
    if principal <= 0:
        raise ValueError("Principal must be positive")
    if years < 1 or years > 30:
        raise ValueError("Years must be between 1 and 30")
    
    monthly_rate = annual_rate / 100 / 12
    num_payments = years * 12
    
    if monthly_rate == 0:
        return principal / num_payments
    
    payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    return round(payment, 2)
```

## AI-Powered Docstring Improvement

The Gradio MCP Server Builder includes an AI-powered docstring improvement feature that can enhance your existing docstrings or create new ones from scratch. This feature uses language models to analyze your function code and generate more comprehensive, clear documentation.

### How AI Improvement Works

The AI improvement process analyzes your function's:

- **Function name and signature** to understand its purpose
- **Parameter types and names** to infer expected inputs
- **Existing docstring content** (if any) to preserve important information
- **Code logic** to understand the function's behavior
- **Return values** to describe outputs accurately

The AI then generates improved docstrings that follow best practices for MCP tool discovery, including better parameter descriptions, usage examples, and clearer explanations.

### When to Use AI Improvement

AI docstring improvement is most beneficial when:

- Your existing docstrings are minimal or unclear
- You want to ensure consistency across all your tools
- You're converting existing code to MCP tools
- You want to follow MCP best practices automatically
- You have many functions that need documentation

### When to Preserve Original Docstrings

There are situations where you should keep your original docstrings:

- Your docstrings are already comprehensive and well-written
- You have specific domain knowledge that the AI might not capture
- You want to maintain exact wording for legal or compliance reasons
- You're working with sensitive or proprietary information
- You prefer to have full control over the documentation

## Model Selection for Docstring Improvement

The quality of AI-generated docstrings depends heavily on the model used. The builder supports various models, each with different strengths:

**Local Models**: Models like `HuggingFaceTB/SmolLM3-3B` run locally and provide good results for most use cases. They're fast, private, and don't require API keys.

**OpenAI-Compatible Models**: Models like GPT-3.5-turbo or GPT-4 provide excellent docstring quality but require API access and may have usage costs.

**Custom Models**: You can use specialized models trained on technical documentation for even better results in specific domains.

### Choosing the Right Model

Consider these factors when selecting a model:

**Accuracy**: Larger models generally produce more accurate and comprehensive docstrings, but they may be slower and more expensive.

**Speed**: Local models are faster but may produce less detailed results. API-based models can be slower due to network latency.

**Privacy**: Local models keep your code private, while API-based models may send your code to external servers.

**Cost**: Local models are free, while API-based models may have usage costs.

**Domain Expertise**: Some models are better at specific domains like finance, healthcare, or technical computing.

## Best Practices for Model-Generated Docstrings

When using AI improvement, follow these guidelines to ensure quality results:

**Review Generated Content**: Always review AI-generated docstrings before deploying. The AI may make mistakes or miss important details.

**Provide Context**: If your functions are part of a larger system, consider adding context about how they fit into the overall workflow.

**Test the Results**: Use the generated docstrings with MCP clients to ensure they work well for tool discovery and usage.

**Iterate and Improve**: Use the AI-generated content as a starting point and refine it based on your specific needs and domain knowledge.

**Consider Domain-Specific Models**: For specialized domains, look for models that have been trained on relevant documentation.

## Configuration Options

The builder provides several configuration options for docstring improvement:

**`--preserve-docstrings`**: Keep your original docstrings without AI improvement. This is useful when you have well-written documentation or want to maintain exact wording.

**`--local-model`**: Specify a local Hugging Face model for docstring improvement. This provides privacy and speed while still offering good quality.

**`--model-endpoint`**: Use an OpenAI-compatible API endpoint for potentially higher quality results.

**Model Configuration**: Customize the AI model's behavior through the `model_config.json` file, including parameters like temperature, max tokens, and prompt templates.

## Troubleshooting Docstring Issues

Common issues with docstrings and their solutions:

**Incorrect Parameter Descriptions**: The AI may misunderstand complex parameters. Review and manually correct parameter descriptions for accuracy.

**Missing Context**: AI-generated docstrings may lack domain-specific context. Add relevant information about when and why to use the tool.

**Overly Generic Language**: AI models sometimes produce generic descriptions. Make them more specific to your use case.

**Inconsistent Style**: When improving multiple functions, ensure consistent style and terminology across all docstrings.

**Missing Examples**: AI may not generate usage examples. Add practical examples that demonstrate typical use cases.

## Quality Assurance

To ensure your docstrings are effective for MCP tool discovery:

**Test with MCP Clients**: Use various MCP clients to test how well your tools are discovered and used.

**Review with Domain Experts**: Have subject matter experts review docstrings for accuracy and completeness.

**Validate Parameter Descriptions**: Ensure parameter descriptions match the actual function behavior.

**Check for Ambiguity**: Look for unclear or ambiguous language that might confuse AI systems or users.

**Verify Examples**: Test the examples in your docstrings to ensure they work correctly.

By following these guidelines and carefully considering when to use AI improvement versus preserving original docstrings, you can create MCP tools that are easily discoverable, well-understood, and effectively used by AI assistants and other systems in the MCP ecosystem. 