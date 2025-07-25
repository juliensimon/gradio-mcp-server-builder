# Agent Client Guide

The Gradio MCP Server Builder generates an intelligent agent client that uses the `smolagents` library to provide natural language interaction with your MCP servers. This guide explains how the agent client works, its architecture, and how to use it effectively.

## Overview

The generated agent client is more than just a simple testing tool—it's a complete conversational AI system that can understand natural language requests and automatically use your MCP tools to fulfill them. Built on the `smolagents` library, it combines a local language model with MCP tool integration to create an intelligent assistant.

## Architecture

The agent client follows a modular architecture designed for flexibility and extensibility:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gradio UI     │    │  smolagents     │    │   MCP Server    │
│   (Chat Interface) │◄──►│   Agent Engine   │◄──►│   (Your Tools)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│  Local Language │◄─────────────┘
                        │     Model       │
                        └─────────────────┘
```

### Core Components

#### 1. **Gradio Chat Interface**
The user-facing component that provides a web-based chat interface:
- **Real-time messaging**: Instant message exchange with the agent
- **Responsive design**: Works on desktop and mobile devices
- **Error handling**: Graceful display of errors and warnings
- **Example prompts**: Pre-configured examples to get users started

#### 2. **smolagents Agent Engine**
The intelligent core that processes requests and manages tool execution:
- **ToolCallingAgent**: The main agent class that orchestrates interactions
- **MCPClient**: Handles communication with your MCP server
- **Tool Discovery**: Automatically discovers available tools and their capabilities
- **Request Processing**: Converts natural language to tool calls

#### 3. **Local Language Model**
The AI brain that understands and responds to user requests:
- **TransformersModel**: Uses Hugging Face models for local inference
- **Context Understanding**: Maintains conversation context
- **Tool Selection**: Determines which tools to use for each request
- **Response Generation**: Creates natural, helpful responses

#### 4. **MCP Server Integration**
The bridge to your generated server:
- **SSE Transport**: Uses Server-Sent Events for real-time communication
- **Tool Metadata**: Extracts function names, descriptions, and parameters
- **Error Handling**: Manages server connection issues gracefully
- **Parameter Validation**: Ensures correct parameter types and values

## How It Works

### 1. **Initialization Process**

When you start the agent client, it goes through several initialization steps:

```python
# 1. Load configuration
config = load_config()  # Reads config.json for server URL and settings

# 2. Connect to MCP server
mcp_client = MCPClient({"url": server_url, "transport": "sse"})

# 3. Discover available tools
tools = mcp_client.get_tools()  # Gets all @mcp.tool() functions

# 4. Initialize language model
model = TransformersModel(
    model_id="HuggingFaceTB/SmolLM3-3B",
    device_map="auto",
    max_new_tokens=512
)

# 5. Create agent
agent = ToolCallingAgent(
    tools=tools,
    model=model,
    max_steps=3
)
```

### 2. **Request Processing Flow**

When a user sends a message, the agent processes it through these steps:

#### **Step 1: Message Reception**
The Gradio interface receives the user's message and passes it to the agent.

#### **Step 2: Natural Language Understanding**
The language model analyzes the message to understand:
- **Intent**: What the user wants to accomplish
- **Entities**: Relevant information (numbers, names, etc.)
- **Context**: How this relates to previous messages

#### **Step 3: Tool Selection**
The agent determines which tool(s) to use based on:
- **Function names**: Matches user intent to function names
- **Docstrings**: Uses function descriptions to understand capabilities
- **Parameter requirements**: Identifies what information is needed

#### **Step 4: Parameter Extraction**
The agent extracts or requests the necessary parameters:
- **Direct extraction**: Numbers, strings mentioned in the message
- **Inference**: Calculated values based on context
- **User prompting**: Requests missing information if needed

#### **Step 5: Tool Execution**
The agent calls the selected tool through the MCP client:
- **Parameter validation**: Ensures correct types and values
- **Function execution**: Runs your actual Python function
- **Result capture**: Gets the function's return value

#### **Step 6: Response Generation**
The agent creates a natural language response:
- **Result formatting**: Presents the output in a user-friendly way
- **Explanation**: Provides context about what was done
- **Follow-up**: Suggests related actions if appropriate

### 3. **Example Interaction Flow**

Here's how a typical interaction works:

```
User: "Calculate the area of a circle with radius 5"

