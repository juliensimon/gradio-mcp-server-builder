"""
Geometry Calculations Module

This module provides geometric calculation tools.
"""
import math

@mcp.tool()
def circle_area(radius: float) -> float:
    """
    Calculate the area of a circle.
    
    Args:
        radius: The radius of the circle
        
    Returns:
        The area of the circle (π * r²)
    """
    return math.pi * radius * radius

@mcp.tool()
def rectangle_area(width: float, height: float) -> float:
    """
    Calculate the area of a rectangle.
    
    Args:
        width: The width of the rectangle
        height: The height of the rectangle
        
    Returns:
        The area of the rectangle (width * height)
    """
    return width * height 