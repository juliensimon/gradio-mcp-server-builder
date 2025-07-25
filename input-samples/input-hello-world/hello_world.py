"""
Basic Hello World MCP Function

This module demonstrates a simple MCP tool function.
"""

@mcp.tool()
def greet(name: str) -> str:
    """
    Generate a friendly greeting message.

    Args:
        name: The name of the person to greet

    Returns:
        A personalized greeting message
    """
    return f"Hello, {name}! Welcome to the MCP server!"