Agent Processing:
1. Intent: Calculate area
2. Tool Selection: calculate_area function
3. Parameter Extraction: radius = 5
4. Tool Execution: calculate_area(5) → 78.54
5. Response: "The area of a circle with radius 5 is 78.54 square units."

User: "What about radius 10?"

Agent Processing:
1. Intent: Calculate area (same as before)
2. Context: Previous calculation provides context
3. Tool Selection: calculate_area function
4. Parameter Extraction: radius = 10
5. Tool Execution: calculate_area(10) → 314.16
6. Response: "The area of a circle with radius 10 is 314.16 square units."
```

## Key Features

### **Intelligent Tool Discovery**

The agent automatically discovers all available tools from your MCP server:

```python
# The agent discovers tools like this:
tools = [
    Tool(name="calculate_area", description="Calculate circle area"),
    Tool(name="add_numbers", description="Add two numbers"),
    Tool(name="greet_user", description="Greet a user by name")
]
```

### **Natural Language Processing**

The agent understands various ways to express the same request:

- "Calculate the area of a circle with radius 5"
- "What's the area for radius 5?"
- "Find the circle area when radius is 5"
- "Area of circle, radius 5"

### **Context Awareness**

The agent maintains conversation context across multiple messages:

```
User: "Calculate 10 + 5"
Agent: "10 + 5 = 15"

User: "Now multiply that by 2"
Agent: "15 * 2 = 30"  # Uses previous result as context
```

### **Error Handling**

The agent gracefully handles various error conditions:

- **Invalid parameters**: "I need a positive number for the radius"
- **Missing information**: "What radius would you like me to calculate?"
- **Server errors**: "I'm having trouble connecting to the server"
- **Tool errors**: "The calculation failed because of invalid input"

### **Multi-Step Reasoning**

For complex requests, the agent can use multiple tools in sequence:

```
User: "Calculate the area of a circle with radius 5, then add 10 to it"

Agent Processing:
1. calculate_area(5) → 78.54
2. add_numbers(78.54, 10) → 88.54
3. Response: "The area is 78.54, and adding 10 gives you 88.54"
```

## Configuration

### **Model Configuration**

You can customize the language model used by the agent:

```python
# In the generated client code
model = TransformersModel(
    model_id="HuggingFaceTB/SmolLM3-3B",  # Change this for different models
    device_map="auto",                     # CPU, CUDA, or MPS
    torch_dtype="float16",                 # Precision setting
    max_new_tokens=512,                    # Response length
    temperature=0.7,                       # Creativity level
    do_sample=True                         # Enable sampling
)
```

### **Agent Configuration**

Customize the agent's behavior:

```python
agent = ToolCallingAgent(
    tools=tools,
    model=model,
    max_steps=3,           # Maximum tool calls per request
    verbose=True,          # Show detailed processing
    temperature=0.7        # Response creativity
)
```

### **Server Configuration**

Configure the MCP server connection:

```json
{
    "mcp_sse_endpoint": "http://127.0.0.1:7860/gradio_api/mcp/sse",
    "client_port": 7861,
    "model_name": "HuggingFaceTB/SmolLM3-3B"
}
```

## Usage Patterns

### **Basic Testing**

Use the agent for basic function testing:

```
User: "Test the add function with 5 and 3"
Agent: "5 + 3 = 8"

User: "Now test with negative numbers: -2 and 7"
Agent: "-2 + 7 = 5"
```

### **Exploratory Testing**

Discover your functions' capabilities:

```
User: "What functions are available?"
Agent: "I can help you with: calculate_area, add_numbers, greet_user, multiply_numbers"

User: "Tell me about the calculate_area function"
Agent: "The calculate_area function calculates the area of a circle. It takes a radius parameter and returns the area in square units."
```

### **Complex Workflows**

Test multi-step processes:

```
User: "Calculate the area of a circle with radius 3, then multiply it by 2"
Agent: "The area of a circle with radius 3 is 28.27 square units. Multiplying by 2 gives you 56.55 square units."
```

### **Error Testing**

Test error conditions:

```
User: "Calculate area with radius -5"
Agent: "I can't calculate the area with a negative radius. Please provide a positive number."

User: "Calculate area without radius"
Agent: "I need a radius value to calculate the area. What radius would you like me to use?"
```

## Customization

### **Modifying the Agent**

You can customize the generated agent client:

```python
# Add custom error handling
def custom_error_handler(error):
    return f"Custom error message: {error}"

# Add custom response formatting
def format_response(result, tool_name):
    return f"Result from {tool_name}: {result}"

# Modify the agent creation
agent = ToolCallingAgent(
    tools=tools,
    model=model,
    error_handler=custom_error_handler,
    response_formatter=format_response
)
```

### **Adding Custom Tools**

Extend the agent with additional capabilities:

```python
# Add a custom tool
@mcp.tool()
def custom_helper(data: str) -> str:
    """A custom helper function."""
    return f"Processed: {data}"

# The agent will automatically discover and use this tool
```

### **UI Customization**

Modify the Gradio interface:

```python
# Custom CSS for styling
css = """
.custom-container {
    max-width: 1000px !important;
    margin: auto !important;
}
"""

# Custom theme
demo = gr.ChatInterface(
    fn=chat_fn,
    theme=gr.themes.Soft(),
    css=css,
    title="My Custom Agent"
)
```

## Troubleshooting

### **Common Issues**

#### **Connection Problems**
```
Error: Failed to connect to MCP server
Solution: Ensure your MCP server is running on the correct port
```

#### **Model Loading Issues**
```
Error: Failed to load language model
Solution: Check internet connection for model download, or use a local model
```

#### **Tool Discovery Problems**
```
Error: No tools found
Solution: Verify your MCP server has @mcp.tool() decorated functions
```

#### **Parameter Issues**
```
Error: Invalid parameter type
Solution: Check that your function parameters match the expected types
```

### **Performance Optimization**

#### **Model Selection**
- **Small models**: Faster but less accurate (SmolLM3-3B)
- **Large models**: More accurate but slower (Llama-2-7B)
- **Local vs. Remote**: Local models for privacy, remote for performance

#### **Device Optimization**
```python
# Use GPU if available
device_map = "cuda" if torch.cuda.is_available() else "cpu"

# Use MPS on Mac
device_map = "mps" if torch.backends.mps.is_available() else "cpu"
```

#### **Memory Management**
```python
# Reduce memory usage
torch_dtype = "float16"  # Use half precision
max_new_tokens = 256     # Limit response length
```

## Best Practices

### **Writing Tool-Friendly Functions**

Design your functions to work well with the agent:

```python
@mcp.tool()
def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle.
    
    Args:
        radius: The radius of the circle (must be positive)
    
    Returns:
        The area of the circle in square units
    """
    if radius <= 0:
        raise ValueError("Radius must be positive")
    return math.pi * radius ** 2
```

### **Providing Good Docstrings**

Clear docstrings help the agent understand your functions:

```python
@mcp.tool()
def process_data(data: dict, operation: str = "sum") -> dict:
    """
    Process numerical data with various operations.
    
    This function can perform different mathematical operations on the values
    in the provided data dictionary. Supported operations include sum, average,
    min, and max.
    
    Args:
        data: Dictionary containing numerical values
        operation: The operation to perform (sum, average, min, max)
    
    Returns:
        Dictionary with the operation result and processed data
    """
    # Function implementation
```

### **Error Handling**

Implement robust error handling:

```python
@mcp.tool()
def safe_divide(a: float, b: float) -> float:
    """
    Safely divide two numbers.
    
    Args:
        a: The numerator
        b: The denominator (must not be zero)
    
    Returns:
        The result of a divided by b
    
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## Conclusion

The agent client provides a powerful, intelligent interface to your MCP servers. By understanding how it works, you can:

- **Test your functions effectively** through natural language
- **Discover edge cases** through conversational exploration
- **Demonstrate your tools** to users and stakeholders
- **Debug issues** with interactive testing
- **Extend functionality** through customization

The combination of local AI processing, MCP tool integration, and natural language interface makes the agent client a valuable tool for development, testing, and demonstration of your MCP servers.

For more information about specific aspects of the agent client, refer to the smolagents documentation or explore the generated client code in your output directory. 